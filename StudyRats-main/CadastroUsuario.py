import lista
from Dados import gerenciador_credenciais, persistencia


class CadastroUsuario:
    def __init__(self) -> None:
        self.estado = lista.estado
        self.persistencia = persistencia
        self.gerenciador_credenciais = gerenciador_credenciais

    def cadastrar(self) -> None:
        print("\n===== TELA DE CADASTRO =====")
        email = self._ler_email()
        if any(usuario["email"].lower() == email for usuario in self.estado.usuarios):
            print("Erro: Este e-mail já está cadastrado!")
            return

        tipo_usuario = self._ler_tipo_usuario()
        senha = self._ler_senha()
        ratname = self._ler_ratname()
        if ratname is None:
            return

        novo_usuario = {
            "email": email,
            "ratname": ratname,
            "tipo_usuario": tipo_usuario,
            **self.gerenciador_credenciais.criar(senha),
        }
        usuarios_atualizados = [*self.estado.usuarios, novo_usuario]
        self.persistencia.salvar("usuarios.json", usuarios_atualizados)
        self.estado.usuarios.append(novo_usuario)
        print("Cadastro realizado com sucesso!")

    def _ler_email(self) -> str:
        while True:
            email = input("Digite seu e-mail institucional: ").strip().lower()
            if email.endswith("@ufrpe.br") and email.count("@") == 1 and len(email) > 9:
                print("Email válido!")
                return email
            print(
                "Email inválido! Verifique se você está colocando o seu "
                "email institucional corretamente!"
            )

    def _ler_tipo_usuario(self) -> str:
        while True:
            print("Tipo de conta:")
            print("1. ESTUDANTE")
            print("2. MONITOR")
            escolha = input("Escolha o tipo de conta: ").strip().upper()
            if escolha in ("1", self.estado.TIPO_ESTUDANTE):
                return self.estado.TIPO_ESTUDANTE
            if escolha in ("2", self.estado.TIPO_MONITOR):
                return self.estado.TIPO_MONITOR
            print("Opção inválida. Escolha ESTUDANTE ou MONITOR.")

    def _ler_senha(self) -> str:
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
                return senha

    def _ler_ratname(self) -> str | None:
        while True:
            ratname = input("Crie o seu Ratname: ").strip()
            if not ratname:
                print("O Ratname não pode ficar vazio.")
                continue
            if any(
                usuario["ratname"].casefold() == ratname.casefold()
                for usuario in self.estado.usuarios
            ):
                print("Erro: Este Ratname já está em uso!")
                return None
            return ratname
