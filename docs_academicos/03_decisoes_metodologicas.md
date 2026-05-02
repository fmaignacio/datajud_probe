# 03 — Decisões Metodológicas

> Registro formal de decisões para preservar memória metodológica.

## Template

### DM-AAAA-MM-DD-XX — Título curto
- **Data (UTC):**
- **Status:** proposta | aprovada | revisada | descartada
- **Decisão:**
- **Justificativa:**
- **Alternativas consideradas:**
- **Impacto no desenho da pesquisa:**
- **Impacto em métricas/avaliação:**
- **Risco introduzido:**
- **Como mitigar:**
- **Relaciona-se a experimentos:**
- **Relaciona-se a achados:**

---

## Decisões registradas

### DM-2026-05-02-001 — Comparar divergência, não erro
- **Data (UTC):** 2026-05-02
- **Status:** aprovada
- **Decisão:** não tratar decisão institucional como ground truth absoluto; comparar padrões de divergência.
- **Justificativa:** decisões jurídicas não são determinísticas e exigem leitura contextual.
- **Alternativas consideradas:** modelar avaliação como “acerto/erro” binário.
- **Impacto no desenho da pesquisa:** foco em distância argumentativa, consistência e sensibilidade a prompt.
- **Impacto em métricas/avaliação:** métricas de divergência, estabilidade e severidade relativa.
- **Risco introduzido:** aumento de complexidade analítica.
- **Como mitigar:** protocolos claros de anotação e critérios explícitos de comparação.
- **Relaciona-se a experimentos:** EXP-*
- **Relaciona-se a achados:** 02_achados_codex.md
