Abaixo está um esquema modular, pensado para você rodar em etapas (download → ETL → armazenamento → preparação semântica).

> Estado atual do projeto: este documento começou como desenho geral. O repo já avançou para uma pipeline STJ/DataJud com notebooks específicos, lookups SGT/STJ e uma preocupação central: organizar os dados por **processo** como chave analítica, não apenas por documento.

***

## Próximo passo prioritário: espinha dorsal por processo

O próximo avanço metodológico deve ser construir uma tabela-mestra por processo, usando `numero_processo` CNJ como chave preferencial e preservando chaves auxiliares quando o CNJ não estiver disponível.

### Objetivo

Criar uma visão em que cada processo tenha:

- chave única preferencial: `numero_processo` CNJ normalizado, com 20 dígitos;
- chaves auxiliares: `numero_registro_stj`, `numero_processo_original` e `processo_agregacao`;
- documentos STJ associados, por `SeqDocumento`;
- eventos/movimentos DataJud em ordem cronológica;
- eventos de distribuição/redistribuição no STJ, quando houver ata;
- classes, assuntos, órgãos julgadores, graus e tribunais;
- indicadores de cobertura: tem texto, tem metadado STJ, tem DataJud, tem movimentos, tem CNJ confiável.

O sentido de “concatenar” aqui não deve ser colar textos sem critério, mas montar uma **linha do tempo estruturada**:

```text
processo -> evento_1 -> evento_2 -> ... -> documento_STJ_1 -> movimento_DataJud_n
```

Essa linha do tempo pode depois gerar uma versão textual para leitura humana ou LLM, mas a camada principal deve continuar tabular.

### Artefatos-alvo

```text
data/processed/process_spine.parquet
data/processed/stj_movimentos_datajud.parquet
data/processed/stj_integras_documentos_manifest.parquet
data/processed/stj_process_events.parquet
data/processed/stj_process_timeline.parquet
data/processed/stj_process_texts.parquet
```

Tabela sugerida para `stj_process_events.parquet`:

| coluna | descrição |
|---|---|
| `processo_agregacao` | chave operacional, CNJ quando disponível |
| `numero_processo` | CNJ normalizado |
| `numero_registro_stj` | chave interna STJ |
| `event_datetime` | data/hora do evento |
| `event_date` | data do evento |
| `event_order` | ordem estável dentro do processo |
| `event_source` | `datajud`, `ata_stj`, `integra_stj` |
| `event_type` | `movimento`, `distribuicao`, `documento`, etc. |
| `event_code` | código SGT/DataJud, quando houver |
| `event_label` | rótulo do evento |
| `event_detail` | detalhe textual curto |
| `tribunal` | tribunal ou fonte |
| `grau` | grau/instância |
| `classe_codigo` | classe processual |
| `classe_label` | rótulo da classe |
| `assunto_codigo_final` | assunto final normalizado |
| `assunto_label` | rótulo do assunto |
| `seq_documento` | documento STJ, quando o evento for documento |

Tabela sugerida para `stj_process_timeline.parquet`:

| coluna | descrição |
|---|---|
| `processo_agregacao` | chave operacional |
| `numero_processo` | CNJ |
| `timeline_event_count` | número de eventos |
| `timeline_start` | primeira data conhecida |
| `timeline_end` | última data conhecida |
| `timeline_text` | narrativa curta ordenada por data |
| `timeline_json` | lista serializada de eventos estruturados |

### Uso do DataJud

O DataJud deve entrar como fonte para reconstruir metadados e movimentações. O fluxo mais seguro é:

1. partir de processos já vistos no STJ;
2. normalizar CNJ;
3. consultar DataJud por `numeroProcesso`;
4. salvar o JSON bruto por tribunal/fonte;
5. extrair `classe`, `assuntos`, `grau`, `tribunal`, `orgaoJulgador`, `dataAjuizamento`, `dataHoraUltimaAtualizacao` e `movimentos`;
6. transformar movimentos em eventos;
7. juntar tudo na linha do tempo por processo.

O notebook mais próximo disso hoje é `notebooks/06_ciclo_vida_processual_stj.ipynb`. Ele já cria `process_spine`, `datajud_movimentos`, `datajud_assuntos` e manifesto de documentos. A melhoria natural é criar explicitamente `stj_process_events.parquet` e `stj_process_timeline.parquet`.

### Recorte temático inicial: drogas

Vale a pena juntar o grupo inteiro de assuntos de drogas, desde que ele seja marcado em duas famílias. A primeira é penal adulta, sob `DIREITO PENAL`:

```text
3607   Crimes de Tráfico Ilícito e Uso Indevido de Drogas
5897   Associação para a Produção e Tráfico e Condutas Afins
5899   Colaboração com Grupo, Organização ou Associação Destinados à Produção ou Tráfico de Drogas
5901   Condução de Embarcação ou Aeronave sob Efeito de Drogas
5894   Fabricação de Objeto Destinado a Produção de Drogas e Condutas Afins
5898   Financiamento ou Custeio de Produção ou Tráfico de Drogas
5895   Indução, Instigação ou Auxílio ao Uso de Drogas
5896   Oferecimento de Drogas para Consumo Conjunto
5885   Posse de Drogas para Consumo Pessoal
5900   Prescrição Culposa de Drogas
3608   Tráfico de Drogas e Condutas Afins
```

No lookup SGT/STJ local, essa árvore aparece sob:

```text
DIREITO PENAL
> Crimes Previstos na Legislação Extravagante
> Crimes de Tráfico Ilícito e Uso Indevido de Drogas
```

Dois códigos citados para esse grupo não apareceram no export SGT/STJ local e devem ser verificados em outra versão/fonte SGT antes de entrar no filtro automático:

```text
10523  Despenalização / Descriminalização
10987  Tráfico Ilícito de Drogas praticado por Funcionário Público
```

A segunda família é de ato infracional, sob `DIREITO DA CRIANÇA E DO ADOLESCENTE`:

```text
9858  De Tráfico Ilícito e Uso Indevido de Drogas
9864  Associação para a Produção e Tráfico e Condutas Afins
9866  Colaboração com Grupo, Organização ou Associação Destinados à Produção ou Tráfico de Drogas
9868  Condução de Embarcação ou Aeronave sob Efeito de Drogas
9861  Fabricação de Objeto Destinado a Produção de Drogas e Condutas Afins
9865  Financiamento ou Custeio de Produção ou Tráfico de Drogas
9862  Indução, Instigação ou Auxílio ao Uso de Drogas
9863  Oferecimento de Drogas para Consumo Conjunto
9860  Posse de Drogas para Consumo Pessoal
9867  Prescrição Culposa de Drogas
9859  Tráfico de Drogas e Condutas Afins
```

No lookup SGT/STJ local, essa árvore aparece sob:

```text
DIREITO DA CRIANÇA E DO ADOLESCENTE
> Ato Infracional
> Previstos na Legislação Extravagante
> De Tráfico Ilícito e Uso Indevido de Drogas
```

Portanto, ela parece representar **atos infracionais análogos a crimes de drogas**, não necessariamente o recorte penal adulto inteiro. Para tráfico penal geral, também é necessário incluir a árvore de `DIREITO PENAL`, por exemplo:

Recomendação prática:

- criar uma lista `ASSUNTOS_DROGAS_PENAL = {3607, 3608, 5885, 5894, 5895, 5896, 5897, 5898, 5899, 5900, 5901}`;
- criar uma lista `ASSUNTOS_DROGAS_ADOLESCENTE = {9858, 9859, ..., 9868}`;
- manter `10523` e `10987` em uma lista `ASSUNTOS_DROGAS_VERIFICAR`, até confirmar se aparecem em outra fonte SGT;
- manter uma coluna `recorte_drogas_tipo`, com valores como `ato_infracional`, `penal_adulto`, `ambos`, `fora_recorte`.

### Instâncias e tribunais a mapear

Para esse recorte, as dimensões mínimas devem ser:

```text
Justiça Estadual
- 1º Grau
- 2º Grau

Tribunais superiores
- STJ
- STF
```

No DataJud, isso deve ser modelado por:

- `tribunal`: tribunal de origem, por exemplo TJ, STJ, STF;
- `grau`: grau informado pelo DataJud;
- partes do CNJ: segmento, tribunal e origem extraídos do número;
- `classe` e `assuntos`, para confirmar se o processo pertence ao recorte.

Para responder “em que instâncias ou tribunais esses assuntos/crimes são julgados”, a tabela esperada é algo como:

| assunto_codigo | assunto_label | tribunal | grau | n_processos | n_movimentos | primeira_data | ultima_data |
|---|---|---|---|---:|---:|---|---|

Essa tabela deve ser derivada de DataJud + SGT/STJ, não apenas dos documentos de íntegra do STJ.

### Cautelas metodológicas

- Documento STJ não é processo completo.
- `SeqDocumento` é chave documental, não chave processual.
- `numeroRegistro` é chave STJ, não substitui o CNJ quando a pergunta é trajetória processual.
- DataJud ajuda a reconstruir andamentos, mas a cobertura precisa ser medida.
- O recorte `9858` é de ato infracional; usar como “crime de drogas” sem essa ressalva pode distorcer a análise.
- A linha do tempo deve preservar fonte e granularidade de cada evento.

***

### 1. **Estrutura de pastas e dependências**

Sugestão de estrutura mínima:

```text
projeto_juridico/
├── config/
│   └── settings.py
├── data/
│   ├── raw_stj/          # arquivos brutos STJ (zip, xml, etc.)
│   ├── raw_datajud/      # json/CSV de DataJud
│   └── processed/        # datasets limpos (parquet ou CSV)
├── src/
│   ├── fetch_stj.py      # download via CKAN
│   ├── fetch_datajud.py  # chamadas à API DataJud
│   ├── parse_stj.py      # parser de íntegras (XML/HTML)
│   └── build_corpus.py   # criação de corpus (textos + metadados)
└── notebooks/
    └── exploratory.ipynb
```

Dependências básicas (ex.: `requirements.txt`):

```txt
requests
pandas
beautifulsoup4
lxml
python-dateutil
fastparquet or pyarrow
tqdm
```


***

### 2. **Passo 1 – Baixar dados STJ (CKAN)**

No STJ o portal de dados expõe arquivos como íntegras, Diários, acórdãos, etc., em pacotes (CSV, XML, ZIP).[^1][^2]

Sugestão de fluxo em `src/fetch_stj.py`:

```python
import requests
import json
from pathlib import Path

CKAN_URL = "https://dadosabertos.web.stj.jus.br/api/3/action"

def list_datasets_stj():
    """Lista datasets do STJ via CKAN."""
    url = f"{CKAN_URL}/package_list"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()["result"]

def get_resource_info(dataset_id: str):
    """Pega os recursos (arquivos) de um dataset."""
    url = f"{CKAN_URL}/package_show?id={dataset_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    pkg = resp.json()["result"]
    return pkg["resources"]  # lista de dicionários com url, format, etc.

def download_resource(url: str, dest: Path):
    """Baixa um recurso (ex.: XML, CSV, ZIP)."""
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

# Exemplo de uso:
if __name__ == "__main__":
    data_dir = Path("data/raw_stj")

    pkgs = list_datasets_stj()
    # filtre por algo como "integra", "acordao", "diario"
    for pkg_name in pkgs:
        if "integra" in pkg_name.lower():
            print("Dataset:", pkg_name)
            resources = get_resource_info(pkg_name)
            for res in resources:
                dest = data_dir / res["name"]
                dest.parent.mkdir(exist_ok=True, parents=True)
                print("Download:", res["url"])
                download_resource(res["url"], dest)
```

Você pode filtrar por nomes como `integra_acordao`, `diario_eletronico`, etc., e baixar os arquivos cruamente.

***

### 3. **Passo 2 – Obter dados processuais via DataJud**

DataJud expõe endpoints REST com metadados de processos (orgão, classe, assunto, etc.), mas não o texto integral.[^3][^4]

Exemplo básico em `src/fetch_datajud.py`:

```python
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path


DATAJUD_URL = "https://api.datajud.cnj.jus.br"

def paginate(endpoint: str):
    """Helper para endpoints paginados do DataJud."""
    page = 0
    while True:
        params = {"page": page, "size": 100}
        resp = requests.get(DATAJUD_URL + endpoint, params=params)
        resp.raise_for_status()
        page_data = resp.json()
        if not page_data["content"]:
            break
        yield from page_data["content"]
        page += 1

def fetch_processos():
    """Baixa processos (ex.: STJ) e salva."""
    rows = []
    for proc in paginate("/api/v1/processo"):
        # selecione campos relevantes para você
        row = {
            "id_processo": proc["id"],
            "numero": proc["numero"],
            "classe": proc["classe"]["nome"],
            "orgao_julgador": proc["orgaoJulgador"]["nome"],
            "assunto": ", ".join([a["nome"] for a in proc["assuntos"]]),
            "data_ajuizamento": proc["dataAjuizamento"],
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_parquet("data/raw_datajud/processos.parquet")
    print("Processos salvos em parquet.")
```

Depois você pode cruzar esses `numero` / `id_processo` com números de processo extraídos das íntegras STJ.

***

### 4. **Passo 3 – Parse de íntegras STJ (XML / HTML)**

Os arquivos do STJ costumam ser em **XML/HTML** (íntegra de acórdãos, votos, etc.). Um parser simples em `src/parse_stj.py`:

```python
from pathlib import Path
import re
from bs4 import BeautifulSoup
import pandas as pd


def parse_integra_html(path: Path):
    """Extrai campos de um arquivo HTML/XML de íntegra."""
    text = path.read_text(encoding="utf-8", errors="ignore")

    # 1) Extração de texto “limpo”
    soup = BeautifulSoup(text, "lxml")
    body = soup.find("body") or soup
    clean_text = body.get_text(" ", strip=True)

    # 2) Extração de metadados (ajuste conforme o padrão do STJ)
    headers = re.findall(r"<span.*?class=['\"]([^'\"]+).*?>(.*?)</span>", text)

    metadata = {
        "file_path": str(path),
        "processo_numero": "",  # preencha com regex adequada
        "classe": "",
        "tipo": "",
        "data_julgamento": "",
    }

    # Exemplo de regex para nº de processo (ajuste conforme o padrão efetivo)
    m = re.search(r"Processo\s*n.\s*([^<>\s]+)", text, re.IGNORECASE)
    if m:
        metadata["processo_numero"] = m.group(1).strip()

    # 3) Montar votos (se o documento diferencia relator, voto, etc.)
    votos = []
    # Ex.: separar por tags/div/classes de votos
    for section in soup.find_all(["div", "p"], class_=re.compile(r"voto|relator", re.IGNORECASE)):
        voto_text = section.get_text(" ", strip=True)
        votos.append({"tipo": "voto", "texto": voto_text})

    return {
        "metadata": metadata,
        "texto_integral": clean_text,
        "votos": votos,
    }


def batch_parse_integras():
    """Percorre todos os arquivos brutos e cria um corpus."""
    integra_dir = Path("data/raw_stj")
    outputs = []

    for p in integra_dir.rglob("*.*"):
        if p.is_file() and p.suffix.lower() in (".html", ".xml", ".htm"):
            print("Parse:", p)
            try:
                doc = parse_integra_html(p)
                outputs.append(doc)
            except Exception as e:
                print("Erro parseando", p, e)

    # Salva metadata + texto em CSV/parquet
    rows = []
    for out in outputs:
        meta = out["metadata"]
        for voto in out["votos"]:
            row = meta.copy()
            row["texto_voto"] = voto["texto"]
            row["tipo_elemento"] = "voto"
            rows.append(row)
        # também pode guardar o texto integral
        row_full = meta.copy()
        row_full["texto_integral"] = out["texto_integral"]
        row_full["tipo_elemento"] = "integral"
        rows.append(row_full)

    df = pd.DataFrame(rows)
    df.to_parquet("data/processed/stj_corpus.parquet")
```

Você pode adaptar as regex e seletores de classe conforme o padrão exato dos arquivos do STJ.

***

### 5. **Passo 4 – Cruzamento STJ + DataJud e armazenamento**

Criar um dataset unificado em `src/build_corpus.py`:

```python
import pandas as pd


def join_stj_datajud():
    # Carrega STJ
    df_stj = pd.read_parquet("data/processed/stj_corpus.parquet")

    # Carrega DataJud (ajuste o caminho de acordo com o que você baixou)
    df_datajud = pd.read_parquet("data/raw_datajud/processos.parquet")

    # Normaliza número de processo (ex.: remover pontos, traços, etc.)
    normalize = lambda x: str(x).replace(".", "").replace("-", "").replace("/", "") if pd.notna(x) else ""
    df_stj["processo_norm"] = df_stj["processo_numero"].apply(normalize)
    df_datajud["processo_norm"] = df_datajud["numero"].apply(normalize)

    # Cruzar STJ x DataJud
    df_joined = df_stj.merge(
        df_datajud,
        left_on="processo_norm",
        right_on="processo_norm",
        suffixes=("_stj", "_datajud"),
        how="left",
    )

    # Colunas relevantes para NLP / embeddings
    cols = [
        "processo_numero",
        "classe_stj",
        "assunto",
        "orgao_julgador",
        "texto_integral",
        "texto_voto",
    ]
    df_final = df_joined[cols].dropna(how="all").drop_duplicates()

    # Salva um corpus “flat” pronto para embeddings
    df_final.to_parquet("data/processed/corpus_semantico.parquet")
    print("Corpus semântico pronto para embeddings.")
```


***

### 6. **Passo 5 – Preparar para embeddings ou fine‑tuning**

Para uso em modelos (ex.: embeddings por documento, fine‑tuning de BERT‑PT), você pode ter um script de preparação:

```python
import pandas as pd
from datasets import Dataset

# Carrega o corpus
df = pd.read_parquet("data/processed/corpus_semantico.parquet")

# Escolha um texto por documento (ex.: voto, ou texto integral)
df_text = df[["processo_numero", "texto_voto"]].dropna(subset=["texto_voto"])
df_text = df_text.rename(columns={"texto_voto": "text"})

# Converte para Dataset do Hugging Face
ds = Dataset.from_pandas(df_text)

# Pode salvar em disco ou usar diretamente no treinamento
ds.save_to_disk("data/processed/dataset_hf")
```


***

### 7. **Resumo do pipeline**

| Etapa | Ferramenta/Fonte | Saída principal |
| :-- | :-- | :-- |
| 1. Download STJ | CKAN API (`dadosabertos.web.stj.jus.br`) | HTML/XML brutos em `data/raw_stj` |
| 2. Download DataJud | API pública `api.datajud.cnj.jus.br` | Parquet/CSV de metadados processuais |
| 3. Parser de íntegras | BeautifulSoup + regex | `corpus_semantico.parquet` com texto e metadados |
| 4. Cruzamento | Pandas merge por número de processo | Dataset unificado |
| 5. Embeddings / fine‑tuning | Transformers + `datasets` | `dataset_hf` pronto para treino |

Se você quiser, na próxima mensagem posso aprofundar em:

- Um **tokenizador de texto jurídico específico** (ex.: remoção de cabeçalhos do STJ, identificação de partes, etc.).
- Ou um **pipeline mínimo usando Sentence‑Transformers** para gerar embeddings por documento a partir desse corpus.

<div align="center">⁂</div>

[^1]: https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/2022/12092022-Portal-de-Dados-Abertos-do-STJ-disponibiliza-informacoes-de-interesse-publico-em-formato-legivel-por-maquina.aspx

[^2]: https://dadosabertos.web.stj.jus.br

[^3]: https://portal.trf6.jus.br/portal-da-transparencia/tecnologia-da-informacao-e-comunicacao-2/dadosabertos/

[^4]: https://datajud-wiki.cnj.jus.br/api-publica/
