# Guia Detalhado dos Notebooks

Este guia complementa o `README.md` com uma leitura operacional dos notebooks do projeto. Ele explica o objetivo de cada notebook, os principais parametros, entradas, saidas e cuidados metodologicos.

## Visao Geral do Fluxo

O projeto trabalha com tres camadas diferentes:

1. **Aquisicao de dados**: baixar metadados JSON e ZIPs de textos do STJ Dados Abertos.
2. **Exploracao documental**: entender escala, datas, tipos documentais, teor, recursos, relatores e assuntos no corpus STJ.
3. **Camada processual/textual**: ligar documento, registro STJ, processo/CNJ e texto integral, com cuidado para nao confundir documentos com vida processual completa.

A unidade observada mais confiavel neste momento e o documento (`SeqDocumento`). A unidade desejada para a pesquisa longitudinal e o processo, preferencialmente por CNJ, mas a ligacao ainda precisa ser consolidada com `numeroRegistro`, Atas de Distribuicao, Movimentacao Processual, DataJud e, no futuro, dados de outras instancias.

## Sequencia Recomendada

Para apresentacao exploratoria:

```text
01_exploracao_stj_metadados.ipynb
08_apresentacao_eda_stj.ipynb
```

Para preparar dados brutos:

```text
00_download_stj_metadados.ipynb
00b_download_stj_textos.ipynb
```

Para texto integral e processo:

```text
02_validacao_integras_txt.ipynb
06_ciclo_vida_processual_stj.ipynb
07_documentos_por_processo_stj.ipynb
```

Para assuntos:

```text
04_parse_tabela_assuntos.ipynb
```

## 00_download_stj_metadados.ipynb

### Objetivo

Baixar os arquivos `metadados<aaaammdd>.json` da base **Integras de Decisoes Terminativas e Acordaos do Diario da Justica** no portal de Dados Abertos do STJ.

### O que mudou

O notebook agora aceita tanto URLs terminadas em:

```text
metadados20240112.json
```

quanto URLs expostas sem extensao final:

```text
metadados20240112
```

Localmente, o arquivo e salvo de forma normalizada como `metadados<aaaammdd>.json`.

### Parametros principais

- `DATA_INICIO`: inicio do recorte temporal.
- `DATA_FIM`: fim do recorte temporal.
- `MAX_DOWNLOADS`: limite para teste. Use `None` para baixar todo o recorte.
- `overwrite` dentro de `download_metadata_file`: se `False`, nao baixa arquivo que ja existe.

### Entradas

- Pagina oficial do dataset STJ.

### Saidas

- `data/raw/stj_integras_metadata/<ano>/metadados<aaaammdd>.json`
- `data/reports/summaries/stj_metadata_download_report.csv`
- `data/reports/summaries/stj_metadata_download_retry_report.csv` quando houver retry.

### Quando rodar

Rode quando quiser ampliar ou atualizar o recorte de metadados.

## 00b_download_stj_textos.ipynb

### Objetivo

Baixar os ZIPs com textos integrais (`textos<aaaammdd>.zip`) do mesmo dataset.

### O que mudou

O portal do STJ usa formatos variados. O notebook aceita:

```text
20240112.zip
20240205
textos20260417.zip
```

Localmente, salva tudo como:

```text
textos<aaaammdd>.zip
```

### Parametros principais

- `ANOS_ANALISE`: anos do corpus. Atualmente `[2024, 2025, 2026]`.
- `DATA_INICIO`: inicio do recorte.
- `DATA_FIM`: fim do recorte.
- `MAX_DOWNLOADS`: limite para teste.
- `RENOMEAR_COM_PREFIXO_TEXTOS`: se `True`, padroniza nomes locais como `textos<aaaammdd>.zip`.
- `OVERWRITE`: controla se arquivos existentes sao baixados novamente.

### Entradas

- Pagina oficial do dataset STJ.

### Saidas

- `data/raw/stj_integras/<ano>/textos<aaaammdd>.zip`
- `data/reports/summaries/stj_textos_download_report.csv`

### Quando rodar

Nao e necessario rodar se os ZIPs ja estiverem baixados em `raw/stj_integras/2024`, `2025` e `2026`.

## 01_exploracao_stj_metadados.ipynb

### Objetivo

Fazer a EDA principal dos metadados STJ sem abrir ZIPs de texto. Este notebook gera os CSVs que alimentam a apresentacao visual.

### O que mudou

- O parser de datas foi ajustado para evitar warnings e tratar formatos conhecidos de forma explicita.
- O campo `ministro` agora combina `ministro`, `NM_MINISTRO` e `relator`, em vez de parar na primeira coluna encontrada. Isso corrigiu o falso diagnostico de que mais de 99% dos ministros estavam vazios.
- O lookup de assuntos foi agregado por codigo. Ainda assim, se a unica fonte local for `78_Tabela_Assuntos_Justica_Federal_1_Grau.xls`, os nomes devem ser tratados como rotulos auxiliares, nao como cobertura multi-instancia.

### Parametros principais

- `ANOS_ANALISE`: anos dos metadados a carregar. Para o corpus atual, use `[2024, 2025, 2026]`. Use `None` para todos os anos disponiveis.

### Entradas

- `data/raw/stj_integras_metadata/<ano>/metadados*.json`
- Opcional: `data/reference/assuntos/processed/assuntos_lookup.parquet` ou `.csv`

### Saidas principais

Em `data/reports/summaries/`:

- `metadata_eda_summary.md`
- `stj_docs_by_publication_year.csv`
- `stj_docs_by_publication_month.csv`
- `stj_processes_by_publication_year.csv`
- `stj_docs_by_type.csv`
- `stj_docs_by_minister.csv`
- `stj_docs_by_teor.csv`
- `stj_docs_by_recurso.csv`
- `stj_docs_by_assunto_*`

### Cuidados

Este notebook descreve documentos e metadados publicados pelo STJ. Ele nao reconstrói a vida processual completa.

## 02_validacao_integras_txt.ipynb

### Objetivo

Validar a ligacao entre um lote de metadados e um ZIP de textos usando `SeqDocumento`.

### Papel atual

Este notebook e um smoke test. Ele nao foi desenhado para processar todos os lotes de 2024-2026.

### Entradas

- Um JSON `metadados*.json` em `data/raw/stj_integras/`
- Um ZIP correspondente em `data/raw/stj_integras/`

### Saidas

- `data/reports/summaries/stj_integras_key_validation.json`
- `data/processed/stj_integras_sample.parquet`
- `data/processed/stj_integras_sample.csv`

### Quando rodar

Rode para validar rapidamente um pacote antes de processar muitos ZIPs.

## 03_analise_textual_inicial.ipynb

### Objetivo

Analisar uma amostra textual previamente gerada pelo notebook 02.

### Entradas

- `data/processed/stj_integras_sample.parquet` ou `.csv`

### Saidas

- Estatisticas simples de tamanho de texto, campos disponiveis e distribuicoes basicas.

### Observacao

Este notebook ainda nao e a analise textual final. Ele depende de uma amostra pequena.

## 04_parse_tabela_assuntos.ipynb

### Objetivo

Converter tabela bruta de assuntos em lookup estruturado.

### Entradas

- Atualmente, pode usar `notebooks/78_Tabela_Assuntos_Justica_Federal_1_Grau.xls` ou arquivos equivalentes.

### Saidas

- `data/reference/assuntos/processed/assuntos_lookup.csv`
- `data/reference/assuntos/processed/assuntos_lookup.parquet`

### Cuidados

Se a fonte for apenas a tabela da Justica Federal de 1º Grau, os nomes de assunto sao rotulos auxiliares dos codigos. Nao apresente isso como cobertura de todas as instancias.

## 05_eda_avancada_stj.ipynb

### Objetivo

Fazer uma EDA mais visual e detalhada com Matplotlib, incluindo volume temporal, composicao documental, relatores/ministros, processos, assuntos e qualidade dos dados.

### O que mudou

- Os graficos foram convertidos de Plotly para Matplotlib para evitar problemas de renderizacao no VS Code/Colab.
- O lookup de assuntos foi ajustado para preservar informacoes de instancias quando existirem, mas atualmente a fonte local ainda parece limitada.

### Parametros principais

- `ANOS_ANALISE`: recorte temporal. Pode usar `[2026]` para exploracao rapida ou `[2024, 2025, 2026]` para o corpus atual.

### Saidas

- Figuras em `data/reports/figures/`
- Tabelas como `data/reports/summaries/stj_top_assuntos_labeled.csv`

### Quando rodar

Rode quando quiser uma EDA mais completa do que a apresentacao do notebook 08. Pode ser mais pesado que o 08.

## 06_ciclo_vida_processual_stj.ipynb

### Objetivo

Construir uma espinha dorsal processual a partir de varias fontes:

- Atas de Distribuicao;
- DataJud/API;
- metadados das integras;
- primeira aparicao no corpus.

### O que mudou

- Adicionado cache para `stj_integras_documentos_manifest.parquet`.
- Adicionado `processo_agregacao`, que usa CNJ quando existe, senao `numeroRegistro`, senao numero original.
- Adicionado controle para evitar leituras longas por acidente.

### Parametros principais

- `ANOS_ANALISE`: anos dos metadados de integras.
- `MAX_ARQUIVOS_METADATA`: limite para teste. Quando definido, ignora o cache.
- `FORCAR_REPROCESSAR_METADATA`: se `True`, reprocessa metadados mesmo com cache.
- `METADATA_CACHE_PATH`: parquet usado como cache.

### Saidas

- `data/processed/stj_processos_ciclo_vida.parquet`
- `data/processed/stj_movimentos_datajud.parquet`
- `data/processed/stj_ata_distribuicoes.parquet`
- `data/processed/stj_integras_documentos_manifest.parquet`
- `data/processed/stj_integras_corpus_por_chave.parquet`
- `data/reports/summaries/stj_ciclo_vida_processual_summary.md`

### Estado metodologico

Este notebook ainda e experimental. Se `process_spine` aparecer com zero processos, isso nao invalida a EDA documental; indica que a ligacao CNJ/registro/processo ainda precisa ser melhor resolvida.

## 07_documentos_por_processo_stj.ipynb

### Objetivo

Construir a tabela documento-texto a partir de varios lotes de JSON + ZIP, preservando uma linha por documento.

### O que mudou

- O notebook agora processa multiplos lotes.
- Ele cruza `metadados<aaaammdd>.json` com `textos<aaaammdd>.zip` ou `<aaaammdd>.zip`.
- Ele usa `processo_agregacao` para agrupar documentos quando CNJ nao esta disponivel.

### Parametros principais

- `ANOS_ANALISE`: anos dos lotes.
- `MAX_LOTES`: limite de lotes para teste.
- `MAX_DOCUMENTOS`: limite de documentos para teste.
- `RANDOM_SAMPLE`: se `True`, amostra documentos aleatoriamente.
- `GERAR_TEXTO_POR_PROCESSO`: se `True`, concatena textos por chave de processo; pode ficar pesado.

### Entradas

- `data/raw/stj_integras_metadata/<ano>/metadados*.json`
- `data/raw/stj_integras/<ano>/textos*.zip`
- Opcional: `data/processed/stj_processos_ciclo_vida.parquet`

### Saidas

- `data/processed/stj_documentos_manifest.parquet`
- `data/processed/stj_documentos_por_processo.parquet`
- `data/processed/stj_textos_por_processo.parquet` quando habilitado
- `data/reports/summaries/stj_documentos_texto_validation.csv`
- `data/reports/summaries/stj_documentos_texto_summary.md`

### Recomendacao de teste

Antes de rodar completo:

```python
ANOS_ANALISE = [2024, 2025, 2026]
MAX_LOTES = 2
MAX_DOCUMENTOS = 500
GERAR_TEXTO_POR_PROCESSO = False
```

Depois aumente gradualmente.

## 08_apresentacao_eda_stj.ipynb

### Objetivo

Gerar uma apresentacao visual e curta da EDA documental para conversa com professor/orientador.

### Entradas

- CSVs e Markdown gerados pelo notebook 01.
- Opcional: resumo do notebook 06 para a secao de limites metodologicos.

### Saidas

- Figuras em `data/reports/figures/apresentacao_eda/`

### O que apresenta bem

- Escala do corpus;
- volume por ano e mes;
- tipos de documento;
- teor;
- recursos;
- relatoria nos metadados;
- concentracao de codigos de assunto;
- limites atuais para vida processual.

### O que nao deve prometer

- Vida processual completa;
- cobertura multi-instancia;
- analise definitiva de ministros ou produtividade;
- interpretacao substantiva de textos antes de processar os ZIPs.

## Sobre Dados de Outras Instancias

Capturar dados de outras instancias e uma boa proxima etapa, mas nao precisa entrar na EDA atual como resultado. A estrategia recomendada e:

1. consolidar a base STJ por documento e registro;
2. enriquecer acordaos com os datasets de Espelhos de Acordaos;
3. usar Atas de Distribuicao e Movimentacao Processual para a vida no STJ;
4. usar DataJud e/ou dados de tribunais de origem para reconstruir a trajetoria anterior.

## Sobre Merge Para `main`

Antes de fazer merge, revise:

- notebooks novos: `00b`, `06`, `07`, `08`;
- README e este guia;
- se outputs grandes ficaram salvos nos notebooks;
- se arquivos de dados brutos nao foram adicionados por engano.

O merge faz sentido quando o objetivo for consolidar a nova arquitetura do projeto. Se a prioridade for manter `main` apenas com notebooks estaveis, considere fazer um commit/PR primeiro e marcar `06` e `07` como experimentais.
