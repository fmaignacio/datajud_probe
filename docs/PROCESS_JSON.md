# JSON por processo

Esta camada gera artefatos orientados a demonstracao e dashboard a partir dos
parquets produzidos pelos notebooks 06, 07, 09 e 10.

## Entradas esperadas

No diretorio `data/processed` ou equivalente no Drive:

- `stj_processos_ciclo_vida.parquet`
- `stj_ata_partes.parquet`
- `stj_ata_advogados.parquet`
- `stj_documentos_por_processo.parquet`
- `stj_process_timeline.parquet`
- `stj_process_events.parquet`
- `stj_datajud_processos.parquet`
- `stj_datajud_assuntos.parquet`

Se `stj_documentos_por_processo.parquet` ainda nao existir, o script usa
`stj_integras_documentos_manifest.parquet` como fallback, mas nesse caso os
JSONs nao terao texto integral.

## Rodar no Colab

Depois de montar o Drive e rodar os notebooks 06 e 07:

```bash
python scripts/build_process_json.py \
  --data-root "/content/drive/MyDrive/Mestrado/2026/llms/data" \
  --only-linked \
  --only-with-text \
  --sort-by-text \
  --limit 20
```

Saidas:

```text
/content/drive/MyDrive/Mestrado/2026/llms/data/processed/process_json/
/content/drive/MyDrive/Mestrado/2026/llms/data/processed/demo/processos_demo.jsonl
/content/drive/MyDrive/Mestrado/2026/llms/data/processed/demo/processos_demo_index.csv
```

## Rodar localmente

Se os parquets estiverem em `data/processed`:

```bash
python3 scripts/build_process_json.py --only-linked --limit 20
```

Para uma demo melhor, priorizando processos que tenham texto disponivel:

```bash
python3 scripts/build_process_json.py \
  --only-linked \
  --only-with-text \
  --sort-by-text \
  --limit 20
```

## Exportar um processo especifico

Por registro STJ:

```bash
python3 scripts/build_process_json.py \
  --data-root "/content/drive/MyDrive/Mestrado/2026/llms/data" \
  --numero-registro-stj 202203601967
```

Por numero CNJ:

```bash
python3 scripts/build_process_json.py \
  --data-root "/content/drive/MyDrive/Mestrado/2026/llms/data" \
  --numero-processo 50066035720214047004
```

## Texto completo ou preview

Por padrao, cada documento inclui ate 4.000 caracteres de `texto_limpo`.
Para incluir o texto completo:

```bash
python3 scripts/build_process_json.py \
  --data-root "/content/drive/MyDrive/Mestrado/2026/llms/data" \
  --only-linked \
  --include-full-text
```

Use texto completo com cuidado: os JSONs podem ficar grandes.

## Uso em dashboard

Para Streamlit, a recomendacao e:

- usar os parquets ou BigQuery para filtros e listagens;
- carregar o JSON de um processo apenas quando o usuario abrir o detalhe;
- usar `processos_demo_index.csv` para uma demo pequena e rapida.

O campo `datajud` ja existe no schema como espaco reservado. Quando os
movimentos DataJud forem carregados, a mesma estrutura pode ser enriquecida sem
mudar o formato geral do JSON.

Na versao atual, a `timeline` ja passa a reaproveitar a timeline consolidada do
notebook 10 quando esse parquet estiver presente.

## Campos do indice

O arquivo `processos_demo_index.csv` agora funciona como catalogo de filtros para
o dashboard. Ele inclui:

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
