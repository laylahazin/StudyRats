from uuid import uuid4

import lista
from Dados import persistencia
from Ratcoins import gerenciador_ratcoins


class GerenciadorComunidades:
    ARQUIVO = "comunidades.json"
    TIPO_ESTUDANTES = "ESTUDANTES"
    TIPO_ESTUDANTES_MONITORES = "ESTUDANTES_MONITORES"
    TIPO_MONITORES = "MONITORES"

    def __init__(self) -> None:
        self.estado = lista.estado
        self.persistencia = persistencia
        self.ratcoins = gerenciador_ratcoins

    def _carregar(self) -> list[dict]:
        comunidades = self.persistencia.carregar(self.ARQUIVO, [])
        if not isinstance(comunidades, list):
            raise ValueError("O arquivo comunidades.json deve conter uma lista.")

        alterado = False
        for comunidade in comunidades:
            if not isinstance(comunidade, dict):
                raise ValueError("Uma comunidade salva possui formato inválido.")
            if "disciplina" not in comunidade and "disciplina(s)" in comunidade:
                comunidade["disciplina"] = comunidade["disciplina(s)"]
                alterado = True
            if "assunto" not in comunidade and "tag" in comunidade:
                comunidade["assunto"] = comunidade["tag"]
                alterado = True
            if "tipo_acesso" not in comunidade:
                tipo_criador = self._tipo_usuario(comunidade.get("criador"))
                comunidade["tipo_acesso"] = (
                    self.TIPO_MONITORES
                    if tipo_criador == self.estado.TIPO_MONITOR
                    else self.TIPO_ESTUDANTES
                )
                alterado = True
            if comunidade["tipo_acesso"] not in (
                self.TIPO_ESTUDANTES,
                self.TIPO_ESTUDANTES_MONITORES,
                self.TIPO_MONITORES,
            ):
                raise ValueError(
                    f"O público da comunidade '{comunidade['nome']}' está inválido."
                )
            for campo in ("nome", "disciplina", "assunto", "descricao", "criador"):
                if not isinstance(comunidade.get(campo), str):
                    raise ValueError(f"O campo '{campo}' de uma comunidade está inválido.")
            if "id" not in comunidade:
                comunidade["id"] = uuid4().hex
                alterado = True
            if "membros" not in comunidade:
                comunidade["membros"] = [comunidade["criador"]]
                alterado = True
            if "publicacoes" not in comunidade:
                comunidade["publicacoes"] = []
                alterado = True
            if "mensagens" not in comunidade:
                comunidade["mensagens"] = []
                alterado = True
            if not isinstance(comunidade["membros"], list):
                raise ValueError(f"Os membros da comunidade '{comunidade['nome']}' estão inválidos.")
            if not isinstance(comunidade["publicacoes"], list):
                raise ValueError(f"As publicações da comunidade '{comunidade['nome']}' estão inválidas.")
            if not isinstance(comunidade["mensagens"], list):
                raise ValueError(f"As mensagens da comunidade '{comunidade['nome']}' estão inválidas.")
            for publicacao in comunidade["publicacoes"]:
                if not isinstance(publicacao, dict):
                    raise ValueError("Uma publicação da comunidade possui formato inválido.")
                for campo in ("likes", "dislikes", "favoritos"):
                    if campo not in publicacao:
                        publicacao[campo] = []
                        alterado = True
                    if not isinstance(publicacao[campo], list):
                        raise ValueError("As interações de uma publicação estão inválidas.")

        if alterado:
            self._salvar(comunidades)
        return comunidades

    def _salvar(self, comunidades: list[dict]) -> None:
        self.persistencia.salvar(self.ARQUIVO, comunidades)

    def menu(self) -> None:
        if self._usuario_atual() is None:
            return
        while True:
            print("\n========== COMUNIDADES RAT ==========")
            print("1. Ver todas as comunidades")
            print("2. Pesquisar comunidades")
            print("3. Entrar em uma comunidade")
            print("4. Criar comunidade")
            print("5. Editar minha comunidade")
            print("6. Excluir minha comunidade")
            print("0. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ").strip()
            acoes = {
                "1": self.listar,
                "2": self.pesquisar,
                "3": self.entrar,
                "4": self.criar,
                "5": self.editar,
                "6": self.excluir,
            }
            if opcao == "0":
                return
            acao = acoes.get(opcao)
            if acao is None:
                print("Opção inválida. Tente novamente.")
            else:
                acao()

    def listar(self) -> None:
        comunidades = self._carregar()
        print("\n===== COMUNIDADES RAT =====")
        if not comunidades:
            print("Ainda não existem comunidades cadastradas.")
            return
        for indice, comunidade in enumerate(comunidades, start=1):
            print(f"\n{indice}. {comunidade['nome']}")
            print(f"Disciplina: {comunidade['disciplina']}")
            print(f"Assunto: {comunidade['assunto']}")
            print(f"Público: {self._nome_tipo_acesso(comunidade['tipo_acesso'])}")
            print(f"Participantes: {len(comunidade['membros'])}")

    def pesquisar(self) -> None:
        comunidades = self._carregar()
        print("\n===== PESQUISAR COMUNIDADES =====")
        pesquisa = input("Digite o nome, disciplina ou assunto: ").strip().casefold()
        if not pesquisa:
            print("Digite algo para pesquisar.")
            return

        resultados = [
            comunidade
            for comunidade in comunidades
            if any(
                pesquisa in comunidade[campo].casefold()
                for campo in ("nome", "disciplina", "assunto")
            )
        ]
        if not resultados:
            print("Nenhuma comunidade encontrada.")
            return
        for indice, comunidade in enumerate(resultados, start=1):
            print(f"\n{indice}. {comunidade['nome']}")
            print(f"Disciplina: {comunidade['disciplina']}")
            print(f"Assunto: {comunidade['assunto']}")

    def criar(self) -> None:
        ratname = self._usuario_atual()
        if ratname is None:
            return
        comunidades = self._carregar()
        print("\n===== CRIAR COMUNIDADE RAT =====")
        tipo_usuario = self.estado.tipo_usuario_logado
        if tipo_usuario == self.estado.TIPO_ESTUDANTE:
            print("Público da comunidade:")
            print("1. Apenas estudantes")
            print("2. Estudantes e monitores")
            opcao_acesso = input("Escolha o público: ").strip()
            if opcao_acesso == "1":
                tipo_acesso = self.TIPO_ESTUDANTES
            elif opcao_acesso == "2":
                tipo_acesso = self.TIPO_ESTUDANTES_MONITORES
            else:
                print("Opção de público inválida.")
                return
        elif tipo_usuario == self.estado.TIPO_MONITOR:
            print("Como monitor, esta comunidade será exclusiva para monitores.")
            tipo_acesso = self.TIPO_MONITORES
        else:
            print("Tipo de usuário inválido.")
            return

        nome = input("Nome da comunidade: ").strip()
        if not nome:
            print("O nome da comunidade não pode ficar vazio.")
            return
        if any(comunidade["nome"].casefold() == nome.casefold() for comunidade in comunidades):
            print("Já existe uma comunidade com esse nome.")
            return

        disciplina = input("Disciplina(s): ").strip()
        tag = input("Assunto de interesse: ").strip()
        descricao = input("Descrição da comunidade: ").strip()
        if not disciplina or not tag or not descricao:
            print("Preencha todas as informações.")
            return

        id_comunidade = uuid4().hex
        comunidade = {
            "id": id_comunidade,
            "nome": nome,
            "disciplina": disciplina,
            "assunto": tag,
            "descricao": descricao,
            "criador": ratname,
            "tipo_acesso": tipo_acesso,
            "membros": [ratname],
            "publicacoes": [],
            "mensagens": [],
        }
        comunidades.append(comunidade)
        self._salvar(comunidades)
        if self.estado.tipo_usuario_logado == self.estado.TIPO_ESTUDANTE:
            self.ratcoins.registrar_ganho(
                ratname,
                f"Criar comunidade: {nome}",
                20,
                evento_id=f"comunidade-criar:{id_comunidade}",
            )
        print("\nComunidade criada com sucesso!")
        print("Você já faz parte dela como criador.")

    def editar(self) -> None:
        comunidades = self._carregar()
        self.listar()
        comunidade = self._selecionar(comunidades, "Digite o número da comunidade que deseja editar: ")
        if comunidade is None:
            return
        if comunidade["criador"] != self.estado.usuario_logado:
            print("Somente o criador pode editar essa comunidade.")
            return

        print("\nDeixe em branco o que não deseja alterar.")
        novo_nome = input("Novo nome: ").strip()
        nova_disciplina = input("Nova disciplina: ").strip()
        novo_assunto = input("Novo assunto: ").strip()
        nova_descricao = input("Nova descrição: ").strip()
        if novo_nome and any(
            outra is not comunidade and outra["nome"].casefold() == novo_nome.casefold()
            for outra in comunidades
        ):
            print("Já existe outra comunidade com esse nome.")
            return
        if novo_nome:
            comunidade["nome"] = novo_nome
        if nova_disciplina:
            comunidade["disciplina"] = nova_disciplina
        if novo_assunto:
            comunidade["assunto"] = novo_assunto
        if nova_descricao:
            comunidade["descricao"] = nova_descricao
        self._salvar(comunidades)
        print("Comunidade atualizada com sucesso!")

    def excluir(self) -> None:
        comunidades = self._carregar()
        self.listar()
        comunidade = self._selecionar(comunidades, "Digite o número da comunidade que deseja excluir: ")
        if comunidade is None:
            return
        if comunidade["criador"] != self.estado.usuario_logado:
            print("Somente o criador pode excluir essa comunidade.")
            return
        confirmacao = input(
            f"Tem certeza que deseja excluir '{comunidade['nome']}'? (s/n): "
        ).strip().lower()
        if confirmacao != "s":
            print("Exclusão cancelada.")
            return
        comunidades.remove(comunidade)
        self._salvar(comunidades)
        print("Comunidade excluída com sucesso!")

    def entrar(self) -> None:
        ratname = self._usuario_atual()
        if ratname is None:
            return
        comunidades = self._carregar()
        self.listar()
        comunidade = self._selecionar(
            comunidades, "Digite o número da comunidade que deseja acessar: "
        )
        if comunidade is None:
            return
        self._exibir_detalhes(comunidade)
        if not self._usuario_pode_acessar(ratname, comunidade):
            print(
                "\nEsta comunidade não permite a participação "
                f"da sua conta do tipo {self.estado.tipo_usuario_logado}."
            )
            return
        if ratname not in comunidade["membros"]:
            resposta = input(
                "\nDeseja fazer parte dessa Comunidade Rat? (s/n): "
            ).strip().lower()
            if resposta != "s":
                print("Você voltou ao menu de comunidades.")
                return
            comunidade["membros"].append(ratname)
            self._salvar(comunidades)
            if self.estado.tipo_usuario_logado == self.estado.TIPO_ESTUDANTE:
                self.ratcoins.registrar_ganho(
                    ratname,
                    f"Entrar na comunidade: {comunidade['nome']}",
                    10,
                    evento_id=f"comunidade-entrar:{comunidade['id']}:{ratname}",
                )
            print("Você agora faz parte dessa Comunidade Rat!")

        self._menu_publicacoes(comunidade, comunidades)

    def _menu_publicacoes(self, comunidade: dict, comunidades: list[dict]) -> None:
        while True:
            print(f"\n===== COMUNIDADE: {comunidade['nome']} =====")
            print("1. Ver publicações")
            print("2. Criar publicação")
            print("3. Responder publicação")
            print("4. Abrir chat da comunidade")
            print("5. Interagir com uma publicação")
            print("6. Consultar minhas publicações favoritas")
            print("0. Voltar às comunidades")
            opcao = input("Escolha uma opção: ").strip()
            acoes = {
                "1": lambda: self._ver_publicacoes(comunidade),
                "2": lambda: self._criar_publicacao(comunidade, comunidades),
                "3": lambda: self._responder_publicacao(comunidade, comunidades),
                "4": lambda: self._menu_chat(comunidade, comunidades),
                "5": lambda: self._interagir_publicacao(comunidade, comunidades),
                "6": lambda: self._consultar_favoritos(comunidades),
            }
            if opcao == "0":
                return
            acao = acoes.get(opcao)
            if acao is None:
                print("Opção inválida. Tente novamente.")
            else:
                acao()

    def _ver_publicacoes(self, comunidade: dict) -> None:
        print("\n===== PUBLICAÇÕES =====")
        publicacoes = comunidade["publicacoes"]
        if not publicacoes:
            print("Ainda não existem publicações nessa comunidade.")
            return
        for indice, publicacao in enumerate(publicacoes, start=1):
            print(f"\nPublicação {indice}")
            print(f"Autor: {publicacao['autor']}")
            print(f"Conteúdo: {publicacao['conteudo']}")
            if publicacao.get("material"):
                print(f"Material compartilhado: {publicacao['material']}")
            print(f"Likes: {len(publicacao['likes'])}")
            print(f"Dislikes: {len(publicacao['dislikes'])}")
            print("Respostas:")
            if not publicacao["respostas"]:
                print("Ainda não existem respostas.")
            for resposta in publicacao["respostas"]:
                print(f"- {resposta['autor']}: {resposta['conteudo']}")

    def _interagir_publicacao(
        self,
        comunidade: dict,
        comunidades: list[dict],
    ) -> None:
        ratname = self._usuario_atual()
        if ratname is None:
            return
        if ratname not in comunidade["membros"]:
            print("Você precisa entrar na comunidade para interagir com publicações.")
            return
        if not comunidade["publicacoes"]:
            print("Não existem publicações para interagir.")
            return

        self._ver_publicacoes(comunidade)
        publicacao = self._selecionar(
            comunidade["publicacoes"],
            "Digite o número da publicação que deseja interagir: ",
        )
        if publicacao is None:
            print("Não foi possível realizar a interação: publicação não encontrada.")
            return

        print("\n1. Curtir")
        print("2. Não curtir")
        print("3. Favoritar ou desfavoritar")
        opcao = input("Escolha uma interação: ").strip()

        if opcao not in ("1", "2", "3"):
            print("Opção de interação inválida.")
            return

        if opcao == "1":
            if ratname in publicacao["likes"]:
                publicacao["likes"].remove(ratname)
                print("Sua curtida foi retirada.")
            else:
                if ratname in publicacao["dislikes"]:
                    publicacao["dislikes"].remove(ratname)
                publicacao["likes"].append(ratname)
                print("Publicação curtida!")
        elif opcao == "2":
            if ratname in publicacao["dislikes"]:
                publicacao["dislikes"].remove(ratname)
                print("Seu dislike foi retirado.")
            else:
                if ratname in publicacao["likes"]:
                    publicacao["likes"].remove(ratname)
                publicacao["dislikes"].append(ratname)
                print("Publicação marcada como não curtida.")
        else:
            if ratname in publicacao["favoritos"]:
                publicacao["favoritos"].remove(ratname)
                print("Publicação removida dos favoritos.")
            else:
                publicacao["favoritos"].append(ratname)
                print("Publicação adicionada aos favoritos!")

        self._salvar(comunidades)
        print(
            f"Likes: {len(publicacao['likes'])} | "
            f"Dislikes: {len(publicacao['dislikes'])}"
        )

    def _consultar_favoritos(self, comunidades: list[dict]) -> None:
        ratname = self._usuario_atual()
        if ratname is None:
            return

        encontrados = []
        for comunidade in comunidades:
            for publicacao in comunidade["publicacoes"]:
                if ratname in publicacao["favoritos"]:
                    encontrados.append((comunidade, publicacao))

        print("\n===== MINHAS PUBLICAÇÕES FAVORITAS =====")
        if not encontrados:
            print("Você ainda não possui publicações favoritas.")
            return
        for indice, (comunidade, publicacao) in enumerate(encontrados, start=1):
            print(f"\n{indice}. Comunidade: {comunidade['nome']}")
            print(f"Autor: {publicacao['autor']}")
            print(f"Conteúdo: {publicacao['conteudo']}")
            if publicacao.get("material"):
                print(f"Material compartilhado: {publicacao['material']}")

    def _criar_publicacao(self, comunidade: dict, comunidades: list[dict]) -> None:
        if self.estado.usuario_logado not in comunidade["membros"]:
            print("Somente participantes podem publicar nesta comunidade.")
            return
        if not self._usuario_pode_acessar(self.estado.usuario_logado, comunidade):
            print("Sua conta não pode publicar nesta comunidade.")
            return
        print("\n===== NOVA PUBLICAÇÃO =====")
        conteudo = input("Escreva sua publicação: ").strip()
        if not conteudo:
            print("A publicação não pode ficar vazia.")
            return
        material = input(
            "Deseja compartilhar um link ou material? (Se não, deixe vazio): "
        ).strip()
        comunidade["publicacoes"].append(
            {
                "autor": self.estado.usuario_logado,
                "conteudo": conteudo,
                "material": material,
                "respostas": [],
                "likes": [],
                "dislikes": [],
                "favoritos": [],
            }
        )
        self._salvar(comunidades)
        print("Publicação criada com sucesso!")

    def _responder_publicacao(
        self,
        comunidade: dict,
        comunidades: list[dict],
    ) -> None:
        if self.estado.usuario_logado not in comunidade["membros"]:
            print("Somente participantes podem responder nesta comunidade.")
            return
        if not self._usuario_pode_acessar(self.estado.usuario_logado, comunidade):
            print("Sua conta não pode responder nesta comunidade.")
            return
        publicacoes = comunidade["publicacoes"]
        if not publicacoes:
            print("Não existem publicações para responder.")
            return
        self._ver_publicacoes(comunidade)
        publicacao = self._selecionar(
            publicacoes, "Digite o número da publicação que deseja responder: "
        )
        if publicacao is None:
            return
        resposta = input("Digite sua resposta: ").strip()
        if not resposta:
            print("A resposta não pode ficar vazia.")
            return
        publicacao["respostas"].append(
            {"autor": self.estado.usuario_logado, "conteudo": resposta}
        )
        self._salvar(comunidades)
        print("Resposta publicada com sucesso!")

    def _menu_chat(self, comunidade: dict, comunidades: list[dict]) -> None:
        ratname = self._usuario_atual()
        if ratname is None:
            return
        if ratname not in comunidade["membros"]:
            print("Somente participantes podem acessar o chat desta comunidade.")
            return
        if not self._usuario_pode_acessar(ratname, comunidade):
            print("Sua conta não pode participar do chat desta comunidade.")
            return

        while True:
            print(f"\n===== CHAT: {comunidade['nome']} =====")
            mensagens = comunidade["mensagens"]
            if not mensagens:
                print("Ainda não existem mensagens neste chat.")
            else:
                for mensagem in mensagens:
                    print(f"- {mensagem['autor']}: {mensagem['conteudo']}")
            print("\n1. Enviar mensagem")
            print("0. Voltar à comunidade")
            opcao = input("Escolha uma opção: ").strip()
            if opcao == "0":
                return
            if opcao != "1":
                print("Opção inválida.")
                continue

            conteudo = input("Digite sua mensagem: ").strip()
            if not conteudo:
                print("A mensagem não pode ficar vazia.")
                continue
            mensagens.append({"autor": ratname, "conteudo": conteudo})
            self._salvar(comunidades)
            print("Mensagem enviada.")

    def _usuario_atual(self) -> str | None:
        ratname = self.estado.usuario_logado
        if ratname is None:
            print("Você precisa fazer login para acessar as Comunidades Rat.")
        return ratname

    def _tipo_usuario(self, ratname: str | None) -> str | None:
        if not isinstance(ratname, str):
            return None
        usuario = next(
            (
                item
                for item in self.estado.usuarios
                if item.get("ratname") == ratname
            ),
            None,
        )
        if usuario is None:
            return None
        return usuario.get("tipo_usuario", self.estado.TIPO_ESTUDANTE)

    def _usuario_pode_acessar(self, ratname: str, comunidade: dict) -> bool:
        tipo_usuario = self._tipo_usuario(ratname)
        tipo_acesso = comunidade["tipo_acesso"]
        if tipo_acesso == self.TIPO_ESTUDANTES:
            return tipo_usuario == self.estado.TIPO_ESTUDANTE
        if tipo_acesso == self.TIPO_MONITORES:
            return tipo_usuario == self.estado.TIPO_MONITOR
        if tipo_acesso == self.TIPO_ESTUDANTES_MONITORES:
            return tipo_usuario in (
                self.estado.TIPO_ESTUDANTE,
                self.estado.TIPO_MONITOR,
            )
        return False

    def _nome_tipo_acesso(self, tipo_acesso: str) -> str:
        nomes = {
            self.TIPO_ESTUDANTES: "Apenas estudantes",
            self.TIPO_ESTUDANTES_MONITORES: "Estudantes e monitores",
            self.TIPO_MONITORES: "Apenas monitores",
        }
        return nomes[tipo_acesso]

    @staticmethod
    def _selecionar(itens: list[dict], pergunta: str) -> dict | None:
        if not itens:
            return None
        try:
            numero = int(input(pergunta).strip())
        except ValueError:
            print("Digite um número válido.")
            return None
        if numero < 1 or numero > len(itens):
            print("Item não encontrado.")
            return None
        return itens[numero - 1]

    @staticmethod
    def _exibir_detalhes(comunidade: dict) -> None:
        print("\n===== INFORMAÇÕES DA COMUNIDADE =====")
        print(f"Nome: {comunidade['nome']}")
        print(f"Disciplina: {comunidade['disciplina']}")
        print(f"Assunto: {comunidade['assunto']}")
        print(f"Descrição: {comunidade['descricao']}")
        print(f"Criador: {comunidade['criador']}")
        nomes = {
            GerenciadorComunidades.TIPO_ESTUDANTES: "Apenas estudantes",
            GerenciadorComunidades.TIPO_ESTUDANTES_MONITORES: "Estudantes e monitores",
            GerenciadorComunidades.TIPO_MONITORES: "Apenas monitores",
        }
        print(f"Público: {nomes[comunidade['tipo_acesso']]}")
        print(f"Participantes: {len(comunidade['membros'])}")
