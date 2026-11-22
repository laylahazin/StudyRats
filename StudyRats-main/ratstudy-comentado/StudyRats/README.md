# StudyRats — cópia comentada para estudo

Esta pasta contém uma cópia dos módulos Python da aplicação StudyRats. Ela foi
sincronizada com os arquivos Python da pasta principal; os JSON locais foram
preservados. A cópia serve para leitura e experimentação, e não é a fonte
principal do projeto.

## Executar

Requisitos: Python 3.10 ou superior, com Tkinter disponível. Não há dependências
externas necessárias.

```powershell
python main.py
```

Esse comando abre a janela Tkinter. Para executar o menu de terminal:

```powershell
python main.py --cli
```

Os dados da cópia são gravados em `dados/`, separadamente dos dados da pasta
principal. Faça backup dessa pasta antes de testar alterações.

## Como estudar o código

1. Leia `main.py` para acompanhar a composição dos serviços e o fluxo dos menus.
2. Leia `lista.py` para entender o estado compartilhado e o login atual.
3. Leia `Dados.py` para ver persistência JSON e proteção das senhas.
4. Escolha um fluxo, como modelo de estudo ou presença, e acompanhe os módulos
   correspondentes no guia.
5. Consulte `GUIA_DO_CODIGO.md` para o mapa de classes, métodos, dados e fluxo.
6. Para entender a janela, veja `gui_app.py` junto da seção sobre Tkinter no
   README da pasta principal.

Todos os arquivos Python desta pasta incluem comentários explicativos junto às
linhas de código. `GUIA_DO_CODIGO.md` complementa essas anotações com o mapa de
arquitetura, dados e relações entre módulos. Os comentários não alteram as
regras funcionais da cópia.

## Ratinho

O Ratinho é um ajudante local baseado em palavras-chave em
`AssistenteRatinho.py`. Ele não usa um serviço de IA generativa e não envia
perguntas à internet.

## Arquivos de dados

Os arquivos JSON ficam em `dados/` e contêm contas, modelos, presenças,
participantes de salas, comunidades, calendário, notas, RatCoins, horários e
notificações. Eles podem conter dados pessoais: não publique nem compartilhe
essa pasta.
