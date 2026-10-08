import lista
from CadastroUsuario import cadastrar_usuario
from LoginUsuario import realizar_login, deslogar

def menu_principal():
    while True:
        print("\n====================")
        
    
        if lista.usuario_logado:
            print(f" Status: LOGADO como ({lista.usuario_logado})")
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
        if lista.usuario_logado is not None:
            if opcao == "1":
                print(f"\nBem-vindo(a), {lista.usuario_logado}!")
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
