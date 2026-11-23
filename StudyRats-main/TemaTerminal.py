import os
import sys

CORES = {
    "titulo": "95",
    "destaque": "96",
    "opcao": "94",
    "prompt": "93",
    "sucesso": "92",
    "aviso": "93",
    "erro": "91",
    "suave": "90",
    "reset": "0",
}

def _ativar_ansi_windows() -> None:
    if os.name != "nt":
        return
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        identificador = kernel32.GetStdHandle(-11)
        modo = ctypes.c_uint()
        if kernel32.GetConsoleMode(identificador, ctypes.byref(modo)):
            kernel32.SetConsoleMode(identificador, modo.value | 0x0004)
    except (AttributeError, OSError):
        return


_ativar_ansi_windows()


def colorir(texto: object, cor: str) -> str:
    conteudo = str(texto)
    if "NO_COLOR" in os.environ or not sys.stdout.isatty():
        return conteudo
    codigo = CORES.get(cor)
    if codigo is None or cor == "reset":
        return conteudo
    return f"\033[{codigo}m{conteudo}\033[{CORES['reset']}m"


def titulo(texto: str) -> None:
    largura = max(34, len(texto) + 4)
    print(colorir("=" * largura, "titulo"))
    print(colorir(f"  {texto}", "titulo"))
    print(colorir("=" * largura, "titulo"))


def opcao(numero: str, descricao: str) -> None:
    print(f"  {colorir(numero, 'opcao')}  {descricao}")


def perguntar(texto: str) -> str:
    return input(colorir(texto, "prompt"))


def mensagem(texto: str, tipo: str = "suave") -> None:
    print(colorir(texto, tipo))

