# Handoff Para Novo Chat

Este documento serve para iniciar um novo chat com o maximo de contexto util
sobre o projeto `datajud_probe`, especialmente no eixo:

- `ATA STJ`
- `integra STJ`
- `DataJud STJ`
- `JSON por processo`
- `dashboard Streamlit`

O objetivo e reduzir perda de contexto e acelerar a retomada do trabalho.

## Resumo executivo

O projeto conseguiu avancar da exploracao de fontes separadas para uma camada
analitica real sobre a **vida util processual no STJ**.

Hoje existem dois eixos principais funcionando:

1. **Eixo processual estruturado**
   - `ATA STJ + DataJud STJ`
   - usado para distribuicao, partes, advogados, classe, assuntos, orgao
     julgador e movimentacoes no STJ

2. **Eixo documental/semantico**
   - `ATA STJ + integra STJ`
   - usado para documentos, metadados documentais e texto limpo

A formulacao metodologica mais segura neste momento e:

> Vida util processual no STJ, enriquecida com data de ajuizamento e
> metadados processuais do DataJud.

## Estado atual do projeto

### O que ja funciona

- notebook `06` monta a espinha dorsal de processos do STJ a partir da ATA
- notebook `07` monta a camada documental/textual das integras
- notebook `09` consulta o `api_publica_stj` do DataJud por `numero_processo`
- notebook `10` monta:
  - `stj_process_events.parquet`
  - `stj_process_timeline.parquet`
- `scripts/build_process_json.py` gera JSONs por processo
- `apps/process_dashboard.py` le os JSONs e o indice CSV no Streamlit

### O que ainda nao fecha totalmente

- o subconjunto com `DataJud` ainda nao se sobrepoe ao subconjunto com
  `documentos textuais`
- ou seja:
  - ha processos com boa timeline de movimentos no STJ
  - ha processos com boa camada documental/textual
  - mas ainda nao ha interseccao forte entre os dois na camada de demo atual

### Cobertura atual

No indice consolidado:

- `2582` processos exportados
- `17` com `tem_datajud = True`
- `73` com `tem_documentos_textuais = True`
- `0` com as duas coisas ao mesmo tempo

## Leitura recomendada para o novo chat

Se o novo chat puder ler poucos arquivos primeiro, a ordem ideal e:

1. [docs/STJ_DATAJUD_STATUS_E_PROXIMOS_PASSOS.md](/Users/felipeignacio/Projects/datajud_probe/docs/STJ_DATAJUD_STATUS_E_PROXIMOS_PASSOS.md)
   - documento mais importante para absorver o raciocinio geral

2. [docs/CAMPOS_E_CASOS_DEMO_STJ.md](/Users/felipeignacio/Projects/datajud_probe/docs/CAMPOS_E_CASOS_DEMO_STJ.md)
   - mostra campos disponiveis, cobertura e casos de demo

3. [docs/NOTEBOOK_GUIDE.md](/Users/felipeignacio/Projects/datajud_probe/docs/NOTEBOOK_GUIDE.md)
   - explica o papel de cada notebook

4. [docs/PROCESS_JSON.md](/Users/felipeignacio/Projects/datajud_probe/docs/PROCESS_JSON.md)
   - explica a camada de JSON por processo

5. [docs/STREAMLIT_DASHBOARD.md](/Users/felipeignacio/Projects/datajud_probe/docs/STREAMLIT_DASHBOARD.md)
   - explica como o dashboard le os artefatos

Depois disso, vale abrir estes arquivos de codigo:

6. [scripts/build_process_json.py](/Users/felipeignacio/Projects/datajud_probe/scripts/build_process_json.py)
7. [apps/process_dashboard.py](/Users/felipeignacio/Projects/datajud_probe/apps/process_dashboard.py)

Se o novo chat precisar entender os notebooks:

8. [notebooks/06_ciclo_vida_processual_stj.ipynb](/Users/felipeignacio/Projects/datajud_probe/notebooks/06_ciclo_vida_processual_stj.ipynb)
9. [notebooks/07_documentos_por_processo_stj.ipynb](/Users/felipeignacio/Projects/datajud_probe/notebooks/07_documentos_por_processo_stj.ipynb)
10. [notebooks/09_datajud_stj_por_cnj.ipynb](/Users/felipeignacio/Projects/datajud_probe/notebooks/09_datajud_stj_por_cnj.ipynb)
11. [notebooks/10_vida_util_stj_enriquecida.ipynb](/Users/felipeignacio/Projects/datajud_probe/notebooks/10_vida_util_stj_enriquecida.ipynb)

## Fontes e papeis de cada uma

### ATA STJ

Fonte de:

- `numero_processo` CNJ
- `numero_registro_stj`
- classe STJ
- distribuicao/registro/redistribuicao
- partes
- advogados e OAB

E a principal tabela-ponte entre:

- `numero_processo` do DataJud
- `numero_registro_stj` das integras

### integra STJ

Fonte de:

- documentos
- metadados documentais
- ministro do documento
- datas de documento
- texto limpo

Usa principalmente:

- `numero_registro_stj`

### DataJud STJ

Fonte de:

- classe processual
- assuntos
- data de ajuizamento
- data de ultima atualizacao
- orgao julgador
- nivel de sigilo
- movimentos processuais

Usa principalmente:

- `numero_processo`

## Chaves importantes

### Chave principal do processo

- `numero_processo`

### Chave auxiliar documental

- `numero_registro_stj`

### Regra de integracao

- `DataJud STJ <-> ATA STJ` por `numero_processo`
- `ATA STJ <-> integra STJ` por `numero_registro_stj`

## Artefatos relevantes em `data/processed`

### Da ATA / espinha dorsal

- `stj_processos_ciclo_vida.parquet`
- `stj_ata_distribuicoes.parquet`
- `stj_ata_partes.parquet`
- `stj_ata_advogados.parquet`

### Da camada documental

- `stj_documentos_por_processo.parquet`
- `stj_textos_por_processo.parquet`
- `stj_integras_documentos_manifest.parquet`

### Do DataJud STJ

- `stj_datajud_lookup_status.parquet`
- `stj_datajud_processos.parquet`
- `stj_datajud_movimentos.parquet`
- `stj_datajud_assuntos.parquet`

### Da timeline consolidada

- `stj_process_events.parquet`
- `stj_process_timeline.parquet`

### Da camada de demo

- `process_json/*.json`
- `demo/processos_demo.jsonl`
- `demo/processos_demo_index.csv`

## Notebooks e o que cada um faz

### Notebook 06

Arquivo:

- [notebooks/06_ciclo_vida_processual_stj.ipynb](/Users/felipeignacio/Projects/datajud_probe/notebooks/06_ciclo_vida_processual_stj.ipynb)

Papel:

- monta `process_spine`
- consolida distribuicoes da ATA
- liga corpus documental ao STJ

Correcao importante feita:

- o merge com o corpus documental passou a considerar tambem
  `numero_registro_stj`
- antes disso, `com_documentos_corpus` estava zerado

### Notebook 07

Arquivo:

- [notebooks/07_documentos_por_processo_stj.ipynb](/Users/felipeignacio/Projects/datajud_probe/notebooks/07_documentos_por_processo_stj.ipynb)

Papel:

- produz camada documental e textual

Correcao importante feita:

- enriquecimento pelo `numero_registro_stj` quando o CNJ nao esta disponivel

### Notebook 09

Arquivo:

- [notebooks/09_datajud_stj_por_cnj.ipynb](/Users/felipeignacio/Projects/datajud_probe/notebooks/09_datajud_stj_por_cnj.ipynb)

Papel:

- consulta DataJud STJ por `numero_processo`
- salva JSON bruto de lookup
- extrai tabelas de processo, movimentos e assuntos

Observacao importante:

- precisa da variavel de ambiente `DATAJUD_API_KEY_PUBLICA`
- quando ela estava ausente, o notebook retornou `401 Unauthorized`

### Notebook 10

Arquivo:

- [notebooks/10_vida_util_stj_enriquecida.ipynb](/Users/felipeignacio/Projects/datajud_probe/notebooks/10_vida_util_stj_enriquecida.ipynb)

Papel:

- monta eventos unificados
- monta timeline agregada por processo

Problema relevante que apareceu:

- erro `Cannot compare tz-naive and tz-aware timestamps`

Causa:

- datas mistas entre:
  - ISO com `Z`
  - formatos compactos tipo `YYYYMMDDHHMMSS`
  - datas sem timezone

Foi resolvido com normalizacao de datas no notebook.

## Script de JSON por processo

Arquivo:

- [scripts/build_process_json.py](/Users/felipeignacio/Projects/datajud_probe/scripts/build_process_json.py)

Papel atual:

- le parquets da camada processada
- gera JSONs por processo
- usa `stj_process_timeline.parquet` quando disponivel
- usa `stj_datajud_processos.parquet` e `stj_datajud_assuntos.parquet`
- gera `processos_demo_index.csv` com campos de filtro

Campos importantes do indice:

- `classe_stj`
- `classe_datajud`
- `segmento_cnj`
- `tribunal_cnj`
- `assunto_cnj_ata`
- `ano_origem_cnj`
- `relator_ata_principal`
- `n_partes`
- `n_advogados`
- `n_documentos`
- `n_eventos_timeline`
- `n_eventos_ata_stj`
- `n_eventos_datajud_stj`
- `n_eventos_integra_stj`
- `tem_datajud`
- `tem_documentos_textuais`
- `fontes_timeline`

## Dashboard Streamlit

Arquivo:

- [apps/process_dashboard.py](/Users/felipeignacio/Projects/datajud_probe/apps/process_dashboard.py)

Papel atual:

- le `processos_demo_index.csv`
- le `process_json/*.json`
- mostra:
  - resumo do processo
  - timeline
  - partes
  - documentos
  - bloco STJ
  - bloco DataJud
  - JSON bruto

Filtros atuais:

- busca por CNJ ou registro STJ
- classe STJ
- classe DataJud
- segmento CNJ
- tribunal CNJ
- relator ATA
- ano de origem
- somente com DataJud
- somente com documentos textuais

Observacao importante:

- o dashboard precisou resolver caminhos absolutos de Colab
- por isso ha uma funcao `resolve_json_path(...)`

## Casos de demonstracao recomendados

Os tres casos recomendados hoje estao descritos em:

- [docs/CAMPOS_E_CASOS_DEMO_STJ.md](/Users/felipeignacio/Projects/datajud_probe/docs/CAMPOS_E_CASOS_DEMO_STJ.md)

Em resumo:

### Caso 1: melhor para mostrar vida util com DataJud

- `202301327446`
- `00000094820228272722`
- `REsp`
- `120` eventos

### Caso 2: arco temporal longo e origem federal

- `201700539640`
- `00000270520134047105`
- `AREsp`
- `67` eventos

### Caso 3: melhor para camada documental/textual

- `202302264705`
- `02264702720233000000`
- `HC`
- `2` documentos textuais

## Comandos uteis

### Regenerar JSONs localmente com tudo

```bash
./.venv/bin/python scripts/build_process_json.py \
  --processed-dir "$HOME/Library/CloudStorage/GoogleDrive-fmaignacio@gmail.com/Meu Drive/Mestrado/2026/llms/data/processed"
```

### Regenerar JSONs filtrando para processos com texto

```bash
./.venv/bin/python scripts/build_process_json.py \
  --processed-dir "$HOME/Library/CloudStorage/GoogleDrive-fmaignacio@gmail.com/Meu Drive/Mestrado/2026/llms/data/processed" \
  --only-linked \
  --only-with-text \
  --sort-by-text
```

### Rodar o dashboard localmente

```bash
export DATAJUD_PROCESSED_DIR="$HOME/Library/CloudStorage/GoogleDrive-fmaignacio@gmail.com/Meu Drive/Mestrado/2026/llms/data/processed"
streamlit run apps/process_dashboard.py
```

### Sincronizar o script para a pasta operacional do Drive

```bash
cp scripts/build_process_json.py \
  "$HOME/Library/CloudStorage/GoogleDrive-fmaignacio@gmail.com/Meu Drive/Mestrado/2026/llms/scripts/build_process_json.py"
```

## Ambiente e caminhos relevantes

### Repositorio local

- `/Users/felipeignacio/Projects/datajud_probe`

### Pasta operacional no Google Drive Desktop

- `/Users/felipeignacio/Library/CloudStorage/GoogleDrive-fmaignacio@gmail.com/Meu Drive/Mestrado/2026/llms`

### Equivalente no Colab

- `/content/drive/MyDrive/Mestrado/2026/llms`

## Problemas conhecidos

### 1. Subconjuntos ainda separados

Hoje, os processos com `DataJud` e os processos com `documentos textuais`
ainda nao formam um subconjunto comum na camada de demo.

### 2. Encoding em dados do DataJud

Alguns nomes de orgao julgador/ministro apareceram com mojibake, por exemplo:

- `FALCÃ\x83O`
- `MAGALHÃ\x83ES`

Isso ainda pode precisar de limpeza posterior.

### 3. Datas mistas

Os dados do DataJud podem vir em formatos como:

- `2023-04-26T00:00:00.000Z`
- `20230623000000`

Qualquer nova etapa de integracao temporal deve tratar isso explicitamente.

## Proximos passos mais promissores

Se um novo chat for retomar o trabalho, as melhores linhas de continuidade sao:

1. aumentar a interseccao entre `DataJud` e `documentos textuais`
2. melhorar a selecao de casos de demo
3. enriquecer o dashboard com filtros por cobertura e fonte
4. normalizar melhor encoding e datas
5. refinar a apresentacao metodologica para orientador e banca

## Prompt curto sugerido para novo chat

Se quiser iniciar um novo chat rapidamente, este texto deve funcionar bem:

> Leia primeiro `docs/STJ_DATAJUD_STATUS_E_PROXIMOS_PASSOS.md`,
> `docs/CAMPOS_E_CASOS_DEMO_STJ.md`, `docs/NOTEBOOK_GUIDE.md`,
> `docs/PROCESS_JSON.md` e `docs/STREAMLIT_DASHBOARD.md`.
> Depois inspecione `scripts/build_process_json.py` e
> `apps/process_dashboard.py`.
> O projeto ja constroi vida util processual no STJ em dois eixos:
> `ATA + DataJud STJ` para movimentos e `ATA + integra STJ` para camada
> documental/textual. Preciso continuar a partir desse estado, sem perder as
> decisoes tecnicas ja tomadas.
