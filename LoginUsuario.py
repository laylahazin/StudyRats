import lista
from Persistencia import carregar_json, salvar_json, verificar_senha 


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


def excluir_conta():
    if lista.usuario_logado is None:
        print("\nVocê precisa estar conectado para excluir a conta.") 
        return 

    usuario = next(  # busca a conta correspondente ao ratname que representa a sessão atualmente autenticada, o next é usado para obter o primeiro item que satisfaz a condição, sem criar uma lista completa
        (item for item in lista.usuarios if item["ratname"] == lista.usuario_logado),
        None,  # vai usar none como resultado quando o estado de login não corresponde a uma conta carregada
    ) 
    if usuario is None: 
        print("\nConta não encontrada para exclusão.") 
        lista.usuario_logado = None 
        return

    lista.usuarios = [  # vai atualizar a lista pra tirar a conta do usuário logado
        item for item in lista.usuarios if item["ratname"] != lista.usuario_logado 
    ]  
    salvar_json("usuarios.json", lista.usuarios)  

    planos = carregar_json("modelos_estudo.json", {})  # vai recuperar os planos de estudo do usuario antes de remover a conta, pra que os dados nao fiquem sem dono
    if isinstance(planos, dict):  # o isinstance vai fazer com que a aplicação só tente remover o plano se a estrutura do arquivo for a normal
        planos.pop(lista.usuario_logado, None)  # o pop é pra remover o plano do usuário logado, se existir, e não falha se não tiver plano
        salvar_json("modelos_estudo.json", planos)  

    presencas = carregar_json("presencas.json", {})  # mesma coisa mas agora com sessoes de estudo
    if isinstance(presencas, dict):
        presencas.pop(lista.usuario_logado, None)  
        salvar_json("presencas.json", presencas)  

    print(f"\nA conta de {lista.usuario_logado} foi excluída com sucesso.") 
    lista.usuario_logado = None  # finaliza a sessão de usuario


def menu_perfil(): 
    if lista.usuario_logado is None:  
        print("\nVocê precisa fazer login para acessar o perfil.")  
        return  

    while True: 
        print(f"\n=== PERFIL: {lista.usuario_logado} ===")  
        print("1. Excluir conta")  
        print("0. Voltar") 
        escolha = input("Escolha uma opção: ").strip()  

        if escolha == "1":  
            confirmacao = input("Digite EXCLUIR para confirmar a remoção da sua conta: ").strip()  
            if confirmacao != "EXCLUIR":  
                print("Exclusão cancelada. Sua conta foi mantida.") 
                return  
            excluir_conta()  
            return  

        if escolha == "0":  
            return 

        print("Opção inválida, tente novamente.")


def deslogar():
    print(f"\nSaindo da conta de {lista.usuario_logado}...")
    lista.usuario_logado = None
    print("Você saiu da conta com sucesso!")
