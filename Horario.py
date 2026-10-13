from datetime import datetime  

from Persistencia import carregar_json, salvar_json  


ARQUIVO_CONFIGURACAO = "configuracao_horario.json"  


def obter_horario_atual():  
    configuracao = carregar_json(  
        ARQUIVO_CONFIGURACAO,  
        {"modo": "automatico", "data_hora_manual": None},  
    )  
    if not isinstance(configuracao, dict):  
        raise ValueError("A configuração do horário deve ser um objeto JSON.")  

    modo = configuracao.get("modo")  
    if modo == "automatico":  
        return datetime.now()  
    if modo == "manual":  
        valor = configuracao.get("data_hora_manual")  
        if not isinstance(valor, str):  
            raise ValueError("O horário manual salvo está inválido.")  
        try:  
            return datetime.fromisoformat(valor)  
        except ValueError as erro:  
            raise ValueError("O horário manual salvo está inválido.") from erro  

    raise ValueError("O modo de horário salvo é inválido.")  


def configurar_horario():  
    while True:  
        horario_atual = obter_horario_atual()  
        modo = "manual" if _modo_manual_ativo() else "automático"  
        print(f"\n=== HORÁRIO DO SISTEMA ({modo}) ===")  
        print(f"Horário considerado: {horario_atual:%d/%m/%Y %H:%M}")  
        print("1. Definir horário manual para testes")  
        print("2. Voltar ao horário automático do sistema")  
        print("0. Voltar ao menu principal")  

        opcao = input("Escolha uma opção: ").strip()  
        if opcao == "1":  
            texto_horario = input("Informe o horário de teste (HH:MM): ").strip()  
            try:  
                horario = datetime.strptime(texto_horario, "%H:%M").time()  
            except ValueError:  
                print("Horário inválido. Use o formato HH:MM, por exemplo 18:30.")  
                continue  

            agora_real = datetime.now()  
            horario_manual = datetime.combine(agora_real.date(), horario)  
            salvar_json(  
                ARQUIVO_CONFIGURACAO,  
                {  
                    "modo": "manual",  
                    "data_hora_manual": horario_manual.isoformat(timespec="minutes"),  
                },  
            )  
            print(  
                f"Horário de teste definido para "  
                f"{horario_manual:%d/%m/%Y %H:%M}. Ele permanecerá fixo "  
                "até você selecionar o modo automático."  
            )  

        elif opcao == "2":  
            salvar_json(  
                ARQUIVO_CONFIGURACAO,  
                {"modo": "automatico", "data_hora_manual": None},  
            )  
            print("Horário automático do sistema restaurado.")  
            return  

        elif opcao == "0":  
            return  

        else:  
            print("Opção inválida, tente novamente.")  


def _modo_manual_ativo():  
    configuracao = carregar_json(  
        ARQUIVO_CONFIGURACAO,  
        {"modo": "automatico", "data_hora_manual": None},  
    )  
    if not isinstance(configuracao, dict):  
        raise ValueError("A configuração do horário deve ser um objeto JSON.")  
    return configuracao.get("modo") == "manual"  
