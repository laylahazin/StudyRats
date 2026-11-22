from datetime import datetime

from Dados import persistencia


class GerenciadorHorario:
    ARQUIVO_CONFIGURACAO = "configuracao_horario.json"
    SENHA_ADMIN_HORARIO = "BSISTUDYRAT"

    def __init__(self) -> None:
        self.persistencia = persistencia

    def obter_horario_atual(self) -> datetime:
        configuracao = self._carregar_configuracao()
        modo = configuracao.get("modo")
        if modo == "automatico":
            return datetime.now()
        if modo == "manual":
            valor = configuracao.get("data_hora_manual")
            if not isinstance(valor, str):
                raise ValueError("O horário manual salvo está inválido.")
            try:
                return datetime.fromisoformat(valor)
            except ValueError as erro:
                raise ValueError("O horário manual salvo está inválido.") from erro

        raise ValueError("O modo de horário salvo é inválido.")

    def acessar_configuracao(self) -> None:
        print("\n=== ADMINISTRAÇÃO ===")
        senha = input("Digite a senha de administrador para ajustar o horário: ").strip()
        if senha != self.SENHA_ADMIN_HORARIO:
            print("Acesso negado. Você não tem permissão para alterar o horário do sistema")
            return

        self.configurar()

    def configurar(self) -> None:
        while True:
            horario_atual = self.obter_horario_atual()
            modo = "manual" if self._modo_manual_ativo() else "automático"
            print(f"\n=== HORÁRIO DO SISTEMA ({modo}) ===")
            print(f"Horário considerado: {horario_atual:%d/%m/%Y %H:%M}")
            print("1. Definir data e horário manual para testes")
            print("2. Voltar ao horário automático do sistema")
            print("0. Voltar ao menu principal")

            opcao = input("Escolha uma opção: ").strip()
            if opcao == "1":
                texto_data = input("Informe a data de teste (DD/MM/AAAA): ").strip()
                texto_horario = input("Informe o horário de teste (HH:MM): ").strip()
                try:
                    data = datetime.strptime(texto_data, "%d/%m/%Y").date()
                    horario = datetime.strptime(texto_horario, "%H:%M").time()
                except ValueError:
                    print(
                        "Data ou horário inválido. Use DD/MM/AAAA e HH:MM, "
                        "por exemplo 01/08/2026 e 18:30."
                    )
                    continue

                horario_manual = datetime.combine(data, horario)
                self.persistencia.salvar(
                    self.ARQUIVO_CONFIGURACAO,
                    {
                        "modo": "manual",
                        "data_hora_manual": horario_manual.isoformat(timespec="minutes"),
                    },
                )
                print(
                    f"Horário de teste definido para "
                    f"{horario_manual:%d/%m/%Y %H:%M}. Data e horário "
                    "permanecerão fixos até você selecionar o modo automático."
                )

            elif opcao == "2":
                self.persistencia.salvar(
                    self.ARQUIVO_CONFIGURACAO,
                    {"modo": "automatico", "data_hora_manual": None},
                )
                print("Horário automático do sistema restaurado")
                return

            elif opcao == "0":
                return

            else:
                print("Opção inválida, tente novamente")

    def _carregar_configuracao(self) -> dict:
        configuracao = self.persistencia.carregar(
            self.ARQUIVO_CONFIGURACAO,
            {"modo": "automatico", "data_hora_manual": None},
        )
        if not isinstance(configuracao, dict):
            raise ValueError("A configuração do horário deve ser um objeto JSON.")
        return configuracao

    def _modo_manual_ativo(self) -> bool:
        return self._carregar_configuracao().get("modo") == "manual"

    def modo_manual_ativo(self) -> bool:
        return self._modo_manual_ativo()
