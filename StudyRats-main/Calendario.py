import calendar
from datetime import datetime

import lista
from Dados import persistencia
from Horario import GerenciadorHorario


class GerenciadorCalendario:
    ARQUIVO = "calendario.json"
    MESES = (
        "janeiro",
        "fevereiro",
        "março",
        "abril",
        "maio",
        "junho",
        "julho",
        "agosto",
        "setembro",
        "outubro",
        "novembro",
        "dezembro",
    )

    def __init__(self, horario: GerenciadorHorario | None = None) -> None:
        self.estado = lista.estado
        self.persistencia = persistencia
        self.horario = horario or GerenciadorHorario()

    def menu(self) -> None:
        if self._usuario_atual() is None:
            return
        while True:
            self.verificar_lembretes()
            print("\n========== CALENDÁRIO ==========")
            print(f"1. Visualizar calendário desse mês ({self.MESES[self.horario.obter_horario_atual().month - 1]})")
            print("2. Ver meus compromissos")
            print("3. Adicionar compromisso")
            print("4. Editar compromisso")
            print("5. Excluir compromisso")
            print("0. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ").strip()
            acoes = {
                "1": self.visualizar_calendario,
                "2": self.listar_compromissos,
                "3": self.adicionar_compromisso,
                "4": self.editar_compromisso,
                "5": self.excluir_compromisso,
            }
            if opcao == "0":
                return
            acao = acoes.get(opcao)
            if acao is None:
                print("Opção inválida. Tente novamente.")
            else:
                acao()

    def _carregar(self) -> dict:
        calendario = self.persistencia.carregar(self.ARQUIVO, {})
        if not isinstance(calendario, dict):
            raise ValueError("O arquivo calendario.json deve conter um objeto JSON.")
        return calendario

    def _compromissos_usuario(self, calendario: dict) -> list[dict]:
        ratname = self._usuario_atual()
        if ratname is None:
            return []
        compromissos = calendario.setdefault(ratname, [])
        if not isinstance(compromissos, list) or not all(
            isinstance(item, dict) for item in compromissos
        ):
            raise ValueError(f"Os compromissos de '{ratname}' estão inválidos.")
        for compromisso in compromissos:
            for campo in ("materia", "descricao", "data", "hora"):
                if not isinstance(compromisso.get(campo), str):
                    raise ValueError(f"Um compromisso de '{ratname}' está inválido.")
            self._data_hora(compromisso)
        return compromissos

    def listar_compromissos(self) -> None:
        calendario = self._carregar()
        compromissos = self._compromissos_usuario(calendario)
        ordenados = sorted(compromissos, key=self._data_hora)
        print("\n===== MEUS COMPROMISSOS =====")
        if not ordenados:
            print("Você ainda não possui compromissos cadastrados.")
            return
        for indice, compromisso in enumerate(ordenados, start=1):
            print(f"\n{indice}. {compromisso['materia']}")
            print(f"Descrição: {compromisso['descricao']}")
            print(f"Data: {compromisso['data']}")
            print(f"Horário: {compromisso['hora']}")

    def adicionar_compromisso(self) -> None:
        calendario = self._carregar()
        compromissos = self._compromissos_usuario(calendario)
        print("\n===== ADICIONAR ESTUDO AO CALENDÁRIO =====")
        materia = input("Qual matéria você vai estudar? ").strip()
        descricao = input("Descrição do estudo: ").strip()
        data = input("Data (DD/MM/AAAA): ").strip()
        hora = input("Horário (HH:MM): ").strip()
        if not materia or not descricao:
            print("Preencha a matéria e a descrição.")
            return
        try:
            data_hora = self._interpretar_data_hora(data, hora)
        except ValueError:
            print("Data ou horário inválido. Use DD/MM/AAAA e HH:MM.")
            return
        if data_hora < self.horario.obter_horario_atual():
            print("Não é possível cadastrar um estudo em uma data passada.")
            return
        compromissos.append(
            {
                "materia": materia,
                "descricao": descricao,
                "data": data_hora.strftime("%d/%m/%Y"),
                "hora": data_hora.strftime("%H:%M"),
                "lembrete_exibido": False,
            }
        )
        self.persistencia.salvar(self.ARQUIVO, calendario)
        print("\nCompromisso adicionado ao calendário com sucesso!")

    def visualizar_calendario(self) -> None:
        compromissos = self._compromissos_usuario(self._carregar())
        agora = self.horario.obter_horario_atual()
        print("\n========== MEU CALENDÁRIO RAT ==========")
        print(f"{self.MESES[agora.month - 1].capitalize()} de {agora.year}")
        print("SEG  TER  QUA  QUI  SEX  SAB  DOM")
        dias_com_compromisso = {
            self._data_hora(compromisso).day
            for compromisso in compromissos
            if self._data_hora(compromisso).month == agora.month
            and self._data_hora(compromisso).year == agora.year
        }
        for semana in calendar.monthcalendar(agora.year, agora.month):
            print(
                "".join(
                    "     " if dia == 0 else f"{dia:02d}{'*' if dia in dias_com_compromisso else ' '}  "
                    for dia in semana
                )
            )
        print("\n* Dia com compromisso de estudo cadastrado.")

    def editar_compromisso(self) -> None:
        calendario = self._carregar()
        compromissos = self._compromissos_usuario(calendario)
        ordenados = sorted(compromissos, key=self._data_hora)
        if not ordenados:
            print("Você não possui compromissos para editar.")
            return
        self._exibir_lista(ordenados)
        indice = self._ler_indice("Digite o número do compromisso que deseja editar: ", len(ordenados))
        if indice is None:
            return
        compromisso = ordenados[indice]
        print("\nDeixe em branco o que não deseja alterar.")
        materia = input("Nova matéria: ").strip() or compromisso["materia"]
        descricao = input("Nova descrição: ").strip() or compromisso["descricao"]
        data = input("Nova data (DD/MM/AAAA): ").strip() or compromisso["data"]
        hora = input("Nova hora (HH:MM): ").strip() or compromisso["hora"]
        try:
            data_hora = self._interpretar_data_hora(data, hora)
        except ValueError:
            print("Data ou horário inválido.")
            return
        if data_hora < self.horario.obter_horario_atual():
            print("Não é possível cadastrar um estudo em uma data passada.")
            return
        compromisso.update(
            {
                "materia": materia,
                "descricao": descricao,
                "data": data_hora.strftime("%d/%m/%Y"),
                "hora": data_hora.strftime("%H:%M"),
                "lembrete_exibido": False,
            }
        )
        self.persistencia.salvar(self.ARQUIVO, calendario)
        print("Compromisso atualizado com sucesso!")

    def excluir_compromisso(self) -> None:
        calendario = self._carregar()
        compromissos = self._compromissos_usuario(calendario)
        ordenados = sorted(compromissos, key=self._data_hora)
        if not ordenados:
            print("Você não possui compromissos para excluir.")
            return
        self._exibir_lista(ordenados)
        indice = self._ler_indice("Digite o número do compromisso que deseja excluir: ", len(ordenados))
        if indice is None:
            return
        compromisso = ordenados[indice]
        confirmacao = input(
            f"Tem certeza que deseja excluir '{compromisso['materia']}'? (s/n): "
        ).strip().lower()
        if confirmacao != "s":
            print("Exclusão cancelada.")
            return
        compromissos.remove(compromisso)
        self.persistencia.salvar(self.ARQUIVO, calendario)
        print("Compromisso excluído com sucesso!")

    def verificar_lembretes(self) -> None:
        calendario = self._carregar()
        compromissos = self._compromissos_usuario(calendario)
        agora = self.horario.obter_horario_atual()
        encontrou = False
        for compromisso in compromissos:
            if self._data_hora(compromisso) <= agora and not compromisso.get(
                "lembrete_exibido", False
            ):
                print("\n====================================")
                print("       HORA DE ESTUDAR!")
                print("====================================")
                print(f"Matéria: {compromisso['materia']}")
                print(f"Atividade: {compromisso['descricao']}")
                print(f"Horário planejado: {compromisso['hora']}")
                print("Não esqueça do seu compromisso de estudo!")
                compromisso["lembrete_exibido"] = True
                encontrou = True
        if encontrou:
            self.persistencia.salvar(self.ARQUIVO, calendario)

    def _usuario_atual(self) -> str | None:
        ratname = self.estado.usuario_logado
        if ratname is None:
            print("Você precisa fazer login para acessar o calendário.")
        return ratname

    @staticmethod
    def _interpretar_data_hora(data: str, hora: str) -> datetime:
        return datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")

    @classmethod
    def _data_hora(cls, compromisso: dict) -> datetime:
        try:
            return cls._interpretar_data_hora(
                compromisso["data"], compromisso["hora"]
            )
        except (KeyError, TypeError, ValueError) as erro:
            raise ValueError("Um compromisso salvo possui data ou horário inválido.") from erro

    @staticmethod
    def _exibir_lista(compromissos: list[dict]) -> None:
        print("\n===== MEUS COMPROMISSOS =====")
        for indice, compromisso in enumerate(compromissos, start=1):
            print(
                f"{indice}. {compromisso['materia']} | "
                f"{compromisso['data']} às {compromisso['hora']}"
            )

    @staticmethod
    def _ler_indice(pergunta: str, quantidade: int) -> int | None:
        try:
            numero = int(input(pergunta).strip())
        except ValueError:
            print("Digite um número válido.")
            return None
        if numero < 1 or numero > quantidade:
            print("Compromisso não encontrado.")
            return None
        return numero - 1
