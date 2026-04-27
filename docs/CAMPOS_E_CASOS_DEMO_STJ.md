# Campos E Casos Demo STJ

## Estado atual

Os JSONs por processo foram regenerados usando a timeline consolidada de:

- `stj_process_timeline.parquet`
- `stj_process_events.parquet`

O indice da demo fica em:

- `data/processed/demo/processos_demo_index.csv`

Na rodada atual, o indice consolidado tem:

- `2582` processos exportados
- `17` processos com `tem_datajud = True`
- `73` processos com `tem_documentos_textuais = True`
- `0` processos com interseccao entre `DataJud` e `documentos textuais`

Essa ultima linha e importante: hoje existem dois subconjuntos fortes, mas ainda sem sobreposicao no recorte exportado.

## Campos disponiveis para filtro no dashboard

O `processos_demo_index.csv` agora expõe os campos abaixo:

- `numero_processo`
- `numero_registro_stj`
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
- `n_documentos_texto_disponiveis`
- `n_eventos_timeline`
- `timeline_start`
- `timeline_end`
- `n_eventos_ata_stj`
- `n_eventos_datajud_stj`
- `n_eventos_integra_stj`
- `tem_datajud`
- `tem_documentos_textuais`
- `fontes_timeline`

## Campos disponiveis dentro do JSON de processo

Cada JSON tem a estrutura:

- `processo`
- `stj`
- `partes`
- `documentos`
- `timeline`
- `datajud`
- `metadados_pipeline`

### `processo`

- `numero_processo`
- `numero_registro_stj`
- `chave_agregacao`
- `classe_stj`
- `classe_datajud`
- `assunto_cnj_ata`
- `ano_origem_cnj`
- `segmento_cnj`
- `tribunal_cnj`
- `origem_cnj`
- `relator_ata_principal`
- `primeira_aparicao_corpus`
- `ja_existia_antes_da_primeira_aparicao_corpus`
- `ano_primeira_aparicao_corpus`
- `anos_entre_origem_e_corpus`

### `stj`

- `data_primeira_distribuicao`
- `data_ultima_distribuicao`
- `n_eventos_distribuicao`
- `formas_distribuicao`
- `relatores`
- `destinos`

### `partes`

Para cada parte:

- `parte_idx`
- `tipo`
- `nome`
- `documento`
- `advogados[]`

Para cada advogado:

- `nome`
- `oab`

### `documentos`

Para cada documento:

- `seq_documento`
- `data_documento`
- `tipo_documento`
- `ministro`
- `assuntos_raw`
- `lote`
- `metadata_file`
- `txt_path`
- `n_words_limpo`
- `texto_vazio`
- `texto_limpo`
- `texto_truncado`

### `timeline`

Na versao atual, a timeline vem preferencialmente do `stj_process_timeline.parquet`.
Cada evento consolidado pode ter:

- `event_datetime`
- `event_source`
- `event_type`
- `event_label`
- `event_detail`
- `seq_documento` (quando aplicavel)

### `datajud`

- `status`
- `tribunal`
- `grau`
- `classe.codigo`
- `classe.nome`
- `orgao_julgador.codigo`
- `orgao_julgador.nome`
- `nivel_sigilo`
- `data_ajuizamento`
- `data_ultima_atualizacao`
- `assuntos[]`

### `metadados_pipeline`

- `fontes`
- `versao_schema`
- `n_documentos_corpus`
- `n_documentos_texto_disponiveis`
- `n_advogados`
- `n_eventos_timeline`
- `timeline_start`
- `timeline_end`
- `timeline_sources`
- `n_eventos_ata_stj`
- `n_eventos_datajud_stj`
- `n_eventos_integra_stj`
- `ja_existia_antes_da_primeira_aparicao_corpus`

## Tres casos exemplares para apresentacao

### 1. Caso mais forte de vida util com DataJud

- `numero_registro_stj`: `202301327446`
- `numero_processo`: `00000094820228272722`
- `classe_stj`: `REsp`
- `classe_datajud`: `Recurso Especial`
- `segmento_cnj`: `Justica Estadual`
- `relator_ata_principal`: `FRANCISCO FALCAO`
- `n_eventos_timeline`: `120`
- `n_eventos_datajud_stj`: `119`
- `n_partes`: `3`
- `n_advogados`: `8`
- `fontes_timeline`: `ata_stj | datajud_stj`

Por que mostrar:

- e o caso mais forte para demonstrar movimentacao no STJ;
- mostra bem a integracao `ATA + DataJud STJ`;
- tem inicio e fim claros da linha do tempo.

Arquivo:

- `data/processed/process_json/202301327446.json`

### 2. Caso com arco temporal longo e origem federal

- `numero_registro_stj`: `201700539640`
- `numero_processo`: `00000270520134047105`
- `classe_stj`: `AREsp`
- `classe_datajud`: `Agravo em Recurso Especial`
- `segmento_cnj`: `Justica Federal`
- `relator_ata_principal`: `VICE-PRESIDENTE DO STJ`
- `n_eventos_timeline`: `67`
- `n_eventos_datajud_stj`: `66`
- `n_partes`: `6`
- `n_advogados`: `2`
- `timeline_start`: `2017-03-15T19:24:06`
- `timeline_end`: `2023-10-27T18:23:06`

Por que mostrar:

- cobre um intervalo temporal longo;
- traz diversidade de origem (`Justica Federal`);
- e um bom contraste com o primeiro caso.

Arquivo:

- `data/processed/process_json/201700539640.json`

### 3. Caso mais forte de camada documental/semantica

- `numero_registro_stj`: `202302264705`
- `numero_processo`: `02264702720233000000`
- `classe_stj`: `HC`
- `segmento_cnj`: `STJ`
- `relator_ata_principal`: `ROGERIO SCHIETTI CRUZ`
- `n_partes`: `6`
- `n_advogados`: `4`
- `n_documentos`: `2`
- `n_documentos_texto_disponiveis`: `4`
- `n_eventos_timeline`: `3`
- `fontes_timeline`: `ata_stj | integra_stj`

Por que mostrar:

- e o melhor caso atual para demonstrar partes, advogados e decisoes textuais;
- funciona bem como prova da camada semantica do STJ;
- ajuda a explicar o que ja temos de texto, mesmo sem DataJud neste recorte.

Arquivo:

- `data/processed/process_json/202302264705.json`

## Leitura metodologica recomendada

Para apresentacao, a formulacao mais segura e:

> Conseguimos reconstruir a vida util processual no STJ em dois eixos complementares: um eixo estruturado de movimentacoes processuais com `ATA + DataJud STJ`, e um eixo documental/semantico com `ATA + integra STJ`.

Hoje, esses eixos ainda nao se sobrepoem no mesmo subconjunto de demonstracao. Esse passa a ser um alvo claro das proximas iteracoes.
