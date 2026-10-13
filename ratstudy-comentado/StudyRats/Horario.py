from datetime import datetime  # fornece tipos e conversões para datas e horários

from Persistencia import carregar_json, salvar_json  # lê e grava a configuração persistente do relógio


ARQUIVO_CONFIGURACAO = "configuracao_horario.json"  # define qual arquivo guarda o modo e o horário manual


def obter_horario_atual():  # retorna o horário configurado para uso nas salas e nos testes
    configuracao = carregar_json(  # carrega as preferências atuais do relógio
        ARQUIVO_CONFIGURACAO,  # seleciona o arquivo JSON que armazena essas preferências
        {"modo": "automatico", "data_hora_manual": None},  # usa o relógio real como padrão se ainda não houver arquivo
    )  # conclui a leitura da configuração
    if not isinstance(configuracao, dict):  # valida que o conteúdo JSON possui as chaves esperadas
        raise ValueError("A configuração do horário deve ser um objeto JSON.")  # informa o formato incorreto em vez de ignorá-lo

    modo = configuracao.get("modo")  # lê o modo selecionado sem presumir que a chave exista
    if modo == "automatico":  # verifica se deve ser usado o relógio local real
        return datetime.now()  # devolve a data e hora atuais do computador
    if modo == "manual":  # verifica se deve ser usado o horário fixado para testes
        valor = configuracao.get("data_hora_manual")  # recupera a data/hora serializada armazenada no arquivo
        if not isinstance(valor, str):  # garante que o valor possa ser convertido a partir de texto
            raise ValueError("O horário manual salvo está inválido.")  # interrompe se o campo estiver ausente ou tiver tipo inesperado
        try:  # tenta converter o formato ISO para um objeto datetime utilizável
            return datetime.fromisoformat(valor)  # converte e devolve o horário manual salvo
        except ValueError as erro:  # captura textos que não representam uma data e hora válidas
            raise ValueError("O horário manual salvo está inválido.") from erro  # preserva o erro original e informa o problema na configuração

    raise ValueError("O modo de horário salvo é inválido.")  # rejeita modos ausentes ou diferentes dos dois modos suportados


def configurar_horario():  # permite fixar um horário de teste ou restaurar o relógio automático
    while True:  # reapresenta as opções até selecionar retorno ou modo automático
        horario_atual = obter_horario_atual()  # consulta o horário que o restante do programa usará neste momento
        modo = "manual" if _modo_manual_ativo() else "automático"  # escolhe o rótulo de exibição conforme a configuração persistida
        print(f"\n=== HORÁRIO DO SISTEMA ({modo}) ===")  # informa se o horário atual está sendo controlado manualmente
        print(f"Horário considerado: {horario_atual:%d/%m/%Y %H:%M}")  # exibe data e hora que as funcionalidades considerarão
        print("1. Definir horário manual para testes")  # oferece definir uma hora fixa para testar as salas
        print("2. Voltar ao horário automático do sistema")  # oferece usar novamente o relógio do computador
        print("0. Voltar ao menu principal")  # oferece sair desta tela sem alterar a configuração

        opcao = input("Escolha uma opção: ").strip()  # lê a opção selecionada e remove espaços externos
        if opcao == "1":  # inicia o processo para configurar uma hora manual
            texto_horario = input("Informe o horário de teste (HH:MM): ").strip()  # solicita a hora usando formato de 24 horas
            try:  # tenta validar e converter a entrada digitada
                horario = datetime.strptime(texto_horario, "%H:%M").time()  # aceita apenas horas e minutos válidos no formato solicitado
            except ValueError:  # trata valores inválidos ou escritos em outro formato
                print("Horário inválido. Use o formato HH:MM, por exemplo 18:30.")  # apresenta o formato correto como exemplo
                continue  # retorna às opções sem alterar o arquivo de configuração

            agora_real = datetime.now()  # obtém a data real para associá-la ao horário digitado
            horario_manual = datetime.combine(agora_real.date(), horario)  # junta a data atual à hora manual escolhida
            salvar_json(  # persiste o modo manual e o instante selecionado
                ARQUIVO_CONFIGURACAO,  # grava no arquivo destinado à configuração de horário
                {  # inicia o objeto JSON com os dois campos de configuração
                    "modo": "manual",  # informa às consultas futuras que devem usar hora fixa
                    "data_hora_manual": horario_manual.isoformat(timespec="minutes"),  # armazena data e hora em texto ISO até o minuto
                },  # conclui o objeto de configuração salvo
            )  # termina a gravação da preferência
            print(  # confirma a configuração e explica como desativá-la
                f"Horário de teste definido para "  # inicia a mensagem de confirmação
                f"{horario_manual:%d/%m/%Y %H:%M}. Ele permanecerá fixo "  # informa a data e o horário escolhidos
                "até você selecionar o modo automático."  # esclarece que a configuração persiste entre execuções
            )  # finaliza a mensagem ao usuário

        elif opcao == "2":  # seleciona novamente o relógio automático
            salvar_json(  # substitui a configuração manual persistida
                ARQUIVO_CONFIGURACAO,  # mantém a preferência no arquivo padrão
                {"modo": "automatico", "data_hora_manual": None},  # apaga a hora fixa e define o uso do relógio real
            )  # conclui a gravação do modo automático
            print("Horário automático do sistema restaurado.")  # confirma que as horas reais serão usadas novamente
            return  # retorna ao menu principal após restaurar o relógio

        elif opcao == "0":  # reconhece o pedido para voltar sem alterar a configuração
            return  # encerra a tela de horário e retorna ao menu

        else:  # trata qualquer número ou texto que não seja uma opção do menu
            print("Opção inválida, tente novamente.")  # solicita nova entrada sem sair da configuração


def _modo_manual_ativo():  # informa se a configuração atual seleciona um horário manual
    configuracao = carregar_json(  # carrega a opção de relógio persistida
        ARQUIVO_CONFIGURACAO,  # consulta o arquivo usado por todas as operações de horário
        {"modo": "automatico", "data_hora_manual": None},  # considera o relógio automático se ainda não houver configuração
    )  # conclui a leitura das preferências
    if not isinstance(configuracao, dict):  # verifica se o conteúdo tem o tipo de objeto JSON esperado
        raise ValueError("A configuração do horário deve ser um objeto JSON.")  # relata dados inválidos em vez de assumir um modo silenciosamente
    return configuracao.get("modo") == "manual"  # retorna verdadeiro somente quando o modo salvo é manual
