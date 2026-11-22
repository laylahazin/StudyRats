import os  # Importa os: acessa diretorios e substitui arquivos temporarios.
import sys  # Importa sys: detecta se a saida usa um terminal interativo.



CORES = {  # Guarda em CORES o valor produzido por {.
    "titulo": "95",  # Na chave "titulo", associa o codigo ANSI usado pelo texto de titulo; nesta entrada recebe "95",.
    "destaque": "96",  # Na chave "destaque", associa o codigo ANSI usado por informacoes destacadas; nesta entrada recebe "96",.
    "opcao": "94",  # Na chave "opcao", associa o codigo ANSI usado nos numeros de opcoes; nesta entrada recebe "94",.
    "prompt": "93",  # Na chave "prompt", associa o codigo ANSI usado nas perguntas digitadas; nesta entrada recebe "93",.
    "sucesso": "92",  # Na chave "sucesso", associa o codigo ANSI usado em mensagens positivas; nesta entrada recebe "92",.
    "aviso": "93",  # Na chave "aviso", associa o codigo ANSI usado em avisos; nesta entrada recebe "93",.
    "erro": "91",  # Na chave "erro", associa o codigo ANSI usado em erros; nesta entrada recebe "91",.
    "suave": "90",  # Na chave "suave", associa o codigo ANSI usado em informacoes secundarias; nesta entrada recebe "90",.
    "reset": "0",  # Na chave "reset", associa o codigo ANSI que encerra a formatacao colorida; nesta entrada recebe "0",.
}  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

def _ativar_ansi_windows() -> None:  # Declara o metodo _ativar_ansi_windows: implementa esta funcionalidade da classe.
    if os.name != "nt":  # Testa a condicao os.name != "nt" e executa o bloco seguinte somente quando ela for verdadeira.
        return  # Encerra este metodo imediatamente sem devolver valor.
    try:  # Protege o bloco seguinte contra dados que podem causar excecao.
        import ctypes  # Importa ctypes: acessa a API do console Windows para ativar ANSI.

        kernel32 = ctypes.windll.kernel32  # Guarda em kernel32 o valor produzido por ctypes.windll.kernel32.
        identificador = kernel32.GetStdHandle(-11)  # Guarda em identificador o valor produzido por kernel32.GetStdHandle(-11).
        modo = ctypes.c_uint()  # determina se a aplicacao usa horario real ou manual
        if kernel32.GetConsoleMode(identificador, ctypes.byref(modo)):  # Testa a condicao kernel32.GetConsoleMode(identificador, ctypes.byref(modo)) e executa o bloco seguinte somente quando ela for verdadeira.
            kernel32.SetConsoleMode(identificador, modo.value | 0x0004)  # Executa nesta linha kernel32.SetConsoleMode(identificador, modo.value | 0x0004) no contexto desta funcionalidade.
    except (AttributeError, OSError):  # Trata (AttributeError, OSError) emitida pelo bloco try, indicando que a entrada ou dado protegido era invalido.
        return  # Encerra este metodo imediatamente sem devolver valor.


_ativar_ansi_windows()  # Executa nesta linha _ativar_ansi_windows() no contexto desta funcionalidade.


def colorir(texto: object, cor: str) -> str:  # Declara o metodo colorir: implementa esta funcionalidade da classe.
    conteudo = str(texto)  # converte o texto de exibicao em objeto textual
    if "NO_COLOR" in os.environ or not sys.stdout.isatty():  # Testa a condicao "NO_COLOR" in os.environ or not sys.stdout.isatty() e executa o bloco seguinte somente quando ela for verdadeira.
        return conteudo  # Encerra o metodo e devolve ao chamador conteudo.
    codigo = CORES.get(cor)  # resolve o codigo ANSI ou o campo correspondente ao estilo ou acesso solicitado
    if codigo is None or cor == "reset":  # Testa a condicao codigo is None or cor == "reset" e executa o bloco seguinte somente quando ela for verdadeira.
        return conteudo  # Encerra o metodo e devolve ao chamador conteudo.
    return f"\033[{codigo}m{conteudo}\033[{CORES['reset']}m"  # Encerra o metodo e devolve ao chamador f"\033[{codigo}m{conteudo}\033[{CORES['reset']}m".


def titulo(texto: str) -> None:  # Declara o metodo titulo: implementa esta funcionalidade da classe.
    largura = max(34, len(texto) + 4)  # calcula uma largura suficiente para enquadrar o titulo
    print(colorir("=" * largura, "titulo"))  # Guarda em print(colorir(" o valor produzido por " * largura, "titulo")).
    print(colorir(f"  {texto}", "titulo"))  # Exibe no terminal {texto}.
    print(colorir("=" * largura, "titulo"))  # Guarda em print(colorir(" o valor produzido por " * largura, "titulo")).


def opcao(numero: str, descricao: str) -> None:  # Declara o metodo opcao: implementa esta funcionalidade da classe.
    print(f"  {colorir(numero, 'opcao')}  {descricao}")  # Exibe no terminal {colorir(numero, .


def perguntar(texto: str) -> str:  # Declara o metodo perguntar: implementa esta funcionalidade da classe.
    return input(colorir(texto, "prompt"))  # Encerra o metodo e devolve ao chamador input(colorir(texto, "prompt")).


def mensagem(texto: str, tipo: str = "suave") -> None:  # Declara o metodo mensagem: implementa esta funcionalidade da classe.
    print(colorir(texto, tipo))  # Escreve no terminal o conteudo preparado por esta chamada.
