# Dashboard Streamlit

App minimalista:

```text
apps/process_dashboard.py
```

Ele lê:

```text
data/processed/demo/processos_demo_index.csv
data/processed/process_json/*.json
```

Na versao atual, o dashboard:

- usa a `timeline` consolidada do notebook 10;
- mostra abas separadas para `STJ` e `DataJud`;
- oferece filtros por classe, segmento, tribunal, relator e flags de cobertura;
- expõe a lista de colunas disponiveis no indice pela barra lateral.

## Gerar JSONs de demo

No Colab:

```bash
python scripts/build_process_json.py \
  --data-root "/content/drive/MyDrive/Mestrado/2026/llms/data" \
  --only-linked
```

Para gerar o conjunto completo:

```bash
python scripts/build_process_json.py \
  --data-root "/content/drive/MyDrive/Mestrado/2026/llms/data"
```

## Rodar localmente

Se `data/processed` estiver local:

```bash
streamlit run apps/process_dashboard.py
```

Se os dados estiverem no Google Drive for Desktop:

```bash
export DATAJUD_PROCESSED_DIR="$HOME/Library/CloudStorage/GoogleDrive-fmaignacio@gmail.com/Meu Drive/Mestrado/2026/llms/data/processed"
streamlit run apps/process_dashboard.py
```

Tambem e possivel informar o caminho pela barra lateral do dashboard.

## Rodar no Colab

O Streamlit precisa de tunel/public URL no Colab. Para uso simples, prefira rodar
localmente com Google Drive for Desktop apontando para `llms/data/processed`.
