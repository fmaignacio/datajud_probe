# datajud_probe

Pequeno probe em Python para consultar a API publica do DataJud e gerar arquivos JSON com amostras brutas e resumos de cobertura de campos.

## Requisitos

- Python 3.10+
- Chave de API do DataJud

## Configuracao

Crie um ambiente virtual e instale as dependencias:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto:

```bash
cp .env.example .env
```

Depois edite `.env` e informe sua chave:

```env
DATAJUD_API_KEY=sua_chave_aqui
```

## Uso

Execute o probe:

```bash
python src/run_probe.py
```

Os resultados gerados ficam em:

- `data/raw/`
- `data/reports/`

Essas pastas nao sao versionadas porque contem saidas geradas pela execucao.
