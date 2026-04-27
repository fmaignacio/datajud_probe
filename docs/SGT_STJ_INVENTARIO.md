# Inventario SGT/STJ

Este arquivo foi gerado por `scripts/extract_stj_sgt.py` a partir dos documentos colocados em `docs/`.

Os arquivos `78_Tabela_*.sql` e `78_Tabela_*.xls` sao exports HTML; os arquivos `dump_*.sql` sao dumps MySQL do schema `sgt_consulta`.

## Fontes HTML lidas

- `78_Tabela_Assuntos_Impressao_STJ.sql`: 7,984,193 bytes
- `78_Tabela_Classes.sql`: 1,164,161 bytes
- `78_Tabela_Documentos_Processuais_Impressao.sql`: 1,320,194 bytes
- `78_Tabela_Movimentos_Impressao_STJ.xls`: 1,032,364 bytes
- `78_Tabela_Movimentos_STJ.sql`: 1,223,478 bytes

## Saidas geradas

- `assuntos`: `data/reference/sgt_stj/processed/sgt_stj_assuntos.csv`
- `assuntos` parquet: `data/reference/sgt_stj/processed/sgt_stj_assuntos.parquet`
- `classes`: `data/reference/sgt_stj/processed/sgt_stj_classes.csv`
- `classes` parquet: `data/reference/sgt_stj/processed/sgt_stj_classes.parquet`
- `documentos`: `data/reference/sgt_stj/processed/sgt_stj_documentos.csv`
- `documentos` parquet: `data/reference/sgt_stj/processed/sgt_stj_documentos.parquet`
- `movimentos`: `data/reference/sgt_stj/processed/sgt_stj_movimentos.csv`
- `movimentos` parquet: `data/reference/sgt_stj/processed/sgt_stj_movimentos.parquet`

## Resumo dos vocabulários STJ

| vocabulario   |   linhas |   codigos_unicos |   raizes_sem_pai |   nivel_maximo_visual |   com_alteracao |   inativos |   com_glossario |
|:--------------|---------:|-----------------:|-----------------:|----------------------:|----------------:|-----------:|----------------:|
| assuntos      |     3292 |             3292 |               18 |                     5 |             360 |          1 |            2925 |
| classes       |      137 |              137 |                4 |                     5 |              38 |          0 |             109 |
| documentos    |     1370 |             1370 |                1 |                     6 |              31 |          0 |               0 |
| movimentos    |      656 |              656 |                1 |                     5 |             124 |          0 |             529 |

## Dump MySQL

Tabelas declaradas em `dump_estrutura.sql`: `itens`, `documento_processual`, `classes`, `assuntos`, `movimentos`, `tipo_complemento`, `complemento`, `complemento_movimento`, `complemento_tabelado`, `procedimento_complementos`, `temporariedade`, `tipo_ramo_justica`, `temp_item`, `objetivo_desenvolvimento_sustentavel`, `assunto_ods`.

Contagem de inserts em `dump_dados.sql`:

- `assunto_ods`: 7,715 inserts
- `assuntos`: 5,187 inserts
- `classes`: 842 inserts
- `complemento`: 62 inserts
- `complemento_movimento`: 359 inserts
- `complemento_tabelado`: 369 inserts
- `documento_processual`: 996 inserts
- `itens`: 8,782 inserts
- `movimentos`: 943 inserts
- `objetivo_desenvolvimento_sustentavel`: 17 inserts
- `procedimento_complementos`: 78 inserts
- `temp_item`: 48,375 inserts
- `temporariedade`: 96 inserts
- `tipo_complemento`: 3 inserts
- `tipo_ramo_justica`: 9 inserts

## Observacoes uteis

- `codigo` e `codigo_pai` permitem reconstruir hierarquias de assuntos, classes, documentos e movimentos.
- `tipo_item` segue a codificacao do SGT: `A` assunto, `C` classe, `D` documento processual, `M` movimento.
- Os exports HTML do STJ sao subconjuntos/visoes de impressao; o dump MySQL contem tambem tabelas auxiliares, complementos, ODS e temporariedade.
- Para enriquecer a EDA do STJ, os arquivos mais imediatamente uteis sao `sgt_stj_assuntos.parquet`, `sgt_stj_classes.parquet` e `sgt_stj_movimentos.parquet`.

## Assuntos

- Linhas extraidas: 3,292
- Coluna de rotulo principal: `assunto`
- Colunas: assunto, codigo, codigo_pai, dispositivo_legal, artigo, ods, data_publicacao, data_alteracao, data_inativacao, data_reativacao, glossario, nivel_visual, tipo_item, fonte, caminho_codigos, caminho_rotulos

Amostra inicial:

|   codigo |   codigo_pai | assunto                                             | caminho_rotulos                                                           |
|---------:|-------------:|:----------------------------------------------------|:--------------------------------------------------------------------------|
|    12795 |        12775 | Acesso                                              | 12775 > Acesso                                                            |
|    12805 |        12795 | Acesso sem Conclusão do Ensino Médio                | 12775 > Acesso > Acesso sem Conclusão do Ensino Médio                     |
|    14177 |        12795 | Ciência Sem Fronteiras                              | 12775 > Acesso > Ciência Sem Fronteiras                                   |
|    12808 |        12795 | Cobrança de Taxa de Matrícula                       | 12775 > Acesso > Cobrança de Taxa de Matrícula                            |
|    12806 |        12795 | Convalidação de Estudos e Reconhecimento de Diploma | 12775 > Acesso > Convalidação de Estudos e Reconhecimento de Diploma      |
|    12809 |        12795 | Cota para Ingresso - Ações Afirmativas              | 12775 > Acesso > Cota para Ingresso - Ações Afirmativas                   |
|    12810 |        12795 | Itinerários Formativos                              | 12775 > Acesso > Itinerários Formativos                                   |
|    12910 |        12810 | Formação Técnica e Profissional                     | 12775 > Acesso > Itinerários Formativos > Formação Técnica e Profissional |

## Classes

- Linhas extraidas: 137
- Coluna de rotulo principal: `classe`
- Colunas: classe, codigo, codigo_pai, dispositivo_legal, artigo, sigla, alteracoes, glossario, data_publicacao, data_alteracao, data_inativacao, data_reativacao, tipo_procedimento, originario_recursal, criminal, nivel_visual, tipo_item, fonte, caminho_codigos, caminho_rotulos

Amostra inicial:

|   codigo |   codigo_pai | classe                                          | caminho_rotulos                                       |
|---------:|-------------:|:------------------------------------------------|:------------------------------------------------------|
|    12729 |          385 | Execução de Medidas Alternativas no Juízo Comum | 385 > Execução de Medidas Alternativas no Juízo Comum |
|    12727 |          385 | Execução de Pena de Multa                       | 385 > Execução de Pena de Multa                       |
|    12728 |          385 | Transferência Entre Estabelecimentos Penais     | 385 > Transferência Entre Estabelecimentos Penais     |
|    12248 |         1198 | Pedido de Cooperação Judiciária                 | 1198 > Pedido de Cooperação Judiciária                |
|     1299 |         1198 | Recurso Administrativo                          | 1198 > Recurso Administrativo                         |
|      256 |         1198 | Representação por Excesso de Prazo              | 1198 > Representação por Excesso de Prazo             |
|     1385 |          547 | Seção Cível                                     | 547 > Seção Cível                                     |
|     1386 |         1385 | Processo de Conhecimento                        | 547 > Seção Cível > Processo de Conhecimento          |

## Documentos

- Linhas extraidas: 1,370
- Coluna de rotulo principal: `documento`
- Colunas: documento, codigo, codigo_pai, data_publicacao, data_alteracao, data_inativacao, data_reativacao, nivel_visual, tipo_item, fonte, caminho_codigos, caminho_rotulos

Amostra inicial:

|   codigo |   codigo_pai | documento                      | caminho_rotulos                                                 |
|---------:|-------------:|:-------------------------------|:----------------------------------------------------------------|
|        3 |            1 | Ações processuais              | 1 > Ações processuais                                           |
|       11 |            3 | Acordo                         | 1 > Ações processuais > Acordo                                  |
|      143 |           11 | Acordo (Outros)                | 1 > Ações processuais > Acordo > Acordo (Outros)                |
|    14274 |           11 | Acordo de Divórcio             | 1 > Ações processuais > Acordo > Acordo de Divórcio             |
|      142 |           11 | Acordo de Não-Persecução Penal | 1 > Ações processuais > Acordo > Acordo de Não-Persecução Penal |
|    14307 |           11 | Acordo Extrajudicial           | 1 > Ações processuais > Acordo > Acordo Extrajudicial           |
|    14275 |           11 | Acordo Resp. Parentais         | 1 > Ações processuais > Acordo > Acordo Resp. Parentais         |
|        7 |            3 | Aditamento                     | 1 > Ações processuais > Aditamento                              |

## Movimentos

- Linhas extraidas: 656
- Coluna de rotulo principal: `movimento_nome`
- Colunas: movimento_nome, codigo, codigo_pai, complemento, movimento, visibilidade_externa, dispositivo_legal, artigo, alteracoes, glossario, data_publicacao, data_alteracao, data_inativacao, data_reativacao, nivel_visual, tipo_item, fonte, caminho_codigos, caminho_rotulos

Amostra inicial:

|   codigo |   codigo_pai | movimento_nome                                 | caminho_rotulos                                                 |
|---------:|-------------:|:-----------------------------------------------|:----------------------------------------------------------------|
|    15185 |            1 | Cooperação Judiciária                          | 1 > Cooperação Judiciária                                       |
|        3 |            1 | Decisão                                        | 1 > Decisão                                                     |
|    15162 |            3 | Acolhimento de Embargos de Declaração          | 1 > Decisão > Acolhimento de Embargos de Declaração             |
|      133 |            3 | Acolhimento de exceção                         | 1 > Decisão > Acolhimento de exceção                            |
|      335 |          133 | de pré-executividade                           | 1 > Decisão > Acolhimento de exceção > de pré-executividade     |
|      940 |          133 | Impedimento ou Suspeição                       | 1 > Decisão > Acolhimento de exceção > Impedimento ou Suspeição |
|      371 |          133 | Incompetência                                  | 1 > Decisão > Acolhimento de exceção > Incompetência            |
|    15163 |            3 | Acolhimento em Parte de Embargos de Declaração | 1 > Decisão > Acolhimento em Parte de Embargos de Declaração    |

