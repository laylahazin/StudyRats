import os  # Usa nesta etapa o valor ou operador específico mostrado em import os; ele participa do estado atual do método.
import shutil  # Usa nesta etapa o valor ou operador específico mostrado em import shutil; ele participa do estado atual do método.
import sys  # Usa nesta etapa o valor ou operador específico mostrado em import sys; ele participa do estado atual do método.
import time  # Usa nesta etapa o valor ou operador específico mostrado em import time; ele participa do estado atual do método.
from datetime import datetime  # Usa nesta etapa o valor ou operador específico mostrado em from datetime import datetime; ele participa do estado atual do método.
from uuid import uuid4  # Usa nesta etapa o valor ou operador específico mostrado em from uuid import uuid4; ele participa do estado atual do método.

import lista  # Usa nesta etapa o valor ou operador específico mostrado em import lista; ele participa do estado atual do método.
from Dados import persistencia  # Usa nesta etapa o valor ou operador específico mostrado em from Dados import persistencia; ele participa do estado atual do método.
from Horario import GerenciadorHorario  # Usa nesta etapa o valor ou operador específico mostrado em from Horario import GerenciadorHorario; ele participa do estado atual do método.
from Ratcoins import gerenciador_ratcoins  # Usa nesta etapa o valor ou operador específico mostrado em from Ratcoins import gerenciador_ratcoins; ele participa do estado atual do método.

if os.name == "nt":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
    import msvcrt  # Usa nesta etapa o valor ou operador específico mostrado em import msvcrt; ele participa do estado atual do método.
else:  # Executa este ramo quando nenhuma condição anterior deste encadeamento foi atendida.
    msvcrt = None  # Guarda em msvcrt o resultado de None, necessário à próxima decisão.


class RegistroPresenca:  # Usa nesta etapa o valor ou operador específico mostrado em class RegistroPresenca:; ele participa do estado atual do método.
    ARQUIVO_PRESENCAS = "presencas.json"  # Guarda em ARQUIVO_PRESENCAS o resultado de "presencas.json", necessário à próxima decisão.
    ARQUIVO_MODELOS = "modelos_estudo.json"  # Nomeia modelos_estudo.json como arquivo dos planos confirmados por conta.
    TEMPO_MINIMO_RATCOINS_SEGUNDOS = 30 * 60  # Exige 1800 segundos efetivos: 30 minutos multiplicados por 60.

    def __init__(self) -> None:  # Define __init__, que executa a operação específica desta etapa.
        self.estado = lista.estado  # Conecta o gerenciador ao estado global com login, usuários e salas.
        self.persistencia = persistencia  # Conecta o gerenciador ao módulo JSON que lê e grava dados.
        self.horario = GerenciadorHorario()  # Define o relógio real ou o relógio fornecido pelos testes.

    def registrar(self) -> None:  # Define registrar, que medir a sessão e salvar sua presença.
        ratname = self.estado.usuario_logado  # Obtém o identificador da conta conectada para vincular modelo, presença ou participação.
        if ratname is None:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("\nVocê precisa fazer login para registrar sua presença.")  # Informa que é necessário autenticar antes de usar este recurso.
            return  # Retorna ao chamador e encerra o método neste ponto.

        disciplinas = {  # Guarda em disciplinas o resultado de {, necessário à próxima decisão.
            sala["materia"].casefold(): sala["materia"]  # Usa nesta etapa o valor ou operador específico mostrado em sala["materia"].casefold(): sala["materia"]; ele participa do estado atual do método.
            for sala in self.estado.salas_disponiveis  # Percorre cada elemento da coleção aplicando as operações deste bloco.
        }  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        print("\n===== REGISTRO DE PRESENÇA =====")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        print("Disciplinas disponíveis:")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        for disciplina in disciplinas.values():  # Percorre cada elemento da coleção aplicando as operações deste bloco.
            print(f"- {disciplina}")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.

        disciplina = self._ler_disciplina(disciplinas)  # Guarda em disciplina o resultado de self._ler_disciplina(disciplinas), necessário à próxima decisão.
        confirmar = input("Deseja iniciar o cronômetro? (s/n): ").strip().casefold()  # Guarda em confirmar o resultado de input("Deseja iniciar o cronômetro? (s/n): ").strip().casefold(), necessário à próxima decisão.
        if confirmar != "s":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("Sessão não iniciada. Você retornará ao menu principal.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return  # Retorna ao chamador e encerra o método neste ponto.

        modelo = self._obter_modelo_atual(ratname)  # Armazena o plano escolhido, cuja lista de blocos será exibida ou usada.
        blocos = self._ler_blocos(modelo)  # Armazena a sequência de estudo e pausa usada pelo cronômetro.
        inicio = self.horario.obter_horario_atual()  # Registra em inicio o valor self.horario.obter_horario_atual(), usado no cálculo temporal desta sessão.
        print(f"\nCronômetro iniciado! Você está estudando: {disciplina}")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        if modelo is not None:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print(f"Modelo em uso: {modelo['nome']}")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        duracao_segundos, tempo_estudo_segundos, fim = self._aguardar_finalizacao(  # Guarda em duracao_segundos, tempo_estudo_segundos, fim o resultado de self._aguardar_finalizacao(, necessário à próxima decisão.
            blocos, inicio  # Usa nesta etapa o valor ou operador específico mostrado em blocos, inicio; ele participa do estado atual do método.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

        registro_id = uuid4().hex  # Gera um ID único para distinguir o registro e evitar cobrança duplicada.
        presencas = self.persistencia.carregar(self.ARQUIVO_PRESENCAS, {})  # Guarda em presencas o resultado de self.persistencia.carregar(self.ARQUIVO_PRESENCAS, {}), necessário à próxima decisão.
        if not isinstance(presencas, dict):  # Valida o tipo do dado carregado antes de continuar o processamento.
            raise ValueError("O arquivo de presencas deve conter um objeto JSON.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.

        historico = presencas.setdefault(ratname, [])  # Guarda em historico o resultado de presencas.setdefault(ratname, []), necessário à próxima decisão.
        if not isinstance(historico, list):  # Valida o tipo do dado carregado antes de continuar o processamento.
            raise ValueError(f"O histórico de presenças de '{ratname}' está inválido.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
        historico.append(  # Adiciona à lista o registro criado nesta etapa.
            {  # Usa nesta etapa o valor ou operador específico mostrado em {; ele participa do estado atual do método.
                "id": registro_id,  # Usa nesta etapa o valor ou operador específico mostrado em "id": registro_id,; ele participa do estado atual do método.
                "disciplina": disciplina,  # Usa nesta etapa o valor ou operador específico mostrado em "disciplina": disciplina,; ele participa do estado atual do método.
                "inicio": inicio.isoformat(timespec="seconds"),  # Guarda em "inicio": inicio.isoformat(timespec o resultado de "seconds"),, necessário à próxima decisão.
                "fim": fim.isoformat(timespec="seconds"),  # Guarda em "fim": fim.isoformat(timespec o resultado de "seconds"),, necessário à próxima decisão.
                "duracao_segundos": duracao_segundos,  # Usa nesta etapa o valor ou operador específico mostrado em "duracao_segundos": duracao_segundos,; ele participa do estado atual do método.
                "tempo_estudo_segundos": tempo_estudo_segundos,  # Usa nesta etapa o valor ou operador específico mostrado em "tempo_estudo_segundos": tempo_estudo_segundos,; ele participa do estado atual do método.
            }  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        self.persistencia.salvar(self.ARQUIVO_PRESENCAS, presencas)  # Grava no JSON o estado atualizado desta conta, sala ou sessão.

        ganhou_ratcoins = (  # Guarda em ganhou_ratcoins o resultado de (, necessário à próxima decisão.
            self.estado.tipo_usuario_logado == self.estado.TIPO_ESTUDANTE  # Atualiza self.estado.tipo_usuario_logado com = self.estado.TIPO_ESTUDANTE, estado usado nas operações seguintes.
            and tempo_estudo_segundos >= self.TEMPO_MINIMO_RATCOINS_SEGUNDOS  # Exige 1800 segundos efetivos: 30 minutos multiplicados por 60.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        if ganhou_ratcoins:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            gerenciador_ratcoins.registrar_ganho(  # Usa nesta etapa o valor ou operador específico mostrado em gerenciador_ratcoins.registrar_ganho(; ele participa do estado atual do método.
                ratname,  # Usa nesta etapa o valor ou operador específico mostrado em ratname,; ele participa do estado atual do método.
                "Registro de presença com pelo menos 30 minutos de estudo",  # Usa nesta etapa o valor ou operador específico mostrado em "Registro de presença com pelo menos 30 minutos de estudo",; ele participa do estado atual do método.
                15,  # Usa nesta etapa o valor ou operador específico mostrado em 15,; ele participa do estado atual do método.
                evento_id=f"presenca:{registro_id}",  # Guarda em evento_id o resultado de f"presenca:{registro_id}",, necessário à próxima decisão.
            )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

        minutos, segundos = divmod(duracao_segundos, 60)  # Guarda em minutos, segundos o resultado de divmod(duracao_segundos, 60), necessário à próxima decisão.
        minutos_estudo, segundos_estudo = divmod(tempo_estudo_segundos, 60)  # Guarda em minutos_estudo, segundos_estudo o resultado de divmod(tempo_estudo_segundos, 60), necessário à próxima decisão.
        if self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            mensagem_ratcoins = (  # Guarda em mensagem_ratcoins o resultado de (, necessário à próxima decisão.
                "\nMonitores ganham RatCoins publicando atividades em salas de estudo."  # Usa nesta etapa o valor ou operador específico mostrado em "\nMonitores ganham RatCoins publicando atividades em salas de estudo."; ele participa do estado atual do método.
            )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        elif ganhou_ratcoins:  # Testa esta alternativa somente após todas as condições anteriores falharem.
            mensagem_ratcoins = "\nVocê ganhou 15 RatCoins!"  # Guarda em mensagem_ratcoins o resultado de "\nVocê ganhou 15 RatCoins!", necessário à próxima decisão.
        else:  # Executa este ramo quando nenhuma condição anterior deste encadeamento foi atendida.
            mensagem_ratcoins = (  # Guarda em mensagem_ratcoins o resultado de (, necessário à próxima decisão.
                "\nVocê não ganhou RatCoins: é necessário estudar por pelo menos "  # Usa nesta etapa o valor ou operador específico mostrado em "\nVocê não ganhou RatCoins: é necessário estudar por pelo menos "; ele participa do estado atual do método.
                "30 minutos."  # Usa nesta etapa o valor ou operador específico mostrado em "30 minutos."; ele participa do estado atual do método.
            )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        print(  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            "\nSessão de estudo finalizada!"  # Usa nesta etapa o valor ou operador específico mostrado em "\nSessão de estudo finalizada!"; ele participa do estado atual do método.
            "\nAtividade registrada e presença confirmada."  # Usa nesta etapa o valor ou operador específico mostrado em "\nAtividade registrada e presença confirmada."; ele participa do estado atual do método.
            f"\nDisciplina: {disciplina}"  # Usa nesta etapa o valor ou operador específico mostrado em f"\nDisciplina: {disciplina}"; ele participa do estado atual do método.
            f"\nTempo total da sessão: {minutos} min {segundos} s"  # Usa nesta etapa o valor ou operador específico mostrado em f"\nTempo total da sessão: {minutos} min {segundos} s"; ele participa do estado atual do método.
            f"\nTempo efetivo de estudo: {minutos_estudo} min {segundos_estudo} s"  # Usa nesta etapa o valor ou operador específico mostrado em f"\nTempo efetivo de estudo: {minutos_estudo} min {segundos_estudo} s"; ele participa do estado atual do método.
            f"{mensagem_ratcoins}"  # Usa nesta etapa o valor ou operador específico mostrado em f"{mensagem_ratcoins}"; ele participa do estado atual do método.
            "\nVocê retornará ao menu principal."  # Usa nesta etapa o valor ou operador específico mostrado em "\nVocê retornará ao menu principal."; ele participa do estado atual do método.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

    def _obter_modelo_atual(self, ratname: str) -> dict | None:  # Define _obter_modelo_atual, que executa a operação específica desta etapa.
        modelos = self.persistencia.carregar(self.ARQUIVO_MODELOS, {})  # Nomeia modelos_estudo.json como arquivo dos planos confirmados por conta.
        if not isinstance(modelos, dict):  # Valida o tipo do dado carregado antes de continuar o processamento.
            raise ValueError("O arquivo de modelos de estudo deve conter um objeto JSON.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
        modelo = modelos.get(ratname)  # Armazena o plano escolhido, cuja lista de blocos será exibida ou usada.
        if modelo is not None and not isinstance(modelo, dict):  # Valida o tipo do dado carregado antes de continuar o processamento.
            raise ValueError(f"O modelo de estudo de '{ratname}' está inválido.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
        return modelo  # Entrega ao chamador o resultado calculado por esta etapa.

    @staticmethod  # Usa nesta etapa o valor ou operador específico mostrado em @staticmethod; ele participa do estado atual do método.
    def _ler_blocos(modelo: dict | None) -> list[tuple[str, int]]:  # Define _ler_blocos, que executa a operação específica desta etapa.
        if modelo is None:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            return []  # Entrega ao chamador o resultado calculado por esta etapa.
        blocos = modelo.get("blocos")  # Armazena a sequência de estudo e pausa usada pelo cronômetro.
        if not isinstance(blocos, list):  # Valida o tipo do dado carregado antes de continuar o processamento.
            raise ValueError("Os blocos do modelo de estudo estão inválidos.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.

        blocos_validos = []  # Guarda em blocos_validos o resultado de [], necessário à próxima decisão.
        for bloco in blocos:  # Percorre os blocos em ordem para mostrar horário ou calcular tempo.
            if (  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                not isinstance(bloco, (list, tuple))  # Usa nesta etapa o valor ou operador específico mostrado em not isinstance(bloco, (list, tuple)); ele participa do estado atual do método.
                or len(bloco) != 2  # Guarda em or len(bloco) ! o resultado de 2, necessário à próxima decisão.
                or not isinstance(bloco[0], str)  # Usa nesta etapa o valor ou operador específico mostrado em or not isinstance(bloco[0], str); ele participa do estado atual do método.
                or type(bloco[1]) is not int  # Usa nesta etapa o valor ou operador específico mostrado em or type(bloco[1]) is not int; ele participa do estado atual do método.
                or bloco[1] <= 0  # Guarda em or bloco[1] < o resultado de 0, necessário à próxima decisão.
            ):  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
                raise ValueError("Um bloco do modelo de estudo está inválido.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
            blocos_validos.append((bloco[0], bloco[1] * 60))  # Adiciona à lista o registro criado nesta etapa.
        return blocos_validos  # Entrega ao chamador o resultado calculado por esta etapa.

    def _aguardar_finalizacao(  # Define _aguardar_finalizacao, que executa a operação específica desta etapa.
        self,  # Usa nesta etapa o valor ou operador específico mostrado em self,; ele participa do estado atual do método.
        blocos: list[tuple[str, int]],  # Usa nesta etapa o valor ou operador específico mostrado em blocos: list[tuple[str, int]],; ele participa do estado atual do método.
        inicio: datetime,  # Recebe o instante inicial desta sessão da sala.
    ) -> tuple[int, int, datetime]:  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        total_planejado = sum(duracao for _, duracao in blocos)  # Guarda em total_planejado o resultado de sum(duracao for _, duracao in blocos), necessário à próxima decisão.
        tempo_decorrido = 0.0  # Inicia o acumulador da sessão em 0 segundo usando ponto flutuante.
        leitura_anterior = inicio  # Usa o início como referência do primeiro intervalo decorrido.
        modo_manual_anterior = self.horario.modo_manual_ativo()  # Guarda em modo_manual_anterior o resultado de self.horario.modo_manual_ativo(), necessário à próxima decisão.

        if not (os.name == "nt" and sys.stdin.isatty()):  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            self._exibir_bloco(blocos, tempo_decorrido)  # Usa nesta etapa o valor ou operador específico mostrado em self._exibir_bloco(blocos, tempo_decorrido); ele participa do estado atual do método.
            while True:  # Repete o bloco até uma operação interna interromper ou concluir o fluxo.
                finalizar = input(  # Guarda em finalizar o resultado de input(, necessário à próxima decisão.
                    '\nDigite "finalizar" quando terminar sua sessão de estudo: '  # Usa nesta etapa o valor ou operador específico mostrado em '\nDigite "finalizar" quando terminar sua sessão de estudo: '; ele participa do estado atual do método.
                ).strip().casefold()  # Remove espaços das extremidades antes de validar esta entrada.
                if finalizar == "finalizar":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                    break  # Encerra o laço após a entrada ou condição estar concluída.
                print('Entrada inválida. Digite "finalizar" para encerrar a sessão.')  # Avisa que a opção não corresponde às alternativas válidas.

                atual = self.horario.obter_horario_atual()  # Registra em atual o valor self.horario.obter_horario_atual(), usado no cálculo temporal desta sessão.
                modo_manual = self.horario.modo_manual_ativo()  # Guarda em modo_manual o resultado de self.horario.modo_manual_ativo(), necessário à próxima decisão.
                if modo_manual == modo_manual_anterior:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                    tempo_decorrido += max(  # Guarda em tempo_decorrido + o resultado de max(, necessário à próxima decisão.
                        0, (atual - leitura_anterior).total_seconds()  # Usa nesta etapa o valor ou operador específico mostrado em 0, (atual - leitura_anterior).total_seconds(); ele participa do estado atual do método.
                    )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
                leitura_anterior = atual  # Guarda em leitura_anterior o resultado de atual, necessário à próxima decisão.
                modo_manual_anterior = modo_manual  # Guarda em modo_manual_anterior o resultado de modo_manual, necessário à próxima decisão.
                if total_planejado and tempo_decorrido >= total_planejado:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                    break  # Encerra o laço após a entrada ou condição estar concluída.

            fim = self.horario.obter_horario_atual()  # Registra em fim o valor self.horario.obter_horario_atual(), usado no cálculo temporal desta sessão.
            modo_manual = self.horario.modo_manual_ativo()  # Guarda em modo_manual o resultado de self.horario.modo_manual_ativo(), necessário à próxima decisão.
            if modo_manual == modo_manual_anterior:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                tempo_decorrido += max(0, (fim - leitura_anterior).total_seconds())  # Guarda em tempo_decorrido + o resultado de max(0, (fim - leitura_anterior).total_seconds()), necessário à próxima decisão.
            if total_planejado:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                tempo_decorrido = min(tempo_decorrido, total_planejado)  # Guarda em tempo_decorrido o resultado de min(tempo_decorrido, total_planejado), necessário à próxima decisão.
            return (  # Entrega ao chamador o resultado calculado por esta etapa.
                int(tempo_decorrido),  # Usa nesta etapa o valor ou operador específico mostrado em int(tempo_decorrido),; ele participa do estado atual do método.
                self._calcular_tempo_estudo(blocos, tempo_decorrido),  # Usa nesta etapa o valor ou operador específico mostrado em self._calcular_tempo_estudo(blocos, tempo_decorrido),; ele participa do estado atual do método.
                fim,  # Usa nesta etapa o valor ou operador específico mostrado em fim,; ele participa do estado atual do método.
            )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

        comando = ""  # Guarda em comando o resultado de "", necessário à próxima decisão.
        ultimo_render = 0.0  # Permite que o cronômetro faça sua primeira atualização visual imediatamente.
        while True:  # Repete o bloco até uma operação interna interromper ou concluir o fluxo.
            atual = self.horario.obter_horario_atual()  # Registra em atual o valor self.horario.obter_horario_atual(), usado no cálculo temporal desta sessão.
            modo_manual = self.horario.modo_manual_ativo()  # Guarda em modo_manual o resultado de self.horario.modo_manual_ativo(), necessário à próxima decisão.
            if modo_manual == modo_manual_anterior:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                tempo_decorrido += max(  # Guarda em tempo_decorrido + o resultado de max(, necessário à próxima decisão.
                    0, (atual - leitura_anterior).total_seconds()  # Usa nesta etapa o valor ou operador específico mostrado em 0, (atual - leitura_anterior).total_seconds(); ele participa do estado atual do método.
                )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
            leitura_anterior = atual  # Guarda em leitura_anterior o resultado de atual, necessário à próxima decisão.
            modo_manual_anterior = modo_manual  # Guarda em modo_manual_anterior o resultado de modo_manual, necessário à próxima decisão.

            if total_planejado and tempo_decorrido >= total_planejado:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                tempo_decorrido = float(total_planejado)  # Guarda em tempo_decorrido o resultado de float(total_planejado), necessário à próxima decisão.
                print("\nModelo de estudo concluído.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                break  # Encerra o laço após a entrada ou condição estar concluída.

            agora_monotonico = time.monotonic()  # Usa o relógio monotônico, não afetado por ajustes manuais da hora.
            if agora_monotonico - ultimo_render >= 1:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                self._exibir_bloco(blocos, tempo_decorrido, comando)  # Usa nesta etapa o valor ou operador específico mostrado em self._exibir_bloco(blocos, tempo_decorrido, comando); ele participa do estado atual do método.
                ultimo_render = agora_monotonico  # Guarda em ultimo_render o resultado de agora_monotonico, necessário à próxima decisão.

            if msvcrt.kbhit():  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                tecla = msvcrt.getwch()  # Guarda em tecla o resultado de msvcrt.getwch(), necessário à próxima decisão.
                if tecla == "\r":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                    if comando.strip().casefold() == "finalizar":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                        break  # Encerra o laço após a entrada ou condição estar concluída.
                    print('\nDigite "finalizar" para encerrar a sessão.')  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                    comando = ""  # Guarda em comando o resultado de "", necessário à próxima decisão.
                elif tecla == "\b":  # Testa esta alternativa somente após todas as condições anteriores falharem.
                    comando = comando[:-1]  # Guarda em comando o resultado de comando[:-1], necessário à próxima decisão.
                elif tecla == "\x03":  # Testa esta alternativa somente após todas as condições anteriores falharem.
                    raise KeyboardInterrupt  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
                elif tecla.isprintable() and len(comando) < len("finalizar"):  # Testa esta alternativa somente após todas as condições anteriores falharem.
                    comando += tecla  # Guarda em comando + o resultado de tecla, necessário à próxima decisão.
            time.sleep(0.1)  # Aguarda 100 ms para limitar consultas ao teclado e ao relógio.

        fim = self.horario.obter_horario_atual()  # Registra em fim o valor self.horario.obter_horario_atual(), usado no cálculo temporal desta sessão.
        return (  # Entrega ao chamador o resultado calculado por esta etapa.
            int(tempo_decorrido),  # Usa nesta etapa o valor ou operador específico mostrado em int(tempo_decorrido),; ele participa do estado atual do método.
            self._calcular_tempo_estudo(blocos, tempo_decorrido),  # Usa nesta etapa o valor ou operador específico mostrado em self._calcular_tempo_estudo(blocos, tempo_decorrido),; ele participa do estado atual do método.
            fim,  # Usa nesta etapa o valor ou operador específico mostrado em fim,; ele participa do estado atual do método.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

    def _exibir_bloco(  # Define _exibir_bloco, que executa a operação específica desta etapa.
        self,  # Usa nesta etapa o valor ou operador específico mostrado em self,; ele participa do estado atual do método.
        blocos: list[tuple[str, int]],  # Usa nesta etapa o valor ou operador específico mostrado em blocos: list[tuple[str, int]],; ele participa do estado atual do método.
        tempo_decorrido: float,  # Usa nesta etapa o valor ou operador específico mostrado em tempo_decorrido: float,; ele participa do estado atual do método.
        comando: str = "",  # Guarda em comando: str o resultado de "",, necessário à próxima decisão.
    ) -> None:  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        atividade, restante = self._bloco_atual(blocos, tempo_decorrido)  # Guarda em atividade, restante o resultado de self._bloco_atual(blocos, tempo_decorrido), necessário à próxima decisão.
        tipo_bloco = (  # Guarda em tipo_bloco o resultado de (, necessário à próxima decisão.
            "BLOCO DE DESCANSO"  # Usa nesta etapa o valor ou operador específico mostrado em "BLOCO DE DESCANSO"; ele participa do estado atual do método.
            if self._eh_pausa(atividade)  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            else "BLOCO DE ESTUDO"  # Usa nesta etapa o valor ou operador específico mostrado em else "BLOCO DE ESTUDO"; ele participa do estado atual do método.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        status = (  # Guarda em status o resultado de (, necessário à próxima decisão.
            f"{tipo_bloco} | {atividade} | "  # Usa nesta etapa o valor ou operador específico mostrado em f"{tipo_bloco} | {atividade} | "; ele participa do estado atual do método.
            f"{self._formatar_duracao(tempo_decorrido)}"  # Usa nesta etapa o valor ou operador específico mostrado em f"{self._formatar_duracao(tempo_decorrido)}"; ele participa do estado atual do método.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        if restante is not None:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            status += f" | Restante {self._formatar_duracao(restante)}"  # Guarda em status + o resultado de f" | Restante {self._formatar_duracao(restante)}", necessário à próxima decisão.
        status += f" | finalizar: {comando}"  # Guarda em status + o resultado de f" | finalizar: {comando}", necessário à próxima decisão.

        largura = max(2, shutil.get_terminal_size((80, 24)).columns)  # Guarda em largura o resultado de max(2, shutil.get_terminal_size((80, 24)).columns), necessário à próxima decisão.
        limite = largura - 1  # Guarda em limite o resultado de largura - 1, necessário à próxima decisão.
        if len(status) > limite:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            prefixo = f"{tipo_bloco} | "  # Guarda em prefixo o resultado de f"{tipo_bloco} | ", necessário à próxima decisão.
            sufixo = f" | {self._formatar_duracao(tempo_decorrido)}"  # Guarda em sufixo o resultado de f" | {self._formatar_duracao(tempo_decorrido)}", necessário à próxima decisão.
            if restante is not None:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                sufixo += f" | Restante {self._formatar_duracao(restante)}"  # Guarda em sufixo + o resultado de f" | Restante {self._formatar_duracao(restante)}", necessário à próxima decisão.
            sufixo += f" | finalizar: {comando}"  # Guarda em sufixo + o resultado de f" | finalizar: {comando}", necessário à próxima decisão.
            tamanho_atividade = max(0, limite - len(prefixo) - len(sufixo))  # Guarda em tamanho_atividade o resultado de max(0, limite - len(prefixo) - len(sufixo)), necessário à próxima decisão.
            status = f"{prefixo}{atividade[:tamanho_atividade]}{sufixo}"  # Guarda em status o resultado de f"{prefixo}{atividade[:tamanho_atividade]}{sufixo}", necessário à próxima decisão.
        sys.stdout.write(f"\r{status[:limite].ljust(limite)}")  # Usa nesta etapa o valor ou operador específico mostrado em sys.stdout.write(f"\r{status[:limite].ljust(limite)}"); ele participa do estado atual do método.
        sys.stdout.flush()  # Usa nesta etapa o valor ou operador específico mostrado em sys.stdout.flush(); ele participa do estado atual do método.

    @staticmethod  # Usa nesta etapa o valor ou operador específico mostrado em @staticmethod; ele participa do estado atual do método.
    def _bloco_atual(  # Define _bloco_atual, que executa a operação específica desta etapa.
        blocos: list[tuple[str, int]],  # Usa nesta etapa o valor ou operador específico mostrado em blocos: list[tuple[str, int]],; ele participa do estado atual do método.
        tempo_decorrido: float,  # Usa nesta etapa o valor ou operador específico mostrado em tempo_decorrido: float,; ele participa do estado atual do método.
    ) -> tuple[str, float | None]:  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        restante_total = max(0.0, tempo_decorrido)  # Guarda em restante_total o resultado de max(0.0, tempo_decorrido), necessário à próxima decisão.
        for atividade, duracao in blocos:  # Percorre os blocos em ordem para mostrar horário ou calcular tempo.
            if restante_total < duracao:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                return atividade, duracao - restante_total  # Entrega ao chamador o resultado calculado por esta etapa.
            restante_total -= duracao  # Guarda em restante_total - o resultado de duracao, necessário à próxima decisão.
        if blocos:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            return blocos[-1][0], 0  # Entrega ao chamador o resultado calculado por esta etapa.
        return "Estudo livre", None  # Entrega ao chamador o resultado calculado por esta etapa.

    @classmethod  # Usa nesta etapa o valor ou operador específico mostrado em @classmethod; ele participa do estado atual do método.
    def _calcular_tempo_estudo(  # Define _calcular_tempo_estudo, que executa a operação específica desta etapa.
        cls,  # Usa nesta etapa o valor ou operador específico mostrado em cls,; ele participa do estado atual do método.
        blocos: list[tuple[str, int]],  # Usa nesta etapa o valor ou operador específico mostrado em blocos: list[tuple[str, int]],; ele participa do estado atual do método.
        tempo_decorrido: float,  # Usa nesta etapa o valor ou operador específico mostrado em tempo_decorrido: float,; ele participa do estado atual do método.
    ) -> int:  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        restante = max(0.0, tempo_decorrido)  # Guarda em restante o resultado de max(0.0, tempo_decorrido), necessário à próxima decisão.
        tempo_estudo = 0.0  # Guarda em tempo_estudo o resultado de 0.0, necessário à próxima decisão.
        for atividade, duracao in blocos:  # Percorre os blocos em ordem para mostrar horário ou calcular tempo.
            tempo_bloco = min(restante, duracao)  # Guarda em tempo_bloco o resultado de min(restante, duracao), necessário à próxima decisão.
            if not cls._eh_pausa(atividade):  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                tempo_estudo += tempo_bloco  # Guarda em tempo_estudo + o resultado de tempo_bloco, necessário à próxima decisão.
            restante -= tempo_bloco  # Guarda em restante - o resultado de tempo_bloco, necessário à próxima decisão.
            if restante <= 0:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                break  # Encerra o laço após a entrada ou condição estar concluída.
        if not blocos:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            tempo_estudo = max(0.0, tempo_decorrido)  # Guarda em tempo_estudo o resultado de max(0.0, tempo_decorrido), necessário à próxima decisão.
        return int(tempo_estudo)  # Entrega ao chamador o resultado calculado por esta etapa.

    @staticmethod  # Usa nesta etapa o valor ou operador específico mostrado em @staticmethod; ele participa do estado atual do método.
    def _eh_pausa(atividade: str) -> bool:  # Define _eh_pausa, que executa a operação específica desta etapa.
        nome = atividade.casefold()  # Guarda em nome o resultado de atividade.casefold(), necessário à próxima decisão.
        return any(palavra in nome for palavra in ("pausa", "descanso", "break"))  # Entrega ao chamador o resultado calculado por esta etapa.

    @staticmethod  # Usa nesta etapa o valor ou operador específico mostrado em @staticmethod; ele participa do estado atual do método.
    def _formatar_duracao(segundos: float) -> str:  # Define _formatar_duracao, que executa a operação específica desta etapa.
        minutos, segundos_restantes = divmod(int(segundos), 60)  # Guarda em minutos, segundos_restantes o resultado de divmod(int(segundos), 60), necessário à próxima decisão.
        horas, minutos = divmod(minutos, 60)  # Guarda em horas, minutos o resultado de divmod(minutos, 60), necessário à próxima decisão.
        return f"{horas:02d}:{minutos:02d}:{segundos_restantes:02d}"  # Entrega ao chamador o resultado calculado por esta etapa.

    def _ler_disciplina(self, disciplinas: dict[str, str]) -> str:  # Define _ler_disciplina, que executa a operação específica desta etapa.
        while True:  # Repete o bloco até uma operação interna interromper ou concluir o fluxo.
            entrada = input(  # Guarda em entrada o resultado de input(, necessário à próxima decisão.
                "\nDigite a disciplina ou assunto que vai estudar: "  # Usa nesta etapa o valor ou operador específico mostrado em "\nDigite a disciplina ou assunto que vai estudar: "; ele participa do estado atual do método.
            ).strip()  # Remove espaços das extremidades antes de validar esta entrada.
            disciplina = disciplinas.get(entrada.casefold())  # Guarda em disciplina o resultado de disciplinas.get(entrada.casefold()), necessário à próxima decisão.
            if disciplina is not None:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                return disciplina  # Entrega ao chamador o resultado calculado por esta etapa.
            print("Disciplina inválida. Escolha uma das opções disponíveis.")  # Avisa que a opção não corresponde às alternativas válidas.


if __name__ == "__main__":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
    RegistroPresenca().registrar()  # Usa nesta etapa o valor ou operador específico mostrado em RegistroPresenca().registrar(); ele participa do estado atual do método.
