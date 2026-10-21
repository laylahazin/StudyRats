import lista  # compartilha a lista de contas e o estado da sessão autenticada
from Persistencia import verificar_senha  # recalcula e compara de forma segura o hash da senha


def realizar_login():  # autentica uma conta usando o endereço de e-mail e a senha informados
    print("\n--- TELA DE LOGIN ---")  # identifica a tela de autenticação
    email = input("Digite seu e-mail: ").strip().lower()  # lê o e-mail e normaliza espaços e maiúsculas para comparar contas
    senha = input("Digite sua senha: ")  # lê a senha sem modificá-la, pois espaços podem fazer parte dela

    for usuario in lista.usuarios:  # procura a conta cujo endereço corresponde ao informado
        if usuario["email"].lower() != email:  # ignora as contas com endereços diferentes
            continue  # examina a próxima conta da lista

        if "senha_hash" not in usuario or "senha_salt" not in usuario:  # exige os dois valores usados para conferir a senha
            raise ValueError(  # interrompe a autenticação diante de dados de conta incompatíveis
                "A conta salva não possui credenciais compatíveis. "  # explica que o formato salvo não pode ser verificado
                "Remova-a ou faça a migração antes de tentar entrar."  # indica como corrigir a conta antiga
            )  # conclui a exceção com uma orientação para migração

        if verificar_senha(senha, usuario["senha_salt"], usuario["senha_hash"]):  # deriva o hash informado e compara com as credenciais salvas
            lista.usuario_logado = usuario["ratname"]  # atualiza o estado compartilhado com o Ratname autenticado
            print(f"\nLogin bem-sucedido! Você está conectado como: {lista.usuario_logado}")  # confirma a autenticação e identifica a conta
            return  # encerra a busca imediatamente após autenticar a conta
        break  # não verifica outras contas porque este e-mail já foi localizado

    print("\nErro: E-mail ou senha incorretos.")  # informa que os dados apresentados não permitiram autenticar


def deslogar():  # encerra a sessão autenticada e retorna a aplicação para o estado desconectado
    print(f"\nSaindo da conta de {lista.usuario_logado}...")  # identifica qual conta está encerrando a sessão
    lista.usuario_logado = None  # apaga o Ratname conectado no estado compartilhado
    print("Você saiu da conta com sucesso!")  # confirma que a sessão foi encerrada
