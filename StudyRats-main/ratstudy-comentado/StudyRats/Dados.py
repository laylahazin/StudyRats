import hashlib  # Importa hashlib: fornece PBKDF2 com SHA-256 para proteger senhas.
import hmac  # Importa hmac: compara hashes em tempo constante.
import json  # Importa json: le e escreve os arquivos JSON persistentes.
import os  # Importa os: acessa diretorios e substitui arquivos temporarios.
import secrets  # Importa secrets: gera salts criptograficamente aleatorios.
from pathlib import Path  # Importa de pathlib os recursos Path usados neste modulo.


DIRETORIO_DADOS = Path(__file__).resolve().parent / "dados"  # Resolve a pasta dados ao lado do proprio modulo Dados.py, tornando a persistencia independente do diretorio atual do terminal.


class PersistenciaJSON:  # Declara a classe PersistenciaJSON: centraliza leitura e gravacao segura dos arquivos JSON.
    def __init__(self, diretorio: Path = DIRETORIO_DADOS) -> None:  # Declara o metodo __init__: implementa esta funcionalidade da classe.
        self.diretorio = diretorio  # Guarda em self.diretorio o valor produzido por diretorio.

    def _caminho_arquivo(self, nome: str) -> Path:  # Declara o metodo _caminho_arquivo: implementa esta funcionalidade da classe.
        return self.diretorio / nome  # Encerra o metodo e devolve ao chamador self.diretorio / nome.

    def inicializar_arquivos(self) -> None:  # Declara o metodo inicializar_arquivos: cria cada arquivo JSON ausente com seu valor inicial.
        arquivos_padrao = {  # Guarda em arquivos_padrao o valor produzido por {.
            "usuarios.json": [],  # Armazena na chave "usuarios.json" o valor [], nesta estrutura.
            "participantes_salas.json": {},  # Armazena na chave "participantes_salas.json" o valor {}, nesta estrutura.
            "presencas.json": {},  # Armazena na chave "presencas.json" o valor {}, nesta estrutura.
            "modelos_estudo.json": {},  # Armazena na chave "modelos_estudo.json" o valor {}, nesta estrutura.
            "ratcoins.json": {  # Armazena na chave "ratcoins.json" o valor { nesta estrutura.
                "usuarios": {},  # Na chave "usuarios", organiza dados separados por Ratname dentro deste arquivo; nesta entrada recebe {},.
                "eventos_processados": {},  # Na chave "eventos_processados", marca recompensas ja concedidas para impedir duplicacao; nesta entrada recebe {},.
            },  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            "comunidades.json": [],  # Armazena na chave "comunidades.json" o valor [], nesta estrutura.
            "calendario.json": {},  # Armazena na chave "calendario.json" o valor {}, nesta estrutura.
            "blocos_notas.json": {},  # Armazena na chave "blocos_notas.json" o valor {}, nesta estrutura.
            "configuracao_horario.json": {  # Armazena na chave "configuracao_horario.json" o valor { nesta estrutura.
                "modo": "automatico",  # Na chave "modo", seleciona horario automatico ou manual; nesta entrada recebe "automatico",.
                "data_hora_manual": None,  # Na chave "data_hora_manual", guarda a data e hora fixa usada pelo modo manual; nesta entrada recebe None,.
            },  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
            "notificacoes.json": {  # Armazena na chave "notificacoes.json" o valor { nesta estrutura.
                "usuarios": {},  # Na chave "usuarios", organiza dados separados por Ratname dentro deste arquivo; nesta entrada recebe {},.
                "datas_processadas": [],  # Na chave "datas_processadas", marca datas ja notificadas para evitar repeticao; nesta entrada recebe [],.
            },  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        }  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        for nome, valor_padrao in arquivos_padrao.items():  # Percorre nome, valor_padrao in arquivos_padrao.items(), executando o bloco uma vez para cada elemento.
            if not self._caminho_arquivo(nome).exists():  # Testa a condicao not self._caminho_arquivo(nome).exists() e executa o bloco seguinte somente quando ela for verdadeira.
                self.salvar(nome, valor_padrao)  # Executa self.salvar(nome, valor_padrao); o efeito desta chamada participa diretamente desta funcionalidade.

    def carregar(self, nome: str, valor_padrao):  # Declara o metodo carregar: le o JSON solicitado ou devolve valor_padrao quando o arquivo nao existe.
        caminho = self._caminho_arquivo(nome)  # resolve o caminho completo do arquivo JSON usado nesta operacao
        try:  # Protege o bloco seguinte contra dados que podem causar excecao.
            with caminho.open("r", encoding="utf-8") as arquivo:  # Abre o contexto caminho.open("r", encoding="utf-8") as arquivo e garante o fechamento seguro ao sair do bloco.
                return json.load(arquivo)  # Encerra o metodo e devolve ao chamador json.load(arquivo).
        except FileNotFoundError:  # Trata FileNotFoundError emitida pelo bloco try, indicando que a entrada ou dado protegido era invalido.
            return valor_padrao  # Encerra o metodo e devolve ao chamador valor_padrao.
        except json.JSONDecodeError as erro:  # Trata json.JSONDecodeError as erro emitida pelo bloco try, indicando que a entrada ou dado protegido era invalido.
            raise ValueError(f"O arquivo JSON '{caminho}' está inválido.") from erro  # Interrompe a operacao com ValueError(f"O arquivo JSON '{caminho}' está inválido.") from erro, indicando dados ou estado invalidos.

    def salvar(self, nome: str, dados) -> None:  # Declara o metodo salvar: grava os dados com arquivo temporario e substitui o destino completo.
        self.diretorio.mkdir(parents=True, exist_ok=True)  # Garante que a pasta de dados exista, criando diretorios pais quando necessario e nao falhando caso a pasta ja exista.
        caminho = self._caminho_arquivo(nome)  # resolve o caminho completo do arquivo JSON usado nesta operacao
        temporario = caminho.with_name(f"{caminho.name}.tmp")  # guarda o caminho temporario que sera instalado no destino apos a gravacao completa

        with temporario.open("w", encoding="utf-8") as arquivo:  # Abre o contexto temporario.open("w", encoding="utf-8") as arquivo e garante o fechamento seguro ao sair do bloco.
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)  # Escreve os dados como JSON no arquivo temporario: ensure_ascii=False preserva caracteres Unicode e indent=2 usa recuo de dois espacos por nivel.
            arquivo.write("\n")  # Adiciona uma quebra de linha ao final do conteudo JSON.

        os.replace(temporario, caminho)  # Substitui o destino pelo arquivo temporario ja completo em uma unica operacao atomica.


class GerenciadorCredenciais:  # Declara a classe GerenciadorCredenciais: gera e verifica hashes de senhas.
    ITERACOES = 310_000  # Define 310.000 iteracoes PBKDF2, tornando a derivacao da senha deliberadamente mais lenta contra tentativas por forca bruta.

    def criar(self, senha: str) -> dict[str, str]:  # Declara o metodo criar: gera um salt novo e deriva o hash da senha.
        salt = secrets.token_bytes(16)  # guarda os bytes aleatorios usados por esta derivacao PBKDF2
        senha_hash = hashlib.pbkdf2_hmac(  # guarda o hash derivado da senha sem armazenar texto aberto
            "sha256",  # Executa nesta linha "sha256", no contexto desta funcionalidade.
            senha.encode("utf-8"),  # Executa nesta linha senha.encode("utf-8"), no contexto desta funcionalidade.
            salt,  # Executa nesta linha salt, no contexto desta funcionalidade.
            self.ITERACOES,  # Executa self.ITERACOES,; o efeito desta chamada participa diretamente desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        return {"senha_salt": salt.hex(), "senha_hash": senha_hash.hex()}  # Encerra o metodo e devolve ao chamador {"senha_salt": salt.hex(), "senha_hash": senha_hash.hex()}.

    def verificar(self, senha: str, salt_hex: str, senha_hash_hex: str) -> bool:  # Declara o metodo verificar: deriva o hash da tentativa usando o salt salvo e compara com o hash armazenado.
        salt = bytes.fromhex(salt_hex)  # guarda os bytes aleatorios usados por esta derivacao PBKDF2
        hash_armazenado = bytes.fromhex(senha_hash_hex)  # converte o hash persistido em bytes para comparacao
        hash_informado = hashlib.pbkdf2_hmac(  # calcula o hash da tentativa atual usando o mesmo salt e custo da conta
            "sha256",  # Executa nesta linha "sha256", no contexto desta funcionalidade.
            senha.encode("utf-8"),  # Executa nesta linha senha.encode("utf-8"), no contexto desta funcionalidade.
            salt,  # Executa nesta linha salt, no contexto desta funcionalidade.
            self.ITERACOES,  # Executa self.ITERACOES,; o efeito desta chamada participa diretamente desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        return hmac.compare_digest(hash_informado, hash_armazenado)  # Encerra o metodo e devolve ao chamador hmac.compare_digest(hash_informado, hash_armazenado).


persistencia = PersistenciaJSON()  # Cria o gerenciador global usado para localizar e gravar os arquivos JSON da aplicacao.
gerenciador_credenciais = GerenciadorCredenciais()  # Cria o gerenciador global usado para criar e verificar as credenciais das contas.


def inicializar_arquivos_json() -> None:  # Declara o metodo inicializar_arquivos_json: implementa esta funcionalidade da classe.
    persistencia.inicializar_arquivos()  # Executa nesta linha persistencia.inicializar_arquivos() no contexto desta funcionalidade.


def carregar_json(nome: str, valor_padrao):  # Declara o metodo carregar_json: implementa esta funcionalidade da classe.
    return persistencia.carregar(nome, valor_padrao)  # Encerra o metodo e devolve ao chamador persistencia.carregar(nome, valor_padrao).


def salvar_json(nome: str, dados) -> None:  # Declara o metodo salvar_json: implementa esta funcionalidade da classe.
    persistencia.salvar(nome, dados)  # Executa nesta linha persistencia.salvar(nome, dados) no contexto desta funcionalidade.


def criar_credencial_senha(senha: str) -> dict[str, str]:  # Declara o metodo criar_credencial_senha: implementa esta funcionalidade da classe.
    return gerenciador_credenciais.criar(senha)  # Encerra o metodo e devolve ao chamador gerenciador_credenciais.criar(senha).


def verificar_senha(senha: str, salt_hex: str, senha_hash_hex: str) -> bool:  # Declara o metodo verificar_senha: implementa esta funcionalidade da classe.
    return gerenciador_credenciais.verificar(senha, salt_hex, senha_hash_hex)  # Encerra o metodo e devolve ao chamador gerenciador_credenciais.verificar(senha, salt_hex, senha_hash_hex).
