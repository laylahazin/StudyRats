import lista  # Importa lista: importa o estado central da aplicacao.
from Dados import gerenciador_credenciais, persistencia  # Importa de Dados gerenciador_credenciais, persistencia, reutilizando os recursos centrais de persistencia e credenciais.
from Ratcoins import gerenciador_ratcoins  # Importa de Ratcoins gerenciador_ratcoins, evitando criar outro gerenciador de recompensas.


class GerenciadorConta:  # Declara a classe GerenciadorConta: gerencia login, exclusao, edicao e debug da conta.
    SENHAS_DEBUG = {  # Guarda em SENHAS_DEBUG o valor produzido por {.
        "BSISTUDYRAT": "acesso_debug_1",  # Associa o codigo BSISTUDYRAT ao campo acesso_debug_1, que autoriza ajuste de data e horario.
        "BSISTUDYRATADM": "acesso_debug_2",  # Associa o codigo BSISTUDYRATADM ao campo acesso_debug_2, que autoriza ajuste do saldo RatCoins.
    }  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

    def __init__(self) -> None:  # Declara o metodo __init__: implementa esta funcionalidade da classe.
        self.estado = lista.estado  # Guarda em self.estado o valor produzido por lista.estado.
        self.persistencia = persistencia  # Guarda em self.persistencia o valor produzido por persistencia.
        self.gerenciador_credenciais = gerenciador_credenciais  # Guarda em self.gerenciador_credenciais o valor produzido por gerenciador_credenciais.

    def realizar_login(self) -> None:  # Declara o metodo realizar_login: procura o e-mail, verifica a senha e conecta o Ratname correspondente.
        print("\n--- TELA DE LOGIN ---")  # Exibe no terminal --- TELA DE LOGIN ---.
        email = input("Digite seu e-mail: ").strip().lower()  # guarda o e-mail normalizado usado para cadastrar ou localizar a conta
        senha = input("Digite sua senha: ")  # Guarda em senha o valor produzido por input("Digite sua senha: ").

        for usuario in self.estado.usuarios:  # Percorre usuario in self.estado.usuarios, executando o bloco uma vez para cada elemento.
            if usuario["email"].lower() != email:  # Testa a condicao usuario["email"].lower() != email e executa o bloco seguinte somente quando ela for verdadeira.
                continue  # Pula o restante da iteracao atual e volta ao inicio da proxima repeticao.

            if "senha_hash" not in usuario or "senha_salt" not in usuario:  # Testa a condicao "senha_hash" not in usuario or "senha_salt" not in usuario e executa o bloco seguinte somente quando ela for verdadeira.
                raise ValueError(  # Interrompe a operacao com ValueError(, indicando dados ou estado invalidos.
                    "A conta salva não possui credenciais compatíveis. "  # Executa nesta linha "A conta salva não possui credenciais compatíveis. " no contexto desta funcionalidade.
                    "Remova-a ou faça a migração antes de tentar entrar."  # Executa nesta linha "Remova-a ou faça a migração antes de tentar entrar." no contexto desta funcionalidade.
                )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

            if self.gerenciador_credenciais.verificar(  # Testa a condicao self.gerenciador_credenciais.verificar( e executa o bloco seguinte somente quando ela for verdadeira.
                senha, usuario["senha_salt"], usuario["senha_hash"]  # Executa nesta linha senha, usuario["senha_salt"], usuario["senha_hash"] no contexto desta funcionalidade.
            ):  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                self.estado.definir_usuario_logado(usuario["ratname"])  # Atualiza o usuario conectado com o Ratname informado; None encerra a sessao.
                print(  # Escreve no terminal o conteudo preparado por esta chamada.
                    "\nLogin bem-sucedido! Você está conectado como: "  # Executa nesta linha "\nLogin bem-sucedido! Você está conectado como: " no contexto desta funcionalidade.
                    f"{self.estado.usuario_logado}"  # Executa nesta linha f"{self.estado.usuario_logado}" no contexto desta funcionalidade.
                )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                return  # Encerra este metodo imediatamente sem devolver valor.
            break  # Encerra o loop atual e continua na primeira instrucao apos seu bloco.

        print("\nErro: E-mail ou senha incorretos.")  # Exibe no terminal Erro: E-mail ou senha incorretos..

    def excluir_conta(self) -> None:  # Declara o metodo excluir_conta: remove a conta ativa e seus dados associados.
        ratname = self.estado.usuario_logado  # guarda o nome publico usado como identificador da conta nos modulos da aplicacao
        if ratname is None:  # Verifica que nao existe usuario conectado; o bloco impede acesso aos dados pessoais.
            print("\nVocê precisa estar conectado para excluir a conta.")  # Exibe no terminal Você precisa estar conectado para excluir a conta..
            return  # Encerra este metodo imediatamente sem devolver valor.

        usuarios_atualizados = [  # cria a nova lista de contas contendo esta alteracao, sem perder os demais usuarios
            item for item in self.estado.usuarios if item["ratname"] != ratname  # Executa nesta linha item for item in self.estado.usuarios if item["ratname"] != ratname no contexto desta funcionalidade.
        ]  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        if len(usuarios_atualizados) == len(self.estado.usuarios):  # Testa a condicao len(usuarios_atualizados) == len(self.estado.usuarios) e executa o bloco seguinte somente quando ela for verdadeira.
            print("\nConta não encontrada para exclusão.")  # Exibe no terminal Conta não encontrada para exclusão..
            self.estado.definir_usuario_logado(None)  # Atualiza o usuario conectado com o Ratname informado; None encerra a sessao.
            return  # Encerra este metodo imediatamente sem devolver valor.

        self.persistencia.salvar("usuarios.json", usuarios_atualizados)  # Persiste no arquivo JSON indicado o novo estado da estrutura atual.
        self.estado.substituir_usuarios(usuarios_atualizados)  # Substitui a lista em memoria das contas pela lista atualizada.

        for arquivo in (  # Percorre arquivo in (, executando o bloco uma vez para cada elemento.
            "modelos_estudo.json",  # Executa nesta linha "modelos_estudo.json", no contexto desta funcionalidade.
            "presencas.json",  # Executa nesta linha "presencas.json", no contexto desta funcionalidade.
            "calendario.json",  # Executa nesta linha "calendario.json", no contexto desta funcionalidade.
            "blocos_notas.json",  # Executa nesta linha "blocos_notas.json", no contexto desta funcionalidade.
            "notificacoes.json",  # Executa nesta linha "notificacoes.json", no contexto desta funcionalidade.
        ):  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            dados = self.persistencia.carregar(arquivo, {})  # Guarda em dados o valor produzido por self.persistencia.carregar(arquivo, {}).
            if isinstance(dados, dict):  # Testa a condicao isinstance(dados, dict) e executa o bloco seguinte somente quando ela for verdadeira.
                if arquivo == "notificacoes.json":  # Testa a condicao arquivo == "notificacoes.json" e executa o bloco seguinte somente quando ela for verdadeira.
                    dados.get("usuarios", {}).pop(ratname, None)  # Executa nesta linha dados.get("usuarios", {}).pop(ratname, None) no contexto desta funcionalidade.
                else:  # Executa este bloco quando nenhuma condicao anterior da cadeia foi atendida.
                    dados.pop(ratname, None)  # Executa nesta linha dados.pop(ratname, None) no contexto desta funcionalidade.
                self.persistencia.salvar(arquivo, dados)  # Persiste no arquivo JSON indicado o novo estado da estrutura atual.
        gerenciador_ratcoins.remover_usuario(ratname)  # Remove saldos e eventos RatCoins associados ao Ratname excluido.

        print(f"\nA conta de {ratname} foi excluída com sucesso.")  # Exibe no terminal A conta de {ratname} foi excluída com sucesso..
        self.estado.definir_usuario_logado(None)  # Atualiza o usuario conectado com o Ratname informado; None encerra a sessao.

    def editar_conta(self) -> None:  # Declara o metodo editar_conta: atualiza identidade ou senha depois de confirmar a senha atual.
        usuario = self._usuario_logado()  # recupera o registro completo da conta atualmente conectada
        if usuario is None:  # Verifica que o registro da conta ativa nao foi encontrado.
            return  # Encerra este metodo imediatamente sem devolver valor.
        if not self._confirmar_senha_atual(usuario):  # Testa a condicao not self._confirmar_senha_atual(usuario) e executa o bloco seguinte somente quando ela for verdadeira.
            print("Senha atual incorreta. Nenhuma alteração foi feita.")  # Exibe no terminal Senha atual incorreta. Nenhuma alteração foi feita..
            return  # Encerra este metodo imediatamente sem devolver valor.

        ratname_antigo = usuario["ratname"]  # preserva o nome publico usado antes da edicao
        email_antigo = usuario["email"]  # preserva o e-mail usado antes da edicao
        novo_email = input(  # guarda o novo e-mail digitado ou vazio para manter o atual
            f"Novo e-mail (Enter mantém {email_antigo}): "  # Executa nesta linha f"Novo e-mail (Enter mantém {email_antigo}): " no contexto desta funcionalidade.
        ).strip().lower()  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        novo_ratname = input(  # guarda o novo Ratname digitado ou vazio para manter o atual
            f"Novo Ratname (Enter mantém {ratname_antigo}): "  # Executa nesta linha f"Novo Ratname (Enter mantém {ratname_antigo}): " no contexto desta funcionalidade.
        ).strip()  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        nova_senha = input(  # guarda a nova senha digitada ou vazio para manter a atual
            "Nova senha (Enter mantém a atual): "  # Executa nesta linha "Nova senha (Enter mantém a atual): " no contexto desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

        if novo_email and not self._email_valido(novo_email):  # Testa a condicao novo_email and not self._email_valido(novo_email) e executa o bloco seguinte somente quando ela for verdadeira.
            print("E-mail inválido. Use um endereço institucional @ufrpe.br.")  # Exibe no terminal E-mail inválido. Use um endereço institucional @ufrpe.br..
            return  # Encerra este metodo imediatamente sem devolver valor.
        if novo_email and any(  # Testa a condicao novo_email and any( e executa o bloco seguinte somente quando ela for verdadeira.
            item["ratname"] != ratname_antigo  # Executa nesta linha item["ratname"] != ratname_antigo no contexto desta funcionalidade.
            and item["email"].casefold() == novo_email.casefold()  # Executa nesta linha and item["email"].casefold() == novo_email.casefold() no contexto desta funcionalidade.
            for item in self.estado.usuarios  # Percorre item in self.estado.usuarios, executando o bloco uma vez para cada elemento.
        ):  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            print("Este e-mail já está cadastrado.")  # Exibe no terminal Este e-mail já está cadastrado..
            return  # Encerra este metodo imediatamente sem devolver valor.
        if novo_ratname and any(  # Testa a condicao novo_ratname and any( e executa o bloco seguinte somente quando ela for verdadeira.
            item["ratname"].casefold() == novo_ratname.casefold()  # Executa nesta linha item["ratname"].casefold() == novo_ratname.casefold() no contexto desta funcionalidade.
            and item["ratname"] != ratname_antigo  # Executa nesta linha and item["ratname"] != ratname_antigo no contexto desta funcionalidade.
            for item in self.estado.usuarios  # Percorre item in self.estado.usuarios, executando o bloco uma vez para cada elemento.
        ):  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            print("Este Ratname já está em uso.")  # Exibe no terminal Este Ratname já está em uso..
            return  # Encerra este metodo imediatamente sem devolver valor.
        if nova_senha and not self._senha_valida(nova_senha):  # Testa a condicao nova_senha and not self._senha_valida(nova_senha) e executa o bloco seguinte somente quando ela for verdadeira.
            print(  # Escreve no terminal o conteudo preparado por esta chamada.
                "A senha deve ter de 6 a 8 caracteres, uma letra maiúscula, "  # Executa nesta linha "A senha deve ter de 6 a 8 caracteres, uma letra maiúscula, " no contexto desta funcionalidade.
                "um número e um caractere especial."  # Executa nesta linha "um número e um caractere especial." no contexto desta funcionalidade.
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            return  # Encerra este metodo imediatamente sem devolver valor.

        ratname_novo = novo_ratname or ratname_antigo  # guarda o novo nome publico depois da validacao da edicao
        email_novo = novo_email or email_antigo  # guarda o e-mail final depois da validacao da edicao
        if (  # Testa a condicao ( e executa o bloco seguinte somente quando ela for verdadeira.
            ratname_novo == ratname_antigo  # Executa nesta linha ratname_novo == ratname_antigo no contexto desta funcionalidade.
            and email_novo == email_antigo  # Executa nesta linha and email_novo == email_antigo no contexto desta funcionalidade.
            and not nova_senha  # Executa nesta linha and not nova_senha no contexto desta funcionalidade.
        ):  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            print("Nenhuma alteração foi informada.")  # Exibe no terminal Nenhuma alteração foi informada..
            return  # Encerra este metodo imediatamente sem devolver valor.

        if ratname_novo != ratname_antigo or email_novo != email_antigo:  # Testa a condicao ratname_novo != ratname_antigo or email_novo != email_antigo e executa o bloco seguinte somente quando ela for verdadeira.
            self._atualizar_referencias_usuario(  # Executa self._atualizar_referencias_usuario(; o efeito desta chamada participa diretamente desta funcionalidade.
                ratname_antigo,  # Executa nesta linha ratname_antigo, no contexto desta funcionalidade.
                ratname_novo,  # Executa nesta linha ratname_novo, no contexto desta funcionalidade.
                email_novo,  # Executa nesta linha email_novo, no contexto desta funcionalidade.
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

        usuarios_atualizados = [dict(item) for item in self.estado.usuarios]  # cria a nova lista de contas contendo esta alteracao, sem perder os demais usuarios
        usuario_atualizado = next(  # Guarda em usuario_atualizado o valor produzido por next(.
            item for item in usuarios_atualizados  # Executa nesta linha item for item in usuarios_atualizados no contexto desta funcionalidade.
            if item["ratname"] == ratname_antigo  # Testa a condicao item["ratname"] == ratname_antigo e executa o bloco seguinte somente quando ela for verdadeira.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        usuario_atualizado["ratname"] = ratname_novo  # Guarda em usuario_atualizado["ratname"] o valor produzido por ratname_novo.
        usuario_atualizado["email"] = email_novo  # Guarda em usuario_atualizado["email"] o valor produzido por email_novo.
        if nova_senha:  # Testa a condicao nova_senha e executa o bloco seguinte somente quando ela for verdadeira.
            usuario_atualizado.update(self.gerenciador_credenciais.criar(nova_senha))  # Executa nesta linha usuario_atualizado.update(self.gerenciador_credenciais.criar(nova_senha)) no contexto desta funcionalidade.
        self.persistencia.salvar("usuarios.json", usuarios_atualizados)  # Persiste no arquivo JSON indicado o novo estado da estrutura atual.
        self.estado.substituir_usuarios(usuarios_atualizados)  # Substitui a lista em memoria das contas pela lista atualizada.
        if ratname_novo != ratname_antigo:  # Testa a condicao ratname_novo != ratname_antigo e executa o bloco seguinte somente quando ela for verdadeira.
            self.estado.definir_usuario_logado(ratname_novo)  # Atualiza o usuario conectado com o Ratname informado; None encerra a sessao.
        print("Dados da conta atualizados com sucesso.")  # Exibe no terminal Dados da conta atualizados com sucesso..

    def menu_debug_codes(self) -> None:  # Declara o metodo menu_debug_codes: permite liberar acessos DEBUG ligados aos codigos administrativos.
        usuario = self._usuario_logado()  # recupera o registro completo da conta atualmente conectada
        if usuario is None:  # Verifica que o registro da conta ativa nao foi encontrado.
            return  # Encerra este metodo imediatamente sem devolver valor.
        while True:  # Mantem o loop ativo ate encontrar uma opcao que devolva ou encerre o fluxo.
            print("\n===== ACESSOS DEBUG =====")  # Exibe no terminal ===== ACESSOS DEBUG =====.
            print(  # Escreve no terminal o conteudo preparado por esta chamada.
                "DEBUG 1 - Alteração de data/horário: "  # Executa nesta linha "DEBUG 1 - Alteração de data/horário: " no contexto desta funcionalidade.
                f"{'liberado' if usuario.get('acesso_debug_1') is True else 'bloqueado'}"  # Executa nesta linha f"{'liberado' if usuario.get('acesso_debug_1') is True else 'bloqueado'}" no contexto desta funcionalidade.
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            print(  # Escreve no terminal o conteudo preparado por esta chamada.
                "DEBUG 2 - Alteração do saldo RatCoins: "  # Executa nesta linha "DEBUG 2 - Alteração do saldo RatCoins: " no contexto desta funcionalidade.
                f"{'liberado' if usuario.get('acesso_debug_2') is True else 'bloqueado'}"  # Executa nesta linha f"{'liberado' if usuario.get('acesso_debug_2') is True else 'bloqueado'}" no contexto desta funcionalidade.
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            print("Digite um código administrativo para liberar o acesso correspondente.")  # Exibe no terminal Digite um código administrativo para liberar o acesso correspondente..
            print("0. Voltar ao perfil")  # Exibe no terminal 0. Voltar ao perfil.
            senha = input("Código: ").strip()  # Guarda em senha o valor produzido por input("Código: ").strip().
            if senha == "0":  # Testa a condicao senha == "0" e executa o bloco seguinte somente quando ela for verdadeira.
                return  # Encerra este metodo imediatamente sem devolver valor.
            acesso = self.SENHAS_DEBUG.get(senha)  # Traduz o codigo digitado no campo de permissao correspondente; codigo desconhecido devolve None.
            if acesso is None:  # Testa a condicao acesso is None e executa o bloco seguinte somente quando ela for verdadeira.
                print("Código inválido.")  # Exibe no terminal Código inválido..
                continue  # Pula o restante da iteracao atual e volta ao inicio da proxima repeticao.
            if usuario.get(acesso) is True:  # Testa a condicao usuario.get(acesso) is True e executa o bloco seguinte somente quando ela for verdadeira.
                print("Este acesso DEBUG já está liberado para sua conta.")  # Exibe no terminal Este acesso DEBUG já está liberado para sua conta..
                continue  # Pula o restante da iteracao atual e volta ao inicio da proxima repeticao.
            usuario[acesso] = True  # Marca no registro da conta ativa a permissao correspondente ao codigo digitado.
            self.estado.salvar_usuarios()  # Executa self.estado.salvar_usuarios(); o efeito desta chamada participa diretamente desta funcionalidade.
            print(f"{acesso.replace('acesso_', '').upper()} liberado para esta conta.")  # Exibe no terminal {acesso.replace(.

    @staticmethod  # Aplica o decorador ao metodo seguinte.
    def tem_acesso_debug(usuario: dict, nivel: int) -> bool:  # Declara o metodo tem_acesso_debug: verifica se o campo acesso_debug_1 ou acesso_debug_2 esta liberado.
        if nivel not in (1, 2):  # Testa a condicao nivel not in (1, 2) e executa o bloco seguinte somente quando ela for verdadeira.
            raise ValueError("O nível DEBUG deve ser 1 ou 2.")  # Interrompe a operacao com ValueError("O nível DEBUG deve ser 1 ou 2."), indicando dados ou estado invalidos.
        return usuario.get(f"acesso_debug_{nivel}") is True  # Consulta acesso_debug_1 no nivel 1 ou acesso_debug_2 no nivel 2 e informa se esta liberado.

    def _atualizar_referencias_usuario(  # Declara o metodo _atualizar_referencias_usuario: implementa esta funcionalidade da classe.
        self,  # Executa nesta linha self, no contexto desta funcionalidade.
        ratname_antigo: str,  # Executa nesta linha ratname_antigo: str, no contexto desta funcionalidade.
        ratname_novo: str,  # Executa nesta linha ratname_novo: str, no contexto desta funcionalidade.
        email_novo: str,  # Executa nesta linha email_novo: str, no contexto desta funcionalidade.
    ) -> None:  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        arquivos_chave = (  # Guarda em arquivos_chave o valor produzido por (.
            "modelos_estudo.json",  # Executa nesta linha "modelos_estudo.json", no contexto desta funcionalidade.
            "presencas.json",  # Executa nesta linha "presencas.json", no contexto desta funcionalidade.
            "calendario.json",  # Executa nesta linha "calendario.json", no contexto desta funcionalidade.
            "blocos_notas.json",  # Executa nesta linha "blocos_notas.json", no contexto desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        atualizacoes = {}  # Guarda em atualizacoes o valor produzido por {}.
        for arquivo in arquivos_chave:  # Percorre arquivo in arquivos_chave, executando o bloco uma vez para cada elemento.
            dados = self.persistencia.carregar(arquivo, {})  # Guarda em dados o valor produzido por self.persistencia.carregar(arquivo, {}).
            if not isinstance(dados, dict):  # Testa a condicao not isinstance(dados, dict) e executa o bloco seguinte somente quando ela for verdadeira.
                raise ValueError(f"O arquivo {arquivo} deve conter um objeto JSON.")  # Interrompe a operacao com ValueError(f"O arquivo {arquivo} deve conter um objeto JSON."), indicando dados ou estado invalidos.
            if ratname_novo != ratname_antigo and ratname_novo in dados:  # Testa a condicao ratname_novo != ratname_antigo and ratname_novo in dados e executa o bloco seguinte somente quando ela for verdadeira.
                raise ValueError(  # Interrompe a operacao com ValueError(, indicando dados ou estado invalidos.
                    f"Já existem dados associados ao Ratname '{ratname_novo}'."  # Executa nesta linha f"Já existem dados associados ao Ratname '{ratname_novo}'." no contexto desta funcionalidade.
                )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            if ratname_antigo in dados and ratname_novo != ratname_antigo:  # Testa a condicao ratname_antigo in dados and ratname_novo != ratname_antigo e executa o bloco seguinte somente quando ela for verdadeira.
                dados[ratname_novo] = dados.pop(ratname_antigo)  # Guarda em dados[ratname_novo] o valor produzido por dados.pop(ratname_antigo).
            atualizacoes[arquivo] = dados  # Guarda em atualizacoes[arquivo] o valor produzido por dados.

        participacoes = self.persistencia.carregar("participantes_salas.json", {})  # Guarda em participacoes o valor produzido por self.persistencia.carregar("participantes_salas.json", {}).
        self._atualizar_participacoes(  # Executa self._atualizar_participacoes(; o efeito desta chamada participa diretamente desta funcionalidade.
            participacoes,  # Executa nesta linha participacoes, no contexto desta funcionalidade.
            ratname_antigo,  # Executa nesta linha ratname_antigo, no contexto desta funcionalidade.
            ratname_novo,  # Executa nesta linha ratname_novo, no contexto desta funcionalidade.
            email_novo,  # Executa nesta linha email_novo, no contexto desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        atualizacoes["participantes_salas.json"] = participacoes  # Guarda em atualizacoes["participantes_salas.json"] o valor produzido por participacoes.

        comunidades = self.persistencia.carregar("comunidades.json", [])  # Guarda em comunidades o valor produzido por self.persistencia.carregar("comunidades.json", []).
        self._atualizar_comunidades(  # Executa self._atualizar_comunidades(; o efeito desta chamada participa diretamente desta funcionalidade.
            comunidades, ratname_antigo, ratname_novo  # Executa nesta linha comunidades, ratname_antigo, ratname_novo no contexto desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        atualizacoes["comunidades.json"] = comunidades  # Guarda em atualizacoes["comunidades.json"] o valor produzido por comunidades.

        notificacoes = self.persistencia.carregar(  # Guarda em notificacoes o valor produzido por self.persistencia.carregar(.
            "notificacoes.json",  # Executa nesta linha "notificacoes.json", no contexto desta funcionalidade.
            {"usuarios": {}, "datas_processadas": []},  # Executa nesta linha {"usuarios": {}, "datas_processadas": []}, no contexto desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        self._atualizar_notificacoes(  # Executa self._atualizar_notificacoes(; o efeito desta chamada participa diretamente desta funcionalidade.
            notificacoes, ratname_antigo, ratname_novo  # Executa nesta linha notificacoes, ratname_antigo, ratname_novo no contexto desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        atualizacoes["notificacoes.json"] = notificacoes  # Guarda em atualizacoes["notificacoes.json"] o valor produzido por notificacoes.

        if ratname_novo != ratname_antigo:  # Testa a condicao ratname_novo != ratname_antigo e executa o bloco seguinte somente quando ela for verdadeira.
            dados_ratcoins = gerenciador_ratcoins._carregar_dados()  # Guarda em dados_ratcoins o valor produzido por gerenciador_ratcoins._carregar_dados().
            if (  # Testa a condicao ( e executa o bloco seguinte somente quando ela for verdadeira.
                ratname_novo in dados_ratcoins["usuarios"]  # Executa nesta linha ratname_novo in dados_ratcoins["usuarios"] no contexto desta funcionalidade.
                or ratname_novo in dados_ratcoins["eventos_processados"]  # Executa nesta linha or ratname_novo in dados_ratcoins["eventos_processados"] no contexto desta funcionalidade.
            ):  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                raise ValueError(  # Interrompe a operacao com ValueError(, indicando dados ou estado invalidos.
                    f"Já existem RatCoins associados ao Ratname '{ratname_novo}'."  # Executa nesta linha f"Já existem RatCoins associados ao Ratname '{ratname_novo}'." no contexto desta funcionalidade.
                )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

        for arquivo, dados in atualizacoes.items():  # Percorre arquivo, dados in atualizacoes.items(), executando o bloco uma vez para cada elemento.
            self.persistencia.salvar(arquivo, dados)  # Persiste no arquivo JSON indicado o novo estado da estrutura atual.
        if ratname_novo != ratname_antigo:  # Testa a condicao ratname_novo != ratname_antigo e executa o bloco seguinte somente quando ela for verdadeira.
            gerenciador_ratcoins.renomear_usuario(  # Migra dados RatCoins do Ratname antigo para o novo.
                ratname_antigo, ratname_novo  # Executa nesta linha ratname_antigo, ratname_novo no contexto desta funcionalidade.
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

    @staticmethod  # Aplica o decorador ao metodo seguinte.
    def _atualizar_participacoes(  # Declara o metodo _atualizar_participacoes: implementa esta funcionalidade da classe.
        participacoes: dict,  # Executa nesta linha participacoes: dict, no contexto desta funcionalidade.
        ratname_antigo: str,  # Executa nesta linha ratname_antigo: str, no contexto desta funcionalidade.
        ratname_novo: str,  # Executa nesta linha ratname_novo: str, no contexto desta funcionalidade.
        email_novo: str,  # Executa nesta linha email_novo: str, no contexto desta funcionalidade.
    ) -> None:  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        if not isinstance(participacoes, dict):  # Testa a condicao not isinstance(participacoes, dict) e executa o bloco seguinte somente quando ela for verdadeira.
            raise ValueError("O arquivo participantes_salas.json está inválido.")  # Interrompe a operacao com ValueError("O arquivo participantes_salas.json está inválido."), indicando dados ou estado invalidos.
        for sessoes in participacoes.values():  # Percorre sessoes in participacoes.values(), executando o bloco uma vez para cada elemento.
            if not isinstance(sessoes, dict):  # Testa a condicao not isinstance(sessoes, dict) e executa o bloco seguinte somente quando ela for verdadeira.
                raise ValueError("As sessões de uma sala estão inválidas.")  # Interrompe a operacao com ValueError("As sessões de uma sala estão inválidas."), indicando dados ou estado invalidos.
            for sessao in sessoes.values():  # Percorre sessao in sessoes.values(), executando o bloco uma vez para cada elemento.
                if not isinstance(sessao, dict):  # Testa a condicao not isinstance(sessao, dict) e executa o bloco seguinte somente quando ela for verdadeira.
                    raise ValueError("Uma sessão de sala está inválida.")  # Interrompe a operacao com ValueError("Uma sessão de sala está inválida."), indicando dados ou estado invalidos.
                participantes = sessao.get("participantes", {})  # Guarda em participantes o valor produzido por sessao.get("participantes", {}).
                if not isinstance(participantes, dict):  # Testa a condicao not isinstance(participantes, dict) e executa o bloco seguinte somente quando ela for verdadeira.
                    raise ValueError("Os participantes de uma sessão estão inválidos.")  # Interrompe a operacao com ValueError("Os participantes de uma sessão estão inválidos."), indicando dados ou estado invalidos.
                if (  # Testa a condicao ( e executa o bloco seguinte somente quando ela for verdadeira.
                    ratname_novo != ratname_antigo  # Executa nesta linha ratname_novo != ratname_antigo no contexto desta funcionalidade.
                    and ratname_antigo in participantes  # Executa nesta linha and ratname_antigo in participantes no contexto desta funcionalidade.
                    and ratname_novo in participantes  # Executa nesta linha and ratname_novo in participantes no contexto desta funcionalidade.
                ):  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                    raise ValueError(  # Interrompe a operacao com ValueError(, indicando dados ou estado invalidos.
                        f"Já existe participação registrada para '{ratname_novo}'."  # Executa nesta linha f"Já existe participação registrada para '{ratname_novo}'." no contexto desta funcionalidade.
                    )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                if ratname_antigo in participantes:  # Testa a condicao ratname_antigo in participantes e executa o bloco seguinte somente quando ela for verdadeira.
                    participante = participantes.pop(ratname_antigo)  # Guarda em participante o valor produzido por participantes.pop(ratname_antigo).
                    participante["email"] = email_novo  # Guarda em participante["email"] o valor produzido por email_novo.
                    participantes[ratname_novo] = participante  # Guarda em participantes[ratname_novo] o valor produzido por participante.
                for atividade in sessao.get("atividades", []):  # Percorre atividade in sessao.get("atividades", []), executando o bloco uma vez para cada elemento.
                    if atividade.get("monitor") == ratname_antigo:  # Testa a condicao atividade.get("monitor") == ratname_antigo e executa o bloco seguinte somente quando ela for verdadeira.
                        atividade["monitor"] = ratname_novo  # Guarda em atividade["monitor"] o valor produzido por ratname_novo.
                for duvida in sessao.get("duvidas", []):  # Percorre duvida in sessao.get("duvidas", []), executando o bloco uma vez para cada elemento.
                    if duvida.get("usuario") == ratname_antigo:  # Testa a condicao duvida.get("usuario") == ratname_antigo e executa o bloco seguinte somente quando ela for verdadeira.
                        duvida["usuario"] = ratname_novo  # Guarda em duvida["usuario"] o valor produzido por ratname_novo.
                    for resposta in duvida.get("respostas", []):  # Percorre resposta in duvida.get("respostas", []), executando o bloco uma vez para cada elemento.
                        if resposta.get("usuario") == ratname_antigo:  # Testa a condicao resposta.get("usuario") == ratname_antigo e executa o bloco seguinte somente quando ela for verdadeira.
                            resposta["usuario"] = ratname_novo  # Guarda em resposta["usuario"] o valor produzido por ratname_novo.

    @staticmethod  # Aplica o decorador ao metodo seguinte.
    def _atualizar_comunidades(  # Declara o metodo _atualizar_comunidades: implementa esta funcionalidade da classe.
        comunidades: list,  # Executa nesta linha comunidades: list, no contexto desta funcionalidade.
        ratname_antigo: str,  # Executa nesta linha ratname_antigo: str, no contexto desta funcionalidade.
        ratname_novo: str,  # Executa nesta linha ratname_novo: str, no contexto desta funcionalidade.
    ) -> None:  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        if not isinstance(comunidades, list):  # Testa a condicao not isinstance(comunidades, list) e executa o bloco seguinte somente quando ela for verdadeira.
            raise ValueError("O arquivo comunidades.json está inválido.")  # Interrompe a operacao com ValueError("O arquivo comunidades.json está inválido."), indicando dados ou estado invalidos.
        for comunidade in comunidades:  # Percorre comunidade in comunidades, executando o bloco uma vez para cada elemento.
            if not isinstance(comunidade, dict):  # Testa a condicao not isinstance(comunidade, dict) e executa o bloco seguinte somente quando ela for verdadeira.
                raise ValueError("Uma comunidade salva está inválida.")  # Interrompe a operacao com ValueError("Uma comunidade salva está inválida."), indicando dados ou estado invalidos.
            if comunidade.get("criador") == ratname_antigo:  # Testa a condicao comunidade.get("criador") == ratname_antigo e executa o bloco seguinte somente quando ela for verdadeira.
                comunidade["criador"] = ratname_novo  # Guarda em comunidade["criador"] o valor produzido por ratname_novo.
            membros = comunidade.get("membros", [])  # Guarda em membros o valor produzido por comunidade.get("membros", []).
            if not isinstance(membros, list):  # Testa a condicao not isinstance(membros, list) e executa o bloco seguinte somente quando ela for verdadeira.
                raise ValueError("A lista de membros de uma comunidade está inválida.")  # Interrompe a operacao com ValueError("A lista de membros de uma comunidade está inválida."), indicando dados ou estado invalidos.
            comunidade["membros"] = [  # Guarda em comunidade["membros"] o valor produzido por [.
                ratname_novo if membro == ratname_antigo else membro  # Executa nesta linha ratname_novo if membro == ratname_antigo else membro no contexto desta funcionalidade.
                for membro in membros  # Percorre membro in membros, executando o bloco uma vez para cada elemento.
            ]  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            for publicacao in comunidade.get("publicacoes", []):  # Percorre publicacao in comunidade.get("publicacoes", []), executando o bloco uma vez para cada elemento.
                if publicacao.get("autor") == ratname_antigo:  # Testa a condicao publicacao.get("autor") == ratname_antigo e executa o bloco seguinte somente quando ela for verdadeira.
                    publicacao["autor"] = ratname_novo  # Guarda em publicacao["autor"] o valor produzido por ratname_novo.
                for resposta in publicacao.get("respostas", []):  # Percorre resposta in publicacao.get("respostas", []), executando o bloco uma vez para cada elemento.
                    if resposta.get("autor") == ratname_antigo:  # Testa a condicao resposta.get("autor") == ratname_antigo e executa o bloco seguinte somente quando ela for verdadeira.
                        resposta["autor"] = ratname_novo  # Guarda em resposta["autor"] o valor produzido por ratname_novo.

    @staticmethod  # Aplica o decorador ao metodo seguinte.
    def _atualizar_notificacoes(  # Declara o metodo _atualizar_notificacoes: implementa esta funcionalidade da classe.
        notificacoes: dict,  # Executa nesta linha notificacoes: dict, no contexto desta funcionalidade.
        ratname_antigo: str,  # Executa nesta linha ratname_antigo: str, no contexto desta funcionalidade.
        ratname_novo: str,  # Executa nesta linha ratname_novo: str, no contexto desta funcionalidade.
    ) -> None:  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        if not isinstance(notificacoes, dict):  # Testa a condicao not isinstance(notificacoes, dict) e executa o bloco seguinte somente quando ela for verdadeira.
            raise ValueError("O arquivo notificacoes.json está inválido.")  # Interrompe a operacao com ValueError("O arquivo notificacoes.json está inválido."), indicando dados ou estado invalidos.
        usuarios = notificacoes.setdefault("usuarios", {})  # representa a lista ou o mapa de usuarios usado pela operacao atual
        if not isinstance(usuarios, dict):  # Testa a condicao not isinstance(usuarios, dict) e executa o bloco seguinte somente quando ela for verdadeira.
            raise ValueError("A lista de notificações de usuários está inválida.")  # Interrompe a operacao com ValueError("A lista de notificações de usuários está inválida."), indicando dados ou estado invalidos.
        pendentes = usuarios.pop(ratname_antigo, [])  # Remove a lista de pendencias do Ratname antigo para transferi-las ao novo nome.
        usuarios.setdefault(ratname_novo, []).extend(pendentes)  # Obtem ou cria a lista de pendencias do novo Ratname e acrescenta as notificacoes transferidas.
        for lista_notificacoes in usuarios.values():  # Percorre lista_notificacoes in usuarios.values(), executando o bloco uma vez para cada elemento.
            if not isinstance(lista_notificacoes, list):  # Testa a condicao not isinstance(lista_notificacoes, list) e executa o bloco seguinte somente quando ela for verdadeira.
                raise ValueError("Uma lista de notificações está inválida.")  # Interrompe a operacao com ValueError("Uma lista de notificações está inválida."), indicando dados ou estado invalidos.
            for notificacao in lista_notificacoes:  # Percorre notificacao in lista_notificacoes, executando o bloco uma vez para cada elemento.
                if isinstance(notificacao, dict) and isinstance(  # Testa a condicao isinstance(notificacao, dict) and isinstance( e executa o bloco seguinte somente quando ela for verdadeira.
                    notificacao.get("mensagem"), str  # Executa nesta linha notificacao.get("mensagem"), str no contexto desta funcionalidade.
                ):  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                    notificacao["mensagem"] = notificacao["mensagem"].replace(  # Guarda em notificacao["mensagem"] o valor produzido por notificacao["mensagem"].replace(.
                        ratname_antigo, ratname_novo  # Executa nesta linha ratname_antigo, ratname_novo no contexto desta funcionalidade.
                    )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

    def _usuario_logado(self) -> dict | None:  # Declara o metodo _usuario_logado: localiza o registro da conta atualmente conectada.
        ratname = self.estado.usuario_logado  # guarda o nome publico usado como identificador da conta nos modulos da aplicacao
        if ratname is None:  # Verifica que nao existe usuario conectado; o bloco impede acesso aos dados pessoais.
            print("Você precisa fazer login para acessar esta opção.")  # Exibe no terminal Você precisa fazer login para acessar esta opção..
            return None  # Encerra o metodo e devolve ao chamador None.
        usuario = next(  # recupera o registro completo da conta atualmente conectada
            (item for item in self.estado.usuarios if item["ratname"] == ratname),  # Representa um bloco com a atividade descrita e a duracao em minutos indicada por item for item in self.estado.usuarios if item["ratname"] == ratname.
            None,  # Executa nesta linha None, no contexto desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        if usuario is None:  # Verifica que o registro da conta ativa nao foi encontrado.
            raise ValueError("O usuário conectado não existe na lista de contas.")  # Interrompe a operacao com ValueError("O usuário conectado não existe na lista de contas."), indicando dados ou estado invalidos.
        return usuario  # Encerra o metodo e devolve ao chamador usuario.

    def _confirmar_senha_atual(self, usuario: dict) -> bool:  # Declara o metodo _confirmar_senha_atual: verifica novamente a senha antes de alteracoes sensiveis.
        senha_atual = input("Confirme sua senha atual: ")  # Guarda em senha_atual o valor produzido por input("Confirme sua senha atual: ").
        return self.gerenciador_credenciais.verificar(  # Encerra o metodo e devolve ao chamador self.gerenciador_credenciais.verificar(.
            senha_atual, usuario["senha_salt"], usuario["senha_hash"]  # Executa nesta linha senha_atual, usuario["senha_salt"], usuario["senha_hash"] no contexto desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

    @staticmethod  # Aplica o decorador ao metodo seguinte.
    def _email_valido(email: str) -> bool:  # Declara o metodo _email_valido: aceita apenas o formato de e-mail institucional da UFRPE.
        return email.endswith("@ufrpe.br") and email.count("@") == 1 and len(email) > 9  # Encerra o metodo e devolve ao chamador email.endswith("@ufrpe.br") and email.count("@") == 1 and len(email) > 9.

    @staticmethod  # Aplica o decorador ao metodo seguinte.
    def _senha_valida(senha: str) -> bool:  # Declara o metodo _senha_valida: confirma todas as regras exigidas para a senha.
        return (  # Encerra o metodo e devolve ao chamador (.
            6 <= len(senha) <= 8  # Executa nesta linha 6 <= len(senha) <= 8 no contexto desta funcionalidade.
            and any(letra.isupper() for letra in senha)  # Executa nesta linha and any(letra.isupper() for letra in senha) no contexto desta funcionalidade.
            and any(letra.isdigit() for letra in senha)  # Executa nesta linha and any(letra.isdigit() for letra in senha) no contexto desta funcionalidade.
            and not senha.isalnum()  # Executa nesta linha and not senha.isalnum() no contexto desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

    def deslogar(self) -> None:  # Declara o metodo deslogar: encerra a sessao ativa.
        print(f"\nSaindo da conta de {self.estado.usuario_logado}...")  # Exibe no terminal Saindo da conta de {self.estado.usuario_logado}....
        self.estado.definir_usuario_logado(None)  # Atualiza o usuario conectado com o Ratname informado; None encerra a sessao.
        print("Você saiu da conta com sucesso!")  # Exibe no terminal Você saiu da conta com sucesso!.
