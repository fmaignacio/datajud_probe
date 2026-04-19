# Relatório de Contexto do Projeto (insumo para chatbot)

## 1) Objetivo do projeto (estado atual)

O projeto está em fase **exploratória** de pesquisa de mestrado, com foco em avaliar se bases públicas jurídicas são adequadas para sustentar uma etapa futura de análise semântica e comparação com saídas de LLMs.

O eixo técnico foi consolidado na base **STJ Dados Abertos — Íntegras de Decisões Terminativas e Acórdãos**, com uso de `SeqDocumento` como chave de vínculo entre metadados e textos integrais.

Neste momento, o objetivo **não** é treinar modelo, fazer fine-tuning, construir aplicação, nem tirar conclusões causais. O objetivo é validar qualidade, cobertura e estrutura dos dados para etapas posteriores.

## 2) Histórico resumido do que já foi feito

1. Projeto preparado para versionamento no Git/GitHub, com higiene inicial de publicação:
   - criação/ajuste de `.gitignore`, `.env.example`, README;
   - proteção de arquivos sensíveis e saídas geradas;
   - remoção de logs de chave.
2. Direcionamento metodológico documentado:
   - DataJud ficou como probe inicial;
   - STJ passou a ser a fonte principal para exploração semântica.
3. Estrutura de notebooks foi organizada em pipeline:
   - `00_download_stj_metadados.ipynb` (download iterativo dos metadados);
   - `01_exploracao_stj_metadados.ipynb` (EDA de metadados);
   - `02_validacao_integras_txt.ipynb` (vínculo `SeqDocumento` x TXT no ZIP);
   - `03_analise_textual_inicial.ipynb` (análise textual inicial);
   - `04_parse_tabela_assuntos.ipynb` (parser de tabela de assuntos para lookup).
4. Parser reutilizável criado em `src/assuntos.py` para tratar tabelas de assuntos em formato HTML com extensão `.xls`.
5. Lookup de assuntos passou a ser gerado (CSV/Parquet) para enriquecer a EDA com rótulos textuais quando disponível.

## 3) Achados principais até aqui

### 3.1 Sobre fontes de dados

- **DataJud**: útil para metadados processuais e movimentações, mas insuficiente (até aqui) como corpus textual principal.
- **TJSP**: útil para consultas pontuais, menor escalabilidade para coleta massiva.
- **STJ Dados Abertos**: melhor candidato atual para corpus semântico por oferecer metadados + íntegra em TXT + dicionário.

### 3.2 Sobre a exploração STJ

- O pipeline de metadados está operacional com download iterativo por período e organização por ano.
- A EDA passou de recortes de 1 dia para recortes maiores (jan–abr/2026 e depois 2024–2026 em execuções específicas), o que permitiu análises mensais/anuais.
- O campo `assuntos` foi confirmado como **código/trilha hierárquica**, não rótulo textual direto.
- Foi possível iniciar enriquecimento semântico de assuntos via tabela externa (lookup), incluindo resolução de exemplos como código `03608`.

## 4) Dificuldades e como foram tratadas

1. **Instabilidade do servidor STJ (HTTP 522)** durante downloads iterativos:
   - mitigado com retry, backoff, pausas e relatório de falhas.
2. **Erro de montagem do Drive no Colab** (`Mountpoint must not already contain files`):
   - mitigado com verificação de mount e fluxo de restart quando necessário.
3. **Falhas por arquivo não encontrado / caminhos misturados local x Colab**:
   - mitigado com padronização de caminhos por ambiente e validações de existência.
4. **Conflitos de notebook e metadados do Colab (`metadata.widgets`)**:
   - mitigado com limpeza de metadados/outputs para versionamento estável.
5. **EDA de assuntos com erros de pandas (colunas/índices duplicados no crosstab)**:
   - mitigado com normalização de colunas e reset de índice antes dos cruzamentos.
6. **Códigos de assunto perdendo zeros à esquerda (ex.: `03608` virando `3608`)**:
   - mitigado com normalização explícita para string de 5 dígitos por nível.
7. **Ambiente Python inconsistente (venv apontando para outro diretório)**:
   - identificado como causa de módulos “não encontrados”; correção orientada com recriação/seleção correta do kernel.

## 5) Estado atual (o que já está “pronto”)

- Estratégia do projeto e restrições estão documentadas.
- Fluxo de notebooks está definido por etapas.
- Download de metadados por recorte temporal está operacional.
- EDA de metadados está operacional (incluindo visão mensal e agregações por campos-chave).
- Parser de assuntos existe e já viabiliza geração de lookup para enriquecimento.

## 6) Riscos metodológicos em aberto

1. **Heterogeneidade temporal de schema** nos metadados (campos com padrão de preenchimento desigual por período).
2. **Cobertura incompleta de mapeamento de assuntos** (lookup pode não cobrir 100% dos códigos observados no STJ).
3. **Diferenças por instância judicial** nas tabelas de assuntos (possível divergência de nomenclatura/escopo por código).
4. **Volume e custo computacional** com expansão do período (2024–2026+), exigindo controle de memória e persistência incremental.

## 7) Próximos passos recomendados (ordem de execução)

1. **Consolidar lookup de assuntos**
   - Rodar `04_parse_tabela_assuntos.ipynb` localmente.
   - Gerar/atualizar `assuntos_lookup.parquet`.
   - Medir cobertura do lookup sobre os códigos de `assunto_final` da EDA.
2. **Expandir metadados por recorte temporal controlado**
   - Rodar `00_download_stj_metadados.ipynb` para 2025; depois 2024.
   - Manter organização por subpasta anual.
3. **Reexecutar EDA enriquecida**
   - Rodar `01_exploracao_stj_metadados.ipynb` com `ANOS_ANALISE` parametrizado.
   - Produzir tabelas comparáveis entre anos (ano/mês x tipo, teor, ministro, assuntos rotulados).
4. **Validação de vínculo textual**
   - Rodar `02_validacao_integras_txt.ipynb` em amostras controladas.
   - Confirmar cobertura `SeqDocumento` x TXT por período.
5. **Análise textual inicial (somente após passos acima)**
   - Rodar `03_analise_textual_inicial.ipynb` com corpus amostral rastreável.

## 8) Instruções de contexto para chatbot (como “entender” o projeto)

- Tratar o projeto como **pesquisa exploratória em andamento**, não produto final.
- Priorizar interpretações de **qualidade de dados, cobertura e consistência** antes de inferências substantivas.
- Sempre diferenciar:
  - metadado vs texto integral;
  - código de assunto vs rótulo textual mapeado;
  - contagem de documentos vs processos únicos.
- Ao sugerir análises, manter a ordem metodológica: metadados → vínculo com textos → textual.
- Ao reportar achados, explicitar período coberto e limitações de preenchimento dos campos.

## 9) Resumo executivo (curto)

O projeto evoluiu de um probe inicial do DataJud para um pipeline exploratório centrado no STJ Dados Abertos. Já existe infraestrutura de notebooks para download/EDA/validação textual, além de parser para mapear códigos de assuntos em rótulos textuais. O principal ganho foi sair de amostras pontuais para recortes temporais maiores e mais reprodutíveis. O próximo ciclo é consolidar o lookup de assuntos, ampliar o recorte temporal com controle de qualidade e só então avançar para análise textual amostral.
