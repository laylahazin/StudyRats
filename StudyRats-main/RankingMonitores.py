import lista
from Ratcoins import gerenciador_ratcoins


class GerenciadorRankingMonitores:
    def __init__(self) -> None:
        self.estado = lista.estado
        self.ratcoins = gerenciador_ratcoins

    def exibir(self) -> None:
        if self.estado.usuario_logado is None:
            print("Você precisa fazer login para consultar o ranking dos monitores.")
            return
        monitores = [
            usuario
            for usuario in self.estado.usuarios
            if usuario.get("tipo_usuario", self.estado.TIPO_ESTUDANTE)
            == self.estado.TIPO_MONITOR
        ]
        ranking = sorted(
            (
                (monitor["ratname"], self.ratcoins.saldo(monitor["ratname"]))
                for monitor in monitores
            ),
            key=lambda item: (-item[1], item[0].casefold()),
        )
        print("\n========== RANKING DE MONITORES ==========")
        if not ranking:
            print("Ainda não existem contas de monitor cadastradas.")
            return
        for posicao, (ratname, saldo) in enumerate(ranking, start=1):
            print(f"{posicao}. {ratname} | {saldo} RatCoins")

    def menu(self) -> None:
        self.exibir()
