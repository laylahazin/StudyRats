from Dados import carregar_json, salvar_json  # Importa de Dados carregar_json, salvar_json, reutilizando os recursos centrais de persistencia e credenciais.


class EstadoAplicacao:  # Declara a classe EstadoAplicacao: mantem usuarios, usuario conectado e salas compartilhadas.
    TIPO_ESTUDANTE = "ESTUDANTE"  # Guarda em TIPO_ESTUDANTE o valor produzido por "ESTUDANTE".
    TIPO_MONITOR = "MONITOR"  # Guarda em TIPO_MONITOR o valor produzido por "MONITOR".

    SALAS_DISPONIVEIS = [  # Guarda em SALAS_DISPONIVEIS o valor produzido por [.
        {  # Executa nesta linha { no contexto desta funcionalidade.
            "id": "pp",  # Armazena na chave "id" o valor "pp", nesta estrutura.
            "nome": "Sala de Principios de Programação",  # Na chave "nome", define o nome exibido do modelo ou da sala; nesta entrada recebe "Sala de Principios de Programação",.
            "materia": "Programação",  # Na chave "materia", classifica a sala pela disciplina correspondente; nesta entrada recebe "Programação",.
            "descricao": "Revisão dos princípios de programação.",  # Na chave "descricao", fornece o texto explicativo exibido sobre a sala; nesta entrada recebe "Revisão dos princípios de programação.",.
            "monitor": "Monitor responsável",  # Na chave "monitor", identifica o responsavel pela sala ou atividade; nesta entrada recebe "Monitor responsável",.
            "inicio": "13:00",  # Na chave "inicio", define o horario inicial da sala no formato HH:MM; nesta entrada recebe "13:00",.
            "fim": "14:30",  # Na chave "fim", define o horario final da sala no formato HH:MM; nesta entrada recebe "14:30",.
            "capacidade": 10,  # Na chave "capacidade", limita o numero maximo de participantes da sala; nesta entrada recebe 10,.
            "ativa": True,  # Na chave "ativa", indica se a sala aceita participantes; nesta entrada recebe True,.
        },  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        {  # Executa nesta linha { no contexto desta funcionalidade.
            "id": "fund",  # Armazena na chave "id" o valor "fund", nesta estrutura.
            "nome": "Sala de Fundamentos de Matemática",  # Na chave "nome", define o nome exibido do modelo ou da sala; nesta entrada recebe "Sala de Fundamentos de Matemática",.
            "materia": "Matemática",  # Na chave "materia", classifica a sala pela disciplina correspondente; nesta entrada recebe "Matemática",.
            "descricao": "Revisão de conceitos fundamentais de matemática.",  # Na chave "descricao", fornece o texto explicativo exibido sobre a sala; nesta entrada recebe "Revisão de conceitos fundamentais de matemática.",.
            "monitor": "Monitor responsável",  # Na chave "monitor", identifica o responsavel pela sala ou atividade; nesta entrada recebe "Monitor responsável",.
            "inicio": "15:00",  # Na chave "inicio", define o horario inicial da sala no formato HH:MM; nesta entrada recebe "15:00",.
            "fim": "16:30",  # Na chave "fim", define o horario final da sala no formato HH:MM; nesta entrada recebe "16:30",.
            "capacidade": 10,  # Na chave "capacidade", limita o numero maximo de participantes da sala; nesta entrada recebe 10,.
            "ativa": True,  # Na chave "ativa", indica se a sala aceita participantes; nesta entrada recebe True,.
        },  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        {  # Executa nesta linha { no contexto desta funcionalidade.
            "id": "adm",  # Armazena na chave "id" o valor "adm", nesta estrutura.
            "nome": "Sala de Introdução à Administração",  # Na chave "nome", define o nome exibido do modelo ou da sala; nesta entrada recebe "Sala de Introdução à Administração",.
            "materia": "Administração",  # Na chave "materia", classifica a sala pela disciplina correspondente; nesta entrada recebe "Administração",.
            "descricao": "Discussão de conceitos básicos de administração.",  # Na chave "descricao", fornece o texto explicativo exibido sobre a sala; nesta entrada recebe "Discussão de conceitos básicos de administração.",.
            "monitor": "Monitor responsável",  # Na chave "monitor", identifica o responsavel pela sala ou atividade; nesta entrada recebe "Monitor responsável",.
            "inicio": "17:00",  # Na chave "inicio", define o horario inicial da sala no formato HH:MM; nesta entrada recebe "17:00",.
            "fim": "18:30",  # Na chave "fim", define o horario final da sala no formato HH:MM; nesta entrada recebe "18:30",.
            "capacidade": 5,  # Na chave "capacidade", limita o numero maximo de participantes da sala; nesta entrada recebe 5,.
            "ativa": True,  # Na chave "ativa", indica se a sala aceita participantes; nesta entrada recebe True,.
        },  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        {  # Executa nesta linha { no contexto desta funcionalidade.
            "id": "pisi",  # Armazena na chave "id" o valor "pisi", nesta estrutura.
            "nome": "Sala de Projeto Interdisciplinar de Sistemas de Informação",  # Na chave "nome", define o nome exibido do modelo ou da sala; nesta entrada recebe "Sala de Projeto Interdisciplinar de Sistemas de Informação",.
            "materia": "Pisi",  # Na chave "materia", classifica a sala pela disciplina correspondente; nesta entrada recebe "Pisi",.
            "descricao": "Projeto interdisciplinar de sistemas de informação.",  # Na chave "descricao", fornece o texto explicativo exibido sobre a sala; nesta entrada recebe "Projeto interdisciplinar de sistemas de informação.",.
            "monitor": "Monitor responsável",  # Na chave "monitor", identifica o responsavel pela sala ou atividade; nesta entrada recebe "Monitor responsável",.
            "inicio": "19:00",  # Na chave "inicio", define o horario inicial da sala no formato HH:MM; nesta entrada recebe "19:00",.
            "fim": "20:30",  # Na chave "fim", define o horario final da sala no formato HH:MM; nesta entrada recebe "20:30",.
            "capacidade": 20,  # Na chave "capacidade", limita o numero maximo de participantes da sala; nesta entrada recebe 20,.
            "ativa": True,  # Na chave "ativa", indica se a sala aceita participantes; nesta entrada recebe True,.
        },  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        {  # Executa nesta linha { no contexto desta funcionalidade.
            "id": "sus",  # Armazena na chave "id" o valor "sus", nesta estrutura.
            "nome": "Sala de Sustentabilidade em Sistemas de Informação",  # Na chave "nome", define o nome exibido do modelo ou da sala; nesta entrada recebe "Sala de Sustentabilidade em Sistemas de Informação",.
            "materia": "Sustentabilidade",  # Na chave "materia", classifica a sala pela disciplina correspondente; nesta entrada recebe "Sustentabilidade",.
            "descricao": "Sustentabilidade em Sistemas de Informação.",  # Na chave "descricao", fornece o texto explicativo exibido sobre a sala; nesta entrada recebe "Sustentabilidade em Sistemas de Informação.",.
            "monitor": "Monitor responsável",  # Na chave "monitor", identifica o responsavel pela sala ou atividade; nesta entrada recebe "Monitor responsável",.
            "inicio": "21:00",  # Na chave "inicio", define o horario inicial da sala no formato HH:MM; nesta entrada recebe "21:00",.
            "fim": "22:00",  # Na chave "fim", define o horario final da sala no formato HH:MM; nesta entrada recebe "22:00",.
            "capacidade": 3,  # Na chave "capacidade", limita o numero maximo de participantes da sala; nesta entrada recebe 3,.
            "ativa": True,  # Na chave "ativa", indica se a sala aceita participantes; nesta entrada recebe True,.
        },  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
    ]  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

    def __init__(self) -> None:  # Declara o metodo __init__: implementa esta funcionalidade da classe.
        self.usuarios = carregar_json("usuarios.json", [])  # representa a lista ou o mapa de usuarios usado pela operacao atual
        if not isinstance(self.usuarios, list):  # Testa a condicao not isinstance(self.usuarios, list) e executa o bloco seguinte somente quando ela for verdadeira.
            raise ValueError(  # Interrompe a operacao com ValueError(, indicando dados ou estado invalidos.
                "O arquivo dados/usuarios.json deve conter uma lista de usuários."  # Executa nesta linha "O arquivo dados/usuarios.json deve conter uma lista de usuários." no contexto desta funcionalidade.
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        self.usuario_logado = None  # Guarda em self.usuario_logado o valor produzido por None.
        self.salas_disponiveis = self.SALAS_DISPONIVEIS  # Guarda em self.salas_disponiveis o valor produzido por self.SALAS_DISPONIVEIS.

    def salvar_usuarios(self) -> None:  # Declara o metodo salvar_usuarios: implementa esta funcionalidade da classe.
        salvar_json("usuarios.json", self.usuarios)  # Executa nesta linha salvar_json("usuarios.json", self.usuarios) no contexto desta funcionalidade.

    def definir_usuario_logado(self, ratname: str | None) -> None:  # Declara o metodo definir_usuario_logado: implementa esta funcionalidade da classe.
        global usuario_logado  # Faz os nomes usuario_logado referirem-se a variaveis globais deste modulo.
        self.usuario_logado = ratname  # Guarda em self.usuario_logado o valor produzido por ratname.
        usuario_logado = ratname  # Guarda em usuario_logado o valor produzido por ratname.

    def substituir_usuarios(self, novos_usuarios: list[dict]) -> None:  # Declara o metodo substituir_usuarios: implementa esta funcionalidade da classe.
        global usuarios  # Faz os nomes usuarios referirem-se a variaveis globais deste modulo.
        self.usuarios = novos_usuarios  # representa a lista ou o mapa de usuarios usado pela operacao atual
        usuarios = novos_usuarios  # representa a lista ou o mapa de usuarios usado pela operacao atual

    @property  # Aplica o decorador ao metodo seguinte.
    def tipo_usuario_logado(self) -> str | None:  # Declara o metodo tipo_usuario_logado: implementa esta funcionalidade da classe.
        if self.usuario_logado is None:  # Testa a condicao self.usuario_logado is None e executa o bloco seguinte somente quando ela for verdadeira.
            return None  # Encerra o metodo e devolve ao chamador None.

        usuario = next(  # recupera o registro completo da conta atualmente conectada
            (  # Executa nesta linha ( no contexto desta funcionalidade.
                item  # Executa nesta linha item no contexto desta funcionalidade.
                for item in self.usuarios  # Percorre item in self.usuarios, executando o bloco uma vez para cada elemento.
                if item["ratname"] == self.usuario_logado  # Testa a condicao item["ratname"] == self.usuario_logado e executa o bloco seguinte somente quando ela for verdadeira.
            ),  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            None,  # Executa nesta linha None, no contexto desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        if usuario is None:  # Verifica que o registro da conta ativa nao foi encontrado.
            raise ValueError("O usuário conectado não existe na lista de contas.")  # Interrompe a operacao com ValueError("O usuário conectado não existe na lista de contas."), indicando dados ou estado invalidos.

        tipo_usuario = usuario.get("tipo_usuario", self.TIPO_ESTUDANTE)  # registra ESTUDANTE ou MONITOR para controlar os recursos disponiveis
        if tipo_usuario not in (self.TIPO_ESTUDANTE, self.TIPO_MONITOR):  # Testa a condicao tipo_usuario not in (self.TIPO_ESTUDANTE, self.TIPO_MONITOR) e executa o bloco seguinte somente quando ela for verdadeira.
            raise ValueError(  # Interrompe a operacao com ValueError(, indicando dados ou estado invalidos.
                f"O tipo de usuário salvo para '{self.usuario_logado}' é inválido."  # Executa nesta linha f"O tipo de usuário salvo para '{self.usuario_logado}' é inválido." no contexto desta funcionalidade.
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        return tipo_usuario  # Encerra o metodo e devolve ao chamador tipo_usuario.


estado = EstadoAplicacao()  # Guarda em estado o valor produzido por EstadoAplicacao().
usuarios = estado.usuarios  # representa a lista ou o mapa de usuarios usado pela operacao atual
usuario_logado = None  # Guarda em usuario_logado o valor produzido por None.
salas_disponiveis = estado.salas_disponiveis  # Guarda em salas_disponiveis o valor produzido por estado.salas_disponiveis.
