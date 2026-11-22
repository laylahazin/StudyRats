from Dados import carregar_json, salvar_json


class EstadoAplicacao:
    TIPO_ESTUDANTE = "ESTUDANTE"
    TIPO_MONITOR = "MONITOR"

    SALAS_DISPONIVEIS = [
        {
            "id": "pp",
            "nome": "Sala de Principios de Programação",
            "materia": "Programação",
            "descricao": "Revisão dos princípios de programação.",
            "monitor": "Monitor responsável",
            "inicio": "13:00",
            "fim": "14:30",
            "capacidade": 10,
            "ativa": True,
        },
        {
            "id": "fund",
            "nome": "Sala de Fundamentos de Matemática",
            "materia": "Matemática",
            "descricao": "Revisão de conceitos fundamentais de matemática.",
            "monitor": "Monitor responsável",
            "inicio": "15:00",
            "fim": "16:30",
            "capacidade": 10,
            "ativa": True,
        },
        {
            "id": "adm",
            "nome": "Sala de Introdução à Administração",
            "materia": "Administração",
            "descricao": "Discussão de conceitos básicos de administração.",
            "monitor": "Monitor responsável",
            "inicio": "17:00",
            "fim": "18:30",
            "capacidade": 5,
            "ativa": True,
        },
        {
            "id": "pisi",
            "nome": "Sala de Projeto Interdisciplinar de Sistemas de Informação",
            "materia": "Pisi",
            "descricao": "Projeto interdisciplinar de sistemas de informação.",
            "monitor": "Monitor responsável",
            "inicio": "19:00",
            "fim": "20:30",
            "capacidade": 20,
            "ativa": True,
        },
        {
            "id": "sus",
            "nome": "Sala de Sustentabilidade em Sistemas de Informação",
            "materia": "Sustentabilidade",
            "descricao": "Sustentabilidade em Sistemas de Informação.",
            "monitor": "Monitor responsável",
            "inicio": "21:00",
            "fim": "22:00",
            "capacidade": 3,
            "ativa": True,
        },
    ]

    def __init__(self) -> None:
        self.usuarios = carregar_json("usuarios.json", [])
        if not isinstance(self.usuarios, list):
            raise ValueError(
                "O arquivo dados/usuarios.json deve conter uma lista de usuários."
            )
        self.usuario_logado = None
        self.salas_disponiveis = self.SALAS_DISPONIVEIS

    def salvar_usuarios(self) -> None:
        salvar_json("usuarios.json", self.usuarios)

    def definir_usuario_logado(self, ratname: str | None) -> None:
        global usuario_logado
        self.usuario_logado = ratname
        usuario_logado = ratname

    def substituir_usuarios(self, novos_usuarios: list[dict]) -> None:
        global usuarios
        self.usuarios = novos_usuarios
        usuarios = novos_usuarios

    @property
    def tipo_usuario_logado(self) -> str | None:
        if self.usuario_logado is None:
            return None

        usuario = next(
            (
                item
                for item in self.usuarios
                if item["ratname"] == self.usuario_logado
            ),
            None,
        )
        if usuario is None:
            raise ValueError("O usuário conectado não existe na lista de contas.")

        tipo_usuario = usuario.get("tipo_usuario", self.TIPO_ESTUDANTE)
        if tipo_usuario not in (self.TIPO_ESTUDANTE, self.TIPO_MONITOR):
            raise ValueError(
                f"O tipo de usuário salvo para '{self.usuario_logado}' é inválido."
            )
        return tipo_usuario


estado = EstadoAplicacao()
usuarios = estado.usuarios
usuario_logado = None
salas_disponiveis = estado.salas_disponiveis
