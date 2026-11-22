from uuid import uuid4  # Importa uuid4 para gerar identificadores exclusivos de comunidades e eventos processados.

import lista  # Importa o modulo lista para compartilhar o estado global de login, perfil e usuarios desta aplicacao.
from Dados import persistencia  # Importa o gerenciador persistencia para ler e salvar os arquivos JSON desta funcionalidade.


class GerenciadorRatCoins:  # Define a classe GerenciadorRatCoins, responsavel por saldo, historico e ajustes de RatCoins.
    ARQUIVO = "ratcoins.json"  # Define o arquivo JSON ratcoins.json como destino e origem da persistencia desta funcionalidade.

    def __init__(self) -> None:  # Declara o metodo __init__ nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self.estado = lista.estado  # Atribui ao objeto o estado global que informa usuario conectado, tipo de conta e usuarios cadastrados.
        self.persistencia = persistencia  # Atribui ao objeto o gerenciador central usado para carregar e salvar os dados JSON.

    def _carregar_dados(self) -> dict:  # Declara o metodo _carregar_dados nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        dados = self.persistencia.carregar(  # Le os dados persistidos ou aplica o valor padrao definido nesta chamada.
            self.ARQUIVO,  # Executa nesta linha da classe GerenciadorRatCoins e do metodo _carregar_dados a instrucao especifica: self.ARQUIVO,
            {"usuarios": {}, "eventos_processados": {}},  # Inicia o objeto desta etapa e define nas linhas seguintes os campos e valores do novo registro.
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        if not isinstance(dados, dict):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError("O arquivo ratcoins.json deve conter um objeto JSON.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.

        if "usuarios" in dados and "eventos_processados" in dados:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            usuarios = dados["usuarios"]  # Atribui a usuarios o resultado desta expressao: dados["usuarios"]; esse valor sera usado nas proximas linhas.
            eventos = dados["eventos_processados"]  # Atribui a eventos o resultado desta expressao: dados["eventos_processados"]; esse valor sera usado nas proximas linhas.
            if not isinstance(usuarios, dict) or not isinstance(eventos, dict):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                raise ValueError("A estrutura do arquivo ratcoins.json está inválida.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        else:  # Executa o tratamento do caso restante que nao satisfez as condicoes anteriores desta decisao.
            usuarios = dados  # Atribui a usuarios o resultado desta expressao: dados; esse valor sera usado nas proximas linhas.
            eventos = {}  # Atribui a eventos o resultado desta expressao: {}; esse valor sera usado nas proximas linhas.

        for ratname, historico in usuarios.items():  # Percorre cada registro do historico para validar pontos ou somar o saldo.
            if not isinstance(historico, list):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                raise ValueError(f"O histórico de RatCoins de '{ratname}' está inválido.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        for ratname, chaves in eventos.items():  # Percorre a colecao especificada nesta linha e repete a instrucao do bloco para cada elemento.
            if not isinstance(chaves, list) or not all(  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                isinstance(chave, str) for chave in chaves  # Confere o tipo do dado antes de trata-lo como lista, objeto ou texto.
            ):  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
                raise ValueError(  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
                    f"Os eventos de RatCoins de '{ratname}' estão inválidos."  # Executa nesta linha da classe GerenciadorRatCoins e do metodo _carregar_dados a instrucao especifica: f"Os eventos de RatCoins de '{ratname}' estão inválidos."
                )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.

        return {"usuarios": usuarios, "eventos_processados": eventos}  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

    def _salvar_dados(self, dados: dict) -> None:  # Declara o metodo _salvar_dados nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self.persistencia.salvar(self.ARQUIVO, dados)  # Persiste no arquivo JSON estarutura atualizada desta operacao.

    def registrar_ganho(  # Declara o metodo registrar_ganho nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        self,  # Executa nesta linha da classe GerenciadorRatCoins e do metodo registrar_ganho a instrucao especifica: self,
        ratname: str,  # Executa nesta linha da classe GerenciadorRatCoins e do metodo registrar_ganho a instrucao especifica: ratname: str,
        atividade: str,  # Executa nesta linha da classe GerenciadorRatCoins e do metodo registrar_ganho a instrucao especifica: atividade: str,
        pontos: int,  # Executa nesta linha da classe GerenciadorRatCoins e do metodo registrar_ganho a instrucao especifica: pontos: int,
        evento_id: str | None = None,  # Executa nesta linha da classe GerenciadorRatCoins e do metodo registrar_ganho a instrucao especifica: evento_id: str | None = None,
    ) -> bool:  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        if not ratname or not isinstance(ratname, str):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError("É necessário informar um usuário para registrar RatCoins.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        if not atividade or not isinstance(atividade, str):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError("É necessário informar a atividade que gerou RatCoins.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        if type(pontos) is not int or pontos <= 0:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            raise ValueError("A quantidade de RatCoins deve ser um inteiro positivo.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        if evento_id is not None and (  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            not isinstance(evento_id, str) or not evento_id  # Confere o tipo do dado antes de trata-lo como lista, objeto ou texto.
        ):  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            raise ValueError("O identificador do evento deve ser um texto não vazio.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.

        dados = self._carregar_dados()  # Atribui a dados o resultado desta expressao: self._carregar_dados(); esse valor sera usado nas proximas linhas.
        usuarios = dados["usuarios"]  # Atribui a usuarios o resultado desta expressao: dados["usuarios"]; esse valor sera usado nas proximas linhas.
        eventos = dados["eventos_processados"]  # Atribui a eventos o resultado desta expressao: dados["eventos_processados"]; esse valor sera usado nas proximas linhas.
        eventos_usuario = eventos.setdefault(ratname, [])  # Recupera a colecao da chave ou cria uma lista vazia antes de inserir o novo dado.
        if evento_id is not None and evento_id in eventos_usuario:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            return False  # Retorna falso porque o ganho, ajuste ou alteracao nao sera aplicado nesta condicao.

        registro = {"atividade": atividade, "pontos": pontos}  # Atribui a registro o resultado desta expressao: {"atividade": atividade, "pontos": pontos}; esse valor sera usado nas proximas linhas.
        if evento_id is not None:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            registro["evento_id"] = evento_id  # Executa nesta linha da classe GerenciadorRatCoins e do metodo registrar_ganho a instrucao especifica: registro["evento_id"] = evento_id
            eventos_usuario.append(evento_id)  # Insere no fim da colecao o registro ou texto criado nesta etapa.
        usuarios.setdefault(ratname, []).append(registro)  # Recupera a colecao da chave ou cria uma lista vazia antes de inserir o novo dado.
        self._salvar_dados(dados)  # Executa nesta linha da classe GerenciadorRatCoins e do metodo registrar_ganho a instrucao especifica: self._salvar_dados(dados)
        print(f"Você ganhou {pontos} RatCoins!")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
        return True  # Retorna verdadeiro confirmando que o ganho ou ajuste foi registrado.

    def saldo(self, ratname: str) -> int:  # Declara o metodo saldo nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        historico = self._carregar_dados()["usuarios"].get(ratname, [])  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
        saldo_atual = 0  # Atribui a saldo_atual o resultado desta expressao: 0; esse valor sera usado nas proximas linhas.
        for registro in historico:  # Percorre cada registro do historico para validar pontos ou somar o saldo.
            if not isinstance(registro, dict):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
                raise ValueError(f"Um registro de RatCoins de '{ratname}' está inválido.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
            pontos = registro.get("pontos")  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
            if type(pontos) is not int:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
                raise ValueError(f"Um registro de RatCoins de '{ratname}' está inválido.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
            saldo_atual += pontos  # Executa nesta linha da classe GerenciadorRatCoins e do metodo saldo a instrucao especifica: saldo_atual += pontos
        return saldo_atual  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

    def ajustar_saldo(self, ratname: str, novo_saldo: int) -> bool:  # Declara o metodo ajustar_saldo nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        if not ratname or not isinstance(ratname, str):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError("É necessário informar um usuário para ajustar RatCoins.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        if type(novo_saldo) is not int or novo_saldo < 0:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            raise ValueError("O saldo deve ser um inteiro não negativo.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        if self.estado.usuario_logado != ratname:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            raise PermissionError("Só é possível ajustar o saldo da conta conectada.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        usuario = next(  # Atribui a usuario o resultado desta expressao: next(; esse valor sera usado nas proximas linhas.
            (item for item in self.estado.usuarios if item["ratname"] == ratname),  # Executa nesta linha da classe GerenciadorRatCoins e do metodo ajustar_saldo a instrucao especifica: (item for item in self.estado.usuarios if item["ratname"] == ratname),
            None,  # Executa nesta linha da classe GerenciadorRatCoins e do metodo ajustar_saldo a instrucao especifica: None,
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        if usuario is None or usuario.get("acesso_debug_2") is not True:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            raise PermissionError("O ajuste de saldo exige acesso ao DEBUG 2.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.

        dados = self._carregar_dados()  # Atribui a dados o resultado desta expressao: self._carregar_dados(); esse valor sera usado nas proximas linhas.
        historico = dados["usuarios"].setdefault(ratname, [])  # Recupera a colecao da chave ou cria uma lista vazia antes de inserir o novo dado.
        if not isinstance(historico, list):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError(f"O histórico de RatCoins de '{ratname}' está inválido.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        saldo_atual = sum(  # Atribui a saldo_atual o resultado desta expressao: sum(; esse valor sera usado nas proximas linhas.
            registro.get("pontos")  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
            for registro in historico  # Percorre cada registro do historico para validar pontos ou somar o saldo.
            if isinstance(registro, dict)  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            and type(registro.get("pontos")) is int  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        if any(  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            not isinstance(registro, dict)  # Confere o tipo do dado antes de trata-lo como lista, objeto ou texto.
            or type(registro.get("pontos")) is not int  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
            for registro in historico  # Percorre cada registro do historico para validar pontos ou somar o saldo.
        ):  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
            raise ValueError(f"O histórico de RatCoins de '{ratname}' está inválido.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        diferenca = novo_saldo - saldo_atual  # Atribui a diferenca o resultado desta expressao: novo_saldo - saldo_atual; esse valor sera usado nas proximas linhas.
        if diferenca == 0:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print(f"O saldo já é {novo_saldo} RC. Nenhum ajuste foi necessário.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return False  # Retorna falso porque o ganho, ajuste ou alteracao nao sera aplicado nesta condicao.

        evento_id = f"ajuste-saldo:{uuid4().hex}"  # Gera uma identificacao hexadecimal unica para o registro ou evento.
        historico.append(  # Insere no fim da colecao o registro ou texto criado nesta etapa.
            {  # Inicia o objeto desta etapa e define nas linhas seguintes os campos e valores do novo registro.
                "atividade": "Ajuste administrativo do saldo total",  # Define a chave "atividade" destestarutura para representar a atividade premiada.
                "pontos": diferenca,  # Define a chave "pontos" destestarutura para representar a quantidade de RatCoins.
                "tipo": "ajuste_saldo",  # Define a chave "tipo" destestarutura para representar o tipo administrativo do registro.
                "evento_id": evento_id,  # Define a chave "evento_id" destestarutura para representar o identificador unico do ganho ou ajuste.
            }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
        )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        dados["eventos_processados"].setdefault(ratname, []).append(evento_id)  # Recupera a colecao da chave ou cria uma lista vazia antes de inserir o novo dado.
        self._salvar_dados(dados)  # Executa nesta linha da classe GerenciadorRatCoins e do metodo ajustar_saldo a instrucao especifica: self._salvar_dados(dados)
        print(f"Saldo ajustado de {saldo_atual} para {novo_saldo} RC.")  # Exibe o saldo atual calculado em RatCoins nesta linha da interface.
        return True  # Retorna verdadeiro confirmando que o ganho ou ajuste foi registrado.

    def renomear_usuario(self, ratname_antigo: str, ratname_novo: str) -> None:  # Declara o metodo renomear_usuario nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        dados = self._carregar_dados()  # Atribui a dados o resultado desta expressao: self._carregar_dados(); esse valor sera usado nas proximas linhas.
        usuarios = dados["usuarios"]  # Atribui a usuarios o resultado desta expressao: dados["usuarios"]; esse valor sera usado nas proximas linhas.
        eventos = dados["eventos_processados"]  # Atribui a eventos o resultado desta expressao: dados["eventos_processados"]; esse valor sera usado nas proximas linhas.
        if ratname_novo in usuarios or ratname_novo in eventos:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            raise ValueError(  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
                f"Já existem dados de RatCoins associados a '{ratname_novo}'."  # Executa nesta linha da classe GerenciadorRatCoins e do metodo renomear_usuario a instrucao especifica: f"Já existem dados de RatCoins associados a '{ratname_novo}'."
            )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.

        historico = usuarios.pop(ratname_antigo, [])  # Remove destarutura a entrada escolhida pela posicao ou chave desta linha.
        if not isinstance(historico, list):  # Valida o tipo do dado carregado e interrompe o fluxo se ele nao corresponde ao formato esperado.
            raise ValueError(  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
                f"O histórico de RatCoins de '{ratname_antigo}' está inválido."  # Executa nesta linha da classe GerenciadorRatCoins e do metodo renomear_usuario a instrucao especifica: f"O histórico de RatCoins de '{ratname_antigo}' está inválido."
            )  # Fecha a chamada ou expressao iniciada acima e completa seus argumentos ou valores.
        usuarios[ratname_novo] = historico  # Executa nesta linha da classe GerenciadorRatCoins e do metodo renomear_usuario a instrucao especifica: usuarios[ratname_novo] = historico
        eventos_usuario = eventos.pop(ratname_antigo, [])  # Remove destarutura a entrada escolhida pela posicao ou chave desta linha.
        eventos[ratname_novo] = [  # Executa nesta linha da classe GerenciadorRatCoins e do metodo renomear_usuario a instrucao especifica: eventos[ratname_novo] = [
            evento.replace(ratname_antigo, ratname_novo)  # Executa nesta linha da classe GerenciadorRatCoins e do metodo renomear_usuario a instrucao especifica: evento.replace(ratname_antigo, ratname_novo)
            for evento in eventos_usuario  # Percorre a colecao especificada nesta linha e repete a instrucao do bloco para cada elemento.
        ]  # Executa nesta linha da classe GerenciadorRatCoins e do metodo renomear_usuario a instrucao especifica: ]
        self._salvar_dados(dados)  # Executa nesta linha da classe GerenciadorRatCoins e do metodo renomear_usuario a instrucao especifica: self._salvar_dados(dados)

    def historico(self, ratname: str) -> list[dict]:  # Declara o metodo historico nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        historico = self._carregar_dados()["usuarios"].get(ratname, [])  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
        if not all(isinstance(registro, dict) for registro in historico):  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            raise ValueError(f"O histórico de RatCoins de '{ratname}' está inválido.")  # Interrompe o fluxo com o erro especificado porque o dado persistido ou a autorizacao desta operacao falhou.
        return historico  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

    def remover_usuario(self, ratname: str) -> None:  # Declara o metodo remover_usuario nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        dados = self._carregar_dados()  # Atribui a dados o resultado desta expressao: self._carregar_dados(); esse valor sera usado nas proximas linhas.
        dados["usuarios"].pop(ratname, None)  # Remove destarutura a entrada escolhida pela posicao ou chave desta linha.
        dados["eventos_processados"].pop(ratname, None)  # Remove destarutura a entrada escolhida pela posicao ou chave desta linha.
        self._salvar_dados(dados)  # Executa nesta linha da classe GerenciadorRatCoins e do metodo remover_usuario a instrucao especifica: self._salvar_dados(dados)

    def consultar_saldo(self) -> None:  # Declara o metodo consultar_saldo nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self._usuario_atual()  # Atribui a ratname o resultado desta expressao: self._usuario_atual(); esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        print("\n===== MINHAS RATCOINS =====")  # Exibe o cabecalho desta secao da interface: \n===== MINHAS RATCOINS =====.
        print(f"Usuário: {ratname}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
        print(f"Saldo atual: {self.saldo(ratname)} RC")  # Exibe o saldo atual calculado em RatCoins nesta linha da interface.

    def consultar_historico(self) -> None:  # Declara o metodo consultar_historico nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self._usuario_atual()  # Atribui a ratname o resultado desta expressao: self._usuario_atual(); esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        historico = self.historico(ratname)  # Atribui a historico o resultado desta expressao: self.historico(ratname); esse valor sera usado nas proximas linhas.
        print("\n===== HISTÓRICO DE RATCOINS =====")  # Exibe o cabecalho desta secao da interface: \n===== HISTÓRICO DE RATCOINS =====.
        if not historico:  # Executa a ramificacao porque a colecao ou condicao especificadestaa vazia ou negada.
            print("Você ainda não ganhou RatCoins.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        for indice, registro in enumerate(historico, start=1):  # Percorre cada registro do historico para validar pontos ou somar o saldo.
            print(f"\n{indice}. {registro['atividade']}")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            print(f"Pontos: {registro['pontos']} RC")  # Exibe os pontos ganhos no registro atual nesta linha da interface.

    def menu(self) -> None:  # Declara o metodo menu nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        if self._usuario_atual() is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
        while True:  # Mantem o loop ativo enquanto a condicao desta linha permanece verdadeira, encerrando-o por return ou escolha de saida.
            print("\n========== RATCOINS ==========")  # Exibe o cabecalho desta secao da interface: \n========== RATCOINS ==========.
            print("1. Consultar meu saldo")  # Exibe na tela a opcao numero 1 com o texto e a acao correspondentes estae menu.
            print("2. Ver histórico de pontos")  # Exibe na tela a opcao numero 2 com o texto e a acao correspondentes estae menu.
            print("0. Voltar ao menu principal")  # Exibe a opcao 0, que encerrestaa tela e volta ao menu anterior.
            opcao = input("Escolha uma opção: ").strip()  # Atribui a opcao a resposta digitada no prompt Escolha uma opção: , removendo espacos externos antes da validacao.
            acoes = {  # Atribui a acoes o resultado desta expressao: {; esse valor sera usado nas proximas linhas.
                "1": self.consultar_saldo,  # Define a chave "1" destestarutura para representar o valor especifico desta entrada.
                "2": self.consultar_historico,  # Define a chave "2" destestarutura para representar o valor especifico desta entrada.
            }  # Fecha o objeto iniciado anteriormente, mantendo todos os pares chave-valor ja definidos.
            if opcao == "0":  # Executestaa ramificacao somente quando a escolha digitada for exatamente o numero ou texto indicado.
                return  # Encerrestae metodo e devolve o controle ao menu ou chamada anterior neste ponto.
            acao = acoes.get(opcao)  # Consulta o campo indicado e usa o valor padrao quando essa chave nao existe.
            if acao is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
                print("Opção inválida. Tente novamente.")  # Exibe na tela a mensagem especifica formada por esta expressao de print.
            else:  # Executa o tratamento do caso restante que nao satisfez as condicoes anteriores desta decisao.
                acao()  # Executa nesta linha da classe GerenciadorRatCoins e do metodo menu a instrucao especifica: acao()

    def _usuario_atual(self) -> str | None:  # Declara o metodo _usuario_atual nesta classe com esta assinatura, incluindo os parametros necessarios para realizar a operacao indicada pelo nome.
        ratname = self.estado.usuario_logado  # Atribui a ratname o resultado desta expressao: self.estado.usuario_logado; esse valor sera usado nas proximas linhas.
        if ratname is None:  # Avalia a condicao concreta desta linha antes de executar o bloco correspondente.
            print("Você precisa fazer login para acessar suas RatCoins.")  # Informa que o usuario precisestaar autenticado antes desta operacao.
        return ratname  # Devolve para a chamada anterior o valor definido nesta linha de retorno.

gerenciador_ratcoins = GerenciadorRatCoins()  # Atribui a gerenciador_ratcoins o resultado desta expressao: GerenciadorRatCoins(); esse valor sera usado nas proximas linhas.
