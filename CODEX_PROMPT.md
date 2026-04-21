# Prompt de Contexto para ChatGPT/Codex — Projeto STJ/DataJud e Dissertacao de Mestrado

Use este documento como prompt inicial ao conectar um novo chat/projeto ChatGPT a este repositório. A primeira tarefa do assistente deve ser ler `README.md` e `docs/NOTEBOOK_GUIDE.md`, porque esses dois arquivos documentam a estrutura operacional mais atual.

## 1. Identidade do projeto

Repositorio: `datajud_probe`

Branch de transicao recomendada para continuar o trabalho:

```text
transicao/stj-eda-pipeline
```

Branch original de desenvolvimento:

```text
claude/evaluate-legal-databases-yWU5P
```

O projeto nasceu como um probe da API publica do DataJud, mas evoluiu para uma investigacao empirica com dados abertos do STJ, especialmente o conjunto:

```text
STJ - Integras de Decisoes Terminativas e Acordaos do Diario da Justica
```

O objetivo tecnico imediato e construir um corpus juridico confiavel para analise empirica e, futuramente, comparacao com saidas de LLMs. O objetivo academico maior e sustentar uma dissertacao de mestrado sobre LLMs, conhecimento institucional, delegacao cognitiva e riscos epistemicos no setor publico brasileiro.

## 2. Contexto academico da dissertacao

Area geral: Ciencia de Dados / sociedade / instituicoes publicas / direito / LLMs.

Tema teorico em construcao:

- LLMs como infraestrutura de mediacao cognitiva;
- governanca epistemica;
- conhecimento institucional;
- delegacao cognitiva;
- confianca, validacao e autoridade epistemica;
- riscos de simplificacao, automacao interpretativa e reproducao de regularidades historicas.

Pergunta teorica provisoria:

> Como o uso de LLMs em contextos institucionais reconfigura a producao, a validacao e o uso do conhecimento institucional no setor publico brasileiro?

Hipotese teorica provisoria:

> LLMs podem funcionar como forma implicita de delegacao cognitiva, alterando praticas de validacao, confianca e autoridade epistemica.

Pergunta empirica provisoria:

> Como saidas geradas por LLMs diferem de decisoes humanas institucionais em casos juridicos estruturados com dados publicos?

Hipotese empirica provisoria:

> LLMs tenderao a divergir de decisoes humanas institucionais de forma nao aleatoria, revelando padroes de simplificacao, sensibilidade a formulacao do caso e possivel reproducao de regularidades historicas.

Importante: a pesquisa ainda esta em fase exploratoria. Nao trate os resultados atuais como conclusoes finais sobre vies, causalidade, desempenho judicial, produtividade de ministros ou validade juridica das decisoes.

## 3. Estado atual do corpus e recorte

Recorte atual de trabalho:

```text
2024, 2025, 2026
```

A base principal atual e STJ Integras. Ela oferece:

- JSONs de metadados: `metadados<aaaammdd>.json`;
- ZIPs de textos integrais: `textos<aaaammdd>.zip` ou originalmente `<aaaammdd>.zip`;
- chave documental: `SeqDocumento`.

Estrutura esperada no Drive/Colab:

```text
/content/drive/MyDrive/Mestrado/2026/llms/data/
├── raw/
│   ├── stj_integras_metadata/
│   │   ├── 2024/metadados2024....json
│   │   ├── 2025/metadados2025....json
│   │   └── 2026/metadados2026....json
│   └── stj_integras/
│       ├── 2024/textos2024....zip
│       ├── 2025/textos2025....zip
│       └── 2026/textos2026....zip
├── processed/
├── reports/
│   ├── summaries/
│   └── figures/
└── reference/
    └── assuntos/processed/assuntos_lookup.parquet
```

No repositório local, dados brutos grandes em `data/raw/` e relatórios em `data/reports/` ficam ignorados pelo Git. Alguns arquivos menores de contexto da API estão em `data/api/`.

## 4. Camadas conceituais: documento, registro, processo e instancia

Este e o ponto metodologico mais importante.

A base STJ Integras e excelente para **documentos**. Ela ainda nao resolve automaticamente a **vida processual completa**.

Camadas:

1. Documento STJ
   - Chave principal: `SeqDocumento`.
   - Uso: texto integral, tipo documental, teor, recurso, assunto, data de publicacao.

2. Registro STJ
   - Chave importante: `numeroRegistro`.
   - Uso: agrupar documentos quando o CNJ nao aparece de forma confiavel.

3. Processo/CNJ
   - Chave desejada: numero CNJ normalizado, quando disponivel.
   - Uso: vida processual, origem, conexao com DataJud e outras instancias.

4. Outras instancias
   - Ainda nao capturadas de forma robusta.
   - Futuro: DataJud, tribunais de origem, movimentacoes, espelhos/acordaos e outros datasets.

Nao confundir:

- contagem de documentos com contagem de processos;
- `numeroRegistro` STJ com CNJ;
- primeira aparicao no corpus com nascimento do processo;
- metadados STJ com vida processual completa.

## 5. Achados atuais da EDA documental

A EDA 2024-2026, gerada pelo notebook `01` e apresentada no `08`, indica aproximadamente:

- 551 arquivos de metadados;
- 1,54 milhao de documentos;
- 1,1 milhao de processos/registros unicos segundo os campos disponiveis;
- 1,53 milhao de `SeqDocumento` unicos;
- predominancia de `DECISAO` sobre `ACORDAO`;
- teor concentrado em `Nao Conhecendo` e `Negando`;
- recursos frequentes como `AgInt`, `EDcl`, `AgRg`;
- concentracoes tematicas fortes em codigos de assunto penal, alem de civil, consumidor e tributario.

Depois de corrigir a preparacao do campo de ministro, a EDA combina `ministro`, `NM_MINISTRO` e `relator`. Antes disso, parecia haver mais de 99% de vazio, mas era um erro de coalescencia de coluna. Ainda assim, relatoria nos metadados deve ser apresentada como concentracao documental no STJ, nao como produtividade judicial completa.

## 6. Estado dos assuntos

O campo `assuntos` nos metadados vem como codigo/trilha hierarquica. O projeto tenta rotular esses codigos usando um lookup gerado no notebook `04`.

Cuidado: a fonte local inicialmente usada foi:

```text
notebooks/78_Tabela_Assuntos_Justica_Federal_1_Grau.xls
```

Portanto, os nomes de assunto sao **rotulos auxiliares provisórios**. Nao apresente a coluna `instancia` como prova de cobertura multi-instancia. O uso seguro e:

> Os codigos de assunto indicam concentracoes tematicas; os nomes textuais atuais ajudam na leitura, mas precisam ser ampliados com tabelas CNJ/outras instancias.

## 7. Dados STJ alem das Integras

Na pagina de Dados Abertos do STJ ha 19 conjuntos. Proximos candidatos importantes:

### Espelhos de Acordaos

Muito promissor para enriquecer acordaos, pois traz:

- `numeroProcesso`;
- `numeroRegistro`;
- `siglaClasse`;
- `descricaoClasse`;
- `nomeOrgaoJulgador`;
- `ministroRelator`;
- `ementa`;
- `tipoDeDecisao`;
- `dataDecisao`;
- `decisao`;
- `jurisprudenciaCitada`;
- `informacoesComplementares`;
- `termosAuxiliares`;
- `teseJuridica`;
- `tema`;
- `referenciasLegislativas`;
- `acordaosSimilares`;
- `dataPublicacao`.

Prioridade futura: criar notebooks para baixar, explorar e juntar Espelhos de Acordaos com Integras por `numeroRegistro` e/ou `numeroProcesso`.

### Atas de Distribuicao

Boa para eventos de entrada/distribuicao/redistribuicao no STJ. Ja ha arquivos de exemplo em `data/api/`.

### Movimentacao Processual

Pode ser importante para reconstruir a vida interna do processo no STJ.

### DataJud

Util para metadados nacionais, classes, assuntos, orgaos, graus e movimentos padronizados. Ate agora nao se confirmou como fonte textual principal.

## 8. Notebooks e papel de cada um

Leia `docs/NOTEBOOK_GUIDE.md` para detalhes, mas a visao resumida e:

- `00_download_stj_metadados.ipynb`: baixa JSONs `metadados*`.
- `00b_download_stj_textos.ipynb`: baixa ZIPs de textos e normaliza nomes para `textos<aaaammdd>.zip`.
- `01_exploracao_stj_metadados.ipynb`: EDA principal dos metadados; gera os CSVs e Markdown em `reports/summaries`.
- `02_validacao_integras_txt.ipynb`: smoke test de um lote JSON + ZIP usando `SeqDocumento`.
- `03_analise_textual_inicial.ipynb`: analise de amostra textual gerada pelo `02`.
- `04_parse_tabela_assuntos.ipynb`: gera lookup de assuntos.
- `05_eda_avancada_stj.ipynb`: EDA mais completa/visual em Matplotlib.
- `06_ciclo_vida_processual_stj.ipynb`: experimental; tenta construir espinha dorsal processual.
- `07_documentos_por_processo_stj.ipynb`: experimental/pesado; processa multiplos ZIPs e gera documento-texto.
- `08_apresentacao_eda_stj.ipynb`: notebook visual para apresentacao de 30 minutos.

## 9. Estado dos notebooks mais importantes

### Notebook 01

Confiavel para EDA documental. Deve ser rerodado quando mudar:

- recorte de anos;
- lookup de assuntos;
- regra de coalescencia de ministro/relator;
- metadados baixados.

### Notebook 08

Bom para apresentacao. Usa outputs do `01` e deve ser interpretado como EDA documental STJ, nao vida processual final.

### Notebook 06

Experimental. Se `process_spine` aparecer com zero processos, isso nao invalida o corpus; apenas indica que a ligacao CNJ/registro/processo ainda nao esta resolvida.

### Notebook 07

Experimental e potencialmente pesado. Antes de rodar completo, testar com:

```python
ANOS_ANALISE = [2024, 2025, 2026]
MAX_LOTES = 2
MAX_DOCUMENTOS = 500
GERAR_TEXTO_POR_PROCESSO = False
```

Depois ampliar gradualmente.

## 10. Como orientar uma apresentacao ao professor

Mensagem central:

> Esta etapa nao entrega uma conclusao juridica final; ela mostra que o corpus STJ 2024-2026 e grande, estruturavel e promissor, mas que a pesquisa depende de uma chave processual bem construida.

Roteiro recomendado:

1. Escopo: EDA documental STJ, nao vida processual completa.
2. Escala: mais de 1,5 milhao de documentos.
3. Temporalidade: 2024-2026, com 2026 parcial.
4. Composicao: decisoes e acordaos.
5. Teor e recursos: predominancia de filtros/negativas/nao conhecimento.
6. Relatoria: concentracao documental, com cautela.
7. Assuntos: concentracao por codigos; nomes provisórios.
8. Limite: falta consolidar documento -> registro STJ -> CNJ -> trajetoria.
9. Proximo passo: integrar Espelhos de Acordaos, Movimentacao Processual e outras instancias.

Perguntas provaveis e respostas:

- Isso reconstrói a vida do processo?
  - Ainda nao. A EDA atual descreve documentos STJ. A vida processual e a proxima camada.

- Por que nao usar apenas CNJ?
  - Porque nos metadados de integras a chave mais estavel parece ser `numeroRegistro`/`processo`; o CNJ precisa de normalizacao e cruzamento.

- Assuntos sao de qual instancia?
  - Os codigos vêm dos metadados STJ; os rotulos atuais usam lookup auxiliar e precisam ser ampliados.

- Ministro e confiavel?
  - Apos coalescer `ministro`, `NM_MINISTRO` e `relator`, e informativo para documentos STJ, mas nao equivale a produtividade completa.

## 11. Diretrizes para proximas tarefas

Priorize:

1. Documentar e estabilizar a EDA atual.
2. Criar pipeline para Espelhos de Acordaos.
3. Unir Integras + Espelhos por `numeroRegistro` e/ou `numeroProcesso`.
4. Melhorar a camada de vida processual no STJ com Atas e Movimentacao Processual.
5. Depois, pensar em outras instancias/DataJud.
6. So depois formular experimentos com LLM.

Nao priorizar ainda:

- fine-tuning;
- benchmarking final de LLM;
- aplicacao web;
- automacao de Selenium;
- conclusoes de vies;
- afirmacoes sobre causalidade.

## 12. Regras de cuidado metodologico

- Nunca contar documentos como se fossem processos sem declarar a unidade.
- Nunca tratar primeira aparicao no corpus como data de origem do processo.
- Nunca tratar lookup de assuntos de uma instancia como cobertura completa de todas as instancias.
- Nunca inferir produtividade de ministro sem validar campo, cobertura e unidade de contagem.
- Manter dados brutos preservados.
- Preferir outputs derivados em `data/processed` e `data/reports`.
- Em notebooks pesados, parametrizar amostras antes de rodar tudo.

## 13. Primeira mensagem recomendada para um novo chat

Cole algo assim:

```text
Estou na branch transicao/stj-eda-pipeline do repo datajud_probe.
Leia README.md, docs/NOTEBOOK_GUIDE.md e CODEX_PROMPT.md primeiro.
Quero continuar uma pesquisa de mestrado sobre LLMs, conhecimento institucional e decisões jurídicas com dados públicos do STJ/DataJud.
A EDA atual é documental, com recorte 2024-2026, e não deve ser confundida com vida processual completa.
Meu próximo objetivo é conectar a análise exploratória do corpus STJ ao desenho da dissertação, planejando a integração com Espelhos de Acórdãos, Movimentação Processual e, futuramente, outras instâncias.
```
