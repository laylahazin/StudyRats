import argparse

import lista
from TemaTerminal import mensagem, opcao, perguntar, titulo
from AreaMonitor import AreaMonitor
from Calendario import GerenciadorCalendario
from CadastroUsuario import CadastroUsuario
from Comunidades import GerenciadorComunidades
from Dados import persistencia
from Horario import GerenciadorHorario
from LoginUsuario import GerenciadorConta
from ModeloEstudo import GerenciadorModelosEstudo
from Ratcoins import gerenciador_ratcoins
from RegistroPresenca import RegistroPresenca
from RankingEstudantes import GerenciadorRankingEstudantes
from RankingMonitores import GerenciadorRankingMonitores
from Recompensas import Recompensas
from SalaEstudo import GerenciadorSalas

class AplicacaoStudyRats:
    def __init__(self) -> None:
        self.estado = lista.estado
        self.cadastro = CadastroUsuario()
        self.contas = GerenciadorConta()
        self.horario = GerenciadorHorario()
        self.registro_presenca = RegistroPresenca()
        self.salas = GerenciadorSalas(self.horario)
        self.comunidades = GerenciadorComunidades()
        self.calendario = GerenciadorCalendario(self.horario)
        self.area_monitor = AreaMonitor(self.salas)
        self.modelos_estudo = GerenciadorModelosEstudo(self.estado, persistencia)
        self.ranking_estudantes = GerenciadorRankingEstudantes(self.estado)
        self.ranking_monitores = GerenciadorRankingMonitores()
        self.recompensas = Recompensas(self.horario)

    def executar(self) -> None:
        persistencia.inicializar_arquivos()
        self.salas.limpar_sessoes_expiradas()
        while True:
            if self.estado.usuario_logado is not None:
                self.recompensas.verificar_notificacoes()
            self._exibir_menu()
            escolha = perguntar("\nSelecione uma opção: ").strip()
            if self.estado.usuario_logado is not None:
                if self._processar_menu_conectado(escolha):
                    return
            elif self._processar_menu_desconectado(escolha):
                return

    def _exibir_menu(self) -> None:
        print()
        titulo("STUDYRATS | Estude, conquiste, cresça")

        if self.estado.usuario_logado:
            mensagem(
                f"Conectado como {self.estado.usuario_logado} "
                f"| Tipo: {self.estado.tipo_usuario_logado}",
                "destaque",
            )
            opcao("1", "Perfil")
            opcao("2", "Modelo de estudo")
            opcao("3", "Sala com monitor")
            opcao("4", "Sessão de estudo")
            opcao("5", "Comunidades")
            opcao("6", "Sair da conta")
            usuario = self._usuario_atual()
            if usuario is not None and (
                self.contas.tem_acesso_debug(usuario, 1)
                or self.contas.tem_acesso_debug(usuario, 2)
            ):
                opcao("7", "Debug")
            opcao("0", "Encerrar aplicação")
        else:
            mensagem("Desconectado", "destaque")
            opcao("1", "Cadastrar novo usuário")
            opcao("2", "Fazer login")
            opcao("3", "Encerrar aplicação")
            mensagem(
                "Sessão de estudo e modelo de estudo ficam disponíveis após o login.",
                "suave",
            )

    def _processar_menu_conectado(self, opcao: str) -> bool:
        acoes = {
            "1": self._menu_perfil,
            "2": self._usar_modelo_estudo,
            "3": self.salas.exibir_sala_de_estudo,
            "4": self.registro_presenca.registrar,
            "5": self.comunidades.menu,
            "6": self.contas.deslogar,
        }
        if opcao == "7":
            self._menu_debug()
            return False
        if opcao == "0":
            mensagem("Encerrando os estudos, até logo!", "sucesso")
            return True

        acao = acoes.get(opcao)
        if acao is None:
            mensagem("Opção inválida, tente novamente.", "erro")
        else:
            acao()
        return False

    def _menu_perfil(self) -> None:
        while self.estado.usuario_logado is not None:
            ratname = self.estado.usuario_logado
            usuario = self._usuario_atual()
            if usuario is None:
                return
            modelos = persistencia.carregar("modelos_estudo.json", {})
            if not isinstance(modelos, dict):
                raise ValueError("ERRO: O arquivo de modelos de estudo deve conter um objeto JSON.")
            modelo = modelos.get(ratname)

            titulo(f"PERFIL: {ratname}")
            mensagem(f"Tipo de conta: {self.estado.tipo_usuario_logado}", "destaque")
            if isinstance(modelo, dict):
                mensagem(f"Modelo de estudo em uso: {modelo.get('nome', 'Sem nome')}")
            else:
                mensagem("Modelo de estudo em uso: nenhum selecionado", "suave")
            mensagem(
                "Acesso DEBUG 1: "
                f"{'liberado' if self.contas.tem_acesso_debug(usuario, 1) else 'bloqueado'}",
                "sucesso" if self.contas.tem_acesso_debug(usuario, 1) else "suave",
            )
            mensagem(
                "Acesso DEBUG 2: "
                f"{'liberado' if self.contas.tem_acesso_debug(usuario, 2) else 'bloqueado'}",
                "sucesso" if self.contas.tem_acesso_debug(usuario, 2) else "suave",
            )
            opcao("1.1", "RatCoins e recompensas")
            opcao("1.2", "Ranking de estudantes/monitores")
            opcao("1.3", "Calendário de estudo")
            opcao("1.4", "DEBUG CODE")
            opcao("1.5", "Excluir conta")
            opcao("1.6", "Editar conta")
            if self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR:
                opcao("1.7", "Área do monitor")
            opcao("0", "Voltar ao menu principal")
            escolha = perguntar("Escolha uma opção: ").strip()
            if escolha in ("0", "1.5"):
                if escolha == "1.5":
                    confirmacao = input(
                        "Digite EXCLUIR para confirmar a remoção da sua conta: "
                    ).strip()
                    if confirmacao == "EXCLUIR":
                        self.contas.excluir_conta()
                    else:
                        mensagem("Exclusão cancelada. Sua conta foi mantida.", "aviso")
                return
            if escolha == "1.1":
                self.recompensas.menu()
            elif escolha == "1.2":
                self.ranking_estudantes.exibir_ranking()
                self.ranking_monitores.exibir()
            elif escolha == "1.3":
                self.calendario.menu()
            elif escolha == "1.4":
                self.contas.menu_debug_codes()
            elif escolha == "1.6":
                self.contas.editar_conta()
            elif (
                escolha == "1.7"
                and self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR
            ):
                self.area_monitor.menu()
            else:
                mensagem("Opção inválida. Tente novamente.", "erro")

    def _menu_debug(self) -> None:
        usuario = self._usuario_atual()
        if usuario is None:
            return
        acesso_horario = self.contas.tem_acesso_debug(usuario, 1)
        acesso_ratcoins = self.contas.tem_acesso_debug(usuario, 2)
        if not acesso_horario and not acesso_ratcoins:
            print("Você precisa liberar um acesso DEBUG no seu perfil.")
            return
        while True:
            titulo("DEBUG")
            if acesso_horario:
                opcao("1", "Alterar data e horário do sistema")
            if acesso_ratcoins:
                opcao("2", "Alterar saldo total de RatCoins")
            opcao("0", "Voltar ao menu principal")
            escolha = perguntar("Escolha uma opção: ").strip()
            if escolha == "0":
                return
            if escolha == "1" and acesso_horario:
                self.horario.configurar()
            elif escolha == "2" and acesso_ratcoins:
                self._alterar_saldo_ratcoins()
            else:
                mensagem("Opção inválida ou acesso DEBUG não liberado.", "erro")

    def _alterar_saldo_ratcoins(self) -> None:
        ratname = self.estado.usuario_logado
        if ratname is None:
            return
        usuario = self._usuario_atual()
        if usuario is None or not self.contas.tem_acesso_debug(usuario, 2):
            print("A alteração de RatCoins exige acesso ao DEBUG 2.")
            return
        mensagem(f"Saldo atual: {gerenciador_ratcoins.saldo(ratname)} RC", "destaque")
        try:
            novo_saldo = int(perguntar("Novo saldo total (RC): ").strip())
        except ValueError:
            mensagem("Informe um número inteiro não negativo.", "erro")
            return
        if novo_saldo < 0:
            mensagem("O saldo não pode ser negativo.", "erro")
            return
        if perguntar(f"Confirmar saldo total de {novo_saldo} RC? (s/n): ").strip().lower() != "s":
            mensagem("Alteração cancelada.", "aviso")
            return
        gerenciador_ratcoins.ajustar_saldo(ratname, novo_saldo)

    def _usuario_atual(self) -> dict | None:
        ratname = self.estado.usuario_logado
        if ratname is None:
            return None
        return next(
            (usuario for usuario in self.estado.usuarios if usuario["ratname"] == ratname),
            None,
        )

    def _usar_modelo_estudo(self) -> None:
        ratname = self.estado.usuario_logado
        if ratname is None:
            self.modelos_estudo.executar()
            return

        modelos = persistencia.carregar("modelos_estudo.json", {})
        if not isinstance(modelos, dict):
            raise ValueError("O arquivo de modelos de estudo deve conter um objeto JSON.")
        primeiro_modelo = ratname not in modelos
        self.modelos_estudo.executar()
        modelos_atualizados = persistencia.carregar("modelos_estudo.json", {})
        if not isinstance(modelos_atualizados, dict):
            raise ValueError("O arquivo de modelos de estudo deve conter um objeto JSON.")
        if (
            primeiro_modelo
            and ratname in modelos_atualizados
            and self.estado.tipo_usuario_logado == self.estado.TIPO_ESTUDANTE
        ):
            gerenciador_ratcoins.registrar_ganho(
                ratname,
                "Criar e usar o primeiro modelo de estudo",
                15,
                evento_id=f"modelo-primeiro-uso:{ratname}",
            )

    def _processar_menu_desconectado(self, opcao: str) -> bool:
        acoes = {
            "1": self.cadastro.cadastrar,
            "2": self.contas.realizar_login,
        }
        if opcao == "3":
            mensagem("Encerrando os estudos, até logo!", "sucesso")
            return True

        acao = acoes.get(opcao)
        if acao is None:
            mensagem("Opção inválida, tente novamente.", "erro")
        else:
            acao()
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="StudyRats")
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Executar a interface colorida no terminal",
    )
    argumentos = parser.parse_args()
    aplicacao = AplicacaoStudyRats()
    if argumentos.cli:
        aplicacao.executar()
    else:
        from gui_app import iniciar_interface

        iniciar_interface(aplicacao)
