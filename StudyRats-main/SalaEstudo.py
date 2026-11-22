from datetime import datetime, timedelta
from uuid import uuid4

import lista
from Dados import persistencia
from Horario import GerenciadorHorario
from Ratcoins import gerenciador_ratcoins


class GerenciadorSalas:
    ARQUIVO_PARTICIPANTES = "participantes_salas.json"

    def __init__(
        self,
        horario: GerenciadorHorario | None = None,
    ) -> None:
        self.estado = lista.estado
        self.persistencia = persistencia
        self.horario = horario or GerenciadorHorario()

    def _intervalo_sessao(self, sala: dict, agora: datetime) -> tuple:
        inicio_hora = datetime.strptime(sala["inicio"], "%H:%M").time()
        fim_hora = datetime.strptime(sala["fim"], "%H:%M").time()
        atravessa_meia_noite = fim_hora <= inicio_hora

        if atravessa_meia_noite and agora.time() < fim_hora:
            data_inicio = agora.date() - timedelta(days=1)
        else:
            data_inicio = agora.date()

        inicio = datetime.combine(data_inicio, inicio_hora)
        data_fim = data_inicio + timedelta(days=1) if atravessa_meia_noite else data_inicio
        fim = datetime.combine(data_fim, fim_hora)
        ativo = inicio <= agora < fim
        return inicio, fim, ativo

    @staticmethod
    def _chave_sessao(inicio: datetime) -> str:
        return inicio.isoformat(timespec="minutes")

    def _carregar_participacoes(self, agora: datetime) -> dict:
        participacoes = self.persistencia.carregar(self.ARQUIVO_PARTICIPANTES, {})
        if not isinstance(participacoes, dict):
            raise ValueError("O arquivo de participantes deve conter um objeto JSON.")

        alterado = False
        for sala_id in list(participacoes):
            sessoes = participacoes[sala_id]
            if not isinstance(sessoes, dict):
                raise ValueError(f"As sessões da sala '{sala_id}' estão inválidas.")
            for chave in list(sessoes):
                sessao = sessoes[chave]
                fim_texto = sessao.get("fim") if isinstance(sessao, dict) else None
                if not isinstance(fim_texto, str):
                    raise ValueError(
                        f"A sessão '{chave}' da sala '{sala_id}' está inválida."
                    )
                try:
                    fim = datetime.fromisoformat(fim_texto)
                except ValueError as erro:
                    raise ValueError(
                        f"O horário final da sessão '{chave}' está inválido."
                    ) from erro
                if fim <= agora:
                    del sessoes[chave]
                    alterado = True
            if not sessoes:
                del participacoes[sala_id]
                alterado = True

        if alterado:
            self.persistencia.salvar(self.ARQUIVO_PARTICIPANTES, participacoes)
        return participacoes

    def limpar_sessoes_expiradas(self) -> None:
        self._carregar_participacoes(self.horario.obter_horario_atual())

    def _obter_sessao(
        self,
        participacoes: dict,
        sala: dict,
        inicio: datetime,
        fim: datetime,
    ) -> dict:
        sessoes_sala = participacoes.setdefault(sala["id"], {})
        chave = self._chave_sessao(inicio)
        sessao = sessoes_sala.get(chave)
        if sessao is None:
            sessao = {
                "fim": fim.isoformat(timespec="minutes"),
                "participantes": {},
                "duvidas": [],
                "atividades": [],
            }
            sessoes_sala[chave] = sessao
        sessao.setdefault("duvidas", [])
        sessao.setdefault("atividades", [])
        if not isinstance(sessao["duvidas"], list):
            raise ValueError(f"As dúvidas da sala '{sala['id']}' estão inválidas.")
        if not isinstance(sessao["atividades"], list):
            raise ValueError(f"As atividades da sala '{sala['id']}' estão inválidas.")
        return sessao

    @staticmethod
    def _contar_participantes_ativos(participantes: dict) -> int:
        return sum(
            participante["inicio_atividade"] is not None
            and participante.get("tipo_usuario", "ESTUDANTE") != "MONITOR"
            for participante in participantes.values()
        )

    def listar_salas(self) -> None:
        agora = self.horario.obter_horario_atual()
        participacoes = self._carregar_participacoes(agora)
        print(f"\n=== SALAS DE ESTUDO | {agora:%d/%m/%Y %H:%M} ===")

        if not self.estado.salas_disponiveis:
            print("Nenhuma sala de estudo disponível no momento.")
            return

        for indice, sala in enumerate(self.estado.salas_disponiveis, start=1):
            inicio, fim, ativo = self._intervalo_sessao(sala, agora)
            sessao = self._obter_sessao(participacoes, sala, inicio, fim)
            participantes = sessao["participantes"]
            quantidade_ativos = self._contar_participantes_ativos(participantes)
            vagas = sala["capacidade"] - quantidade_ativos

            if not sala["ativa"]:
                status = "Indisponível"
            elif ativo and vagas <= 0:
                status = (
                    "Lotada para estudantes"
                    if self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR
                    else "Lotada"
                )
            elif ativo:
                status = "Em andamento"
            else:
                status = "Fora do horário"

            print(
                f"{indice}. {sala['nome']} | Matéria: {sala['materia']} | "
                f"Horário: {sala['inicio']} - {sala['fim']} | "
                f"Monitor: {sala['monitor']} | Participantes: "
                f"{quantidade_ativos}/{sala['capacidade']} | Status: {status}"
            )

        print("0. Voltar ao menu principal")

    def exibir_sala_de_estudo(self) -> None:
        if self.estado.usuario_logado is None:
            print("\nVocê precisa fazer login para acessar as salas de estudo.")
            return

        ratname = self.estado.usuario_logado
        tipo_usuario = self.estado.tipo_usuario_logado
        eh_monitor = tipo_usuario == self.estado.TIPO_MONITOR
        if not any(
            usuario["ratname"] == ratname for usuario in self.estado.usuarios
        ):
            raise ValueError("O usuário conectado não existe na lista persistida de contas.")

        self.listar_salas()
        escolha = input("\nEscolha uma sala para entrar (ou 0 para voltar): ").strip()
        if not escolha.isdigit():
            print("Opção inválida.")
            return

        indice_sala = int(escolha)
        if indice_sala == 0:
            return
        if indice_sala < 1 or indice_sala > len(self.estado.salas_disponiveis):
            print("Sala inválida. Tente novamente.")
            return

        sala = self.estado.salas_disponiveis[indice_sala - 1]
        agora = self.horario.obter_horario_atual()
        inicio, fim, ativo = self._intervalo_sessao(sala, agora)
        participacoes = self._carregar_participacoes(agora)
        sessao = self._obter_sessao(participacoes, sala, inicio, fim)
        participantes = sessao["participantes"]
        ja_esta_ativo = (
            ratname in participantes
            and participantes[ratname]["inicio_atividade"] is not None
        )

        quantidade_ativos = self._contar_participantes_ativos(participantes)
        vagas = sala["capacidade"] - quantidade_ativos
        if not sala["ativa"] or not ativo:
            print(
                f"\nA sala '{sala['nome']}' só permite entrada entre "
                f"{sala['inicio']} e {sala['fim']} "
                f"(horário considerado: {agora:%H:%M})."
            )
            return
        if vagas <= 0 and not ja_esta_ativo and not eh_monitor:
            print(f"\nA sala '{sala['nome']}' atingiu o limite de participantes.")
            return

        self._exibir_detalhes_sala(sala, quantidade_ativos)
        entrar = input(
            '\nDigite "entrar" para participar desta sala: '
        ).strip().lower()
        if entrar != "entrar":
            print("Você decidiu não entrar na sala de estudos.")
            return

        agora = self.horario.obter_horario_atual()
        inicio, fim, ativo = self._intervalo_sessao(sala, agora)
        if not ativo:
            print("O horário da sala terminou antes da confirmação da entrada.")
            return

        participacoes = self._carregar_participacoes(agora)
        sessao = self._obter_sessao(participacoes, sala, inicio, fim)
        participantes = sessao["participantes"]
        ja_esta_ativo = (
            ratname in participantes
            and participantes[ratname]["inicio_atividade"] is not None
        )
        quantidade_ativos = self._contar_participantes_ativos(participantes)
        if quantidade_ativos >= sala["capacidade"] and not ja_esta_ativo and not eh_monitor:
            print(f"\nA sala '{sala['nome']}' atingiu o limite de participantes.")
            return

        participante = participantes.get(ratname)
        primeira_entrada = participante is None
        if participante is None:
            participante = {
                "email": next(
                    usuario["email"]
                    for usuario in self.estado.usuarios
                    if usuario["ratname"] == ratname
                ),
                "tipo_usuario": tipo_usuario,
                "primeira_entrada": agora.isoformat(timespec="seconds"),
                "inicio_atividade": agora.isoformat(timespec="seconds"),
                "tempo_total_segundos": 0,
            }
            participantes[ratname] = participante
        else:
            participante.setdefault("tipo_usuario", tipo_usuario)
            if participante["inicio_atividade"] is None:
                participante["inicio_atividade"] = agora.isoformat(timespec="seconds")

        self.persistencia.salvar(self.ARQUIVO_PARTICIPANTES, participacoes)
        if primeira_entrada and tipo_usuario == self.estado.TIPO_ESTUDANTE:
            gerenciador_ratcoins.registrar_ganho(
                ratname,
                f"Entrada na sala de estudo: {sala['nome']}",
                20,
                evento_id=(
                    f"sala:{sala['id']}:{self._chave_sessao(inicio)}:{ratname}"
                ),
            )
        print(f"\n{ratname}, você entrou na sala '{sala['nome']}' com sucesso!")
        print(
            "Você pode acompanhar a resolução de questões, enviar dúvidas "
            "e participar da discussão."
        )
        self._interagir_com_sala(
            sala, inicio, fim, ratname, participante, participacoes
        )

    @staticmethod
    def _exibir_detalhes_sala(sala: dict, quantidade_ativos: int) -> None:
        print(f"\n=== {sala['nome']} ===")
        print(f"Matéria: {sala['materia']}")
        print(f"Descrição: {sala['descricao']}")
        print(f"Monitor responsável: {sala['monitor']}")
        print(f"Horário: {sala['inicio']} - {sala['fim']}")
        print(f"Participantes: {quantidade_ativos}/{sala['capacidade']}")

    def _interagir_com_sala(
        self,
        sala: dict,
        inicio: datetime,
        fim: datetime,
        ratname: str,
        participante: dict,
        participacoes: dict,
    ) -> None:
        eh_monitor = self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR
        while True:
            print("\nOpções da sala:")
            print("1. Ver atividades e dúvidas")
            if eh_monitor:
                print("2. Criar atividade")
                print("3. Responder dúvida")
                print("4. Participar da discussão")
                print("5. Sair da sala")
            else:
                print("2. Enviar dúvida")
                print("3. Participar da discussão")
                print("4. Sair da sala")

            opcao = input("Escolha uma opção: ").strip()
            agora = self.horario.obter_horario_atual()
            if agora >= fim:
                self._finalizar_atividade(participante, fim)
                self._carregar_participacoes(agora)
                print("\nO horário da sala terminou. Sua participação foi registrada.")
                return

            if opcao == "1":
                participacoes = self._carregar_participacoes(agora)
                sessao = self._obter_sessao(participacoes, sala, inicio, fim)
                self._exibir_atividades_e_duvidas(sala, sessao)
            elif eh_monitor and opcao == "2":
                if self._criar_atividade(
                    sala, inicio, fim, ratname, participante
                ):
                    return
            elif eh_monitor and opcao == "3":
                if self._responder_duvida(
                    sala, inicio, fim, ratname, participante
                ):
                    return
            elif (eh_monitor and opcao == "4") or (not eh_monitor and opcao == "3"):
                print(f"{ratname} participou da discussão da sala.")
            elif (eh_monitor and opcao == "5") or (not eh_monitor and opcao == "4"):
                self._sair_da_sala(
                    sala, inicio, ratname, participante, participacoes, agora
                )
                return
            elif not eh_monitor and opcao == "2":
                if self._enviar_duvida(sala, inicio, fim, ratname, participante):
                    return
            else:
                print("Opção inválida. Tente novamente.")

    def _exibir_atividades_e_duvidas(self, sala: dict, sessao: dict) -> None:
        print(f"\n=== Atividades: {sala['nome']} ===")
        atividades = sessao["atividades"]
        if not atividades:
            print("Ainda não há atividades cadastradas nesta sessão.")
        for indice, atividade in enumerate(atividades, start=1):
            print(f"{indice}. {atividade['titulo']}")
            print(f"   Descrição: {atividade['descricao']}")
            print(f"   Criada por: {atividade['monitor']}")
            print(f"   Horário: {atividade['horario']}")

        print("\n=== Dúvidas e respostas ===")
        duvidas = sessao["duvidas"]
        if not duvidas:
            print("Ainda não há dúvidas nesta sessão.")
        for indice, duvida in enumerate(duvidas, start=1):
            print(
                f"{indice}. {duvida['usuario']} perguntou "
                f"({duvida['horario']}): {duvida['mensagem']}"
            )
            respostas = duvida.get("respostas", [])
            if not isinstance(respostas, list):
                raise ValueError(f"As respostas da dúvida {indice} estão inválidas.")
            if not respostas:
                print("   Ainda sem resposta.")
            for resposta in respostas:
                print(
                    f"   {resposta['usuario']} respondeu "
                    f"({resposta['horario']}): {resposta['mensagem']}"
                )

    def _criar_atividade(
        self,
        sala: dict,
        inicio: datetime,
        fim: datetime,
        ratname: str,
        participante: dict,
    ) -> bool:
        if self.estado.tipo_usuario_logado != self.estado.TIPO_MONITOR:
            print("Somente monitores podem criar atividades.")
            return False

        titulo = input("Título da atividade: ").strip()
        if not titulo:
            print("O título da atividade não pode ficar vazio.")
            return False
        descricao = input("Descrição da atividade: ").strip()
        if not descricao:
            print("A descrição da atividade não pode ficar vazia.")
            return False

        agora = self.horario.obter_horario_atual()
        if agora >= fim:
            self._finalizar_atividade(participante, fim)
            self._carregar_participacoes(agora)
            print("\nO horário da sala terminou. Sua participação foi registrada.")
            return True

        participacoes = self.persistencia.carregar(self.ARQUIVO_PARTICIPANTES, {})
        sessao = self._obter_sessao(participacoes, sala, inicio, fim)
        atividade_id = uuid4().hex
        sessao["atividades"].append(
            {
                "id": atividade_id,
                "titulo": titulo,
                "descricao": descricao,
                "monitor": ratname,
                "horario": agora.isoformat(timespec="seconds"),
            }
        )
        self.persistencia.salvar(self.ARQUIVO_PARTICIPANTES, participacoes)
        print("Atividade criada e disponibilizada para os estudantes da sala.")
        gerenciador_ratcoins.registrar_ganho(
            ratname,
            f"Publicar atividade: {titulo}",
            5,
            evento_id=f"atividade-monitor:{atividade_id}",
        )
        return False

    def _responder_duvida(
        self,
        sala: dict,
        inicio: datetime,
        fim: datetime,
        ratname: str,
        participante: dict,
    ) -> bool:
        if self.estado.tipo_usuario_logado != self.estado.TIPO_MONITOR:
            print("Somente monitores podem responder dúvidas.")
            return False

        participacoes = self.persistencia.carregar(self.ARQUIVO_PARTICIPANTES, {})
        sessao = self._obter_sessao(participacoes, sala, inicio, fim)
        duvidas = sessao["duvidas"]
        if not duvidas:
            print("Ainda não há dúvidas para responder nesta sala.")
            return False

        print("\nDúvidas recebidas:")
        for indice, duvida in enumerate(duvidas, start=1):
            print(
                f"{indice}. {duvida['usuario']}: {duvida['mensagem']}"
            )
            for resposta in duvida.get("respostas", []):
                print(
                    f"   Resposta de {resposta['usuario']}: "
                    f"{resposta['mensagem']}"
                )

        escolha = input(
            "Número da dúvida para responder (ou 0 para voltar): "
        ).strip()
        if escolha == "0":
            return False
        if not escolha.isdigit() or not 1 <= int(escolha) <= len(duvidas):
            print("Número de dúvida inválido.")
            return False

        mensagem = input("Digite sua resposta: ").strip()
        if not mensagem:
            print("A resposta não pode ficar vazia.")
            return False

        agora = self.horario.obter_horario_atual()
        if agora >= fim:
            self._finalizar_atividade(participante, fim)
            self._carregar_participacoes(agora)
            print("\nO horário da sala terminou. Sua participação foi registrada.")
            return True

        participacoes = self.persistencia.carregar(self.ARQUIVO_PARTICIPANTES, {})
        sessao = self._obter_sessao(participacoes, sala, inicio, fim)
        indice_duvida = int(escolha) - 1
        if indice_duvida >= len(sessao["duvidas"]):
            raise ValueError("A dúvida selecionada não existe mais nesta sessão.")
        duvida = sessao["duvidas"][indice_duvida]
        respostas = duvida.setdefault("respostas", [])
        if not isinstance(respostas, list):
            raise ValueError("As respostas da dúvida selecionada estão inválidas.")
        respostas.append(
            {
                "usuario": ratname,
                "mensagem": mensagem,
                "horario": agora.isoformat(timespec="seconds"),
            }
        )
        self.persistencia.salvar(self.ARQUIVO_PARTICIPANTES, participacoes)
        print("Resposta enviada. Os estudantes podem consultá-la na sala.")
        return False

    def _enviar_duvida(
        self,
        sala: dict,
        inicio: datetime,
        fim: datetime,
        ratname: str,
        participante: dict,
    ) -> bool:
        if self.estado.tipo_usuario_logado != self.estado.TIPO_ESTUDANTE:
            print("Somente estudantes podem enviar dúvidas.")
            return False

        duvida = input("Digite sua dúvida para o monitor: ").strip()
        agora = self.horario.obter_horario_atual()
        if agora >= fim:
            self._finalizar_atividade(participante, fim)
            self._carregar_participacoes(agora)
            print("\nO horário da sala terminou. Sua participação foi registrada.")
            return True
        if not duvida:
            print("Você precisa escrever uma dúvida antes de enviar.")
            return False

        participacoes = self.persistencia.carregar(self.ARQUIVO_PARTICIPANTES, {})
        sessao = participacoes[sala["id"]][self._chave_sessao(inicio)]
        sessao["duvidas"].append(
            {
                "usuario": ratname,
                "mensagem": duvida,
                "horario": agora.isoformat(timespec="seconds"),
                "respostas": [],
            }
        )
        self.persistencia.salvar(self.ARQUIVO_PARTICIPANTES, participacoes)
        print("Sua dúvida foi enviada ao monitor.")
        return False

    def _sair_da_sala(
        self,
        sala: dict,
        inicio: datetime,
        ratname: str,
        participante: dict,
        participacoes: dict,
        agora: datetime,
    ) -> None:
        self._finalizar_atividade(participante, agora)
        participacoes = self.persistencia.carregar(self.ARQUIVO_PARTICIPANTES, {})
        sessao = participacoes[sala["id"]][self._chave_sessao(inicio)]
        sessao["participantes"][ratname] = participante
        self.persistencia.salvar(self.ARQUIVO_PARTICIPANTES, participacoes)

        tempo_total = participante["tempo_total_segundos"]
        horas, resto = divmod(tempo_total, 3600)
        minutos, segundos = divmod(resto, 60)
        print(f"\nVocê saiu da sala '{sala['nome']}' com sucesso.")
        print(f"Tempo ativo nesta sessão: {horas}h {minutos}m {segundos}s")
        print(
            "Sua vaga foi liberada. O histórico da sessão permanece salvo "
            "até o horário da sala acabar."
        )

    @staticmethod
    def _finalizar_atividade(participante: dict, horario_fim: datetime) -> None:
        inicio_atividade = participante["inicio_atividade"]
        if inicio_atividade is None:
            return

        inicio = datetime.fromisoformat(inicio_atividade)
        segundos = max(0, int((horario_fim - inicio).total_seconds()))
        participante["tempo_total_segundos"] += segundos
        participante["inicio_atividade"] = None
