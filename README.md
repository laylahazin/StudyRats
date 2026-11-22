# StudyRats

> **Estude, conquiste, cresça.**

O **StudyRats** é uma aplicação de gestão de estudos gamificada desenvolvida em **Python 3.10+**, com duas interfaces intercambiáveis: uma **CLI colorida** para terminal e uma **GUI em Tkinter**. O sistema integra cadastro de usuários, modelos de estudo (Pomodoro personalizável), salas de estudo com monitores, comunidades, calendário, rankings e um sistema de recompensas chamado **RatCoins**.

---

## Sumário

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura e Organização dos Módulos](#-arquitetura-e-organização-dos-módulos)
- [Bibliotecas Utilizadas](#-bibliotecas-utilizadas)
- [Requisitos e Instalação](#-requisitos-e-instalação)
- [Como Rodar](#-como-rodar)
- [Fluxogramas](#-fluxogramas)

---

## Visão Geral

O StudyRats foi projetado para ajudar estudantes e monitores a organizarem sua rotina de estudos de forma engajadora. A aplicação combina:

- **Gestão acadêmica**: cadastro, login, perfil, edição e exclusão de conta;
- **Foco nos estudos**: modelos de estudo com blocos de foco/pausa (estilo Pomodoro), cronômetro de presença e calendário com lembretes;
- **Colaboração**: salas de estudo com monitores, comunidades com posts, chat, likes e favoritos;
- **Gamificação**: sistema de RatCoins, rankings de estudantes e monitores, e recompensas por conquistas.

O projeto adota uma **arquitetura modular baseada em gerenciadores especializados**, com separação clara entre domínio, persistência, estado global e apresentação.

---

## Funcionalidades

| Módulo | Funcionalidades |
|---|---|
| **Autenticação** | Cadastro com validação de e-mail institucional (`@ufrpe.br`), senha forte (6–8 caracteres, maiúscula, número e caractere especial) e Ratname único; login com hash + salt; edição e exclusão de conta com confirmação. |
| **Modelos de estudo** | Criação de modelos personalizados com blocos de estudo e pausa (Pomodoro customizável), persistidos por usuário. |
| **Registro de presença** | Cronômetro com blocos do modelo; modo interativo no Windows (`msvcrt`) e modo "digite `finalizar`" em outros TTYs; cálculo do tempo efetivo de estudo (excluindo pausas). |
| **Salas de estudo** | Salas por disciplina com monitores, sessões com expiração, atividades, dúvidas e respostas. |
| **Área do monitor** | Blocos de notas por matéria, materiais complementares e exclusão. |
| **Comunidades** | Criação com controle de público (estudantes / estudantes+monitores / monitores), posts com material compartilhado, respostas, likes/dislikes/favoritos e chat. |
| **Calendário** | Compromissos de estudo com data/hora, visualização mensal com marcadores e lembretes automáticos. |
| **RatCoins** | Saldo, histórico, ganho idempotente por evento e ajuste administrativo (DEBUG 2). |
| **Rankings** | Rankings de estudantes e de monitores. |
| **Assistente Ratinho** | Chat de ajuda embutido na GUI, respondendo dúvidas sobre o uso do sistema. |

---

## Arquitetura e Organização dos Módulos

O projeto segue uma **organização por feature/domínio**, com um orquestrador central (`AplicacaoStudyRats` em `main.py`) que instancia e injeta dependências entre os gerenciadores.


### Convenções identificadas

- **Classes `Gerenciador*`** para domínios com estado persistente.
- **Singleton de módulo** para `gerenciador_ratcoins` (importado diretamente por outros módulos).
- **Menu pattern**: cada gerenciador expõe `menu()` que faz loop de `input()` + dispatch por dicionário de ações.
- **Validação de schema inline** em `_carregar()` de cada gerenciador, com `ValueError` descritivo.
- **Injeção de dependência** entre gerenciadores (ex.: `GerenciadorSalas(horario)`, `GerenciadorCalendario(horario)`, `AreaMonitor(salas)`).

### Módulos internos

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada + orquestrador `AplicacaoStudyRats`; parsing de `--cli`. |
| `gui_app.py` | Interface Tkinter; integra a GUI com a lógica CLI via filas. |
| `lista.py` | Estado global compartilhado (`estado.usuarios`, `estado.usuario_logado`, etc.). |
| `Dados.py` | `persistencia` (JSON) + `gerenciador_credenciais` (hash/salt). |
| `TemaTerminal.py` | Cores ANSI + helpers de terminal (`titulo`, `opcao`, `perguntar`, `mensagem`). |
| `Horario.py` | `GerenciadorHorario` (modo automático/manual para testes). |
| `CadastroUsuario.py` | Cadastro de novos usuários. |
| `LoginUsuario.py` | Login, edição/exclusão de conta, códigos DEBUG. |
| `ModeloEstudo.py` | Modelos de estudo personalizados. |
| `RegistroPresenca.py` | Cronômetro de estudo + concessão de RatCoins. |
| `SalaEstudo.py` | Salas de estudo com monitores e sessões. |
| `AreaMonitor.py` | Área exclusiva do monitor (notas, salas). |
| `Comunidades.py` | Comunidades, posts, chat, interações. |
| `Calendario.py` | Compromissos de estudo e lembretes. |
| `Ratcoins.py` | Gerenciador de RatCoins (singleton). |
| `Recompensas.py` | Menu de recompensas + notificações. |
| `RankingEstudantes.py` | Ranking de estudantes. |
| `RankingMonitores.py` | Ranking de monitores. |
| `AssistenteRatinho.py` | Assistente de ajuda (`responder(pergunta)`). |


### Arquivos JSON

| Arquivo |	Conteúdo |
|---|---|
|usuarios.json	| Contas cadastradas (credenciais com hash/salt). |
|modelos_estudo.json	| Modelos de estudo por usuário. |
|presencas.json | Histórico de sessões de estudo. |
|calendario.json | Compromissos por usuário. |
|blocos_notas.json | Notas criadas por monitores. |
|comunidades.json | Comunidades, posts, chats e interações. |
|ratcoins.json | Histórico de RatCoins e eventos processados. |
|notificacoes.json | Notificações pendentes por usuário. |
|participantes_salas.json | Participantes e atividades das salas.|
|configuracao_horario.json | Configuração do modo de horário (automático/manual). |

---

## Bibliotecas Utilizadas

O projeto prioriza a **biblioteca padrão do Python**, com apenas o `tkinter` (que acompanha o CPython) para a GUI. **Não há dependências externas obrigatórias**.

| Biblioteca | Origem | Uso no projeto | Justificativa |
|---|---|---|---|
| `tkinter` / `tkinter.ttk` | Stdlib | Interface gráfica (`gui_app.py`) | Widgets nativos multiplataforma sem dependências externas. |
| `queue` | Stdlib | Ponte thread↔GUI | `Queue` é thread-safe por design — ideal para comunicação entre a thread de negócio e o loop Tk. |
| `threading` | Stdlib | Execução das ações sem travar a GUI | Necessário porque `mainloop()` do Tk é single-threaded. |
| `argparse` | Stdlib | Flag `--cli` em `main.py` | Parsing de argumentos robusto e auto-documentado. |
| `builtins` | Stdlib | Interceptação de `input`/`print` | Permite reutilizar todo o código CLI na GUI sem reescrevê-lo. |
| `json` | Stdlib | Persistência | Formato legível, inspecionável manualmente, sem servidor. |
| `uuid` | Stdlib | IDs únicos de comunidades, presenças, eventos RatCoins | Evita colisão sem coordenação central. |
| `hashlib` / `secrets` | Stdlib | Hash + salt de senhas | Boas práticas de armazenamento de credenciais. |
| `datetime` | Stdlib | Calendário, cronômetro, horário simulável | Manipulação de datas robusta. |
| `calendar` | Stdlib | Renderização do calendário mensal | Geração da matriz semanal pronta. |
| `os`, `sys`, `shutil`, `time` | Stdlib | Detecção de TTY, largura do terminal, temporização, ANSI no Windows | Controle fino da saída em terminal. |
| `msvcrt` | Stdlib (Windows) | Leitura não-bloqueante de teclas no cronômetro | Único meio nativo no Windows para `kbhit`/`getwch`. |
| `ctypes` | Stdlib | Ativação de ANSI no console Windows | Habilita `ENABLE_VIRTUAL_TERMINAL_PROCESSING`. |

---

## Requisitos e Instalação

### Requisitos

- **Python 3.10+** (uso intensivo de `str | None`, `dict | None`, `tuple[str, str]`).
- **Tkinter** disponível na instalação.
  - No **Linux (Debian/Ubuntu)**: `sudo apt install python3-tk`
  - No **Windows/macOS**: já incluso na instalação oficial do Python.
- **Terminal com suporte a TTY** para a experiência CLI colorida (opcional; a GUI é o padrão).

## Como Rodar

# Interface gráfica (recomendada)
python main.py

# Interface CLI colorida (terminal)
python main.py --cli

## Fluxogramas
Link: https://app.diagrams.net/#G1xDOIbS7_qCYvkIVmBODh53pixesGJsD9#%7B%22pageId%22%3A%227CZMHdt9vsC0GG7J5-9B%22%7D
