import lista
from Dados import persistencia
from Horario import GerenciadorHorario
from Ratcoins import gerenciador_ratcoins


class Recompensas:
    RECOMPENSAS_POR_ACAO = (
        ("Estudar pelo menos 30 minutos no registro de presença", 15),
        ("Criar e usar o primeiro modelo de estudo", 15),
        ("Entrar em uma sala de estudo (por sessão diária)", 20),
        ("Entrar em uma comunidade", 10),
        ("Criar uma comunidade", 20),
    )
    RECOMPENSAS_MONITOR = (("Publicar uma atividade em uma sala de estudo", 5),)
    LINKS_CURSOS_GRATUITOS = (
        ("freeCodeCamp", "https://www.freecodecamp.org/learn/"),
        ("CS50x", "https://cs50.harvard.edu/x/"),
        ("The Odin Project", "https://www.theodinproject.com/"),
    )
    ARQUIVO_NOTIFICACOES = "notificacoes.json"

    def __init__(self, horario: GerenciadorHorario | None = None) -> None:
        self.estado = lista.estado
        self.ratcoins = gerenciador_ratcoins
        self.persistencia = persistencia
        self.horario = horario or GerenciadorHorario()

    def menu(self) -> None:
        ratname = self.estado.usuario_logado
        if ratname is None:
            print("Você precisa fazer login para consultar suas recompensas.")
            return
        print("\n========== RATCOINS E RECOMPENSAS ==========")
        print(f"Saldo: {self.ratcoins.saldo(ratname)} RC")
        print("\nComo ganhar RatCoins:")
        recompensas = (
            self.RECOMPENSAS_MONITOR
            if self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR
            else self.RECOMPENSAS_POR_ACAO
        )
        for descricao, pontos in recompensas:
            print(f"- {descricao}: +{pontos} RC")
        if self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR:
            print("Publicações em comunidades e entradas em salas não geram bônus para monitores.")
        print("\n===== GERENCIAR RATCOINS =====")
        self.ratcoins.menu()

    def verificar_notificacoes(self) -> None:
        ratname = self.estado.usuario_logado
        if ratname is None:
            return

        notificacoes = self.persistencia.carregar(
            self.ARQUIVO_NOTIFICACOES,
            {"usuarios": {}, "datas_processadas": []},
        )
        if not isinstance(notificacoes, dict):
            raise ValueError("O arquivo notificacoes.json deve conter um objeto JSON.")
        usuarios = notificacoes.setdefault("usuarios", {})
        datas_processadas = notificacoes.setdefault("datas_processadas", [])
        if (
            not isinstance(usuarios, dict)
            or not isinstance(datas_processadas, list)
            or not all(isinstance(item, str) for item in datas_processadas)
        ):
            raise ValueError("A estrutura do arquivo notificacoes.json está inválida.")

        agora = self.horario.obter_horario_atual()
        if agora.month in (1, 8) and agora.day == 1:
            self._notificar_lideres(notificacoes, agora.year, agora.month)

        pendentes = usuarios.get(ratname, [])
        if not isinstance(pendentes, list):
            raise ValueError(f"As notificações de '{ratname}' estão inválidas.")
        alterado = False
        for notificacao in pendentes:
            if not isinstance(notificacao, dict):
                raise ValueError(f"Uma notificação de '{ratname}' está inválida.")
            if notificacao.get("lida"):
                continue
            print(f"\n===== NOTIFICAÇÃO =====\n{notificacao['mensagem']}")
            print("Sua recompensa inclui estes cursos de programação gratuitos:")
            for nome, url in notificacao["links"]:
                print(f"- {nome}: {url}")
            notificacao["lida"] = True
            alterado = True
        if alterado:
            self.persistencia.salvar(self.ARQUIVO_NOTIFICACOES, notificacoes)

    def _notificar_lideres(
        self,
        notificacoes: dict,
        ano: int,
        mes: int,
    ) -> None:
        usuarios = notificacoes["usuarios"]
        datas_processadas = notificacoes["datas_processadas"]
        alterado = False
        for tipo_usuario in (self.estado.TIPO_ESTUDANTE, self.estado.TIPO_MONITOR):
            evento_id = f"{ano}-{mes:02d}:{tipo_usuario}"
            if evento_id in datas_processadas:
                continue
            contas = [
                usuario
                for usuario in self.estado.usuarios
                if usuario.get("tipo_usuario", self.estado.TIPO_ESTUDANTE)
                == tipo_usuario
            ]
            ranking = sorted(
                (
                    (conta["ratname"], self.ratcoins.saldo(conta["ratname"]))
                    for conta in contas
                ),
                key=lambda item: (-item[1], item[0].casefold()),
            )
            if not ranking:
                continue
            vencedor = ranking[0][0]
            usuarios.setdefault(vencedor, []).append(
                {
                    "evento_id": evento_id,
                    "mensagem": (
                        f"Parabéns, {vencedor}! Você ficou em 1º lugar no "
                        f"ranking de {tipo_usuario.lower()} em "
                        f"{mes:02d}/{ano} e recebeu uma recompensa."
                    ),
                    "links": [list(item) for item in self.LINKS_CURSOS_GRATUITOS],
                    "lida": False,
                }
            )
            datas_processadas.append(evento_id)
            alterado = True
        if alterado:
            self.persistencia.salvar(self.ARQUIVO_NOTIFICACOES, notificacoes)
