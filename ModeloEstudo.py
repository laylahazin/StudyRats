import lista  
from Persistencia import carregar_json, salvar_json  


ARQUIVO_MODELOS = "modelos_estudo.json"  
MODELOS_PREDEFINIDOS = {  
    "1": {  
        "nome": "Pomodoro",  
        "blocos": [("Estudo", 25), ("Pausa", 5)] * 3  
        + [("Estudo", 25), ("Pausa longa", 15)],  
    },  
    "2": {  
        "nome": "Estudo aprofundado",  
        "blocos": [("Estudo", 50), ("Pausa", 10)] * 3,  
    },  
    "3": {  
        "nome": "Revisão e exercícios",  
        "blocos": [  
            ("Revisão do conteúdo", 30),  
            ("Pausa", 5),  
            ("Resolução de exercícios", 30),  
            ("Pausa", 5),  
            ("Resumo final", 20),  
        ],  
    },  
    "4": {  
        "nome": "Sessão curta",  
        "blocos": [("Estudo", 20), ("Pausa", 5)] * 2  
        + [("Estudo", 20)],  
    },  
}  


def _ler_duracao(pergunta: str, minimo: int, maximo: int) -> int:  
    while True:  
        resposta = input(pergunta).strip()  
        if resposta.isdigit() and minimo <= int(resposta) <= maximo:  
            return int(resposta)  
        print(f"Informe um número entre {minimo} e {maximo}.")  


def _criar_modelo_personalizado() -> dict:  
    while True:  
        tema = input("Qual assunto você vai estudar? ").strip()  
        if tema:  
            break  
        print("O assunto não pode ficar vazio.")  

    duracao = _ler_duracao("Duração de cada bloco de estudo (minutos, 1-180): ", 1, 180)  
    pausa = _ler_duracao("Duração das pausas (minutos, 1-60): ", 1, 60)  
    quantidade = _ler_duracao("Quantidade de blocos de estudo (1-8): ", 1, 8)  
    blocos = []  
    for indice in range(quantidade):  
        blocos.append((f"Estudo: {tema}", duracao))  
        if indice < quantidade - 1:  
            blocos.append(("Pausa", pausa))  
    return {"nome": f"Plano personalizado: {tema}", "blocos": blocos}  


def _salvar_modelo(modelo: dict) -> None:  
    planos = carregar_json(ARQUIVO_MODELOS, {})  
    if not isinstance(planos, dict):  
        raise ValueError("O arquivo de modelos de estudo deve conter um objeto JSON.")  
    planos[lista.usuario_logado] = modelo  
    salvar_json(ARQUIVO_MODELOS, planos)  


def _exibir_modelo(modelo: dict) -> None:  
    print(f"\n=== {modelo['nome']} ===")  
    horario_minuto = 0  
    for indice, (atividade, duracao) in enumerate(modelo["blocos"], start=1):  
        fim_minuto = horario_minuto + duracao  
        print(  
            f"{indice}. {atividade}: "  
            f"{horario_minuto // 60:02d}:{horario_minuto % 60:02d} - "  
            f"{fim_minuto // 60:02d}:{fim_minuto % 60:02d} "  
            f"({duracao} min)"  
        )  
        horario_minuto = fim_minuto  
    print(f"Duração total: {horario_minuto // 60}h {horario_minuto % 60}min")  


def modelo_estudo() -> None:  
    if lista.usuario_logado is None:  
        print("\nVocê precisa fazer login para acessar os modelos de estudo.")  
        return  

    while True:  
        print("\n===== MODELO DE ESTUDO =====")  
        for escolha, modelo in MODELOS_PREDEFINIDOS.items():  
            print(f"{escolha}. {modelo['nome']}")  
        print("5. Criar modelo personalizado")  
        print("0. Voltar ao menu principal")  
        escolha = input("Escolha um modelo: ").strip()  

        if escolha == "0":  
            return  
        if escolha == "5":  
            modelo = _criar_modelo_personalizado()  
        elif escolha in MODELOS_PREDEFINIDOS:  
            modelo = MODELOS_PREDEFINIDOS[escolha]  
        else:  
            print("Opção inválida, tente novamente.")  
            continue  

        _exibir_modelo(modelo)  
        _salvar_modelo(modelo)  
        print("Modelo salvo para sua conta.")  
        return  


if __name__ == "__main__":  
    modelo_estudo()  
