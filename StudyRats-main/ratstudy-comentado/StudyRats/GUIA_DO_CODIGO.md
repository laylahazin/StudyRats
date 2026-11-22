# Guia detalhado de leitura do StudyRats

Este guia acompanha a cópia Python desta pasta. Ele explica o papel dos módulos,
as classes e funções principais, os dados que circulam entre elas e o caminho de
execução. Cada módulo Python tem comentários junto às instruções para explicar o
código linha a linha; este guia complementa as anotações com o mapa da
arquitetura e as relações entre arquivos. A cópia permanece funcionalmente
equivalente aos módulos da raiz.

## Visão geral da arquitetura

O programa é composto por quatro camadas simples:

1. **Entrada e interface:** `main.py` decide entre a janela Tkinter e o menu CLI.
   `gui_app.py` conecta botões e campos ao mesmo objeto de aplicação.
2. **Coordenação e estado:** `AplicacaoStudyRats` monta os gerenciadores; `lista.py`
   contém o estado compartilhado, como usuário conectado e salas.
3. **Regras de negócio:** módulos como `RegistroPresenca.py`, `SalaEstudo.py`,
   `Comunidades.py` e `Calendario.py` implementam os fluxos do aplicativo.
4. **Persistência:** `Dados.py` lê e grava arquivos JSON na pasta `dados/`.
   Gerenciadores de funcionalidades chamam esse serviço e validam a estrutura
   lida antes de usá-la.

### Fluxo de inicialização

1. O bloco `if __name__ == "__main__"` de `main.py` interpreta `--cli`.
2. `AplicacaoStudyRats()` cria o estado compartilhado e instancia os serviços.
3. No modo gráfico, `iniciar_interface` inicializa os JSON, remove sessões de
   sala expiradas e cria `StudyRatsGUI`.
4. No modo terminal, `AplicacaoStudyRats.executar` faz a mesma preparação e
   inicia o laço de menu.
5. Após uma operação, os menus são reconstruídos a partir do usuário conectado.

## Estado e persistência

### `lista.py` — `EstadoAplicacao`

- `usuarios`: lista de dicionários de contas carregada e atualizada pelo estado.
- `usuario_logado`: Ratname da conta conectada, ou `None`.
- `salas_disponiveis`: catálogo de salas definidas pelo aplicativo.
- `TIPO_ESTUDANTE` e `TIPO_MONITOR`: valores de referência usados nas permissões.
- `definir_usuario_logado`: define ou limpa a identidade da sessão; o tipo é
  derivado da conta por meio da propriedade `tipo_usuario_logado`.
- `substituir_usuarios` e `salvar_usuarios`: atualizam a lista e sua persistência.
- `tipo_usuario_logado`: propriedade para consultar o tipo da conta conectada.

O objeto global `estado` é compartilhado pelos gerenciadores; os nomes globais
legados (`usuarios`, `usuario_logado`, `salas_disponiveis`) preservam acessos
de compatibilidade.

### `Dados.py` — armazenamento e credenciais

`DIRETORIO_DADOS` determina o local dos arquivos JSON em relação ao próprio
módulo.

**`PersistenciaJSON`**

- `diretorio`: caminho-base do repositório, substituível em testes.
- `_caminho_arquivo`: combina o diretório-base com o nome do arquivo.
- `inicializar_arquivos`: cria apenas os JSON ausentes com valores iniciais.
- `carregar`: interpreta JSON; se o arquivo não existe, devolve o padrão
  solicitado. JSON malformado resulta em `ValueError`, não em dados vazios
  silenciosos.
- `salvar`: serializa UTF-8 em arquivo temporário e usa `os.replace` para
  substituir o destino depois da gravação.

**`GerenciadorCredenciais`**

- `ITERACOES`: custo computacional configurado para PBKDF2.
- `criar`: gera salt aleatório e calcula hash PBKDF2-HMAC-SHA-256 da senha.
- `verificar`: recalcula o hash com o salt guardado e compara com
  `hmac.compare_digest`.

Os objetos globais `persistencia` e `gerenciador_credenciais` são usados pelos
adaptadores de compatibilidade (`carregar_json`, `salvar_json` etc.). A senha
original não é armazenada.

## Entrada, conta e navegação

### `main.py` — `AplicacaoStudyRats`

O construtor guarda o estado e instancia cadastro, contas, relógio, salas,
comunidades, calendário, presença, modelos, rankings e recompensas.

- `executar`: inicializa dados e salas expiradas; mantém o laço principal,
  verifica notificações e direciona a escolha conforme haja login.
- `_exibir_menu`: apresenta opções diferentes para sessão conectada e
  desconectada.
- `_processar_menu_conectado` / `_processar_menu_desconectado`: mapeiam opções
  textuais para funções e informam opções inválidas.
- `_menu_perfil`: centraliza calendário, rankings, RatCoins, edição/exclusão e
  opções de depuração; a área do monitor só aparece para monitores.
- `_menu_debug`: oferece apenas os níveis DEBUG já liberados para a conta.
- `_alterar_saldo_ratcoins`: valida número, permissão e confirmação antes do
  ajuste administrativo.
- `_usuario_atual`: localiza a conta correspondente ao Ratname conectado.
- `_usar_modelo_estudo`: chama o gerenciador e verifica se o primeiro modelo
  confirmado deve conceder a recompensa de estudante.

### `CadastroUsuario.py` — `CadastroUsuario`

- `cadastrar`: executa o fluxo e salva a nova conta após validações.
- `_ler_email`: solicita e valida o e-mail institucional.
- `_ler_tipo_usuario`: seleciona estudante ou monitor.
- `_ler_senha`: solicita e valida uma senha conforme as regras do programa.
- `_ler_ratname`: coleta o identificador de usuário e valida unicidade/formato.

### `LoginUsuario.py` — `GerenciadorConta`

- `realizar_login`: verifica os dados de acesso e atualiza o estado de sessão.
- `deslogar`: encerra a sessão conectada.
- `editar_conta`: atualiza credenciais e/ou identificador após validações.
- `_confirmar_senha_atual`, `_email_valido` e `_senha_valida`: verificações
  reutilizadas nos fluxos de conta.
- `excluir_conta`: confirma e remove a conta e suas referências locais.
- `_atualizar_referencias_usuario`: coordena a mudança de Ratname nos dados.
- `_atualizar_participacoes`, `_atualizar_comunidades` e
  `_atualizar_notificacoes`: migram as referências de usuário nesses arquivos.
- `menu_debug_codes` e `tem_acesso_debug`: liberam e consultam permissões
  DEBUG persistidas na conta.
- `_usuario_logado`: recupera a conta atual para operações protegidas.

## Modelos, sessões e salas

### `ModeloEstudo.py` — `GerenciadorModelosEstudo`

Este módulo contém comentários pedagógicos mais próximos do código. Um modelo é
um dicionário com `nome` e `blocos`; cada bloco é um par com o texto da atividade
e sua duração em minutos.

- `ARQUIVO_MODELOS`: nome do JSON dos modelos ativos.
- `MODELOS_PREDEFINIDOS`: catálogo com quatro planos disponíveis no menu.
- `__init__`: recebe estado e repositório substituíveis, ou usa os padrões.
- `_ler_duracao`: repete a pergunta até receber inteiro dentro dos limites.
- `_criar_modelo_personalizado`: lê tema, duração de estudo, duração de pausa e
  quantidade de blocos; produz a mesma estrutura dos planos prontos.
- `_salvar_modelo`: carrega os modelos existentes, marca confirmação e salva o
  plano sob o Ratname.
- `_exibir_modelo`: percorre blocos, acumula minutos e mostra início/fim e total.
- `_exibir_modelo_atual`: busca o plano da conta e lida com ausência de plano.
- `executar`: exige login, apresenta o menu, permite visualizar, selecionar ou
  criar um plano e só salva após confirmação.
- `modelo_estudo`: função de entrada para executar o gerenciador diretamente.

### `RegistroPresenca.py` — `RegistroPresenca`

O registro integra o modelo ativo, o relógio, o histórico de presença e a
recompensa.

- `registrar`: valida login e disciplina, inicia o cronômetro, calcula duração
  total e tempo efetivo, salva um evento com ID e aplica a regra de RatCoins.
- `_obter_modelo_atual`: lê e valida o plano associado à conta.
- `_ler_blocos`: converte minutos salvos para segundos e valida cada par.
- `_aguardar_finalizacao`: acompanha tempo; suporta finalização digitada e
  tratamento de relógio manual.
- `_exibir_bloco` e `_bloco_atual`: identificam a atividade atual e exibem o
  tempo decorrido/restante.
- `_calcular_tempo_estudo`: soma apenas blocos que não são pausas.
- `_eh_pausa`: reconhece nomes com “pausa”, “descanso” ou “break”.
- `_formatar_duracao`: converte segundos em `HH:MM:SS`.
- `_ler_disciplina`: aceita uma disciplina disponível sem diferenciar caixa.

Em Windows com terminal interativo, `msvcrt` permite ler teclas sem exigir
Enter em cada caractere; em outros contextos, o fluxo usa `input()`.

### `SalaEstudo.py` — `GerenciadorSalas`

- `_intervalo_sessao`: calcula começo/fim da sala no dia corrente, inclusive
  salas que atravessam a meia-noite.
- `_chave_sessao`: transforma o início em identificador da sessão recorrente.
- `_carregar_participacoes`: valida JSON e remove sessões expiradas.
- `_obter_sessao`: recupera ou cria os dados de uma sala/sessão.
- `_contar_participantes_ativos`: conta estudantes ativos para o limite de vagas.
- `listar_salas`: apresenta horário, capacidade e disponibilidade.
- `exibir_sala_de_estudo`: valida login, sala, horário e vagas antes de entrar.
- `_exibir_detalhes_sala` e `_interagir_com_sala`: conduzem a tela e as ações
  disponíveis a estudantes ou monitores.
- `_exibir_atividades_e_duvidas`, `_criar_atividade`, `_responder_duvida` e
  `_enviar_duvida`: administram atividades e perguntas da sessão.
- `_sair_da_sala` e `_finalizar_atividade`: encerram participação/atividade e
  atualizam dados persistidos.
- `limpar_sessoes_expiradas`: executa a limpeza usando o relógio atual.

O objeto de horário é injetável no construtor para que salas e testes usem a
mesma fonte de tempo.

### `Horario.py` — `GerenciadorHorario`

- `obter_horario_atual`: retorna horário real ou data/hora manual configurada.
- `acessar_configuracao` / `_carregar_configuracao`: leem e validam o JSON.
- `configurar`: permite alterar modo ou horário quando chamado pelo DEBUG.
- `_modo_manual_ativo` / `modo_manual_ativo`: informam se o relógio está manual.

## Comunidades, calendário e área de monitor

### `Comunidades.py` — `GerenciadorComunidades`

Os registros de comunidade guardam identificação, criador, público, membros,
publicações e mensagens. Publicações possuem listas de likes, dislikes e
favoritos.

- `_carregar` / `_salvar`: lê, migra campos antigos quando necessário, valida e
  grava comunidades.
- `menu`: apresenta ações para usuário conectado.
- `listar` / `pesquisar`: exibem comunidades ou filtram por nome, disciplina e
  assunto.
- `criar` / `editar` / `excluir`: mantêm comunidades respeitando autoria e
  permissões.
- `entrar`: associa usuário elegível como membro e registra o evento pertinente.
- `_menu_publicacoes` / `_ver_publicacoes`: navegam pelas publicações.
- `_interagir_publicacao`: gerencia reações e favoritos.
- `_criar_publicacao` / `_responder_publicacao`: publicam conteúdo e respostas.
- `_consultar_favoritos`: mostra publicações salvas pelo usuário.
- `_menu_chat`: lê e publica mensagens de chat.
- `_usuario_atual`, `_tipo_usuario`, `_usuario_pode_acessar` e
  `_nome_tipo_acesso`: consultam sessão e aplicam regras de público.
- `_selecionar` / `_exibir_detalhes`: selecionam uma comunidade e mostram seus
  dados.

### `Calendario.py` — `GerenciadorCalendario`

- `menu`: encaminha para listar, visualizar, criar, editar e excluir eventos.
- `_carregar` / `_compromissos_usuario`: recuperam eventos e isolam os da conta.
- `listar_compromissos` / `visualizar_calendario`: exibem lista ou mês.
- `adicionar_compromisso`, `editar_compromisso`, `excluir_compromisso`: mantêm
  compromissos da conta autenticada.
- `verificar_lembretes`: identifica e processa lembretes vencidos.
- `_interpretar_data_hora` / `_data_hora`: convertem entradas em valores de
  data/hora usados pelo calendário.
- `_exibir_lista` / `_ler_indice`: formatam resultados e validam seleção.
- `_usuario_atual`: restringe ações ao usuário conectado.

### `AreaMonitor.py` — `AreaMonitor`

- `menu`: apresenta notas e ferramentas disponíveis ao monitor.
- `_monitor_logado`: verifica o tipo da conta antes de liberar a área.
- `_carregar`: lê os blocos de notas do arquivo JSON.
- `criar_bloco`, `listar_blocos` e `excluir_bloco`: criam, exibem e removem
  notas privadas.
- O construtor recebe o gerenciador de salas para reutilizar consulta de salas.

## RatCoins, rankings e recompensas

### `Ratcoins.py` — `GerenciadorRatCoins`

- `_carregar_dados`: valida a estrutura atual e reconhece o formato legado.
- `_salvar_dados`: persiste o histórico e os IDs de eventos.
- `registrar_ganho`: valida valor, registra atividade e evita repetição do mesmo
  `evento_id`.
- `saldo`: soma os pontos validados do histórico.
- `ajustar_saldo`: exige usuário conectado e DEBUG 2; grava apenas a diferença
  como ajuste rastreável.
- `renomear_usuario` / `remover_usuario`: migram ou removem os registros da
  conta.
- `historico`, `consultar_saldo` e `consultar_historico`: consultam e exibem
  lançamentos.
- `menu` / `_usuario_atual`: protegem o menu com login.
- `gerenciador_ratcoins`: instância compartilhada usada pelos demais módulos.

### `Recompensas.py` — `Recompensas`

- `menu`: explica as regras de pontuação por tipo de conta.
- `verificar_notificacoes`: verifica datas e posições do ranking já processadas.
- `_notificar_lideres`: cria notificações para líderes nas datas previstas.

### `RankingEstudantes.py` — `GerenciadorRankingEstudantes`

- `exibir_ranking`: filtra estudantes, consulta seus saldos e ordena a lista.
- `menu`: apresenta o ranking pelo menu do perfil.

### `RankingMonitores.py` — `GerenciadorRankingMonitores`

- `exibir`: filtra e ordena monitores pelo saldo de RatCoins.
- `menu`: oferece a consulta pelo menu de perfil.

## Interface, assistente e terminal

### `gui_app.py` — `StudyRatsGUI`

Tkinter fornece widgets e o ciclo de eventos; o projeto constrói a tela e as
ações.

- `_SaidaJanela.write`: envia texto para uma fila em vez de alterar widgets por
  uma thread de trabalho.
- `StudyRatsGUI.__init__`: configura janela, filas, estado dos controles e
  agendamento do processamento de eventos.
- `_criar_widgets`: monta navegação, área de texto, entrada, botões e Ratinho.
- `_atualizar_menu`: reconstrói opções conforme o usuário conectado.
- `_executar`: roda uma operação legada em thread; adapta `input` e `print` para
  as filas e restaura as funções originais ao terminar.
- `_processar_eventos`: na thread gráfica, recebe saída, prompts e conclusão.
- `_enviar_entrada`: devolve a resposta à thread que aguarda `input`.
- `_perguntar` / `_mostrar_resposta`: encaminham e exibem respostas do Ratinho.
- `_escrever`: atualiza o widget de saída na thread da interface.
- `_habilitar_menu`: evita iniciar ações sobrepostas.
- `_fechar`: acorda uma entrada pendente e encerra a janela.
- `executar`: inicia `mainloop`.
- `iniciar_interface`: prepara persistência/salas e inicia a janela.

`queue.Queue` é o canal seguro de mensagens entre threads; `root.after` agenda
o consumo dessa fila no ciclo do Tkinter. Widgets devem ser atualizados pela
thread gráfica, não diretamente pela thread trabalhadora.

### `AssistenteRatinho.py`

- `ORIENTACOES`: catálogo local de tópicos, termos de busca e respostas.
- `_normalizar`: coloca texto em forma comparável, removendo diferenças de caixa
  e acentos.
- `responder`: identifica tópicos correspondentes e retorna uma resposta ou
  orientação de fallback.

O ajudante é determinístico e não é um modelo generativo. Para ampliar o
vocabulário, atualize as orientações no próprio módulo.

### `TemaTerminal.py`

- `CORES`: nomes associados a sequências ANSI personalizáveis.
- `_ativar_ansi_windows`: prepara suporte a ANSI no terminal Windows quando
  disponível.
- `colorir`: adiciona sequência de cor se a saída interativa permitir.
- `titulo`, `opcao`, `perguntar` e `mensagem`: centralizam formatação do CLI.

O módulo evita colorir quando `NO_COLOR` está definido ou quando a saída não é
um terminal interativo.

## Fluxos em uma frase

- **Cadastro/login:** `main.py` → `CadastroUsuario` ou `GerenciadorConta` →
  `EstadoAplicacao` e `Dados.py`.
- **Modelo:** menu → `GerenciadorModelosEstudo` → `modelos_estudo.json`.
- **Presença:** menu → `RegistroPresenca` → relógio/modelo → `presencas.json` →
  `GerenciadorRatCoins`, se a regra for satisfeita.
- **Sala:** menu → `GerenciadorSalas` → horário e participantes → atividades,
  dúvidas e RatCoins de monitor conforme a ação.
- **Calendário/comunidades:** menu → gerenciador correspondente → JSON local.
- **Ratinho:** campo da GUI → `responder` → base `ORIENTACOES`; sem chamada à
  rede.

## Observações para edição

- O formato de JSON é parte do contrato entre os módulos; preserve chaves e
  tipos ou implemente migração explícita.
- Use `PersistenciaJSON` em vez de abrir os arquivos de dados diretamente.
- IDs estáveis de evento protegem recompensas contra duplicação.
- A GUI reutiliza fluxos de terminal; por isso, novas operações que chamem
  `input`/`print` são encaminhadas pelo adaptador de `gui_app.py`.
- `ratstudy-comentado` é uma cópia de estudo. Ao mudar regras na aplicação
  principal, atualize a cópia conscientemente para evitar divergência.
