import calendar  # Importa a biblioteca calendar para montar a grade mensal do calendario por semanas e dias.
from datetime import datetime  # Importa datetime para converter, comparar e formatar as datas e horas dos compromissos.

import lista  # Importa o modulo lista para compartilhar o estado global de login, perfil e usuarios desta aplicacao.
from Dados import persistencia  # Importa o gerenciador persistencia para ler e salvar os arquivos JSON desta funcionalidade.
from Horario import GerenciadorHorario  # Importa GerenciadorHorario para obter a data e o horario atual usados pela funcionalidade.


class GerenciadorCalendario:  # Define a classe GerenciadorCalendario, responsavel por os compromissos, o calendario mensal e os lembretes.
    ARQUIVO = "calendario.json"  # Define o arquivo JSON calendario.json como destino e origem da persistencia desta funcionalidade.
    MESES = (  # Define a sequencia dos nomes dos meses usada para identificar e exibir o mes atual.
        "janeiro",  # Executa nesta linha da classe GerenciadorCalendario e do metodo nivel do modulo a instrucao especifica: "janeiro",
        "fevereiro",  # Executa nesta linha da classe GerenciadorCalendario e do metodo nivel do modulo a instrucao especifica: "fevereiro",
        "março",  # Executa nesta linha da classe GerenciadorCalendario e do metodo nivel do modulo a instrucao especifica: "março",
        "abril",  # Executa nesta linha da classe GerenciadorCalendario e do metodo nivel do modulo a instrucao especifica: "abril",
        "maio",  # Executa nesta linha da classe GerenciadorCalendario e do metodo nivel do modulo a instrucao especifica: "maio",
        "junho",  # Executa nesta linha da classe GerenciadorCalendario e do metodo nivel do modulo a instrucao especifica: "junho",
        "julho",  # Executa nesta linha da classe GerenciadorCalendario e do metodo nivel do modulo a instrucao especifica: "julho",
        "agosto",  # Executa nesta linha da classe GerenciadorCalendario e do metodo nivel do modulo a instrucao especifica: "agosto",
        "setembro",  # Executa nesta linha da classe GerenciadorCalendario e do metodo nivel do modulo a instrucao especifica: "setembro",
        "outubro",  # Executa nesta linha da classe GerenciadorCalendario e do metodo nivel do modulo a instrucao especifica: "outubro",
        "novembro",  # Executa nesta linha da classe GerenciadorCalendario e do metodo nivel do modulo a instrucao especifica: "novembro",
        "dezembro",  # Executa nesta linha da classe GerenciadorCalendario e do metodo nivel do modulo a instrucao especifica: "dezembro",
    )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.

    def __init__(self, horario: GerenciadorHorario | None = None) -> None:  # Declara o metodo __init__ nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self.estado = lista.estado  # Atribui ao objeto o estado global que informa usuario conectado, tipo de conta e usuarios cadastrados.
        self.persistencia = persistencia  # Atribui ao objeto o gerenciador central usado para carregar e salvar os dados JSON.
        self.horario = horario or GerenciadorHorario()  # Atribui ao objeto o gerenciador fornecido ou o gerenciador padrao usado para datas e lembretes.

    def menu(self) -> None:  # Declara o metodo menu nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        if self._usuario_atual() is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        while True:  # Mantem o loop ativo enquanto a condicao desta linha permanece verdadeira, encerrando-o por return ou escolha de saida.
            self.verificar_lembretes()  # Executa nesta linha da classe GerenciadorCalendario e do metodo menu a instrucao especifica: self.verificar_lembretes()
            print("\n========== CALENDÁRIO ==========")  # Exibe o cabecalho desta secao da interface: \n========== CALENDÁRIO ==========.
            print(f"1. Visualizar calendário desse mês ({self.MESES[self.horario.obter_horario_atual().month - 1]})")  # Exibe na tela a opcao numero 1 com o texto e a acao correspondentes estae menu.
            print("2. Ver meus compromissos")  # Exibe na tela a opcao numero 2 com o texto e a acao correspondentes estae menu.
            print("3. Adicionar compromisso")  # Exibe na tela a opcao numero 3 com o texto e a acao correspondentes estae menu.
            print("4. Editar compromisso")  # Exibe na tela a opcao numero 4 com o texto e a acao correspondentes estae menu.
            print("5. Excluir compromisso")  # Exibe na tela a opcao numero 5 com o texto e a acao correspondentes estae menu.
            print("0. Voltar ao menu principal")  # Exibe a opcao 0, que encerrestaa tela e volta ao menu anterior.
            opcao = input("Escolha uma opção: ").strip()  # Atribui a opcao a resposta digitada no prompt Escolha uma opção: , removendo espacos externos antes da validacao.
            acoes = {  # Atribui a acoes o resultado desta expressao: {; esse valor sera usado nas proximas linhas.
                "1": self.visualizar_calendario,  # Define a chave "1" destestarutura para representar o valor especifico desta entrada.
                "2": self.listar_compromissos,  # Define a chave "2" destestarutura para representar o valor especifico desta entrada.
                "3": self.adicionar_compromisso,  # Define a chave "3" destestarutura para representar o valor especifico desta entrada.
                "4": self.editar_compromisso,  # Define a chave "4" destestarutura para representar o valor especifico desta entrada.
                "5": self.excluir_compromisso,  # Define a chave "5" destestarutura para representar o valor especifico desta entrada.
            }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
            if opcao == "0":  # Executestaa ramificacao somente quando a escolha digitada for exatamente o numero ou texto indicado.
                return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
            acao = acoes.get(opcao)  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
            if acao is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
                print("Opção inválida. Tente novamente.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            else:  # Executa o tratamento do caso restante que nao satisfez as condicoes anteriores desta decisao.
                acao()  # Executa nesta linha da classe GerenciadorCalendario e do metodo menu a instrucao especifica: acao()

    def _carregar(self) -> dict:  # Declara o metodo _carregar nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        calendario = self.persistencia.carregar(self.ARQUIVO, {})  # Le os dados persistidos ou aplica o valor padrao definido nesta chamada.
        if not isinstance(calendario, dict):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError("O arquivo calendario.json deve conter um objeto JSON.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        return calendario  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

    def _compromissos_usuario(self, calendario: dict) -> list[dict]:  # Declara o metodo _compromissos_usuario nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self._usuario_atual()  # Atribui a ratname o resultado desta expressao: self._usuario_atual(); esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return []  # Devolve para a chamada anterior o valor definido nesta linha de retorno.
        compromissos = calendario.setdefault(ratname, [])  # Recupera a colecao da chave ou cria uma lista vazia antes de inserir o novo dado.
        if not isinstance(compromissos, list) or not all(  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            isinstance(item, dict) for item in compromissos  # Confere o tipo do dado antes de trata-lo como lista, objeto ou texto.
        ):  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            raise ValueError(f"Os compromissos de '{ratname}' estão inválidos.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        for compromisso in compromissos:  # Percorre cada compromisso da conta atual para validar, exibir ou processar lembrete.
            for campo in ("materia", "descricao", "data", "hora"):  # Percorre cada campo obrigatorio e valida seu tipo ou existencia no registro.
                if not isinstance(compromisso.get(campo), str):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                    raise ValueError(f"Um compromisso de '{ratname}' está inválido.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
            self._data_hora(compromisso)  # Executa nesta linha da classe GerenciadorCalendario e do metodo _compromissos_usuario a instrucao especifica: self._data_hora(compromisso)
        return compromissos  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

    def listar_compromissos(self) -> None:  # Declara o metodo listar_compromissos nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        calendario = self._carregar()  # Atribui a calendario o resultado desta expressao: self._carregar(); esse valor sera usado nas proximas linhas.
        compromissos = self._compromissos_usuario(calendario)  # Atribui a compromissos o resultado desta expressao: self._compromissos_usuario(calendario); esse valor sera usado nas proximas linhas.
        ordenados = sorted(compromissos, key=self._data_hora)  # Ordena os registros pela chave declarada nesta chamada.
        print("\n===== MEUS COMPROMISSOS =====")  # Exibe o cabecalho desta secao da interface: \n===== MEUS COMPROMISSOS =====.
        if not ordenados:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Você ainda não possui compromissos cadastrados.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        for indice, compromisso in enumerate(ordenados, start=1):  # Percorre cada compromisso da conta atual para validar, exibir ou processar lembrete.
            print(f"\n{indice}. {compromisso['materia']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            print(f"Descrição: {compromisso['descricao']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            print(f"Data: {compromisso['data']}")  # Exibe a data armazenada no formato DD/MM/AAAA nesta linha da interface.
            print(f"Horário: {compromisso['hora']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.

    def adicionar_compromisso(self) -> None:  # Declara o metodo adicionar_compromisso nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        calendario = self._carregar()  # Atribui a calendario o resultado desta expressao: self._carregar(); esse valor sera usado nas proximas linhas.
        compromissos = self._compromissos_usuario(calendario)  # Atribui a compromissos o resultado desta expressao: self._compromissos_usuario(calendario); esse valor sera usado nas proximas linhas.
        print("\n===== ADICIONAR ESTUDO AO CALENDÁRIO =====")  # Exibe o cabecalho desta secao da interface: \n===== ADICIONAR ESTUDO AO CALENDÁRIO =====.
        materia = input("Qual matéria você vai estudar? ").strip()  # Atribui a materia a resposta digitada no prompt Qual matéria você vai estudar , removendo espacos externos antes da validacao.
        descricao = input("Descrição do estudo: ").strip()  # Atribui a descricao a resposta digitada no prompt Descrição do estudo: , removendo espacos externos antes da validacao.
        data = input("Data (DD/MM/AAAA): ").strip()  # Atribui a data a resposta digitada no prompt Data (DD/MM/AAAA): , removendo espacos externos antes da validacao.
        hora = input("Horário (HH:MM): ").strip()  # Atribui a hora a resposta digitada no prompt Horário (HH:MM): , removendo espacos externos antes da validacao.
        if not materia or not descricao:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Preencha a matéria e a descrição.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        try:  # Inicia a operacao protegida; conversao ou acesso invalido sera tratado pelo bloco except seguinte.
            data_hora = self._interpretar_data_hora(data, hora)  # Atribui a data_hora o resultado desta expressao: self._interpretar_data_hora(data, hora); esse valor sera usado nas proximas linhas.
        except ValueError:  # Captura o erro especificado nesta linha e informa ou cancela a operacao sem processar dados invalidos.
            print("Data ou horário inválido. Use DD/MM/AAAA e HH:MM.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if data_hora < self.horario.obter_horario_atual():  # Rejeita o compromisso cujo instante ocorre antes do horario atual do gerenciador.
            print("Não é possível cadastrar um estudo em uma data passada.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        compromissos.append(  # Insere no fim da colecao o registro ou texto criado nesta etapa.
            {  # Inicia o objeto desta etapa e define nas linhas seguintes os campos e valores do novo registro.
                "materia": materia,  # Define a chave "materia" destestarutura para representar a materia do compromisso ou nota.
                "descricao": descricao,  # Define a chave "descricao" destestarutura para representar a descricao do estudo ou comunidade.
                "data": data_hora.strftime("%d/%m/%Y"),  # Define a chave "data" destestarutura para representar a data no formato DD/MM/AAAA.
                "hora": data_hora.strftime("%H:%M"),  # Define a chave "hora" destestarutura para representar o horario no formato HH:MM.
                "lembrete_exibido": False,  # Define a chave "lembrete_exibido" destestarutura para representar se o lembrete desse compromisso ja foi exibido.
            }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        self.persistencia.salvar(self.ARQUIVO, calendario)  # Persiste no arquivo JSON estarutura atualizada desta operacao.
        print("\nCompromisso adicionado ao calendário com sucesso!")  # Informa ao usuario o resultado concluido ou cancelado desta operacao.

    def visualizar_calendario(self) -> None:  # Declara o metodo visualizar_calendario nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        compromissos = self._compromissos_usuario(self._carregar())  # Atribui a compromissos o resultado desta expressao: self._compromissos_usuario(self._carregar()); esse valor sera usado nas proximas linhas.
        agora = self.horario.obter_horario_atual()  # Atribui a agora o resultado desta expressao: self.horario.obter_horario_atual(); esse valor sera usado nas proximas linhas.
        print("\n========== MEU CALENDÁRIO RAT ==========")  # Exibe o cabecalho desta secao da interface: \n========== MEU CALENDÁRIO RAT ==========.
        print(f"{self.MESES[agora.month - 1].capitalize()} de {agora.year}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
        print("SEG  TER  QUA  QUI  SEX  SAB  DOM")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
        dias_com_compromisso = {  # Atribui a dias_com_compromisso o resultado desta expressao: {; esse valor sera usado nas proximas linhas.
            self._data_hora(compromisso).day  # Executa nesta linha da classe GerenciadorCalendario e do metodo visualizar_calendario a instrucao especifica: self._data_hora(compromisso).day
            for compromisso in compromissos  # Percorre cada compromisso da conta atual para validar, exibir ou processar lembrete.
            if self._data_hora(compromisso).month == agora.month  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            and self._data_hora(compromisso).year == agora.year  # Executa nesta linha da classe GerenciadorCalendario e do metodo visualizar_calendario a instrucao especifica: and self._data_hora(compromisso).year == agora.year
        }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
        for semana in calendar.monthcalendar(agora.year, agora.month):  # Percorre a colecao especificada nesta linha e repete a instrucao do bloco para cada elemento.
            print(  # Exibe na tela a mensagem especifica formada por esta expressao de print.
                "".join(  # Executa nesta linha da classe GerenciadorCalendario e do metodo visualizar_calendario a instrucao especifica: "".join(
                    "     " if dia == 0 else f"{dia:02d}{'*' if dia in dias_com_compromisso else ' '}  "  # Executa nesta linha da classe GerenciadorCalendario e do metodo visualizar_calendario a instrucao especifica: "     " if dia == 0 else f"{dia:02d}{'*' if dia in dias_com_compromisso else ' '}  "
                    for dia in semana  # Percorre a colecao especificada nesta linha e repete a instrucao do bloco para cada elemento.
                )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        print("\n* Dia com compromisso de estudo cadastrado.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.

    def editar_compromisso(self) -> None:  # Declara o metodo editar_compromisso nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        calendario = self._carregar()  # Atribui a calendario o resultado desta expressao: self._carregar(); esse valor sera usado nas proximas linhas.
        compromissos = self._compromissos_usuario(calendario)  # Atribui a compromissos o resultado desta expressao: self._compromissos_usuario(calendario); esse valor sera usado nas proximas linhas.
        ordenados = sorted(compromissos, key=self._data_hora)  # Ordena os registros pela chave declarada nesta chamada.
        if not ordenados:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Você não possui compromissos para editar.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        self._exibir_lista(ordenados)  # Executa nesta linha da classe GerenciadorCalendario e do metodo editar_compromisso a instrucao especifica: self._exibir_lista(ordenados)
        indice = self._ler_indice("Digite o número do compromisso que deseja editar: ", len(ordenados))  # Conta participantes ou elementos para exibir quantidade ou validar uma posicao.
        if indice is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        compromisso = ordenados[indice]  # Atribui a compromisso o resultado desta expressao: ordenados[indice]; esse valor sera usado nas proximas linhas.
        print("\nDeixe em branco o que não deseja alterar.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
        materia = input("Nova matéria: ").strip() or compromisso["materia"]  # Atribui a materia a resposta digitada no prompt Nova matéria: , removendo espacos externos antes da validacao.
        descricao = input("Nova descrição: ").strip() or compromisso["descricao"]  # Atribui a descricao a resposta digitada no prompt Nova descrição: , removendo espacos externos antes da validacao.
        data = input("Nova data (DD/MM/AAAA): ").strip() or compromisso["data"]  # Atribui a data a resposta digitada no prompt Nova data (DD/MM/AAAA): , removendo espacos externos antes da validacao.
        hora = input("Nova hora (HH:MM): ").strip() or compromisso["hora"]  # Atribui a hora a resposta digitada no prompt Nova hora (HH:MM): , removendo espacos externos antes da validacao.
        try:  # Inicia a operacao protegida; conversao ou acesso invalido sera tratado pelo bloco except seguinte.
            data_hora = self._interpretar_data_hora(data, hora)  # Atribui a data_hora o resultado desta expressao: self._interpretar_data_hora(data, hora); esse valor sera usado nas proximas linhas.
        except ValueError:  # Captura o erro especificado nesta linha e informa ou cancela a operacao sem processar dados invalidos.
            print("Data ou horário inválido.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        if data_hora < self.horario.obter_horario_atual():  # Rejeita o compromisso cujo instante ocorre antes do horario atual do gerenciador.
            print("Não é possível cadastrar um estudo em uma data passada.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        compromisso.update(  # Atualiza o registro com os pares chave-valor enviados pela edicao.
            {  # Inicia o objeto desta etapa e define nas linhas seguintes os campos e valores do novo registro.
                "materia": materia,  # Define a chave "materia" destestarutura para representar a materia do compromisso ou nota.
                "descricao": descricao,  # Define a chave "descricao" destestarutura para representar a descricao do estudo ou comunidade.
                "data": data_hora.strftime("%d/%m/%Y"),  # Define a chave "data" destestarutura para representar a data no formato DD/MM/AAAA.
                "hora": data_hora.strftime("%H:%M"),  # Define a chave "hora" destestarutura para representar o horario no formato HH:MM.
                "lembrete_exibido": False,  # Define a chave "lembrete_exibido" destestarutura para representar se o lembrete desse compromisso ja foi exibido.
            }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        self.persistencia.salvar(self.ARQUIVO, calendario)  # Persiste no arquivo JSON estarutura atualizada desta operacao.
        print("Compromisso atualizado com sucesso!")  # Informa ao usuario o resultado concluido ou cancelado desta operacao.

    def excluir_compromisso(self) -> None:  # Declara o metodo excluir_compromisso nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        calendario = self._carregar()  # Atribui a calendario o resultado desta expressao: self._carregar(); esse valor sera usado nas proximas linhas.
        compromissos = self._compromissos_usuario(calendario)  # Atribui a compromissos o resultado desta expressao: self._compromissos_usuario(calendario); esse valor sera usado nas proximas linhas.
        ordenados = sorted(compromissos, key=self._data_hora)  # Ordena os registros pela chave declarada nesta chamada.
        if not ordenados:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Você não possui compromissos para excluir.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        self._exibir_lista(ordenados)  # Executa nesta linha da classe GerenciadorCalendario e do metodo excluir_compromisso a instrucao especifica: self._exibir_lista(ordenados)
        indice = self._ler_indice("Digite o número do compromisso que deseja excluir: ", len(ordenados))  # Conta participantes ou elementos para exibir quantidade ou validar uma posicao.
        if indice is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        compromisso = ordenados[indice]  # Atribui a compromisso o resultado desta expressao: ordenados[indice]; esse valor sera usado nas proximas linhas.
        confirmacao = input(  # Atribui a confirmacao a resposta digitada no prompt campo solicitado, removendo espacos externos antes da validacao.
            f"Tem certeza que deseja excluir '{compromisso['materia']}'? (s/n): "  # Executa nesta linha da classe GerenciadorCalendario e do metodo excluir_compromisso a instrucao especifica: f"Tem certeza que deseja excluir '{compromisso['materia']}' (s/n): "
        ).strip().lower()  # Remove espacos externos antes da validacao ou armazenamento da entrada.
        if confirmacao != "s":  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print("Exclusão cancelada.")  # Informa ao usuario o resultado concluido ou cancelado desta operacao.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        compromissos.remove(compromisso)  # Remove da colecao o elemento identificado pela acao atual.
        self.persistencia.salvar(self.ARQUIVO, calendario)  # Persiste no arquivo JSON estarutura atualizada desta operacao.
        print("Compromisso excluído com sucesso!")  # Informa ao usuario o resultado concluido ou cancelado desta operacao.

    def verificar_lembretes(self) -> None:  # Declara o metodo verificar_lembretes nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        calendario = self._carregar()  # Atribui a calendario o resultado desta expressao: self._carregar(); esse valor sera usado nas proximas linhas.
        compromissos = self._compromissos_usuario(calendario)  # Atribui a compromissos o resultado desta expressao: self._compromissos_usuario(calendario); esse valor sera usado nas proximas linhas.
        agora = self.horario.obter_horario_atual()  # Atribui a agora o resultado desta expressao: self.horario.obter_horario_atual(); esse valor sera usado nas proximas linhas.
        encontrou = False  # Atribui a encontrou o resultado desta expressao: False; esse valor sera usado nas proximas linhas.
        for compromisso in compromissos:  # Percorre cada compromisso da conta atual para validar, exibir ou processar lembrete.
            if self._data_hora(compromisso) <= agora and not compromisso.get(  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                "lembrete_exibido", False  # Executa nesta linha da classe GerenciadorCalendario e do metodo verificar_lembretes a instrucao especifica: "lembrete_exibido", False
            ):  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
                print("\n====================================")  # Exibe o cabecalho desta secao da interface: \n====================================.
                print("       HORA DE ESTUDAR!")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
                print("====================================")  # Exibe o cabecalho desta secao da interface: ====================================.
                print(f"Matéria: {compromisso['materia']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
                print(f"Atividade: {compromisso['descricao']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
                print(f"Horário planejado: {compromisso['hora']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
                print("Não esqueça do seu compromisso de estudo!")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
                compromisso["lembrete_exibido"] = True  # Executa nesta linha da classe GerenciadorCalendario e do metodo verificar_lembretes a instrucao especifica: compromisso["lembrete_exibido"] = True
                encontrou = True  # Atribui a encontrou o resultado desta expressao: True; esse valor sera usado nas proximas linhas.
        if encontrou:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            self.persistencia.salvar(self.ARQUIVO, calendario)  # Persiste no arquivo JSON estarutura atualizada desta operacao.

    def _usuario_atual(self) -> str | None:  # Declara o metodo _usuario_atual nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self.estado.usuario_logado  # Atribui a ratname o resultado desta expressao: self.estado.usuario_logado; esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print("Você precisa fazer login para acessar o calendário.")  # Informa que o usuario precisestaar autenticado antes desta operacao.
        return ratname  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

    @staticmethod  # Aplica ao metodo seguinte o modificador @staticmethod para definir como ele sera chamado pela classe ou instancia.
    def _interpretar_data_hora(data: str, hora: str) -> datetime:  # Declara o metodo _interpretar_data_hora nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        return datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

    @classmethod  # Aplica ao metodo seguinte o modificador @classmethod para definir como ele sera chamado pela classe ou instancia.
    def _data_hora(cls, compromisso: dict) -> datetime:  # Declara o metodo _data_hora nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        try:  # Inicia a operacao protegida; conversao ou acesso invalido sera tratado pelo bloco except seguinte.
            return cls._interpretar_data_hora(  # Devolve para a chamada anterior o valor definido nesta linha de retorno.
                compromisso["data"], compromisso["hora"]  # Executa nesta linha da classe GerenciadorCalendario e do metodo _data_hora a instrucao especifica: compromisso["data"], compromisso["hora"]
            )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        except (KeyError, TypeError, ValueError) as erro:  # Captura o erro especificado nesta linha e informa ou cancela a operacao sem processar dados invalidos.
            raise ValueError("Um compromisso salvo possui data ou horário inválido.") from erro  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.

    @staticmethod  # Aplica ao metodo seguinte o modificador @staticmethod para definir como ele sera chamado pela classe ou instancia.
    def _exibir_lista(compromissos: list[dict]) -> None:  # Declara o metodo _exibir_lista nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        print("\n===== MEUS COMPROMISSOS =====")  # Exibe o cabecalho desta secao da interface: \n===== MEUS COMPROMISSOS =====.
        for indice, compromisso in enumerate(compromissos, start=1):  # Percorre cada compromisso da conta atual para validar, exibir ou processar lembrete.
            print(  # Exibe na tela a mensagem especifica formada por esta expressao de print.
                f"{indice}. {compromisso['materia']} | "  # Executa nesta linha da classe GerenciadorCalendario e do metodo _exibir_lista a instrucao especifica: f"{indice}. {compromisso['materia']} | "
                f"{compromisso['data']} às {compromisso['hora']}"  # Executa nesta linha da classe GerenciadorCalendario e do metodo _exibir_lista a instrucao especifica: f"{compromisso['data']} às {compromisso['hora']}"
            )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.

    @staticmethod  # Aplica ao metodo seguinte o modificador @staticmethod para definir como ele sera chamado pela classe ou instancia.
    def _ler_indice(pergunta: str, quantidade: int) -> int | None:  # Declara o metodo _ler_indice nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        try:  # Inicia a operacao protegida; conversao ou acesso invalido sera tratado pelo bloco except seguinte.
            numero = int(input(pergunta).strip())  # Remove espacos externos antes da validacao ou armazenamento da entrada.
        except ValueError:  # Captura o erro especificado nesta linha e informa ou cancela a operacao sem processar dados invalidos.
            print("Digite um número válido.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return None  # Encerra sem resultado porque login, perfil ou validacao bloqueou a operacao atual.
        if numero < 1 or numero > quantidade:  # Rejeita o numero fora das posicoes existentes na lista numerada exibida.
            print("Compromisso não encontrado.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return None  # Encerra sem resultado porque login, perfil ou validacao bloqueou a operacao atual.
        return numero - 1  # Devolve para a chamada anterior o valor definido nesta linha de retorno.
