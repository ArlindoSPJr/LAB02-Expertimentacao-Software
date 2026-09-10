# Hipóteses e Métricas do Experimento

Este documento cobre a parte de **hipóteses (H0/H1)** e **métricas** do Passo 1 — Desenho do Experimento (`docs/enunciado.md`): as questões de pesquisa RQ1–RQ3 já estão fixadas pelo enunciado; aqui formalizamos as hipóteses estatísticas correspondentes, as variáveis do experimento e a escolha (com justificativa) das métricas usadas para respondê-las, dentre as candidatas listadas no GQM. Ameaças à validade ficam em documento separado.

Convenção adotada: para cada RQ, **H0** afirma que o uso do assistente de IA (Claude Code) **não tem efeito** sobre a variável dependente correspondente (mediana das diferenças pareadas igual a zero); **H1** afirma apenas que **há efeito** (diferença), sem presumir a direção — a hipótese não deve conter a resposta da RQ, só a afirmação testável de que existe diferença entre os tratamentos. Qual tratamento é melhor é uma conclusão da análise (S03), não uma premissa do desenho. Como o desenho é within-subject/pareado, as hipóteses são testadas sobre a **diferença por par** (mesmo integrante, mesmo kata, tratamento com IA vs. sem IA), com teste de Wilcoxon signed-rank **bilateral**.

## 1. Hipóteses

### RQ1 — Tempo

> O uso de assistente de IA reduz o tempo necessário para resolver uma tarefa de programação?

- **H0₁:** não há diferença na mediana do tempo até passar todos os testes de aceitação (time-to-green) entre os tratamentos com IA e sem IA.
- **H1₁:** há diferença na mediana do tempo até passar todos os testes de aceitação entre os tratamentos com IA e sem IA.

Trials que atingem o time-box de 35 min sem sucesso são registrados como **censurados em 35 min** (não descartados) — a hipótese é testada sobre esse valor, o que torna o teste conservador a favor de H0 quando um tratamento tem mais censuras.

### RQ2 — Defeitos

> O uso de assistente de IA reduz a quantidade de defeitos (testes que falham) no código produzido?

- **H0₂:** não há diferença na mediana da taxa de sucesso dos testes de aceitação (% de testes passando ao final do time-box) entre os tratamentos com IA e sem IA.
- **H1₂:** há diferença na mediana da taxa de sucesso dos testes de aceitação entre os tratamentos com IA e sem IA.

### RQ3 — Estrutura do código

> O uso de assistente de IA altera a complexidade ciclomática ou a duplicação do código produzido?

Como a RQ3 cobre duas propriedades estruturais distintas, ela é tratada como duas sub-hipóteses independentes, ambas normalizadas por LOC (métrica de controle, ver seção 3):

- **H0₃ₐ:** não há diferença na complexidade ciclomática média (WMC/CK) entre os tratamentos com IA e sem IA.
- **H1₃ₐ:** a complexidade ciclomática média difere entre os tratamentos com IA e sem IA.
- **H0₃ᵦ:** não há diferença no percentual de linhas duplicadas (PMD-CPD) entre os tratamentos com IA e sem IA.
- **H1₃ᵦ:** há diferença no percentual de linhas duplicadas entre os tratamentos com IA e sem IA.

Para RQ3 a ausência de direção em H1 é ainda mais natural que em RQ1/RQ2: não há uma direção esperada a priori — código gerado com apoio de IA pode ser mais verboso e repetitivo (aumentando duplicação) ou mais organizado (reduzindo complexidade) —, e o enunciado trata a RQ3 como exploratória.

## 2. Variáveis do Experimento

### 2.1 Variável independente

| Variável | Tipo | Níveis |
|---|---|---|
| Uso de assistente de IA (Claude Code) | Categórica binária, manipulada | `com-ia` / `manual` |

### 2.2 Variáveis dependentes

| Variável | Operacionalização | RQ |
|---|---|---|
| Tempo até time-to-green | Segundos do início do trial até todos os testes de aceitação passarem, ou 35 min (2100 s) se censurado | RQ1 |
| Censura do trial | Booleano: `true` se o trial atingiu o time-box sem passar todos os testes | RQ1 |
| Taxa de sucesso dos testes | `testes_passando / testes_total` ao final do trial | RQ2 |
| Nº de testes falhando | `testes_total − testes_passando` ao final do trial | RQ2 (complementar) |
| Complexidade ciclomática (WMC) | Soma/média de complexidade ciclomática McCabe por classe, via CK | RQ3 |
| % de linhas duplicadas | Linhas duplicadas / total de linhas, via PMD-CPD | RQ3 |
| LOC | Linhas de código do trial final (CK ou contagem própria) | RQ3 (controle) |

Todas as variáveis dependentes são coletadas por trial (kata × tratamento × integrante), conforme os campos já definidos em `docs/scripts-metricas.md`.

## 3. Métricas escolhidas

O enunciado lista métricas candidatas por RQ e deixa a cada grupo escolher e justificar. Adotamos as métricas **primárias/recomendadas** em cada caso, deixando as opcionais fora do escopo obrigatório (ver observações):

| RQ | Métrica adotada | Ferramenta/fonte | Justificativa |
|---|---|---|---|
| RQ1 | Time-to-green (mediana por tratamento) | Script de cronometragem (Python) | Métrica primária recomendada pelo enunciado; mediana em vez de média por causa do N pequeno (4–6 trials/integrante) e sensibilidade da média a outliers/censuras |
| RQ2 | Taxa de sucesso (% testes passando) | Saída do `mvn test` (Surefire), extraída pelo script de cronometragem | Recomendada como mais robusta que a contagem bruta, pois normaliza katas com números diferentes de testes de aceitação |
| RQ2 | Nº absoluto de testes falhando | Idem | Métrica complementar, mais simples de reportar e de interpretar caso a caso |
| RQ3 | WMC (complexidade ciclomática somada/média por classe) | CK | Única ferramenta de complexidade citada para Java no enunciado |
| RQ3 | % de linhas duplicadas | PMD-CPD | Ferramenta de duplicação citada para Java no enunciado |
| RQ3 | LOC | CK (ou contagem própria) | **Obrigatória** sempre que WMC/duplicação forem reportados — controla o efeito de verbosidade (código gerado por IA pode ser mais extenso) |

**Métricas opcionais do enunciado, não adotadas nesta iteração** (podem ser revisitadas na discussão qualitativa do Relatório Final, mas não fazem parte da coleta obrigatória nem das hipóteses acima):
- Nº de prompts/interações com a IA por trial (RQ1) — não obrigatória; se registrada, é só para discussão qualitativa, sem hipótese estatística associada.
- Densidade de defeitos (testes falhando / KLOC) (RQ2) — útil apenas se os katas tiverem tamanhos muito diferentes entre si, o que não é o caso aqui (katas de dificuldade equivalente, ver `docs/katas.md`).
- Índice de Manutenibilidade — Maintainability Index (RQ3, via Radon `mi`) — não se aplica: o experimento usa Java (CK/PMD), não Python/Radon.

## 4. Agregação e testes estatísticos

Consistente com o desenho within-subject e o N pequeno:

- **Estatística descritiva:** mediana e IQR (intervalo interquartil) por tratamento, para todas as variáveis dependentes acima — nunca média/desvio-padrão como estatística principal.
- **Estatística inferencial:** teste de Wilcoxon signed-rank (pareado, **bilateral**), aplicado sobre a diferença por par (mesmo integrante, mesmo kata, com IA vs. sem IA) para cada uma das quatro hipóteses (H1₁, H1₂, H1₃ₐ, H1₃ᵦ). O teste bilateral é consistente com H1 não-direcional (seção 1): a análise da S03 reporta o p-valor e, separadamente, o sinal da mediana das diferenças — é aí, e não no desenho, que se conclui qual tratamento teve o melhor resultado. Teste executado sobre os dados consolidados pelos scripts da S01/S02.

## Referências

- `docs/enunciado.md` — RQs, GQM e métricas candidatas originais
- `docs/entendimento-e-planejamento.md` — entendimento geral do trabalho
- `docs/ambiente-experimento.md` — ambiente fixado do experimento
- `docs/scripts-metricas.md` — campos brutos coletados pelos scripts (fonte das métricas acima)
- `docs/ameacas-validade.md` — ameaças à validade (issue separada)
