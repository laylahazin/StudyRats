import lista  # Usa nesta etapa o valor ou operador específico mostrado em import lista; ele participa do estado atual do método.
from Dados import persistencia  # Usa nesta etapa o valor ou operador específico mostrado em from Dados import persistencia; ele participa do estado atual do método.


class GerenciadorModelosEstudo:  # Usa nesta etapa o valor ou operador específico mostrado em class GerenciadorModelosEstudo:; ele participa do estado atual do método.
    ARQUIVO_MODELOS = "modelos_estudo.json"  # Nomeia modelos_estudo.json como arquivo dos planos confirmados por conta.

    MODELOS_PREDEFINIDOS = {  # Armazena os quatro planos e seus blocos configurados em minutos.
        "1": {  # Usa nesta etapa o valor ou operador específico mostrado em "1": {; ele participa do estado atual do método.
            "nome": "Pomodoro",  # Usa nesta etapa o valor ou operador específico mostrado em "nome": "Pomodoro",; ele participa do estado atual do método.
            "blocos": [("Estudo", 25), ("Pausa", 5)] * 3  # Usa nesta etapa o valor ou operador específico mostrado em "blocos": [("Estudo", 25), ("Pausa", 5)] * 3; ele participa do estado atual do método.
            + [("Estudo", 25), ("Pausa longa", 15)],  # Usa nesta etapa o valor ou operador específico mostrado em + [("Estudo", 25), ("Pausa longa", 15)],; ele participa do estado atual do método.
        },  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        "2": {  # Usa nesta etapa o valor ou operador específico mostrado em "2": {; ele participa do estado atual do método.
            "nome": "Estudo aprofundado",  # Usa nesta etapa o valor ou operador específico mostrado em "nome": "Estudo aprofundado",; ele participa do estado atual do método.
            "blocos": [("Estudo", 50), ("Pausa", 10)] * 3,  # Usa nesta etapa o valor ou operador específico mostrado em "blocos": [("Estudo", 50), ("Pausa", 10)] * 3,; ele participa do estado atual do método.
        },  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        "3": {  # Usa nesta etapa o valor ou operador específico mostrado em "3": {; ele participa do estado atual do método.
            "nome": "Revisão e exercícios",  # Usa nesta etapa o valor ou operador específico mostrado em "nome": "Revisão e exercícios",; ele participa do estado atual do método.
            "blocos": [  # Usa nesta etapa o valor ou operador específico mostrado em "blocos": [; ele participa do estado atual do método.
                ("Revisão do conteúdo", 30),  # Usa nesta etapa o valor ou operador específico mostrado em ("Revisão do conteúdo", 30),; ele participa do estado atual do método.
                ("Pausa", 5),  # Usa nesta etapa o valor ou operador específico mostrado em ("Pausa", 5),; ele participa do estado atual do método.
                ("Resolução de exercícios", 30),  # Usa nesta etapa o valor ou operador específico mostrado em ("Resolução de exercícios", 30),; ele participa do estado atual do método.
                ("Pausa", 5),  # Usa nesta etapa o valor ou operador específico mostrado em ("Pausa", 5),; ele participa do estado atual do método.
                ("Resumo final", 20),  # Usa nesta etapa o valor ou operador específico mostrado em ("Resumo final", 20),; ele participa do estado atual do método.
            ],  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        },  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
        "4": {  # Usa nesta etapa o valor ou operador específico mostrado em "4": {; ele participa do estado atual do método.
            "nome": "Sessão curta",  # Usa nesta etapa o valor ou operador específico mostrado em "nome": "Sessão curta",; ele participa do estado atual do método.
            "blocos": [("Estudo", 20), ("Pausa", 5)] * 2  # Usa nesta etapa o valor ou operador específico mostrado em "blocos": [("Estudo", 20), ("Pausa", 5)] * 2; ele participa do estado atual do método.
            + [("Estudo", 20)],  # Usa nesta etapa o valor ou operador específico mostrado em + [("Estudo", 20)],; ele participa do estado atual do método.
        },  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    }  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

    def __init__(self, estado=None, repositorio=None) -> None:  # Define __init__, que executa a operação específica desta etapa.
        self.estado = estado if estado is not None else lista.estado  # Conecta o gerenciador ao estado global com login, usuários e salas.
        self.repositorio = repositorio if repositorio is not None else persistencia  # Atualiza self.repositorio com repositorio if repositorio is not None else persistencia, estado usado nas operações seguintes.

    @staticmethod  # Usa nesta etapa o valor ou operador específico mostrado em @staticmethod; ele participa do estado atual do método.
    def _ler_duracao(pergunta: str, minimo: int, maximo: int) -> int:  # Define _ler_duracao, que executa a operação específica desta etapa.
        while True:  # Repete o bloco até uma operação interna interromper ou concluir o fluxo.
            resposta = input(pergunta).strip()  # Guarda em resposta o resultado de input(pergunta).strip(), necessário à próxima decisão.
            if resposta.isdigit() and minimo <= int(resposta) <= maximo:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                return int(resposta)  # Entrega ao chamador o resultado calculado por esta etapa.
            print(f"Informe um número entre {minimo} e {maximo}.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.

    def _criar_modelo_personalizado(self) -> dict:  # Define _criar_modelo_personalizado, que executa a operação específica desta etapa.
        while True:  # Repete o bloco até uma operação interna interromper ou concluir o fluxo.
            tema = input("Qual assunto você vai estudar? ").strip()  # Guarda em tema o resultado de input("Qual assunto você vai estudar? ").strip(), necessário à próxima decisão.
            if tema:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                break  # Encerra o laço após a entrada ou condição estar concluída.
            print("O assunto não pode ficar vazio.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.

        duracao = self._ler_duracao("Duração de cada bloco de estudo (minutos, 1-180): ", 1, 180)  # Guarda em duracao o resultado de self._ler_duracao("Duração de cada bloco de estudo (minutos, 1-180): ", 1, 180), necessário à próxima decisão.
        pausa = self._ler_duracao("Duração das pausas (minutos, 1-60): ", 1, 60)  # Guarda em pausa o resultado de self._ler_duracao("Duração das pausas (minutos, 1-60): ", 1, 60), necessário à próxima decisão.
        quantidade = self._ler_duracao("Quantidade de blocos de estudo (1-8): ", 1, 8)  # Guarda em quantidade o resultado de self._ler_duracao("Quantidade de blocos de estudo (1-8): ", 1, 8), necessário à próxima decisão.
        blocos = []  # Armazena a sequência de estudo e pausa usada pelo cronômetro.
        for indice in range(quantidade):  # Percorre cada elemento da coleção aplicando as operações deste bloco.
            blocos.append((f"Estudo: {tema}", duracao))  # Adiciona à lista o registro criado nesta etapa.
            if indice < quantidade - 1:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.

                blocos.append(("Pausa", pausa))  # Adiciona à lista o registro criado nesta etapa.
        return {"nome": f"Plano personalizado: {tema}", "blocos": blocos}  # Entrega ao chamador o resultado calculado por esta etapa.

    def _salvar_modelo(self, ratname: str, modelo: dict) -> None:  # Define _salvar_modelo, que executa a operação específica desta etapa.
        planos = self.repositorio.carregar(self.ARQUIVO_MODELOS, {})  # Nomeia modelos_estudo.json como arquivo dos planos confirmados por conta.
        if not isinstance(planos, dict):  # Valida o tipo do dado carregado antes de continuar o processamento.
            raise ValueError("O arquivo de modelos de estudo deve conter um objeto JSON.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
        modelo_confirmado = dict(modelo)  # Guarda em modelo_confirmado o resultado de dict(modelo), necessário à próxima decisão.
        modelo_confirmado["confirmado"] = True  # Guarda em modelo_confirmado["confirmado"] o resultado de True, necessário à próxima decisão.
        planos[ratname] = modelo_confirmado  # Guarda em planos[ratname] o resultado de modelo_confirmado, necessário à próxima decisão.
        self.repositorio.salvar(self.ARQUIVO_MODELOS, planos)  # Nomeia modelos_estudo.json como arquivo dos planos confirmados por conta.

    @staticmethod  # Usa nesta etapa o valor ou operador específico mostrado em @staticmethod; ele participa do estado atual do método.
    def _exibir_modelo(modelo: dict) -> None:  # Define _exibir_modelo, que executa a operação específica desta etapa.
        print(f"\n=== {modelo['nome']} ===")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        horario_minuto = 0  # Guarda em horario_minuto o resultado de 0, necessário à próxima decisão.
        for indice, (atividade, duracao) in enumerate(modelo["blocos"], start=1):  # Percorre os blocos em ordem para mostrar horário ou calcular tempo.
            fim_minuto = horario_minuto + duracao  # Guarda em fim_minuto o resultado de horario_minuto + duracao, necessário à próxima decisão.
            print(  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                f"{indice}. {atividade}: "  # Usa nesta etapa o valor ou operador específico mostrado em f"{indice}. {atividade}: "; ele participa do estado atual do método.

                f"{horario_minuto // 60:02d}:{horario_minuto % 60:02d} - "  # Usa nesta etapa o valor ou operador específico mostrado em f"{horario_minuto // 60:02d}:{horario_minuto % 60:02d} - "; ele participa do estado atual do método.
                f"{fim_minuto // 60:02d}:{fim_minuto % 60:02d} "  # Usa nesta etapa o valor ou operador específico mostrado em f"{fim_minuto // 60:02d}:{fim_minuto % 60:02d} "; ele participa do estado atual do método.
                f"({duracao} min)"  # Usa nesta etapa o valor ou operador específico mostrado em f"({duracao} min)"; ele participa do estado atual do método.
            )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
            horario_minuto = fim_minuto  # Guarda em horario_minuto o resultado de fim_minuto, necessário à próxima decisão.
        print(f"Duração total: {horario_minuto // 60}h {horario_minuto % 60}min")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.

    def _exibir_modelo_atual(self, ratname: str) -> None:  # Define _exibir_modelo_atual, que executa a operação específica desta etapa.
        planos = self.repositorio.carregar(self.ARQUIVO_MODELOS, {})  # Nomeia modelos_estudo.json como arquivo dos planos confirmados por conta.
        if not isinstance(planos, dict):  # Valida o tipo do dado carregado antes de continuar o processamento.
            raise ValueError("O arquivo de modelos de estudo deve conter um objeto JSON.")  # Interrompe o fluxo porque os dados persistidos falharam na validação esperada.
        modelo = planos.get(ratname)  # Armazena o plano escolhido, cuja lista de blocos será exibida ou usada.
        if not isinstance(modelo, dict):  # Valida o tipo do dado carregado antes de continuar o processamento.
            print("Você ainda não selecionou um modelo de estudo.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return  # Retorna ao chamador e encerra o método neste ponto.
        print("\n===== MODELO ATUAL =====")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
        self._exibir_modelo(modelo)  # Usa nesta etapa o valor ou operador específico mostrado em self._exibir_modelo(modelo); ele participa do estado atual do método.

    def executar(self) -> None:  # Define executar, que executa a operação específica desta etapa.
        ratname = self.estado.usuario_logado  # Obtém o identificador da conta conectada para vincular modelo, presença ou participação.
        if ratname is None:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            print("\nVocê precisa fazer login para acessar os modelos de estudo.")  # Informa que é necessário autenticar antes de usar este recurso.
            return  # Retorna ao chamador e encerra o método neste ponto.

        while True:  # Repete o bloco até uma operação interna interromper ou concluir o fluxo.
            print("\n===== MODELO DE ESTUDO =====")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            for escolha, modelo in self.MODELOS_PREDEFINIDOS.items():  # Armazena os quatro planos e seus blocos configurados em minutos.
                print(f"{escolha}. {modelo['nome']}")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            print("5. Criar modelo personalizado")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            print("6. Visualizar modelo atual")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            print("0. Voltar ao menu principal")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            escolha = input("Escolha um modelo: ").strip()  # Guarda em escolha o resultado de input("Escolha um modelo: ").strip(), necessário à próxima decisão.

            if escolha == "0":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                return  # Retorna ao chamador e encerra o método neste ponto.
            if escolha == "6":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                self._exibir_modelo_atual(ratname)  # Usa nesta etapa o valor ou operador específico mostrado em self._exibir_modelo_atual(ratname); ele participa do estado atual do método.
                continue  # Descarta esta volta e abre imediatamente a próxima apresentação ou validação.
            if escolha == "5":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                modelo = self._criar_modelo_personalizado()  # Armazena o plano escolhido, cuja lista de blocos será exibida ou usada.
            elif escolha in self.MODELOS_PREDEFINIDOS:  # Armazena os quatro planos e seus blocos configurados em minutos.
                modelo = self.MODELOS_PREDEFINIDOS[escolha]  # Armazena os quatro planos e seus blocos configurados em minutos.
            else:  # Executa este ramo quando nenhuma condição anterior deste encadeamento foi atendida.
                print("Opção inválida, tente novamente.")  # Avisa que a opção não corresponde às alternativas válidas.
                continue  # Descarta esta volta e abre imediatamente a próxima apresentação ou validação.

            self._exibir_modelo(modelo)  # Usa nesta etapa o valor ou operador específico mostrado em self._exibir_modelo(modelo); ele participa do estado atual do método.
            confirmar = input("Confirmar e usar este modelo? (s/n): ").strip().casefold()  # Guarda em confirmar o resultado de input("Confirmar e usar este modelo? (s/n): ").strip().casefold(), necessário à próxima decisão.
            if confirmar != "s":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
                print("Modelo não alterado.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
                continue  # Descarta esta volta e abre imediatamente a próxima apresentação ou validação.

            self._salvar_modelo(ratname, modelo)  # Usa nesta etapa o valor ou operador específico mostrado em self._salvar_modelo(ratname, modelo); ele participa do estado atual do método.
            print("Modelo salvo para sua conta.")  # Apresenta ao usuário o conteúdo específico desta etapa da operação.
            return  # Retorna ao chamador e encerra o método neste ponto.


def modelo_estudo() -> None:  # Define modelo_estudo, que executa a operação específica desta etapa.
    GerenciadorModelosEstudo().executar()  # Usa nesta etapa o valor ou operador específico mostrado em GerenciadorModelosEstudo().executar(); ele participa do estado atual do método.


if __name__ == "__main__":  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
    modelo_estudo()  # Usa nesta etapa o valor ou operador específico mostrado em modelo_estudo(); ele participa do estado atual do método.
