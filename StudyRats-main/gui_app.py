import builtins
import queue
import sys
import threading
import tkinter as tk
from tkinter import ttk

import lista
from AssistenteRatinho import responder
from Dados import persistencia


class _SaidaJanela:
    encoding = "utf-8"

    def __init__(self, eventos: queue.Queue[tuple[str, str]]) -> None:
        self.eventos = eventos

    def write(self, texto: str) -> int:
        if texto:
            self.eventos.put(("saida", texto.replace("\r", "\n")))
        return len(texto)

    def flush(self) -> None:
        pass

    def isatty(self) -> bool:
        return False


class StudyRatsGUI:
    def __init__(self, aplicacao) -> None:
        self.aplicacao = aplicacao
        self.root = tk.Tk()
        self.root.title("StudyRats")
        self.root.geometry("940x680")
        self.root.minsize(760, 560)
        self.root.protocol("WM_DELETE_WINDOW", self._fechar)

        self._eventos: queue.Queue[tuple[str, str]] = queue.Queue()
        self._entradas: queue.Queue[str | None] = queue.Queue()
        self._executando = False
        self._aguardando_entrada = False
        self._entrada_sensivel = False
        self._encerrando = False
        self._botoes: list[ttk.Button] = []

        self._criar_widgets()
        self._atualizar_menu()
        self.root.after(50, self._processar_eventos)

    def _criar_widgets(self) -> None:
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        navegacao = ttk.Frame(self.root, padding=12)
        navegacao.grid(row=0, column=0, sticky="ns")
        ttk.Label(navegacao, text="StudyRats", font=("TkDefaultFont", 16, "bold")).pack(
            pady=(0, 6)
        )
        self._status = ttk.Label(navegacao, text="", wraplength=170)
        self._status.pack(pady=(0, 10))
        self._menu = ttk.Frame(navegacao)
        self._menu.pack(fill="x", expand=True)
        ttk.Button(navegacao, text="Encerrar aplicação", command=self._fechar).pack(
            side="bottom", fill="x", pady=(12, 0)
        )

        conteudo = ttk.Frame(self.root, padding=(0, 12, 12, 12))
        conteudo.grid(row=0, column=1, sticky="nsew")
        conteudo.columnconfigure(0, weight=1)
        conteudo.rowconfigure(1, weight=1)
        ttk.Label(conteudo, text="Saída e entrada do aplicativo").grid(
            row=0, column=0, sticky="w"
        )

        self._saida = tk.Text(conteudo, height=16, wrap="word", state="disabled")
        self._saida.grid(row=1, column=0, sticky="nsew", pady=(6, 6))
        rolagem = ttk.Scrollbar(conteudo, command=self._saida.yview)
        rolagem.grid(row=1, column=1, sticky="ns", pady=(6, 6))
        self._saida.configure(yscrollcommand=rolagem.set)

        linha_entrada = ttk.Frame(conteudo)
        linha_entrada.grid(row=2, column=0, columnspan=2, sticky="ew")
        linha_entrada.columnconfigure(0, weight=1)
        self._entrada = ttk.Entry(linha_entrada, state="disabled")
        self._entrada.grid(row=0, column=0, sticky="ew")
        self._entrada.bind("<Return>", self._enviar_entrada)
        self._enviar = ttk.Button(
            linha_entrada,
            text="Enviar",
            command=self._enviar_entrada,
            state="disabled",
        )
        self._enviar.grid(row=0, column=1, padx=(6, 0))

        ttk.Separator(conteudo).grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=12
        )
        ttk.Label(conteudo, text="Ratinho — ajuda sobre o StudyRats").grid(
            row=4, column=0, columnspan=2, sticky="w"
        )
        linha_assistente = ttk.Frame(conteudo)
        linha_assistente.grid(row=5, column=0, columnspan=2, sticky="ew", pady=6)
        linha_assistente.columnconfigure(0, weight=1)
        self._pergunta = ttk.Entry(linha_assistente)
        self._pergunta.grid(row=0, column=0, sticky="ew")
        self._pergunta.bind("<Return>", self._perguntar)
        ttk.Button(
            linha_assistente,
            text="Perguntar",
            command=self._perguntar,
        ).grid(row=0, column=1, padx=(6, 0))
        self._resposta = tk.Text(conteudo, height=5, wrap="word", state="disabled")
        self._resposta.grid(row=6, column=0, columnspan=2, sticky="ew")
        self._mostrar_resposta(
            "Olá! Sou o Ratinho. Pergunte como usar cadastro, modelos, sessões, "
            "salas, comunidades, calendário ou RatCoins."
        )

    def _atualizar_menu(self) -> None:
        for botao in self._botoes:
            botao.destroy()
        self._botoes.clear()

        if lista.estado.usuario_logado is None:
            self._status.configure(text="Desconectado")
            opcoes = [
                ("Cadastrar usuário", self.aplicacao.cadastro.cadastrar),
                ("Fazer login", self.aplicacao.contas.realizar_login),
            ]
        else:
            ratname = lista.estado.usuario_logado
            self._status.configure(
                text=f"{ratname}\n{lista.estado.tipo_usuario_logado}"
            )
            opcoes = [
                ("Perfil", self.aplicacao._menu_perfil),
                ("Modelo de estudo", self.aplicacao._usar_modelo_estudo),
                ("Sala com monitor", self.aplicacao.salas.exibir_sala_de_estudo),
                ("Sessão de estudo", self.aplicacao.registro_presenca.registrar),
                ("Comunidades", self.aplicacao.comunidades.menu),
                ("RatCoins", self.aplicacao.recompensas.menu),
                ("Calendário", self.aplicacao.calendario.menu),
                ("Ranking", self._abrir_ranking),
            ]
            usuario = self.aplicacao._usuario_atual()
            if usuario is not None and (
                self.aplicacao.contas.tem_acesso_debug(usuario, 1)
                or self.aplicacao.contas.tem_acesso_debug(usuario, 2)
            ):
                opcoes.append(("Debug", self.aplicacao._menu_debug))
            if lista.estado.tipo_usuario_logado == lista.estado.TIPO_MONITOR:
                opcoes.append(("Área do monitor", self.aplicacao.area_monitor.menu))
            opcoes.append(("Sair da conta", self.aplicacao.contas.deslogar))

        for texto, acao in opcoes:
            botao = ttk.Button(
                self._menu,
                text=texto,
                command=lambda funcao=acao: self._executar(funcao),
            )
            botao.pack(fill="x", pady=2)
            self._botoes.append(botao)

    def _abrir_ranking(self) -> None:
        self.aplicacao.ranking_estudantes.exibir_ranking()
        self.aplicacao.ranking_monitores.exibir()

    def _executar(self, acao) -> None:
        if self._executando:
            return
        self._executando = True
        self._habilitar_menu(False)
        self._escrever("\n")

        def executar_acao() -> None:
            entrada_original = builtins.input
            impressao_original = builtins.print
            saida_original = sys.stdout

            def input_gui(prompt: object = "") -> str:
                texto = str(prompt)
                self._eventos.put(("prompt", texto))
                resposta = self._entradas.get()
                if resposta is None:
                    raise EOFError("A janela foi fechada.")
                return resposta

            def print_gui(*valores, sep=" ", end="\n", file=None, flush=False) -> None:
                if file is not None:
                    impressao_original(*valores, sep=sep, end=end, file=file, flush=flush)
                    return
                texto = sep.join(str(valor) for valor in valores) + end
                self._eventos.put(("saida", texto))

            builtins.input = input_gui
            builtins.print = print_gui
            sys.stdout = _SaidaJanela(self._eventos)
            try:
                acao()
                if lista.estado.usuario_logado is not None:
                    self.aplicacao.recompensas.verificar_notificacoes()
            except EOFError:
                pass
            finally:
                builtins.input = entrada_original
                builtins.print = impressao_original
                sys.stdout = saida_original
                self._eventos.put(("fim", ""))

        threading.Thread(target=executar_acao, daemon=True).start()

    def _processar_eventos(self) -> None:
        try:
            while True:
                tipo, texto = self._eventos.get_nowait()
                if tipo == "saida":
                    self._escrever(texto)
                elif tipo == "prompt":
                    self._aguardando_entrada = True
                    self._entrada_sensivel = "senha" in texto.casefold()
                    self._entrada.configure(
                        state="normal",
                        show="*" if self._entrada_sensivel else "",
                    )
                    self._enviar.configure(state="normal")
                    self._entrada.focus_set()
                    if texto:
                        self._escrever(texto)
                elif tipo == "fim":
                    self._executando = False
                    self._aguardando_entrada = False
                    self._entrada.configure(state="disabled", show="")
                    self._enviar.configure(state="disabled")
                    self._entrada.delete(0, "end")
                    self._atualizar_menu()
                    self._habilitar_menu(True)
        except queue.Empty:
            pass
        if not self._encerrando:
            self.root.after(50, self._processar_eventos)

    def _enviar_entrada(self, _evento=None):
        if not self._aguardando_entrada:
            return "break"
        resposta = self._entrada.get()
        if not self._entrada_sensivel:
            self._escrever(f"> {resposta}\n")
        self._entrada.delete(0, "end")
        self._entrada.configure(state="disabled", show="")
        self._enviar.configure(state="disabled")
        self._aguardando_entrada = False
        self._entradas.put(resposta)
        return "break"

    def _perguntar(self, _evento=None):
        pergunta = self._pergunta.get().strip()
        if not pergunta:
            return "break"
        self._pergunta.delete(0, "end")
        self._mostrar_resposta(responder(pergunta))
        return "break"

    def _mostrar_resposta(self, texto: str) -> None:
        self._resposta.configure(state="normal")
        self._resposta.delete("1.0", "end")
        self._resposta.insert("1.0", texto)
        self._resposta.configure(state="disabled")

    def _escrever(self, texto: str) -> None:
        self._saida.configure(state="normal")
        self._saida.insert("end", texto)
        self._saida.see("end")
        self._saida.configure(state="disabled")

    def _habilitar_menu(self, habilitado: bool) -> None:
        estado = "normal" if habilitado else "disabled"
        for botao in self._botoes:
            botao.configure(state=estado)

    def _fechar(self) -> None:
        self._encerrando = True
        self._entradas.put(None)
        self.root.destroy()

    def executar(self) -> None:
        self.root.mainloop()


def iniciar_interface(aplicacao) -> None:
    persistencia.inicializar_arquivos()
    aplicacao.salas.limpar_sessoes_expiradas()
    StudyRatsGUI(aplicacao).executar()
