# Study Rats

**Transforme horas de estudo em conquistas.**

## Sobre o projeto

O Study Rats é uma ferramenta de apoio aos estudos desenvolvida para auxiliar estudantes na organização, acompanhamento e melhoria de sua rotina de estudos.

A proposta é transformar o tempo dedicado aos estudos em uma experiência mais organizada, motivadora e interativa.

## Funcionalidades por Release

### Release 1.0 — 1ª VA

Nesta primeira versão, serão desenvolvidas e disponibilizadas as seguintes funcionalidades:

* **Cadastro de usuário:** permite que o estudante crie sua conta no Study Rats.
* **Login de usuário:** permite que o estudante acesse sua conta utilizando seus dados cadastrados.
* **Registro da presença:** permite registrar a presença do estudante durante sua sessão de estudos.
* **Modelo de estudo:** disponibiliza um facilitador para organização dos estudos, funcionando como um cronograma para auxiliar o estudante no planejamento de sua rotina.
* **Sala de estudo:** permite que o estudante acesse salas de estudo organizadas por disciplina ou assunto, acompanhe as atividades e participe da resolução de questões.

### Persistência local

Os dados são armazenados em arquivos JSON na pasta `dados`, criada automaticamente ao iniciar a aplicação:

* `usuarios.json`: contas cadastradas. As senhas são guardadas como hashes com salt, nunca em texto puro.
* `participantes_salas.json`: participantes e tempo ativo de cada sala e sessão. A capacidade e a contagem consideram apenas quem está dentro da sala; ao sair, a vaga é liberada e o histórico do participante permanece até o término do horário da sessão.
* `presencas.json`: histórico das sessões de estudo, com disciplina, horários de início e fim e duração.
* `modelos_estudo.json`: modelo de estudo mais recente salvo por cada usuário.
* `configuracao_horario.json`: modo do relógio usado pelo programa. No menu principal, selecione **Configurar horário de teste** para fixar um horário ou voltar ao horário automático do sistema.

Após fazer login, o menu permite registrar uma sessão de estudo com cronômetro ou escolher um dos quatro modelos prontos e criar um plano personalizado.

Os horários das salas são recorrentes diariamente e usam o relógio local do computador (ou o horário manual definido para testes). Por ser um banco de dados local em arquivos, os dados ficam disponíveis neste computador e nesta cópia do projeto.

### Release 2.0 — 2ª VA

Na segunda versão, serão desenvolvidas mais cinco funcionalidades:

* **Comunidades:** permite que os estudantes participem de comunidades relacionadas a disciplinas ou assuntos de interesse.
* **Ganho de RatCoins:** permite que o estudante acumule RatCoins de acordo com sua participação e atividades realizadas no Study Rats.
* **Ranking:** permite acompanhar a posição dos estudantes de acordo com seu desempenho na plataforma.
* **Recompensas:** permite utilizar os RatCoins para obter benefícios, como recompensas relacionadas à Udemy ou Alura.
* **Interface gráfica:** desenvolvimento da interface gráfica do sistema, tornando a utilização da plataforma mais visual e interativa.

### Release 3.0 — 3ª VA

A terceira versão contará com novas funcionalidades que serão definidas durante o desenvolvimento do projeto.

* **Ratinho de IA:** assistente de inteligência artificial integrado ao Study Rats.
* **Demais funcionalidades:** a serem definidas.
