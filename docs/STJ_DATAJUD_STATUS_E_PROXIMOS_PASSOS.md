# STJ + DataJud: Status, Decisoes e Proximos Passos

Este documento consolida o estado atual do projeto depois da primeira rodada
bem-sucedida de integracao entre:

- ATA de distribuicao do STJ;
- metadados e textos das integras do STJ;
- dashboard Streamlit baseado em JSON por processo;
- primeiros testes de consulta ao `api_publica_stj` do DataJud.

O objetivo deste material e preservar a memoria operacional do que ja foi
feito, evitar retrabalho e orientar a proxima fase: reconstruir a **vida util
processual no STJ**, enriquecida com metadados e movimentacoes do DataJud.

## 1. Posicao metodologica atual

O projeto nao esta mais tentando responder, neste momento, a pergunta de
"corpus textual geral do Judiciario".

A formulacao metodologica atual mais segura e:

> Construir a vida util processual no STJ, enriquecida com data de ajuizamento
> e metadados processuais do DataJud, mantendo a camada semantica textual
> restrita ao corpus de integras do STJ.

Isso implica as seguintes decisoes:

- **DataJud nao sera tratado como corpus textual principal**.
- **Integras do STJ seguem como fonte semantica principal**.
- **DataJud entra como camada estruturante de metadados e movimentacoes**.
- **ATA do STJ e a ponte principal entre CNJ e registro STJ**.

## 2. O que ja foi construido

### 2.1 Notebook 06: espinha dorsal processual

O notebook `06_ciclo_vida_processual_stj.ipynb` passou a gerar uma espinha
dorsal funcional por processo com base na ATA do STJ.

Resultados relevantes da rodada validada:

- `processos_total = 2582`
- `com_ata_distribuicao = 2582`
- `com_datajud = 0` na rodada antiga do cache local do notebook
- `com_documentos_corpus = 48`
- `ja_existia_antes_corpus = 48`

Esses 48 processos sao os casos em que a ligacao:

```text
ATA (CNJ + registro STJ) <-> integras STJ (registro STJ)
```

funcionou com sucesso.

### 2.2 Correcao importante ja incorporada

O ponto decisivo foi perceber que:

- a ATA do STJ carrega `numero_processo` e `numero_registro_stj`;
- as integras do STJ, em grande parte, nao carregam CNJ, mas carregam
  `numero_registro_stj`;
- portanto, o merge com o corpus documental precisava usar **registro STJ**.

Essa correcao foi incorporada no notebook 06 e permitiu sair de:

```text
com_documentos_corpus = 0
```

para:

```text
com_documentos_corpus = 48
```

### 2.3 Notebook 07: documento-texto por processo

O notebook `07_documentos_por_processo_stj.ipynb` foi validado com sucesso.

Resultados relevantes:

- `metadata_rows = 93482`
- `metadata_com_txt = 84224`
- `metadata_sem_txt = 9258`
- `txt_files = 86574`
- `txt_sem_metadata = 2350`
- `processos_com_chave_agregacao = 89873`
- `Documentos enriquecidos por registro STJ = 78`
- `textos_por_processo = (81049, 11)`

Interpretacao:

- o pipeline documento-texto esta funcional;
- a camada semantica do STJ e robusta;
- parte dos processos da ATA ja consegue herdar documentos do corpus textual.

### 2.4 JSON por processo

Foi criado o script:

```text
scripts/build_process_json.py
```

Ele gera:

```text
data/processed/process_json/*.json
data/processed/demo/processos_demo.jsonl
data/processed/demo/processos_demo_index.csv
```

O schema atual do JSON por processo inclui:

- `processo`
- `stj`
- `partes`
- `documentos`
- `timeline`
- `datajud`
- `metadados_pipeline`

O bloco `datajud` ainda existe como placeholder, pronto para enriquecimento.

### 2.5 Dashboard Streamlit

Foi criado um dashboard minimalista:

```text
apps/process_dashboard.py
```

Capacidades atuais:

- carregar indice de demo;
- selecionar processo;
- exibir resumo;
- mostrar partes e advogados;
- mostrar timeline;
- mostrar documentos textuais;
- abrir o JSON bruto.

Correcao importante incorporada:

- o dashboard agora resolve automaticamente caminhos absolutos do Colab
  (`/content/drive/...`) para o caminho local sincronizado do Google Drive for
  Desktop.

## 3. O que aprendemos sobre as chaves

### 3.1 Chaves do lado STJ

No projeto, as chaves relevantes hoje sao:

- `numero_processo`: CNJ
- `numero_registro_stj`: registro interno STJ
- `seq_documento`: chave documental

### 3.2 Relacao entre as fontes

```text
ATA STJ -> numero_processo + numero_registro_stj
Integras STJ -> numero_registro_stj + seq_documento
DataJud STJ -> numeroProcesso
```

Conclusao operacional:

- **CNJ deve ser a chave principal de processo**
- **registro STJ deve ser a chave auxiliar para o corpus documental**
- **SeqDocumento deve continuar sendo chave documental**

## 4. O que o teste no DataJud STJ mostrou

O notebook `99_teste.ipynb` confirmou que o endpoint:

```text
https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search
```

devolve, pelo menos para o STJ:

- `numeroProcesso`
- `classe`
- `tribunal`
- `grau`
- `dataHoraUltimaAtualizacao`
- `dataAjuizamento`
- `movimentos`
- `orgaoJulgador`
- `assuntos`
- `nivelSigilo`

Isso e crucial porque torna viavel a seguinte formulacao:

> Vida util processual no STJ, enriquecida com data de ajuizamento e metadados
> processuais do DataJud.

### 4.1 O que isso permite reconstruir

No STJ, com a integracao correta, podemos reconstruir:

- entrada/distribuicao no STJ;
- movimentacoes no STJ;
- peticoes, remessas, conclusoes, publicacoes e baixas;
- documentos textuais do corpus de integras;
- partes e advogados da ATA;
- assuntos e classe processual.

### 4.2 O que isso ainda nao garante

Ainda nao garante, sem ressalvas:

- vida util completa do processo no Judiciario inteiro;
- todos os eventos anteriores ao STJ;
- cobertura uniforme de tribunais de origem.

Portanto, a linguagem metodologica recomendada e:

```text
vida util processual no STJ
```

e nao:

```text
vida util completa do processo no Brasil
```

## 5. Papel do XSD / Modelo de Transferencia de Dados

O arquivo:

```text
modelo-de-transferencia-de-dados-1.2-81544272558adf336e6c4d58ed66e4f7.xsd
```

foi identificado como referencia importante para a proxima fase.

Ele nao resolve sozinho a heterogeneidade real das implementacoes, mas ajuda a:

- definir schema canonicamente esperado;
- interpretar tipos de pessoa, OAB, endereco e outros objetos;
- mapear campos entre tribunais;
- separar "campo inexistente" de "campo divergente da implementacao".

Interpretacao recomendada:

- o XSD e uma **referencia de schema**;
- nao e prova de consistencia empirica entre todos os tribunais;
- mas e excelente para desenhar a camada canônica de ingestao DataJud.

## 6. Decisao sobre banco de dados

Foi decidido **nao criar banco agora**.

Justificativa:

- os parquets e JSONs atuais ja sustentam exploracao, dashboard e prova de
  conceito;
- o problema principal agora nao e armazenamento, e integracao de chaves e
  movimentos;
- criar banco agora aumentaria complexidade antes da consolidacao da camada
  analitica.

## 7. Redesenho recomendado dos notebooks

O fluxo atual ainda mistura duas preocupacoes:

- construir o backbone do processo;
- anexar texto/documento;
- testar DataJud.

Para reduzir confusao, o fluxo recomendado daqui para frente e:

### Notebook 06

Manter como:

```text
espinha dorsal STJ + ATA + manifesto documental + ligacao por registro STJ
```

Responsabilidades:

- carregar ATA;
- carregar manifesto das integras;
- manter `stj_processos_ciclo_vida.parquet`;
- manter `stj_integras_corpus_por_chave.parquet`;
- manter parte documental agregada por processo/chave.

Nao deve tentar virar, sozinho, a timeline final enriquecida.

### Notebook 07

Manter como:

```text
camada documento-texto
```

Responsabilidades:

- ligar metadados e ZIPs de texto;
- produzir `stj_documentos_por_processo.parquet`;
- produzir `stj_textos_por_processo.parquet`;
- enriquecer documentos pela espinha dorsal quando possivel.

### Novo Notebook 09

Novo foco:

```text
coleta DataJud STJ por CNJ
```

Responsabilidades:

- ler `stj_processos_ciclo_vida.parquet`;
- consultar `api_publica_stj` por `numeroProcesso`;
- salvar resposta bruta;
- extrair:
  - processo DataJud;
  - movimentos;
  - assuntos;
  - orgao julgador;
  - status de encontro/nao encontro;
- gerar:
  - `stj_datajud_processos.parquet`
  - `stj_datajud_movimentos.parquet`
  - `stj_datajud_assuntos.parquet`
  - `stj_datajud_lookup_status.parquet`

### Novo Notebook 10

Novo foco:

```text
vida util STJ enriquecida
```

Responsabilidades:

- juntar:
  - espinha dorsal do notebook 06;
  - movimentos DataJud STJ do notebook 09;
  - documentos/textos do notebook 07;
- gerar timeline unificada;
- produzir JSON por processo enriquecido;
- medir cobertura final.

## 8. Proposta objetiva para os proximos passos

### Passo 1

Consolidar o DataJud STJ como fonte de movimentos por CNJ.

Meta:

- testar primeiro com os 20 processos de demo;
- depois escalar para os 2582 da ATA.

### Passo 2

Criar uma tabela de status por CNJ:

```text
numero_processo
numero_registro_stj
status_datajud
n_movimentos
tem_assuntos
tem_orgao_julgador
data_ajuizamento
data_ultima_atualizacao
```

### Passo 3

Gerar uma timeline enriquecida por processo:

```text
ata_stj + datajud_stj + integra_stj
```

### Passo 4

Atualizar o JSON por processo para incluir:

- `datajud.status`
- `datajud.data_ajuizamento`
- `datajud.data_ultima_atualizacao`
- `datajud.movimentos`
- `datajud.assuntos`

### Passo 5

Atualizar o dashboard Streamlit para mostrar:

- movimentos DataJud;
- comparacao entre timeline documental e timeline processual;
- indicadores de cobertura.

## 9. Formula de trabalho recomendada

Para reduzir dispersao, a prioridade sugerida e:

1. fechar o notebook 09;
2. validar DataJud STJ em lote pequeno;
3. fechar o notebook 10;
4. regenerar JSONs;
5. evoluir o dashboard.

## 10. Frases metodologicas recomendadas para apresentacao

### Formula forte e segura

> Reconstruimos uma vida util processual no STJ, combinando atos de
> distribuicao, partes e advogados da ATA, movimentos estruturados do DataJud e
> documentos textuais das integras do STJ.

### Formula com ressalva correta

> A camada semantica textual, por ora, esta restrita ao STJ. O DataJud entra
> como camada estruturante de metadados e movimentacoes, nao como corpus textual
> principal.

### Formula a evitar

Evitar dizer sem qualificacao:

> vida util completa do processo em todas as instancias

porque isso ainda exigiria integrar tribunais de origem.
