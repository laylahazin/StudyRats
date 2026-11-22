from uuid import uuid4

import lista
from Dados import persistencia


class GerenciadorRatCoins:
    ARQUIVO = "ratcoins.json"

    def __init__(self) -> None:
        self.estado = lista.estado
        self.persistencia = persistencia

    def _carregar_dados(self) -> dict:
        dados = self.persistencia.carregar(
            self.ARQUIVO,
            {"usuarios": {}, "eventos_processados": {}},
        )
        if not isinstance(dados, dict):
            raise ValueError("O arquivo ratcoins.json deve conter um objeto JSON.")

        if "usuarios" in dados and "eventos_processados" in dados:
            usuarios = dados["usuarios"]
            eventos = dados["eventos_processados"]
            if not isinstance(usuarios, dict) or not isinstance(eventos, dict):
                raise ValueError("A estrutura do arquivo ratcoins.json está inválida.")
        else:
            usuarios = dados
            eventos = {}

        for ratname, historico in usuarios.items():
            if not isinstance(historico, list):
                raise ValueError(f"O histórico de RatCoins de '{ratname}' está inválido.")
        for ratname, chaves in eventos.items():
            if not isinstance(chaves, list) or not all(
                isinstance(chave, str) for chave in chaves
            ):
                raise ValueError(
                    f"Os eventos de RatCoins de '{ratname}' estão inválidos."
                )

        return {"usuarios": usuarios, "eventos_processados": eventos}

    def _salvar_dados(self, dados: dict) -> None:
        self.persistencia.salvar(self.ARQUIVO, dados)

    def registrar_ganho(
        self,
        ratname: str,
        atividade: str,
        pontos: int,
        evento_id: str | None = None,
    ) -> bool:
        if not ratname or not isinstance(ratname, str):
            raise ValueError("É necessário informar um usuário para registrar RatCoins.")
        if not atividade or not isinstance(atividade, str):
            raise ValueError("É necessário informar a atividade que gerou RatCoins.")
        if type(pontos) is not int or pontos <= 0:
            raise ValueError("A quantidade de RatCoins deve ser um inteiro positivo.")
        if evento_id is not None and (
            not isinstance(evento_id, str) or not evento_id
        ):
            raise ValueError("O identificador do evento deve ser um texto não vazio.")

        dados = self._carregar_dados()
        usuarios = dados["usuarios"]
        eventos = dados["eventos_processados"]
        eventos_usuario = eventos.setdefault(ratname, [])
        if evento_id is not None and evento_id in eventos_usuario:
            return False

        registro = {"atividade": atividade, "pontos": pontos}
        if evento_id is not None:
            registro["evento_id"] = evento_id
            eventos_usuario.append(evento_id)
        usuarios.setdefault(ratname, []).append(registro)
        self._salvar_dados(dados)
        print(f"Você ganhou {pontos} RatCoins!")
        return True

    def saldo(self, ratname: str) -> int:
        historico = self._carregar_dados()["usuarios"].get(ratname, [])
        saldo_atual = 0
        for registro in historico:
            if not isinstance(registro, dict):
                raise ValueError(f"Um registro de RatCoins de '{ratname}' está inválido.")
            pontos = registro.get("pontos")
            if type(pontos) is not int:
                raise ValueError(f"Um registro de RatCoins de '{ratname}' está inválido.")
            saldo_atual += pontos
        return saldo_atual

    def ajustar_saldo(self, ratname: str, novo_saldo: int) -> bool:
        if not ratname or not isinstance(ratname, str):
            raise ValueError("É necessário informar um usuário para ajustar RatCoins.")
        if type(novo_saldo) is not int or novo_saldo < 0:
            raise ValueError("O saldo deve ser um inteiro não negativo.")
        if self.estado.usuario_logado != ratname:
            raise PermissionError("Só é possível ajustar o saldo da conta conectada.")
        usuario = next(
            (item for item in self.estado.usuarios if item["ratname"] == ratname),
            None,
        )
        if usuario is None or usuario.get("acesso_debug_2") is not True:
            raise PermissionError("O ajuste de saldo exige acesso ao DEBUG 2.")

        dados = self._carregar_dados()
        historico = dados["usuarios"].setdefault(ratname, [])
        if not isinstance(historico, list):
            raise ValueError(f"O histórico de RatCoins de '{ratname}' está inválido.")
        saldo_atual = sum(
            registro.get("pontos")
            for registro in historico
            if isinstance(registro, dict)
            and type(registro.get("pontos")) is int
        )
        if any(
            not isinstance(registro, dict)
            or type(registro.get("pontos")) is not int
            for registro in historico
        ):
            raise ValueError(f"O histórico de RatCoins de '{ratname}' está inválido.")
        diferenca = novo_saldo - saldo_atual
        if diferenca == 0:
            print(f"O saldo já é {novo_saldo} RC. Nenhum ajuste foi necessário.")
            return False

        evento_id = f"ajuste-saldo:{uuid4().hex}"
        historico.append(
            {
                "atividade": "Ajuste administrativo do saldo total",
                "pontos": diferenca,
                "tipo": "ajuste_saldo",
                "evento_id": evento_id,
            }
        )
        dados["eventos_processados"].setdefault(ratname, []).append(evento_id)
        self._salvar_dados(dados)
        print(f"Saldo ajustado de {saldo_atual} para {novo_saldo} RC.")
        return True

    def renomear_usuario(self, ratname_antigo: str, ratname_novo: str) -> None:
        dados = self._carregar_dados()
        usuarios = dados["usuarios"]
        eventos = dados["eventos_processados"]
        if ratname_novo in usuarios or ratname_novo in eventos:
            raise ValueError(
                f"Já existem dados de RatCoins associados a '{ratname_novo}'."
            )

        historico = usuarios.pop(ratname_antigo, [])
        if not isinstance(historico, list):
            raise ValueError(
                f"O histórico de RatCoins de '{ratname_antigo}' está inválido."
            )
        usuarios[ratname_novo] = historico
        eventos_usuario = eventos.pop(ratname_antigo, [])
        eventos[ratname_novo] = [
            evento.replace(ratname_antigo, ratname_novo)
            for evento in eventos_usuario
        ]
        self._salvar_dados(dados)

    def historico(self, ratname: str) -> list[dict]:
        historico = self._carregar_dados()["usuarios"].get(ratname, [])
        if not all(isinstance(registro, dict) for registro in historico):
            raise ValueError(f"O histórico de RatCoins de '{ratname}' está inválido.")
        return historico

    def remover_usuario(self, ratname: str) -> None:
        dados = self._carregar_dados()
        dados["usuarios"].pop(ratname, None)
        dados["eventos_processados"].pop(ratname, None)
        self._salvar_dados(dados)

    def consultar_saldo(self) -> None:
        ratname = self._usuario_atual()
        if ratname is None:
            return
        print("\n===== MINHAS RATCOINS =====")
        print(f"Usuário: {ratname}")
        print(f"Saldo atual: {self.saldo(ratname)} RC")

    def consultar_historico(self) -> None:
        ratname = self._usuario_atual()
        if ratname is None:
            return
        historico = self.historico(ratname)
        print("\n===== HISTÓRICO DE RATCOINS =====")
        if not historico:
            print("Você ainda não ganhou RatCoins.")
            return
        for indice, registro in enumerate(historico, start=1):
            print(f"\n{indice}. {registro['atividade']}")
            print(f"Pontos: {registro['pontos']} RC")

    def menu(self) -> None:
        if self._usuario_atual() is None:
            return
        while True:
            print("\n========== RATCOINS ==========")
            print("1. Consultar meu saldo")
            print("2. Ver histórico de pontos")
            print("0. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ").strip()
            acoes = {
                "1": self.consultar_saldo,
                "2": self.consultar_historico,
            }
            if opcao == "0":
                return
            acao = acoes.get(opcao)
            if acao is None:
                print("Opção inválida. Tente novamente.")
            else:
                acao()

    def _usuario_atual(self) -> str | None:
        ratname = self.estado.usuario_logado
        if ratname is None:
            print("Você precisa fazer login para acessar suas RatCoins.")
        return ratname

gerenciador_ratcoins = GerenciadorRatCoins()
