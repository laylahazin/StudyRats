# StudyRats

O StudyRats é um aplicativo de organização guiada para os estudos dos estudantes de BSI da UFRPE, unindo os alunos e monitores numa única plataforma. StudyRats reúne modelos de estudo, estudos guiados por esses modelos, salas de estudo, comunidades, calendário, rankings e recompensas em RatCoins e em Cursos. Os dados são armazenados localmente na máquina do usuário em arquivos JSON.

## Conteúdo

- Requisitos e execução
- Usando o StudyRats
- Interface Tkinter
- Ratinho, o ajudante local
- Funcionalidades
- RatCoins e regras de recompensa
- Dados e persistência
- Estrutura do projeto
- Personalizar as cores do terminal
- Privacidade e limitações

## Requisitos e execução

- Python 3.10 ou superior.
- Tkinter, incluído nas distribuições comuns de Python para Windows e mac.

Num terminal, execute o código a seguir para usar o App:

python main.py

E para usar as funcionalidades do StudyRats por meio do próprio terminal:

python main.py --cli

## Usando o StudyRats

### Sem login

Na janela, escolha *Cadastrar usuário* para criar uma conta ou *Fazer login* para entrar em uma conta existente. Durante essas operações, os prompts aparecem na área de entrada da própria janela. A senha é tratada como asteriscos enquanto é digitada por proteção.

O cadastro aceita contas do tipo `ESTUDANTE` ou `MONITOR`, exige e-mail institucional `@ufrpe.br` e valida a senha conforme as regras mostradas pelo programa.

### Com login

O painel oferece atalhos para:

Perfil -> Ver a conta, abrir operações de edição/exclusão, calendário, rankings, recompensas e acessos DEBUG.
Modelo de estudo -> Selecionar ou criar um plano de blocos de estudo e pausas.
Monitoria (Salas de Estudo) -> Consultar salas e participar durante o horário disponível.
Sessão de estudo -> Registrar disciplina e duração de uma sessão.
Comunidades -> Criar e acessar grupos, publicações, respostas e chat.
RatCoins -> Ver saldo, histórico e recompensas.
Calendário -> Consultar e administrar compromissos e lembretes.
Ranking -> Consultar os rankings de estudantes e monitores.
Área do monitor -> Criar, consultar e excluir notas privadas de monitor.
Debug -> Acessar opções habilitadas na conta, como relógio de teste e ajuste administrativo do saldo.

Algumas operações têm perguntas e submenus. A saída dessas operações e seus pedidos de informação são encaminhados para a área de texto da janela. Clique no campo de entrada e pressione *Enter* ou use o botão clicável *Enviar* para responder ou enviar dados. Não inicie outra operação enquanto a anterior estiver aguardando uma resposta.

## Interface Tkinter

A janela ao App usa o Tkinter, uma biblioteca de interface gráfica que acompanha o Python (já vem instalado com o python). O Tkinter fornece componentes básicos (Frame,Label,Button,Entry,Text e barra de rolagem), mas não fornece uma tela pronta do StudyRats. O código do projeto cria a janela, posiciona os componentes e define o que cada botão faz.

A classe 'StudyRatsGUI' em 'gui_app.py' cria a janela e os widgets. O método 'executar' chama 'mainloop', o ciclo de eventos do Tkinter que mantém a janela aberta e reage a cliques, teclas e fechamentos.

As funcionalidades antigas foram escritas para o terminal e usam `input()` e `print()`. Para aproveitá-las sem duplicar regras de negócio, a interface as executa em uma thread de trabalho. Filas (`queue.Queue`) transportam prompts, respostas e texto entre essa thread e a janela. A thread gráfica atualiza os
widgets; a thread de trabalho executa cadastro, salas, calendário e os demais
serviços. Senhas são mascaradas e não são repetidas no histórico visual.

### Como a janela é montada

1. `tk.Tk()` cria a janela principal.
2. `title`, `geometry` e `minsize` configuram título e dimensões iniciais.
3. `Frame` organiza os grupos de componentes.
4. `Label`, `Button`, `Entry`, `Text` e `Scrollbar` formam navegação,
   entrada/saída e área do Ratinho.
5. `bind("<Return>", ...)` associa a tecla Enter a uma ação.
6. O argumento `command` dos botões associa cliques a funções Python.
7. `after(50, ...)` agenda a leitura periódica da fila de eventos sem bloquear
   o ciclo gráfico.
8. `mainloop()` mantém o programa atendendo aos eventos da janela.

Portanto, trata-se de uma janela básica feita com componentes fornecidos pelo
Tkinter, não de uma tela pré-fabricada. O layout e o comportamento são definidos
no código e podem ser alterados em `gui_app.py`.

## Ratinho, o ajudante local

O campo **Ratinho — ajuda sobre o StudyRats** aceita perguntas sobre as opções
e as regras do aplicativo. A função `responder` de `AssistenteRatinho.py`
normaliza o texto digitado (minúsculas, remoção de acentos e separação em
palavras), compara os termos com tópicos de orientação e mostra as respostas
mais relevantes.

Esse ajudante é local, determinístico e não envia perguntas ou dados para a
internet. Não é um modelo de linguagem generativo: responde usando uma base
curada sobre as funcionalidades conhecidas. Para ensinar um tópico novo,
adicione palavras-chave e uma resposta à constante `ORIENTACOES` nesse arquivo.
Se a pergunta não combinar com nenhum tópico, ele indica os assuntos que sabe
explicar.

## Funcionalidades

### Contas - Cadastro, Login e CRUD COMPLETO

Cadastro de estudante ou monitor com e-mail institucional.
Login com verificação de credenciais.
Edição de e-mail, Ratname e senha.
Migração das referências locais ao trocar o Ratname.
Exclusão de conta e dados associados.
Liberação dos níveis DEBUG disponíveis.

### Modelos de estudo e sessões de estudo

Há quatro modelos predefinidos: Pomodoro, Estudo aprofundado, Revisão e
exercícios e Sessão curta. Também é possível criar um modelo personalizado com
tema, duração do bloco, duração das pausas e quantidade de blocos.

O registro de presença usa o modelo confirmado quando há um. A duração efetiva
separa estudo de pausas; somente o tempo de estudo conta para o limite de
recompensa.

### Monitoria (Salas de Estudo)

As salas são definidas em `lista.py` e têm matéria, descrição, horário e
capacidade. As sessões são recorrentes diariamente. Estudantes participam,
acompanham atividades e enviam dúvidas; monitores podem publicar atividades e
responder dúvidas. Monitores não consomem as vagas reservadas ao limite de
estudantes.

### Comunidades - Interações com outros usuários por meio do chat

Usuários podem pesquisar, criar, editar e excluir comunidades conforme as
permissões de autoria e tipo de conta. Participantes podem publicar, responder,
reagir às publicações, guardar favoritos e conversar no chat. As permissões
definem se a comunidade aceita estudantes, monitores ou ambos.

### Calendário

Compromissos guardam matéria, descrição, data e horário. É possível visualizar
o mês, adicionar, editar e excluir compromissos. O programa verifica lembretes
vencidos quando o calendário é aberto.

### Rankings, recompensas e área do monitor

Os rankings de estudantes e monitores são ordenados pelo saldo de RatCoins.
Em datas de premiação previstas no código, líderes podem receber notificações
com materiais de programação. Monitores também têm uma área de notas privada.

## RatCoins e regras de recompensa

Os ganhos são salvos em `ratcoins.json`. Eventos têm identificadores estáveis para evitar que a mesma ação gere o mesmo bônus mais de uma vez.

| Ação | Recompensa |
|---|---:|
| Presença de estudante com pelo menos 30 minutos efetivos de estudo | +15 RC |
| Primeiro modelo de estudo salvo e usado por um estudante | +15 RC |
| Primeira entrada de estudante na sala em cada sessão diária | +20 RC |
| Entrada explícita de estudante em uma comunidade | +10 RC |
| Criação de comunidade por estudante | +20 RC |
| Atividade publicada por monitor em uma sala | +5 RC |

Pausas não contam como tempo efetivo para os 30 minutos. Monitores não recebem
os bônus reservados a estudantes. Ajustes administrativos pelo DEBUG 2 ficam
registrados como lançamentos próprios e não alteram o histórico original.

## Dados e persistência

Os arquivos ficam na pasta `dados/`, ao lado do código principal. `Dados.py`
cria os arquivos ausentes e faz leitura/gravação JSON. Ao salvar, o programa
grava primeiro em um arquivo temporário e o move para o destino, reduzindo o
risco de deixar um JSON parcialmente escrito.

| Arquivo | Conteúdo |
|---|---|
| `usuarios.json` | Contas, tipo de usuário, e-mail, Ratname, salt e hash da senha. |
| `modelos_estudo.json` | Modelo de estudo ativo de cada Ratname. |
| `presencas.json` | Histórico de sessões e tempo efetivo por usuário. |
| `participantes_salas.json` | Participantes, atividades e dúvidas por sala e sessão. |
| `ratcoins.json` | Histórico de lançamentos e eventos de recompensa processados. |
| `comunidades.json` | Comunidades, membros, publicações, respostas, reações e mensagens. |
| `calendario.json` | Compromissos e estado dos lembretes por usuário. |
| `blocos_notas.json` | Notas privadas dos monitores. |
| `configuracao_horario.json` | Relógio automático ou horário manual para testes. |
| `notificacoes.json` | Notificações de recompensa e datas já processadas. |

Os dados não são enviados a um servidor e não são compartilhados entre cópias
do projeto. Faça cópias de segurança da pasta `dados/` para preservar contas e
históricos.

As senhas não são gravadas em texto puro: `Dados.py` gera um salt aleatório e
usa PBKDF2-HMAC com SHA-256. A verificação compara os hashes com
`hmac.compare_digest`.

## Estrutura do projeto

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Compõe os gerenciadores e inicia a interface gráfica ou o menu CLI. |
| `gui_app.py` | Janela Tkinter, navegação, entrada/saída, threads e comunicação com a aplicação. |
| `AssistenteRatinho.py` | Base local de conhecimento e busca de orientações do Ratinho. |
| `TemaTerminal.py` | Paleta ANSI e funções de apresentação do menu de terminal. |
| `lista.py` | Estado compartilhado, usuários conectados e salas disponíveis. |
| `Dados.py` | Persistência JSON e criação/verificação de credenciais. |
| `CadastroUsuario.py` | Validação e criação de contas. |
| `LoginUsuario.py` | Login, logout, edição, exclusão, permissões e migração de dados da conta. |
| `ModeloEstudo.py` | Modelos predefinidos, criação personalizada, confirmação e exibição. |
| `RegistroPresenca.py` | Cronômetro, alternância de blocos e gravação do histórico de estudo. |
| `SalaEstudo.py` | Horários, capacidade, participação e interações nas salas. |
| `Comunidades.py` | Comunidades, membros, publicações, chat e permissões. |
| `Calendario.py` | Compromissos, visualização mensal e lembretes. |
| `Horario.py` | Relógio automático ou manual para testes. |
| `Ratcoins.py` | Ganhos, saldo, histórico, ajustes e proteção contra duplicidades. |
| `Recompensas.py` | Regras e notificações de recompensas. |
| `RankingEstudantes.py` | Ranking de estudantes por saldo. |
| `RankingMonitores.py` | Ranking de monitores por saldo. |
| `AreaMonitor.py` | Acesso às salas e notas privadas do monitor. |

## Personalizar as cores do terminal

O modo `--cli` usa sequências ANSI sem pacote externo. Edite a constante
`CORES` em `TemaTerminal.py` para mudar as cores. O programa desativa a cor
quando a saída não é um terminal interativo ou quando a variável `NO_COLOR`
está definida.

## Privacidade e limitações

- O banco de dados é local em JSON, sem sincronização entre dispositivos.
- O Ratinho responde apenas a tópicos incluídos em sua base local e pode não
  entender perguntas fora desse escopo.
- O calendário e as salas usam o relógio local, exceto quando DEBUG 1 define
  um horário manual.
- A janela usa os diálogos de texto das funcionalidades atuais dentro de um
  painel; ela não transforma automaticamente cada formulário de terminal em
  um formulário gráfico separado.
