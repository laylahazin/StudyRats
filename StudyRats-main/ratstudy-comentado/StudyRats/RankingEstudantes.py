import lista  # Importa o modulo lista para compartilhar o estado global de login, perfil e usuarios desta aplicacao.
from Ratcoins import gerenciador_ratcoins  # Importa o gerenciador compartilhado usado para consultar saldos e registrar ganhos de RatCoins.


class GerenciadorRankingEstudantes:  # Define a classe GerenciadorRankingEstudantes, responsavel por o ranking das contas estudantes.
    def __init__(self, estado=None, ratcoins=None) -> None:  # Declara o metodo __init__ nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self.estado = estado if estado is not None else lista.estado  # Atribui ao objeto o estado global que informa usuario conectado, tipo de conta e usuarios cadastrados.
        self.ratcoins = ratcoins if ratcoins is not None else gerenciador_ratcoins  # Atribui ao objeto o gerenciador compartilhado que consulta saldo e registra ganhos de RatCoins.

    def exibir_ranking(self) -> None:  # Declara o metodo exibir_ranking nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        if self.estado.usuario_logado is None:  # Bloqueia o acesso porque nenhuma contestaa conectada ao estado da aplicacao.
            print("Você precisa fazer login para consultar o ranking.")  # Informa que o usuario precisestaar autenticado antes desta operacao.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.

        estudantes = [  # Atribui estaudantes o resultado desta expressao: [; esse valor sera usado nas proximas linhas.
            usuario  # Executa nesta linha da classe GerenciadorRankingEstudantes e do metodo exibir_ranking a instrucao especifica: usuario
            for usuario in self.estado.usuarios  # Percorre a colecao especificada nesta linha e repete a instrucao do bloco para cada elemento.
            if usuario.get("tipo_usuario", self.estado.TIPO_ESTUDANTE)  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            == self.estado.TIPO_ESTUDANTE  # Executa nesta linha da classe GerenciadorRankingEstudantes e do metodo exibir_ranking a instrucao especifica: == self.estado.TIPO_ESTUDANTE
        ]  # Executa nesta linha da classe GerenciadorRankingEstudantes e do metodo exibir_ranking a instrucao especifica: ]
        ranking = sorted(  # Ordena os registros pela chave declarada nesta chamada.
            (  # Executa nesta linha da classe GerenciadorRankingEstudantes e do metodo exibir_ranking a instrucao especifica: (
                (estudante["ratname"], self.ratcoins.saldo(estudante["ratname"]))  # Executa nesta linha da classe GerenciadorRankingEstudantes e do metodo exibir_ranking a instrucao especifica: (estudante["ratname"], self.ratcoins.saldo(estudante["ratname"]))
                for estudante in estudantes  # Percorre a colecao especificada nesta linha e repete a instrucao do bloco para cada elemento.
            ),  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            key=lambda item: (-item[1], item[0].casefold()),  # Normaliza nomes ou pesquisas para uma comparacao consistente.
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.

        print("\n========== RANKING DE ESTUDANTES ==========")  # Exibe o cabecalho desta secao da interface: \n========== RANKING DE ESTUDANTES ==========.
        if not ranking:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Ainda não existem contas de estudante cadastradas.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        for posicao, (ratname, saldo) in enumerate(ranking, start=1):  # Percorre a colecao atribuindo a cada elemento uma posicao sequencial para exibicao ou selecao.
            print(f"{posicao}. {ratname} | {saldo} RatCoins")  # Exibe na tela a mensagem especifica formada por esta expressao de print.

    def menu(self) -> None:  # Declara o metodo menu nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self.exibir_ranking()  # Executa nesta linha da classe GerenciadorRankingEstudantes e do metodo menu a instrucao especifica: self.exibir_ranking()
