import argparse  # Importa argparse: interpreta os argumentos da linha de comando, incluindo --cli.

import lista  # Importa lista: importa o estado central da aplicacao.
from TemaTerminal import mensagem, opcao, perguntar, titulo  # Importa de TemaTerminal os recursos mensagem, opcao, perguntar, titulo usados neste modulo.
from AreaMonitor import AreaMonitor  # Importa de AreaMonitor os recursos AreaMonitor usados neste modulo.
from Calendario import GerenciadorCalendario  # Importa de Calendario os recursos GerenciadorCalendario usados neste modulo.
from CadastroUsuario import CadastroUsuario  # Importa de CadastroUsuario os recursos CadastroUsuario usados neste modulo.
from Comunidades import GerenciadorComunidades  # Importa de Comunidades os recursos GerenciadorComunidades usados neste modulo.
from Dados import persistencia  # Importa de Dados persistencia, reutilizando os recursos centrais de persistencia e credenciais.
from Horario import GerenciadorHorario  # Importa de Horario os recursos GerenciadorHorario usados neste modulo.
from LoginUsuario import GerenciadorConta  # Importa de LoginUsuario os recursos GerenciadorConta usados neste modulo.
from ModeloEstudo import GerenciadorModelosEstudo  # Importa de ModeloEstudo os recursos GerenciadorModelosEstudo usados neste modulo.
from Ratcoins import gerenciador_ratcoins  # Importa de Ratcoins gerenciador_ratcoins, evitando criar outro gerenciador de recompensas.
from RegistroPresenca import RegistroPresenca  # Importa de RegistroPresenca os recursos RegistroPresenca usados neste modulo.
from RankingEstudantes import GerenciadorRankingEstudantes  # Importa de RankingEstudantes os recursos GerenciadorRankingEstudantes usados neste modulo.
from RankingMonitores import GerenciadorRankingMonitores  # Importa de RankingMonitores os recursos GerenciadorRankingMonitores usados neste modulo.
from Recompensas import Recompensas  # Importa de Recompensas os recursos Recompensas usados neste modulo.
from SalaEstudo import GerenciadorSalas  # Importa de SalaEstudo os recursos GerenciadorSalas usados neste modulo.

class AplicacaoStudyRats:  # Declara a classe AplicacaoStudyRats: coordena os menus e os modulos da aplicacao.
    def __init__(self) -> None:  # Declara o metodo __init__: implementa esta funcionalidade da classe.
        self.estado = lista.estado  # Guarda em self.estado o valor produzido por lista.estado.
        self.cadastro = CadastroUsuario()  # Guarda em self.cadastro o valor produzido por CadastroUsuario().
        self.contas = GerenciadorConta()  # Guarda em self.contas o valor produzido por GerenciadorConta().
        self.horario = GerenciadorHorario()  # converte a entrada em objeto time
        self.registro_presenca = RegistroPresenca()  # Guarda em self.registro_presenca o valor produzido por RegistroPresenca().
        self.salas = GerenciadorSalas(self.horario)  # Guarda em self.salas o valor produzido por GerenciadorSalas(self.horario).
        self.comunidades = GerenciadorComunidades()  # Guarda em self.comunidades o valor produzido por GerenciadorComunidades().
        self.calendario = GerenciadorCalendario(self.horario)  # Guarda em self.calendario o valor produzido por GerenciadorCalendario(self.horario).
        self.area_monitor = AreaMonitor(self.salas)  # Guarda em self.area_monitor o valor produzido por AreaMonitor(self.salas).
        self.modelos_estudo = GerenciadorModelosEstudo(self.estado, persistencia)  # Guarda em self.modelos_estudo o valor produzido por GerenciadorModelosEstudo(self.estado, persistencia).
        self.ranking_estudantes = GerenciadorRankingEstudantes(self.estado)  # Guarda em self.ranking_estudantes o valor produzido por GerenciadorRankingEstudantes(self.estado).
        self.ranking_monitores = GerenciadorRankingMonitores()  # Guarda em self.ranking_monitores o valor produzido por GerenciadorRankingMonitores().
        self.recompensas = Recompensas(self.horario)  # Guarda em self.recompensas o valor produzido por Recompensas(self.horario).

    def executar(self) -> None:  # Declara o metodo executar: mantem o ciclo principal ou o menu de modelos ativo ate haver encerramento.
        persistencia.inicializar_arquivos()  # Executa nesta linha persistencia.inicializar_arquivos() no contexto desta funcionalidade.
        self.salas.limpar_sessoes_expiradas()  # Executa self.salas.limpar_sessoes_expiradas(); o efeito desta chamada participa diretamente desta funcionalidade.
        while True:  # Mantem o loop ativo ate encontrar uma opcao que devolva ou encerre o fluxo.
            if self.estado.usuario_logado is not None:  # Testa a condicao self.estado.usuario_logado is not None e executa o bloco seguinte somente quando ela for verdadeira.
                self.recompensas.verificar_notificacoes()  # Executa self.recompensas.verificar_notificacoes(); o efeito desta chamada participa diretamente desta funcionalidade.
            self._exibir_menu()  # Executa self._exibir_menu(); o efeito desta chamada participa diretamente desta funcionalidade.
            escolha = perguntar("\nSelecione uma opção: ").strip()  # guarda a opcao digitada no menu atual
            if self.estado.usuario_logado is not None:  # Testa a condicao self.estado.usuario_logado is not None e executa o bloco seguinte somente quando ela for verdadeira.
                if self._processar_menu_conectado(escolha):  # Testa a condicao self._processar_menu_conectado(escolha) e executa o bloco seguinte somente quando ela for verdadeira.
                    return  # Encerra este metodo imediatamente sem devolver valor.
            elif self._processar_menu_desconectado(escolha):  # Testa a alternativa self._processar_menu_desconectado(escolha) somente depois que as condicoes anteriores falharam.
                return  # Encerra este metodo imediatamente sem devolver valor.

    def _exibir_menu(self) -> None:  # Declara o metodo _exibir_menu: implementa esta funcionalidade da classe.
        print()  # Escreve no terminal o conteudo preparado por esta chamada.
        titulo("STUDYRATS | Estude, conquiste, cresça")  # Exibe o titulo usando a largura e as cores configuradas para o terminal.

        if self.estado.usuario_logado:  # Testa a condicao self.estado.usuario_logado e executa o bloco seguinte somente quando ela for verdadeira.
            mensagem(  # Exibe no terminal a mensagem usando o tipo de estilo informado pelo segundo argumento.
                f"Conectado como {self.estado.usuario_logado} "  # Executa nesta linha f"Conectado como {self.estado.usuario_logado} " no contexto desta funcionalidade.
                f"| Tipo: {self.estado.tipo_usuario_logado}",  # Executa nesta linha f"| Tipo: {self.estado.tipo_usuario_logado}", no contexto desta funcionalidade.
                "destaque",  # Executa nesta linha "destaque", no contexto desta funcionalidade.
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            opcao("1", "Perfil")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("2", "Modelo de estudo")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("3", "Sala com monitor")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("4", "Sessão de estudo")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("5", "Comunidades")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("6", "Sair da conta")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            usuario = self._usuario_atual()  # recupera o registro completo da conta atualmente conectada
            if usuario is not None and (  # Testa a condicao usuario is not None and ( e executa o bloco seguinte somente quando ela for verdadeira.
                self.contas.tem_acesso_debug(usuario, 1)  # Executa self.contas.tem_acesso_debug(usuario, 1); o efeito desta chamada participa diretamente desta funcionalidade.
                or self.contas.tem_acesso_debug(usuario, 2)  # Executa nesta linha or self.contas.tem_acesso_debug(usuario, 2) no contexto desta funcionalidade.
            ):  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                opcao("7", "Debug")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("0", "Encerrar aplicação")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
        else:  # Executa este bloco quando nenhuma condicao anterior da cadeia foi atendida.
            mensagem("Desconectado", "destaque")  # Exibe no terminal Desconectado usando o tipo de estilo informado pelo segundo argumento.
            opcao("1", "Cadastrar novo usuário")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("2", "Fazer login")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("3", "Encerrar aplicação")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            mensagem(  # Exibe no terminal a mensagem usando o tipo de estilo informado pelo segundo argumento.
                "Sessão de estudo e modelo de estudo ficam disponíveis após o login.",  # Executa nesta linha "Sessão de estudo e modelo de estudo ficam disponíveis após o login.", no contexto desta funcionalidade.
                "suave",  # Executa nesta linha "suave", no contexto desta funcionalidade.
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

    def _processar_menu_conectado(self, opcao: str) -> bool:  # Declara o metodo _processar_menu_conectado: implementa esta funcionalidade da classe.
        acoes = {  # Guarda em acoes o valor produzido por {.
            "1": self._menu_perfil,  # Abre o menu Perfil da conta atualmente conectada.
            "2": self._usar_modelo_estudo,  # Abre a escolha e o uso de modelos de estudo.
            "3": self.salas.exibir_sala_de_estudo,  # Abre o menu de salas de estudo com monitor.
            "4": self.registro_presenca.registrar,  # Abre o registro de presenca em uma sessao ativa.
            "5": self.comunidades.menu,  # Abre o menu de comunidades.
            "6": self.contas.deslogar,  # Encerra a sessao da conta atualmente conectada.
        }  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        if opcao == "7":  # Testa a condicao opcao == "7" e executa o bloco seguinte somente quando ela for verdadeira.
            self._menu_debug()  # Executa self._menu_debug(); o efeito desta chamada participa diretamente desta funcionalidade.
            return False  # Encerra o metodo e devolve ao chamador False.
        if opcao == "0":  # Verifica se a opcao 0 foi escolhida para sair do menu atual.
            mensagem("Encerrando os estudos, até logo!", "sucesso")  # Exibe no terminal Encerrando os estudos, até logo! usando o tipo de estilo informado pelo segundo argumento.
            return True  # Encerra o metodo e devolve ao chamador True.

        acao = acoes.get(opcao)  # Guarda em acao o valor produzido por acoes.get(opcao).
        if acao is None:  # Testa a condicao acao is None e executa o bloco seguinte somente quando ela for verdadeira.
            mensagem("Opção inválida, tente novamente.", "erro")  # Exibe no terminal Opção inválida, tente novamente. usando o tipo de estilo informado pelo segundo argumento.
        else:  # Executa este bloco quando nenhuma condicao anterior da cadeia foi atendida.
            acao()  # Executa nesta linha acao() no contexto desta funcionalidade.
        return False  # Encerra o metodo e devolve ao chamador False.

    def _menu_perfil(self) -> None:  # Declara o metodo _menu_perfil: exibe dados da conta e abre recursos escolhidos no perfil.
        while self.estado.usuario_logado is not None:  # Repete o bloco enquanto self.estado.usuario_logado is not None continuar verdadeiro.
            ratname = self.estado.usuario_logado  # guarda o nome publico usado como identificador da conta nos modulos da aplicacao
            usuario = self._usuario_atual()  # recupera o registro completo da conta atualmente conectada
            if usuario is None:  # Verifica que o registro da conta ativa nao foi encontrado.
                return  # Encerra este metodo imediatamente sem devolver valor.
            modelos = persistencia.carregar("modelos_estudo.json", {})  # recupera os modelos persistidos associados aos Ratnames
            if not isinstance(modelos, dict):  # Testa a condicao not isinstance(modelos, dict) e executa o bloco seguinte somente quando ela for verdadeira.
                raise ValueError("ERRO: O arquivo de modelos de estudo deve conter um objeto JSON.")  # Interrompe a operacao com ValueError("ERRO: O arquivo de modelos de estudo deve conter um objeto JSON."), indicando dados ou estado invalidos.
            modelo = modelos.get(ratname)  # seleciona o modelo que sera exibido ou salvo

            titulo(f"PERFIL: {ratname}")  # Exibe o titulo usando a largura e as cores configuradas para o terminal.
            mensagem(f"Tipo de conta: {self.estado.tipo_usuario_logado}", "destaque")  # Exibe no terminal Tipo de conta: {self.estado.tipo_usuario_logado} usando o tipo de estilo informado pelo segundo argumento.
            if isinstance(modelo, dict):  # Testa a condicao isinstance(modelo, dict) e executa o bloco seguinte somente quando ela for verdadeira.
                mensagem(f"Modelo de estudo em uso: {modelo.get('nome', 'Sem nome')}")  # Exibe no terminal Modelo de estudo em uso: {modelo.get( usando o tipo de estilo informado pelo segundo argumento.
            else:  # Executa este bloco quando nenhuma condicao anterior da cadeia foi atendida.
                mensagem("Modelo de estudo em uso: nenhum selecionado", "suave")  # Exibe no terminal Modelo de estudo em uso: nenhum selecionado usando o tipo de estilo informado pelo segundo argumento.
            mensagem(  # Exibe no terminal a mensagem usando o tipo de estilo informado pelo segundo argumento.
                "Acesso DEBUG 1: "  # Executa nesta linha "Acesso DEBUG 1: " no contexto desta funcionalidade.
                f"{'liberado' if self.contas.tem_acesso_debug(usuario, 1) else 'bloqueado'}",  # Executa nesta linha f"{'liberado' if self.contas.tem_acesso_debug(usuario, 1) else 'bloqueado'}", no contexto desta funcionalidade.
                "sucesso" if self.contas.tem_acesso_debug(usuario, 1) else "suave",  # Executa nesta linha "sucesso" if self.contas.tem_acesso_debug(usuario, 1) else "suave", no contexto desta funcionalidade.
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            mensagem(  # Exibe no terminal a mensagem usando o tipo de estilo informado pelo segundo argumento.
                "Acesso DEBUG 2: "  # Executa nesta linha "Acesso DEBUG 2: " no contexto desta funcionalidade.
                f"{'liberado' if self.contas.tem_acesso_debug(usuario, 2) else 'bloqueado'}",  # Executa nesta linha f"{'liberado' if self.contas.tem_acesso_debug(usuario, 2) else 'bloqueado'}", no contexto desta funcionalidade.
                "sucesso" if self.contas.tem_acesso_debug(usuario, 2) else "suave",  # Executa nesta linha "sucesso" if self.contas.tem_acesso_debug(usuario, 2) else "suave", no contexto desta funcionalidade.
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            opcao("1.1", "RatCoins e recompensas")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("1.2", "Ranking de estudantes/monitores")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("1.3", "Calendário de estudo")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("1.4", "DEBUG CODE")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("1.5", "Excluir conta")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("1.6", "Editar conta")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            if self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR:  # Testa a condicao self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR e executa o bloco seguinte somente quando ela for verdadeira.
                opcao("1.7", "Área do monitor")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("0", "Voltar ao menu principal")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            escolha = perguntar("Escolha uma opção: ").strip()  # guarda a opcao digitada no menu atual
            if escolha in ("0", "1.5"):  # Testa a condicao escolha in ("0", "1.5") e executa o bloco seguinte somente quando ela for verdadeira.
                if escolha == "1.5":  # Testa a condicao escolha == "1.5" e executa o bloco seguinte somente quando ela for verdadeira.
                    confirmacao = input(  # Guarda em confirmacao o valor produzido por input(.
                        "Digite EXCLUIR para confirmar a remoção da sua conta: "  # Executa nesta linha "Digite EXCLUIR para confirmar a remoção da sua conta: " no contexto desta funcionalidade.
                    ).strip()  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                    if confirmacao == "EXCLUIR":  # Testa a condicao confirmacao == "EXCLUIR" e executa o bloco seguinte somente quando ela for verdadeira.
                        self.contas.excluir_conta()  # Executa self.contas.excluir_conta(); o efeito desta chamada participa diretamente desta funcionalidade.
                    else:  # Executa este bloco quando nenhuma condicao anterior da cadeia foi atendida.
                        mensagem("Exclusão cancelada. Sua conta foi mantida.", "aviso")  # Exibe no terminal Exclusão cancelada. Sua conta foi mantida. usando o tipo de estilo informado pelo segundo argumento.
                return  # Encerra este metodo imediatamente sem devolver valor.
            if escolha == "1.1":  # Testa a condicao escolha == "1.1" e executa o bloco seguinte somente quando ela for verdadeira.
                self.recompensas.menu()  # Executa self.recompensas.menu(); o efeito desta chamada participa diretamente desta funcionalidade.
            elif escolha == "1.2":  # Testa a alternativa escolha == "1.2" somente depois que as condicoes anteriores falharam.
                self.ranking_estudantes.exibir_ranking()  # Executa self.ranking_estudantes.exibir_ranking(); o efeito desta chamada participa diretamente desta funcionalidade.
                self.ranking_monitores.exibir()  # Executa self.ranking_monitores.exibir(); o efeito desta chamada participa diretamente desta funcionalidade.
            elif escolha == "1.3":  # Testa a alternativa escolha == "1.3" somente depois que as condicoes anteriores falharam.
                self.calendario.menu()  # Executa self.calendario.menu(); o efeito desta chamada participa diretamente desta funcionalidade.
            elif escolha == "1.4":  # Testa a alternativa escolha == "1.4" somente depois que as condicoes anteriores falharam.
                self.contas.menu_debug_codes()  # Executa self.contas.menu_debug_codes(); o efeito desta chamada participa diretamente desta funcionalidade.
            elif escolha == "1.6":  # Testa a alternativa escolha == "1.6" somente depois que as condicoes anteriores falharam.
                self.contas.editar_conta()  # Executa self.contas.editar_conta(); o efeito desta chamada participa diretamente desta funcionalidade.
            elif (  # Testa a alternativa ( somente depois que as condicoes anteriores falharam.
                escolha == "1.7"  # Executa nesta linha escolha == "1.7" no contexto desta funcionalidade.
                and self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR  # Executa nesta linha and self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR no contexto desta funcionalidade.
            ):  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                self.area_monitor.menu()  # Executa self.area_monitor.menu(); o efeito desta chamada participa diretamente desta funcionalidade.
            else:  # Executa este bloco quando nenhuma condicao anterior da cadeia foi atendida.
                mensagem("Opção inválida. Tente novamente.", "erro")  # Exibe no terminal Opção inválida. Tente novamente. usando o tipo de estilo informado pelo segundo argumento.

    def _menu_debug(self) -> None:  # Declara o metodo _menu_debug: exibe somente ferramentas DEBUG autorizadas pela conta.
        usuario = self._usuario_atual()  # recupera o registro completo da conta atualmente conectada
        if usuario is None:  # Verifica que o registro da conta ativa nao foi encontrado.
            return  # Encerra este metodo imediatamente sem devolver valor.
        acesso_horario = self.contas.tem_acesso_debug(usuario, 1)  # registra a permissao DEBUG 1 para ajustar data e horario
        acesso_ratcoins = self.contas.tem_acesso_debug(usuario, 2)  # registra a permissao DEBUG 2 para ajustar RatCoins
        if not acesso_horario and not acesso_ratcoins:  # Testa a condicao not acesso_horario and not acesso_ratcoins e executa o bloco seguinte somente quando ela for verdadeira.
            print("Você precisa liberar um acesso DEBUG no seu perfil.")  # Exibe no terminal Você precisa liberar um acesso DEBUG no seu perfil..
            return  # Encerra este metodo imediatamente sem devolver valor.
        while True:  # Mantem o loop ativo ate encontrar uma opcao que devolva ou encerre o fluxo.
            titulo("DEBUG")  # Exibe o titulo usando a largura e as cores configuradas para o terminal.
            if acesso_horario:  # Testa a condicao acesso_horario e executa o bloco seguinte somente quando ela for verdadeira.
                opcao("1", "Alterar data e horário do sistema")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            if acesso_ratcoins:  # Testa a condicao acesso_ratcoins e executa o bloco seguinte somente quando ela for verdadeira.
                opcao("2", "Alterar saldo total de RatCoins")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            opcao("0", "Voltar ao menu principal")  # Adiciona ao menu a opcao formada pelo numero e pela descricao informados.
            escolha = perguntar("Escolha uma opção: ").strip()  # guarda a opcao digitada no menu atual
            if escolha == "0":  # Verifica se o usuario escolheu 0 para voltar ou encerrar.
                return  # Encerra este metodo imediatamente sem devolver valor.
            if escolha == "1" and acesso_horario:  # Testa a condicao escolha == "1" and acesso_horario e executa o bloco seguinte somente quando ela for verdadeira.
                self.horario.configurar()  # Executa self.horario.configurar(); o efeito desta chamada participa diretamente desta funcionalidade.
            elif escolha == "2" and acesso_ratcoins:  # Testa a alternativa escolha == "2" and acesso_ratcoins somente depois que as condicoes anteriores falharam.
                self._alterar_saldo_ratcoins()  # Executa self._alterar_saldo_ratcoins(); o efeito desta chamada participa diretamente desta funcionalidade.
            else:  # Executa este bloco quando nenhuma condicao anterior da cadeia foi atendida.
                mensagem("Opção inválida ou acesso DEBUG não liberado.", "erro")  # Exibe no terminal Opção inválida ou acesso DEBUG não liberado. usando o tipo de estilo informado pelo segundo argumento.

    def _alterar_saldo_ratcoins(self) -> None:  # Declara o metodo _alterar_saldo_ratcoins: valida, confirma e persiste um novo saldo RatCoins.
        ratname = self.estado.usuario_logado  # guarda o nome publico usado como identificador da conta nos modulos da aplicacao
        if ratname is None:  # Verifica que nao existe usuario conectado; o bloco impede acesso aos dados pessoais.
            return  # Encerra este metodo imediatamente sem devolver valor.
        usuario = self._usuario_atual()  # recupera o registro completo da conta atualmente conectada
        if usuario is None or not self.contas.tem_acesso_debug(usuario, 2):  # Testa a condicao usuario is None or not self.contas.tem_acesso_debug(usuario, 2) e executa o bloco seguinte somente quando ela for verdadeira.
            print("A alteração de RatCoins exige acesso ao DEBUG 2.")  # Exibe no terminal A alteração de RatCoins exige acesso ao DEBUG 2..
            return  # Encerra este metodo imediatamente sem devolver valor.
        mensagem(f"Saldo atual: {gerenciador_ratcoins.saldo(ratname)} RC", "destaque")  # Exibe no terminal Saldo atual: {gerenciador_ratcoins.saldo(ratname)} RC usando o tipo de estilo informado pelo segundo argumento.
        try:  # Protege o bloco seguinte contra dados que podem causar excecao.
            novo_saldo = int(perguntar("Novo saldo total (RC): ").strip())  # guarda o novo saldo inteiro informado pelo administrador
        except ValueError:  # Trata ValueError emitida pelo bloco try, indicando que a entrada ou dado protegido era invalido.
            mensagem("Informe um número inteiro não negativo.", "erro")  # Exibe no terminal Informe um número inteiro não negativo. usando o tipo de estilo informado pelo segundo argumento.
            return  # Encerra este metodo imediatamente sem devolver valor.
        if novo_saldo < 0:  # Verifica se o saldo informado seria negativo.
            mensagem("O saldo não pode ser negativo.", "erro")  # Exibe no terminal O saldo não pode ser negativo. usando o tipo de estilo informado pelo segundo argumento.
            return  # Encerra este metodo imediatamente sem devolver valor.
        if perguntar(f"Confirmar saldo total de {novo_saldo} RC? (s/n): ").strip().lower() != "s":  # Cancela o ajuste se o administrador nao confirmar explicitamente com s.
            mensagem("Alteração cancelada.", "aviso")  # Exibe no terminal Alteração cancelada. usando o tipo de estilo informado pelo segundo argumento.
            return  # Encerra este metodo imediatamente sem devolver valor.
        gerenciador_ratcoins.ajustar_saldo(ratname, novo_saldo)  # Substitui o saldo RatCoins do Ratname pelo inteiro confirmado pelo administrador.

    def _usuario_atual(self) -> dict | None:  # Declara o metodo _usuario_atual: retorna o registro da conta atualmente conectada.
        ratname = self.estado.usuario_logado  # guarda o nome publico usado como identificador da conta nos modulos da aplicacao
        if ratname is None:  # Verifica que nao existe usuario conectado; o bloco impede acesso aos dados pessoais.
            return None  # Encerra o metodo e devolve ao chamador None.
        return next(  # Encerra o metodo e devolve ao chamador next(.
            (usuario for usuario in self.estado.usuarios if usuario["ratname"] == ratname),  # Representa um bloco com a atividade descrita e a duracao em minutos indicada por usuario for usuario in self.estado.usuarios if usuario["ratname"] == ratname.
            None,  # Executa nesta linha None, no contexto desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

    def _usar_modelo_estudo(self) -> None:  # Declara o metodo _usar_modelo_estudo: implementa esta funcionalidade da classe.
        ratname = self.estado.usuario_logado  # guarda o nome publico usado como identificador da conta nos modulos da aplicacao
        if ratname is None:  # Verifica que nao existe usuario conectado; o bloco impede acesso aos dados pessoais.
            self.modelos_estudo.executar()  # Executa self.modelos_estudo.executar(); o efeito desta chamada participa diretamente desta funcionalidade.
            return  # Encerra este metodo imediatamente sem devolver valor.

        modelos = persistencia.carregar("modelos_estudo.json", {})  # recupera os modelos persistidos associados aos Ratnames
        if not isinstance(modelos, dict):  # Testa a condicao not isinstance(modelos, dict) e executa o bloco seguinte somente quando ela for verdadeira.
            raise ValueError("O arquivo de modelos de estudo deve conter um objeto JSON.")  # Interrompe a operacao com ValueError("O arquivo de modelos de estudo deve conter um objeto JSON."), indicando dados ou estado invalidos.
        primeiro_modelo = ratname not in modelos  # Guarda em primeiro_modelo o valor produzido por ratname not in modelos.
        self.modelos_estudo.executar()  # Executa self.modelos_estudo.executar(); o efeito desta chamada participa diretamente desta funcionalidade.
        modelos_atualizados = persistencia.carregar("modelos_estudo.json", {})  # Guarda em modelos_atualizados o valor produzido por persistencia.carregar("modelos_estudo.json", {}).
        if not isinstance(modelos_atualizados, dict):  # Testa a condicao not isinstance(modelos_atualizados, dict) e executa o bloco seguinte somente quando ela for verdadeira.
            raise ValueError("O arquivo de modelos de estudo deve conter um objeto JSON.")  # Interrompe a operacao com ValueError("O arquivo de modelos de estudo deve conter um objeto JSON."), indicando dados ou estado invalidos.
        if (  # Testa a condicao ( e executa o bloco seguinte somente quando ela for verdadeira.
            primeiro_modelo  # Executa nesta linha primeiro_modelo no contexto desta funcionalidade.
            and ratname in modelos_atualizados  # Executa nesta linha and ratname in modelos_atualizados no contexto desta funcionalidade.
            and self.estado.tipo_usuario_logado == self.estado.TIPO_ESTUDANTE  # Executa nesta linha and self.estado.tipo_usuario_logado == self.estado.TIPO_ESTUDANTE no contexto desta funcionalidade.
        ):  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            gerenciador_ratcoins.registrar_ganho(  # Registra a recompensa unica de 15 RC pelo primeiro uso de modelo.
                ratname,  # Executa nesta linha ratname, no contexto desta funcionalidade.
                "Criar e usar o primeiro modelo de estudo",  # Executa nesta linha "Criar e usar o primeiro modelo de estudo", no contexto desta funcionalidade.
                15,  # Executa nesta linha 15, no contexto desta funcionalidade.
                evento_id=f"modelo-primeiro-uso:{ratname}",  # Guarda em evento_id o valor produzido por f"modelo-primeiro-uso:{ratname}".
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

    def _processar_menu_desconectado(self, opcao: str) -> bool:  # Declara o metodo _processar_menu_desconectado: implementa esta funcionalidade da classe.
        acoes = {  # Guarda em acoes o valor produzido por {.
            "1": self.cadastro.cadastrar,  # Executa o cadastro de um novo usuario.
            "2": self.contas.realizar_login,  # Executa o login com e-mail e senha.
        }  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        if opcao == "3":  # Testa a condicao opcao == "3" e executa o bloco seguinte somente quando ela for verdadeira.
            mensagem("Encerrando os estudos, até logo!", "sucesso")  # Exibe no terminal Encerrando os estudos, até logo! usando o tipo de estilo informado pelo segundo argumento.
            return True  # Encerra o metodo e devolve ao chamador True.

        acao = acoes.get(opcao)  # Guarda em acao o valor produzido por acoes.get(opcao).
        if acao is None:  # Testa a condicao acao is None e executa o bloco seguinte somente quando ela for verdadeira.
            mensagem("Opção inválida, tente novamente.", "erro")  # Exibe no terminal Opção inválida, tente novamente. usando o tipo de estilo informado pelo segundo argumento.
        else:  # Executa este bloco quando nenhuma condicao anterior da cadeia foi atendida.
            acao()  # Executa nesta linha acao() no contexto desta funcionalidade.
        return False  # Encerra o metodo e devolve ao chamador False.


if __name__ == "__main__":  # Executa este bloco somente quando o arquivo for iniciado diretamente pelo Python.
    parser = argparse.ArgumentParser(description="StudyRats")  # Guarda em parser o valor produzido por argparse.ArgumentParser(description="StudyRats").
    parser.add_argument(  # Executa nesta linha parser.add_argument( no contexto desta funcionalidade.
        "--cli",  # Executa nesta linha "--cli", no contexto desta funcionalidade.
        action="store_true",  # Guarda em action o valor produzido por "store_true".
        help="Executar a interface colorida no terminal",  # Guarda em help o valor produzido por "Executar a interface colorida no terminal".
    )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
    argumentos = parser.parse_args()  # armazena os parametros reconhecidos pela linha de comando
    aplicacao = AplicacaoStudyRats()  # mantem a instancia central que coordena os modulos da aplicacao
    if argumentos.cli:  # Testa a condicao argumentos.cli e executa o bloco seguinte somente quando ela for verdadeira.
        aplicacao.executar()  # Executa nesta linha aplicacao.executar() no contexto desta funcionalidade.
    else:  # Executa este bloco quando nenhuma condicao anterior da cadeia foi atendida.
        from gui_app import iniciar_interface  # Importa a interface grafica usada no modo padrao, quando --cli nao foi informado.

        iniciar_interface(aplicacao)  # Executa nesta linha iniciar_interface(aplicacao) no contexto desta funcionalidade.
