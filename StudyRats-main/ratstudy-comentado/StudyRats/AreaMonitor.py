import lista  # Importa o modulo lista para compartilhar o estado global de login, perfil e usuarios desta aplicacao.
from Dados import persistencia  # Importa o gerenciador persistencia para ler e salvar os arquivos JSON desta funcionalidade.
from SalaEstudo import GerenciadorSalas  # Importa o tipo GerenciadorSalas usado pela area do monitor para receber o gerenciador de salas.


class AreaMonitor:  # Define a classe AreaMonitor, responsavel por a area do monitor e suas notas privadas.
    ARQUIVO = "blocos_notas.json"  # Define o arquivo JSON blocos_notas.json como destino e origem da persistencia desta funcionalidade.

    def __init__(self, salas: GerenciadorSalas) -> None:  # Declara o metodo __init__ nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self.estado = lista.estado  # Atribui ao objeto o estado global que informa usuario conectado, tipo de conta e usuarios cadastrados.
        self.persistencia = persistencia  # Atribui ao objeto o gerenciador central usado para carregar e salvar os dados JSON.
        self.salas = salas  # Atribui ao objeto o gerenciador recebido para listar e consultar as salas de estudo.

    def menu(self) -> None:  # Declara o metodo menu nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        if self.estado.usuario_logado is None:  # Bloqueia o acesso porque nenhuma contestaa conectada ao estado da aplicacao.
            print("Você precisa fazer login para acessar a área do monitor.")  # Informa que o usuario precisestaar autenticado antes desta operacao.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if self.estado.tipo_usuario_logado != self.estado.TIPO_MONITOR:  # Compara o perfil conectado ao perfil autorizado pela condicao desta acao.
            print("Esta área está disponível somente para contas de monitor.")  # Informa que o perfil, criador ou participante nao satisfaz a exigencia desta acao.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        while True:  # Mantem o loop ativo enquanto a condicao desta linha permanece verdadeira, encerrando-o por return ou escolha de saida.
            print("\n========== ÁREA DO MONITOR ==========")  # Exibe o cabecalho desta secao da interface: \n========== ÁREA DO MONITOR ==========.
            print("1. Visualizar salas de estudo")  # Exibe na tela a opcao numero 1 com o texto e a acao correspondentes estae menu.
            print("2. Criar notas")  # Exibe na tela a opcao numero 2 com o texto e a acao correspondentes estae menu.
            print("3. Ver minhas notas")  # Exibe na tela a opcao numero 3 com o texto e a acao correspondentes estae menu.
            print("4. Excluir notas")  # Exibe na tela a opcao numero 4 com o texto e a acao correspondentes estae menu.
            print("0. Voltar ao menu principal")  # Exibe a opcao 0, que encerrestaa tela e volta ao menu anterior.
            opcao = input("Escolha uma opção: ").strip()  # Atribui a opcao a resposta digitada no prompt Escolha uma opção: , removendo espacos externos antes da validacao.
            acoes = {  # Atribui a acoes o resultado desta expressao: {; esse valor sera usado nas proximas linhas.
                "1": self.salas.listar_salas,  # Define a chave "1" destestarutura para representar o valor especifico desta entrada.
                "2": self.criar_bloco,  # Define a chave "2" destestarutura para representar o valor especifico desta entrada.
                "3": self.listar_blocos,  # Define a chave "3" destestarutura para representar o valor especifico desta entrada.
                "4": self.excluir_bloco,  # Define a chave "4" destestarutura para representar o valor especifico desta entrada.
            }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
            if opcao == "0":  # Executestaa ramificacao somente quando a escolha digitada for exatamente o numero ou texto indicado.
                return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
            acao = acoes.get(opcao)  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
            if acao is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
                print("Opção inválida. Tente novamente.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            else:  # Executa o tratamento do caso restante que nao satisfez as condicoes anteriores desta decisao.
                acao()  # Executa nesta linha da classe AreaMonitor e do metodo menu a instrucao especifica: acao()

    def _carregar(self) -> dict:  # Declara o metodo _carregar nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        blocos = self.persistencia.carregar(self.ARQUIVO, {})  # Le os dados persistidos ou aplica o valor padrao definido nesta chamada.
        if not isinstance(blocos, dict):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError("O arquivo blocos_notas.json deve conter um objeto JSON.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        return blocos  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

    def criar_bloco(self) -> None:  # Declara o metodo criar_bloco nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self._monitor_logado()  # Atribui a ratname o resultado desta expressao: self._monitor_logado(); esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        todos_blocos = self._carregar()  # Atribui a todos_blocos o resultado desta expressao: self._carregar(); esse valor sera usado nas proximas linhas.
        print("\n===== CRIAR NOTAS =====")  # Exibe o cabecalho desta secao da interface: \n===== CRIAR NOTAS =====.
        materia = input("Matéria das notas: ").strip()  # Atribui a materia a resposta digitada no prompt Matéria das notas: , removendo espacos externos antes da validacao.
        duvida = input("Dúvida/Tema: ").strip()  # Atribui a duvida a resposta digitada no prompt Dúvida/Tema: , removendo espacos externos antes da validacao.
        anotacoes = input("Descrição: ").strip()  # Atribui a anotacoes a resposta digitada no prompt Descrição: , removendo espacos externos antes da validacao.
        materiais = input("Material complementar a ser usado: ").strip()  # Atribui a materiais a resposta digitada no prompt Material complementar a ser usado: , removendo espacos externos antes da validacao.
        if not materia:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("A matéria não pode ficar vazia.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        blocos_usuario = todos_blocos.setdefault(ratname, [])  # Recupera a colecao da chave ou cria uma lista vazia antes de inserir o novo dado.
        if not isinstance(blocos_usuario, list):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError(f"Os blocos de notas de '{ratname}' estão inválidos.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        blocos_usuario.append(  # Insere no fim da colecao o registro ou texto criado nesta etapa.
            {  # Inicia o objeto desta etapa e define nas linhas seguintes os campos e valores do novo registro.
                "materia": materia,  # Define a chave "materia" destestarutura para representar a materia do compromisso ou nota.
                "duvida": duvida,  # Define a chave "duvida" destestarutura para representar a duvida ou tema da nota.
                "materiais_complementares": materiais,  # Define a chave "materiais_complementares" destestarutura para representar os materiais indicados pelo monitor.
                "anotacoes_gerais": anotacoes,  # Define a chave "anotacoes_gerais" destestarutura para representar a descricao geral da nota.
            }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        self.persistencia.salvar(self.ARQUIVO, todos_blocos)  # Persiste no arquivo JSON estarutura atualizada desta operacao.
        print("Nota criada com sucesso!")  # Informa ao usuario o resultado concluido ou cancelado desta operacao.

    def listar_blocos(self) -> None:  # Declara o metodo listar_blocos nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self._monitor_logado()  # Atribui a ratname o resultado desta expressao: self._monitor_logado(); esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        blocos = self._carregar().get(ratname, [])  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
        if not isinstance(blocos, list):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError(f"As notas de '{ratname}' estão inválidas.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        print("\n===== MINHAS NOTAS =====")  # Exibe o cabecalho desta secao da interface: \n===== MINHAS NOTAS =====.
        if not blocos:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Você ainda não criou notas.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        for indice, bloco in enumerate(blocos, start=1):  # Percorre a colecao atribuindo a cada elemento uma posicao sequencial para exibicao ou selecao.
            if not isinstance(bloco, dict):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                raise ValueError(f"A nota {indice} de '{ratname}' está inválida.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
            print(f"\n{indice}. {bloco.get('materia', 'Sem matéria')}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            print(f"Dúvida/Tema: {bloco.get('duvida', '')}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            print(f"Materiais complementares: {bloco.get('materiais_complementares', '')}")  # Exibe os materiais indicados na nota atual nesta linha da interface.
            print(f"Descrição: {bloco.get('anotacoes_gerais', '')}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.

    def excluir_bloco(self) -> None:  # Declara o metodo excluir_bloco nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self._monitor_logado()  # Atribui a ratname o resultado desta expressao: self._monitor_logado(); esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        todos_blocos = self._carregar()  # Atribui a todos_blocos o resultado desta expressao: self._carregar(); esse valor sera usado nas proximas linhas.
        blocos = todos_blocos.get(ratname, [])  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
        if not isinstance(blocos, list):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError(f"Os blocos de notas de '{ratname}' estão inválidos.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        if not blocos:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Você não possui blocos de notas para excluir.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        self.listar_blocos()  # Executa nesta linha da classe AreaMonitor e do metodo excluir_bloco a instrucao especifica: self.listar_blocos()
        try:  # Inicia a operacao protegida; conversao ou acesso invalido sera tratado pelo bloco except seguinte.
            numero = int(input("Digite o número da nota que deseja excluir: ").strip())  # Remove espacos externos antes da validacao ou armazenamento da entrada.
        except ValueError:  # Captura o erro especificado nesta linha e informa ou cancela a operacao sem processar dados invalidos.
            print("Digite um número válido.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if numero < 1 or numero > len(blocos):  # Rejeita o numero fora das posicoes existentes na lista numerada exibida.
            print("Nota não encontrada.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if input("Confirma a exclusão? (s/n): ").strip().lower() != "s":  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print("Exclusão cancelada.")  # Informa ao usuario o resultado concluido ou cancelado desta operacao.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        blocos.pop(numero - 1)  # Remove destarutura a entrada escolhida pela posicao ou chave desta linha.
        self.persistencia.salvar(self.ARQUIVO, todos_blocos)  # Persiste no arquivo JSON estarutura atualizada desta operacao.
        print("Nota excluída com sucesso!")  # Informa ao usuario o resultado concluido ou cancelado desta operacao.

    def _monitor_logado(self) -> str | None:  # Declara o metodo _monitor_logado nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self.estado.usuario_logado  # Atribui a ratname o resultado desta expressao: self.estado.usuario_logado; esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print("Você precisa fazer login para acessar a área do monitor.")  # Informa que o usuario precisestaar autenticado antes desta operacao.
            return None  # Encerra sem resultado porque login, perfil ou validacao bloqueou a operacao atual.
        if self.estado.tipo_usuario_logado != self.estado.TIPO_MONITOR:  # Compara o perfil conectado ao perfil autorizado pela condicao desta acao.
            print("Esta área está disponível somente para contas de monitor.")  # Informa que o perfil, criador ou participante nao satisfaz a exigencia desta acao.
            return None  # Encerra sem resultado porque login, perfil ou validacao bloqueou a operacao atual.
        return ratname  # Devolve para a chamada anterior o valor definido nesta linha de retorno.
