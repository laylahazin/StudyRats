from datetime import datetime  # Importa de datetime os recursos datetime usados neste modulo.

from Dados import persistencia  # Importa de Dados persistencia, reutilizando os recursos centrais de persistencia e credenciais.


class GerenciadorHorario:  # Declara a classe GerenciadorHorario: controla o horario real ou manual usado pela aplicacao.
    ARQUIVO_CONFIGURACAO = "configuracao_horario.json"  # Guarda em ARQUIVO_CONFIGURACAO o valor produzido por "configuracao_horario.json".
    SENHA_ADMIN_HORARIO = "BSISTUDYRAT"  # Guarda em SENHA_ADMIN_HORARIO o valor produzido por "BSISTUDYRAT".

    def __init__(self) -> None:  # Declara o metodo __init__: implementa esta funcionalidade da classe.
        self.persistencia = persistencia  # Guarda em self.persistencia o valor produzido por persistencia.

    def obter_horario_atual(self) -> datetime:  # Declara o metodo obter_horario_atual: retorna o horario real ou o instante manual configurado.
        configuracao = self._carregar_configuracao()  # recupera o modo de horario e a data manual persistidos
        modo = configuracao.get("modo")  # determina se a aplicacao usa horario real ou manual
        if modo == "automatico":  # No modo automatico, usa datetime.now() para considerar o horario real do sistema.
            return datetime.now()  # Encerra o metodo e devolve ao chamador datetime.now().
        if modo == "manual":  # No modo manual, busca em data_hora_manual o instante fixo configurado para testes.
            valor = configuracao.get("data_hora_manual")  # le o valor manual antes de validar seu formato ISO
            if not isinstance(valor, str):  # Rejeita o horario manual salvo quando ele nao esta armazenado como texto ISO.
                raise ValueError("O horário manual salvo está inválido.")  # Interrompe a operacao com ValueError("O horário manual salvo está inválido."), indicando dados ou estado invalidos.
            try:  # Protege o bloco seguinte contra dados que podem causar excecao.
                return datetime.fromisoformat(valor)  # Converte o texto ISO do horario manual em um objeto datetime utilizavel.
            except ValueError as erro:  # Trata ValueError as erro emitida pelo bloco try, indicando que a entrada ou dado protegido era invalido.
                raise ValueError("O horário manual salvo está inválido.") from erro  # Interrompe a operacao com ValueError("O horário manual salvo está inválido.") from erro, indicando dados ou estado invalidos.

        raise ValueError("O modo de horário salvo é inválido.")  # Interrompe a operacao com ValueError("O modo de horário salvo é inválido."), indicando dados ou estado invalidos.

    def acessar_configuracao(self) -> None:  # Declara o metodo acessar_configuracao: exige a senha administrativa antes de abrir o ajuste de horario.
        print("\n=== ADMINISTRAÇÃO ===")  # Exibe no terminal === ADMINISTRAÇÃO ===.
        senha = input("Digite a senha de administrador para ajustar o horário: ").strip()  # Guarda em senha o valor produzido por input("Digite a senha de administrador para ajustar o horário: ").strip().
        if senha != self.SENHA_ADMIN_HORARIO:  # Testa a condicao senha != self.SENHA_ADMIN_HORARIO e executa o bloco seguinte somente quando ela for verdadeira.
            print("Acesso negado. Você não tem permissão para alterar o horário do sistema")  # Exibe no terminal Acesso negado. Você não tem permissão para alterar o horário do sistema.
            return  # Encerra este metodo imediatamente sem devolver valor.

        self.configurar()  # Executa self.configurar(); o efeito desta chamada participa diretamente desta funcionalidade.

    def configurar(self) -> None:  # Declara o metodo configurar: permite fixar horario de teste ou restaurar o horario automatico.
        while True:  # Mantem o loop ativo ate encontrar uma opcao que devolva ou encerre o fluxo.
            horario_atual = self.obter_horario_atual()  # guarda o instante considerado pelo menu administrativo
            modo = "manual" if self._modo_manual_ativo() else "automático"  # determina se a aplicacao usa horario real ou manual
            print(f"\n=== HORÁRIO DO SISTEMA ({modo}) ===")  # Exibe no terminal === HORÁRIO DO SISTEMA ({modo}) ===.
            print(f"Horário considerado: {horario_atual:%d/%m/%Y %H:%M}")  # Exibe no terminal Horário considerado: {horario_atual:%d/%m/%Y %H:%M}.
            print("1. Definir data e horário manual para testes")  # Exibe no terminal 1. Definir data e horário manual para testes.
            print("2. Voltar ao horário automático do sistema")  # Exibe no terminal 2. Voltar ao horário automático do sistema.
            print("0. Voltar ao menu principal")  # Exibe no terminal 0. Voltar ao menu principal.

            opcao = input("Escolha uma opção: ").strip()  # Guarda em opcao o valor produzido por input("Escolha uma opção: ").strip().
            if opcao == "1":  # Seleciona a configuracao manual e inicia a coleta de data DD/MM/AAAA e horario HH:MM.
                texto_data = input("Informe a data de teste (DD/MM/AAAA): ").strip()  # captura a data digitada no formato DD/MM/AAAA
                texto_horario = input("Informe o horário de teste (HH:MM): ").strip()  # captura o horario digitado no formato HH:MM
                try:  # Protege o bloco seguinte contra dados que podem causar excecao.
                    data = datetime.strptime(texto_data, "%d/%m/%Y").date()  # converte a entrada em objeto date
                    horario = datetime.strptime(texto_horario, "%H:%M").time()  # converte a entrada em objeto time
                except ValueError:  # Trata ValueError emitida pelo bloco try, indicando que a entrada ou dado protegido era invalido.
                    print(  # Escreve no terminal o conteudo preparado por esta chamada.
                        "Data ou horário inválido. Use DD/MM/AAAA e HH:MM, "  # Executa nesta linha "Data ou horário inválido. Use DD/MM/AAAA e HH:MM, " no contexto desta funcionalidade.
                        "por exemplo 01/08/2026 e 18:30."  # Executa nesta linha "por exemplo 01/08/2026 e 18:30." no contexto desta funcionalidade.
                    )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                    continue  # Pula o restante da iteracao atual e volta ao inicio da proxima repeticao.

                horario_manual = datetime.combine(data, horario)  # combina data e horario em um datetime persistivel
                self.persistencia.salvar(  # Persiste no arquivo JSON indicado o novo estado da estrutura atual.
                    self.ARQUIVO_CONFIGURACAO,  # Executa self.ARQUIVO_CONFIGURACAO,; o efeito desta chamada participa diretamente desta funcionalidade.
                    {  # Executa nesta linha { no contexto desta funcionalidade.
                        "modo": "manual",  # Na chave "modo", seleciona horario automatico ou manual; nesta entrada recebe "manual",.
                        "data_hora_manual": horario_manual.isoformat(timespec="minutes"),  # Na chave "data_hora_manual", guarda a data e hora fixa usada pelo modo manual; nesta entrada recebe horario_manual.isoformat(timespec="minutes"),.
                    },  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                print(  # Escreve no terminal o conteudo preparado por esta chamada.
                    f"Horário de teste definido para "  # Executa nesta linha f"Horário de teste definido para " no contexto desta funcionalidade.
                    f"{horario_manual:%d/%m/%Y %H:%M}. Data e horário "  # Executa nesta linha f"{horario_manual:%d/%m/%Y %H:%M}. Data e horário " no contexto desta funcionalidade.
                    "permanecerão fixos até você selecionar o modo automático."  # Executa nesta linha "permanecerão fixos até você selecionar o modo automático." no contexto desta funcionalidade.
                )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.

            elif opcao == "2":  # Testa a alternativa opcao == "2" somente depois que as condicoes anteriores falharam.
                self.persistencia.salvar(  # Persiste no arquivo JSON indicado o novo estado da estrutura atual.
                    self.ARQUIVO_CONFIGURACAO,  # Executa self.ARQUIVO_CONFIGURACAO,; o efeito desta chamada participa diretamente desta funcionalidade.
                    {"modo": "automatico", "data_hora_manual": None},  # Executa nesta linha {"modo": "automatico", "data_hora_manual": None}, no contexto desta funcionalidade.
                )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
                print("Horário automático do sistema restaurado")  # Exibe no terminal Horário automático do sistema restaurado.
                return  # Encerra este metodo imediatamente sem devolver valor.

            elif opcao == "0":  # Seleciona voltar ao menu principal sem alterar o modo de horario.
                return  # Encerra este metodo imediatamente sem devolver valor.

            else:  # Executa este bloco quando nenhuma condicao anterior da cadeia foi atendida.
                print("Opção inválida, tente novamente")  # Exibe no terminal Opção inválida, tente novamente.

    def _carregar_configuracao(self) -> dict:  # Declara o metodo _carregar_configuracao: implementa esta funcionalidade da classe.
        configuracao = self.persistencia.carregar(  # recupera o modo de horario e a data manual persistidos
            self.ARQUIVO_CONFIGURACAO,  # Executa self.ARQUIVO_CONFIGURACAO,; o efeito desta chamada participa diretamente desta funcionalidade.
            {"modo": "automatico", "data_hora_manual": None},  # Executa nesta linha {"modo": "automatico", "data_hora_manual": None}, no contexto desta funcionalidade.
        )  # Fecha a estrutura ou expressao iniciada nas linhas anteriores.
        if not isinstance(configuracao, dict):  # Testa a condicao not isinstance(configuracao, dict) e executa o bloco seguinte somente quando ela for verdadeira.
            raise ValueError("A configuração do horário deve ser um objeto JSON.")  # Interrompe a operacao com ValueError("A configuração do horário deve ser um objeto JSON."), indicando dados ou estado invalidos.
        return configuracao  # Encerra o metodo e devolve ao chamador configuracao.

    def _modo_manual_ativo(self) -> bool:  # Declara o metodo _modo_manual_ativo: implementa esta funcionalidade da classe.
        return self._carregar_configuracao().get("modo") == "manual"  # Encerra o metodo e devolve ao chamador self._carregar_configuracao().get("modo") == "manual".

    def modo_manual_ativo(self) -> bool:  # Declara o metodo modo_manual_ativo: implementa esta funcionalidade da classe.
        return self._modo_manual_ativo()  # Encerra o metodo e devolve ao chamador self._modo_manual_ativo().
