import lista 
from Dados import persistencia  

class GerenciadorModelosEstudo:  
    ARQUIVO_MODELOS = "modelos_estudo.json"  
    MODELOS_PREDEFINIDOS = {  
        "1": {  
            "nome": "Pomodoro",  
            "blocos": [("Estudo", 25), ("Pausa", 5)] * 3  
            + [("Estudo", 25), ("Pausa longa", 15)],  
        },  
        "2": {  
            "nome": "Estudo aprofundado",  
            "blocos": [("Estudo", 50), ("Pausa", 10)] * 3,  
        }, 
        "3": {  
            "nome": "Revisão e exercícios",      
            "blocos": [  
                ("Revisão do conteúdo", 30), 
                ("Pausa", 5),  
                ("Resolução de exercícios", 30), 
                ("Pausa", 5),  
                ("Resumo final", 20),  
            ],  
        }, 
        "4": {  
            "nome": "Sessão curta",  
            "blocos": [("Estudo", 20), ("Pausa", 5)] * 2 
            + [("Estudo", 20)],  
        }, 
    }  

    def __init__(self, estado=None, repositorio=None) -> None: 
        self.estado = estado if estado is not None else lista.estado  
        self.repositorio = repositorio if repositorio is not None else persistencia 

    @staticmethod  
    def _ler_duracao(pergunta: str, minimo: int, maximo: int) -> int:  
        while True:  
            resposta = input(pergunta).strip()  
            if resposta.isdigit() and minimo <= int(resposta) <= maximo:  
                return int(resposta)  
            print(f"Informe um número entre {minimo} e {maximo}.")  


    def _criar_modelo_personalizado(self) -> dict:  
        while True: 
            tema = input("Qual assunto você vai estudar? ").strip()  
            if tema: 
                break 
            print("O assunto não pode ficar vazio.") 

        duracao = self._ler_duracao("Duração de cada bloco de estudo (minutos, 1-180): ", 1, 180)  
        pausa = self._ler_duracao("Duração das pausas (minutos, 1-60): ", 1, 60) 
        quantidade = self._ler_duracao("Quantidade de blocos de estudo (1-8): ", 1, 8) 
        blocos = []  
        for indice in range(quantidade):  
            blocos.append((f"Estudo: {tema}", duracao))  
            if indice < quantidade - 1:  
                blocos.append(("Pausa", pausa)) 
        return {"nome": f"Plano personalizado: {tema}", "blocos": blocos}  


    def _salvar_modelo(self, ratname:str, modelo: dict) -> None: 
        planos = self.repositorio.carregar(self.ARQUIVO_MODELOS, {})  
        if not isinstance(planos, dict):  
            raise ValueError("O arquivo de modelos de estudo deve conter um objeto JSON.")  
        modelo_confirmado = dict(modelo)  
        modelo_confirmado["confirmado"] = True 
        planos[ratname] = modelo_confirmado  
        self.repositorio.salvar(self.ARQUIVO_MODELOS, planos)  

    @staticmethod  
    def _exibir_modelo(modelo: dict) -> None: 
        print(f"\n=== {modelo['nome']} ===")  
        horario_minuto = 0  
        for indice, (atividade, duracao) in enumerate(modelo["blocos"], start=1):  
            fim_minuto = horario_minuto + duracao  
            print(  
                f"{indice}. {atividade}: "  
                f"{horario_minuto // 60:02d}:{horario_minuto % 60:02d} - "  
                f"{fim_minuto // 60:02d}:{fim_minuto % 60:02d} "  
                f"({duracao} min)" 
            )  
            horario_minuto = fim_minuto  
        print(f"Duração total: {horario_minuto // 60}h {horario_minuto % 60}min")  

    def _exibir_modelo_atual(self, ratname: str) -> None:
        planos = self.repositorio.carregar(self.ARQUIVO_MODELOS, {})  
        if not isinstance(planos, dict): 
            raise ValueError("O arquivo de modelos de estudo deve conter um objeto JSON.")
        modelo = planos.get(ratname)
        if not isinstance(modelo, dict):  
            print("Você ainda não selecionou um modelo de estudo.")  
            return  
        print("\n===== MODELO ATUAL =====") 
        self._exibir_modelo(modelo)

    def executar(self) -> None:  
        ratname = self.estado.usuario_logado  
        if ratname is None: 
            print("\nVocê precisa fazer login para acessar os modelos de estudo.")  
            return 

        while True: 
            print("\n===== MODELO DE ESTUDO =====")  
            for escolha, modelo in self.MODELOS_PREDEFINIDOS.items(): 
                print(f"{escolha}. {modelo['nome']}")  
            print("5. Criar modelo personalizado")  
            print("6. Visualizar modelo atual")
            print("0. Voltar ao menu principal") 
            escolha = input("Escolha um modelo: ").strip() 

            if escolha == "0":  
                return 
            if escolha == "6": 
                self._exibir_modelo_atual(ratname)  
                continue  
            if escolha == "5":  
                modelo = self._criar_modelo_personalizado()  
            elif escolha in self.MODELOS_PREDEFINIDOS: 
                modelo = self.MODELOS_PREDEFINIDOS[escolha]  
            else: 
                print("Opção inválida, tente novamente.") 
                continue  

            self._exibir_modelo(modelo)  
            confirmar = input("Confirmar e usar este modelo? (s/n): ").strip().casefold()  
            if confirmar != "s":  
                print("Modelo não alterado.")  
                continue  
            self._salvar_modelo(ratname, modelo)  
            print("Modelo salvo para sua conta.")  
            return  



def modelo_estudo() -> None:  
    GerenciadorModelosEstudo().executar()  


if __name__ == "__main__":  
    modelo_estudo()  