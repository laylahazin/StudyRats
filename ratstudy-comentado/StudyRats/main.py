import lista  # importa o estado compartilhado de usuários, salas e conta conectada
from CadastroUsuario import cadastrar_usuario  # importa a rotina para criar uma conta nova
from Horario import configurar_horario  # importa a opção que ajusta o relógio usado em testes
from LoginUsuario import realizar_login, deslogar  # importa as ações de entrar e sair da conta
from ModeloEstudo import modelo_estudo  # Conecta a escolha do plano de estudos ao menu.
from Persistencia import inicializar_arquivos_json  # importa a criação dos arquivos JSON necessários
from RegistroPresenca import registro_presenca  # Conecta o registro de sessões ao menu.
from SalaEstudo import exibir_sala_de_estudo, limpar_sessoes_expiradas  # importa o acesso às salas e a limpeza de sessões vencidas


def menu_principal():  # define o ponto principal de interação e mantém o menu aberto
    inicializar_arquivos_json()  # cria os arquivos de dados ausentes com os valores iniciais
    limpar_sessoes_expiradas()  # remove registros de salas cujo horário já terminou
    while True:  # repete o menu até que o usuário escolha encerrar a aplicação
        print("\n====================")  # separa visualmente uma iteração do menu

        if lista.usuario_logado:  # mostra ações restritas quando há um Ratname conectado
            print(f" Status: LOGADO como ({lista.usuario_logado})")  # identifica a conta atualmente autenticada
            print("====================")  # separa o status das opções disponíveis
            print("1. Perfil")  # oferece a visualização do perfil da conta
            print("2. Sala de estudo")  # oferece o acesso às salas compartilhadas
            print("3. Sair da conta (Logoff)")  # permite encerrar a sessão autenticada
            print("4. Configurar horário de teste")  # abre a configuração do relógio de teste
            print("5. Sessão de Estudo - Registrar presença")  # oferece o registro autenticado de uma sessão de estudo
            print("6. Modelo de estudo")  # oferece a seleção ou criação de um cronograma
            print("7. Encerrar aplicação")  # oferece o encerramento do programa
        else:  # mostra as ações acessíveis antes de autenticar uma conta
            print(" Status: DESCONECTADO")  # informa que ainda não há usuário conectado
            print("====================")  # separa o status das opções disponíveis
            print("1. Cadastrar novo usuário")  # oferece o cadastro de uma conta
            print("2. Fazer Login")  # oferece a autenticação de uma conta existente
            print("3. Encerrar aplicação")  # permite sair sem iniciar sessão
            print("4. Configurar horário de teste")  # mantém a configuração de horário acessível durante testes
            print("Registro de presença e Modelo de estudo ficam disponíveis após o login.")  # explica por que as opções autenticadas não aparecem

        opcao = input("\nEscolha uma opção: ").strip()  # lê a opção e remove espaços acidentais nas extremidades

        # --- Encaminha as opções exibidas para usuários autenticados ---
        if lista.usuario_logado is not None:  # verifica novamente o estado da sessão para decidir qual menu processar
            if opcao == "1":  # reconhece a opção de perfil
                print(f"\nBem-vindo(a), {lista.usuario_logado}!")  # apresenta o Ratname conectado
            elif opcao == "2":  # reconhece a opção de sala de estudo
                exibir_sala_de_estudo()  # inicia o fluxo de entrada e participação em salas
            elif opcao == "3":  # reconhece a opção de logoff
                deslogar()  # limpa o usuário conectado e retorna ao menu desconectado
            elif opcao == "4":  # reconhece a configuração de horário de teste
                configurar_horario()  # abre o fluxo para ajustar ou restaurar o relógio
            elif opcao == "5":  # reconhece o registro de presença
                registro_presenca()  # inicia o cronômetro e salva a sessão da conta conectada
            elif opcao == "6":  # reconhece a escolha de modelo de estudo
                modelo_estudo()  # exibe e salva o cronograma selecionado
            elif opcao == "7":  # reconhece o pedido para encerrar o programa
                print("Encerrando a aplicação. Até logo!")  # confirma o encerramento ao usuário
                break  # termina o laço principal do menu
            else:  # trata qualquer entrada que não corresponda às opções autenticadas
                print("Opção inválida, tente novamente.")  # solicita uma escolha válida sem encerrar o menu

        # --- Encaminha as opções exibidas para usuários desconectados ---
        else:  # processa apenas cadastro, login, horário de teste e encerramento
            if opcao == "1":  # reconhece a opção de cadastro
                cadastrar_usuario()  # solicita os dados e persiste a nova conta
            elif opcao == "2":  # reconhece a opção de login
                realizar_login()  # valida as credenciais e atualiza o estado compartilhado
            elif opcao == "3":  # reconhece o pedido para encerrar o programa
                print("Encerrando a aplicação. Até logo!")  # confirma o encerramento ao usuário
                break  # termina o laço principal do menu
            elif opcao == "4":  # reconhece a configuração de horário de teste
                configurar_horario()  # abre o fluxo para ajustar ou restaurar o relógio
            else:  # trata qualquer entrada que não corresponda às opções desconectadas
                print("Opção inválida, tente novamente.")  # solicita uma escolha válida sem encerrar o menu


if __name__ == "__main__":  # executa o menu somente quando este arquivo é iniciado diretamente
    menu_principal()  # inicia o fluxo interativo do StudyRats
