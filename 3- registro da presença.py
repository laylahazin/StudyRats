# Código do Registro de Presença do StudyRats


def registro_presenca():

    print()
    print('===== REGISTRO DE PRESENÇA =====')
    print()

    # Verifica se já existe um check-in em andamento

    checkin_andamento = input('Você já possui um check-in em andamento? (sim/não): ')

    if checkin_andamento.lower() == 'sim':

        print('Muito bem, você já está em uma missão em andamento.')
        return


    # Usuário escolhe a disciplina ou assunto

    disciplina = input('Digite a disciplina ou assunto que você vai estudar: ')

    if disciplina == '':

        print('Você precisa informar uma disciplina ou assunto.')
        print('Não esqueça de confirmar a sua presença diária hoje!')
        return


    print()
    print('Sua presença será associada à disciplina:', disciplina)
    print()


    # Usuário confirma o início do cronômetro

    iniciar = input('Deseja iniciar o cronômetro? (sim/não): ')

    if iniciar.lower() != 'sim':

        print()
        print('Não esqueça de confirmar a sua presença diária hoje!')
        print('Você retornará ao menu principal.')
        return


    # Início da sessão de estudo

    print()
    print('Cronômetro iniciado!')
    print('Você está estudando:', disciplina)
    print()


    # Usuário finaliza a sessão de estudo

    finalizar = input('Digite "finalizar" quando terminar sua sessão de estudo: ')


    if finalizar.lower() == 'finalizar':

        print()
        print('Sessão de estudo finalizada!')
        print('Atividade registrada!')
        print('Check-in salvo com sucesso!')
        print()
        print('Sua presença hoje foi confirmada na comunidade Rat.')
        print()
        print('Você será direcionado para o Menu.')


    else:

        print()
        print('Sessão não finalizada.')
        print('Não esqueça de confirmar a sua presença diária hoje!')
        print('Você retornará ao menu principal.')


# Inicia o Registro de Presença

registro_presenca()