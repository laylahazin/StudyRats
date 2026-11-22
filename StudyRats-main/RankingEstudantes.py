import lista
from Ratcoins import gerenciador_ratcoins


class GerenciadorRankingEstudantes:
    def __init__(self, estado=None, ratcoins=None) -> None:
        self.estado = estado if estado is not None else lista.estado
        self.ratcoins = ratcoins if ratcoins is not None else gerenciador_ratcoins

    def exibir_ranking(self) -> None:
        if self.estado.usuario_logado is None:
            print("Você precisa fazer login para consultar o ranking.")
            return

        estudantes = [
            usuario
            for usuario in self.estado.usuarios
            if usuario.get("tipo_usuario", self.estado.TIPO_ESTUDANTE)
            == self.estado.TIPO_ESTUDANTE
        ]
        ranking = sorted(
            (
                (estudante["ratname"], self.ratcoins.saldo(estudante["ratname"]))
                for estudante in estudantes
            ),
            key=lambda item: (-item[1], item[0].casefold()),
        )

        print("\n========== RANKING DE ESTUDANTES ==========")
        if not ranking:
            print("Ainda não existem contas de estudante cadastradas.")
            return
        for posicao, (ratname, saldo) in enumerate(ranking, start=1):
            print(f"{posicao}. {ratname} | {saldo} RatCoins")

    def menu(self) -> None:
        self.exibir_ranking()
