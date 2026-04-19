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

1. Baixar uma amostra da base STJ de integras.
2. Rodar `notebooks/00_download_stj_metadados.ipynb` para baixar apenas os JSONs de metadados do recorte desejado.
3. Rodar `notebooks/04_parse_tabela_assuntos.ipynb` para gerar `data/reference/assuntos/processed/assuntos_lookup.parquet`.
4. Rodar `notebooks/01_exploracao_stj_metadados.ipynb` para explorar os metadados sem carregar textos grandes; se o lookup existir, os assuntos sao enriquecidos com rotulos textuais.
5. Colocar um pacote bruto em `data/raw/stj_integras/`, quando for necessario validar TXT.
6. Rodar `notebooks/02_validacao_integras_txt.ipynb` para validar a ligacao entre `SeqDocumento` e os TXT do ZIP.
7. Rodar `notebooks/03_analise_textual_inicial.ipynb` apenas depois de gerar uma amostra textual processada.
