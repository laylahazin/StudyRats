import lista
from Dados import gerenciador_credenciais, persistencia
from Ratcoins import gerenciador_ratcoins


class GerenciadorConta:
    SENHAS_DEBUG = {
        "BSISTUDYRAT": "acesso_debug_1",
        "BSISTUDYRATADM": "acesso_debug_2",
    }

    def __init__(self) -> None:
        self.estado = lista.estado
        self.persistencia = persistencia
        self.gerenciador_credenciais = gerenciador_credenciais

    def realizar_login(self) -> None:
        print("\n--- TELA DE LOGIN ---")
        email = input("Digite seu e-mail: ").strip().lower()
        senha = input("Digite sua senha: ")

        for usuario in self.estado.usuarios:
            if usuario["email"].lower() != email:
                continue

            if "senha_hash" not in usuario or "senha_salt" not in usuario:
                raise ValueError(
                    "A conta salva não possui credenciais compatíveis. "
                    "Remova-a ou faça a migração antes de tentar entrar."
                )

            if self.gerenciador_credenciais.verificar(
                senha, usuario["senha_salt"], usuario["senha_hash"]
            ):
                self.estado.definir_usuario_logado(usuario["ratname"])
                print(
                    "\nLogin bem-sucedido! Você está conectado como: "
                    f"{self.estado.usuario_logado}"
                )
                return
            break

        print("\nErro: E-mail ou senha incorretos.")

    def excluir_conta(self) -> None:
        ratname = self.estado.usuario_logado
        if ratname is None:
            print("\nVocê precisa estar conectado para excluir a conta.")
            return

        usuarios_atualizados = [
            item for item in self.estado.usuarios if item["ratname"] != ratname
        ]
        if len(usuarios_atualizados) == len(self.estado.usuarios):
            print("\nConta não encontrada para exclusão.")
            self.estado.definir_usuario_logado(None)
            return

        self.persistencia.salvar("usuarios.json", usuarios_atualizados)
        self.estado.substituir_usuarios(usuarios_atualizados)

        for arquivo in (
            "modelos_estudo.json",
            "presencas.json",
            "calendario.json",
            "blocos_notas.json",
            "notificacoes.json",
        ):
            dados = self.persistencia.carregar(arquivo, {})
            if isinstance(dados, dict):
                if arquivo == "notificacoes.json":
                    dados.get("usuarios", {}).pop(ratname, None)
                else:
                    dados.pop(ratname, None)
                self.persistencia.salvar(arquivo, dados)
        gerenciador_ratcoins.remover_usuario(ratname)

        print(f"\nA conta de {ratname} foi excluída com sucesso.")
        self.estado.definir_usuario_logado(None)

    def editar_conta(self) -> None:
        usuario = self._usuario_logado()
        if usuario is None:
            return
        if not self._confirmar_senha_atual(usuario):
            print("Senha atual incorreta. Nenhuma alteração foi feita.")
            return

        ratname_antigo = usuario["ratname"]
        email_antigo = usuario["email"]
        novo_email = input(
            f"Novo e-mail (Enter mantém {email_antigo}): "
        ).strip().lower()
        novo_ratname = input(
            f"Novo Ratname (Enter mantém {ratname_antigo}): "
        ).strip()
        nova_senha = input(
            "Nova senha (Enter mantém a atual): "
        )

        if novo_email and not self._email_valido(novo_email):
            print("E-mail inválido. Use um endereço institucional @ufrpe.br.")
            return
        if novo_email and any(
            item["ratname"] != ratname_antigo
            and item["email"].casefold() == novo_email.casefold()
            for item in self.estado.usuarios
        ):
            print("Este e-mail já está cadastrado.")
            return
        if novo_ratname and any(
            item["ratname"].casefold() == novo_ratname.casefold()
            and item["ratname"] != ratname_antigo
            for item in self.estado.usuarios
        ):
            print("Este Ratname já está em uso.")
            return
        if nova_senha and not self._senha_valida(nova_senha):
            print(
                "A senha deve ter de 6 a 8 caracteres, uma letra maiúscula, "
                "um número e um caractere especial."
            )
            return

        ratname_novo = novo_ratname or ratname_antigo
        email_novo = novo_email or email_antigo
        if (
            ratname_novo == ratname_antigo
            and email_novo == email_antigo
            and not nova_senha
        ):
            print("Nenhuma alteração foi informada.")
            return

        if ratname_novo != ratname_antigo or email_novo != email_antigo:
            self._atualizar_referencias_usuario(
                ratname_antigo,
                ratname_novo,
                email_novo,
            )

        usuarios_atualizados = [dict(item) for item in self.estado.usuarios]
        usuario_atualizado = next(
            item for item in usuarios_atualizados
            if item["ratname"] == ratname_antigo
        )
        usuario_atualizado["ratname"] = ratname_novo
        usuario_atualizado["email"] = email_novo
        if nova_senha:
            usuario_atualizado.update(self.gerenciador_credenciais.criar(nova_senha))
        self.persistencia.salvar("usuarios.json", usuarios_atualizados)
        self.estado.substituir_usuarios(usuarios_atualizados)
        if ratname_novo != ratname_antigo:
            self.estado.definir_usuario_logado(ratname_novo)
        print("Dados da conta atualizados com sucesso.")

    def menu_debug_codes(self) -> None:
        usuario = self._usuario_logado()
        if usuario is None:
            return
        while True:
            print("\n===== ACESSOS DEBUG =====")
            print(
                "DEBUG 1 - Alteração de data/horário: "
                f"{'liberado' if usuario.get('acesso_debug_1') is True else 'bloqueado'}"
            )
            print(
                "DEBUG 2 - Alteração do saldo RatCoins: "
                f"{'liberado' if usuario.get('acesso_debug_2') is True else 'bloqueado'}"
            )
            print("Digite um código administrativo para liberar o acesso correspondente.")
            print("0. Voltar ao perfil")
            senha = input("Código: ").strip()
            if senha == "0":
                return
            acesso = self.SENHAS_DEBUG.get(senha)
            if acesso is None:
                print("Código inválido.")
                continue
            if usuario.get(acesso) is True:
                print("Este acesso DEBUG já está liberado para sua conta.")
                continue
            usuario[acesso] = True
            self.estado.salvar_usuarios()
            print(f"{acesso.replace('acesso_', '').upper()} liberado para esta conta.")

    @staticmethod
    def tem_acesso_debug(usuario: dict, nivel: int) -> bool:
        if nivel not in (1, 2):
            raise ValueError("O nível DEBUG deve ser 1 ou 2.")
        return usuario.get(f"acesso_debug_{nivel}") is True

    def _atualizar_referencias_usuario(
        self,
        ratname_antigo: str,
        ratname_novo: str,
        email_novo: str,
    ) -> None:
        arquivos_chave = (
            "modelos_estudo.json",
            "presencas.json",
            "calendario.json",
            "blocos_notas.json",
        )
        atualizacoes = {}
        for arquivo in arquivos_chave:
            dados = self.persistencia.carregar(arquivo, {})
            if not isinstance(dados, dict):
                raise ValueError(f"O arquivo {arquivo} deve conter um objeto JSON.")
            if ratname_novo != ratname_antigo and ratname_novo in dados:
                raise ValueError(
                    f"Já existem dados associados ao Ratname '{ratname_novo}'."
                )
            if ratname_antigo in dados and ratname_novo != ratname_antigo:
                dados[ratname_novo] = dados.pop(ratname_antigo)
            atualizacoes[arquivo] = dados

        participacoes = self.persistencia.carregar("participantes_salas.json", {})
        self._atualizar_participacoes(
            participacoes,
            ratname_antigo,
            ratname_novo,
            email_novo,
        )
        atualizacoes["participantes_salas.json"] = participacoes

        comunidades = self.persistencia.carregar("comunidades.json", [])
        self._atualizar_comunidades(
            comunidades, ratname_antigo, ratname_novo
        )
        atualizacoes["comunidades.json"] = comunidades

        notificacoes = self.persistencia.carregar(
            "notificacoes.json",
            {"usuarios": {}, "datas_processadas": []},
        )
        self._atualizar_notificacoes(
            notificacoes, ratname_antigo, ratname_novo
        )
        atualizacoes["notificacoes.json"] = notificacoes

        if ratname_novo != ratname_antigo:
            dados_ratcoins = gerenciador_ratcoins._carregar_dados()
            if (
                ratname_novo in dados_ratcoins["usuarios"]
                or ratname_novo in dados_ratcoins["eventos_processados"]
            ):
                raise ValueError(
                    f"Já existem RatCoins associados ao Ratname '{ratname_novo}'."
                )

        for arquivo, dados in atualizacoes.items():
            self.persistencia.salvar(arquivo, dados)
        if ratname_novo != ratname_antigo:
            gerenciador_ratcoins.renomear_usuario(
                ratname_antigo, ratname_novo
            )

    @staticmethod
    def _atualizar_participacoes(
        participacoes: dict,
        ratname_antigo: str,
        ratname_novo: str,
        email_novo: str,
    ) -> None:
        if not isinstance(participacoes, dict):
            raise ValueError("O arquivo participantes_salas.json está inválido.")
        for sessoes in participacoes.values():
            if not isinstance(sessoes, dict):
                raise ValueError("As sessões de uma sala estão inválidas.")
            for sessao in sessoes.values():
                if not isinstance(sessao, dict):
                    raise ValueError("Uma sessão de sala está inválida.")
                participantes = sessao.get("participantes", {})
                if not isinstance(participantes, dict):
                    raise ValueError("Os participantes de uma sessão estão inválidos.")
                if (
                    ratname_novo != ratname_antigo
                    and ratname_antigo in participantes
                    and ratname_novo in participantes
                ):
                    raise ValueError(
                        f"Já existe participação registrada para '{ratname_novo}'."
                    )
                if ratname_antigo in participantes:
                    participante = participantes.pop(ratname_antigo)
                    participante["email"] = email_novo
                    participantes[ratname_novo] = participante
                for atividade in sessao.get("atividades", []):
                    if atividade.get("monitor") == ratname_antigo:
                        atividade["monitor"] = ratname_novo
                for duvida in sessao.get("duvidas", []):
                    if duvida.get("usuario") == ratname_antigo:
                        duvida["usuario"] = ratname_novo
                    for resposta in duvida.get("respostas", []):
                        if resposta.get("usuario") == ratname_antigo:
                            resposta["usuario"] = ratname_novo

    @staticmethod
    def _atualizar_comunidades(
        comunidades: list,
        ratname_antigo: str,
        ratname_novo: str,
    ) -> None:
        if not isinstance(comunidades, list):
            raise ValueError("O arquivo comunidades.json está inválido.")
        for comunidade in comunidades:
            if not isinstance(comunidade, dict):
                raise ValueError("Uma comunidade salva está inválida.")
            if comunidade.get("criador") == ratname_antigo:
                comunidade["criador"] = ratname_novo
            membros = comunidade.get("membros", [])
            if not isinstance(membros, list):
                raise ValueError("A lista de membros de uma comunidade está inválida.")
            comunidade["membros"] = [
                ratname_novo if membro == ratname_antigo else membro
                for membro in membros
            ]
            for publicacao in comunidade.get("publicacoes", []):
                if publicacao.get("autor") == ratname_antigo:
                    publicacao["autor"] = ratname_novo
                for resposta in publicacao.get("respostas", []):
                    if resposta.get("autor") == ratname_antigo:
                        resposta["autor"] = ratname_novo

    @staticmethod
    def _atualizar_notificacoes(
        notificacoes: dict,
        ratname_antigo: str,
        ratname_novo: str,
    ) -> None:
        if not isinstance(notificacoes, dict):
            raise ValueError("O arquivo notificacoes.json está inválido.")
        usuarios = notificacoes.setdefault("usuarios", {})
        if not isinstance(usuarios, dict):
            raise ValueError("A lista de notificações de usuários está inválida.")
        pendentes = usuarios.pop(ratname_antigo, [])
        usuarios.setdefault(ratname_novo, []).extend(pendentes)
        for lista_notificacoes in usuarios.values():
            if not isinstance(lista_notificacoes, list):
                raise ValueError("Uma lista de notificações está inválida.")
            for notificacao in lista_notificacoes:
                if isinstance(notificacao, dict) and isinstance(
                    notificacao.get("mensagem"), str
                ):
                    notificacao["mensagem"] = notificacao["mensagem"].replace(
                        ratname_antigo, ratname_novo
                    )

    def _usuario_logado(self) -> dict | None:
        ratname = self.estado.usuario_logado
        if ratname is None:
            print("Você precisa fazer login para acessar esta opção.")
            return None
        usuario = next(
            (item for item in self.estado.usuarios if item["ratname"] == ratname),
            None,
        )
        if usuario is None:
            raise ValueError("O usuário conectado não existe na lista de contas.")
        return usuario

    def _confirmar_senha_atual(self, usuario: dict) -> bool:
        senha_atual = input("Confirme sua senha atual: ")
        return self.gerenciador_credenciais.verificar(
            senha_atual, usuario["senha_salt"], usuario["senha_hash"]
        )

    @staticmethod
    def _email_valido(email: str) -> bool:
        return email.endswith("@ufrpe.br") and email.count("@") == 1 and len(email) > 9

    @staticmethod
    def _senha_valida(senha: str) -> bool:
        return (
            6 <= len(senha) <= 8
            and any(letra.isupper() for letra in senha)
            and any(letra.isdigit() for letra in senha)
            and not senha.isalnum()
        )

    def deslogar(self) -> None:
        print(f"\nSaindo da conta de {self.estado.usuario_logado}...")
        self.estado.definir_usuario_logado(None)
        print("Você saiu da conta com sucesso!")
