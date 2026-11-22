import lista  # Importa o modulo lista para compartilhar o estado global de login, perfil e usuarios desta aplicacao.
from Dados import persistencia  # Importa o gerenciador persistencia para ler e salvar os arquivos JSON desta funcionalidade.
from Horario import GerenciadorHorario  # Importa GerenciadorHorario para obter a data e o horario atual usados pela funcionalidade.
from Ratcoins import gerenciador_ratcoins  # Importa o gerenciador compartilhado usado para consultar saldos e registrar ganhos de RatCoins.


class Recompensas:  # Define a classe Recompensas, responsavel por recompensas por atividade e notificacoes aos lideres.
    RECOMPENSAS_POR_ACAO = (  # Define as descricoes e quantidades de pontos das atividades premiadas deste perfil.
        ("Estudar pelo menos 30 minutos no registro de presença", 15),  # Executa nesta linha da classe Recompensas e do metodo nivel do modulo a instrucao especifica: ("Estudar pelo menos 30 minutos no registro de presença", 15),
        ("Criar e usar o primeiro modelo de estudo", 15),  # Executa nesta linha da classe Recompensas e do metodo nivel do modulo a instrucao especifica: ("Criar e usar o primeiro modelo de estudo", 15),
        ("Entrar em uma sala de estudo (por sessão diária)", 20),  # Executa nesta linha da classe Recompensas e do metodo nivel do modulo a instrucao especifica: ("Entrar em uma sala de estudo (por sessão diária)", 20),
        ("Entrar em uma comunidade", 10),  # Executa nesta linha da classe Recompensas e do metodo nivel do modulo a instrucao especifica: ("Entrar em uma comunidade", 10),
        ("Criar uma comunidade", 20),  # Executa nesta linha da classe Recompensas e do metodo nivel do modulo a instrucao especifica: ("Criar uma comunidade", 20),
    )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
    RECOMPENSAS_MONITOR = (("Publicar uma atividade em uma sala de estudo", 5),)  # Define as descricoes e quantidades de pontos das atividades premiadas deste perfil.
    LINKS_CURSOS_GRATUITOS = (  # Define os pares nome-URL dos cursos gratuitos anexados as notificacoes de recompensa.
        ("freeCodeCamp", "https://www.freecodecamp.org/learn/"),  # Executa nesta linha da classe Recompensas e do metodo nivel do modulo a instrucao especifica: ("freeCodeCamp", "https://www.freecodecamp.org/learn/"),
        ("CS50x", "https://cs50.harvard.edu/x/"),  # Executa nesta linha da classe Recompensas e do metodo nivel do modulo a instrucao especifica: ("CS50x", "https://cs50.harvard.edu/x/"),
        ("The Odin Project", "https://www.theodinproject.com/"),  # Executa nesta linha da classe Recompensas e do metodo nivel do modulo a instrucao especifica: ("The Odin Project", "https://www.theodinproject.com/"),
    )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
    ARQUIVO_NOTIFICACOES = "notificacoes.json"  # Atribui a ARQUIVO_NOTIFICACOES o resultado desta expressao: "notificacoes.json"; esse valor sera usado nas proximas linhas.

    def __init__(self, horario: GerenciadorHorario | None = None) -> None:  # Declara o metodo __init__ nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self.estado = lista.estado  # Atribui ao objeto o estado global que informa usuario conectado, tipo de conta e usuarios cadastrados.
        self.ratcoins = gerenciador_ratcoins  # Atribui ao objeto o gerenciador compartilhado que consulta saldo e registra ganhos de RatCoins.
        self.persistencia = persistencia  # Atribui ao objeto o gerenciador central usado para carregar e salvar os dados JSON.
        self.horario = horario or GerenciadorHorario()  # Atribui ao objeto o gerenciador fornecido ou o gerenciador padrao usado para datas e lembretes.

    def menu(self) -> None:  # Declara o metodo menu nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self.estado.usuario_logado  # Atribui a ratname o resultado desta expressao: self.estado.usuario_logado; esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print("Você precisa fazer login para consultar suas recompensas.")  # Informa que o usuario precisestaar autenticado antes desta operacao.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        print("\n========== RATCOINS E RECOMPENSAS ==========")  # Exibe o cabecalho desta secao da interface: \n========== RATCOINS E RECOMPENSAS ==========.
        print(f"Saldo: {self.ratcoins.saldo(ratname)} RC")  # Exibe o saldo atual calculado em RatCoins nesta linha da interface.
        print("\nComo ganhar RatCoins:")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
        recompensas = (  # Atribui a recompensas o resultado desta expressao: (; esse valor sera usado nas proximas linhas.
            self.RECOMPENSAS_MONITOR  # Executa nesta linha da classe Recompensas e do metodo menu a instrucao especifica: self.RECOMPENSAS_MONITOR
            if self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR  # Compara o perfil conectado ao perfil autorizado pela condicao desta acao.
            else self.RECOMPENSAS_POR_ACAO  # Executa nesta linha da classe Recompensas e do metodo menu a instrucao especifica: else self.RECOMPENSAS_POR_ACAO
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        for descricao, pontos in recompensas:  # Percorre a colecao especificada nesta linha e repete a instrucao do bloco para cada elemento.
            print(f"- {descricao}: +{pontos} RC")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
        if self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR:  # Compara o perfil conectado ao perfil autorizado pela condicao desta acao.
            print("Publicações em comunidades e entradas em salas não geram bônus para monitores.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
        print("\n===== GERENCIAR RATCOINS =====")  # Exibe o cabecalho desta secao da interface: \n===== GERENCIAR RATCOINS =====.
        self.ratcoins.menu()  # Executa nesta linha da classe Recompensas e do metodo menu a instrucao especifica: self.ratcoins.menu()

    def verificar_notificacoes(self) -> None:  # Declara o metodo verificar_notificacoes nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self.estado.usuario_logado  # Atribui a ratname o resultado desta expressao: self.estado.usuario_logado; esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.

        notificacoes = self.persistencia.carregar(  # Le os dados persistidos ou aplica o valor padrao definido nesta chamada.
            self.ARQUIVO_NOTIFICACOES,  # Executa nesta linha da classe Recompensas e do metodo verificar_notificacoes a instrucao especifica: self.ARQUIVO_NOTIFICACOES,
            {"usuarios": {}, "datas_processadas": []},  # Inicia o objeto desta etapa e define nas linhas seguintes os campos e valores do novo registro.
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        if not isinstance(notificacoes, dict):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError("O arquivo notificacoes.json deve conter um objeto JSON.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        usuarios = notificacoes.setdefault("usuarios", {})  # Recupera a colecao da chave ou cria uma lista vazia antes de inserir o novo dado.
        datas_processadas = notificacoes.setdefault("datas_processadas", [])  # Recupera a colecao da chave ou cria uma lista vazia antes de inserir o novo dado.
        if (  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            not isinstance(usuarios, dict)  # Confere o tipo do dado antes de trata-lo como lista, objeto ou texto.
            or not isinstance(datas_processadas, list)  # Confere o tipo do dado antes de trata-lo como lista, objeto ou texto.
            or not all(isinstance(item, str) for item in datas_processadas)  # Confere o tipo do dado antes de trata-lo como lista, objeto ou texto.
        ):  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            raise ValueError("A estrutura do arquivo notificacoes.json está inválida.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.

        agora = self.horario.obter_horario_atual()  # Atribui a agora o resultado desta expressao: self.horario.obter_horario_atual(); esse valor sera usado nas proximas linhas.
        if agora.month in (1, 8) and agora.day == 1:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            self._notificar_lideres(notificacoes, agora.year, agora.month)  # Executa nesta linha da classe Recompensas e do metodo verificar_notificacoes a instrucao especifica: self._notificar_lideres(notificacoes, agora.year, agora.month)

        pendentes = usuarios.get(ratname, [])  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
        if not isinstance(pendentes, list):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError(f"As notificações de '{ratname}' estão inválidas.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        alterado = False  # Atribui a alterado o resultado desta expressao: False; esse valor sera usado nas proximas linhas.
        for notificacao in pendentes:  # Percorre cada notificacao pendente da conta atual para entrega ao usuario.
            if not isinstance(notificacao, dict):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                raise ValueError(f"Uma notificação de '{ratname}' está inválida.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
            if notificacao.get("lida"):  # Ignorestaa notificacao quando ela ja foi marcada como lida anteriormente.
                continue  # Encerra apenas a iteracao atual do loop e passa diretamente para o proximo elemento ou opcao.
            print(f"\n===== NOTIFICAÇÃO =====\n{notificacao['mensagem']}")  # Exibe o cabecalho desta secao da interface: ]}.
            print("Sua recompensa inclui estes cursos de programação gratuitos:")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            for nome, url in notificacao["links"]:  # Percorre cada notificacao pendente da conta atual para entrega ao usuario.
                print(f"- {nome}: {url}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            notificacao["lida"] = True  # Executa nesta linha da classe Recompensas e do metodo verificar_notificacoes a instrucao especifica: notificacao["lida"] = True
            alterado = True  # Atribui a alterado o resultado desta expressao: True; esse valor sera usado nas proximas linhas.
        if alterado:  # So persiste novamente se pelo menos uma notificacao ou registro foi realmente alterado.
            self.persistencia.salvar(self.ARQUIVO_NOTIFICACOES, notificacoes)  # Persiste no arquivo JSON estarutura atualizada desta operacao.

    def _notificar_lideres(  # Declara o metodo _notificar_lideres nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self,  # Executa nesta linha da classe Recompensas e do metodo _notificar_lideres a instrucao especifica: self,
        notificacoes: dict,  # Executa nesta linha da classe Recompensas e do metodo _notificar_lideres a instrucao especifica: notificacoes: dict,
        ano: int,  # Executa nesta linha da classe Recompensas e do metodo _notificar_lideres a instrucao especifica: ano: int,
        mes: int,  # Executa nesta linha da classe Recompensas e do metodo _notificar_lideres a instrucao especifica: mes: int,
    ) -> None:  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        usuarios = notificacoes["usuarios"]  # Atribui a usuarios o resultado desta expressao: notificacoes["usuarios"]; esse valor sera usado nas proximas linhas.
        datas_processadas = notificacoes["datas_processadas"]  # Atribui a datas_processadas o resultado desta expressao: notificacoes["datas_processadas"]; esse valor sera usado nas proximas linhas.
        alterado = False  # Atribui a alterado o resultado desta expressao: False; esse valor sera usado nas proximas linhas.
        for tipo_usuario in (self.estado.TIPO_ESTUDANTE, self.estado.TIPO_MONITOR):  # Percorre cada perfil premiavel e calcula seu ranking separadamente.
            evento_id = f"{ano}-{mes:02d}:{tipo_usuario}"  # Atribui a evento_id o resultado desta expressao: f"{ano}-{mes:02d}:{tipo_usuario}"; esse valor sera usado nas proximas linhas.
            if evento_id in datas_processadas:  # Impede processar novamente o mesmo perfil no mesmo ano e mes.
                continue  # Encerra apenas a iteracao atual do loop e passa diretamente para o proximo elemento ou opcao.
            contas = [  # Atribui a contas o resultado desta expressao: [; esse valor sera usado nas proximas linhas.
                usuario  # Executa nesta linha da classe Recompensas e do metodo _notificar_lideres a instrucao especifica: usuario
                for usuario in self.estado.usuarios  # Percorre a colecao especificada nesta linha e repete a instrucao do bloco para cada elemento.
                if usuario.get("tipo_usuario", self.estado.TIPO_ESTUDANTE)  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
                == tipo_usuario  # Executa nesta linha da classe Recompensas e do metodo _notificar_lideres a instrucao especifica: == tipo_usuario
            ]  # Executa nesta linha da classe Recompensas e do metodo _notificar_lideres a instrucao especifica: ]
            ranking = sorted(  # Ordena os registros pela chave declarada nesta chamada.
                (  # Executa nesta linha da classe Recompensas e do metodo _notificar_lideres a instrucao especifica: (
                    (conta["ratname"], self.ratcoins.saldo(conta["ratname"]))  # Executa nesta linha da classe Recompensas e do metodo _notificar_lideres a instrucao especifica: (conta["ratname"], self.ratcoins.saldo(conta["ratname"]))
                    for conta in contas  # Percorre a colecao especificada nesta linha e repete a instrucao do bloco para cada elemento.
                ),  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
                key=lambda item: (-item[1], item[0].casefold()),  # Normaliza nomes ou pesquisas para uma comparacao consistente.
            )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            if not ranking:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                continue  # Encerra apenas a iteracao atual do loop e passa diretamente para o proximo elemento ou opcao.
            vencedor = ranking[0][0]  # Atribui a vencedor o resultado desta expressao: ranking[0][0]; esse valor sera usado nas proximas linhas.
            usuarios.setdefault(vencedor, []).append(  # Recupera a colecao da chave ou cria uma lista vazia antes de inserir o novo dado.
                {  # Inicia o objeto desta etapa e define nas linhas seguintes os campos e valores do novo registro.
                    "evento_id": evento_id,  # Define a chave "evento_id" destestarutura para representar o identificador unico do ganho ou ajuste.
                    "mensagem": (  # Define a chave "mensagem" destestarutura para representar o texto da notificacao.
                        f"Parabéns, {vencedor}! Você ficou em 1º lugar no "  # Executa nesta linha da classe Recompensas e do metodo _notificar_lideres a instrucao especifica: f"Parabéns, {vencedor}! Você ficou em 1º lugar no "
                        f"ranking de {tipo_usuario.lower()} em "  # Normaliza a caixa do texto para comparar a escolha digitada.
                        f"{mes:02d}/{ano} e recebeu uma recompensa."  # Executa nesta linha da classe Recompensas e do metodo _notificar_lideres a instrucao especifica: f"{mes:02d}/{ano} e recebeu uma recompensa."
                    ),  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
                    "links": [list(item) for item in self.LINKS_CURSOS_GRATUITOS],  # Define a chave "links" destestarutura para representar os cursos gratuitos anexados.
                    "lida": False,  # Define a chave "lida" destestarutura para representar se a notificacao foi lida.
                }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
            )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            datas_processadas.append(evento_id)  # Insere no fim da colecao o registro ou texto criado nesta etapa.
            alterado = True  # Atribui a alterado o resultado desta expressao: True; esse valor sera usado nas proximas linhas.
        if alterado:  # So persiste novamente se pelo menos uma notificacao ou registro foi realmente alterado.
            self.persistencia.salvar(self.ARQUIVO_NOTIFICACOES, notificacoes)  # Persiste no arquivo JSON estarutura atualizada desta operacao.
