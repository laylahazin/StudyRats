from Persistencia import carregar_json, salvar_json  # lê e grava os dados persistentes das contas


usuarios = carregar_json("usuarios.json", [])  # carrega as contas cadastradas ou inicia uma lista vazia
if not isinstance(usuarios, list):  # confirma que o conteúdo salvo pode ser percorrido como uma lista
    raise ValueError("O arquivo dados/usuarios.json deve conter uma lista de usuários.")  # identifica o formato incorreto sem ignorar os dados

usuario_logado = None  # guarda o Ratname da sessão atual ou None quando ninguém está autenticado

salas_disponiveis = [  # reúne a configuração fixa das salas que aparecem na aplicação
    {  # inicia os dados da sala de Princípios de Programação
        "id": "pp",  # identifica a sala nas participações persistidas
        "nome": "Sala de Principios de Programação",  # define o nome que aparece na interface textual
        "materia": "Programação",  # associa a sala à disciplina selecionável no registro de presença
        "descricao": "Revisão dos princípios de programação.",  # descreve a atividade disponível na sala
        "monitor": "Monitor responsável",  # informa quem acompanha a sessão da sala
        "inicio": "13:00",  # define o horário diário em que a sala abre
        "fim": "14:30",  # define o horário diário em que a sala fecha
        "capacidade": 10,  # limita a quantidade de Ratnames participantes
        "ativa": True,  # habilita a sala para entrada durante o horário definido
    },  # conclui os dados da sala de Programação
    {  # inicia os dados da sala de Fundamentos de Matemática
        "id": "fund",  # identifica a sala nas participações persistidas
        "nome": "Sala de Fundamentos de Matemática",  # define o nome que aparece na interface textual
        "materia": "Matemática",  # associa a sala à disciplina selecionável no registro de presença
        "descricao": "Revisão de conceitos fundamentais de matemática.",  # descreve a atividade disponível na sala
        "monitor": "Monitor responsável",  # informa quem acompanha a sessão da sala
        "inicio": "15:00",  # define o horário diário em que a sala abre
        "fim": "16:30",  # define o horário diário em que a sala fecha
        "capacidade": 10,  # limita a quantidade de Ratnames participantes
        "ativa": True,  # habilita a sala para entrada durante o horário definido
    },  # conclui os dados da sala de Matemática
    {  # inicia os dados da sala de Introdução à Administração
        "id": "adm",  # identifica a sala nas participações persistidas
        "nome": "Sala de Introdução à Administração",  # define o nome que aparece na interface textual
        "materia": "Administração",  # associa a sala à disciplina selecionável no registro de presença
        "descricao": "Discussão de conceitos básicos de administração.",  # descreve a atividade disponível na sala
        "monitor": "Monitor responsável",  # informa quem acompanha a sessão da sala
        "inicio": "17:00",  # define o horário diário em que a sala abre
        "fim": "18:30",  # define o horário diário em que a sala fecha
        "capacidade": 5,  # limita a quantidade de Ratnames participantes
        "ativa": True,  # habilita a sala para entrada durante o horário definido
    },  # conclui os dados da sala de Administração
    {  # inicia os dados da sala de Projeto Interdisciplinar de Sistemas de Informação
        "id": "pisi",  # identifica a sala nas participações persistidas
        "nome": "Sala de Projeto Interdisciplinar de Sistemas de Informação",  # define o nome que aparece na interface textual
        "materia": "Pisi",  # associa a sala à disciplina selecionável no registro de presença
        "descricao": "Projeto interdisciplinar de sistemas de informação.",  # descreve a atividade disponível na sala
        "monitor": "Monitor responsável",  # informa quem acompanha a sessão da sala
        "inicio": "19:00",  # define o horário diário em que a sala abre
        "fim": "20:30",  # define o horário diário em que a sala fecha
        "capacidade": 20,  # limita a quantidade de Ratnames participantes
        "ativa": True,  # habilita a sala para entrada durante o horário definido
    },  # conclui os dados da sala de Pisi
    {  # inicia os dados da sala de Sustentabilidade
        "id": "sus",  # identifica a sala nas participações persistidas
        "nome": "Sala de Sustentabilidade em Sistemas de Informação",  # define o nome que aparece na interface textual
        "materia": "Sustentabilidade",  # associa a sala à disciplina selecionável no registro de presença
        "descricao": "Sustentabilidade em Sistemas de Informação.",  # descreve a atividade disponível na sala
        "monitor": "Monitor responsável",  # informa quem acompanha a sessão da sala
        "inicio": "21:00",  # define o horário diário em que a sala abre
        "fim": "22:00",  # define o horário diário em que a sala fecha
        "capacidade": 3,  # limita a quantidade de Ratnames participantes
        "ativa": True,  # habilita a sala para entrada durante o horário definido
    },  # conclui os dados da sala de Sustentabilidade
]  # finaliza a lista de salas usada nos menus e nas validações


def salvar_usuarios():  # grava a lista atualizada de contas no arquivo persistente
    salvar_json("usuarios.json", usuarios)  # serializa todos os usuários carregados em memória
