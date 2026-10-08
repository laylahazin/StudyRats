import lista

def realizar_login():
    print("\n--- TELA DE LOGIN ---")
    email = input("Digite seu e-mail: ").strip().lower()
    senha = input("Digite sua senha: ")

    for usuario in lista.usuarios:
        if usuario["email"] == email and usuario["senha"] == senha:
            lista.usuario_logado = usuario["ratname"]
            print(f"\nLogin bem-sucedido! Você está conectado como: {lista.usuario_logado}")
            return

    print("\nErro: E-mail ou senha incorretos.")


def deslogar():
    print(f"\nSaindo da conta de {lista.usuario_logado}...")
    lista.usuario_logado = None
    print("Você saiu da conta com sucesso!")
