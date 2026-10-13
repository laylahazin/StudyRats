import hashlib  # importa funções de hash e derivação de chave, usadas para armazenar credenciais sem guardar senhas em texto puro
import hmac  # importa a comparação resistente a diferenças de tempo, usada para verificar hashes de senha
import json  # importa funções para converter dados Python em JSON e carregar JSON de arquivos
import os  # importa funções do sistema operacional para substituir arquivos de forma segura
import secrets  # importa o gerador criptograficamente seguro usado para criar valores aleatórios de salt
# salt é um valor aleatório salvo junto ao hash; ele faz senhas iguais produzirem hashes distintos e dificulta ataques com tabelas pré-calculadas
from pathlib import Path  # importa uma API para compor e manipular caminhos de arquivos de forma multiplataforma


DIRETORIO_DADOS = Path(__file__).resolve().parent / "dados" # parent é o diretório que contém este arquivo, e "dados" é a pasta onde os arquivos JSON serão salvos

def _caminho_arquivo(nome):  # converte o nome de um arquivo de dados no caminho absoluto usado pelo projeto
    """Retorna o caminho do arquivo JSON solicitado dentro da pasta de dados."""  # documenta o propósito deste auxiliar interno
    return DIRETORIO_DADOS / nome  # combina a pasta persistente com o nome de arquivo informado


def inicializar_arquivos_json():  # cria os arquivos de dados que ainda não existem e preserva os que já contêm dados
    arquivos_padrao = {  # relaciona cada arquivo inicial ao tipo de dado esperado nele
        "usuarios.json": [],  # começa a base de contas como uma lista vazia
        "participantes_salas.json": {},  # começa os participantes das salas como um objeto vazio
        "presencas.json": {},  # começa os históricos de presença como um objeto indexado por usuário
        "modelos_estudo.json": {},  # começa os modelos salvos como um objeto indexado por usuário
        "configuracao_horario.json": {  # define os campos iniciais usados pelo relógio de teste
            "modo": "automatico",  # seleciona o relógio real do sistema como padrão
            "data_hora_manual": None,  # não define uma hora fixa enquanto o modo automático estiver ativo
        },  # conclui a configuração inicial do relógio
    }  # termina o mapa entre arquivos e estruturas padrão
    for nome, valor_padrao in arquivos_padrao.items():  # percorre cada par de arquivo e valor padrão a ser verificado
        if not _caminho_arquivo(nome).exists():  # evita substituir qualquer arquivo criado em uma execução anterior
            salvar_json(nome, valor_padrao)  # cria somente os arquivos ausentes usando o gravador centralizado


def carregar_json(nome, valor_padrao):  # lê e converte para objetos Python o conteúdo de um arquivo JSON da pasta de dados
    caminho = _caminho_arquivo(nome)  # resolve o caminho completo a partir do nome fornecido pelo chamador
    try:  # tenta abrir e interpretar o JSON, tratando separadamente arquivo ausente e conteúdo corrompido
        with caminho.open("r", encoding="utf-8") as arquivo:  # abre em modo de leitura UTF-8 e fecha o arquivo mesmo se a leitura falhar
            return json.load(arquivo)  # converte o conteúdo JSON em lista, dicionário ou outro valor Python correspondente
    except FileNotFoundError:  # ocorre quando ainda não existe arquivo com o nome solicitado
        return valor_padrao  # devolve o padrão ao chamador sem criar ou gravar arquivo
    except json.JSONDecodeError as erro:  # ocorre quando o arquivo existe, mas seu conteúdo não é JSON válido
        raise ValueError(f"O arquivo JSON '{caminho}' está inválido.") from erro  # identifica o arquivo inválido e preserva a causa original para diagnóstico


def salvar_json(nome, dados):  # serializa dados Python em JSON e substitui o arquivo persistido pelo conteúdo atualizado
    DIRETORIO_DADOS.mkdir(parents=True, exist_ok=True)  # cria a pasta de dados e seus pais se necessário, sem falhar se ela já existir
    caminho = _caminho_arquivo(nome)  # resolve o destino definitivo dentro da pasta de dados
    temporario = caminho.with_name(f"{caminho.name}.tmp")  # prepara um arquivo temporário ao lado do destino para evitar gravação parcial do original

    with temporario.open("w", encoding="utf-8") as arquivo:  # abre ou cria o temporário para escrita textual e garante seu fechamento
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)  # grava JSON legível, preserva caracteres acentuados e indenta os campos com dois espaços
        arquivo.write("\n")  # adiciona uma quebra de linha no final para manter o arquivo organizado

    os.replace(temporario, caminho)  # troca o destino pelo arquivo completo em uma operação, criando-o se ainda não existir


def criar_credencial_senha(senha):  # deriva os valores que serão armazenados para verificar uma senha posteriormente
    salt = secrets.token_bytes(16)  # gera 16 bytes imprevisíveis para que senhas iguais não resultem no mesmo hash
    senha_hash = hashlib.pbkdf2_hmac(  # calcula uma derivação de senha custosa para dificultar tentativas automatizadas
        "sha256",  # seleciona SHA-256 como função de hash subjacente ao PBKDF2
        senha.encode("utf-8"),  # converte a senha textual em bytes usando uma codificação definida
        salt,  # incorpora o salt aleatório exclusivo desta credencial ao cálculo
        310_000,  # repete o cálculo para aumentar o custo de cada tentativa de adivinhar a senha
    )  # conclui a derivação do hash binário da senha
    return {"senha_salt": salt.hex(), "senha_hash": senha_hash.hex()}  # retorna salt e hash como texto hexadecimal para armazenamento em JSON


def verificar_senha(senha, salt_hex, senha_hash_hex):  # confere uma senha digitada comparando sua derivação com a credencial persistida
    salt = bytes.fromhex(salt_hex)  # converte o salt armazenado em hexadecimal de volta para bytes
    hash_armazenado = bytes.fromhex(senha_hash_hex)  # converte o hash hexadecimal da conta para o formato binário usado na comparação
    hash_informado = hashlib.pbkdf2_hmac(  # deriva o hash da senha submetida usando exatamente os parâmetros do cadastro
        "sha256",  # mantém a mesma função de hash usada ao criar a credencial
        senha.encode("utf-8"),  # converte a senha digitada para os bytes que PBKDF2 processa
        salt,  # usa o salt salvo da conta, necessário para reproduzir o hash original
        310_000,  # mantém o mesmo número de iterações aplicado durante a criação
    )  # conclui o cálculo que será comparado com o hash persistido
    return hmac.compare_digest(hash_informado, hash_armazenado)  # retorna igualdade sem comparação de tempo variável por prefixo coincidente
