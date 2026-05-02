# 07 — Rastreabilidade de Resultados

> Relacione hipótese, experimento, saída técnica e seção da dissertação.

| Hipótese/Pergunta | Experimento (ID) | Saída técnica (arquivo/tabela) | Evidência principal | Seção alvo da dissertação |
|---|---|---|---|---|
| Ex.: STJ é corpus semântico viável? | EXP-... | data/processed/... | cobertura, completude, amostra textual | Fontes e método |
| Ex.: unidade por processo melhora análise? | EXP-... | stj_process_events.parquet | consistência temporal e integridade de chaves | Método |
| Ex.: há padrão de divergência LLM? | EXP-... | relatório comparativo | distâncias de desfecho/argumento | Resultados e discussão |

## Regras de preenchimento
1. Cada linha deve apontar para ao menos um artefato versionado.
2. Cada evidência deve ter referência a commit.
3. Não registrar inferência sem evidência associada.
