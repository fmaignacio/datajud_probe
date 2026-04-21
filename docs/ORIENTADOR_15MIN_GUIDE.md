# Guia de Apresentacao ao Orientador - 15 minutos

Este guia serve para uma apresentacao curta ao orientador sobre o estado atual da pesquisa com dados STJ/DataJud. A apresentacao deve usar principalmente o notebook `notebooks/08_apresentacao_eda_stj.ipynb`.

## Mensagem central

> A EDA atual mostra que o corpus STJ 2024-2026 e grande, estruturavel e promissor para uma pesquisa empirica com LLMs. O principal achado metodologico e que a unidade documental esta bem capturada, mas a vida processual completa ainda exige construir uma chave de ligacao entre documento, registro STJ, CNJ, movimentacoes e possivelmente outras instancias.

Em outras palavras: a reuniao nao deve vender uma conclusao juridica final. Deve mostrar que a base e viavel e que os proximos gargalos metodologicos estao identificados.

## Objetivo da apresentacao

Em 15 minutos, o objetivo e responder quatro perguntas:

1. Qual e a fonte de dados escolhida e por que ela e promissora?
2. Qual e a escala e composicao do corpus?
3. Quais concentracoes iniciais aparecem nos metadados?
4. O que falta para conectar essa EDA ao desenho da dissertacao?

## Roteiro minuto a minuto

### 0:00-1:30 - Escopo da conversa

Diga algo como:

> Hoje eu nao vou apresentar ainda uma analise final de decisoes ou de vies de LLM. Vou apresentar a EDA do corpus STJ 2024-2026 e explicar por que ela parece uma boa base para a etapa empirica da dissertacao.

Pontos importantes:

- Unidade atual: documento STJ (`SeqDocumento`).
- Unidade futura desejada: processo/trajetoria processual.
- Recorte atual: 2024-2026.

Notebook sugerido:

- `08_apresentacao_eda_stj.ipynb`, secao **Escopo e unidade de analise**.

### 1:30-4:00 - Escala do corpus

Mostrar o grafico de KPIs:

- 551 arquivos de origem;
- 1,54 milhao de documentos;
- aproximadamente 1,1 milhao de processos/registros unicos;
- 1,53 milhao de `SeqDocumento` unicos.

Fala sugerida:

> O primeiro resultado importante e de escala. A base e grande o suficiente para uma pesquisa empirica robusta, mas a escala tambem obriga a separar documento, registro e processo. Se eu contar documentos como processos, a analise fica errada.

Figura:

- `data/reports/figures/apresentacao_eda/01_kpis_corpus.png`

### 4:00-6:00 - Cobertura temporal

Mostrar documentos por ano e, se houver tempo, por mes.

Pontos:

- 2025 e o ano mais volumoso.
- 2024 tambem tem grande cobertura.
- 2026 e parcial, entao nao deve ser comparado como ano fechado.

Fala sugerida:

> O recorte tem boa cobertura em 2024 e 2025. O ano de 2026 ainda esta em andamento/parcial, entao eu trato como recorte parcial, nao como queda substantiva.

Figuras:

- `02_documentos_por_ano.png`
- `03_documentos_por_mes.png`, se houver tempo.

### 6:00-8:30 - Composicao documental e teor

Mostrar tipo documental e teor.

Pontos:

- Predominancia de `DECISAO`.
- `ACORDAO` e menor em volume, mas juridicamente mais rico.
- Teores mais frequentes: `Nao Conhecendo` e `Negando`.

Fala sugerida:

> A base parece muito marcada pela funcao recursal/filtro do STJ. Grande parte dos documentos esta associada a decisoes e a resultados como nao conhecimento ou negativa. Isso e relevante para pensar o experimento com LLM, porque o corpus nao e uma colecao neutra de casos; ele expressa uma pratica institucional especifica.

Figura:

- `04_tipo_e_teor.png`

### 8:30-10:00 - Recursos e relatoria

Mostrar recursos e relatoria, rapidamente.

Pontos:

- Recursos frequentes: `AgInt`, `EDcl`, `AgRg`.
- O campo de relatoria foi corrigido combinando `ministro`, `NM_MINISTRO` e `relator`.
- Nao apresentar como produtividade judicial completa.

Fala sugerida:

> Depois da correcao dos metadados, o campo de relatoria passou a ser informativo. Ainda assim, eu trato isso como concentracao documental nos metadados do STJ, nao como medida de produtividade ou desempenho de gabinete.

Figuras:

- `05_recursos.png`
- `06_ministros_preenchidos.png`

Se o tempo estiver curto, mostrar apenas recursos e mencionar relatoria oralmente.

### 10:00-12:00 - Assuntos e concentracao tematica

Mostrar top assuntos.

Pontos:

- Forte presenca de temas penais: trafico de drogas, homicidio qualificado, roubo majorado, prisao preventiva.
- Tambem aparecem civil, consumidor, tributario.
- Os codigos de assunto vêm dos metadados STJ.
- Os nomes textuais atuais vêm de lookup auxiliar, inicialmente da Justica Federal de 1º Grau, portanto sao rotulos provisorios.

Fala sugerida:

> Aqui eu tenho uma leitura tematica inicial. O que e mais seguro afirmar e a concentracao dos codigos de assunto. Os rotulos textuais ajudam a interpretar, mas ainda preciso ampliar o lookup para nao depender apenas da tabela da Justica Federal de 1º Grau.

Figura:

- `07_top_assuntos.png`

Nao insistir em `instancia`. A fonte atual de rotulos nao prova cobertura multi-instancia.

### 12:00-14:00 - Limite metodologico e proximo passo

Mostrar a secao de limite da ligacao processual.

Pontos:

- A EDA documental esta forte.
- A vida processual completa ainda nao esta resolvida.
- Proxima etapa: construir ligacao documento -> registro STJ -> CNJ -> movimentacoes -> outras instancias.
- Espelhos de Acordaos sao uma fonte promissora para relator, orgao julgador, ementa, tese juridica e referencias.

Fala sugerida:

> O gargalo principal agora nao e apenas baixar texto. E construir uma unidade processual confiavel. Para a dissertacao, isso e importante porque a comparacao com LLM precisa estar ancorada em casos juridicos bem definidos, e nao em documentos soltos.

Figura:

- `09_limite_ciclo_vida.png`

### 14:00-15:00 - Fechamento

Fechar com tres conclusoes:

1. O corpus STJ 2024-2026 e viavel e grande.
2. A EDA revela concentracoes documentais, decisorias e tematicas.
3. A etapa critica seguinte e metodologica: consolidar a unidade processual e enriquecer com Espelhos de Acordaos/Movimentacao.

Fala final sugerida:

> Meu entendimento agora e que a base STJ e um bom ponto de partida para a etapa empirica da dissertacao, mas a pergunta de pesquisa precisa respeitar essa arquitetura: primeiro caracterizar documentos e decisoes; depois reconstruir trajetorias processuais; so entao comparar com respostas de LLM.

## O que mostrar se o tempo apertar

Prioridade maxima:

1. Escopo e unidade de analise.
2. KPIs do corpus.
3. Tipo documental + teor.
4. Top assuntos.
5. Limite metodologico/proximos passos.

Pular se necessario:

- grafico mensal;
- relatoria detalhada;
- assuntos raiz.

## O que nao prometer

Nao dizer:

- que a vida processual completa ja foi reconstruida;
- que a base cobre todas as instancias;
- que os assuntos estao rotulados por uma tabela universal completa;
- que relatoria equivale a produtividade de ministro;
- que ja ha resultado sobre vies de LLM;
- que DataJud sera o corpus textual principal.

Dizer em vez disso:

- a EDA documental esta consolidada;
- a unidade de processo ainda esta em construcao;
- os rotulos de assunto sao auxiliares;
- o proximo passo e integrar bases complementares.

## Perguntas provaveis e respostas curtas

### Isso ja responde sua pergunta de mestrado?

Ainda nao. Responde uma etapa anterior: se existe um corpus publico, grande e estruturavel para sustentar a pergunta empirica.

### Por que STJ?

Porque o STJ oferece metadados e textos integrais em lote, com chave documental (`SeqDocumento`) e campos juridicos relevantes. DataJud e util para metadados/movimentos, mas nao se mostrou a melhor fonte textual.

### A unidade e processo ou documento?

Neste momento, documento. A unidade futura desejada e processo/trajetoria. Essa distincao e um dos principais achados metodologicos da EDA.

### Por que aparecem tantos documentos e tantos processos?

Porque o corpus e documental e contem decisoes/acordaos publicados. Um processo pode aparecer em multiplos documentos, recursos e publicacoes. Por isso a etapa de deduplicacao/process spine e critica.

### O campo ministro e confiavel?

Ele ficou mais informativo depois de combinar `ministro`, `NM_MINISTRO` e `relator`. Mesmo assim, deve ser interpretado como relatoria nos documentos STJ, nao produtividade ou comportamento individual final.

### Os assuntos sao de qual instancia?

Os codigos vêm dos metadados STJ. Os nomes textuais atuais vêm de lookup auxiliar; no momento, a fonte local inicial e da Justica Federal de 1º Grau. Portanto, os nomes ajudam a ler, mas ainda nao representam cobertura completa de instancias.

### Onde entram os Espelhos de Acordaos?

Como proxima camada de enriquecimento. Eles trazem relator, orgao julgador, ementa, decisao, tese juridica, tema, jurisprudencia citada e referencias legislativas. Isso parece muito promissor para ligar a EDA documental ao conteudo juridico substantivo.

### Onde entram outras instancias?

Na reconstrucao da trajetoria processual. Primeiro e preciso estabilizar documento -> registro STJ -> CNJ. Depois, usar DataJud e bases dos tribunais de origem para mapear o caminho anterior ao STJ.

## Slide mental unico

Se fosse resumir tudo em uma frase para orientar a conversa:

> Eu ja tenho um corpus documental STJ grande e analisavel; agora preciso transformar esse corpus em casos/processos bem definidos para que a comparacao futura com LLM seja metodologicamente defensavel.

## Arquivos de apoio

- `notebooks/08_apresentacao_eda_stj.ipynb`
- `data/reports/figures/apresentacao_eda/`
- `data/reports/summaries/metadata_eda_summary.md`
- `docs/NOTEBOOK_GUIDE.md`
- `CODEX_PROMPT.md`
