from datetime import datetime  # fornece data e hora para medir cada sessão de estudo

import lista  # fornece a conta conectada e a lista de matérias disponíveis
from Persistencia import carregar_json, salvar_json  # carrega e grava o histórico de presença em JSON


ARQUIVO_PRESENCAS = "presencas.json"  # define o nome do arquivo que mantém as sessões registradas


def registro_presenca() -> None:  # registra uma sessão de estudo para o usuário atualmente conectado
    if lista.usuario_logado is None:  # impede registrar presença sem uma conta autenticada
        print("\nVocê precisa fazer login para registrar sua presença.")  # informa como liberar o acesso ao registro
        return  # sai da rotina sem criar uma sessão

    disciplinas = {  # cria um índice das matérias para validar a escolha digitada
        sala["materia"].casefold(): sala["materia"]  # usa a forma normalizada como chave e guarda o nome original como valor
        for sala in lista.salas_disponiveis  # obtém cada matéria da configuração das salas disponíveis
    }  # conclui o dicionário que relaciona chaves normalizadas e nomes exibíveis
    print("\n===== REGISTRO DE PRESENÇA =====")  # identifica no terminal o início da rotina de presença
    print("Disciplinas disponíveis:")  # anuncia que as opções listadas podem ser selecionadas
    for disciplina in disciplinas.values():  # percorre cada nome original de matéria uma única vez
        print(f"- {disciplina}")  # mostra uma matéria disponível para o usuário

    while True:  # continua solicitando a matéria até receber uma opção válida
        entrada = input("\nDigite a disciplina ou assunto que vai estudar: ").strip()  # lê o texto digitado e remove espaços externos
        disciplina = disciplinas.get(entrada.casefold())  # procura a matéria ignorando diferenças entre maiúsculas e minúsculas
        if disciplina is not None:  # verifica se a entrada corresponde a uma matéria configurada
            break  # encerra a validação após encontrar uma matéria existente
        print("Disciplina inválida. Escolha uma das opções disponíveis.")  # explica o erro e permite tentar novamente

    confirmar = input("Deseja iniciar o cronômetro? (sim/não): ").strip().casefold()  # lê e normaliza a confirmação para iniciar a contagem
    if confirmar != "sim":  # interrompe o registro quando a resposta não confirma o início
        print("Sessão não iniciada. Você retornará ao menu principal.")  # confirma que nenhum cronômetro foi iniciado
        return  # retorna ao menu sem salvar presença

    inicio = datetime.now()  # guarda o instante inicial que será usado no cálculo do tempo estudado
    print(f"\nCronômetro iniciado! Você está estudando: {disciplina}")  # informa ao usuário qual matéria está sendo contabilizada
    while True:  # mantém a sessão aberta enquanto o usuário não pedir para finalizar
        finalizar = input(  # lê a palavra que encerra a sessão
            'Digite "finalizar" quando terminar sua sessão de estudo: '  # instrui sobre o texto esperado para terminar
        ).strip().casefold()  # remove espaços externos e normaliza o texto digitado
        if finalizar == "finalizar":  # verifica se o comando digitado corresponde ao encerramento esperado
            break  # sai do cronômetro quando o usuário termina a sessão
        print('Entrada inválida. Digite "finalizar" para encerrar a sessão.')  # repete a instrução para qualquer outro texto

    fim = datetime.now()  # registra o instante em que o usuário encerrou a sessão
    duracao_segundos = max(0, int((fim - inicio).total_seconds()))  # calcula segundos decorridos e evita duração negativa
    presencas = carregar_json(ARQUIVO_PRESENCAS, {})  # carrega registros anteriores ou usa um dicionário vazio como padrão
    if not isinstance(presencas, dict):  # verifica se o JSON tem a estrutura indexada por usuário esperada
        raise ValueError("O arquivo de presenças deve conter um objeto JSON.")  # interrompe a gravação se o arquivo estiver malformado

    historico = presencas.setdefault(lista.usuario_logado, [])  # recupera o histórico do Ratname ou cria uma lista para ele
    if not isinstance(historico, list):  # verifica se o histórico individual permite acrescentar novas sessões
        raise ValueError(  # sinaliza dados inválidos sem sobrescrever o conteúdo existente
            f"O histórico de presenças de '{lista.usuario_logado}' está inválido."  # identifica qual conta contém o histórico incorreto
        )  # completa a exceção com contexto específico do usuário afetado
    historico.append(  # acrescenta ao histórico uma entrada para a sessão recém-concluída
        {  # inicia o dicionário que descreve os dados persistidos desta sessão
            "disciplina": disciplina,  # guarda a matéria escolhida para a sessão
            "inicio": inicio.isoformat(timespec="seconds"),  # serializa o instante de início em formato ISO legível
            "fim": fim.isoformat(timespec="seconds"),  # serializa o instante de término em formato ISO legível
            "duracao_segundos": duracao_segundos,  # guarda a duração calculada como número inteiro de segundos
        }  # conclui o registro individual da sessão
    )  # finaliza a inclusão da sessão na lista de histórico
    salvar_json(ARQUIVO_PRESENCAS, presencas)  # grava todos os históricos atualizados no arquivo de presença

    minutos, segundos = divmod(duracao_segundos, 60)  # converte o total em minutos inteiros e segundos restantes
    print(  # apresenta a confirmação e o resumo da sessão recém-salva
        "\nSessão de estudo finalizada!"  # confirma que a contagem foi encerrada
        "\nAtividade registrada e presença confirmada."  # informa que a sessão foi persistida com sucesso
        f"\nDisciplina: {disciplina}"  # identifica a matéria associada ao registro
        f"\nTempo de estudo: {minutos} min {segundos} s"  # mostra a duração convertida para leitura simples
        "\nVocê retornará ao menu principal."  # informa que o fluxo voltará ao menu
    )  # finaliza a exibição do resumo


if __name__ == "__main__":  # permite executar a rotina diretamente sem iniciá-la ao importar o módulo
    registro_presenca()  # inicia o registro quando este arquivo for chamado como programa
