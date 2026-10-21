from datetime import datetime

import lista
from Persistencia import carregar_json, salvar_json


ARQUIVO_PRESENCAS = "presencas.json"


def registro_presenca() -> None:
    if lista.usuario_logado is None:
        print("\nVocê precisa fazer login para registrar sua presença.")
        return

    disciplinas = {
        sala["materia"].casefold(): sala["materia"]
        for sala in lista.salas_disponiveis
    }
    print("\n===== REGISTRO DE PRESENÇA =====")
    print("Disciplinas disponíveis:")
    for disciplina in disciplinas.values():
        print(f"- {disciplina}")

    while True:
        entrada = input("\nDigite a disciplina ou assunto que vai estudar: ").strip()
        disciplina = disciplinas.get(entrada.casefold())
        if disciplina is not None:
            break
        print("Disciplina inválida. Escolha uma das opções disponíveis.")

    confirmar = input("Deseja iniciar o cronômetro? (sim/não): ").strip().casefold()
    if confirmar != "sim":
        print("Sessão não iniciada. Você retornará ao menu principal.")
        return

    inicio = datetime.now()
    print(f"\nCronômetro iniciado! Você está estudando: {disciplina}")
    while True:
        finalizar = input(
            'Digite "finalizar" quando terminar sua sessão de estudo: '
        ).strip().casefold()
        if finalizar == "finalizar":
            break
        print('Entrada inválida. Digite "finalizar" para encerrar a sessão.')

    fim = datetime.now()
    duracao_segundos = max(0, int((fim - inicio).total_seconds()))
    presencas = carregar_json(ARQUIVO_PRESENCAS, {})
    if not isinstance(presencas, dict):
        raise ValueError("O arquivo de presencas deve conter um objeto JSON.")

    historico = presencas.setdefault(lista.usuario_logado, [])
    if not isinstance(historico, list):
        raise ValueError(
            f"O histórico de presenças de '{lista.usuario_logado}' está inválido."
        )
    historico.append(
        {
            "disciplina": disciplina,
            "inicio": inicio.isoformat(timespec="seconds"),
            "fim": fim.isoformat(timespec="seconds"),
            "duracao_segundos": duracao_segundos,
        }
    )
    salvar_json(ARQUIVO_PRESENCAS, presencas)

    minutos, segundos = divmod(duracao_segundos, 60)
    print(
        "\nSessão de estudo finalizada!"
        "\nAtividade registrada e presença confirmada."
        f"\nDisciplina: {disciplina}"
        f"\nTempo de estudo: {minutos} min {segundos} s"
        "\nVocê retornará ao menu principal."
    )


if __name__ == "__main__":
    registro_presenca()
