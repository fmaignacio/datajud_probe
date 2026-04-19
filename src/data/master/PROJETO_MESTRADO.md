# Documento de Ideia do Projeto de Mestrado

## 1. Título provisório

**Governança epistêmica de LLMs no setor público brasileiro: entre conhecimento institucional, delegação cognitiva e análise exploratória de dados públicos**

## 2. Situação atual do projeto

O projeto ainda não está fechado. Ele está em fase exploratória e deve priorizar pesquisa, leitura, validação de fontes e refinamento metodológico antes de consolidar o recorte final.

A ideia central é investigar como LLMs podem afetar a produção, validação e uso do conhecimento institucional no setor público brasileiro.

A hipótese teórica provisória é que LLMs podem operar como forma implícita de delegação cognitiva, alterando práticas de validação, confiança e autoridade epistêmica.

Entretanto, após conversa com o orientador, ficou claro que o projeto não deve permanecer excessivamente teórico. É necessário construir um caminho mais técnico, objetivo e executável, preferencialmente com dados públicos.

## 3. Formulação teórica provisória

### Pergunta teórica

Como o uso de LLMs em contextos institucionais reconfigura a produção, a validação e o uso do conhecimento institucional no setor público brasileiro?

### Hipótese teórica

LLMs podem funcionar como forma implícita de delegação cognitiva, alterando práticas de validação, confiança e autoridade epistêmica.

## 4. Formulação empírica provisória

### Pergunta empírica

Como saídas geradas por LLMs diferem de decisões humanas institucionais em casos jurídicos estruturados com dados públicos?

### Hipótese empírica

LLMs tenderão a divergir de decisões humanas institucionais de forma não aleatória, revelando padrões de simplificação, sensibilidade à formulação do caso e possível reprodução de regularidades históricas.

## 5. Por que o campo jurídico aparece como recorte possível

O campo jurídico é promissor porque:

- há dados públicos;
- decisões são documentos institucionais formalizados;
- há textos produzidos por agentes públicos;
- há metadados estruturados;
- há possibilidade de analisar linguagem, justificativa e decisão;
- o direito público exige fundamentação e legitimidade, diferentemente de decisões privadas opacas.

O objetivo, porém, **não é afirmar que LLMs devem substituir juízes**.

O objetivo é analisar, de forma controlada, como LLMs podem divergir, simplificar ou tensionar padrões de decisão e justificativa institucional.

## 6. Principais riscos metodológicos

### Risco 1 — transformar o projeto em “LLM como juiz”

Evitar essa formulação. A pesquisa não deve assumir substituição de agentes humanos por IA.

### Risco 2 — tratar a decisão humana como verdade absoluta

O juiz ou ministro não deve ser tratado como ground truth perfeito. A comparação deve ser com a decisão institucional real, não com uma verdade jurídica absoluta.

### Risco 3 — prometer causalidade forte demais

Evitar afirmações como “LLMs introduzem viés e mudam decisões públicas” sem evidência adequada. O foco inicial deve estar em padrões, divergências e hipóteses interpretativas.

### Risco 4 — depender de fonte de dados inadequada

Os testes iniciais indicaram que algumas fontes são boas para estrutura processual, mas fracas para semântica textual.

## 7. Achados iniciais sobre fontes públicas

### DataJud

Testes iniciais indicaram que o DataJud é forte para:

- metadados processuais;
- classes;
- assuntos;
- órgãos julgadores;
- graus;
- movimentações;
- data de ajuizamento.

Porém, nos testes realizados, não apareceram campos textuais relevantes como:

- `txtEmenta`;
- `txtDecisao`;
- `relator`;
- `dataPublicacao`;
- `dataJulgamento`.

Conclusão provisória: DataJud é bom para estrutura e recorte processual, mas não deve ser tratado, por ora, como corpus semântico principal.

### TJSP

O portal do TJSP oferece filtros úteis, mas o acesso parece orientado à navegação individual e extração caso a caso em PDF.

Conclusão provisória: TJSP pode servir para amostra qualitativa pequena, mas não parece adequado como base escalável.

### STJ — Íntegras de Decisões Terminativas e Acórdãos

Esta é a fonte mais promissora até aqui para análise semântica.

Ela oferece:

- ZIP com textos integrais;
- JSON com metadados;
- CSV com dicionário;
- ligação entre metadado e texto por `SeqDocumento`.

Conclusão provisória: a base do STJ deve ser explorada como corpus semântico principal.

### STJ — Movimentação Processual

Pode ser útil como base complementar, mas parece mais orientada a fluxo processual do que a semântica textual.

## 8. Arquitetura empírica provisória

A pesquisa deve operar com fontes em camadas:

| Camada | Fonte | Função |
|---|---|---|
| Estrutural/processual | DataJud | Recorte, metadados, movimentações |
| Semântica/textual | STJ Íntegras | Corpus principal para NLP e análise semântica |
| Complementar/qualitativa | TJSP | Amostra manual, se necessário |
| Complementar/processual | STJ Movimentação | Trajetória e histórico do processo |

## 9. Possíveis caminhos de pesquisa

### Caminho A — Análise semântica exploratória

Objetivo: entender a estrutura, conteúdo e padrões semânticos da base do STJ.

Possíveis técnicas:

- limpeza de texto;
- estatísticas descritivas;
- embeddings;
- clustering;
- busca semântica;
- análise por ministro, tipo de documento, teor e assunto.

Esse é o caminho inicial recomendado.

### Caminho B — Comparação LLM versus decisão institucional

Objetivo: estruturar casos públicos e gerar respostas com LLM para comparar com decisões reais.

Possíveis análises:

- divergência de desfecho;
- divergência argumentativa;
- sensibilidade a prompt;
- consistência entre execuções;
- simplificação de raciocínio.

Esse caminho deve ser considerado apenas depois de validar a base semântica.

### Caminho C — Governança epistêmica e risco institucional

Objetivo: usar os achados empíricos para discutir implicações teóricas.

Possíveis questões:

- quando o apoio por LLM vira delegação cognitiva?
- como validar outputs de LLM em contexto público?
- como preservar justificativa reflexiva?
- que riscos epistêmicos aparecem em fluxos institucionais?

## 10. Plano imediato

A etapa atual deve ser limitada à análise exploratória da base STJ.

### Objetivos imediatos

1. baixar um pacote pequeno da base de íntegras;
2. ler metadados JSON;
3. abrir ZIP com textos integrais;
4. vincular TXT e JSON por `SeqDocumento`;
5. limpar texto minimamente;
6. gerar estatísticas descritivas;
7. avaliar viabilidade de análise semântica.

### Entregáveis imediatos

- notebook exploratório;
- relatório curto de qualidade da base;
- DataFrame amostral;
- nota metodológica;
- decisão sobre continuidade do recorte empírico.

## 11. Relação com a disciplina de Fundamentos de Sistemas de Informação

O trabalho da disciplina pode funcionar como primeiro artefato formal do projeto.

Ele pode articular:

- estado da arte sobre LLMs, governança e setor público;
- contextualização do tema em Sistemas de Informação;
- reflexão sociotécnica;
- design especulativo de cenários futuros;
- relação entre infraestrutura de IA, conhecimento institucional e risco epistêmico.

## 12. Princípio orientador

A pesquisa deve permanecer híbrida:

> A empiria existe para dar concretude à teoria; a teoria existe para impedir que a empiria vire apenas um exercício técnico.

## 13. Como o Codex deve apoiar

O Codex deve ser usado para:

- entender a estrutura do repositório;
- ajudar a criar scripts exploratórios;
- melhorar legibilidade e modularização;
- propor testes pequenos;
- documentar decisões técnicas;
- evitar complexidade desnecessária.

O Codex não deve:

- inventar conclusões acadêmicas;
- prometer viabilidade sem testar;
- criar arquitetura pesada antes da exploração;
- introduzir scraping agressivo;
- misturar protótipo exploratório com sistema de produção.
