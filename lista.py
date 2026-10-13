from Persistencia import carregar_json, salvar_json  


usuarios = carregar_json("usuarios.json", [])  
if not isinstance(usuarios, list):  
    raise ValueError("O arquivo dados/usuarios.json deve conter uma lista de usuários.")  

usuario_logado = None  

salas_disponiveis = [  
    {  
        "id": "pp",  
        "nome": "Sala de Principios de Programação",  
        "materia": "Programação",  
        "descricao": "Revisão dos princípios de programação.",  
        "monitor": "Monitor responsável",  
        "inicio": "13:00",  
        "fim": "14:30",  
        "capacidade": 10,  
        "ativa": True,  
    },  
    {  
        "id": "fund",  
        "nome": "Sala de Fundamentos de Matemática",  
        "materia": "Matemática",  
        "descricao": "Revisão de conceitos fundamentais de matemática.",  
        "monitor": "Monitor responsável",  
        "inicio": "15:00",  
        "fim": "16:30",  
        "capacidade": 10,  
        "ativa": True,  
    },  
    {  
        "id": "adm",  
        "nome": "Sala de Introdução à Administração",  
        "materia": "Administração",  
        "descricao": "Discussão de conceitos básicos de administração.",  
        "monitor": "Monitor responsável",  
        "inicio": "17:00",  
        "fim": "18:30",  
        "capacidade": 5,  
        "ativa": True,  
    },  
    {  
        "id": "pisi",  
        "nome": "Sala de Projeto Interdisciplinar de Sistemas de Informação",  
        "materia": "Pisi",  
        "descricao": "Projeto interdisciplinar de sistemas de informação.",  
        "monitor": "Monitor responsável",  
        "inicio": "19:00",  
        "fim": "20:30",  
        "capacidade": 20,  
        "ativa": True,  
    },  
    {  
        "id": "sus",  
        "nome": "Sala de Sustentabilidade em Sistemas de Informação",  
        "materia": "Sustentabilidade",  
        "descricao": "Sustentabilidade em Sistemas de Informação.",  
        "monitor": "Monitor responsável",  
        "inicio": "21:00",  
        "fim": "22:00",  
        "capacidade": 3,  
        "ativa": True,  
    },  
]  


def salvar_usuarios():  
    salvar_json("usuarios.json", usuarios)  
