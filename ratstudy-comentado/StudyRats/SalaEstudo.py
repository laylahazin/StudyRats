from datetime import datetime, timedelta  # converte horários de sala e calcula datas de sessões

import lista  # fornece salas disponíveis, contas cadastradas e o Ratname conectado
from Horario import obter_horario_atual  # obtém o relógio real ou manual configurado para os testes
from Persistencia import carregar_json, salvar_json  # carrega e grava as participações das salas em JSON


ARQUIVO_PARTICIPANTES = "participantes_salas.json"  # identifica o arquivo que guarda sessões, participantes e dúvidas


def _intervalo_sessao(sala, agora):  # calcula os limites da sessão recorrente e informa se ela está ativa
    inicio_hora = datetime.strptime(sala["inicio"], "%H:%M").time()  # converte a hora de abertura configurada para um objeto time
    fim_hora = datetime.strptime(sala["fim"], "%H:%M").time()  # converte a hora de encerramento configurada para um objeto time
    atravessa_meia_noite = fim_hora <= inicio_hora  # detecta sessões que terminam no dia seguinte ao dia de início

    if atravessa_meia_noite and agora.time() < fim_hora:  # identifica a parte da sessão que ocorre depois da meia-noite
        data_inicio = agora.date() - timedelta(days=1)  # associa o horário atual à sessão iniciada no dia anterior
    else:  # usa a data atual quando a sessão começou hoje ou ainda não atravessou a meia-noite
        data_inicio = agora.date()  # define hoje como a data de início da sessão

    inicio = datetime.combine(data_inicio, inicio_hora)  # combina o dia correto com a hora de abertura
    data_fim = data_inicio + timedelta(days=1) if atravessa_meia_noite else data_inicio  # avança um dia apenas se a sala passar da meia-noite
    fim = datetime.combine(data_fim, fim_hora)  # combina a data final com a hora de encerramento
    ativo = inicio <= agora < fim  # considera ativa a sessão desde a abertura até antes do horário final
    return inicio, fim, ativo  # devolve os limites calculados e o estado da sala neste instante


def _chave_sessao(inicio):  # cria uma chave estável que identifica a ocorrência diária de uma sala
    return inicio.isoformat(timespec="minutes")  # serializa a abertura em formato ISO até o minuto para indexar os dados


def _carregar_participacoes(agora):  # carrega os dados das salas e remove sessões já encerradas
    participacoes = carregar_json(ARQUIVO_PARTICIPANTES, {})  # recupera o objeto salvo ou usa um objeto vazio na primeira execução
    if not isinstance(participacoes, dict):  # verifica que o JSON está indexado por identificador de sala
        raise ValueError("O arquivo de participantes deve conter um objeto JSON.")  # relata dados incompatíveis sem substituí-los

    alterado = False  # registra se alguma sessão vencida foi removida e precisa ser salva
    for sala_id in list(participacoes):  # percorre uma cópia das chaves para permitir remover salas do objeto
        sessoes = participacoes[sala_id]  # obtém as ocorrências registradas para esta sala
        if not isinstance(sessoes, dict):  # valida que as ocorrências estejam indexadas por sessão
            raise ValueError(f"As sessões da sala '{sala_id}' estão inválidas.")  # informa qual sala contém dados no formato incorreto
        for chave in list(sessoes):  # percorre uma cópia das sessões para permitir sua remoção segura
            sessao = sessoes[chave]  # obtém os detalhes da ocorrência que será validada
            fim_texto = sessao.get("fim") if isinstance(sessao, dict) else None  # extrai o horário final somente se a sessão for um objeto
            if not isinstance(fim_texto, str):  # exige uma data final serializada para identificar expiração
                raise ValueError(f"A sessão '{chave}' da sala '{sala_id}' está inválida.")  # aponta a sessão que não pode ser interpretada
            try:  # tenta converter a data ISO armazenada para comparar com o relógio atual
                fim = datetime.fromisoformat(fim_texto)  # converte o horário final em objeto datetime
            except ValueError as erro:  # captura textos que não representam data/hora ISO válida
                raise ValueError(f"O horário final da sessão '{chave}' está inválido.") from erro  # preserva a causa e identifica a sessão incorreta
            if fim <= agora:  # identifica uma sessão cujo horário já terminou
                del sessoes[chave]  # remove a ocorrência vencida junto com seus participantes e dúvidas
                alterado = True  # marca que os dados em memória diferem do arquivo persistido
        if not sessoes:  # verifica se a sala ficou sem ocorrências após a limpeza
            del participacoes[sala_id]  # remove a entrada vazia para não manter salas sem sessão registrada
            alterado = True  # marca também esta remoção para persistir o resultado

    if alterado:  # evita gravar novamente o arquivo quando nada foi removido
        salvar_json(ARQUIVO_PARTICIPANTES, participacoes)  # persiste somente quando sessões expiradas foram descartadas
    return participacoes  # devolve os registros válidos para as rotinas chamadoras


def limpar_sessoes_expiradas():  # remove registros de sala cujo horário terminou antes do início da aplicação
    _carregar_participacoes(obter_horario_atual())  # usa o relógio configurado para limpar participações antigas


def _obter_sessao(participacoes, sala, inicio, fim):  # obtém os dados de uma ocorrência ou cria seu registro inicial
    sessoes_sala = participacoes.setdefault(sala["id"], {})  # cria um dicionário para a sala se ela ainda não tiver sessões
    chave = _chave_sessao(inicio)  # calcula a chave baseada no horário de abertura desta ocorrência diária
    sessao = sessoes_sala.get(chave)  # procura uma ocorrência criada anteriormente para o mesmo início
    if sessao is None:  # cria estrutura inicial somente quando ainda não existe registro para esta sessão
        sessao = {"fim": fim.isoformat(timespec="minutes"), "participantes": {}, "duvidas": []}  # guarda encerramento, participantes únicos e dúvidas recebidas
        sessoes_sala[chave] = sessao  # associa os dados novos à chave desta sessão
    return sessao  # devolve a estrutura existente ou recém-criada


def _contar_participantes_ativos(participantes):  # conta somente usuários que ainda estão dentro da sala
    return sum(  # soma os resultados booleanos da verificação de atividade de cada usuário
        participante["inicio_atividade"] is not None  # considera ativo quem possui um período de atividade em andamento
        for participante in participantes.values()  # percorre os registros preservados nesta ocorrência
    )  # devolve a quantidade de participantes atualmente ativos


def listar_salas():  # mostra horários, ocupação e situação atual de cada sala cadastrada
    agora = obter_horario_atual()  # usa o relógio comum do programa para avaliar horários das salas
    participacoes = _carregar_participacoes(agora)  # carrega participações e elimina registros vencidos
    print(f"\n=== SALAS DE ESTUDO | {agora:%d/%m/%Y %H:%M} ===")  # informa a data e hora usadas para calcular os estados

    if not lista.salas_disponiveis:  # verifica se há salas configuradas para exibir
        print("Nenhuma sala de estudo disponível no momento.")  # informa que a lista de salas está vazia
        return  # não continua para o laço de exibição

    for indice, sala in enumerate(lista.salas_disponiveis, start=1):  # percorre as salas e cria numeração iniciada em 1 para a seleção
        inicio, fim, ativo = _intervalo_sessao(sala, agora)  # calcula o período de funcionamento e se a sala está aberta
        sessao = _obter_sessao(participacoes, sala, inicio, fim)  # obtém a ocorrência do dia para contar ocupação atual
        participantes = sessao["participantes"]  # recupera participantes já registrados nesta ocorrência
        quantidade_ativos = _contar_participantes_ativos(participantes)  # ignora quem saiu e conserva apenas a ocupação atual
        vagas = sala["capacidade"] - quantidade_ativos  # subtrai a ocupação atual da capacidade máxima

        if not sala["ativa"] or (ativo and vagas <= 0):  # identifica sala desativada ou sala aberta sem vagas livres
            status = "Lotada" if sala["ativa"] else "Indisponível"  # distingue capacidade esgotada de sala desativada
        elif ativo:  # verifica se a sala está aberta e ainda tem vagas
            status = "Em andamento"  # indica que a sessão pode receber participantes
        else:  # cobre salas ativas cujo horário não está ocorrendo agora
            status = "Fora do horário"  # informa que a entrada ainda não está liberada ou já terminou

        print(  # monta uma linha resumida com os dados mais úteis para escolher uma sala
            f"{indice}. {sala['nome']} | Matéria: {sala['materia']} | "  # identifica a opção e sua disciplina
            f"Horário: {sala['inicio']} - {sala['fim']} | "  # mostra o período diário configurado
            f"Monitor: {sala['monitor']} | Participantes: "  # identifica o monitor e inicia a contagem de participantes
            f"{quantidade_ativos}/{sala['capacidade']} | Status: {status}"  # informa usuários presentes agora e a capacidade máxima
        )  # conclui a linha informativa da sala

    print("0. Voltar ao menu principal")  # reserva a opção zero para cancelar a seleção de sala


def exibir_sala_de_estudo():  # controla a seleção da sala, o ingresso do usuário e as interações durante a sessão
    if lista.usuario_logado is None:  # impede a participação de quem ainda não se autenticou
        print("\nVocê precisa fazer login para acessar as salas de estudo.")  # informa que a funcionalidade exige login
        return  # retorna ao menu sem acessar participações

    if not any(  # procura uma conta persistida correspondente ao usuário marcado como conectado
        usuario["ratname"] == lista.usuario_logado  # compara o Ratname da conta atual com o estado da sessão
        for usuario in lista.usuarios  # percorre as contas carregadas do arquivo de usuários
    ):  # conclui a busca booleana pelas contas cadastradas
        raise ValueError("O usuário conectado não existe na lista persistida de contas.")  # aponta inconsistência entre sessão e dados persistidos

    listar_salas()  # exibe opções e situação atual antes de solicitar uma escolha
    escolha = input("\nEscolha uma sala para entrar (ou 0 para voltar): ").strip()  # lê a opção e remove espaços externos
    if not escolha.isdigit():  # aceita apenas algarismos antes de converter a escolha para inteiro
        print("Opção inválida.")  # informa que a entrada não representa um número de sala
        return  # cancela esta tentativa e retorna ao menu principal

    escolha = int(escolha)  # converte a opção validada de texto para número inteiro
    if escolha == 0:  # interpreta zero como cancelamento da seleção de sala
        return  # retorna sem iniciar participação
    if escolha < 1 or escolha > len(lista.salas_disponiveis):  # verifica se o número está dentro dos índices exibidos no menu
        print("Sala inválida. Tente novamente.")  # informa que não existe sala com essa opção
        return  # encerra a tentativa em vez de acessar um índice inválido

    sala = lista.salas_disponiveis[escolha - 1]  # traduz a numeração iniciada em 1 para o índice iniciado em 0 da lista
    agora = obter_horario_atual()  # obtém o relógio configurado para validar o horário da sala
    inicio, fim, ativo = _intervalo_sessao(sala, agora)  # calcula os limites da ocorrência e confirma se está aberta
    participacoes = _carregar_participacoes(agora)  # carrega participações e limpa ocorrências que já terminaram
    sessao = _obter_sessao(participacoes, sala, inicio, fim)  # recupera os dados desta ocorrência diária da sala
    participantes = sessao["participantes"]  # obtém o mapa de Ratnames já inscritos na sessão
    ratname = lista.usuario_logado  # guarda o identificador da conta que pretende entrar
    ja_esta_ativo = (  # verifica se este usuário já está contado entre os ocupantes atuais da sala
        ratname in participantes  # exige que exista um registro de participação nesta ocorrência
        and participantes[ratname]["inicio_atividade"] is not None  # confirma que o período ativo ainda não foi encerrado
    )  # conclui a verificação da presença atual

    quantidade_ativos = _contar_participantes_ativos(participantes)  # conta ocupantes atuais sem incluir participantes que já saíram
    vagas = sala["capacidade"] - quantidade_ativos  # calcula as vagas usando apenas pessoas que permanecem na sala
    if not sala["ativa"] or not ativo:  # bloqueia salas desativadas ou acessos fora do horário configurado
        print(  # explica a indisponibilidade e apresenta o período previsto
            f"\nA sala '{sala['nome']}' só permite entrada entre "  # identifica a sala que não pode ser acessada agora
            f"{sala['inicio']} e {sala['fim']} (horário considerado: {agora:%H:%M})."  # informa horário de abertura, fechamento e hora avaliada
        )  # finaliza a mensagem que explica o motivo do bloqueio
        return  # impede entrada fora do horário permitido
    if vagas <= 0 and not ja_esta_ativo:  # impede nova entrada quando a capacidade de participantes ativos está esgotada
        print(f"\nA sala '{sala['nome']}' atingiu o limite de participantes.")  # informa que não há vagas disponíveis
        return  # não altera o registro de participantes

    print(f"\n=== {sala['nome']} ===")  # apresenta o título da sala escolhida
    print(f"Matéria: {sala['materia']}")  # apresenta a disciplina associada à sala
    print(f"Descrição: {sala['descricao']}")  # apresenta as atividades previstas para a sessão
    print(f"Monitor responsável: {sala['monitor']}")  # informa quem acompanha a sala
    print(f"Horário: {sala['inicio']} - {sala['fim']}")  # apresenta a janela diária de funcionamento
    print(f"Participantes: {quantidade_ativos}/{sala['capacidade']}")  # mostra quantas pessoas estão na sala e seu limite total

    entrar = input('\nDigite "entrar" para participar desta sala: ').strip().lower()  # solicita confirmação e normaliza a palavra digitada
    if entrar != "entrar":  # verifica se a pessoa confirmou a entrada explicitamente
        print("Você decidiu não entrar na sala de estudos.")  # confirma que nenhuma entrada foi registrada
        return  # retorna ao menu sem alterar a sessão

    agora = obter_horario_atual()  # atualiza a hora para não confiar na validação feita antes da confirmação
    inicio, fim, ativo = _intervalo_sessao(sala, agora)  # recalcula a janela porque o tempo pode ter passado
    if not ativo:  # verifica se a sala continua aberta no momento da confirmação
        print("O horário da sala terminou antes da confirmação da entrada.")  # informa que a entrada não foi aceita por encerramento da sessão
        return  # interrompe antes de alterar a lista de participantes

    participacoes = _carregar_participacoes(agora)  # recarrega os dados para validar a ocupação mais recente
    sessao = _obter_sessao(participacoes, sala, inicio, fim)  # recupera novamente a ocorrência que será atualizada
    participantes = sessao["participantes"]  # obtém a contagem atualizada de Ratnames nesta ocorrência
    ja_esta_ativo = (  # atualiza a presença do usuário antes de aplicar novamente o limite
        ratname in participantes  # verifica se já existe registro para esta conta
        and participantes[ratname]["inicio_atividade"] is not None  # verifica se ela continua ativa na sala
    )  # conclui a verificação atualizada de presença
    quantidade_ativos = _contar_participantes_ativos(participantes)  # recalcula a ocupação depois de carregar novamente os dados
    if quantidade_ativos >= sala["capacidade"] and not ja_esta_ativo:  # barra a entrada se usuários ativos já preencheram a capacidade
        print(f"\nA sala '{sala['nome']}' atingiu o limite de participantes.")  # avisa quando outra entrada ocupou a última vaga
        return  # cancela a entrada para manter o limite da sala

    participante = participantes.get(ratname)  # procura o registro existente para evitar duplicar o mesmo usuário
    if participante is None:  # cria os dados da pessoa apenas na primeira entrada nesta ocorrência
        participante = {  # inicia o registro individual que será persistido para este Ratname
            "email": next(  # procura o e-mail cadastrado associado ao identificador conectado
                usuario["email"]  # seleciona o endereço da conta correspondente
                for usuario in lista.usuarios  # examina as contas carregadas no sistema
                if usuario["ratname"] == ratname  # limita o resultado à conta que está entrando na sala
            ),  # conclui a busca pelo e-mail do usuário
            "primeira_entrada": agora.isoformat(timespec="seconds"),  # registra quando o usuário entrou pela primeira vez nesta sessão
            "inicio_atividade": agora.isoformat(timespec="seconds"),  # inicia a medição do período ativo atual
            "tempo_total_segundos": 0,  # começa o acumulador de tempo da sessão sem duração anterior
        }  # conclui a estrutura inicial do participante
        participantes[ratname] = participante  # indexa o registro pelo Ratname para impedir duplicação e facilitar consulta
    elif participante["inicio_atividade"] is None:  # retoma o contador se o participante havia saído e voltou
        participante["inicio_atividade"] = agora.isoformat(timespec="seconds")  # marca o instante inicial do novo período ativo

    salvar_json(ARQUIVO_PARTICIPANTES, participacoes)  # persiste a entrada antes de abrir as opções interativas
    print(f"\n{ratname}, você entrou na sala '{sala['nome']}' com sucesso!")  # confirma qual usuário entrou em qual sala
    print("Você pode acompanhar a resolução de questões, enviar dúvidas e participar da discussão.")  # resume as ações disponíveis durante a participação

    while True:  # mantém o usuário na sala até sair ou chegar ao encerramento do horário
        print("\nOpções da sala:")  # introduz as ações específicas desta sala
        print("1. Ver atividades da sala")  # oferece consultar a descrição das atividades
        print("2. Enviar dúvida")  # oferece enviar uma mensagem para o monitor
        print("3. Participar da discussão")  # oferece registrar participação na discussão
        print("4. Sair da sala")  # oferece encerrar a participação antes do fim do horário

        opcao = input("Escolha uma opção: ").strip()  # lê a ação escolhida e remove espaços externos
        agora = obter_horario_atual()  # atualiza a hora para verificar se a sessão continua aberta
        if agora >= fim:  # encerra o fluxo quando o relógio alcança o limite da sala
            _finalizar_atividade(participante, fim)  # soma o último período ativo até o horário oficial de encerramento
            _carregar_participacoes(agora)  # remove os dados da sessão agora expirada do arquivo persistido
            print("\nO horário da sala terminou. Sua participação foi registrada.")  # confirma que a atividade foi finalizada
            return  # sai da sala e retorna ao menu principal

        if opcao == "1":  # reconhece o pedido para consultar as atividades
            print(f"\nAtividades da sala: {sala['descricao']}")  # reapresenta a descrição cadastrada para esta sala
        elif opcao == "2":  # reconhece o pedido para enviar uma dúvida
            duvida = input("Digite sua dúvida para o monitor: ").strip()  # lê a mensagem e remove espaços externos
            agora = obter_horario_atual()  # verifica novamente o horário após a digitação da mensagem
            if agora >= fim:  # impede envio de dúvidas depois que a sala fechou
                _finalizar_atividade(participante, fim)  # contabiliza o tempo até o limite final da sessão
                _carregar_participacoes(agora)  # remove a ocorrência encerrada e seus dados associados
                print("\nO horário da sala terminou. Sua participação foi registrada.")  # avisa que a sessão terminou durante a digitação
                return  # encerra a participação depois do término do horário
            if duvida:  # salva somente mensagens que contenham algum texto
                participacoes = carregar_json(ARQUIVO_PARTICIPANTES, {})  # recarrega os registros mais recentes antes de alterar a sessão
                sessao = participacoes[sala["id"]][_chave_sessao(inicio)]  # localiza a ocorrência exata da sala em que o usuário entrou
                sessao["duvidas"].append(  # acrescenta a pergunta ao histórico de dúvidas da sessão
                    {  # inicia o registro individual da dúvida
                        "usuario": ratname,  # guarda o Ratname de quem enviou a mensagem
                        "mensagem": duvida,  # guarda o conteúdo escrito pelo participante
                        "horario": agora.isoformat(timespec="seconds"),  # registra quando a pergunta foi enviada
                    }  # conclui os dados da dúvida
                )  # termina o acréscimo da dúvida à lista da sessão
                salvar_json(ARQUIVO_PARTICIPANTES, participacoes)  # persiste o histórico de dúvidas atualizado
                print("Sua dúvida foi enviada ao monitor.")  # confirma que a mensagem foi salva
            else:  # trata a tentativa de enviar uma mensagem vazia
                print("Você precisa escrever uma dúvida antes de enviar.")  # pede que o usuário digite conteúdo antes de enviar
        elif opcao == "3":  # reconhece a opção de participar da discussão
            print(f"{ratname} participou da discussão da sala.")  # informa a participação no terminal
        elif opcao == "4":  # reconhece o pedido de saída voluntária da sala
            agora = obter_horario_atual()  # captura o horário exato em que o usuário saiu
            _finalizar_atividade(participante, agora)  # acumula o tempo ativo desde o início ou retorno mais recente
            participacoes = carregar_json(ARQUIVO_PARTICIPANTES, {})  # carrega os dados atualizados antes de gravar o participante
            sessao = participacoes[sala["id"]][_chave_sessao(inicio)]  # localiza a sessão diária correta da sala
            sessao["participantes"][ratname] = participante  # atualiza o registro deste Ratname com o tempo acumulado
            salvar_json(ARQUIVO_PARTICIPANTES, participacoes)  # persiste a saída sem liberar a vaga antes do fim da sessão

            tempo_total = participante["tempo_total_segundos"]  # recupera o total somado nos períodos ativos desta pessoa
            horas, resto = divmod(tempo_total, 3600)  # separa horas completas dos segundos restantes
            minutos, segundos = divmod(resto, 60)  # converte o restante em minutos completos e segundos finais
            print(f"\nVocê saiu da sala '{sala['nome']}' com sucesso.")  # confirma o encerramento voluntário da participação
            print(f"Tempo ativo nesta sessão: {horas}h {minutos}m {segundos}s")  # mostra a duração total em formato de relógio
            print("Sua vaga foi liberada. O histórico da sessão permanece salvo até o horário da sala acabar.")  # confirma que saiu sem apagar o tempo já acumulado
            return  # encerra o fluxo da sala e retorna ao menu
        else:  # trata valores que não correspondem a nenhuma ação da sala
            print("Opção inválida. Tente novamente.")  # pede uma opção válida e mantém a sessão aberta


def _finalizar_atividade(participante, horario_fim):  # acumula o tempo do período ativo que acabou de terminar
    inicio_atividade = participante["inicio_atividade"]  # recupera o início do período ainda não contabilizado
    if inicio_atividade is None:  # verifica se não há período ativo para finalizar
        return  # evita somar novamente um intervalo já contabilizado

    inicio = datetime.fromisoformat(inicio_atividade)  # converte o início ISO salvo em data/hora para subtrair do fim
    segundos = max(0, int((horario_fim - inicio).total_seconds()))  # calcula o intervalo em segundos e impede valores negativos
    participante["tempo_total_segundos"] += segundos  # soma o intervalo ao total já acumulado nesta sala
    participante["inicio_atividade"] = None  # marca o período como encerrado para não contabilizá-lo duas vezes
