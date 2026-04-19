# datajud_probe

Repositorio exploratorio para apoiar um projeto de mestrado em Ciencia de Dados sobre LLMs, governanca epistemica e conhecimento institucional no setor publico brasileiro.

O projeto nasceu como um probe da API publica do DataJud, mas os testes iniciais indicaram que a fonte mais promissora para analise semantica e o STJ Dados Abertos, especialmente a base de integras de decisoes terminativas e acordaos do Diario da Justica.

## Objetivo atual

A etapa atual nao busca treinar modelos, criar uma aplicacao ou comparar LLMs com decisoes humanas.

O foco imediato e fazer uma analise exploratoria minima e reprodutivel da base do STJ:

- carregar metadados em JSON;
- abrir o ZIP com textos integrais em TXT;
- validar a ligacao entre `SeqDocumento` e os arquivos de texto;
- montar amostras com metadados e texto integral;
- limpar marcacoes simples, como `<br>`;
- produzir estatisticas descritivas;
- gerar um relatorio de cobertura e qualidade da base.
- mapear codigos de assuntos processuais para rotulos textuais quando a tabela CNJ/STJ estiver disponivel.

Antes de qualquer analise com LLM, o objetivo e entender se a base e adequada como corpus semantico.

## Contexto da pesquisa

A pergunta teorica provisoria e:

> Como o uso de LLMs em contextos institucionais reconfigura a producao, a validacao e o uso do conhecimento institucional no setor publico brasileiro?

A hipotese teorica provisoria e que LLMs podem funcionar como uma forma implicita de delegacao cognitiva, alterando praticas de validacao, confianca e autoridade epistemica.

A pergunta empirica provisoria e:

> Como saidas geradas por LLMs diferem de decisoes humanas institucionais em casos juridicos estruturados com dados publicos?

Essa comparacao, no entanto, so deve ser considerada depois da validacao exploratoria da base textual.

## Fontes avaliadas

### DataJud

Util para metadados processuais, classes, assuntos, orgaos julgadores, graus, movimentacoes e datas. Nos testes iniciais, nao se confirmou como corpus textual principal.

### TJSP

Pode ser util para amostras qualitativas pequenas, mas parece menos adequado para coleta escalavel.

### STJ Dados Abertos

Fonte principal atual. A base de integras de decisoes terminativas e acordaos oferece:

- ZIP com textos integrais em TXT;
- JSON com metadados;
- CSV com dicionario de dados;
- chave `SeqDocumento` para vincular metadados e textos.

## Estrutura atual

```text
.
├── CODEX_PROMPT.md
├── README.md
├── requirements.txt
└── src/
    ├── assuntos.py
    ├── client.py
    ├── config.py
    ├── queries.py
    ├── run_probe.py
    └── data/
        └── master/
            └── PROJETO_MESTRADO.md
```

## Configuracao do probe DataJud

O probe original ainda usa a API publica do DataJud.

Crie um ambiente virtual e instale as dependencias:

```bash
python3 -m venv .venv
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

## Uso do probe atual

```bash
python3 src/run_probe.py
```

Os resultados gerados ficam em:

- `data/raw/`
- `data/reports/`

Essas pastas nao sao versionadas porque contem saidas geradas pela execucao.

## Proximos passos

1. Instale dependências (incluindo `plotly`, `nbformat`, `kaleido`):
   ```bash
   pip install -r requirements.txt
   ```

2. **Metadados:** Rode `notebooks/00_download_stj_metadados.ipynb` para baixar apenas os JSONs de metadados do recorte desejado.

3. **Lookup de assuntos (local):** Rode `notebooks/04_parse_tabela_assuntos.ipynb` para gerar `data/reference/assuntos/processed/assuntos_lookup.parquet`.

4. **EDA metadados (sem textos grandes):** Rode `notebooks/01_exploracao_stj_metadados.ipynb` para explorar os metadados; se o lookup existir, os assuntos são enriquecidos com rótulos textuais.

5. **EDA avancada (Plotly + Insights):** Rode `notebooks/05_eda_avancada_stj.ipynb` para análise completa com gráficos interativos (volume temporal, composição documental, ministros, processos CNJ, assuntos, qualidade de dados).

6. **Validação de textos:** Coloque um pacote bruto em `data/raw/stj_integras/` e rode `notebooks/02_validacao_integras_txt.ipynb` para validar a ligação entre `SeqDocumento` e os TXT do ZIP.

7. **Análise textual inicial:** Rode `notebooks/03_analise_textual_inicial.ipynb` apenas depois de gerar uma amostra textual processada.

## Estrutura

```text
.
├── CODEX_PROMPT.md                    # Instruções para Codex
├── README.md
├── requirements.txt
├── .vscode/
│   ├── settings.json                  # Configuração VS Code
│   └── extensions.json                # Extensões recomendadas
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── assuntos.py                    # Parser de tabela de assuntos (HTML/XLS)
│   ├── client.py                      # Cliente DataJud
│   ├── config.py                      # Configuração (API_KEY lazy)
│   ├── queries.py                     # Queries DataJud
│   ├── run_probe.py                   # Probe original DataJud
│   └── data/master/
│       └── PROJETO_MESTRADO.md        # Documento de ideia do projeto
├── data/
│   ├── raw/
│   │   └── stj_integras/              # ZIP + JSON brutos (em .gitignore)
│   ├── reports/
│   │   ├── summaries/                 # CSVs e Markdown de relatórios
│   │   └── figures/                   # Gráficos Plotly (HTML + PNG)
│   └── reference/
│       └── assuntos/processed/        # Lookup parseado (CSV + Parquet)
└── notebooks/
    ├── 00_download_stj_metadados.ipynb     # Download iterativo de JSONs
    ├── 01_exploracao_stj_metadados.ipynb   # EDA básica (sem textos)
    ├── 02_validacao_integras_txt.ipynb     # Validação SeqDocumento ↔ TXT
    ├── 03_analise_textual_inicial.ipynb    # Análise textual inicial
    ├── 04_parse_tabela_assuntos.ipynb      # Parser de assuntos
    ├── 05_eda_avancada_stj.ipynb           # EDA completa com Plotly
    └── 78_Tabela_Assuntos_Justica_Federal_1_Grau.xls
```

