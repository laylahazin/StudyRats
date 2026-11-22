import lista  # Importa lista: importa o estado central da aplicacao.
from Dados import gerenciador_credenciais, persistencia  # Importa de Dados gerenciador_credenciais, persistencia, reutilizando os recursos centrais de persistencia e credenciais.


class CadastroUsuario:  # Declara a classe CadastroUsuario: coleta, valida e salva novas contas.
    def __init__(self) -> None:  # Declara o metodo __init__: implementa esta funcionalidade da classe.
        self.estado = lista.estado  # Guarda em self.estado o valor produzido por lista.estado.
        self.persistencia = persistencia  # Guarda em self.persistencia o valor produzido por persistencia.
        self.gerenciador_credenciais = gerenciador_credenciais  # Guarda em self.gerenciador_credenciais o valor produzido por gerenciador_credenciais.

    def cadastrar(self) -> None:  # Declara o metodo cadastrar: coleta os dados da nova conta, valida duplicidade e persiste a conta.
        print("\n===== TELA DE CADASTRO =====")  # Exibe no terminal ===== TELA DE CADASTRO =====.
        email = self._ler_email()  # guarda o e-mail normalizado usado para cadastrar ou localizar a conta
        if any(usuario["email"].lower() == email for usuario in self.estado.usuarios):  # Testa a condicao any(usuario["email"].lower() == email for usuario in self.estado.usuarios) e executa o bloco seguinte somente quando ela for verdadeira.
            print("Erro: Este e-mail já está cadastrado!")  # Exibe no terminal Erro: Este e-mail já está cadastrado!.
            return  # Encerra este metodo imediatamente sem devolver valor.

        tipo_usuario = self._ler_tipo_usuario()  # registra ESTUDANTE ou MONITOR para controlar os recursos disponiveis
        senha = self._ler_senha()  # Guarda em senha o valor produzido por self._ler_senha().
        ratname = self._ler_ratname()  # guarda o nome publico usado como identificador da conta nos modulos da aplicacao
        if ratname is None:  # Verifica que nao existe usuario conectado; o bloco impede acesso aos dados pessoais.
            return  # Encerra este metodo imediatamente sem devolver valor.

        novo_usuario = {  # monta o registro completo da nova conta com identidade e credenciais
            "email": email,  # Na chave "email", guarda o e-mail institucional usado para cadastro e login; nesta entrada recebe email,.
            "ratname": ratname,  # Na chave "ratname", guarda o nome publico usado como chave entre conta, modelos e recompensas; nesta entrada recebe ratname,.
            "tipo_usuario": tipo_usuario,  # Na chave "tipo_usuario", distingue estudante de monitor e define menus correspondentes; nesta entrada recebe tipo_usuario,.
            **self.gerenciador_credenciais.criar(senha),  # Continua a expressao anterior pelo operador ou elemento **self.gerenciador_credenciais.criar(senha),.
        }  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        usuarios_atualizados = [*self.estado.usuarios, novo_usuario]  # cria a nova lista de contas contendo esta alteracao, sem perder os demais usuarios
        self.persistencia.salvar("usuarios.json", usuarios_atualizados)  # Persiste no arquivo JSON indicado o novo estado da estrutura atual.
        self.estado.usuarios.append(novo_usuario)  # Executa self.estado.usuarios.append(novo_usuario); o efeito desta chamada participa diretamente desta funcionalidade.
        print("Cadastro realizado com sucesso!")  # Exibe no terminal Cadastro realizado com sucesso!.

    def _ler_email(self) -> str:  # Declara o metodo _ler_email: repete a coleta ate obter um e-mail institucional UFRPE valido.
        while True:  # Mantem o loop ativo ate encontrar uma opcao que devolva ou encerre o fluxo.
            email = input("Digite seu e-mail institucional: ").strip().lower()  # guarda o e-mail normalizado usado para cadastrar ou localizar a conta
            if email.endswith("@ufrpe.br") and email.count("@") == 1 and len(email) > 9:  # Testa a condicao email.endswith("@ufrpe.br") and email.count("@") == 1 and len(email) > 9 e executa o bloco seguinte somente quando ela for verdadeira.
                print("Email válido!")  # Exibe no terminal Email válido!.
                return email  # Encerra o metodo e devolve ao chamador email.
            print(  # Escreve no terminal o conteudo preparado por esta chamada.
                "Email inválido! Verifique se você está colocando o seu "  # Executa nesta linha "Email inválido! Verifique se você está colocando o seu " no contexto desta funcionalidade.
                "email institucional corretamente!"  # Executa nesta linha "email institucional corretamente!" no contexto desta funcionalidade.
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

    def _ler_tipo_usuario(self) -> str:  # Declara o metodo _ler_tipo_usuario: converte a escolha em ESTUDANTE ou MONITOR.
        while True:  # Mantem o loop ativo ate encontrar uma opcao que devolva ou encerre o fluxo.
            print("Tipo de conta:")  # Exibe no terminal Tipo de conta:.
            print("1. ESTUDANTE")  # Exibe no terminal 1. ESTUDANTE.
            print("2. MONITOR")  # Exibe no terminal 2. MONITOR.
            escolha = input("Escolha o tipo de conta: ").strip().upper()  # guarda a opcao digitada no menu atual
            if escolha in ("1", self.estado.TIPO_ESTUDANTE):  # Aceita 1 ou ESTUDANTE como escolha da conta de estudante.
                return self.estado.TIPO_ESTUDANTE  # Encerra o metodo e devolve ao chamador self.estado.TIPO_ESTUDANTE.
            if escolha in ("2", self.estado.TIPO_MONITOR):  # Aceita 2 ou MONITOR como escolha da conta de monitor.
                return self.estado.TIPO_MONITOR  # Encerra o metodo e devolve ao chamador self.estado.TIPO_MONITOR.
            print("Opção inválida. Escolha ESTUDANTE ou MONITOR.")  # Exibe no terminal Opção inválida. Escolha ESTUDANTE ou MONITOR..

    def _ler_senha(self) -> str:  # Declara o metodo _ler_senha: valida comprimento, maiuscula, numero e caractere especial da senha.
        while True:  # Mantem o loop ativo ate encontrar uma opcao que devolva ou encerre o fluxo.
            senha = input(  # Guarda em senha o valor produzido por input(.
                "Crie a sua senha no StudyRats! (Ela deve conter de 6 a 8 "  # Executa nesta linha "Crie a sua senha no StudyRats! (Ela deve conter de 6 a 8 " no contexto desta funcionalidade.
                "caracteres, uma letra maiúscula, um caractere especial e um numeral): "  # Executa nesta linha "caracteres, uma letra maiúscula, um caractere especial e um numeral): " no contexto desta funcionalidade.
            )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

            if len(senha) < 6:  # Testa a condicao len(senha) < 6 e executa o bloco seguinte somente quando ela for verdadeira.
                print("Senha inválida! A senha deve ter no mínimo 6 caracteres! Tente novamente.")  # Exibe no terminal Senha inválida! A senha deve ter no mínimo 6 caracteres! Tente novamente..
            elif len(senha) > 8:  # Testa a alternativa len(senha) > 8 somente depois que as condicoes anteriores falharam.
                print("Senha inválida! A senha deve ter no máximo 8 caracteres! Tente novamente.")  # Exibe no terminal Senha inválida! A senha deve ter no máximo 8 caracteres! Tente novamente..
            elif not any(letra.isupper() for letra in senha):  # Exige pelo menos uma letra maiuscula na senha.
                print("Senha inválida! A senha deve conter pelo menos uma letra maiúscula! Tente novamente.")  # Exibe no terminal Senha inválida! A senha deve conter pelo menos uma letra maiúscula! Tente novamente..
            elif not any(letra.isdigit() for letra in senha):  # Exige pelo menos um digito numerico na senha.
                print("Senha inválida! A senha deve conter pelo menos um número! Tente novamente.")  # Exibe no terminal Senha inválida! A senha deve conter pelo menos um número! Tente novamente..
            elif senha.isalnum():  # Rejeita uma senha sem caractere especial; letras e numeros sozinhos nao bastam.
                print("Senha inválida! A senha deve conter pelo menos um caractere especial! Tente novamente.")  # Exibe no terminal Senha inválida! A senha deve conter pelo menos um caractere especial! Tente novamente..
            else:  # Executa este bloco quando nenhuma condicao anterior da cadeia foi atendida.
                print("Senha válida!")  # Exibe no terminal Senha válida!.
                return senha  # Encerra o metodo e devolve ao chamador senha.

    def _ler_ratname(self) -> str | None:  # Declara o metodo _ler_ratname: rejeita Ratname vazio ou ja usado por outra conta.
        while True:  # Mantem o loop ativo ate encontrar uma opcao que devolva ou encerre o fluxo.
            ratname = input("Crie o seu Ratname: ").strip()  # guarda o nome publico usado como identificador da conta nos modulos da aplicacao
            if not ratname:  # Testa a condicao not ratname e executa o bloco seguinte somente quando ela for verdadeira.
                print("O Ratname não pode ficar vazio.")  # Exibe no terminal O Ratname não pode ficar vazio..
                continue  # Pula o restante da iteracao atual e volta ao inicio da proxima repeticao.
            if any(  # Testa a condicao any( e executa o bloco seguinte somente quando ela for verdadeira.
                usuario["ratname"].casefold() == ratname.casefold()  # Executa nesta linha usuario["ratname"].casefold() == ratname.casefold() no contexto desta funcionalidade.
                for usuario in self.estado.usuarios  # Percorre usuario in self.estado.usuarios, executando o bloco uma vez para cada elemento.
            ):  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                print("Erro: Este Ratname já está em uso!")  # Exibe no terminal Erro: Este Ratname já está em uso!.
                return None  # Encerra o metodo e devolve ao chamador None.
            return ratname  # Encerra o metodo e devolve ao chamador ratname.
