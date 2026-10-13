from Persistencia import criar_credencial_senha, salvar_json  
from lista import usuarios  


def cadastrar_usuario():  
    print("\n--- TELA DE CADASTRO ---")  
    while True:  
        email = input("Digite seu e-mail: ").strip().lower()  
        if email.endswith("@ufrpe.br") and email.count("@") == 1 and len(email) > 9:  
            print("Email válido!")  
            break  
        print(  
            "Email inválido! Verifique se você está colocando o seu "  
            "email institucional corretamente!"  
        )  

    if any(usuario["email"].lower() == email for usuario in usuarios):  
        print("Erro: Este e-mail já está cadastrado!")  
        return  

    while True:  
        senha = input(  
            "Crie a sua senha no StudyRats! (Ela deve conter de 6 a 8 "  
            "caracteres, uma letra maiúscula, um caractere especial e um numeral): "  
        )  

        if len(senha) < 6:  
            print("Senha inválida! A senha deve ter no mínimo 6 caracteres! Tente novamente.")  
        elif len(senha) > 8:  
            print("Senha inválida! A senha deve ter no máximo 8 caracteres! Tente novamente.")  
        elif not any(letra.isupper() for letra in senha):  
            print("Senha inválida! A senha deve conter pelo menos uma letra maiúscula! Tente novamente.")  
        elif not any(letra.isdigit() for letra in senha):  
            print("Senha inválida! A senha deve conter pelo menos um número! Tente novamente.")  
        elif senha.isalnum():  
            print("Senha inválida! A senha deve conter pelo menos um caractere especial! Tente novamente.")  
        else:  
            print("Senha válida!")  
            break  

    while True:  
        ratname = input("Crie o seu Ratname: ").strip()  
        if not ratname:  
            print("O Ratname não pode ficar vazio.")  
            continue  
        if any(usuario["ratname"].casefold() == ratname.casefold() for usuario in usuarios):  
            print("Erro: Este Ratname já está em uso!")  
            return  
        break  

    novo_usuario = {  
        "email": email,  
        "ratname": ratname,  
        **criar_credencial_senha(senha),  
    }  
    salvar_json("usuarios.json", [*usuarios, novo_usuario])  
    usuarios.append(novo_usuario)  
    print("Cadastro realizado com sucesso!")  
