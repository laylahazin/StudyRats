
# Código do Login do usuário no StudyRats

print('===== STUDYRATS =====')
print('Login do usuário')


def login():

    while True:

        email = input('Digite seu email institucional: ')

        if not email.endswith('@ufrpe.br'):
            print('Verifique se o email está correto!')
        else:
            break

    while True:

        senha = input('Digite sua senha: ')

        if senha != senha_cadastrada:
            print('Senha incorreta, tente novamente!')
        else:
            print('Está pronto para arrebentar hoje?')
            break


def menu():

    print()
    print('===== MENU =====')

    registro = input('Deseja registrar presença? (sim/não): ')

    if registro.lower() == 'sim':
        print('Você será direcionado para o Registro de Presença.')

    else:
        modelo = input('Deseja ir no modelo de estudo? (sim/não): ')

        if modelo.lower() == 'sim':
            print('Você será direcionado para o Modelo de Estudo.')

        else:
            sala = input('Deseja ir na sala de estudo? (sim/não): ')

            if sala.lower() == 'sim':
                print('Você será direcionado para a Sala de Estudo.')

            else:
                comunidades = input('Deseja ir nas comunidades? (sim/não): ')

                if comunidades.lower() == 'sim':
                    print('Você será direcionado para as Comunidades.')

                else:
                    print('Aplicativo encerrado. Até mais!')


# Dados cadastrados pelo usuário
email_cadastrado = input('Digite o email cadastrado: ')
senha_cadastrada = input('Digite a senha cadastrada: ')

print()
print('Agora vamos realizar o login.')

login()
menu()
