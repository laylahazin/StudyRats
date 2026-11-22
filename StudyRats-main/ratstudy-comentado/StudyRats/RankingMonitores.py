import lista  # Importa o modulo lista para compartilhar o estado global de login, perfil e usuarios desta aplicacao.
from Ratcoins import gerenciador_ratcoins  # Importa o gerenciador compartilhado usado para consultar saldos e registrar ganhos de RatCoins.


class GerenciadorRankingMonitores:  # Define a classe GerenciadorRankingMonitores, responsavel por o ranking das contas monitoras.
    def __init__(self) -> None:  # Declara o metodo __init__ nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self.estado = lista.estado  # Atribui ao objeto o estado global que informa usuario conectado, tipo de conta e usuarios cadastrados.
        self.ratcoins = gerenciador_ratcoins  # Atribui ao objeto o gerenciador compartilhado que consulta saldo e registra ganhos de RatCoins.

    def exibir(self) -> None:  # Declara o metodo exibir nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        if self.estado.usuario_logado is None:  # Bloqueia o acesso porque nenhuma contestaa conectada ao estado da aplicacao.
            print("Você precisa fazer login para consultar o ranking dos monitores.")  # Informa que o usuario precisestaar autenticado antes desta operacao.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        monitores = [  # Atribui a monitores o resultado desta expressao: [; esse valor sera usado nas proximas linhas.
            usuario  # Executa nesta linha da classe GerenciadorRankingMonitores e do metodo exibir a instrucao especifica: usuario
            for usuario in self.estado.usuarios  # Percorre a colecao especificada nesta linha e repete a instrucao do bloco para cada elemento.
            if usuario.get("tipo_usuario", self.estado.TIPO_ESTUDANTE)  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            == self.estado.TIPO_MONITOR  # Executa nesta linha da classe GerenciadorRankingMonitores e do metodo exibir a instrucao especifica: == self.estado.TIPO_MONITOR
        ]  # Executa nesta linha da classe GerenciadorRankingMonitores e do metodo exibir a instrucao especifica: ]
        ranking = sorted(  # Ordena os registros pela chave declarada nesta chamada.
            (  # Executa nesta linha da classe GerenciadorRankingMonitores e do metodo exibir a instrucao especifica: (
                (monitor["ratname"], self.ratcoins.saldo(monitor["ratname"]))  # Executa nesta linha da classe GerenciadorRankingMonitores e do metodo exibir a instrucao especifica: (monitor["ratname"], self.ratcoins.saldo(monitor["ratname"]))
                for monitor in monitores  # Percorre a colecao especificada nesta linha e repete a instrucao do bloco para cada elemento.
            ),  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            key=lambda item: (-item[1], item[0].casefold()),  # Normaliza nomes ou pesquisas para uma comparacao consistente.
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        print("\n========== RANKING DE MONITORES ==========")  # Exibe o cabecalho desta secao da interface: \n========== RANKING DE MONITORES ==========.
        if not ranking:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Ainda não existem contas de monitor cadastradas.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        for posicao, (ratname, saldo) in enumerate(ranking, start=1):  # Percorre a colecao atribuindo a cada elemento uma posicao sequencial para exibicao ou selecao.
            print(f"{posicao}. {ratname} | {saldo} RatCoins")  # Exibe na tela a mensagem especifica formada por esta expressao de print.

    def menu(self) -> None:  # Declara o metodo menu nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self.exibir()  # Executa nesta linha da classe GerenciadorRankingMonitores e do metodo menu a instrucao especifica: self.exibir()
