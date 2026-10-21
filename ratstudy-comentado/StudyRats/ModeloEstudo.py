import lista  # fornece o Ratname conectado, usado como chave do plano salvo
from Persistencia import carregar_json, salvar_json  # carrega os planos existentes e grava o modelo escolhido


ARQUIVO_MODELOS = "modelos_estudo.json"  # define o arquivo JSON que persiste o último plano de cada pessoa
MODELOS_PREDEFINIDOS = {  # reúne os cronogramas prontos, indexados pelo número apresentado no menu
    "1": {  # configura a primeira opção como uma sessão no formato Pomodoro
        "nome": "Pomodoro",  # guarda o nome que será apresentado ao usuário
        "blocos": [("Estudo", 25), ("Pausa", 5)] * 3  # repete três períodos de estudo de 25 min seguidos de pausas de 5 min
        + [("Estudo", 25), ("Pausa longa", 15)],  # acrescenta um quarto período de estudo e uma pausa final mais longa
    },  # termina os dados do modelo Pomodoro
    "2": {  # configura a segunda opção como períodos de concentração mais longos
        "nome": "Estudo aprofundado",  # guarda o nome que identifica este cronograma
        "blocos": [("Estudo", 50), ("Pausa", 10)] * 3,  # agenda três ciclos com 50 min de estudo e 10 min de pausa
    },  # termina os dados do modelo de estudo aprofundado
    "3": {  # configura a terceira opção para alternar revisão, prática e síntese
        "nome": "Revisão e exercícios",  # guarda o nome que identifica este cronograma
        "blocos": [  # lista as etapas ordenadas do cronograma de revisão
            ("Revisão do conteúdo", 30),  # reserva 30 min para reler e revisar o conteúdo
            ("Pausa", 5),  # separa as atividades com 5 min de descanso
            ("Resolução de exercícios", 30),  # reserva 30 min para praticar com exercícios
            ("Pausa", 5),  # inclui outro intervalo de 5 min antes da síntese
            ("Resumo final", 20),  # reserva 20 min para consolidar os pontos estudados
        ],  # conclui a sequência de atividades deste modelo
    },  # termina os dados do modelo de revisão
    "4": {  # configura a quarta opção para uma sessão total mais curta
        "nome": "Sessão curta",  # guarda o nome que identifica este cronograma
        "blocos": [("Estudo", 20), ("Pausa", 5)] * 2  # repete duas vezes um bloco de 20 min e uma pausa de 5 min
        + [("Estudo", 20)],  # inclui um último bloco de estudo sem pausa posterior
    },  # termina os dados do modelo curto
}  # conclui o dicionário dos modelos predefinidos


def _ler_duracao(pergunta: str, minimo: int, maximo: int) -> int:  # lê uma quantidade inteira até receber um valor dentro do intervalo permitido
    while True:  # repete a pergunta enquanto a entrada não atender aos limites
        resposta = input(pergunta).strip()  # apresenta a pergunta recebida e remove espaços externos da resposta
        if resposta.isdigit() and minimo <= int(resposta) <= maximo:  # valida que a resposta contém dígitos e respeita os dois limites
            return int(resposta)  # devolve a duração já convertida para inteiro
        print(f"Informe um número entre {minimo} e {maximo}.")  # informa os valores mínimo e máximo aceitos


def _criar_modelo_personalizado() -> dict:  # coleta os dados do usuário e monta um cronograma próprio
    while True:  # exige que o assunto informado tenha pelo menos um caractere
        tema = input("Qual assunto você vai estudar? ").strip()  # solicita o tema e remove espaços no começo e no fim
        if tema:  # verifica se restou algum texto após remover os espaços
            break  # aceita o tema e passa para a configuração dos blocos
        print("O assunto não pode ficar vazio.")  # explica por que é necessário informar um tema

    duracao = _ler_duracao("Duração de cada bloco de estudo (minutos, 1-180): ", 1, 180)  # lê a duração de cada bloco e limita-a a 1–180 min
    pausa = _ler_duracao("Duração das pausas (minutos, 1-60): ", 1, 60)  # lê a duração das pausas e limita-a a 1–60 min
    quantidade = _ler_duracao("Quantidade de blocos de estudo (1-8): ", 1, 8)  # lê quantos períodos de estudo serão incluídos no plano
    blocos = []  # prepara a lista ordenada que receberá períodos de estudo e pausas
    for indice in range(quantidade):  # cria um período de estudo para cada número solicitado
        blocos.append((f"Estudo: {tema}", duracao))  # registra o tema e a duração de um bloco de estudo
        if indice < quantidade - 1:  # evita inserir uma pausa depois do último bloco
            blocos.append(("Pausa", pausa))  # acrescenta uma pausa entre este bloco e o próximo
    return {"nome": f"Plano personalizado: {tema}", "blocos": blocos}  # devolve o plano com seu nome e a sequência de atividades


def _salvar_modelo(modelo: dict) -> None:  # salva o plano escolhido para o usuário autenticado
    planos = carregar_json(ARQUIVO_MODELOS, {})  # carrega planos anteriores ou começa com um objeto sem usuários
    if not isinstance(planos, dict):  # confirma que o arquivo tem o formato de mapeamento esperado
        raise ValueError("O arquivo de modelos de estudo deve conter um objeto JSON.")  # sinaliza a estrutura inválida sem descartá-la
    planos[lista.usuario_logado] = modelo  # associa o cronograma atual à conta que está conectada
    salvar_json(ARQUIVO_MODELOS, planos)  # grava em disco o dicionário completo de planos atualizado


def _exibir_modelo(modelo: dict) -> None:  # apresenta cada bloco como horário relativo desde o início do plano
    print(f"\n=== {modelo['nome']} ===")  # identifica o cronograma que será mostrado
    horario_minuto = 0  # inicia a agenda em zero minutos decorridos
    for indice, (atividade, duracao) in enumerate(modelo["blocos"], start=1):  # percorre blocos em ordem e numera o primeiro como 1
        fim_minuto = horario_minuto + duracao  # calcula o instante final somando o tamanho do bloco ao horário atual
        print(  # imprime atividade, horários de início e fim e duração em uma linha
            f"{indice}. {atividade}: "  # inclui número e nome da atividade
            f"{horario_minuto // 60:02d}:{horario_minuto % 60:02d} - "  # converte o início de minutos decorridos para horas e minutos
            f"{fim_minuto // 60:02d}:{fim_minuto % 60:02d} "  # converte o fim do bloco para horas e minutos
            f"({duracao} min)"  # mostra a duração configurada para este bloco
        )  # finaliza a apresentação da linha da atividade
        horario_minuto = fim_minuto  # inicia o próximo bloco quando o bloco atual terminar
    print(f"Duração total: {horario_minuto // 60}h {horario_minuto % 60}min")  # exibe o total acumulado em horas e minutos


def modelo_estudo() -> None:  # permite escolher um cronograma pronto ou compor um plano personalizado
    if lista.usuario_logado is None:  # protege os planos pessoais contra uso sem autenticação
        print("\nVocê precisa fazer login para acessar os modelos de estudo.")  # informa que o login é necessário
        return  # retorna ao menu sem exibir ou salvar planos

    while True:  # mantém a seleção aberta até escolher um plano válido ou voltar
        print("\n===== MODELO DE ESTUDO =====")  # identifica a tela de seleção de cronogramas
        for escolha, modelo in MODELOS_PREDEFINIDOS.items():  # percorre as opções numeradas dos modelos prontos
            print(f"{escolha}. {modelo['nome']}")  # mostra o número da opção e seu nome
        print("5. Criar modelo personalizado")  # oferece a criação de um cronograma definido pelo usuário
        print("0. Voltar ao menu principal")  # oferece retorno sem selecionar ou salvar um plano
        escolha = input("Escolha um modelo: ").strip()  # lê a opção digitada e remove espaços externos

        if escolha == "0":  # verifica se a pessoa pediu para voltar ao menu principal
            return  # sai sem salvar nenhuma alteração
        if escolha == "5":  # verifica se a pessoa pediu para criar um plano próprio
            modelo = _criar_modelo_personalizado()  # coleta tema, duração, pausas e quantidade de blocos
        elif escolha in MODELOS_PREDEFINIDOS:  # verifica se a opção corresponde a um modelo predefinido
            modelo = MODELOS_PREDEFINIDOS[escolha]  # seleciona os dados do cronograma numerado
        else:  # trata entradas que não são opções disponíveis
            print("Opção inválida, tente novamente.")  # explica que a opção não existe
            continue  # reapresenta as escolhas sem salvar plano

        _exibir_modelo(modelo)  # apresenta todas as atividades e a duração total do plano
        _salvar_modelo(modelo)  # associa o cronograma selecionado à conta conectada e grava-o
        print("Modelo salvo para sua conta.")  # confirma que o plano foi persistido para o usuário
        return  # retorna ao menu após concluir a seleção e o salvamento


if __name__ == "__main__":  # impede que a interação comece quando o módulo for importado por outro arquivo
    modelo_estudo()  # executa diretamente a seleção de modelo quando este arquivo for iniciado
