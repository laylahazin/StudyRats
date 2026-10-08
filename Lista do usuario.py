usuarios = []

usuario_logado = None


def cadastrar_usuario():
    print("\n--- TELA DE CADASTRO ---")
    email = input("Digite seu e-mail: ").strip().lower()

    for usuario in usuarios:
        if usuario["email"] == email:
            print("Erro: Este e-mail já está cadastrado!")
            return

    senha = input("Digite sua senha: ")
    ratname = input("Digite seu Ratname: ")

    for usuario in usuarios:
        if usuario["ratname"] == ratname:
            print("Erro: Este Ratname já está em uso!")
            return

    novo_usuario = {"email": email, "senha": senha, "ratname": ratname}

    usuarios.append(novo_usuario)
    print("Cadastro realizado com sucesso!")


def realizar_login():
    global usuario_logado

    print("\n--- TELA DE LOGIN ---")
    email = input("Digite seu e-mail: ").strip().lower()
    senha = input("Digite sua senha: ")

    # busca a lista
    for usuario in usuarios:
        if usuario["email"] == email and usuario["senha"] == senha:
            usuario_logado = usuario["ratname"]  # Define o usuário como logado
            print(f"\nLogin bem-sucedido! Você está conectado como: {usuario_logado}")
            return

    print("\nErro: E-mail ou senha incorretos.")


def deslogar():
    global usuario_logado
    print(f"\nSaindo da conta de {usuario_logado}...")
    usuario_logado = None  # tira o login do usuario
    print("Você saiu da conta com sucesso!")


def menu_principal():
    while True:
        print("\n====================")
        
    
        if usuario_logado:
            print(f" Status: LOGADO como ({usuario_logado})")
            print("====================")
            print("1. Área Restrita / Perfil")
            print("2. Sair da conta (Logoff)")
            print("3. Encerrar aplicação")
        else:
            print(" Status: DESCONECTADO")
            print("====================")
            print("1. Cadastrar novo usuário")
            print("2. Fazer Login")
            print("3. Encerrar aplicação")

        opcao = input("\nEscolha uma opção: ").strip()

        # --- FLUXO QUANDO O USUÁRIO JÁ ESTÁ LOGADO ---
        if usuario_logado is not None:
            if opcao == "1":
                print(f"\n[ÁREA RESTRITA] Bem-vindo ao painel do usuário, {usuario_logado}!")
            elif opcao == "2":
                deslogar()  # Apenas limpa a variável logado, sem fechar o programa
            elif opcao == "3":
                print("Encerrando a aplicação. Até logo!")
                break
            else:
                print("Opção inválida, tente novamente.")

        # --- FLUXO QUANDO NINGUÉM ESTÁ LOGADO ---
        else:
            if opcao == "1":
                cadastrar_usuario()
            elif opcao == "2":
                realizar_login()
            elif opcao == "3":
                print("Encerrando a aplicação. Até logo!")
                break
            else:
                print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu_principal()