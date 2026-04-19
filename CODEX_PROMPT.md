# Prompt para Codex — Projeto de Mestrado / Exploração STJ

Você está atuando como assistente técnico de desenvolvimento em um projeto de mestrado em Ciência de Dados.

## 1. Contexto acadêmico

O projeto investiga LLMs, governança epistêmica, conhecimento institucional, delegação cognitiva e riscos epistêmicos no setor público brasileiro.

O projeto ainda está em fase exploratória. Portanto, o objetivo atual não é construir uma solução final, nem um produto, nem um pipeline definitivo. O objetivo é realizar uma análise exploratória inicial de bases públicas que possam sustentar uma futura análise semântica.

## 2. Estado atual da pesquisa

A formulação teórica provisória é:

**Pergunta teórica:**  
Como o uso de LLMs em contextos institucionais reconfigura a produção, a validação e o uso do conhecimento institucional no setor público brasileiro?

**Hipótese teórica:**  
LLMs podem funcionar como forma implícita de delegação cognitiva, alterando práticas de validação, confiança e autoridade epistêmica.

A formulação empírica provisória é:

**Pergunta empírica:**  
Como saídas geradas por LLMs diferem de decisões humanas institucionais em casos jurídicos estruturados com dados públicos?

**Hipótese empírica:**  
LLMs tenderão a divergir de decisões humanas institucionais de forma não aleatória, revelando padrões de simplificação, sensibilidade à formulação do caso e possível reprodução de regularidades históricas.

## 3. Achados prévios sobre dados

Testes iniciais indicaram:

- DataJud é útil para metadados processuais e movimentações.
- DataJud não se confirmou, até aqui, como fonte textual/semântica principal.
- TJSP parece útil para consulta individual, mas pouco escalável.
- STJ Dados Abertos, especialmente o conjunto “Íntegras de Decisões Terminativas e Acórdãos do Diário da Justiça”, é o melhor candidato atual para corpus semântico.

## 4. Fonte principal atual

A fonte principal a explorar é:

**STJ — Íntegras de Decisões Terminativas e Acórdãos do Diário da Justiça**

A base contém:

- ZIP com textos integrais em TXT;
- JSON com metadados;
- CSV com dicionário de dados.

O campo-chave é:

- `SeqDocumento`

Segundo o dicionário, `SeqDocumento` identifica a decisão ou acórdão e corresponde ao nome do arquivo TXT dentro do ZIP.

Campos relevantes esperados nos metadados:

- `SeqDocumento`
- `dataPublicacao`
- `tipoDocumento`
- `numeroRegistro`
- `processo`
- `dataRecebimento`
- `dataDistribuicao`
- `ministro`
- `recurso`
- `teor`
- `descricaoMonocratica`
- `assuntos`

## 5. Objetivo técnico imediato

Criar uma análise exploratória mínima e reprodutível para:

1. carregar o JSON de metadados;
2. abrir o ZIP dos textos integrais;
3. validar a ligação entre `SeqDocumento` e arquivos TXT;
4. montar um DataFrame com metadados + texto integral;
5. limpar marcações HTML simples, como `<br>`;
6. gerar estatísticas descritivas;
7. salvar uma amostra processada;
8. produzir um relatório de cobertura e qualidade da base.

## 6. Restrições importantes

Não faça ainda:

- fine-tuning;
- treinamento de modelos;
- agente LLM;
- aplicação web;
- FastAPI;
- scraping do TJSP;
- Selenium;
- análise causal;
- conclusão sobre viés;
- comparação final com LLM.

Antes de qualquer modelo, precisamos entender a base.

## 7. Diretrizes de código

Use Python 3.11.

Priorize bibliotecas simples:

- pandas
- numpy
- zipfile
- json
- pathlib
- beautifulsoup4
- tqdm
- pyarrow, se necessário

Código deve ser:

- simples;
- modular;
- legível;
- documentado;
- seguro para dados brutos;
- sem abstrações prematuras.

Nunca sobrescreva dados brutos.

## 8. Estrutura desejada

Se a estrutura não existir, sugira ou crie:

```text
datajud_stj_semantic_probe/
├── README.md
├── docs/
│   ├── PROJETO_MESTRADO.md
│   └── CODEX_PROMPT.md
├── data/
│   ├── raw/
│   │   └── stj_integras/
│   ├── interim/
│   └── processed/
├── notebooks/
│   ├── 00_download_stj_metadados.ipynb
│   ├── 01_exploracao_stj_metadados.ipynb
│   ├── 02_validacao_integras_txt.ipynb
│   └── 03_analise_textual_inicial.ipynb
├── src/
│   ├── __init__.py
│   ├── io_stj.py
│   ├── clean_text.py
│   ├── eda.py
│   └── config.py
├── reports/
│   ├── figures/
│   └── summaries/
├── requirements.txt
└── .gitignore
```

## 9. Primeiras tarefas esperadas

### Tarefa A — inspeção da pasta de dados

Verifique quais arquivos existem em `data/raw/stj_integras/`.

Identifique:

- JSON de metadados;
- ZIP com textos;
- CSV do dicionário.

### Tarefa B — leitura dos metadados

Criar função:

```python
load_metadata(path: str | Path) -> pandas.DataFrame
```

A função deve:

- ler JSON;
- retornar DataFrame;
- preservar nomes de colunas;
- reportar número de linhas e colunas.

### Tarefa C — listagem do ZIP

Criar função:

```python
list_zip_txt_files(zip_path: str | Path) -> list[str]
```

A função deve listar arquivos TXT dentro do ZIP.

### Tarefa D — validação da chave

Criar função que compare:

- `SeqDocumento` no JSON;
- nomes dos arquivos TXT no ZIP.

Produzir relatório:

- total de metadados;
- total de TXT;
- quantos metadados têm TXT correspondente;
- quantos TXT não têm metadado correspondente.

### Tarefa E — construção de corpus amostral

Criar função:

```python
build_sample_corpus(metadata_df, zip_path, n=50) -> pandas.DataFrame
```

Campos esperados:

- `SeqDocumento`
- `dataPublicacao`
- `tipoDocumento`
- `processo`
- `ministro`
- `teor`
- `descricaoMonocratica`
- `assuntos`
- `texto_original`
- `texto_limpo`

### Tarefa F — limpeza textual básica

Criar função:

```python
clean_legal_text(text: str) -> str
```

Ela deve:

- converter `<br>` em quebra ou espaço;
- remover tags HTML simples;
- normalizar espaços;
- preservar pontuação e termos jurídicos;
- não aplicar stemming;
- não remover stopwords nesta fase.

### Tarefa G — relatório exploratório

Gerar arquivo em `reports/summaries/eda_summary.md` com:

- total de documentos;
- distribuição por tipo de documento;
- distribuição por ministro;
- distribuição por teor;
- tamanho médio, mínimo e máximo dos textos;
- percentual de textos vazios;
- observações sobre qualidade da base.

## 10. Estilo de resposta esperado

Ao responder, faça:

1. explique rapidamente o que vai alterar;
2. mostre apenas os trechos de código necessários;
3. evite código excessivo se a mudança for pequena;
4. não faça refatorações grandes sem necessidade;
5. mantenha o foco na etapa exploratória.

## 11. Resultado esperado desta interação

Ao final, o repositório deve permitir rodar uma primeira exploração local da base do STJ e responder:

- os textos estão acessíveis?
- os metadados se ligam corretamente aos TXT?
- a base tem qualidade mínima para análise semântica?
- quais campos são mais úteis para recorte posterior?
