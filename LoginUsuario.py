from lista import usuarios
from lista import usuario_logado

def realizar_login():
    global usuario_logado

    print("\n--- TELA DE LOGIN ---")
    email = input("Digite seu e-mail: ").strip().lower()
    senha = input("Digite sua senha: ")

    # busca a lista
    for usuario in usuarios:
        if usuario["email"] == email and usuario["senha"] == senha:
            usuario_logado = usuario["ratname"]
            print(f"\nLogin bem-sucedido! Você está conectado como: {usuario_logado}")
            return

    print("\nErro: E-mail ou senha incorretos.")


def deslogar():
    global usuario_logado
    print(f"\nSaindo da conta de {usuario_logado}...")
    usuario_logado = None
    print("Você saiu da conta com sucesso!")
