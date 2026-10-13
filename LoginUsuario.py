import lista  
from Persistencia import verificar_senha  


def realizar_login():  
    print("\n--- TELA DE LOGIN ---")  
    email = input("Digite seu e-mail: ").strip().lower()  
    senha = input("Digite sua senha: ")  

    for usuario in lista.usuarios:  
        if usuario["email"].lower() != email:
            continue  

        if "senha_hash" not in usuario or "senha_salt" not in usuario:  
            raise ValueError(  
                "A conta salva não possui credenciais compatíveis. "  
                "Remova-a ou faça a migração antes de tentar entrar."  
            )  

        if verificar_senha(senha, usuario["senha_salt"], usuario["senha_hash"]):  
            lista.usuario_logado = usuario["ratname"]  
            print(f"\nLogin bem-sucedido! Você está conectado como: {lista.usuario_logado}")  
            return  
        break  

    print("\nErro: E-mail ou senha incorretos.")  


def deslogar():  
    print(f"\nSaindo da conta de {lista.usuario_logado}...")  
    lista.usuario_logado = None  
    print("Você saiu da conta com sucesso!")  
