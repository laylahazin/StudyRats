import lista
from Dados import persistencia
from SalaEstudo import GerenciadorSalas


class AreaMonitor:
    ARQUIVO = "blocos_notas.json"

    def __init__(self, salas: GerenciadorSalas) -> None:
        self.estado = lista.estado
        self.persistencia = persistencia
        self.salas = salas

    def menu(self) -> None:
        if self.estado.usuario_logado is None:
            print("Você precisa fazer login para acessar a área do monitor.")
            return
        if self.estado.tipo_usuario_logado != self.estado.TIPO_MONITOR:
            print("Esta área está disponível somente para contas de monitor.")
            return
        while True:
            print("\n========== ÁREA DO MONITOR ==========")
            print("1. Visualizar salas de estudo")
            print("2. Criar notas")
            print("3. Ver minhas notas")
            print("4. Excluir notas")
            print("0. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ").strip()
            acoes = {
                "1": self.salas.listar_salas,
                "2": self.criar_bloco,
                "3": self.listar_blocos,
                "4": self.excluir_bloco,
            }
            if opcao == "0":
                return
            acao = acoes.get(opcao)
            if acao is None:
                print("Opção inválida. Tente novamente.")
            else:
                acao()

    def _carregar(self) -> dict:
        blocos = self.persistencia.carregar(self.ARQUIVO, {})
        if not isinstance(blocos, dict):
            raise ValueError("O arquivo blocos_notas.json deve conter um objeto JSON.")
        return blocos

    def criar_bloco(self) -> None:
        ratname = self._monitor_logado()
        if ratname is None:
            return
        todos_blocos = self._carregar()
        print("\n===== CRIAR NOTAS =====")
        materia = input("Matéria das notas: ").strip()
        duvida = input("Dúvida/Tema: ").strip()
        anotacoes = input("Descrição: ").strip()
        materiais = input("Material complementar a ser usado: ").strip()
        if not materia:
            print("A matéria não pode ficar vazia.")
            return
        blocos_usuario = todos_blocos.setdefault(ratname, [])
        if not isinstance(blocos_usuario, list):
            raise ValueError(f"Os blocos de notas de '{ratname}' estão inválidos.")
        blocos_usuario.append(
            {
                "materia": materia,
                "duvida": duvida,
                "materiais_complementares": materiais,
                "anotacoes_gerais": anotacoes,
            }
        )
        self.persistencia.salvar(self.ARQUIVO, todos_blocos)
        print("Nota criada com sucesso!")

    def listar_blocos(self) -> None:
        ratname = self._monitor_logado()
        if ratname is None:
            return
        blocos = self._carregar().get(ratname, [])
        if not isinstance(blocos, list):
            raise ValueError(f"As notas de '{ratname}' estão inválidas.")
        print("\n===== MINHAS NOTAS =====")
        if not blocos:
            print("Você ainda não criou notas.")
            return
        for indice, bloco in enumerate(blocos, start=1):
            if not isinstance(bloco, dict):
                raise ValueError(f"A nota {indice} de '{ratname}' está inválida.")
            print(f"\n{indice}. {bloco.get('materia', 'Sem matéria')}")
            print(f"Dúvida/Tema: {bloco.get('duvida', '')}")
            print(f"Materiais complementares: {bloco.get('materiais_complementares', '')}")
            print(f"Descrição: {bloco.get('anotacoes_gerais', '')}")

    def excluir_bloco(self) -> None:
        ratname = self._monitor_logado()
        if ratname is None:
            return
        todos_blocos = self._carregar()
        blocos = todos_blocos.get(ratname, [])
        if not isinstance(blocos, list):
            raise ValueError(f"Os blocos de notas de '{ratname}' estão inválidos.")
        if not blocos:
            print("Você não possui blocos de notas para excluir.")
            return
        self.listar_blocos()
        try:
            numero = int(input("Digite o número da nota que deseja excluir: ").strip())
        except ValueError:
            print("Digite um número válido.")
            return
        if numero < 1 or numero > len(blocos):
            print("Nota não encontrada.")
            return
        if input("Confirma a exclusão? (s/n): ").strip().lower() != "s":
            print("Exclusão cancelada.")
            return
        blocos.pop(numero - 1)
        self.persistencia.salvar(self.ARQUIVO, todos_blocos)
        print("Nota excluída com sucesso!")

    def _monitor_logado(self) -> str | None:
        ratname = self.estado.usuario_logado
        if ratname is None:
            print("Você precisa fazer login para acessar a área do monitor.")
            return None
        if self.estado.tipo_usuario_logado != self.estado.TIPO_MONITOR:
            print("Esta área está disponível somente para contas de monitor.")
            return None
        return ratname
