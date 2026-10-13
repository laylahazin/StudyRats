import hashlib  
import hmac  
import json  
import os  
import secrets  

from pathlib import Path  


DIRETORIO_DADOS = Path(__file__).resolve().parent / "dados" 

def _caminho_arquivo(nome):  
    """Retorna o caminho do arquivo JSON solicitado dentro da pasta de dados."""  
    return DIRETORIO_DADOS / nome  


def inicializar_arquivos_json():  
    arquivos_padrao = {  
        "usuarios.json": [],  
        "participantes_salas.json": {},  
        "presencas.json": {},  
        "modelos_estudo.json": {},  
        "configuracao_horario.json": {  
            "modo": "automatico",  
            "data_hora_manual": None,  
        },  
    }  
    for nome, valor_padrao in arquivos_padrao.items():  
        if not _caminho_arquivo(nome).exists():  
            salvar_json(nome, valor_padrao)  


def carregar_json(nome, valor_padrao):  
    caminho = _caminho_arquivo(nome)  
    try:  
        with caminho.open("r", encoding="utf-8") as arquivo:  
            return json.load(arquivo)  
    except FileNotFoundError:  
        return valor_padrao  
    except json.JSONDecodeError as erro:  
        raise ValueError(f"O arquivo JSON '{caminho}' está inválido.") from erro  


def salvar_json(nome, dados):  
    DIRETORIO_DADOS.mkdir(parents=True, exist_ok=True)  
    caminho = _caminho_arquivo(nome)  
    temporario = caminho.with_name(f"{caminho.name}.tmp")  

    with temporario.open("w", encoding="utf-8") as arquivo:  
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)  
        arquivo.write("\n")  

    os.replace(temporario, caminho)  


def criar_credencial_senha(senha):  
    salt = secrets.token_bytes(16)  
    senha_hash = hashlib.pbkdf2_hmac(  
        "sha256",  
        senha.encode("utf-8"),  
        salt,  
        310_000,  
    )  
    return {"senha_salt": salt.hex(), "senha_hash": senha_hash.hex()}  


def verificar_senha(senha, salt_hex, senha_hash_hex):  
    salt = bytes.fromhex(salt_hex)  
    hash_armazenado = bytes.fromhex(senha_hash_hex)  
    hash_informado = hashlib.pbkdf2_hmac(  
        "sha256",  
        senha.encode("utf-8"),  
        salt,  
        310_000,  
    )  
    return hmac.compare_digest(hash_informado, hash_armazenado)  
