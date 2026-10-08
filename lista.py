usuarios = []

usuario_logado = None


def cadastrar_usuario():
    print("\n--- TELA DE CADASTRO ---")
    while True:
        email = input("Digite seu e-mail: ").strip().lower()
        if email.endswith('@ufrpe.br') and email.count('@') == 1 and len(email) > 9:
            print('Email válido!')
            break
        else:
            print('Email inválido! Verifique se você está colocando o seu email institucional corretamente!')

    for usuario in usuarios:
        if usuario["email"] == email:
            print("Erro: Este e-mail já está cadastrado!")
            return

    while True:
        senha = input('Crie a sua senha no StudyRats! (Ela deve conter de 6 a 8 caracteres, uma letra maiúscula, um caractere especial e um numeral): ')

        if len(senha) < 6:
            print('Senha inválida! A senha deve ter no mínimo 6 caracteres! Tente novamente.')

        elif len(senha) > 8:
            print('Senha inválida! A senha deve ter no máximo 8 caracteres! Tente novamente.')

        elif not any(letra.isupper() for letra in senha):
            print('Senha inválida! A senha deve conter pelo menos uma letra maiúscula! Tente novamente.')

        elif not any(letra.isdigit() for letra in senha):
            print('Senha inválida! A senha deve conter pelo menos um número! Tente novamente.')

        elif senha.isalnum():
            print('Senha inválida! A senha deve conter pelo menos um caractere especial! Tente novamente.')

        else:
            print('Senha válida!')
            break

            
    ratname = input('Crie o seu Ratname: ')

    for usuario in usuarios:
        if usuario["ratname"] == ratname and ratname != '':
            print("Erro: Este Ratname já está em uso ou é inválido!")
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
            usuario_logado = usuario["ratname"]
            print(f"\nLogin bem-sucedido! Você está conectado como: {usuario_logado}")
            return

    print("\nErro: E-mail ou senha incorretos.")


def deslogar():
    global usuario_logado
    print(f"\nSaindo da conta de {usuario_logado}...")
    usuario_logado = None
    print("Você saiu da conta com sucesso!")


def menu_principal():
    while True:
        print("\n====================")
        
    
        if usuario_logado:
            print(f" Status: LOGADO como ({usuario_logado})")
            print("====================")
            print("1. Perfil")
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
                print(f"\nBem-vindo(a), {usuario_logado}!")
            elif opcao == "2":
                deslogar()
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