
import re  # Usa nesta etapa o valor ou operador específico mostrado em import re; ele participa do estado atual do método.
import unicodedata  # Usa nesta etapa o valor ou operador específico mostrado em import unicodedata; ele participa do estado atual do método.



ORIENTACOES = (  # Guarda em ORIENTACOES o resultado de (, necessário à próxima decisão.
    (  # Usa nesta etapa o valor ou operador específico mostrado em (; ele participa do estado atual do método.
        {"cadastro", "conta", "registrar", "email", "senha"},  # Usa nesta etapa o valor ou operador específico mostrado em {"cadastro", "conta", "registrar", "email", "senha"},; ele participa do estado atual do método.
        "Para criar uma conta, escolha Cadastrar. O projeto aceita e-mail "  # Usa nesta etapa o valor ou operador específico mostrado em "Para criar uma conta, escolha Cadastrar. O projeto aceita e-mail "; ele participa do estado atual do método.
        "institucional @ufrpe.br e exige senha de 6 a 8 caracteres com "  # Usa nesta etapa o valor ou operador específico mostrado em "institucional @ufrpe.br e exige senha de 6 a 8 caracteres com "; ele participa do estado atual do método.
        "maiúscula, número e caractere especial. Depois, use Fazer login.",  # Usa nesta etapa o valor ou operador específico mostrado em "maiúscula, número e caractere especial. Depois, use Fazer login.",; ele participa do estado atual do método.
    ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    (  # Usa nesta etapa o valor ou operador específico mostrado em (; ele participa do estado atual do método.
        {"login", "entrar", "acessar", "conectar"},  # Usa nesta etapa o valor ou operador específico mostrado em {"login", "entrar", "acessar", "conectar"},; ele participa do estado atual do método.
        "Use Fazer login e informe o e-mail e a senha cadastrados. Se não "  # Usa nesta etapa o valor ou operador específico mostrado em "Use Fazer login e informe o e-mail e a senha cadastrados. Se não "; ele participa do estado atual do método.
        "conseguir entrar, confira se está usando o e-mail institucional correto.",  # Usa nesta etapa o valor ou operador específico mostrado em "conseguir entrar, confira se está usando o e-mail institucional correto.",; ele participa do estado atual do método.
    ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    (  # Usa nesta etapa o valor ou operador específico mostrado em (; ele participa do estado atual do método.
        {"perfil", "editar", "excluir", "ratname"},  # Usa nesta etapa o valor ou operador específico mostrado em {"perfil", "editar", "excluir", "ratname"},; ele participa do estado atual do método.
        "No menu principal, abra Perfil. Lá você encontra edição e exclusão "  # Usa nesta etapa o valor ou operador específico mostrado em "No menu principal, abra Perfil. Lá você encontra edição e exclusão "; ele participa do estado atual do método.
        "da conta, acessos DEBUG, RatCoins, rankings e calendário.",  # Usa nesta etapa o valor ou operador específico mostrado em "da conta, acessos DEBUG, RatCoins, rankings e calendário.",; ele participa do estado atual do método.
    ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    (  # Usa nesta etapa o valor ou operador específico mostrado em (; ele participa do estado atual do método.
        {"modelo", "pomodoro", "bloco", "pausa", "estudo"},  # Usa nesta etapa o valor ou operador específico mostrado em {"modelo", "pomodoro", "bloco", "pausa", "estudo"},; ele participa do estado atual do método.
        "Abra Modelo de estudo para selecionar Pomodoro, Estudo aprofundado, "  # Usa nesta etapa o valor ou operador específico mostrado em "Abra Modelo de estudo para selecionar Pomodoro, Estudo aprofundado, "; ele participa do estado atual do método.
        "Revisão e exercícios, Sessão curta ou montar um plano personalizado.",  # Usa nesta etapa o valor ou operador específico mostrado em "Revisão e exercícios, Sessão curta ou montar um plano personalizado.",; ele participa do estado atual do método.
    ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    (  # Usa nesta etapa o valor ou operador específico mostrado em (; ele participa do estado atual do método.
        {"presenca", "cronometro", "sessao", "tempo", "estudar"},  # Usa nesta etapa o valor ou operador específico mostrado em {"presenca", "cronometro", "sessao", "tempo", "estudar"},; ele participa do estado atual do método.
        "Sessão de estudo registra a disciplina e o tempo. Estudantes ganham "  # Usa nesta etapa o valor ou operador específico mostrado em "Sessão de estudo registra a disciplina e o tempo. Estudantes ganham "; ele participa do estado atual do método.
        "15 RatCoins quando completam pelo menos 30 minutos efetivos de estudo.",  # Usa nesta etapa o valor ou operador específico mostrado em "15 RatCoins quando completam pelo menos 30 minutos efetivos de estudo.",; ele participa do estado atual do método.
    ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    (  # Usa nesta etapa o valor ou operador específico mostrado em (; ele participa do estado atual do método.
        {"sala", "monitor", "duvida", "atividade", "participar"},  # Usa nesta etapa o valor ou operador específico mostrado em {"sala", "monitor", "duvida", "atividade", "participar"},; ele participa do estado atual do método.
        "Em Sala com monitor, escolha uma sala disponível no horário indicado. "  # Usa nesta etapa o valor ou operador específico mostrado em "Em Sala com monitor, escolha uma sala disponível no horário indicado. "; ele participa do estado atual do método.
        "Estudantes podem enviar dúvidas; monitores podem publicar atividades "  # Usa nesta etapa o valor ou operador específico mostrado em "Estudantes podem enviar dúvidas; monitores podem publicar atividades "; ele participa do estado atual do método.
        "e responder dúvidas.",  # Usa nesta etapa o valor ou operador específico mostrado em "e responder dúvidas.",; ele participa do estado atual do método.
    ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    (  # Usa nesta etapa o valor ou operador específico mostrado em (; ele participa do estado atual do método.
        {"comunidade", "publicacao", "publicar", "chat", "grupo"},  # Usa nesta etapa o valor ou operador específico mostrado em {"comunidade", "publicacao", "publicar", "chat", "grupo"},; ele participa do estado atual do método.
        "Abra Comunidades para listar, pesquisar, criar ou acessar grupos. "  # Usa nesta etapa o valor ou operador específico mostrado em "Abra Comunidades para listar, pesquisar, criar ou acessar grupos. "; ele participa do estado atual do método.
        "Dentro de uma comunidade, você pode publicar, responder e usar o chat.",  # Usa nesta etapa o valor ou operador específico mostrado em "Dentro de uma comunidade, você pode publicar, responder e usar o chat.",; ele participa do estado atual do método.
    ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    (  # Usa nesta etapa o valor ou operador específico mostrado em (; ele participa do estado atual do método.
        {"calendario", "compromisso", "lembrete", "data"},  # Usa nesta etapa o valor ou operador específico mostrado em {"calendario", "compromisso", "lembrete", "data"},; ele participa do estado atual do método.
        "No Perfil, escolha Calendário de estudo para visualizar, adicionar, "  # Usa nesta etapa o valor ou operador específico mostrado em "No Perfil, escolha Calendário de estudo para visualizar, adicionar, "; ele participa do estado atual do método.
        "editar ou excluir compromissos.",  # Usa nesta etapa o valor ou operador específico mostrado em "editar ou excluir compromissos.",; ele participa do estado atual do método.
    ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    (  # Usa nesta etapa o valor ou operador específico mostrado em (; ele participa do estado atual do método.
        {"ratcoin", "recompensa", "saldo", "ganhar", "pontos"},  # Usa nesta etapa o valor ou operador específico mostrado em {"ratcoin", "recompensa", "saldo", "ganhar", "pontos"},; ele participa do estado atual do método.
        "RatCoins e recompensas ficam no Perfil. Estudantes recebem +15 por "  # Usa nesta etapa o valor ou operador específico mostrado em "RatCoins e recompensas ficam no Perfil. Estudantes recebem +15 por "; ele participa do estado atual do método.
        "presença com pelo menos 30 minutos efetivos, +15 pelo primeiro modelo, "  # Usa nesta etapa o valor ou operador específico mostrado em "presença com pelo menos 30 minutos efetivos, +15 pelo primeiro modelo, "; ele participa do estado atual do método.
        "+20 pela primeira entrada diária em uma sala e pontos por comunidades. "  # Usa nesta etapa o valor ou operador específico mostrado em "+20 pela primeira entrada diária em uma sala e pontos por comunidades. "; ele participa do estado atual do método.
        "Monitores recebem +5 por atividade publicada em sala.",  # Usa nesta etapa o valor ou operador específico mostrado em "Monitores recebem +5 por atividade publicada em sala.",; ele participa do estado atual do método.
    ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    (  # Usa nesta etapa o valor ou operador específico mostrado em (; ele participa do estado atual do método.
        {"ranking", "classificacao", "lider"},  # Usa nesta etapa o valor ou operador específico mostrado em {"ranking", "classificacao", "lider"},; ele participa do estado atual do método.
        "No Perfil, abra Ranking de estudantes/monitores para consultar os dois rankings.",  # Usa nesta etapa o valor ou operador específico mostrado em "No Perfil, abra Ranking de estudantes/monitores para consultar os dois rankings.",; ele participa do estado atual do método.
    ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    (  # Usa nesta etapa o valor ou operador específico mostrado em (; ele participa do estado atual do método.
        {"debug", "horario", "ajustar"},  # Usa nesta etapa o valor ou operador específico mostrado em {"debug", "horario", "ajustar"},; ele participa do estado atual do método.
        "Os acessos DEBUG são liberados no Perfil por meio de um código. DEBUG 1 "  # Usa nesta etapa o valor ou operador específico mostrado em "Os acessos DEBUG são liberados no Perfil por meio de um código. DEBUG 1 "; ele participa do estado atual do método.
        "permite configurar data/horário para testes; DEBUG 2 permite ajustar "  # Usa nesta etapa o valor ou operador específico mostrado em "permite configurar data/horário para testes; DEBUG 2 permite ajustar "; ele participa do estado atual do método.
        "o saldo de RatCoins.",  # Usa nesta etapa o valor ou operador específico mostrado em "o saldo de RatCoins.",; ele participa do estado atual do método.
    ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    (  # Usa nesta etapa o valor ou operador específico mostrado em (; ele participa do estado atual do método.
        {"nota", "notas", "monitoria"},  # Usa nesta etapa o valor ou operador específico mostrado em {"nota", "notas", "monitoria"},; ele participa do estado atual do método.
        "A Área do monitor fica no Perfil de uma conta MONITOR. Ela permite "  # Usa nesta etapa o valor ou operador específico mostrado em "A Área do monitor fica no Perfil de uma conta MONITOR. Ela permite "; ele participa do estado atual do método.
        "criar, consultar e excluir notas privadas.",  # Usa nesta etapa o valor ou operador específico mostrado em "criar, consultar e excluir notas privadas.",; ele participa do estado atual do método.
    ),  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
)  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.


def _normalizar(texto: str) -> set[str]:  # Define _normalizar, que executa a operação específica desta etapa.

    sem_acentos = unicodedata.normalize("NFKD", texto.casefold())  # Guarda em sem_acentos o resultado de unicodedata.normalize("NFKD", texto.casefold()), necessário à próxima decisão.
    sem_acentos = "".join(  # Guarda em sem_acentos o resultado de "".join(, necessário à próxima decisão.
        caractere for caractere in sem_acentos  # Usa nesta etapa o valor ou operador específico mostrado em caractere for caractere in sem_acentos; ele participa do estado atual do método.
        if not unicodedata.combining(caractere)  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
    )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    palavras = re.findall(r"[a-z0-9]+", sem_acentos)  # Guarda em palavras o resultado de re.findall(r"[a-z0-9]+", sem_acentos), necessário à próxima decisão.
    ignorar = {"a", "ao", "as", "com", "da", "das", "de", "do", "dos",  # Guarda em ignorar o resultado de {"a", "ao", "as", "com", "da", "das", "de", "do", "dos",, necessário à próxima decisão.
               "e", "em", "eu", "o", "os", "para", "por", "que", "quero",  # Usa nesta etapa o valor ou operador específico mostrado em "e", "em", "eu", "o", "os", "para", "por", "que", "quero",; ele participa do estado atual do método.
               "como", "me", "minha", "no", "na", "um", "uma", "usar"}  # Usa nesta etapa o valor ou operador específico mostrado em "como", "me", "minha", "no", "na", "um", "uma", "usar"}; ele participa do estado atual do método.
    termos = {palavra for palavra in palavras if palavra not in ignorar}  # Guarda em termos o resultado de {palavra for palavra in palavras if palavra not in ignorar}, necessário à próxima decisão.

    termos.update(  # Usa nesta etapa o valor ou operador específico mostrado em termos.update(; ele participa do estado atual do método.
        palavra[:-1]  # Usa nesta etapa o valor ou operador específico mostrado em palavra[:-1]; ele participa do estado atual do método.
        for palavra in palavras  # Percorre cada elemento da coleção aplicando as operações deste bloco.
        if palavra.endswith("s") and len(palavra) > 3  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
    )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.
    return termos  # Entrega ao chamador o resultado calculado por esta etapa.


def responder(pergunta: str) -> str:  # Define responder, que executa a operação específica desta etapa.

    termos = _normalizar(pergunta)  # Guarda em termos o resultado de _normalizar(pergunta), necessário à próxima decisão.
    if not termos:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
        return (  # Entrega ao chamador o resultado calculado por esta etapa.
            "Oi! Sou o Ratinho StudyRats. Pergunte sobre login, modelos, "  # Usa nesta etapa o valor ou operador específico mostrado em "Oi! Sou o Ratinho StudyRats. Pergunte sobre login, modelos, "; ele participa do estado atual do método.
            "presença, salas, comunidades, calendário, RatCoins ou rankings."  # Usa nesta etapa o valor ou operador específico mostrado em "presença, salas, comunidades, calendário, RatCoins ou rankings."; ele participa do estado atual do método.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

    melhores = []  # Guarda em melhores o resultado de [], necessário à próxima decisão.
    maior_pontuacao = 0  # Registra em maior_pontuacao quantas palavras correspondem à orientação atual.
    for chaves, resposta in ORIENTACOES:  # Percorre dúvidas ou respostas desta sessão para apresentá-las ao usuário.
        pontuacao = len(termos & chaves)  # Registra em pontuacao quantas palavras correspondem à orientação atual.
        if pontuacao > maior_pontuacao:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
            maior_pontuacao = pontuacao  # Registra em maior_pontuacao quantas palavras correspondem à orientação atual.
            melhores = [resposta]  # Guarda em melhores o resultado de [resposta], necessário à próxima decisão.
        elif pontuacao == maior_pontuacao and pontuacao:  # Testa esta alternativa somente após todas as condições anteriores falharem.
            melhores.append(resposta)  # Adiciona à lista o registro criado nesta etapa.

    if not melhores:  # Executa o bloco somente quando a condição descreve o estado permitido nesta etapa.
        return (  # Entrega ao chamador o resultado calculado por esta etapa.
            "Ainda não encontrei essa opção na ajuda local. Posso orientar sobre "  # Usa nesta etapa o valor ou operador específico mostrado em "Ainda não encontrei essa opção na ajuda local. Posso orientar sobre "; ele participa do estado atual do método.
            "cadastro e login, perfil, modelos de estudo, presença, salas, "  # Usa nesta etapa o valor ou operador específico mostrado em "cadastro e login, perfil, modelos de estudo, presença, salas, "; ele participa do estado atual do método.
            "comunidades, calendário, RatCoins, rankings e DEBUG."  # Usa nesta etapa o valor ou operador específico mostrado em "comunidades, calendário, RatCoins, rankings e DEBUG."; ele participa do estado atual do método.
        )  # Fecha a estrutura iniciada acima e entrega seu conteúdo completo ao chamador.

    return "\n\n".join(melhores[:2])  # Entrega ao chamador o resultado calculado por esta etapa.
