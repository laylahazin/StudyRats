# Código do cadastro do usuário no StudyRats

print('Seja bem-vindo ao StudyRats!')
print('Precisamos que você digite o seu email institucional.')


def funcao_email():

    while True:
        email = input('Digite o seu email institucional: ')

        if email.endswith('@ufrpe.br'):
            print('Email válido!')
            break
        else:
            print('Email inválido! Verifique se você está colocando o seu email institucional!')


def ratname():

    while True:
        ratname = input('Crie o seu Ratname: ')

        jaexistente = False

        if ratname == '':
            print('Ratname inválido! Digite um Ratname.')
        elif jaexistente == True:
            print('Ratname já existente! Crie outro Ratname.')
        else:
            print('Seu Ratname é válido!')
            break


def senha():

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


funcao_email()
ratname()
senha()

print()
print('Cadastro realizado com sucesso!')
print('Seus dados foram salvos.')

login = input('Você deseja realizar o login? (sim/não): ')

if login.lower() == 'sim':
    print('Você será direcionado para o login do usuário.')
    # O código da segunda funcionalidade será colocado aqui.
else:
    print('Aplicativo encerrado. Até mais!')
