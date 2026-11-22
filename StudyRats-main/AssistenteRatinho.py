import re
import unicodedata


ORIENTACOES = (
    (
        {"cadastro", "conta", "registrar", "email", "senha"},
        "Para criar uma conta, escolha Cadastrar. O projeto aceita e-mail "
        "institucional @ufrpe.br e exige senha de 6 a 8 caracteres com "
        "maiúscula, número e caractere especial. Depois, use Fazer login.",
    ),
    (
        {"login", "entrar", "acessar", "conectar"},
        "Use Fazer login e informe o e-mail e a senha cadastrados. Se não "
        "conseguir entrar, confira se está usando o e-mail institucional correto.",
    ),
    (
        {"perfil", "editar", "excluir", "ratname"},
        "No menu principal, abra Perfil. Lá você encontra edição e exclusão "
        "da conta, acessos DEBUG, RatCoins, rankings e calendário.",
    ),
    (
        {"modelo", "pomodoro", "bloco", "pausa", "estudo"},
        "Abra Modelo de estudo para selecionar Pomodoro, Estudo aprofundado, "
        "Revisão e exercícios, Sessão curta ou montar um plano personalizado.",
    ),
    (
        {"presenca", "cronometro", "sessao", "tempo", "estudar"},
        "Sessão de estudo registra a disciplina e o tempo. Estudantes ganham "
        "15 RatCoins quando completam pelo menos 30 minutos efetivos de estudo.",
    ),
    (
        {"sala", "monitor", "duvida", "atividade", "participar"},
        "Em Sala com monitor, escolha uma sala disponível no horário indicado. "
        "Estudantes podem enviar dúvidas; monitores podem publicar atividades "
        "e responder dúvidas.",
    ),
    (
        {"comunidade", "publicacao", "publicar", "chat", "grupo"},
        "Abra Comunidades para listar, pesquisar, criar ou acessar grupos. "
        "Dentro de uma comunidade, você pode publicar, responder e usar o chat.",
    ),
    (
        {"calendario", "compromisso", "lembrete", "data"},
        "No Perfil, escolha Calendário de estudo para visualizar, adicionar, "
        "editar ou excluir compromissos.",
    ),
    (
        {"ratcoin", "recompensa", "saldo", "ganhar", "pontos"},
        "RatCoins e recompensas ficam no Perfil. Estudantes recebem +15 por "
        "presença com pelo menos 30 minutos efetivos, +15 pelo primeiro modelo, "
        "+20 pela primeira entrada diária em uma sala e pontos por comunidades. "
        "Monitores recebem +5 por atividade publicada em sala.",
    ),
    (
        {"ranking", "classificacao", "lider"},
        "No Perfil, abra Ranking de estudantes/monitores para consultar os dois rankings.",
    ),
    (
        {"debug", "horario", "ajustar"},
        "Os acessos DEBUG são liberados no Perfil por meio de um código. DEBUG 1 "
        "permite configurar data/horário para testes; DEBUG 2 permite ajustar "
        "o saldo de RatCoins.",
    ),
    (
        {"nota", "notas", "monitoria"},
        "A Área do monitor fica no Perfil de uma conta MONITOR. Ela permite "
        "criar, consultar e excluir notas privadas.",
    ),
)


def _normalizar(texto: str) -> set[str]:
    sem_acentos = unicodedata.normalize("NFKD", texto.casefold())
    sem_acentos = "".join(
        caractere for caractere in sem_acentos
        if not unicodedata.combining(caractere)
    )
    palavras = re.findall(r"[a-z0-9]+", sem_acentos)
    ignorar = {"a", "ao", "as", "com", "da", "das", "de", "do", "dos",
               "e", "em", "eu", "o", "os", "para", "por", "que", "quero",
               "como", "me", "minha", "no", "na", "um", "uma", "usar"}
    termos = {palavra for palavra in palavras if palavra not in ignorar}
    termos.update(
        palavra[:-1]
        for palavra in palavras
        if palavra.endswith("s") and len(palavra) > 3
    )
    return termos


def responder(pergunta: str) -> str:
    termos = _normalizar(pergunta)
    if not termos:
        return (
            "Olá usuário! Eu sou o Ratinho IA. Me faça perguntas sobre login, modelos, "
            "presença, salas, comunidades, calendário, RatCoins ou rankings."
        )

    melhores = []
    maior_pontuacao = 0
    for chaves, resposta in ORIENTACOES:
        pontuacao = len(termos & chaves)
        if pontuacao > maior_pontuacao:
            maior_pontuacao = pontuacao
            melhores = [resposta]
        elif pontuacao == maior_pontuacao and pontuacao:
            melhores.append(resposta)

    if not melhores:
        return (
            "Não encontrei resposta para sua pergunta na minha cachola. Posso orientar sobre "
            "cadastro e login, perfil, modelos de estudo, presença, salas, "
            "comunidades, calendário, RatCoins e rankings."
        )
    return "\n\n".join(melhores[:2])
