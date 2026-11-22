import os
import shutil
import sys
import time
from datetime import datetime
from uuid import uuid4

import lista
from Dados import persistencia
from Horario import GerenciadorHorario
from Ratcoins import gerenciador_ratcoins

if os.name == "nt":
    import msvcrt
else:
    msvcrt = None


class RegistroPresenca:
    ARQUIVO_PRESENCAS = "presencas.json"
    ARQUIVO_MODELOS = "modelos_estudo.json"
    TEMPO_MINIMO_RATCOINS_SEGUNDOS = 30 * 60

    def __init__(self) -> None:
        self.estado = lista.estado
        self.persistencia = persistencia
        self.horario = GerenciadorHorario()

    def registrar(self) -> None:
        ratname = self.estado.usuario_logado
        if ratname is None:
            print("\nVocê precisa fazer login para registrar sua presença.")
            return

        disciplinas = {
            sala["materia"].casefold(): sala["materia"]
            for sala in self.estado.salas_disponiveis
        }
        print("\n===== REGISTRO DE PRESENÇA =====")
        print("Disciplinas disponíveis:")
        for disciplina in disciplinas.values():
            print(f"- {disciplina}")

        disciplina = self._ler_disciplina(disciplinas)
        confirmar = input("Deseja iniciar o cronômetro? (s/n): ").strip().casefold()
        if confirmar != "s":
            print("Sessão não iniciada. Você retornará ao menu principal.")
            return

        modelo = self._obter_modelo_atual(ratname)
        blocos = self._ler_blocos(modelo)
        inicio = self.horario.obter_horario_atual()
        print(f"\nCronômetro iniciado! Você está estudando: {disciplina}")
        if modelo is not None:
            print(f"Modelo em uso: {modelo['nome']}")
        duracao_segundos, tempo_estudo_segundos, fim = self._aguardar_finalizacao(
            blocos, inicio
        )

        registro_id = uuid4().hex
        presencas = self.persistencia.carregar(self.ARQUIVO_PRESENCAS, {})
        if not isinstance(presencas, dict):
            raise ValueError("O arquivo de presencas deve conter um objeto JSON.")

        historico = presencas.setdefault(ratname, [])
        if not isinstance(historico, list):
            raise ValueError(f"O histórico de presenças de '{ratname}' está inválido.")
        historico.append(
            {
                "id": registro_id,
                "disciplina": disciplina,
                "inicio": inicio.isoformat(timespec="seconds"),
                "fim": fim.isoformat(timespec="seconds"),
                "duracao_segundos": duracao_segundos,
                "tempo_estudo_segundos": tempo_estudo_segundos,
            }
        )
        self.persistencia.salvar(self.ARQUIVO_PRESENCAS, presencas)

        ganhou_ratcoins = (
            self.estado.tipo_usuario_logado == self.estado.TIPO_ESTUDANTE
            and tempo_estudo_segundos >= self.TEMPO_MINIMO_RATCOINS_SEGUNDOS
        )
        if ganhou_ratcoins:
            gerenciador_ratcoins.registrar_ganho(
                ratname,
                "Registro de presença com pelo menos 30 minutos de estudo",
                15,
                evento_id=f"presenca:{registro_id}",
            )

        minutos, segundos = divmod(duracao_segundos, 60)
        minutos_estudo, segundos_estudo = divmod(tempo_estudo_segundos, 60)
        if self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR:
            mensagem_ratcoins = (
                "\nMonitores ganham RatCoins publicando atividades em salas de estudo."
            )
        elif ganhou_ratcoins:
            mensagem_ratcoins = "\nVocê ganhou 15 RatCoins!"
        else:
            mensagem_ratcoins = (
                "\nVocê não ganhou RatCoins: é necessário estudar por pelo menos "
                "30 minutos."
            )
        print(
            "\nSessão de estudo finalizada!"
            "\nAtividade registrada e presença confirmada."
            f"\nDisciplina: {disciplina}"
            f"\nTempo total da sessão: {minutos} min {segundos} s"
            f"\nTempo efetivo de estudo: {minutos_estudo} min {segundos_estudo} s"
            f"{mensagem_ratcoins}"
            "\nVocê retornará ao menu principal."
        )

    def _obter_modelo_atual(self, ratname: str) -> dict | None:
        modelos = self.persistencia.carregar(self.ARQUIVO_MODELOS, {})
        if not isinstance(modelos, dict):
            raise ValueError("O arquivo de modelos de estudo deve conter um objeto JSON.")
        modelo = modelos.get(ratname)
        if modelo is not None and not isinstance(modelo, dict):
            raise ValueError(f"O modelo de estudo de '{ratname}' está inválido.")
        return modelo

    @staticmethod
    def _ler_blocos(modelo: dict | None) -> list[tuple[str, int]]:
        if modelo is None:
            return []
        blocos = modelo.get("blocos")
        if not isinstance(blocos, list):
            raise ValueError("Os blocos do modelo de estudo estão inválidos.")

        blocos_validos = []
        for bloco in blocos:
            if (
                not isinstance(bloco, (list, tuple))
                or len(bloco) != 2
                or not isinstance(bloco[0], str)
                or type(bloco[1]) is not int
                or bloco[1] <= 0
            ):
                raise ValueError("Um bloco do modelo de estudo está inválido.")
            blocos_validos.append((bloco[0], bloco[1] * 60))
        return blocos_validos

    def _aguardar_finalizacao(
        self,
        blocos: list[tuple[str, int]],
        inicio: datetime,
    ) -> tuple[int, int, datetime]:
        total_planejado = sum(duracao for _, duracao in blocos)
        tempo_decorrido = 0.0
        leitura_anterior = inicio
        modo_manual_anterior = self.horario.modo_manual_ativo()

        if not (os.name == "nt" and sys.stdin.isatty()):
            self._exibir_bloco(blocos, tempo_decorrido)
            while True:
                finalizar = input(
                    '\nDigite "finalizar" quando terminar sua sessão de estudo: '
                ).strip().casefold()
                if finalizar == "finalizar":
                    break
                print('Entrada inválida. Digite "finalizar" para encerrar a sessão.')

                atual = self.horario.obter_horario_atual()
                modo_manual = self.horario.modo_manual_ativo()
                if modo_manual == modo_manual_anterior:
                    tempo_decorrido += max(
                        0, (atual - leitura_anterior).total_seconds()
                    )
                leitura_anterior = atual
                modo_manual_anterior = modo_manual
                if total_planejado and tempo_decorrido >= total_planejado:
                    break

            fim = self.horario.obter_horario_atual()
            modo_manual = self.horario.modo_manual_ativo()
            if modo_manual == modo_manual_anterior:
                tempo_decorrido += max(0, (fim - leitura_anterior).total_seconds())
            if total_planejado:
                tempo_decorrido = min(tempo_decorrido, total_planejado)
            return (
                int(tempo_decorrido),
                self._calcular_tempo_estudo(blocos, tempo_decorrido),
                fim,
            )

        comando = ""
        ultimo_render = 0.0
        while True:
            atual = self.horario.obter_horario_atual()
            modo_manual = self.horario.modo_manual_ativo()
            if modo_manual == modo_manual_anterior:
                tempo_decorrido += max(
                    0, (atual - leitura_anterior).total_seconds()
                )
            leitura_anterior = atual
            modo_manual_anterior = modo_manual

            if total_planejado and tempo_decorrido >= total_planejado:
                tempo_decorrido = float(total_planejado)
                print("\nModelo de estudo concluído.")
                break

            agora_monotonico = time.monotonic()
            if agora_monotonico - ultimo_render >= 1:
                self._exibir_bloco(blocos, tempo_decorrido, comando)
                ultimo_render = agora_monotonico

            if msvcrt.kbhit():
                tecla = msvcrt.getwch()
                if tecla == "\r":
                    if comando.strip().casefold() == "finalizar":
                        break
                    print('\nDigite "finalizar" para encerrar a sessão.')
                    comando = ""
                elif tecla == "\b":
                    comando = comando[:-1]
                elif tecla == "\x03":
                    raise KeyboardInterrupt
                elif tecla.isprintable() and len(comando) < len("finalizar"):
                    comando += tecla
            time.sleep(0.1)

        fim = self.horario.obter_horario_atual()
        return (
            int(tempo_decorrido),
            self._calcular_tempo_estudo(blocos, tempo_decorrido),
            fim,
        )

    def _exibir_bloco(
        self,
        blocos: list[tuple[str, int]],
        tempo_decorrido: float,
        comando: str = "",
    ) -> None:
        atividade, restante = self._bloco_atual(blocos, tempo_decorrido)
        tipo_bloco = (
            "BLOCO DE DESCANSO"
            if self._eh_pausa(atividade)
            else "BLOCO DE ESTUDO"
        )
        status = (
            f"{tipo_bloco} | {atividade} | "
            f"{self._formatar_duracao(tempo_decorrido)}"
        )
        if restante is not None:
            status += f" | Restante {self._formatar_duracao(restante)}"
        status += f" | finalizar: {comando}"

        largura = max(2, shutil.get_terminal_size((80, 24)).columns)
        limite = largura - 1
        if len(status) > limite:
            prefixo = f"{tipo_bloco} | "
            sufixo = f" | {self._formatar_duracao(tempo_decorrido)}"
            if restante is not None:
                sufixo += f" | Restante {self._formatar_duracao(restante)}"
            sufixo += f" | finalizar: {comando}"
            tamanho_atividade = max(0, limite - len(prefixo) - len(sufixo))
            status = f"{prefixo}{atividade[:tamanho_atividade]}{sufixo}"
        sys.stdout.write(f"\r{status[:limite].ljust(limite)}")
        sys.stdout.flush()

    @staticmethod
    def _bloco_atual(
        blocos: list[tuple[str, int]],
        tempo_decorrido: float,
    ) -> tuple[str, float | None]:
        restante_total = max(0.0, tempo_decorrido)
        for atividade, duracao in blocos:
            if restante_total < duracao:
                return atividade, duracao - restante_total
            restante_total -= duracao
        if blocos:
            return blocos[-1][0], 0
        return "Estudo livre", None

    @classmethod
    def _calcular_tempo_estudo(
        cls,
        blocos: list[tuple[str, int]],
        tempo_decorrido: float,
    ) -> int:
        restante = max(0.0, tempo_decorrido)
        tempo_estudo = 0.0
        for atividade, duracao in blocos:
            tempo_bloco = min(restante, duracao)
            if not cls._eh_pausa(atividade):
                tempo_estudo += tempo_bloco
            restante -= tempo_bloco
            if restante <= 0:
                break
        if not blocos:
            tempo_estudo = max(0.0, tempo_decorrido)
        return int(tempo_estudo)

    @staticmethod
    def _eh_pausa(atividade: str) -> bool:
        nome = atividade.casefold()
        return any(palavra in nome for palavra in ("pausa", "descanso", "break"))

    @staticmethod
    def _formatar_duracao(segundos: float) -> str:
        minutos, segundos_restantes = divmod(int(segundos), 60)
        horas, minutos = divmod(minutos, 60)
        return f"{horas:02d}:{minutos:02d}:{segundos_restantes:02d}"

    def _ler_disciplina(self, disciplinas: dict[str, str]) -> str:
        while True:
            entrada = input(
                "\nDigite a disciplina ou assunto que vai estudar: "
            ).strip()
            disciplina = disciplinas.get(entrada.casefold())
            if disciplina is not None:
                return disciplina
            print("Disciplina inválida. Escolha uma das opções disponíveis.")


if __name__ == "__main__":
    RegistroPresenca().registrar()
