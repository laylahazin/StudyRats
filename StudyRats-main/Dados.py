import hashlib
import hmac
import json
import os
import secrets
from pathlib import Path


DIRETORIO_DADOS = Path(__file__).resolve().parent / "dados"


class PersistenciaJSON:
    def __init__(self, diretorio: Path = DIRETORIO_DADOS) -> None:
        self.diretorio = diretorio

    def _caminho_arquivo(self, nome: str) -> Path:
        return self.diretorio / nome

    def inicializar_arquivos(self) -> None:
        arquivos_padrao = {
            "usuarios.json": [],
            "participantes_salas.json": {},
            "presencas.json": {},
            "modelos_estudo.json": {},
            "ratcoins.json": {
                "usuarios": {},
                "eventos_processados": {},
            },
            "comunidades.json": [],
            "calendario.json": {},
            "blocos_notas.json": {},
            "configuracao_horario.json": {
                "modo": "automatico",
                "data_hora_manual": None,
            },
            "notificacoes.json": {
                "usuarios": {},
                "datas_processadas": [],
            },
        }
        for nome, valor_padrao in arquivos_padrao.items():
            if not self._caminho_arquivo(nome).exists():
                self.salvar(nome, valor_padrao)

    def carregar(self, nome: str, valor_padrao):
        caminho = self._caminho_arquivo(nome)
        try:
            with caminho.open("r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            return valor_padrao
        except json.JSONDecodeError as erro:
            raise ValueError(f"O arquivo JSON '{caminho}' está inválido.") from erro

    def salvar(self, nome: str, dados) -> None:
        self.diretorio.mkdir(parents=True, exist_ok=True)
        caminho = self._caminho_arquivo(nome)
        temporario = caminho.with_name(f"{caminho.name}.tmp")

        with temporario.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
            arquivo.write("\n")

        os.replace(temporario, caminho)


class GerenciadorCredenciais:
    ITERACOES = 310_000

    def criar(self, senha: str) -> dict[str, str]:
        salt = secrets.token_bytes(16)
        senha_hash = hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode("utf-8"),
            salt,
            self.ITERACOES,
        )
        return {"senha_salt": salt.hex(), "senha_hash": senha_hash.hex()}

    def verificar(self, senha: str, salt_hex: str, senha_hash_hex: str) -> bool:
        salt = bytes.fromhex(salt_hex)
        hash_armazenado = bytes.fromhex(senha_hash_hex)
        hash_informado = hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode("utf-8"),
            salt,
            self.ITERACOES,
        )
        return hmac.compare_digest(hash_informado, hash_armazenado)


persistencia = PersistenciaJSON()
gerenciador_credenciais = GerenciadorCredenciais()


def inicializar_arquivos_json() -> None:
    persistencia.inicializar_arquivos()


def carregar_json(nome: str, valor_padrao):
    return persistencia.carregar(nome, valor_padrao)


def salvar_json(nome: str, dados) -> None:
    persistencia.salvar(nome, dados)


def criar_credencial_senha(senha: str) -> dict[str, str]:
    return gerenciador_credenciais.criar(senha)


def verificar_senha(senha: str, salt_hex: str, senha_hash_hex: str) -> bool:
    return gerenciador_credenciais.verificar(senha, salt_hex, senha_hash_hex)
