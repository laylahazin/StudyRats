from Persistencia import criar_credencial_senha, salvar_json  # gera credenciais protegidas e grava o cadastro no arquivo JSON
from lista import usuarios  # usa a lista compartilhada de contas existentes


def cadastrar_usuario():  # coleta e valida os dados necessários para criar uma nova conta
    print("\n--- TELA DE CADASTRO ---")  # identifica a tela de cadastro
    while True:  # solicita novamente o e-mail até receber um endereço institucional válido
        email = input("Digite seu e-mail: ").strip().lower()  # lê o endereço e normaliza espaços e letras maiúsculas
        if email.endswith("@ufrpe.br") and email.count("@") == 1 and len(email) > 9:  # exige domínio institucional e um único separador @
            print("Email válido!")  # confirma que o formato básico do endereço passou pela validação
            break  # encerra o laço para prosseguir com os dados da conta
        print(  # explica por que o endereço não foi aceito
            "Email inválido! Verifique se você está colocando o seu "  # inicia a orientação para revisar o endereço
            "email institucional corretamente!"  # informa que o domínio institucional é obrigatório
        )  # finaliza a mensagem de validação

    if any(usuario["email"].lower() == email for usuario in usuarios):  # procura um cadastro anterior com o mesmo e-mail normalizado
        print("Erro: Este e-mail já está cadastrado!")  # impede que o mesmo endereço seja associado a outra conta
        return  # interrompe o cadastro duplicado e volta ao menu

    while True:  # repete a solicitação até que a senha satisfaça todas as regras
        senha = input(  # coleta a senha sem armazená-la em texto puro no arquivo
            "Crie a sua senha no StudyRats! (Ela deve conter de 6 a 8 "  # explica o intervalo de tamanho exigido
            "caracteres, uma letra maiúscula, um caractere especial e um numeral): "  # lista os tipos de caractere exigidos
        )  # conclui a leitura da senha digitada

        if len(senha) < 6:  # rejeita senhas menores que o tamanho mínimo definido pelo sistema
            print("Senha inválida! A senha deve ter no mínimo 6 caracteres! Tente novamente.")  # mostra o requisito que falhou
        elif len(senha) > 8:  # rejeita senhas que ultrapassam o tamanho máximo definido
            print("Senha inválida! A senha deve ter no máximo 8 caracteres! Tente novamente.")  # explica o limite superior permitido
        elif not any(letra.isupper() for letra in senha):  # verifica se existe ao menos uma letra maiúscula
            print("Senha inválida! A senha deve conter pelo menos uma letra maiúscula! Tente novamente.")  # pede a inclusão de uma maiúscula
        elif not any(letra.isdigit() for letra in senha):  # verifica se existe ao menos um caractere numérico
            print("Senha inválida! A senha deve conter pelo menos um número! Tente novamente.")  # pede a inclusão de um numeral
        elif senha.isalnum():  # rejeita a senha quando todos os caracteres são letras ou números
            print("Senha inválida! A senha deve conter pelo menos um caractere especial! Tente novamente.")  # pede a inclusão de pontuação ou símbolo
        else:  # alcança este ramo quando a senha satisfez todos os critérios anteriores
            print("Senha válida!")  # confirma que a senha pode ser usada para criar credenciais
            break  # encerra a validação e segue para a escolha do Ratname

    while True:  # solicita um nome público até que ele seja preenchido e esteja disponível
        ratname = input("Crie o seu Ratname: ").strip()  # lê o identificador e remove espaços externos
        if not ratname:  # impede que uma conta seja criada sem identificador
            print("O Ratname não pode ficar vazio.")  # informa que o campo é obrigatório
            continue  # solicita outro Ratname sem prosseguir ao salvamento
        if any(usuario["ratname"].casefold() == ratname.casefold() for usuario in usuarios):  # compara nomes sem diferenciar maiúsculas e minúsculas
            print("Erro: Este Ratname já está em uso!")  # informa que o identificador pertence a outra conta
            return  # cancela o cadastro para evitar nomes de usuário duplicados
        break  # aceita o Ratname e encerra o laço de validação

    novo_usuario = {  # monta o registro que será guardado para a nova conta
        "email": email,  # associa o e-mail institucional validado à conta
        "ratname": ratname,  # associa o identificador público escolhido pelo usuário
        **criar_credencial_senha(senha),  # inclui salt e hash derivados sem persistir a senha original
    }  # conclui o dicionário completo do novo usuário
    salvar_json("usuarios.json", [*usuarios, novo_usuario])  # grava a lista atual junto com a conta recém-criada
    usuarios.append(novo_usuario)  # atualiza a lista carregada em memória para a sessão atual
    print("Cadastro realizado com sucesso!")  # confirma a criação da conta ao usuário
