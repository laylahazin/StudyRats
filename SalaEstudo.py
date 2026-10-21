from datetime import datetime, timedelta  

import lista  
from Horario import obter_horario_atual  
from Persistencia import carregar_json, salvar_json  


ARQUIVO_PARTICIPANTES = "participantes_salas.json"  


def _intervalo_sessao(sala, agora):  
    inicio_hora = datetime.strptime(sala["inicio"], "%H:%M").time()  
    fim_hora = datetime.strptime(sala["fim"], "%H:%M").time()  
    atravessa_meia_noite = fim_hora <= inicio_hora  

    if atravessa_meia_noite and agora.time() < fim_hora:  
        data_inicio = agora.date() - timedelta(days=1)  
    else:  
        data_inicio = agora.date()  

    inicio = datetime.combine(data_inicio, inicio_hora)  
    data_fim = data_inicio + timedelta(days=1) if atravessa_meia_noite else data_inicio  
    fim = datetime.combine(data_fim, fim_hora)  
    ativo = inicio <= agora < fim  
    return inicio, fim, ativo  


def _chave_sessao(inicio):  
    return inicio.isoformat(timespec="minutes")  


def _carregar_participacoes(agora):  
    participacoes = carregar_json(ARQUIVO_PARTICIPANTES, {})  
    if not isinstance(participacoes, dict):  
        raise ValueError("O arquivo de participantes deve conter um objeto JSON.")  

    alterado = False  
    for sala_id in list(participacoes):  
        sessoes = participacoes[sala_id]  
        if not isinstance(sessoes, dict):  
            raise ValueError(f"As sessões da sala '{sala_id}' estão inválidas.")  
        for chave in list(sessoes):  
            sessao = sessoes[chave]  
            fim_texto = sessao.get("fim") if isinstance(sessao, dict) else None  
            if not isinstance(fim_texto, str):  
                raise ValueError(f"A sessão '{chave}' da sala '{sala_id}' está inválida.")  
            try:  
                fim = datetime.fromisoformat(fim_texto)  
            except ValueError as erro:  
                raise ValueError(f"O horário final da sessão '{chave}' está inválido.") from erro  
            if fim <= agora:  
                del sessoes[chave]  
                alterado = True  
        if not sessoes:  
            del participacoes[sala_id]  
            alterado = True  

    if alterado:  
        salvar_json(ARQUIVO_PARTICIPANTES, participacoes)  
    return participacoes  


def limpar_sessoes_expiradas():  
    _carregar_participacoes(obter_horario_atual())  


def _obter_sessao(participacoes, sala, inicio, fim):  
    sessoes_sala = participacoes.setdefault(sala["id"], {})  
    chave = _chave_sessao(inicio)  
    sessao = sessoes_sala.get(chave)  
    if sessao is None:  
        sessao = {"fim": fim.isoformat(timespec="minutes"), "participantes": {}, "duvidas": []}  
        sessoes_sala[chave] = sessao  
    return sessao  


def _contar_participantes_ativos(participantes):  
    return sum(  
        participante["inicio_atividade"] is not None  
        for participante in participantes.values()  
    )  


def listar_salas():  
    agora = obter_horario_atual()  
    participacoes = _carregar_participacoes(agora)  
    print(f"\n=== SALAS DE ESTUDO | {agora:%d/%m/%Y %H:%M} ===")  

    if not lista.salas_disponiveis:  
        print("Nenhuma sala de estudo disponível no momento.")  
        return  

    for indice, sala in enumerate(lista.salas_disponiveis, start=1):  
        inicio, fim, ativo = _intervalo_sessao(sala, agora)  
        sessao = _obter_sessao(participacoes, sala, inicio, fim)  
        participantes = sessao["participantes"]  
        quantidade_ativos = _contar_participantes_ativos(participantes)  
        vagas = sala["capacidade"] - quantidade_ativos  

        if not sala["ativa"] or (ativo and vagas <= 0):  
            status = "Lotada" if sala["ativa"] else "Indisponível"  
        elif ativo:  
            status = "Em andamento"  
        else:  
            status = "Fora do horário"  

        print(  
            f"{indice}. {sala['nome']} | Matéria: {sala['materia']} | "  
            f"Horário: {sala['inicio']} - {sala['fim']} | "  
            f"Monitor: {sala['monitor']} | Participantes: "  
            f"{quantidade_ativos}/{sala['capacidade']} | Status: {status}"  
        )  

    print("0. Voltar ao menu principal")  


def exibir_sala_de_estudo():  
    if lista.usuario_logado is None:  
        print("\nVocê precisa fazer login para acessar as salas de estudo.")  
        return  

    if not any(  
        usuario["ratname"] == lista.usuario_logado  
        for usuario in lista.usuarios  
    ):  
        raise ValueError("O usuário conectado não existe na lista persistida de contas.")  

    listar_salas()  
    escolha = input("\nEscolha uma sala para entrar (ou 0 para voltar): ").strip()  
    if not escolha.isdigit():  
        print("Opção inválida.")  
        return  

    escolha = int(escolha)  
    if escolha == 0:  
        return  
    if escolha < 1 or escolha > len(lista.salas_disponiveis):  
        print("Sala inválida. Tente novamente.")  
        return  

    sala = lista.salas_disponiveis[escolha - 1]  
    agora = obter_horario_atual()  
    inicio, fim, ativo = _intervalo_sessao(sala, agora)  
    participacoes = _carregar_participacoes(agora)  
    sessao = _obter_sessao(participacoes, sala, inicio, fim)  
    participantes = sessao["participantes"]  
    ratname = lista.usuario_logado  
    ja_esta_ativo = (  
        ratname in participantes  
        and participantes[ratname]["inicio_atividade"] is not None  
    )  

    quantidade_ativos = _contar_participantes_ativos(participantes)  
    vagas = sala["capacidade"] - quantidade_ativos  
    if not sala["ativa"] or not ativo:  
        print(  
            f"\nA sala '{sala['nome']}' só permite entrada entre "  
            f"{sala['inicio']} e {sala['fim']} (horário considerado: {agora:%H:%M})."  
        )  
        return  
    if vagas <= 0 and not ja_esta_ativo:  
        print(f"\nA sala '{sala['nome']}' atingiu o limite de participantes.")  
        return  

    print(f"\n=== {sala['nome']} ===")  
    print(f"Matéria: {sala['materia']}")  
    print(f"Descrição: {sala['descricao']}")  
    print(f"Monitor responsável: {sala['monitor']}")  
    print(f"Horário: {sala['inicio']} - {sala['fim']}")  
    print(f"Participantes: {quantidade_ativos}/{sala['capacidade']}")  

    entrar = input('\nDigite "entrar" para participar desta sala: ').strip().lower()  
    if entrar != "entrar":  
        print("Você decidiu não entrar na sala de estudos.")  
        return  

    agora = obter_horario_atual()  
    inicio, fim, ativo = _intervalo_sessao(sala, agora)  
    if not ativo:  
        print("O horário da sala terminou antes da confirmação da entrada.")  
        return  

    participacoes = _carregar_participacoes(agora)  
    sessao = _obter_sessao(participacoes, sala, inicio, fim)  
    participantes = sessao["participantes"]  
    ja_esta_ativo = (  
        ratname in participantes  
        and participantes[ratname]["inicio_atividade"] is not None  
    )  
    quantidade_ativos = _contar_participantes_ativos(participantes)  
    if quantidade_ativos >= sala["capacidade"] and not ja_esta_ativo:  
        print(f"\nA sala '{sala['nome']}' atingiu o limite de participantes.")  
        return  

    participante = participantes.get(ratname)  
    if participante is None:  
        participante = {  
            "email": next(  
                usuario["email"]  
                for usuario in lista.usuarios  
                if usuario["ratname"] == ratname  
            ),  
            "primeira_entrada": agora.isoformat(timespec="seconds"),  
            "inicio_atividade": agora.isoformat(timespec="seconds"),  
            "tempo_total_segundos": 0,  
        }  
        participantes[ratname] = participante  
    elif participante["inicio_atividade"] is None:  
        participante["inicio_atividade"] = agora.isoformat(timespec="seconds")  

    salvar_json(ARQUIVO_PARTICIPANTES, participacoes)  
    print(f"\n{ratname}, você entrou na sala '{sala['nome']}' com sucesso!")  
    print("Você pode acompanhar a resolução de questões, enviar dúvidas e participar da discussão.")  

    while True:  
        print("\nOpções da sala:")  
        print("1. Ver atividades da sala")  
        print("2. Enviar dúvida")  
        print("3. Participar da discussão")  
        print("4. Sair da sala")  

        opcao = input("Escolha uma opção: ").strip()  
        agora = obter_horario_atual()  
        if agora >= fim:  
            _finalizar_atividade(participante, fim)  
            _carregar_participacoes(agora)  
            print("\nO horário da sala terminou. Sua participação foi registrada.")  
            return  

        if opcao == "1":  
            print(f"\nAtividades da sala: {sala['descricao']}")  
        elif opcao == "2":  
            duvida = input("Digite sua dúvida para o monitor: ").strip()  
            agora = obter_horario_atual()  
            if agora >= fim:  
                _finalizar_atividade(participante, fim)  
                _carregar_participacoes(agora)  
                print("\nO horário da sala terminou. Sua participação foi registrada.")  
                return  
            if duvida:  
                participacoes = carregar_json(ARQUIVO_PARTICIPANTES, {})  
                sessao = participacoes[sala["id"]][_chave_sessao(inicio)]  
                sessao["duvidas"].append(  
                    {  
                        "usuario": ratname,  
                        "mensagem": duvida,  
                        "horario": agora.isoformat(timespec="seconds"),  
                    }  
                )  
                salvar_json(ARQUIVO_PARTICIPANTES, participacoes)  
                print("Sua dúvida foi enviada ao monitor.")  
            else:  
                print("Você precisa escrever uma dúvida antes de enviar.")  
        elif opcao == "3":  
            print(f"{ratname} participou da discussão da sala.")  
        elif opcao == "4":  
            agora = obter_horario_atual()  
            _finalizar_atividade(participante, agora)  
            participacoes = carregar_json(ARQUIVO_PARTICIPANTES, {})  
            sessao = participacoes[sala["id"]][_chave_sessao(inicio)]  
            sessao["participantes"][ratname] = participante  
            salvar_json(ARQUIVO_PARTICIPANTES, participacoes)  

            tempo_total = participante["tempo_total_segundos"]  
            horas, resto = divmod(tempo_total, 3600)  
            minutos, segundos = divmod(resto, 60)  
            print(f"\nVocê saiu da sala '{sala['nome']}' com sucesso.")  
            print(f"Tempo ativo nesta sessão: {horas}h {minutos}m {segundos}s")  
            print("Sua vaga foi liberada. O histórico da sessão permanece salvo até o horário da sala acabar.")  
            return  
        else:  
            print("Opção inválida. Tente novamente.")  


def _finalizar_atividade(participante, horario_fim):  
    inicio_atividade = participante["inicio_atividade"]  
    if inicio_atividade is None:  
        return  

    inicio = datetime.fromisoformat(inicio_atividade)  
    segundos = max(0, int((horario_fim - inicio).total_seconds()))  
    participante["tempo_total_segundos"] += segundos  
    participante["inicio_atividade"] = None  
