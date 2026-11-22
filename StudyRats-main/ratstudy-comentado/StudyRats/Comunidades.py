from uuid import uuid4  # Importa uuid4 para gerar identificadores exclusivos de comunidades e eventos processados.

import lista  # Importa o modulo lista para compartilhar o estado global de login, perfil e usuarios desta aplicacao.
from Dados import persistencia  # Importa o gerenciador persistencia para ler e salvar os arquivos JSON desta funcionalidade.
from Ratcoins import gerenciador_ratcoins  # Importa o gerenciador compartilhado usado para consultar saldos e registrar ganhos de RatCoins.


class GerenciadorComunidades:  # Define a classe GerenciadorComunidades, responsavel por comunidades, participantes, publicacoes e chat.
    ARQUIVO = "comunidades.json"  # Define o arquivo JSON comunidades.json como destino e origem da persistencia desta funcionalidade.
    TIPO_ESTUDANTES = "ESTUDANTES"  # Define o codigo interno usado nesta classe para representar um tipo de acesso ou perfil.
    TIPO_ESTUDANTES_MONITORES = "ESTUDANTES_MONITORES"  # Define o codigo interno usado nesta classe para representar um tipo de acesso ou perfil.
    TIPO_MONITORES = "MONITORES"  # Define o codigo interno usado nesta classe para representar um tipo de acesso ou perfil.

    def __init__(self) -> None:  # Declara o metodo __init__ nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self.estado = lista.estado  # Atribui ao objeto o estado global que informa usuario conectado, tipo de conta e usuarios cadastrados.
        self.persistencia = persistencia  # Atribui ao objeto o gerenciador central usado para carregar e salvar os dados JSON.
        self.ratcoins = gerenciador_ratcoins  # Atribui ao objeto o gerenciador compartilhado que consulta saldo e registra ganhos de RatCoins.

    def _carregar(self) -> list[dict]:  # Declara o metodo _carregar nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        comunidades = self.persistencia.carregar(self.ARQUIVO, [])  # Le os dados persistidos ou aplica o valor padrao definido nesta chamada.
        if not isinstance(comunidades, list):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError("O arquivo comunidades.json deve conter uma lista.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.

        alterado = False  # Atribui a alterado o resultado desta expressao: False; esse valor sera usado nas proximas linhas.
        for comunidade in comunidades:  # Percorre cada comunidade carregada para listar, pesquisar, validar ou reunir favoritos.
            if not isinstance(comunidade, dict):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                raise ValueError("Uma comunidade salva possui formato inválido.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
            if "disciplina" not in comunidade and "disciplina(s)" in comunidade:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                comunidade["disciplina"] = comunidade["disciplina(s)"]  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: comunidade["disciplina"] = comunidade["disciplina(s)"]
                alterado = True  # Atribui a alterado o resultado desta expressao: True; esse valor sera usado nas proximas linhas.
            if "assunto" not in comunidade and "tag" in comunidade:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                comunidade["assunto"] = comunidade["tag"]  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: comunidade["assunto"] = comunidade["tag"]
                alterado = True  # Atribui a alterado o resultado desta expressao: True; esse valor sera usado nas proximas linhas.
            if "tipo_acesso" not in comunidade:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                tipo_criador = self._tipo_usuario(comunidade.get("criador"))  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
                comunidade["tipo_acesso"] = (  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: comunidade["tipo_acesso"] = (
                    self.TIPO_MONITORES  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: self.TIPO_MONITORES
                    if tipo_criador == self.estado.TIPO_MONITOR  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
                    else self.TIPO_ESTUDANTES  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: else self.TIPO_ESTUDANTES
                )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
                alterado = True  # Atribui a alterado o resultado desta expressao: True; esse valor sera usado nas proximas linhas.
            if comunidade["tipo_acesso"] not in (  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                self.TIPO_ESTUDANTES,  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: self.TIPO_ESTUDANTES,
                self.TIPO_ESTUDANTES_MONITORES,  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: self.TIPO_ESTUDANTES_MONITORES,
                self.TIPO_MONITORES,  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: self.TIPO_MONITORES,
            ):  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
                raise ValueError(  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
                    f"O público da comunidade '{comunidade['nome']}' está inválido."  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: f"O público da comunidade '{comunidade['nome']}' está inválido."
                )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            for campo in ("nome", "disciplina", "assunto", "descricao", "criador"):  # Percorre cada campo obrigatorio e valida seu tipo ou existencia no registro.
                if not isinstance(comunidade.get(campo), str):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                    raise ValueError(f"O campo '{campo}' de uma comunidade está inválido.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
            if "id" not in comunidade:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                comunidade["id"] = uuid4().hex  # Gera uma identificacao hexadecimal unica para o registro ou evento.
                alterado = True  # Atribui a alterado o resultado desta expressao: True; esse valor sera usado nas proximas linhas.
            if "membros" not in comunidade:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                comunidade["membros"] = [comunidade["criador"]]  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: comunidade["membros"] = [comunidade["criador"]]
                alterado = True  # Atribui a alterado o resultado desta expressao: True; esse valor sera usado nas proximas linhas.
            if "publicacoes" not in comunidade:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                comunidade["publicacoes"] = []  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: comunidade["publicacoes"] = []
                alterado = True  # Atribui a alterado o resultado desta expressao: True; esse valor sera usado nas proximas linhas.
            if "mensagens" not in comunidade:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                comunidade["mensagens"] = []  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: comunidade["mensagens"] = []
                alterado = True  # Atribui a alterado o resultado desta expressao: True; esse valor sera usado nas proximas linhas.
            if not isinstance(comunidade["membros"], list):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                raise ValueError(f"Os membros da comunidade '{comunidade['nome']}' estão inválidos.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
            if not isinstance(comunidade["publicacoes"], list):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                raise ValueError(f"As publicações da comunidade '{comunidade['nome']}' estão inválidas.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
            if not isinstance(comunidade["mensagens"], list):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                raise ValueError(f"As mensagens da comunidade '{comunidade['nome']}' estão inválidas.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
            for publicacao in comunidade["publicacoes"]:  # Percorre cada comunidade carregada para listar, pesquisar, validar ou reunir favoritos.
                if not isinstance(publicacao, dict):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                    raise ValueError("Uma publicação da comunidade possui formato inválido.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
                for campo in ("likes", "dislikes", "favoritos"):  # Percorre cada campo obrigatorio e valida seu tipo ou existencia no registro.
                    if campo not in publicacao:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                        publicacao[campo] = []  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: publicacao[campo] = []
                        alterado = True  # Atribui a alterado o resultado desta expressao: True; esse valor sera usado nas proximas linhas.
                    if not isinstance(publicacao[campo], list):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                        raise ValueError("As interações de uma publicação estão inválidas.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.

        if alterado:  # So persiste novamente se pelo menos uma notificacao ou registro foi realmente alterado.
            self._salvar(comunidades)  # Executa nesta linha da classe GerenciadorComunidades e do metodo _carregar a instrucao especifica: self._salvar(comunidades)
        return comunidades  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

    def _salvar(self, comunidades: list[dict]) -> None:  # Declara o metodo _salvar nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self.persistencia.salvar(self.ARQUIVO, comunidades)  # Persiste no arquivo JSON estarutura atualizada desta operacao.

    def menu(self) -> None:  # Declara o metodo menu nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        if self._usuario_atual() is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        while True:  # Mantem o loop ativo enquanto a condicao desta linha permanece verdadeira, encerrando-o por return ou escolha de saida.
            print("\n========== COMUNIDADES RAT ==========")  # Exibe o cabecalho desta secao da interface: \n========== COMUNIDADES RAT ==========.
            print("1. Ver todas as comunidades")  # Exibe na tela a opcao numero 1 com o texto e a acao correspondentes estae menu.
            print("2. Pesquisar comunidades")  # Exibe na tela a opcao numero 2 com o texto e a acao correspondentes estae menu.
            print("3. Entrar em uma comunidade")  # Exibe na tela a opcao numero 3 com o texto e a acao correspondentes estae menu.
            print("4. Criar comunidade")  # Exibe na tela a opcao numero 4 com o texto e a acao correspondentes estae menu.
            print("5. Editar minha comunidade")  # Exibe na tela a opcao numero 5 com o texto e a acao correspondentes estae menu.
            print("6. Excluir minha comunidade")  # Exibe na tela a opcao numero 6 com o texto e a acao correspondentes estae menu.
            print("0. Voltar ao menu principal")  # Exibe a opcao 0, que encerrestaa tela e volta ao menu anterior.
            opcao = input("Escolha uma opção: ").strip()  # Atribui a opcao a resposta digitada no prompt Escolha uma opção: , removendo espacos externos antes da validacao.
            acoes = {  # Atribui a acoes o resultado desta expressao: {; esse valor sera usado nas proximas linhas.
                "1": self.listar,  # Define a chave "1" destestarutura para representar o valor especifico desta entrada.
                "2": self.pesquisar,  # Define a chave "2" destestarutura para representar o valor especifico desta entrada.
                "3": self.entrar,  # Define a chave "3" destestarutura para representar o valor especifico desta entrada.
                "4": self.criar,  # Define a chave "4" destestarutura para representar o valor especifico desta entrada.
                "5": self.editar,  # Define a chave "5" destestarutura para representar o valor especifico desta entrada.
                "6": self.excluir,  # Define a chave "6" destestarutura para representar o valor especifico desta entrada.
            }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
            if opcao == "0":  # Executestaa ramificacao somente quando a escolha digitada for exatamente o numero ou texto indicado.
                return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
            acao = acoes.get(opcao)  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
            if acao is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
                print("Opção inválida. Tente novamente.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            else:  # Executa o tratamento do caso restante que nao satisfez as condicoes anteriores desta decisao.
                acao()  # Executa nesta linha da classe GerenciadorComunidades e do metodo menu a instrucao especifica: acao()

    def listar(self) -> None:  # Declara o metodo listar nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        comunidades = self._carregar()  # Atribui a comunidades o resultado desta expressao: self._carregar(); esse valor sera usado nas proximas linhas.
        print("\n===== COMUNIDADES RAT =====")  # Exibe o cabecalho desta secao da interface: \n===== COMUNIDADES RAT =====.
        if not comunidades:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Ainda não existem comunidades cadastradas.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        for indice, comunidade in enumerate(comunidades, start=1):  # Percorre cada comunidade carregada para listar, pesquisar, validar ou reunir favoritos.
            print(f"\n{indice}. {comunidade['nome']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            print(f"Disciplina: {comunidade['disciplina']}")  # Exibe a disciplina da comunidade atual nesta linha da interface.
            print(f"Assunto: {comunidade['assunto']}")  # Exibe o assunto da comunidade atual nesta linha da interface.
            print(f"Público: {self._nome_tipo_acesso(comunidade['tipo_acesso'])}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            print(f"Participantes: {len(comunidade['membros'])}")  # Exibe a quantidade atual de participantes nesta linha da interface.

    def pesquisar(self) -> None:  # Declara o metodo pesquisar nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        comunidades = self._carregar()  # Atribui a comunidades o resultado desta expressao: self._carregar(); esse valor sera usado nas proximas linhas.
        print("\n===== PESQUISAR COMUNIDADES =====")  # Exibe o cabecalho desta secao da interface: \n===== PESQUISAR COMUNIDADES =====.
        pesquisa = input("Digite o nome, disciplina ou assunto: ").strip().casefold()  # Atribui a pesquisa a resposta digitada no prompt Digite o nome, disciplina ou assunto: , removendo espacos externos antes da validacao.
        if not pesquisa:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Digite algo para pesquisar.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.

        resultados = [  # Atribui a resultados o resultado desta expressao: [; esse valor sera usado nas proximas linhas.
            comunidade  # Executa nesta linha da classe GerenciadorComunidades e do metodo pesquisar a instrucao especifica: comunidade
            for comunidade in comunidades  # Percorre cada comunidade carregada para listar, pesquisar, validar ou reunir favoritos.
            if any(  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
                pesquisa in comunidade[campo].casefold()  # Normaliza nomes ou pesquisas para uma comparacao consistente.
                for campo in ("nome", "disciplina", "assunto")  # Percorre cada campo obrigatorio e valida seu tipo ou existencia no registro.
            )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        ]  # Executa nesta linha da classe GerenciadorComunidades e do metodo pesquisar a instrucao especifica: ]
        if not resultados:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Nenhuma comunidade encontrada.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        for indice, comunidade in enumerate(resultados, start=1):  # Percorre cada comunidade carregada para listar, pesquisar, validar ou reunir favoritos.
            print(f"\n{indice}. {comunidade['nome']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            print(f"Disciplina: {comunidade['disciplina']}")  # Exibe a disciplina da comunidade atual nesta linha da interface.
            print(f"Assunto: {comunidade['assunto']}")  # Exibe o assunto da comunidade atual nesta linha da interface.

    def criar(self) -> None:  # Declara o metodo criar nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self._usuario_atual()  # Atribui a ratname o resultado desta expressao: self._usuario_atual(); esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        comunidades = self._carregar()  # Atribui a comunidades o resultado desta expressao: self._carregar(); esse valor sera usado nas proximas linhas.
        print("\n===== CRIAR COMUNIDADE RAT =====")  # Exibe o cabecalho desta secao da interface: \n===== CRIAR COMUNIDADE RAT =====.
        tipo_usuario = self.estado.tipo_usuario_logado  # Atribui a tipo_usuario o resultado desta expressao: self.estado.tipo_usuario_logado; esse valor sera usado nas proximas linhas.
        if tipo_usuario == self.estado.TIPO_ESTUDANTE:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print("Público da comunidade:")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            print("1. Apenas estudantes")  # Exibe na tela a opcao numero 1 com o texto e a acao correspondentes estae menu.
            print("2. Estudantes e monitores")  # Exibe na tela a opcao numero 2 com o texto e a acao correspondentes estae menu.
            opcao_acesso = input("Escolha o público: ").strip()  # Atribui a opcao_acesso a resposta digitada no prompt Escolha o público: , removendo espacos externos antes da validacao.
            if opcao_acesso == "1":  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
                tipo_acesso = self.TIPO_ESTUDANTES  # Atribui a tipo_acesso o resultado desta expressao: self.TIPO_ESTUDANTES; esse valor sera usado nas proximas linhas.
            elif opcao_acesso == "2":  # Avaliestaa alternativa apenas depois das condicoes anteriores serem falsas, usando os valores desta ramificacao.
                tipo_acesso = self.TIPO_ESTUDANTES_MONITORES  # Atribui a tipo_acesso o resultado desta expressao: self.TIPO_ESTUDANTES_MONITORES; esse valor sera usado nas proximas linhas.
            else:  # Executa o tratamento do caso restante que nao satisfez as condicoes anteriores desta decisao.
                print("Opção de público inválida.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
                return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        elif tipo_usuario == self.estado.TIPO_MONITOR:  # Avaliestaa alternativa apenas depois das condicoes anteriores serem falsas, usando os valores desta ramificacao.
            print("Como monitor, esta comunidade será exclusiva para monitores.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            tipo_acesso = self.TIPO_MONITORES  # Atribui a tipo_acesso o resultado desta expressao: self.TIPO_MONITORES; esse valor sera usado nas proximas linhas.
        else:  # Executa o tratamento do caso restante que nao satisfez as condicoes anteriores desta decisao.
            print("Tipo de usuário inválido.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.

        nome = input("Nome da comunidade: ").strip()  # Atribui a nome a resposta digitada no prompt Nome da comunidade: , removendo espacos externos antes da validacao.
        if not nome:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("O nome da comunidade não pode ficar vazio.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if any(comunidade["nome"].casefold() == nome.casefold() for comunidade in comunidades):  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print("Já existe uma comunidade com esse nome.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.

        disciplina = input("Disciplina(s): ").strip()  # Atribui a disciplina a resposta digitada no prompt Disciplina(s): , removendo espacos externos antes da validacao.
        tag = input("Assunto de interesse: ").strip()  # Atribui a tag a resposta digitada no prompt Assunto de interesse: , removendo espacos externos antes da validacao.
        descricao = input("Descrição da comunidade: ").strip()  # Atribui a descricao a resposta digitada no prompt Descrição da comunidade: , removendo espacos externos antes da validacao.
        if not disciplina or not tag or not descricao:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Preencha todas as informações.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.

        id_comunidade = uuid4().hex  # Gera uma identificacao hexadecimal unica para o registro ou evento.
        comunidade = {  # Atribui a comunidade o resultado desta expressao: {; esse valor sera usado nas proximas linhas.
            "id": id_comunidade,  # Define a chave "id" destestarutura para representar o identificador unico da comunidade.
            "nome": nome,  # Define a chave "nome" destestarutura para representar o nome da comunidade.
            "disciplina": disciplina,  # Define a chave "disciplina" destestarutura para representar a disciplina associada.
            "assunto": tag,  # Define a chave "assunto" destestarutura para representar o assunto da comunidade.
            "descricao": descricao,  # Define a chave "descricao" destestarutura para representar a descricao do estudo ou comunidade.
            "criador": ratname,  # Define a chave "criador" destestarutura para representar o ratname do criador.
            "tipo_acesso": tipo_acesso,  # Define a chave "tipo_acesso" destestarutura para representar o publico autorizado.
            "membros": [ratname],  # Define a chave "membros" destestarutura para representar os ratnames participantes.
            "publicacoes": [],  # Define a chave "publicacoes" destestarutura para representar as publicacoes da comunidade.
            "mensagens": [],  # Define a chave "mensagens" destestarutura para representar as mensagens do chat.
        }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
        comunidades.append(comunidade)  # Insere no fim da colecao o registro ou texto criado nesta etapa.
        self._salvar(comunidades)  # Executa nesta linha da classe GerenciadorComunidades e do metodo criar a instrucao especifica: self._salvar(comunidades)
        if self.estado.tipo_usuario_logado == self.estado.TIPO_ESTUDANTE:  # Compara o perfil conectado ao perfil autorizado pela condicao desta acao.
            self.ratcoins.registrar_ganho(  # Solicita ao gerenciador o credito desta atividade usando o identificador unico do evento.
                ratname,  # Executa nesta linha da classe GerenciadorComunidades e do metodo criar a instrucao especifica: ratname,
                f"Criar comunidade: {nome}",  # Executa nesta linha da classe GerenciadorComunidades e do metodo criar a instrucao especifica: f"Criar comunidade: {nome}",
                20,  # Executa nesta linha da classe GerenciadorComunidades e do metodo criar a instrucao especifica: 20,
                evento_id=f"comunidade-criar:{id_comunidade}",  # Atribui a evento_id o resultado desta expressao: f"comunidade-criar:{id_comunidade}",; esse valor sera usado nas proximas linhas.
            )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        print("\nComunidade criada com sucesso!")  # Informa ao usuario o resultado concluido ou cancelado desta operacao.
        print("Você já faz parte dela como criador.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.

    def editar(self) -> None:  # Declara o metodo editar nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        comunidades = self._carregar()  # Atribui a comunidades o resultado desta expressao: self._carregar(); esse valor sera usado nas proximas linhas.
        self.listar()  # Executa nesta linha da classe GerenciadorComunidades e do metodo editar a instrucao especifica: self.listar()
        comunidade = self._selecionar(comunidades, "Digite o número da comunidade que deseja editar: ")  # Atribui a comunidade o resultado desta expressao: self._selecionar(comunidades, "Digite o número da comunidade que deseja editar: "); esse valor sera usado nas proximas linhas.
        if comunidade is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if comunidade["criador"] != self.estado.usuario_logado:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print("Somente o criador pode editar essa comunidade.")  # Informa que o perfil, criador ou participante nao satisfaz a exigencia desta acao.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.

        print("\nDeixe em branco o que não deseja alterar.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
        novo_nome = input("Novo nome: ").strip()  # Atribui a novo_nome a resposta digitada no prompt Novo nome: , removendo espacos externos antes da validacao.
        nova_disciplina = input("Nova disciplina: ").strip()  # Atribui a nova_disciplina a resposta digitada no prompt Nova disciplina: , removendo espacos externos antes da validacao.
        novo_assunto = input("Novo assunto: ").strip()  # Atribui a novo_assunto a resposta digitada no prompt Novo assunto: , removendo espacos externos antes da validacao.
        nova_descricao = input("Nova descrição: ").strip()  # Atribui a nova_descricao a resposta digitada no prompt Nova descrição: , removendo espacos externos antes da validacao.
        if novo_nome and any(  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            outra is not comunidade and outra["nome"].casefold() == novo_nome.casefold()  # Normaliza nomes ou pesquisas para uma comparacao consistente.
            for outra in comunidades  # Percorre cada comunidade carregada para listar, pesquisar, validar ou reunir favoritos.
        ):  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            print("Já existe outra comunidade com esse nome.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if novo_nome:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            comunidade["nome"] = novo_nome  # Executa nesta linha da classe GerenciadorComunidades e do metodo editar a instrucao especifica: comunidade["nome"] = novo_nome
        if nova_disciplina:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            comunidade["disciplina"] = nova_disciplina  # Executa nesta linha da classe GerenciadorComunidades e do metodo editar a instrucao especifica: comunidade["disciplina"] = nova_disciplina
        if novo_assunto:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            comunidade["assunto"] = novo_assunto  # Executa nesta linha da classe GerenciadorComunidades e do metodo editar a instrucao especifica: comunidade["assunto"] = novo_assunto
        if nova_descricao:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            comunidade["descricao"] = nova_descricao  # Executa nesta linha da classe GerenciadorComunidades e do metodo editar a instrucao especifica: comunidade["descricao"] = nova_descricao
        self._salvar(comunidades)  # Executa nesta linha da classe GerenciadorComunidades e do metodo editar a instrucao especifica: self._salvar(comunidades)
        print("Comunidade atualizada com sucesso!")  # Informa ao usuario o resultado concluido ou cancelado desta operacao.

    def excluir(self) -> None:  # Declara o metodo excluir nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        comunidades = self._carregar()  # Atribui a comunidades o resultado desta expressao: self._carregar(); esse valor sera usado nas proximas linhas.
        self.listar()  # Executa nesta linha da classe GerenciadorComunidades e do metodo excluir a instrucao especifica: self.listar()
        comunidade = self._selecionar(comunidades, "Digite o número da comunidade que deseja excluir: ")  # Atribui a comunidade o resultado desta expressao: self._selecionar(comunidades, "Digite o número da comunidade que deseja excluir: "); esse valor sera usado nas proximas linhas.
        if comunidade is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if comunidade["criador"] != self.estado.usuario_logado:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print("Somente o criador pode excluir essa comunidade.")  # Informa que o perfil, criador ou participante nao satisfaz a exigencia desta acao.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        confirmacao = input(  # Atribui a confirmacao a resposta digitada no prompt campo solicitado, removendo espacos externos antes da validacao.
            f"Tem certeza que deseja excluir '{comunidade['nome']}'? (s/n): "  # Executa nesta linha da classe GerenciadorComunidades e do metodo excluir a instrucao especifica: f"Tem certeza que deseja excluir '{comunidade['nome']}' (s/n): "
        ).strip().lower()  # Remove espacos externos antes da validacao ou armazenamento da entrada.
        if confirmacao != "s":  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print("Exclusão cancelada.")  # Informa ao usuario o resultado concluido ou cancelado desta operacao.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        comunidades.remove(comunidade)  # Remove da colecao o elemento identificado pela acao atual.
        self._salvar(comunidades)  # Executa nesta linha da classe GerenciadorComunidades e do metodo excluir a instrucao especifica: self._salvar(comunidades)
        print("Comunidade excluída com sucesso!")  # Informa ao usuario o resultado concluido ou cancelado desta operacao.

    def entrar(self) -> None:  # Declara o metodo entrar nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self._usuario_atual()  # Atribui a ratname o resultado desta expressao: self._usuario_atual(); esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        comunidades = self._carregar()  # Atribui a comunidades o resultado desta expressao: self._carregar(); esse valor sera usado nas proximas linhas.
        self.listar()  # Executa nesta linha da classe GerenciadorComunidades e do metodo entrar a instrucao especifica: self.listar()
        comunidade = self._selecionar(  # Atribui a comunidade o resultado desta expressao: self._selecionar(; esse valor sera usado nas proximas linhas.
            comunidades, "Digite o número da comunidade que deseja acessar: "  # Executa nesta linha da classe GerenciadorComunidades e do metodo entrar a instrucao especifica: comunidades, "Digite o número da comunidade que deseja acessar: "
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        if comunidade is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        self._exibir_detalhes(comunidade)  # Executa nesta linha da classe GerenciadorComunidades e do metodo entrar a instrucao especifica: self._exibir_detalhes(comunidade)
        if not self._usuario_pode_acessar(ratname, comunidade):  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print(  # Exibe na tela a mensagem especifica formada por esta expressao de print.
                "\nEsta comunidade não permite a participação "  # Executa nesta linha da classe GerenciadorComunidades e do metodo entrar a instrucao especifica: "\nEsta comunidade não permite a participação "
                f"da sua conta do tipo {self.estado.tipo_usuario_logado}."  # Executa nesta linha da classe GerenciadorComunidades e do metodo entrar a instrucao especifica: f"da sua conta do tipo {self.estado.tipo_usuario_logado}."
            )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if ratname not in comunidade["membros"]:  # Verifica se o usuario ainda nao esta na colecao de participantes antes de adicionar o nome.
            resposta = input(  # Atribui a resposta a resposta digitada no prompt campo solicitado, removendo espacos externos antes da validacao.
                "\nDeseja fazer parte dessa Comunidade Rat? (s/n): "  # Executa nesta linha da classe GerenciadorComunidades e do metodo entrar a instrucao especifica: "\nDeseja fazer parte dessa Comunidade Rat (s/n): "
            ).strip().lower()  # Remove espacos externos antes da validacao ou armazenamento da entrada.
            if resposta != "s":  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
                print("Você voltou ao menu de comunidades.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
                return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
            comunidade["membros"].append(ratname)  # Insere no fim da colecao o registro ou texto criado nesta etapa.
            self._salvar(comunidades)  # Executa nesta linha da classe GerenciadorComunidades e do metodo entrar a instrucao especifica: self._salvar(comunidades)
            if self.estado.tipo_usuario_logado == self.estado.TIPO_ESTUDANTE:  # Compara o perfil conectado ao perfil autorizado pela condicao desta acao.
                self.ratcoins.registrar_ganho(  # Solicita ao gerenciador o credito desta atividade usando o identificador unico do evento.
                    ratname,  # Executa nesta linha da classe GerenciadorComunidades e do metodo entrar a instrucao especifica: ratname,
                    f"Entrar na comunidade: {comunidade['nome']}",  # Executa nesta linha da classe GerenciadorComunidades e do metodo entrar a instrucao especifica: f"Entrar na comunidade: {comunidade['nome']}",
                    10,  # Executa nesta linha da classe GerenciadorComunidades e do metodo entrar a instrucao especifica: 10,
                    evento_id=f"comunidade-entrar:{comunidade['id']}:{ratname}",  # Atribui a evento_id o resultado desta expressao: f"comunidade-entrar:{comunidade['id']}:{ratname}",; esse valor sera usado nas proximas linhas.
                )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            print("Você agora faz parte dessa Comunidade Rat!")  # Exibe na tela a mensagem especifica formada por esta expressao de print.

        self._menu_publicacoes(comunidade, comunidades)  # Executa nesta linha da classe GerenciadorComunidades e do metodo entrar a instrucao especifica: self._menu_publicacoes(comunidade, comunidades)

    def _menu_publicacoes(self, comunidade: dict, comunidades: list[dict]) -> None:  # Declara o metodo _menu_publicacoes nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        while True:  # Mantem o loop ativo enquanto a condicao desta linha permanece verdadeira, encerrando-o por return ou escolha de saida.
            print(f"\n===== COMUNIDADE: {comunidade['nome']} =====")  # Exibe o cabecalho desta secao da interface: ]} =====.
            print("1. Ver publicações")  # Exibe na tela a opcao numero 1 com o texto e a acao correspondentes estae menu.
            print("2. Criar publicação")  # Exibe na tela a opcao numero 2 com o texto e a acao correspondentes estae menu.
            print("3. Responder publicação")  # Exibe na tela a opcao numero 3 com o texto e a acao correspondentes estae menu.
            print("4. Abrir chat da comunidade")  # Exibe na tela a opcao numero 4 com o texto e a acao correspondentes estae menu.
            print("5. Interagir com uma publicação")  # Exibe na tela a opcao numero 5 com o texto e a acao correspondentes estae menu.
            print("6. Consultar minhas publicações favoritas")  # Exibe na tela a opcao numero 6 com o texto e a acao correspondentes estae menu.
            print("0. Voltar às comunidades")  # Exibe a opcao 0, que encerrestaa tela e volta ao menu anterior.
            opcao = input("Escolha uma opção: ").strip()  # Atribui a opcao a resposta digitada no prompt Escolha uma opção: , removendo espacos externos antes da validacao.
            acoes = {  # Atribui a acoes o resultado desta expressao: {; esse valor sera usado nas proximas linhas.
                "1": lambda: self._ver_publicacoes(comunidade),  # Define a chave "1" destestarutura para representar o valor especifico desta entrada.
                "2": lambda: self._criar_publicacao(comunidade, comunidades),  # Define a chave "2" destestarutura para representar o valor especifico desta entrada.
                "3": lambda: self._responder_publicacao(comunidade, comunidades),  # Define a chave "3" destestarutura para representar o valor especifico desta entrada.
                "4": lambda: self._menu_chat(comunidade, comunidades),  # Define a chave "4" destestarutura para representar o valor especifico desta entrada.
                "5": lambda: self._interagir_publicacao(comunidade, comunidades),  # Define a chave "5" destestarutura para representar o valor especifico desta entrada.
                "6": lambda: self._consultar_favoritos(comunidades),  # Define a chave "6" destestarutura para representar o valor especifico desta entrada.
            }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
            if opcao == "0":  # Executestaa ramificacao somente quando a escolha digitada for exatamente o numero ou texto indicado.
                return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
            acao = acoes.get(opcao)  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
            if acao is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
                print("Opção inválida. Tente novamente.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            else:  # Executa o tratamento do caso restante que nao satisfez as condicoes anteriores desta decisao.
                acao()  # Executa nesta linha da classe GerenciadorComunidades e do metodo _menu_publicacoes a instrucao especifica: acao()

    def _ver_publicacoes(self, comunidade: dict) -> None:  # Declara o metodo _ver_publicacoes nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        print("\n===== PUBLICAÇÕES =====")  # Exibe o cabecalho desta secao da interface: \n===== PUBLICAÇÕES =====.
        publicacoes = comunidade["publicacoes"]  # Atribui a publicacoes o resultado desta expressao: comunidade["publicacoes"]; esse valor sera usado nas proximas linhas.
        if not publicacoes:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Ainda não existem publicações nessa comunidade.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        for indice, publicacao in enumerate(publicacoes, start=1):  # Percorre cada publicacao para exibir conteudo, contar interacoes ou validar respostas.
            print(f"\nPublicação {indice}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            print(f"Autor: {publicacao['autor']}")  # Exibe o autor da publicacao atual nesta linha da interface.
            print(f"Conteúdo: {publicacao['conteudo']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            if publicacao.get("material"):  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
                print(f"Material compartilhado: {publicacao['material']}")  # Exibe o material anexado a publicacao nesta linha da interface.
            print(f"Likes: {len(publicacao['likes'])}")  # Exibe a quantidade atual de curtidas nesta linha da interface.
            print(f"Dislikes: {len(publicacao['dislikes'])}")  # Exibe a quantidade atual de descurtidas nesta linha da interface.
            print("Respostas:")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            if not publicacao["respostas"]:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                print("Ainda não existem respostas.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            for resposta in publicacao["respostas"]:  # Percorre cada publicacao para exibir conteudo, contar interacoes ou validar respostas.
                print(f"- {resposta['autor']}: {resposta['conteudo']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.

    def _interagir_publicacao(  # Declara o metodo _interagir_publicacao nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self,  # Executa nesta linha da classe GerenciadorComunidades e do metodo _interagir_publicacao a instrucao especifica: self,
        comunidade: dict,  # Executa nesta linha da classe GerenciadorComunidades e do metodo _interagir_publicacao a instrucao especifica: comunidade: dict,
        comunidades: list[dict],  # Executa nesta linha da classe GerenciadorComunidades e do metodo _interagir_publicacao a instrucao especifica: comunidades: list[dict],
    ) -> None:  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        ratname = self._usuario_atual()  # Atribui a ratname o resultado desta expressao: self._usuario_atual(); esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if ratname not in comunidade["membros"]:  # Verifica se o usuario ainda nao esta na colecao de participantes antes de adicionar o nome.
            print("Você precisa entrar na comunidade para interagir com publicações.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if not comunidade["publicacoes"]:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Não existem publicações para interagir.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.

        self._ver_publicacoes(comunidade)  # Executa nesta linha da classe GerenciadorComunidades e do metodo _interagir_publicacao a instrucao especifica: self._ver_publicacoes(comunidade)
        publicacao = self._selecionar(  # Atribui a publicacao o resultado desta expressao: self._selecionar(; esse valor sera usado nas proximas linhas.
            comunidade["publicacoes"],  # Executa nesta linha da classe GerenciadorComunidades e do metodo _interagir_publicacao a instrucao especifica: comunidade["publicacoes"],
            "Digite o número da publicação que deseja interagir: ",  # Executa nesta linha da classe GerenciadorComunidades e do metodo _interagir_publicacao a instrucao especifica: "Digite o número da publicação que deseja interagir: ",
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        if publicacao is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print("Não foi possível realizar a interação: publicação não encontrada.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.

        print("\n1. Curtir")  # Exibe na tela a opcao numero 1 com o texto e a acao correspondentes estae menu.
        print("2. Não curtir")  # Exibe na tela a opcao numero 2 com o texto e a acao correspondentes estae menu.
        print("3. Favoritar ou desfavoritar")  # Exibe na tela a opcao numero 3 com o texto e a acao correspondentes estae menu.
        opcao = input("Escolha uma interação: ").strip()  # Atribui a opcao a resposta digitada no prompt Escolha uma interação: , removendo espacos externos antes da validacao.

        if opcao not in ("1", "2", "3"):  # Reconhece a escolha como invalida quando ela nao corresponde a uma alternativa desta tela.
            print("Opção de interação inválida.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.

        if opcao == "1":  # Executestaa ramificacao somente quando a escolha digitada for exatamente o numero ou texto indicado.
            if ratname in publicacao["likes"]:  # Verifica se o usuario jestaa nessa colecao de like, dislike ou favorito da publicacao.
                publicacao["likes"].remove(ratname)  # Remove da colecao o elemento identificado pela acao atual.
                print("Sua curtida foi retirada.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            else:  # Executa o tratamento do caso restante que nao satisfez as condicoes anteriores desta decisao.
                if ratname in publicacao["dislikes"]:  # Verifica se o usuario jestaa nessa colecao de like, dislike ou favorito da publicacao.
                    publicacao["dislikes"].remove(ratname)  # Remove da colecao o elemento identificado pela acao atual.
                publicacao["likes"].append(ratname)  # Insere no fim da colecao o registro ou texto criado nesta etapa.
                print("Publicação curtida!")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
        elif opcao == "2":  # Avaliestaa alternativa apenas depois das condicoes anteriores serem falsas, usando os valores desta ramificacao.
            if ratname in publicacao["dislikes"]:  # Verifica se o usuario jestaa nessa colecao de like, dislike ou favorito da publicacao.
                publicacao["dislikes"].remove(ratname)  # Remove da colecao o elemento identificado pela acao atual.
                print("Seu dislike foi retirado.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            else:  # Executa o tratamento do caso restante que nao satisfez as condicoes anteriores desta decisao.
                if ratname in publicacao["likes"]:  # Verifica se o usuario jestaa nessa colecao de like, dislike ou favorito da publicacao.
                    publicacao["likes"].remove(ratname)  # Remove da colecao o elemento identificado pela acao atual.
                publicacao["dislikes"].append(ratname)  # Insere no fim da colecao o registro ou texto criado nesta etapa.
                print("Publicação marcada como não curtida.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
        else:  # Executa o tratamento do caso restante que nao satisfez as condicoes anteriores desta decisao.
            if ratname in publicacao["favoritos"]:  # Verifica se o usuario jestaa nessa colecao de like, dislike ou favorito da publicacao.
                publicacao["favoritos"].remove(ratname)  # Remove da colecao o elemento identificado pela acao atual.
                print("Publicação removida dos favoritos.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            else:  # Executa o tratamento do caso restante que nao satisfez as condicoes anteriores desta decisao.
                publicacao["favoritos"].append(ratname)  # Insere no fim da colecao o registro ou texto criado nesta etapa.
                print("Publicação adicionada aos favoritos!")  # Exibe na tela a mensagem especifica formada por esta expressao de print.

        self._salvar(comunidades)  # Executa nesta linha da classe GerenciadorComunidades e do metodo _interagir_publicacao a instrucao especifica: self._salvar(comunidades)
        print(  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            f"Likes: {len(publicacao['likes'])} | "  # Conta participantes ou elementos para exibir quantidade ou validar uma posicao.
            f"Dislikes: {len(publicacao['dislikes'])}"  # Conta participantes ou elementos para exibir quantidade ou validar uma posicao.
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.

    def _consultar_favoritos(self, comunidades: list[dict]) -> None:  # Declara o metodo _consultar_favoritos nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self._usuario_atual()  # Atribui a ratname o resultado desta expressao: self._usuario_atual(); esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.

        encontrados = []  # Atribui a encontrados o resultado desta expressao: []; esse valor sera usado nas proximas linhas.
        for comunidade in comunidades:  # Percorre cada comunidade carregada para listar, pesquisar, validar ou reunir favoritos.
            for publicacao in comunidade["publicacoes"]:  # Percorre cada comunidade carregada para listar, pesquisar, validar ou reunir favoritos.
                if ratname in publicacao["favoritos"]:  # Verifica se o usuario jestaa nessa colecao de like, dislike ou favorito da publicacao.
                    encontrados.append((comunidade, publicacao))  # Insere no fim da colecao o registro ou texto criado nesta etapa.

        print("\n===== MINHAS PUBLICAÇÕES FAVORITAS =====")  # Exibe o cabecalho desta secao da interface: \n===== MINHAS PUBLICAÇÕES FAVORITAS =====.
        if not encontrados:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Você ainda não possui publicações favoritas.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        for indice, (comunidade, publicacao) in enumerate(encontrados, start=1):  # Percorre cada comunidade carregada para listar, pesquisar, validar ou reunir favoritos.
            print(f"\n{indice}. Comunidade: {comunidade['nome']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            print(f"Autor: {publicacao['autor']}")  # Exibe o autor da publicacao atual nesta linha da interface.
            print(f"Conteúdo: {publicacao['conteudo']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            if publicacao.get("material"):  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
                print(f"Material compartilhado: {publicacao['material']}")  # Exibe o material anexado a publicacao nesta linha da interface.

    def _criar_publicacao(self, comunidade: dict, comunidades: list[dict]) -> None:  # Declara o metodo _criar_publicacao nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        if self.estado.usuario_logado not in comunidade["membros"]:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Somente participantes podem publicar nesta comunidade.")  # Informa que o perfil, criador ou participante nao satisfaz a exigencia desta acao.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if not self._usuario_pode_acessar(self.estado.usuario_logado, comunidade):  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Sua conta não pode publicar nesta comunidade.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        print("\n===== NOVA PUBLICAÇÃO =====")  # Exibe o cabecalho desta secao da interface: \n===== NOVA PUBLICAÇÃO =====.
        conteudo = input("Escreva sua publicação: ").strip()  # Atribui a conteudo a resposta digitada no prompt Escreva sua publicação: , removendo espacos externos antes da validacao.
        if not conteudo:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("A publicação não pode ficar vazia.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        material = input(  # Atribui a material a resposta digitada no prompt campo solicitado, removendo espacos externos antes da validacao.
            "Deseja compartilhar um link ou material? (Se não, deixe vazio): "  # Executa nesta linha da classe GerenciadorComunidades e do metodo _criar_publicacao a instrucao especifica: "Deseja compartilhar um link ou material (Se não, deixe vazio): "
        ).strip()  # Remove espacos externos antes da validacao ou armazenamento da entrada.
        comunidade["publicacoes"].append(  # Insere no fim da colecao o registro ou texto criado nesta etapa.
            {  # Inicia o objeto desta etapa e define nas linhas seguintes os campos e valores do novo registro.
                "autor": self.estado.usuario_logado,  # Define a chave "autor" destestarutura para representar o ratname do autor.
                "conteudo": conteudo,  # Define a chave "conteudo" destestarutura para representar o texto publicado ou enviado.
                "material": material,  # Define a chave "material" destestarutura para representar o link ou material compartilhado.
                "respostas": [],  # Define a chave "respostas" destestarutura para representar as respostas da publicacao.
                "likes": [],  # Define a chave "likes" destestarutura para representar os ratnames que curtiram.
                "dislikes": [],  # Define a chave "dislikes" destestarutura para representar os ratnames que nao curtiram.
                "favoritos": [],  # Define a chave "favoritos" destestarutura para representar os ratnames que favoritaram.
            }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        self._salvar(comunidades)  # Executa nesta linha da classe GerenciadorComunidades e do metodo _criar_publicacao a instrucao especifica: self._salvar(comunidades)
        print("Publicação criada com sucesso!")  # Informa ao usuario o resultado concluido ou cancelado desta operacao.

    def _responder_publicacao(  # Declara o metodo _responder_publicacao nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self,  # Executa nesta linha da classe GerenciadorComunidades e do metodo _responder_publicacao a instrucao especifica: self,
        comunidade: dict,  # Executa nesta linha da classe GerenciadorComunidades e do metodo _responder_publicacao a instrucao especifica: comunidade: dict,
        comunidades: list[dict],  # Executa nesta linha da classe GerenciadorComunidades e do metodo _responder_publicacao a instrucao especifica: comunidades: list[dict],
    ) -> None:  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        if self.estado.usuario_logado not in comunidade["membros"]:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Somente participantes podem responder nesta comunidade.")  # Informa que o perfil, criador ou participante nao satisfaz a exigencia desta acao.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if not self._usuario_pode_acessar(self.estado.usuario_logado, comunidade):  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Sua conta não pode responder nesta comunidade.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        publicacoes = comunidade["publicacoes"]  # Atribui a publicacoes o resultado desta expressao: comunidade["publicacoes"]; esse valor sera usado nas proximas linhas.
        if not publicacoes:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Não existem publicações para responder.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        self._ver_publicacoes(comunidade)  # Executa nesta linha da classe GerenciadorComunidades e do metodo _responder_publicacao a instrucao especifica: self._ver_publicacoes(comunidade)
        publicacao = self._selecionar(  # Atribui a publicacao o resultado desta expressao: self._selecionar(; esse valor sera usado nas proximas linhas.
            publicacoes, "Digite o número da publicação que deseja responder: "  # Executa nesta linha da classe GerenciadorComunidades e do metodo _responder_publicacao a instrucao especifica: publicacoes, "Digite o número da publicação que deseja responder: "
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        if publicacao is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        resposta = input("Digite sua resposta: ").strip()  # Atribui a resposta a resposta digitada no prompt Digite sua resposta: , removendo espacos externos antes da validacao.
        if not resposta:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("A resposta não pode ficar vazia.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        publicacao["respostas"].append(  # Insere no fim da colecao o registro ou texto criado nesta etapa.
            {"autor": self.estado.usuario_logado, "conteudo": resposta}  # Inicia o objeto desta etapa e define nas linhas seguintes os campos e valores do novo registro.
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        self._salvar(comunidades)  # Executa nesta linha da classe GerenciadorComunidades e do metodo _responder_publicacao a instrucao especifica: self._salvar(comunidades)
        print("Resposta publicada com sucesso!")  # Informa ao usuario o resultado concluido ou cancelado desta operacao.

    def _menu_chat(self, comunidade: dict, comunidades: list[dict]) -> None:  # Declara o metodo _menu_chat nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self._usuario_atual()  # Atribui a ratname o resultado desta expressao: self._usuario_atual(); esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if ratname not in comunidade["membros"]:  # Verifica se o usuario ainda nao esta na colecao de participantes antes de adicionar o nome.
            print("Somente participantes podem acessar o chat desta comunidade.")  # Informa que o perfil, criador ou participante nao satisfaz a exigencia desta acao.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if not self._usuario_pode_acessar(ratname, comunidade):  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Sua conta não pode participar do chat desta comunidade.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.

        while True:  # Mantem o loop ativo enquanto a condicao desta linha permanece verdadeira, encerrando-o por return ou escolha de saida.
            print(f"\n===== CHAT: {comunidade['nome']} =====")  # Exibe o cabecalho desta secao da interface: ]} =====.
            mensagens = comunidade["mensagens"]  # Atribui a mensagens o resultado desta expressao: comunidade["mensagens"]; esse valor sera usado nas proximas linhas.
            if not mensagens:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                print("Ainda não existem mensagens neste chat.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            else:  # Executa o tratamento do caso restante que nao satisfez as condicoes anteriores desta decisao.
                for mensagem in mensagens:  # Percorre cada mensagem do chat para apresentar autor e texto.
                    print(f"- {mensagem['autor']}: {mensagem['conteudo']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            print("\n1. Enviar mensagem")  # Exibe na tela a opcao numero 1 com o texto e a acao correspondentes estae menu.
            print("0. Voltar à comunidade")  # Exibe a opcao 0, que encerrestaa tela e volta ao menu anterior.
            opcao = input("Escolha uma opção: ").strip()  # Atribui a opcao a resposta digitada no prompt Escolha uma opção: , removendo espacos externos antes da validacao.
            if opcao == "0":  # Executestaa ramificacao somente quando a escolha digitada for exatamente o numero ou texto indicado.
                return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
            if opcao != "1":  # Reconhece a escolha como invalida quando ela nao corresponde a uma alternativa desta tela.
                print("Opção inválida.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
                continue  # Encerra apenas a iteracao atual do loop e passa diretamente para o proximo elemento ou opcao.

            conteudo = input("Digite sua mensagem: ").strip()  # Atribui a conteudo a resposta digitada no prompt Digite sua mensagem: , removendo espacos externos antes da validacao.
            if not conteudo:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                print("A mensagem não pode ficar vazia.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
                continue  # Encerra apenas a iteracao atual do loop e passa diretamente para o proximo elemento ou opcao.
            mensagens.append({"autor": ratname, "conteudo": conteudo})  # Insere no fim da colecao o registro ou texto criado nesta etapa.
            self._salvar(comunidades)  # Executa nesta linha da classe GerenciadorComunidades e do metodo _menu_chat a instrucao especifica: self._salvar(comunidades)
            print("Mensagem enviada.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.

    def _usuario_atual(self) -> str | None:  # Declara o metodo _usuario_atual nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self.estado.usuario_logado  # Atribui a ratname o resultado desta expressao: self.estado.usuario_logado; esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print("Você precisa fazer login para acessar as Comunidades Rat.")  # Informa que o usuario precisestaar autenticado antes desta operacao.
        return ratname  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

    def _tipo_usuario(self, ratname: str | None) -> str | None:  # Declara o metodo _tipo_usuario nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        if not isinstance(ratname, str):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            return None  # Encerra sem resultado porque login, perfil ou validacao bloqueou a operacao atual.
        usuario = next(  # Atribui a usuario o resultado desta expressao: next(; esse valor sera usado nas proximas linhas.
            (  # Executa nesta linha da classe GerenciadorComunidades e do metodo _tipo_usuario a instrucao especifica: (
                item  # Executa nesta linha da classe GerenciadorComunidades e do metodo _tipo_usuario a instrucao especifica: item
                for item in self.estado.usuarios  # Percorre a colecao especificada nesta linha e repete a instrucao do bloco para cada elemento.
                if item.get("ratname") == ratname  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            ),  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            None,  # Executa nesta linha da classe GerenciadorComunidades e do metodo _tipo_usuario a instrucao especifica: None,
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        if usuario is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return None  # Encerra sem resultado porque login, perfil ou validacao bloqueou a operacao atual.
        return usuario.get("tipo_usuario", self.estado.TIPO_ESTUDANTE)  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

    def _usuario_pode_acessar(self, ratname: str, comunidade: dict) -> bool:  # Declara o metodo _usuario_pode_acessar nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        tipo_usuario = self._tipo_usuario(ratname)  # Atribui a tipo_usuario o resultado desta expressao: self._tipo_usuario(ratname); esse valor sera usado nas proximas linhas.
        tipo_acesso = comunidade["tipo_acesso"]  # Atribui a tipo_acesso o resultado desta expressao: comunidade["tipo_acesso"]; esse valor sera usado nas proximas linhas.
        if tipo_acesso == self.TIPO_ESTUDANTES:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return tipo_usuario == self.estado.TIPO_ESTUDANTE  # Devolve para a chamada anterior o valor definido nesta linha de retorno.
        if tipo_acesso == self.TIPO_MONITORES:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return tipo_usuario == self.estado.TIPO_MONITOR  # Devolve para a chamada anterior o valor definido nesta linha de retorno.
        if tipo_acesso == self.TIPO_ESTUDANTES_MONITORES:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return tipo_usuario in (  # Devolve para a chamada anterior o valor definido nesta linha de retorno.
                self.estado.TIPO_ESTUDANTE,  # Executa nesta linha da classe GerenciadorComunidades e do metodo _usuario_pode_acessar a instrucao especifica: self.estado.TIPO_ESTUDANTE,
                self.estado.TIPO_MONITOR,  # Executa nesta linha da classe GerenciadorComunidades e do metodo _usuario_pode_acessar a instrucao especifica: self.estado.TIPO_MONITOR,
            )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        return False  # Retorna falso porque o ganho, ajuste ou alteracao nao sera aplicado nesta condicao.

    def _nome_tipo_acesso(self, tipo_acesso: str) -> str:  # Declara o metodo _nome_tipo_acesso nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        nomes = {  # Atribui a nomes o resultado desta expressao: {; esse valor sera usado nas proximas linhas.
            self.TIPO_ESTUDANTES: "Apenas estudantes",  # Executa nesta linha da classe GerenciadorComunidades e do metodo _nome_tipo_acesso a instrucao especifica: self.TIPO_ESTUDANTES: "Apenas estudantes",
            self.TIPO_ESTUDANTES_MONITORES: "Estudantes e monitores",  # Executa nesta linha da classe GerenciadorComunidades e do metodo _nome_tipo_acesso a instrucao especifica: self.TIPO_ESTUDANTES_MONITORES: "Estudantes e monitores",
            self.TIPO_MONITORES: "Apenas monitores",  # Executa nesta linha da classe GerenciadorComunidades e do metodo _nome_tipo_acesso a instrucao especifica: self.TIPO_MONITORES: "Apenas monitores",
        }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
        return nomes[tipo_acesso]  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

    @staticmethod  # Aplica ao metodo seguinte o modificador @staticmethod para definir como ele sera chamado pela classe ou instancia.
    def _selecionar(itens: list[dict], pergunta: str) -> dict | None:  # Declara o metodo _selecionar nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        if not itens:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            return None  # Encerra sem resultado porque login, perfil ou validacao bloqueou a operacao atual.
        try:  # Inicia a operacao protegida; conversao ou acesso invalido sera tratado pelo bloco except seguinte.
            numero = int(input(pergunta).strip())  # Remove espacos externos antes da validacao ou armazenamento da entrada.
        except ValueError:  # Captura o erro especificado nesta linha e informa ou cancela a operacao sem processar dados invalidos.
            print("Digite um número válido.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return None  # Encerra sem resultado porque login, perfil ou validacao bloqueou a operacao atual.
        if numero < 1 or numero > len(itens):  # Rejeita o numero fora das posicoes existentes na lista numerada exibida.
            print("Item não encontrado.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return None  # Encerra sem resultado porque login, perfil ou validacao bloqueou a operacao atual.
        return itens[numero - 1]  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

    @staticmethod  # Aplica ao metodo seguinte o modificador @staticmethod para definir como ele sera chamado pela classe ou instancia.
    def _exibir_detalhes(comunidade: dict) -> None:  # Declara o metodo _exibir_detalhes nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        print("\n===== INFORMAÇÕES DA COMUNIDADE =====")  # Exibe o cabecalho desta secao da interface: \n===== INFORMAÇÕES DA COMUNIDADE =====.
        print(f"Nome: {comunidade['nome']}")  # Exibe o nome da comunidade atual nesta linha da interface.
        print(f"Disciplina: {comunidade['disciplina']}")  # Exibe a disciplina da comunidade atual nesta linha da interface.
        print(f"Assunto: {comunidade['assunto']}")  # Exibe o assunto da comunidade atual nesta linha da interface.
        print(f"Descrição: {comunidade['descricao']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
        print(f"Criador: {comunidade['criador']}")  # Exibe o ratname criador da comunidade nesta linha da interface.
        nomes = {  # Atribui a nomes o resultado desta expressao: {; esse valor sera usado nas proximas linhas.
            GerenciadorComunidades.TIPO_ESTUDANTES: "Apenas estudantes",  # Executa nesta linha da classe GerenciadorComunidades e do metodo _exibir_detalhes a instrucao especifica: GerenciadorComunidades.TIPO_ESTUDANTES: "Apenas estudantes",
            GerenciadorComunidades.TIPO_ESTUDANTES_MONITORES: "Estudantes e monitores",  # Executa nesta linha da classe GerenciadorComunidades e do metodo _exibir_detalhes a instrucao especifica: GerenciadorComunidades.TIPO_ESTUDANTES_MONITORES: "Estudantes e monitores",
            GerenciadorComunidades.TIPO_MONITORES: "Apenas monitores",  # Executa nesta linha da classe GerenciadorComunidades e do metodo _exibir_detalhes a instrucao especifica: GerenciadorComunidades.TIPO_MONITORES: "Apenas monitores",
        }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
        print(f"Público: {nomes[comunidade['tipo_acesso']]}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
        print(f"Participantes: {len(comunidade['membros'])}")  # Exibe a quantidade atual de participantes nesta linha da interface.
