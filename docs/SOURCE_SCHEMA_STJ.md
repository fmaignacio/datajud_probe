# Schema de Fontes STJ

Este documento define uma camada canonica minima para organizar as fontes do
projeto `datajud_probe` no eixo STJ. O objetivo e separar:

- o papel de cada fonte;
- as chaves de ligacao;
- a cobertura temporal observada;
- os limites metodologicos;
- os recortes usados por notebook.

## Objetivo

O projeto usa o STJ como base textual principal, mas as fontes nao cobrem o
mesmo periodo nem oferecem o mesmo tipo de dado. Por isso, a pergunta correta
nao e apenas "quais dados temos", mas:

> o que cada fonte permite observar, em que periodo, por qual chave, e com
> qual grau de completude.

## Entidades canonicas

### 1. `processo`

Unidade logica de integracao longitudinal.

Campos minimos:

- `numero_processo`
- `numero_registro_stj`
- `processo_agregacao`
- `classe_stj`
- `classe_datajud`
- `tribunal_cnj`
- `segmento_cnj`
- `timeline_start`
- `timeline_end`
- `fontes_disponiveis[]`
- `janela_analitica`

Regras:

- `numero_processo` e a chave principal quando existir.
- `numero_registro_stj` e a chave auxiliar principal no ecossistema STJ.
- `processo_agregacao` pode usar `numero_processo`, senao `numero_registro_stj`.

### 2. `documento`

Unidade textual e documental do corpus STJ.

Campos minimos:

- `seq_documento`
- `numero_registro_stj`
- `numero_processo`
- `data_documento`
- `tipo_documento`
- `ministro_documento`
- `texto_limpo`
- `fonte_documental`
- `metadata_file`
- `txt_path`

Regras:

- `seq_documento` e a chave documental.
- `numero_registro_stj` e a principal ponte com o corpus de integras.

### 3. `evento_processual`

Unidade de linha do tempo.

Campos minimos:

- `processo_agregacao`
- `numero_processo`
- `numero_registro_stj`
- `event_datetime`
- `event_source`
- `event_type`
- `event_label`
- `event_detail`
- `event_code_original`
- `event_parent_code`
- `event_level`

Regras:

- eventos podem vir de `ata_stj`, `datajud_stj`, `integra_stj`,
  `movimentacao_stj` ou outras fontes futuras;
- o schema deve preservar o codigo original e o rotulo normalizado.

### 4. `contexto_juridico`

Camada semantica e classificatoria.

Campos minimos:

- `classe`
- `assuntos[]`
- `precedente_sequencial`
- `precedente_tipo`
- `precedente_numero`
- `questao_submetida`
- `tese_firmada`
- `leading_case`
- `tribunal_origem`
- `tipo_justica_origem`

## Fontes atuais

### `stj_integras`

Papel:

- base textual principal do projeto

Chaves:

- principal: `numero_registro_stj`
- documental: `seq_documento`
- secundaria: `numero_processo` quando existir

Cobertura observada:

- corpus textual disponivel apenas a partir de alguma data de `2021`
- confirmar o marco exato em validacao futura

Limitacoes:

- nao sustenta observacao textual anterior ao inicio do corpus;
- nem todos os documentos trazem CNJ;
- a ponte com processo depende fortemente de `numero_registro_stj`.

### `ata_distribuicao_stj`

Papel:

- metadados de entrada/distribuicao no STJ

Chaves:

- `numeroUnico` / `numero_processo`
- `numeroRegistro` / `numero_registro_stj`

Cobertura observada:

- apenas a partir de `2023-06-30`

Limitacoes:

- nao serve como espinha dorsal unica para recortes `2019-2022`;
- e muito util para periodo recente e para reconciliar CNJ com registro STJ.

### `datajud_stj`

Papel:

- metadados estruturados, assuntos, classe, orgao julgador e movimentos

Chaves:

- principal: `numeroProcesso`

Cobertura observada:

- variavel por processo consultado

Limitacoes:

- cobertura empirica ainda baixa no recorte atual;
- nao deve ser tratado como corpus textual principal.

### `precedentes_stj`

Papel:

- camada juridico-semantica de temas e processos vinculados

Chaves:

- `sequencialPrecedente`
- ponte operacional com o pipeline: `numeroRegistro`

Cobertura observada:

- a confirmar empiricamente no dataset atual

Limitacoes:

- nao substitui timeline processual;
- complementa processo com tese, leading case e contexto de origem.

### `movimentacao_stj`

Papel:

- eventos processuais publicados em XML/MTD

Chaves:

- `numeroUnico`
- `numeroRegistro`

Cobertura observada:

- janela publica limitada, criada em `2022-06-07`
- ultima atualizacao observada em `2024-06-18`

Limitacoes:

- nao cobre bem o historico inteiro de processos longos;
- e mais util como janela parcial e como base para lookup de codigos.

### `dicionarios_stj`

Papel:

- tabelas de dominio e definicao de campos

Subfontes principais:

- `dicionario-atadedistribuicao.csv`
- `classes.csv`
- `assuntos.csv`
- `movimentos.csv`
- `dicionario-tramitando.csv`

Uso recomendado:

- normalizacao semantica;
- traducao de codigos;
- definicao de schema canonico;
- preservacao de hierarquia por `cod_pai` e `nivel`.

## Janelas analiticas recomendadas

As janelas analiticas nao precisam ser identicas aos recortes de download.

### `pre_ia`

- processos cuja vida observada termina ate `2022-12-31`

### `transicao`

- processos cuja vida observada cruza `2023`

### `pos_ia`

- processos com atividade observada em `2024+`

## Politica de recortes por notebook

Os notebooks podem usar recortes diferentes, desde que isso fique explicito.

### Downloads de integras/metadados

Objetivo:

- controlar o periodo fisicamente baixado em `raw`

Exemplos:

- `2019-2023` para ampliar rastreio historico
- `2024-2026` para o corpus mais recente ja consolidado

### Notebooks de processamento

Objetivo:

- escolher subconjuntos do `raw` sem apagar o que ja foi baixado

Recomendacao:

- `00` e `00b` controlam o download
- `06` e `07` controlam o recorte de processamento via `ANOS_ANALISE`
- `09` consome a spine processual produzida por `06`
- `10` consolida timeline com base no recorte processado

## Regra operacional importante

Separar sempre:

- `raw` compartilhado e acumulativo
- `processed` por recorte ou por janela

Exemplos:

- `data/processed_2024_2026`
- `data/processed_2019_2023`
- `data/processed_pre_ia`

Assim, os notebooks podem ser rerodados para janelas diferentes sem
sobrescrever artefatos ja validados.
