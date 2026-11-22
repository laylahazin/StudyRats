from datetime import datetime, timedelta  # Usa nesta etapa o valor ou operador específico mostrado em from datetime import datetime, timedelta; ele participa do estado atual do método.
from uuid import uuid4  # Usa nesta etapa o valor ou operador específico mostrado em from uuid import uuid4; ele participa do estado atual do método.

import lista  # Usa nesta etapa o valor ou operador específico mostrado em import lista; ele participa do estado atual do método.
from Dados import persistencia  # Usa nesta etapa o valor ou operador específico mostrado em from Dados import persistencia; ele participa do estado atual do método.
from Horario import GerenciadorHorario  # Usa nesta etapa o valor ou operador específico mostrado em from Horario import GerenciadorHorario; ele participa do estado atual do método.
from Ratcoins import gerenciador_ratcoins  # Usa nesta etapa o valor ou operador específico mostrado em from Ratcoins import gerenciador_ratcoins; ele participa do estado atual do método.


class GerenciadorSalas:  # Usa nesta etapa o valor ou operador específico mostrado em class GerenciadorSalas:; ele participa do estado atual do método.
    ARQUIVO_PARTICIPANTES = "participantes_salas.json"  # Nomeia participantes_salas.json como persistência das sessões e participantes.

    def __init__(  # Define __init__, que executa a operação específica desta etapa.
        self,  # Usa nesta etapa o valor ou operador específico mostrado em self,; ele participa do estado atual do método.
        horario: GerenciadorHorario | None = None,  # Guarda em horario: GerenciadorHorario | None o resultado de None,, necessário à próxima decisão.
    ) -> None:  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        self.estado = lista.estado  # Conecta o gerenciador ao estado global com login, usuários e salas.
        self.persistencia = persistencia  # Conecta o gerenciador ao módulo JSON que lê e grava dados.
        self.horario = horario or GerenciadorHorario()  # Define o relógio real ou o relógio fornecido pelos testes.

    def _intervalo_sessao(self, sala: dict, agora: datetime) -> tuple:  # Define _intervalo_sessao, que calcular início/fim da sessão e lidar com meia-noite.
        inicio_hora = datetime.strptime(sala["inicio"], "%H:%M").time()  # Converte sala["inicio"] em objeto time, por exemplo 22:00.
        fim_hora = datetime.strptime(sala["fim"], "%H:%M").time()  # Converte sala["fim"] em objeto time usado no cálculo do encerramento.
        atravessa_meia_noite = fim_hora <= inicio_hora  # Compara fim e início para identificar turnos que cruzam meia-noite.

        if atravessa_meia_noite and agora.time() < fim_hora:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            data_inicio = agora.date() - timedelta(days=1)  # Retrocede um dia para ligar início de ontem ao fim de hoje.
        else:  # Executa este ramo quando nenhuma condição anterior deste encadeamento foi atendida.
            data_inicio = agora.date()  # Mantém a data atual em sessões que não atravessam meia-noite.

        inicio = datetime.combine(data_inicio, inicio_hora)  # Combina a data calculada com o horário textual de abertura da sala.
        data_fim = data_inicio + timedelta(days=1) if atravessa_meia_noite else data_inicio  # Avança a data final um dia apenas em turnos que atravessam meia-noite.
        fim = datetime.combine(data_fim, fim_hora)  # Combina a data final com o horário textual de fechamento da sala.
        ativo = inicio <= agora < fim  # Define ativo enquanto agora está dentro do intervalo fechado/aberto da sessão.
        return inicio, fim, ativo  # Devolve início, fim e status ativo da sessão calculada.

    @staticmethod  # Usa nesta etapa o valor ou operador específico mostrado em @staticmethod; ele participa do estado atual do método.
    def _chave_sessao(inicio: datetime) -> str:  # Define _chave_sessao, que executa a operação específica desta etapa.
        return inicio.isoformat(timespec="minutes")  # Entrega ao chamador o resultado calculado por esta etapa.

    def _carregar_participacoes(self, agora: datetime) -> dict:  # Define _carregar_participacoes, que executa a operação específica desta etapa.
        participacoes = self.persistencia.carregar(self.ARQUIVO_PARTICIPANTES, {})  # Nomeia participantes_salas.json como persistência das sessões e participantes.
        if not isinstance(participacoes, dict):  # Valida o tipo do dado carregado antes de continuar o processamento.
            raise ValueError("O arquivo de participantes deve conter um objeto JSON.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.

        alterado = False  # Guarda em alterado o resultado de False, necessário à próxima decisão.
        for sala_id in list(participacoes):  # Percorre cada elemento da coleção aplicando as operações deste bloco.
            sessoes = participacoes[sala_id]  # Guarda em sessoes o resultado de participacoes[sala_id], necessário à próxima decisão.
            if not isinstance(sessoes, dict):  # Valida o tipo do dado carregado antes de continuar o processamento.
                raise ValueError(f"As sessões da sala '{sala_id}' estão inválidas.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
            for chave in list(sessoes):  # Percorre cada elemento da coleção aplicando as operações deste bloco.
                sessao = sessoes[chave]  # Obtém os dados desta sessão: participantes, dúvidas e atividades.
                fim_texto = sessao.get("fim") if isinstance(sessao, dict) else None  # Guarda em fim_texto o resultado de sessao.get("fim") if isinstance(sessao, dict) else None, necessário à próxima decisão.
                if not isinstance(fim_texto, str):  # Valida o tipo do dado carregado antes de continuar o processamento.
                    raise ValueError(  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
                        f"A sessão '{chave}' da sala '{sala_id}' está inválida."  # Usa nesta etapa o valor ou operador específico mostrado em f"A sessão '{chave}' da sala '{sala_id}' está inválida."; ele participa do estado atual do método.
                    )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
                try:  # Usa nesta etapa o valor ou operador específico mostrado em try:; ele participa do estado atual do método.
                    fim = datetime.fromisoformat(fim_texto)  # Registra em fim o valor datetime.fromisoformat(fim_texto), usado no cálculo temporal desta sessão.
                except ValueError as erro:  # Usa nesta etapa o valor ou operador específico mostrado em except ValueError as erro:; ele participa do estado atual do método.
                    raise ValueError(  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
                        f"O horário final da sessão '{chave}' está inválido."  # Usa nesta etapa o valor ou operador específico mostrado em f"O horário final da sessão '{chave}' está inválido."; ele participa do estado atual do método.
                    ) from erro  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
                if fim <= agora:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                    del sessoes[chave]  # Usa nesta etapa o valor ou operador específico mostrado em del sessoes[chave]; ele participa do estado atual do método.
                    alterado = True  # Guarda em alterado o resultado de True, necessário à próxima decisão.
            if not sessoes:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                del participacoes[sala_id]  # Usa nesta etapa o valor ou operador específico mostrado em del participacoes[sala_id]; ele participa do estado atual do método.
                alterado = True  # Guarda em alterado o resultado de True, necessário à próxima decisão.

        if alterado:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            self.persistencia.salvar(self.ARQUIVO_PARTICIPANTES, participacoes)  # Nomeia participantes_salas.json como persistência das sessões e participantes.
        return participacoes  # Entrega ao chamador o resultado calculado por esta etapa.

    def limpar_sessoes_expiradas(self) -> None:  # Define limpar_sessoes_expiradas, que executa a operação específica desta etapa.
        self._carregar_participacoes(self.horario.obter_horario_atual())  # Usa nesta etapa o valor ou operador específico mostrado em self._carregar_participacoes(self.horario.obter_horario_atual()); ele participa do estado atual do método.

    def _obter_sessao(  # Define _obter_sessao, que recuperar ou criar dados desta sessão da sala.
        self,  # Usa nesta etapa o valor ou operador específico mostrado em self,; ele participa do estado atual do método.
        participacoes: dict,  # Recebe o mapa persistido das salas e sessões envolvidas.
        sala: dict,  # Recebe a sala com id, nome, matéria, capacidade e horários.
        inicio: datetime,  # Recebe o instante inicial desta sessão da sala.
        fim: datetime,  # Recebe o instante final desta sessão da sala.
    ) -> dict:  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        sessoes_sala = participacoes.setdefault(sala["id"], {})  # Guarda em sessoes_sala o resultado de participacoes.setdefault(sala["id"], {}), necessário à próxima decisão.
        chave = self._chave_sessao(inicio)  # Guarda em chave o resultado de self._chave_sessao(inicio), necessário à próxima decisão.
        sessao = sessoes_sala.get(chave)  # Obtém os dados desta sessão: participantes, dúvidas e atividades.
        if sessao is None:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            sessao = {  # Obtém os dados desta sessão: participantes, dúvidas e atividades.
                "fim": fim.isoformat(timespec="minutes"),  # Guarda em "fim": fim.isoformat(timespec o resultado de "minutes"),, necessário à próxima decisão.
                "participantes": {},  # Cria o mapa ratname→dados de participação da sessão recém-criada.
                "duvidas": [],  # Cria a lista vazia que receberá dúvidas enviadas pelos estudantes.
                "atividades": [],  # Cria a lista vazia que receberá atividades publicadas pelo monitor.
            }  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
            sessoes_sala[chave] = sessao  # Guarda em sessoes_sala[chave] o resultado de sessao, necessário à próxima decisão.
        sessao.setdefault("duvidas", [])  # Usa nesta etapa o valor ou operador específico mostrado em sessao.setdefault("duvidas", []); ele participa do estado atual do método.
        sessao.setdefault("atividades", [])  # Usa nesta etapa o valor ou operador específico mostrado em sessao.setdefault("atividades", []); ele participa do estado atual do método.
        if not isinstance(sessao["duvidas"], list):  # Valida o tipo do dado carregado antes de continuar o processamento.
            raise ValueError(f"As dúvidas da sala '{sala['id']}' estão inválidas.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
        if not isinstance(sessao["atividades"], list):  # Valida o tipo do dado carregado antes de continuar o processamento.
            raise ValueError(f"As atividades da sala '{sala['id']}' estão inválidas.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
        return sessao  # Entrega ao chamador o resultado calculado por esta etapa.

    @staticmethod  # Usa nesta etapa o valor ou operador específico mostrado em @staticmethod; ele participa do estado atual do método.
    def _contar_participantes_ativos(participantes: dict) -> int:  # Define _contar_participantes_ativos, que executa a operação específica desta etapa.
        return sum(  # Entrega ao chamador o resultado calculado por esta etapa.
            participante["inicio_atividade"] is not None  # Usa nesta etapa o valor ou operador específico mostrado em participante["inicio_atividade"] is not None; ele participa do estado atual do método.
            and participante.get("tipo_usuario", "ESTUDANTE") != "MONITOR"  # Guarda em and participante.get("tipo_usuario", "ESTUDANTE") ! o resultado de "MONITOR", necessário à próxima decisão.
            for participante in participantes.values()  # Inspeciona cada participante para contar vagas, validar estado ou remover vencidos.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

    def listar_salas(self) -> None:  # Define listar_salas, que mostrar disponibilidade e ocupação das salas.
        agora = self.horario.obter_horario_atual()  # Registra em agora o valor self.horario.obter_horario_atual(), usado no cálculo temporal desta sessão.
        participacoes = self._carregar_participacoes(agora)  # Carrega o mapa persistido de sessões e participantes das salas.
        print(f"\n=== SALAS DE ESTUDO | {agora:%d/%m/%Y %H:%M} ===")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.

        if not self.estado.salas_disponiveis:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("Nenhuma sala de estudo disponível no momento.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return  # Retorna ao chamador e encerra o método neste ponto.

        for indice, sala in enumerate(self.estado.salas_disponiveis, start=1):  # Percorre cada elemento da coleção aplicando as operações deste bloco.
            inicio, fim, ativo = self._intervalo_sessao(sala, agora)  # Guarda em inicio, fim, ativo o resultado de self._intervalo_sessao(sala, agora), necessário à próxima decisão.
            sessao = self._obter_sessao(participacoes, sala, inicio, fim)  # Obtém os dados desta sessão: participantes, dúvidas e atividades.
            participantes = sessao["participantes"]  # Obtém o mapa ratname→dados da participação nesta sessão.
            quantidade_ativos = self._contar_participantes_ativos(participantes)  # Guarda em quantidade_ativos o resultado de self._contar_participantes_ativos(participantes), necessário à próxima decisão.
            vagas = sala["capacidade"] - quantidade_ativos  # Guarda em vagas o resultado de sala["capacidade"] - quantidade_ativos, necessário à próxima decisão.

            if not sala["ativa"]:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                status = "Indisponível"  # Guarda em status o resultado de "Indisponível", necessário à próxima decisão.
            elif ativo and vagas <= 0:  # Testa esta alternativa somente após todas as condições anteriores falharem.
                status = (  # Guarda em status o resultado de (, necessário à próxima decisão.
                    "Lotada para estudantes"  # Usa nesta etapa o valor ou operador específico mostrado em "Lotada para estudantes"; ele participa do estado atual do método.
                    if self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                    else "Lotada"  # Usa nesta etapa o valor ou operador específico mostrado em else "Lotada"; ele participa do estado atual do método.
                )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
            elif ativo:  # Testa esta alternativa somente após todas as condições anteriores falharem.
                status = "Em andamento"  # Guarda em status o resultado de "Em andamento", necessário à próxima decisão.
            else:  # Executa este ramo quando nenhuma condição anterior deste encadeamento foi atendida.
                status = "Fora do horário"  # Guarda em status o resultado de "Fora do horário", necessário à próxima decisão.

            print(  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                f"{indice}. {sala['nome']} | Matéria: {sala['materia']} | "  # Usa nesta etapa o valor ou operador específico mostrado em f"{indice}. {sala['nome']} | Matéria: {sala['materia']} | "; ele participa do estado atual do método.
                f"Horário: {sala['inicio']} - {sala['fim']} | "  # Usa nesta etapa o valor ou operador específico mostrado em f"Horário: {sala['inicio']} - {sala['fim']} | "; ele participa do estado atual do método.
                f"Monitor: {sala['monitor']} | Participantes: "  # Usa nesta etapa o valor ou operador específico mostrado em f"Monitor: {sala['monitor']} | Participantes: "; ele participa do estado atual do método.
                f"{quantidade_ativos}/{sala['capacidade']} | Status: {status}"  # Usa nesta etapa o valor ou operador específico mostrado em f"{quantidade_ativos}/{sala['capacidade']} | Status: {status}"; ele participa do estado atual do método.
            )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

        print("0. Voltar ao menu principal")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.

    def exibir_sala_de_estudo(self) -> None:  # Define exibir_sala_de_estudo, que validar conta, horário, vaga e confirmação antes da entrada.
        if self.estado.usuario_logado is None:  # Impede o recurso enquanto a conta não estiver autenticada.
            print("\nVocê precisa fazer login para acessar as salas de estudo.")  # Informa que é necessário autenticar antes de usar este recurso.
            return  # Retorna ao chamador e encerra o método neste ponto.

        ratname = self.estado.usuario_logado  # Obtém o identificador da conta conectada para vincular modelo, presença ou participação.
        tipo_usuario = self.estado.tipo_usuario_logado  # Guarda em tipo_usuario o resultado de self.estado.tipo_usuario_logado, necessário à próxima decisão.
        eh_monitor = tipo_usuario == self.estado.TIPO_MONITOR  # Guarda em eh_monitor o resultado de tipo_usuario == self.estado.TIPO_MONITOR, necessário à próxima decisão.
        if not any(  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            usuario["ratname"] == ratname for usuario in self.estado.usuarios  # Guarda em usuario["ratname"] o resultado de = ratname for usuario in self.estado.usuarios, necessário à próxima decisão.
        ):  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
            raise ValueError("O usuário conectado não existe na lista persistida de contas.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.

        self.listar_salas()  # Usa nesta etapa o valor ou operador específico mostrado em self.listar_salas(); ele participa do estado atual do método.
        escolha = input("\nEscolha uma sala para entrar (ou 0 para voltar): ").strip()  # Guarda em escolha o resultado de input("\nEscolha uma sala para entrar (ou 0 para voltar): ").strip(), necessário à próxima decisão.
        if not escolha.isdigit():  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("Opção inválida.")  # Avisa que a opção não corresponde às alternativas válidas.
            return  # Retorna ao chamador e encerra o método neste ponto.

        indice_sala = int(escolha)  # Guarda em indice_sala o resultado de int(escolha), necessário à próxima decisão.
        if indice_sala == 0:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            return  # Retorna ao chamador e encerra o método neste ponto.
        if indice_sala < 1 or indice_sala > len(self.estado.salas_disponiveis):  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("Sala inválida. Tente novamente.")  # Avisa que a opção não corresponde às alternativas válidas.
            return  # Retorna ao chamador e encerra o método neste ponto.

        sala = self.estado.salas_disponiveis[indice_sala - 1]  # Guarda em sala o resultado de self.estado.salas_disponiveis[indice_sala - 1], necessário à próxima decisão.
        agora = self.horario.obter_horario_atual()  # Registra em agora o valor self.horario.obter_horario_atual(), usado no cálculo temporal desta sessão.
        inicio, fim, ativo = self._intervalo_sessao(sala, agora)  # Guarda em inicio, fim, ativo o resultado de self._intervalo_sessao(sala, agora), necessário à próxima decisão.
        participacoes = self._carregar_participacoes(agora)  # Carrega o mapa persistido de sessões e participantes das salas.
        sessao = self._obter_sessao(participacoes, sala, inicio, fim)  # Obtém os dados desta sessão: participantes, dúvidas e atividades.
        participantes = sessao["participantes"]  # Obtém o mapa ratname→dados da participação nesta sessão.
        ja_esta_ativo = (  # Guarda em ja_esta_ativo o resultado de (, necessário à próxima decisão.
            ratname in participantes  # Usa nesta etapa o valor ou operador específico mostrado em ratname in participantes; ele participa do estado atual do método.
            and participantes[ratname]["inicio_atividade"] is not None  # Usa nesta etapa o valor ou operador específico mostrado em and participantes[ratname]["inicio_atividade"] is not None; ele participa do estado atual do método.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

        quantidade_ativos = self._contar_participantes_ativos(participantes)  # Guarda em quantidade_ativos o resultado de self._contar_participantes_ativos(participantes), necessário à próxima decisão.
        vagas = sala["capacidade"] - quantidade_ativos  # Guarda em vagas o resultado de sala["capacidade"] - quantidade_ativos, necessário à próxima decisão.
        if not sala["ativa"] or not ativo:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print(  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                f"\nA sala '{sala['nome']}' só permite entrada entre "  # Usa nesta etapa o valor ou operador específico mostrado em f"\nA sala '{sala['nome']}' só permite entrada entre "; ele participa do estado atual do método.
                f"{sala['inicio']} e {sala['fim']} "  # Usa nesta etapa o valor ou operador específico mostrado em f"{sala['inicio']} e {sala['fim']} "; ele participa do estado atual do método.
                f"(horário considerado: {agora:%H:%M})."  # Usa nesta etapa o valor ou operador específico mostrado em f"(horário considerado: {agora:%H:%M})."; ele participa do estado atual do método.
            )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
            return  # Retorna ao chamador e encerra o método neste ponto.
        if vagas <= 0 and not ja_esta_ativo and not eh_monitor:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print(f"\nA sala '{sala['nome']}' atingiu o limite de participantes.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return  # Retorna ao chamador e encerra o método neste ponto.

        self._exibir_detalhes_sala(sala, quantidade_ativos)  # Usa nesta etapa o valor ou operador específico mostrado em self._exibir_detalhes_sala(sala, quantidade_ativos); ele participa do estado atual do método.
        entrar = input(  # Guarda em entrar o resultado de input(, necessário à próxima decisão.
            '\nDigite "entrar" para participar desta sala: '  # Usa nesta etapa o valor ou operador específico mostrado em '\nDigite "entrar" para participar desta sala: '; ele participa do estado atual do método.
        ).strip().lower()  # Remove espaços das extremidades antes de validar esta entrada.
        if entrar != "entrar":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("Você decidiu não entrar na sala de estudos.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return  # Retorna ao chamador e encerra o método neste ponto.

        agora = self.horario.obter_horario_atual()  # Registra em agora o valor self.horario.obter_horario_atual(), usado no cálculo temporal desta sessão.
        inicio, fim, ativo = self._intervalo_sessao(sala, agora)  # Guarda em inicio, fim, ativo o resultado de self._intervalo_sessao(sala, agora), necessário à próxima decisão.
        if not ativo:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("O horário da sala terminou antes da confirmação da entrada.")  # Avisa que o horário acabou e que a participação já foi registrada.
            return  # Retorna ao chamador e encerra o método neste ponto.

        participacoes = self._carregar_participacoes(agora)  # Carrega o mapa persistido de sessões e participantes das salas.
        sessao = self._obter_sessao(participacoes, sala, inicio, fim)  # Obtém os dados desta sessão: participantes, dúvidas e atividades.
        participantes = sessao["participantes"]  # Obtém o mapa ratname→dados da participação nesta sessão.
        ja_esta_ativo = (  # Guarda em ja_esta_ativo o resultado de (, necessário à próxima decisão.
            ratname in participantes  # Usa nesta etapa o valor ou operador específico mostrado em ratname in participantes; ele participa do estado atual do método.
            and participantes[ratname]["inicio_atividade"] is not None  # Usa nesta etapa o valor ou operador específico mostrado em and participantes[ratname]["inicio_atividade"] is not None; ele participa do estado atual do método.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        quantidade_ativos = self._contar_participantes_ativos(participantes)  # Guarda em quantidade_ativos o resultado de self._contar_participantes_ativos(participantes), necessário à próxima decisão.
        if quantidade_ativos >= sala["capacidade"] and not ja_esta_ativo and not eh_monitor:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print(f"\nA sala '{sala['nome']}' atingiu o limite de participantes.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return  # Retorna ao chamador e encerra o método neste ponto.

        participante = participantes.get(ratname)  # Guarda em participante o resultado de participantes.get(ratname), necessário à próxima decisão.
        primeira_entrada = participante is None  # Guarda em primeira_entrada o resultado de participante is None, necessário à próxima decisão.
        if participante is None:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            participante = {  # Guarda em participante o resultado de {, necessário à próxima decisão.
                "email": next(  # Guarda o e-mail da conta localizada pelo ratname para identificar o participante.
                    usuario["email"]  # Usa nesta etapa o valor ou operador específico mostrado em usuario["email"]; ele participa do estado atual do método.
                    for usuario in self.estado.usuarios  # Percorre cada elemento da coleção aplicando as operações deste bloco.
                    if usuario["ratname"] == ratname  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
                "tipo_usuario": tipo_usuario,  # Guarda ESTUDANTE ou MONITOR para aplicar permissões e contar vagas.
                "primeira_entrada": agora.isoformat(timespec="seconds"),  # Marca o instante do primeiro ingresso desta conta nesta sessão.
                "inicio_atividade": agora.isoformat(timespec="seconds"),  # Marca o início ativo; None indica que o participante está fora da atividade.
                "tempo_total_segundos": 0,  # Inicializa ou atualiza os segundos acumulados nesta sessão.
            }  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
            participantes[ratname] = participante  # Guarda em participantes[ratname] o resultado de participante, necessário à próxima decisão.
        else:  # Executa este ramo quando nenhuma condição anterior deste encadeamento foi atendida.
            participante.setdefault("tipo_usuario", tipo_usuario)  # Usa nesta etapa o valor ou operador específico mostrado em participante.setdefault("tipo_usuario", tipo_usuario); ele participa do estado atual do método.
            if participante["inicio_atividade"] is None:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                participante["inicio_atividade"] = agora.isoformat(timespec="seconds")  # Guarda em participante["inicio_atividade"] o resultado de agora.isoformat(timespec="seconds"), necessário à próxima decisão.

        self.persistencia.salvar(self.ARQUIVO_PARTICIPANTES, participacoes)  # Nomeia participantes_salas.json como persistência das sessões e participantes.
        if primeira_entrada and tipo_usuario == self.estado.TIPO_ESTUDANTE:  # Segue somente quando o participante entra pela primeira vez nesta sessão.
            gerenciador_ratcoins.registrar_ganho(  # Usa nesta etapa o valor ou operador específico mostrado em gerenciador_ratcoins.registrar_ganho(; ele participa do estado atual do método.
                ratname,  # Usa nesta etapa o valor ou operador específico mostrado em ratname,; ele participa do estado atual do método.
                f"Entrada na sala de estudo: {sala['nome']}",  # Usa nesta etapa o valor ou operador específico mostrado em f"Entrada na sala de estudo: {sala['nome']}",; ele participa do estado atual do método.
                20,  # Usa nesta etapa o valor ou operador específico mostrado em 20,; ele participa do estado atual do método.
                evento_id=(  # Guarda em evento_id o resultado de (, necessário à próxima decisão.
                    f"sala:{sala['id']}:{self._chave_sessao(inicio)}:{ratname}"  # Usa nesta etapa o valor ou operador específico mostrado em f"sala:{sala['id']}:{self._chave_sessao(inicio)}:{ratname}"; ele participa do estado atual do método.
                ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
            )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        print(f"\n{ratname}, você entrou na sala '{sala['nome']}' com sucesso!")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        print(  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            "Você pode acompanhar a resolução de questões, enviar dúvidas "  # Usa nesta etapa o valor ou operador específico mostrado em "Você pode acompanhar a resolução de questões, enviar dúvidas "; ele participa do estado atual do método.
            "e participar da discussão."  # Usa nesta etapa o valor ou operador específico mostrado em "e participar da discussão."; ele participa do estado atual do método.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        self._interagir_com_sala(  # Usa nesta etapa o valor ou operador específico mostrado em self._interagir_com_sala(; ele participa do estado atual do método.
            sala, inicio, fim, ratname, participante, participacoes  # Usa nesta etapa o valor ou operador específico mostrado em sala, inicio, fim, ratname, participante, participacoes; ele participa do estado atual do método.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

    @staticmethod  # Usa nesta etapa o valor ou operador específico mostrado em @staticmethod; ele participa do estado atual do método.
    def _exibir_detalhes_sala(sala: dict, quantidade_ativos: int) -> None:  # Define _exibir_detalhes_sala, que executa a operação específica desta etapa.
        print(f"\n=== {sala['nome']} ===")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        print(f"Matéria: {sala['materia']}")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        print(f"Descrição: {sala['descricao']}")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        print(f"Monitor responsável: {sala['monitor']}")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        print(f"Horário: {sala['inicio']} - {sala['fim']}")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        print(f"Participantes: {quantidade_ativos}/{sala['capacidade']}")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.

    def _interagir_com_sala(  # Define _interagir_com_sala, que executa a operação específica desta etapa.
        self,  # Usa nesta etapa o valor ou operador específico mostrado em self,; ele participa do estado atual do método.
        sala: dict,  # Recebe a sala com id, nome, matéria, capacidade e horários.
        inicio: datetime,  # Recebe o instante inicial desta sessão da sala.
        fim: datetime,  # Recebe o instante final desta sessão da sala.
        ratname: str,  # Recebe o identificador da conta participante.
        participante: dict,  # Recebe os dados ativos e o tempo acumulado deste participante.
        participacoes: dict,  # Recebe o mapa persistido das salas e sessões envolvidas.
    ) -> None:  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        eh_monitor = self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR  # Guarda em eh_monitor o resultado de self.estado.tipo_usuario_logado == self.estado.TIPO_MONITOR, necessário à próxima decisão.
        while True:  # Repete o bloco até uma operação interna interromper ou concluir o fluxo.
            print("\nOpções da sala:")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            print("1. Ver atividades e dúvidas")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            if eh_monitor:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                print("2. Criar atividade")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                print("3. Responder dúvida")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                print("4. Participar da discussão")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                print("5. Sair da sala")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            else:  # Executa este ramo quando nenhuma condição anterior deste encadeamento foi atendida.
                print("2. Enviar dúvida")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                print("3. Participar da discussão")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                print("4. Sair da sala")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.

            opcao = input("Escolha uma opção: ").strip()  # Guarda em opcao o resultado de input("Escolha uma opção: ").strip(), necessário à próxima decisão.
            agora = self.horario.obter_horario_atual()  # Registra em agora o valor self.horario.obter_horario_atual(), usado no cálculo temporal desta sessão.
            if agora >= fim:  # Impede nova ação depois que o horário final da sala foi atingido.
                self._finalizar_atividade(participante, fim)  # Usa nesta etapa o valor ou operador específico mostrado em self._finalizar_atividade(participante, fim); ele participa do estado atual do método.
                self._carregar_participacoes(agora)  # Usa nesta etapa o valor ou operador específico mostrado em self._carregar_participacoes(agora); ele participa do estado atual do método.
                print("\nO horário da sala terminou. Sua participação foi registrada.")  # Avisa que o horário acabou e que a participação já foi registrada.
                return  # Retorna ao chamador e encerra o método neste ponto.

            if opcao == "1":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                participacoes = self._carregar_participacoes(agora)  # Carrega o mapa persistido de sessões e participantes das salas.
                sessao = self._obter_sessao(participacoes, sala, inicio, fim)  # Obtém os dados desta sessão: participantes, dúvidas e atividades.
                self._exibir_atividades_e_duvidas(sala, sessao)  # Usa nesta etapa o valor ou operador específico mostrado em self._exibir_atividades_e_duvidas(sala, sessao); ele participa do estado atual do método.
            elif eh_monitor and opcao == "2":  # Testa esta alternativa somente após todas as condições anteriores falharem.
                if self._criar_atividade(  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                    sala, inicio, fim, ratname, participante  # Usa nesta etapa o valor ou operador específico mostrado em sala, inicio, fim, ratname, participante; ele participa do estado atual do método.
                ):  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
                    return  # Retorna ao chamador e encerra o método neste ponto.
            elif eh_monitor and opcao == "3":  # Testa esta alternativa somente após todas as condições anteriores falharem.
                if self._responder_duvida(  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                    sala, inicio, fim, ratname, participante  # Usa nesta etapa o valor ou operador específico mostrado em sala, inicio, fim, ratname, participante; ele participa do estado atual do método.
                ):  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
                    return  # Retorna ao chamador e encerra o método neste ponto.
            elif (eh_monitor and opcao == "4") or (not eh_monitor and opcao == "3"):  # Testa esta alternativa somente após todas as condições anteriores falharem.
                print(f"{ratname} participou da discussão da sala.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            elif (eh_monitor and opcao == "5") or (not eh_monitor and opcao == "4"):  # Testa esta alternativa somente após todas as condições anteriores falharem.
                self._sair_da_sala(  # Usa nesta etapa o valor ou operador específico mostrado em self._sair_da_sala(; ele participa do estado atual do método.
                    sala, inicio, ratname, participante, participacoes, agora  # Usa nesta etapa o valor ou operador específico mostrado em sala, inicio, ratname, participante, participacoes, agora; ele participa do estado atual do método.
                )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
                return  # Retorna ao chamador e encerra o método neste ponto.
            elif not eh_monitor and opcao == "2":  # Testa esta alternativa somente após todas as condições anteriores falharem.
                if self._enviar_duvida(sala, inicio, fim, ratname, participante):  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                    return  # Retorna ao chamador e encerra o método neste ponto.
            else:  # Executa este ramo quando nenhuma condição anterior deste encadeamento foi atendida.
                print("Opção inválida. Tente novamente.")  # Avisa que a opção não corresponde às alternativas válidas.

    def _exibir_atividades_e_duvidas(self, sala: dict, sessao: dict) -> None:  # Define _exibir_atividades_e_duvidas, que executa a operação específica desta etapa.
        print(f"\n=== Atividades: {sala['nome']} ===")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        atividades = sessao["atividades"]  # Guarda em atividades o resultado de sessao["atividades"], necessário à próxima decisão.
        if not atividades:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("Ainda não há atividades cadastradas nesta sessão.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        for indice, atividade in enumerate(atividades, start=1):  # Percorre cada elemento da coleção aplicando as operações deste bloco.
            print(f"{indice}. {atividade['titulo']}")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            print(f"   Descrição: {atividade['descricao']}")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            print(f"   Criada por: {atividade['monitor']}")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            print(f"   Horário: {atividade['horario']}")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.

        print("\n=== Dúvidas e respostas ===")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        duvidas = sessao["duvidas"]  # Guarda em duvidas o resultado de sessao["duvidas"], necessário à próxima decisão.
        if not duvidas:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("Ainda não há dúvidas nesta sessão.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        for indice, duvida in enumerate(duvidas, start=1):  # Percorre dúvidas ou respostas desta sessão para apresentá-las ao usuário.
            print(  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                f"{indice}. {duvida['usuario']} perguntou "  # Usa nesta etapa o valor ou operador específico mostrado em f"{indice}. {duvida['usuario']} perguntou "; ele participa do estado atual do método.
                f"({duvida['horario']}): {duvida['mensagem']}"  # Usa nesta etapa o valor ou operador específico mostrado em f"({duvida['horario']}): {duvida['mensagem']}"; ele participa do estado atual do método.
            )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
            respostas = duvida.get("respostas", [])  # Guarda em respostas o resultado de duvida.get("respostas", []), necessário à próxima decisão.
            if not isinstance(respostas, list):  # Valida o tipo do dado carregado antes de continuar o processamento.
                raise ValueError(f"As respostas da dúvida {indice} estão inválidas.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
            if not respostas:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                print("   Ainda sem resposta.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            for resposta in respostas:  # Percorre dúvidas ou respostas desta sessão para apresentá-las ao usuário.
                print(  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                    f"   {resposta['usuario']} respondeu "  # Usa nesta etapa o valor ou operador específico mostrado em f"   {resposta['usuario']} respondeu "; ele participa do estado atual do método.
                    f"({resposta['horario']}): {resposta['mensagem']}"  # Usa nesta etapa o valor ou operador específico mostrado em f"({resposta['horario']}): {resposta['mensagem']}"; ele participa do estado atual do método.
                )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

    def _criar_atividade(  # Define _criar_atividade, que publicar uma atividade do monitor e conceder 5 RatCoins.
        self,  # Usa nesta etapa o valor ou operador específico mostrado em self,; ele participa do estado atual do método.
        sala: dict,  # Recebe a sala com id, nome, matéria, capacidade e horários.
        inicio: datetime,  # Recebe o instante inicial desta sessão da sala.
        fim: datetime,  # Recebe o instante final desta sessão da sala.
        ratname: str,  # Recebe o identificador da conta participante.
        participante: dict,  # Recebe os dados ativos e o tempo acumulado deste participante.
    ) -> bool:  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        if self.estado.tipo_usuario_logado != self.estado.TIPO_MONITOR:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("Somente monitores podem criar atividades.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return False  # Entrega ao chamador o resultado calculado por esta etapa.

        titulo = input("Título da atividade: ").strip()  # Guarda em titulo o resultado de input("Título da atividade: ").strip(), necessário à próxima decisão.
        if not titulo:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("O título da atividade não pode ficar vazio.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return False  # Entrega ao chamador o resultado calculado por esta etapa.
        descricao = input("Descrição da atividade: ").strip()  # Guarda em descricao o resultado de input("Descrição da atividade: ").strip(), necessário à próxima decisão.
        if not descricao:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("A descrição da atividade não pode ficar vazia.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return False  # Entrega ao chamador o resultado calculado por esta etapa.

        agora = self.horario.obter_horario_atual()  # Registra em agora o valor self.horario.obter_horario_atual(), usado no cálculo temporal desta sessão.
        if agora >= fim:  # Impede nova ação depois que o horário final da sala foi atingido.
            self._finalizar_atividade(participante, fim)  # Usa nesta etapa o valor ou operador específico mostrado em self._finalizar_atividade(participante, fim); ele participa do estado atual do método.
            self._carregar_participacoes(agora)  # Usa nesta etapa o valor ou operador específico mostrado em self._carregar_participacoes(agora); ele participa do estado atual do método.
            print("\nO horário da sala terminou. Sua participação foi registrada.")  # Avisa que o horário acabou e que a participação já foi registrada.
            return True  # Entrega ao chamador o resultado calculado por esta etapa.

        participacoes = self.persistencia.carregar(self.ARQUIVO_PARTICIPANTES, {})  # Nomeia participantes_salas.json como persistência das sessões e participantes.
        sessao = self._obter_sessao(participacoes, sala, inicio, fim)  # Obtém os dados desta sessão: participantes, dúvidas e atividades.
        atividade_id = uuid4().hex  # Guarda em atividade_id o resultado de uuid4().hex, necessário à próxima decisão.
        sessao["atividades"].append(  # Adiciona à lista o registro criado nesta etapa.
            {  # Usa nesta etapa o valor ou operador específico mostrado em {; ele participa do estado atual do método.
                "id": atividade_id,  # Usa nesta etapa o valor ou operador específico mostrado em "id": atividade_id,; ele participa do estado atual do método.
                "titulo": titulo,  # Usa nesta etapa o valor ou operador específico mostrado em "titulo": titulo,; ele participa do estado atual do método.
                "descricao": descricao,  # Usa nesta etapa o valor ou operador específico mostrado em "descricao": descricao,; ele participa do estado atual do método.
                "monitor": ratname,  # Usa nesta etapa o valor ou operador específico mostrado em "monitor": ratname,; ele participa do estado atual do método.
                "horario": agora.isoformat(timespec="seconds"),  # Guarda em "horario": agora.isoformat(timespec o resultado de "seconds"),, necessário à próxima decisão.
            }  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        self.persistencia.salvar(self.ARQUIVO_PARTICIPANTES, participacoes)  # Nomeia participantes_salas.json como persistência das sessões e participantes.
        print("Atividade criada e disponibilizada para os estudantes da sala.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        gerenciador_ratcoins.registrar_ganho(  # Usa nesta etapa o valor ou operador específico mostrado em gerenciador_ratcoins.registrar_ganho(; ele participa do estado atual do método.
            ratname,  # Usa nesta etapa o valor ou operador específico mostrado em ratname,; ele participa do estado atual do método.
            f"Publicar atividade: {titulo}",  # Usa nesta etapa o valor ou operador específico mostrado em f"Publicar atividade: {titulo}",; ele participa do estado atual do método.
            5,  # Usa nesta etapa o valor ou operador específico mostrado em 5,; ele participa do estado atual do método.
            evento_id=f"atividade-monitor:{atividade_id}",  # Guarda em evento_id o resultado de f"atividade-monitor:{atividade_id}",, necessário à próxima decisão.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        return False  # Entrega ao chamador o resultado calculado por esta etapa.

    def _responder_duvida(  # Define _responder_duvida, que anexar uma resposta do monitor a uma dúvida.
        self,  # Usa nesta etapa o valor ou operador específico mostrado em self,; ele participa do estado atual do método.
        sala: dict,  # Recebe a sala com id, nome, matéria, capacidade e horários.
        inicio: datetime,  # Recebe o instante inicial desta sessão da sala.
        fim: datetime,  # Recebe o instante final desta sessão da sala.
        ratname: str,  # Recebe o identificador da conta participante.
        participante: dict,  # Recebe os dados ativos e o tempo acumulado deste participante.
    ) -> bool:  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        if self.estado.tipo_usuario_logado != self.estado.TIPO_MONITOR:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("Somente monitores podem responder dúvidas.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return False  # Entrega ao chamador o resultado calculado por esta etapa.

        participacoes = self.persistencia.carregar(self.ARQUIVO_PARTICIPANTES, {})  # Nomeia participantes_salas.json como persistência das sessões e participantes.
        sessao = self._obter_sessao(participacoes, sala, inicio, fim)  # Obtém os dados desta sessão: participantes, dúvidas e atividades.
        duvidas = sessao["duvidas"]  # Guarda em duvidas o resultado de sessao["duvidas"], necessário à próxima decisão.
        if not duvidas:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("Ainda não há dúvidas para responder nesta sala.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return False  # Entrega ao chamador o resultado calculado por esta etapa.

        print("\nDúvidas recebidas:")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        for indice, duvida in enumerate(duvidas, start=1):  # Percorre dúvidas ou respostas desta sessão para apresentá-las ao usuário.
            print(  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                f"{indice}. {duvida['usuario']}: {duvida['mensagem']}"  # Usa nesta etapa o valor ou operador específico mostrado em f"{indice}. {duvida['usuario']}: {duvida['mensagem']}"; ele participa do estado atual do método.
            )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
            for resposta in duvida.get("respostas", []):  # Percorre dúvidas ou respostas desta sessão para apresentá-las ao usuário.
                print(  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                    f"   Resposta de {resposta['usuario']}: "  # Usa nesta etapa o valor ou operador específico mostrado em f"   Resposta de {resposta['usuario']}: "; ele participa do estado atual do método.
                    f"{resposta['mensagem']}"  # Usa nesta etapa o valor ou operador específico mostrado em f"{resposta['mensagem']}"; ele participa do estado atual do método.
                )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

        escolha = input(  # Guarda em escolha o resultado de input(, necessário à próxima decisão.
            "Número da dúvida para responder (ou 0 para voltar): "  # Usa nesta etapa o valor ou operador específico mostrado em "Número da dúvida para responder (ou 0 para voltar): "; ele participa do estado atual do método.
        ).strip()  # Remove espaços das extremidades antes de validar esta entrada.
        if escolha == "0":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            return False  # Entrega ao chamador o resultado calculado por esta etapa.
        if not escolha.isdigit() or not 1 <= int(escolha) <= len(duvidas):  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("Número de dúvida inválido.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return False  # Entrega ao chamador o resultado calculado por esta etapa.

        mensagem = input("Digite sua resposta: ").strip()  # Guarda em mensagem o resultado de input("Digite sua resposta: ").strip(), necessário à próxima decisão.
        if not mensagem:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("A resposta não pode ficar vazia.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return False  # Entrega ao chamador o resultado calculado por esta etapa.

        agora = self.horario.obter_horario_atual()  # Registra em agora o valor self.horario.obter_horario_atual(), usado no cálculo temporal desta sessão.
        if agora >= fim:  # Impede nova ação depois que o horário final da sala foi atingido.
            self._finalizar_atividade(participante, fim)  # Usa nesta etapa o valor ou operador específico mostrado em self._finalizar_atividade(participante, fim); ele participa do estado atual do método.
            self._carregar_participacoes(agora)  # Usa nesta etapa o valor ou operador específico mostrado em self._carregar_participacoes(agora); ele participa do estado atual do método.
            print("\nO horário da sala terminou. Sua participação foi registrada.")  # Avisa que o horário acabou e que a participação já foi registrada.
            return True  # Entrega ao chamador o resultado calculado por esta etapa.

        participacoes = self.persistencia.carregar(self.ARQUIVO_PARTICIPANTES, {})  # Nomeia participantes_salas.json como persistência das sessões e participantes.
        sessao = self._obter_sessao(participacoes, sala, inicio, fim)  # Obtém os dados desta sessão: participantes, dúvidas e atividades.
        indice_duvida = int(escolha) - 1  # Guarda em indice_duvida o resultado de int(escolha) - 1, necessário à próxima decisão.
        if indice_duvida >= len(sessao["duvidas"]):  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            raise ValueError("A dúvida selecionada não existe mais nesta sessão.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
        duvida = sessao["duvidas"][indice_duvida]  # Guarda em duvida o resultado de sessao["duvidas"][indice_duvida], necessário à próxima decisão.
        respostas = duvida.setdefault("respostas", [])  # Guarda em respostas o resultado de duvida.setdefault("respostas", []), necessário à próxima decisão.
        if not isinstance(respostas, list):  # Valida o tipo do dado carregado antes de continuar o processamento.
            raise ValueError("As respostas da dúvida selecionada estão inválidas.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
        respostas.append(  # Adiciona à lista o registro criado nesta etapa.
            {  # Usa nesta etapa o valor ou operador específico mostrado em {; ele participa do estado atual do método.
                "usuario": ratname,  # Usa nesta etapa o valor ou operador específico mostrado em "usuario": ratname,; ele participa do estado atual do método.
                "mensagem": mensagem,  # Usa nesta etapa o valor ou operador específico mostrado em "mensagem": mensagem,; ele participa do estado atual do método.
                "horario": agora.isoformat(timespec="seconds"),  # Guarda em "horario": agora.isoformat(timespec o resultado de "seconds"),, necessário à próxima decisão.
            }  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        self.persistencia.salvar(self.ARQUIVO_PARTICIPANTES, participacoes)  # Nomeia participantes_salas.json como persistência das sessões e participantes.
        print("Resposta enviada. Os estudantes podem consultá-la na sala.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        return False  # Entrega ao chamador o resultado calculado por esta etapa.

    def _enviar_duvida(  # Define _enviar_duvida, que publicar uma dúvida do estudante ao monitor.
        self,  # Usa nesta etapa o valor ou operador específico mostrado em self,; ele participa do estado atual do método.
        sala: dict,  # Recebe a sala com id, nome, matéria, capacidade e horários.
        inicio: datetime,  # Recebe o instante inicial desta sessão da sala.
        fim: datetime,  # Recebe o instante final desta sessão da sala.
        ratname: str,  # Recebe o identificador da conta participante.
        participante: dict,  # Recebe os dados ativos e o tempo acumulado deste participante.
    ) -> bool:  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        if self.estado.tipo_usuario_logado != self.estado.TIPO_ESTUDANTE:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("Somente estudantes podem enviar dúvidas.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return False  # Entrega ao chamador o resultado calculado por esta etapa.

        duvida = input("Digite sua dúvida para o monitor: ").strip()  # Guarda em duvida o resultado de input("Digite sua dúvida para o monitor: ").strip(), necessário à próxima decisão.
        agora = self.horario.obter_horario_atual()  # Registra em agora o valor self.horario.obter_horario_atual(), usado no cálculo temporal desta sessão.
        if agora >= fim:  # Impede nova ação depois que o horário final da sala foi atingido.
            self._finalizar_atividade(participante, fim)  # Usa nesta etapa o valor ou operador específico mostrado em self._finalizar_atividade(participante, fim); ele participa do estado atual do método.
            self._carregar_participacoes(agora)  # Usa nesta etapa o valor ou operador específico mostrado em self._carregar_participacoes(agora); ele participa do estado atual do método.
            print("\nO horário da sala terminou. Sua participação foi registrada.")  # Avisa que o horário acabou e que a participação já foi registrada.
            return True  # Entrega ao chamador o resultado calculado por esta etapa.
        if not duvida:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("Você precisa escrever uma dúvida antes de enviar.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return False  # Entrega ao chamador o resultado calculado por esta etapa.

        participacoes = self.persistencia.carregar(self.ARQUIVO_PARTICIPANTES, {})  # Nomeia participantes_salas.json como persistência das sessões e participantes.
        sessao = participacoes[sala["id"]][self._chave_sessao(inicio)]  # Obtém os dados desta sessão: participantes, dúvidas e atividades.
        sessao["duvidas"].append(  # Adiciona à lista o registro criado nesta etapa.
            {  # Usa nesta etapa o valor ou operador específico mostrado em {; ele participa do estado atual do método.
                "usuario": ratname,  # Usa nesta etapa o valor ou operador específico mostrado em "usuario": ratname,; ele participa do estado atual do método.
                "mensagem": duvida,  # Usa nesta etapa o valor ou operador específico mostrado em "mensagem": duvida,; ele participa do estado atual do método.
                "horario": agora.isoformat(timespec="seconds"),  # Guarda em "horario": agora.isoformat(timespec o resultado de "seconds"),, necessário à próxima decisão.
                "respostas": [],  # Usa nesta etapa o valor ou operador específico mostrado em "respostas": [],; ele participa do estado atual do método.
            }  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        self.persistencia.salvar(self.ARQUIVO_PARTICIPANTES, participacoes)  # Nomeia participantes_salas.json como persistência das sessões e participantes.
        print("Sua dúvida foi enviada ao monitor.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        return False  # Entrega ao chamador o resultado calculado por esta etapa.

    def _sair_da_sala(  # Define _sair_da_sala, que fechar atividade, salvar tempo ativo e liberar vaga.
        self,  # Usa nesta etapa o valor ou operador específico mostrado em self,; ele participa do estado atual do método.
        sala: dict,  # Recebe a sala com id, nome, matéria, capacidade e horários.
        inicio: datetime,  # Recebe o instante inicial desta sessão da sala.
        ratname: str,  # Recebe o identificador da conta participante.
        participante: dict,  # Recebe os dados ativos e o tempo acumulado deste participante.
        participacoes: dict,  # Recebe o mapa persistido das salas e sessões envolvidas.
        agora: datetime,  # Recebe o horário efetivo usado para validar ou atualizar a sessão.
    ) -> None:  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        self._finalizar_atividade(participante, agora)  # Usa nesta etapa o valor ou operador específico mostrado em self._finalizar_atividade(participante, agora); ele participa do estado atual do método.
        participacoes = self.persistencia.carregar(self.ARQUIVO_PARTICIPANTES, {})  # Nomeia participantes_salas.json como persistência das sessões e participantes.
        sessao = participacoes[sala["id"]][self._chave_sessao(inicio)]  # Obtém os dados desta sessão: participantes, dúvidas e atividades.
        sessao["participantes"][ratname] = participante  # Guarda em sessao["participantes"][ratname] o resultado de participante, necessário à próxima decisão.
        self.persistencia.salvar(self.ARQUIVO_PARTICIPANTES, participacoes)  # Nomeia participantes_salas.json como persistência das sessões e participantes.

        tempo_total = participante["tempo_total_segundos"]  # Lê o acumulado antes de convertê-lo em horas, minutos e segundos.
        horas, resto = divmod(tempo_total, 3600)  # Separa o acumulado em horas inteiras e o restante usado por minutos.
        minutos, segundos = divmod(resto, 60)  # Converte o restante em minutos inteiros e segundos da saída.
        print(f"\nVocê saiu da sala '{sala['nome']}' com sucesso.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        print(f"Tempo ativo nesta sessão: {horas}h {minutos}m {segundos}s")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        print(  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            "Sua vaga foi liberada. O histórico da sessão permanece salvo "  # Usa nesta etapa o valor ou operador específico mostrado em "Sua vaga foi liberada. O histórico da sessão permanece salvo "; ele participa do estado atual do método.
            "até o horário da sala acabar."  # Usa nesta etapa o valor ou operador específico mostrado em "até o horário da sala acabar."; ele participa do estado atual do método.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

    @staticmethod  # Usa nesta etapa o valor ou operador específico mostrado em @staticmethod; ele participa do estado atual do método.
    def _finalizar_atividade(participante: dict, horario_fim: datetime) -> None:  # Define _finalizar_atividade, que acumular o período ativo até o horário informado.
        inicio_atividade = participante["inicio_atividade"]  # Obtém o instante em que o período ativo atual começou.
        if inicio_atividade is None:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            return  # Retorna ao chamador e encerra o método neste ponto.

        inicio = datetime.fromisoformat(inicio_atividade)  # Reconstrói o datetime ativo a partir do texto ISO persistido.
        segundos = max(0, int((horario_fim - inicio).total_seconds()))  # Calcula duração não negativa convertendo a diferença para segundos inteiros.
        participante["tempo_total_segundos"] += segundos  # Guarda em participante["tempo_total_segundos"] + o resultado de segundos, necessário à próxima decisão.
        participante["inicio_atividade"] = None  # Guarda em participante["inicio_atividade"] o resultado de None, necessário à próxima decisão.
