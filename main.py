import lista 
from CadastroUsuario import cadastrar_usuario  
from Horario import acessar_configuracao_horario  
from LoginUsuario import deslogar, menu_perfil, realizar_login  
from ModeloEstudo import modelo_estudo  
from Persistencia import inicializar_arquivos_json  
from RegistroPresenca import registro_presenca  
from SalaEstudo import exibir_sala_de_estudo, limpar_sessoes_expiradas  


def menu_principal():  
    inicializar_arquivos_json()  
    limpar_sessoes_expiradas()
    while True:  
        print("\n====================")

        if lista.usuario_logado:
            print(f" LOGADO como ({lista.usuario_logado})")
            print("====================")
            print("1. Perfil")
            print("2. Sala de estudo")
            print("3. Sair da conta")
            print("4. Modo Desenvolvedor")
            print("5. Sessão de Estudo/Registrar presença")
            print("6. Modelo de estudo")
            print("7. Encerrar aplicação")
        else:
            print(" DESCONECTADO")
            print("====================")
            print("1. Cadastrar novo usuário")
            print("2. Fazer Login")
            print("3. Encerrar aplicação")
            print("4. Modo Desenvolvedor")
            print("Sessão de estudo e Modelo de estudo ficarão disponíveis após o login")

        opcao = input("\nSelecione uma opção: ").strip()

        if lista.usuario_logado is not None:
            if opcao == "1":
                menu_perfil()
            elif opcao == "2":
                exibir_sala_de_estudo()
            elif opcao == "3":
                deslogar()
            elif opcao == "4":
                acessar_configuracao_horario()
            elif opcao == "5":
                registro_presenca()
            elif opcao == "6":
                modelo_estudo()
            elif opcao == "7":
                print("Encerrando os estudos, até logo!")
                break
            else:
                print("Opção inválida, tente novamente")

        else:
            if opcao == "1":
                cadastrar_usuario()
            elif opcao == "2":
                realizar_login()
            elif opcao == "3":
                print("Encerrando os estudos, até logo!")
                break
            elif opcao == "4":
                acessar_configuracao_horario()
            else:
                print("Opção inválida, tente novamente")


if __name__ == "__main__":
    menu_principal()
