import lista  
from CadastroUsuario import cadastrar_usuario  
from Horario import configurar_horario  
from LoginUsuario import realizar_login, deslogar  
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
            print(f" Status: LOGADO como ({lista.usuario_logado})")  
            print("====================")  
            print("1. Perfil")  
            print("2. Sala de estudo")  
            print("3. Sair da conta (Logoff)")  
            print("4. Configurar horário de teste")  
            print("5. Sessão de Estudo - Registrar presença")  
            print("6. Modelo de estudo")  
            print("7. Encerrar aplicação")  
        else:  
            print(" Status: DESCONECTADO")  
            print("====================")  
            print("1. Cadastrar novo usuário")  
            print("2. Fazer Login")  
            print("3. Encerrar aplicação")  
            print("4. Configurar horário de teste")  
            print("Registro de presença e Modelo de estudo ficam disponíveis após o login.")  

        opcao = input("\nEscolha uma opção: ").strip()  

        
        if lista.usuario_logado is not None:  
            if opcao == "1":  
                print(f"\nBem-vindo(a), {lista.usuario_logado}!")  
            elif opcao == "2":  
                exibir_sala_de_estudo()  
            elif opcao == "3":  
                deslogar()  
            elif opcao == "4":  
                configurar_horario()  
            elif opcao == "5":  
                registro_presenca()  
            elif opcao == "6":  
                modelo_estudo()  
            elif opcao == "7":  
                print("Encerrando a aplicação. Até logo!")  
                break  
            else:  
                print("Opção inválida, tente novamente.")  

        
        else:  
            if opcao == "1":  
                cadastrar_usuario()  
            elif opcao == "2":  
                realizar_login()  
            elif opcao == "3":  
                print("Encerrando a aplicação. Até logo!")  
                break  
            elif opcao == "4":  
                configurar_horario()  
            else:  
                print("Opção inválida, tente novamente.")  


if __name__ == "__main__":  
    menu_principal()  
