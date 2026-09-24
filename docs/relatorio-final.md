# Relatório Final — Assistentes de IA vs. Codificação Manual: um Experimento Controlado

**Disciplina:** Laboratório de Experimentação de Software — Engenharia de Software (6º período, Noite)
**Professor(a):** Danilo Maia
**Trabalho:** LAB02 — Passo 5 (Relatório Final), conforme `docs/enunciado.md`
**Grupo:** Arlindo Junior ([@ArlindoSPJr](https://github.com/ArlindoSPJr)) · Arthur Astolfi Cardoso ([@ArthurAstolfi](https://github.com/ArthurAstolfi)) · Camila Melo Ferreiras ([@CamszMelo](https://github.com/CamszMelo))
**Repositório:** <https://github.com/ArlindoSPJr/LAB02-Expertimentacao-Software>
**GitHub Projects (quadro Kanban do grupo):**

> _[link a preencher pelo grupo]_

---

## 1. Introdução

Ferramentas de IA generativa (GitHub Copilot, ChatGPT, Claude, Gemini etc.) tornaram-se onipresentes no
desenvolvimento de software, mas boa parte do que se afirma sobre seu impacto em produtividade e qualidade
ainda é relato anedótico, não evidência controlada. Este trabalho relata um **experimento controlado,
within-subject e contrabalanceado (crossover)**, comparando o uso de um assistente de IA (Claude Code) contra
a codificação manual na resolução de seis katas de programação em Java, por três integrantes, sob time-box
fixo de 35 minutos por trial.

### 1.1 Goal (GQM)

> Analisar o uso de assistentes de IA generativa na resolução de tarefas de programação, com o propósito de
> comparar seu efeito frente à codificação manual, com respeito a tempo de resolução, qualidade funcional
> (defeitos) e qualidade estrutural do código produzido, do ponto de vista do grupo pesquisador, no contexto de
> katas de dificuldade equivalente resolvidos por estudantes de graduação sob condições controladas (crossover
> within-subject, time-boxed).

### 1.2 Questões de pesquisa e hipóteses

As três questões de pesquisa (RQ1–RQ3) são fixadas pelo enunciado; as hipóteses estatísticas correspondentes
foram formalizadas em `docs/hipoteses-e-metricas.md` (Passo 1) e são reproduzidas aqui. Em todos os casos, H0
afirma ausência de efeito do tratamento (uso de IA) sobre a variável dependente; H1 afirma apenas que **há**
diferença, sem presumir direção — qual tratamento é melhor é conclusão da análise (§3), não premissa do
desenho.

| RQ | Pergunta | H0 | H1 |
|---|---|---|---|
| **RQ1** — Tempo | O uso de assistente de IA reduz o tempo necessário para resolver uma tarefa de programação? | Não há diferença na mediana do tempo até *time-to-green* entre com-IA e manual | Há diferença na mediana do tempo até *time-to-green* entre com-IA e manual |
| **RQ2** — Defeitos | O uso de assistente de IA reduz a quantidade de defeitos (testes que falham) no código produzido? | Não há diferença na mediana da taxa de sucesso dos testes de aceitação entre com-IA e manual | Há diferença na mediana da taxa de sucesso dos testes de aceitação entre com-IA e manual |
| **RQ3a** — Complexidade | O uso de IA altera a complexidade ciclomática do código produzido? | Não há diferença na complexidade ciclomática média (WMC/CK) entre com-IA e manual | Há diferença na complexidade ciclomática média entre com-IA e manual |
| **RQ3b** — Duplicação | O uso de IA altera a duplicação de código produzido? | Não há diferença no % de linhas duplicadas (PMD-CPD) entre com-IA e manual | Há diferença no % de linhas duplicadas entre com-IA e manual |

Teste estatístico adotado para as quatro hipóteses: **Wilcoxon signed-rank, pareado, bilateral** — consistente
com o desenho within-subject e com H1 não-direcional. Estatística descritiva: **mediana e IQR** (intervalo
interquartil), preferidas a média/desvio-padrão dado o N pequeno.

---

## 2. Metodologia

Esta seção documenta o ambiente e o processo com detalhe suficiente para reprodução, conforme exigido no
Passo 5 do enunciado. As decisões abaixo foram fixadas na S01 (`docs/ambiente-experimento.md`) e mantidas sem
alteração até o fim da coleta (S02), para não invalidar a comparação entre trials.

### 2.1 Desenho experimental

- **Tipo:** crossover within-subject, contrabalanceado — cada integrante resolve **todos** os katas, metade
  com IA e metade sem, de forma que cada pessoa serve de seu próprio controle.
- **Variável independente:** uso de assistente de IA (Claude Code), categórica binária: `com-ia` / `manual`.
- **Objetos experimentais:** 6 katas autorais de dificuldade equivalente (§2.2), número par para divisão exata
  entre tratamentos.
- **Quantidade de medições:** 3 integrantes × 6 katas = **18 trials** (9 com-IA, 9 manual).
- **Contrabalanceamento:** a matriz de tratamento por kata/integrante (Tabela 1) foi definida de forma que
  nenhum kata recebe o mesmo tratamento para os três integrantes, distribuindo o efeito de aprendizado
  igualmente entre os dois tratamentos ao longo do grupo (`docs/ameacas-validade.md`, §2).
- **Time-box:** 35 minutos por trial, fixo — só pode ser reduzido (com justificativa), nunca aumentado. Não
  houve necessidade de redução: nenhum trial se aproximou do limite (maior tempo manual observado: 33m13s,
  kata4-sku/integrante-1). Um trial que atingisse o time-box sem passar todos os testes seria registrado como
  **censurado em 35 min (2100 s)**, não descartado.

**Tabela 1 — Matriz de tratamento por integrante e kata**

| Kata | Integrante 1 (Arlindo) | Integrante 2 (Arthur) | Integrante 3 (Camila) |
|---|---|---|---|
| Kata 1 — Placas | Com IA | Manual | Com IA |
| Kata 2 — Bicicletário | Manual | Com IA | Manual |
| Kata 3 — Sensor | Com IA | Manual | Manual |
| Kata 4 — SKU | Manual | Com IA | Com IA |
| Kata 5 — Chamados | Manual | Com IA | Manual |
| Kata 6 — Senha | Com IA | Manual | Com IA |

### 2.2 Objetos experimentais — katas

Foram selecionados **6 katas autorais** (regras de negócio inventadas pelo grupo, não publicadas em
LeetCode/HackerRank/Codewars/Project Euler/AdventOfCode), para reduzir o risco de a IA reproduzir uma solução
memorizada em vez de efetivamente assistir (`docs/enunciado.md`, item H do Passo 1). Todos seguem a mesma
forma — um único método `public static` puro, sem I/O, entrada estruturada → saída estruturada, **8 testes de
aceitação** (caminho feliz + bordas + entrada inválida), solução de referência estimada em 25–55 LOC —, para
manter dificuldade comparável (critério C2, `docs/katas.md`).

| Kata | Núcleo do problema | Assinatura |
|---|---|---|
| 1 — Placas | Normalização de string + deduplicação, dois padrões de formato | `List<String> normalizar(List<String>)` |
| 2 — Bicicletário | Faixas condicionais de tarifa + teto + validação | `int calcularCentavos(int)` |
| 3 — Sensor | Varredura linear com estado (compactação por tolerância) | `List<String> compactar(int[], int)` |
| 4 — SKU | Parsing posicional + dígito verificador (checksum autoral) | `String validar(String)` |
| 5 — Chamados | Parsing de tokens + agrupamento/contagem por chave | `List<String> resumir(List<String>)` |
| 6 — Senha | Contagem de classes de caractere + verificação de adjacência | `String classificar(String)` |

Critérios de seleção (C1–C7), validação de equivalência de dificuldade e o enunciado completo de cada kata
estão em `docs/katas.md`.

### 2.3 Ambiente técnico

| Componente | Escolha | Versão | Motivo |
|---|---|---|---|
| Linguagem das katas | Java | JDK 21 (LTS) | Habilita diretamente CK e PMD (RQ3) |
| Build/test | Maven + JUnit 5 | Maven 3.9.9 / JUnit 5.10.2 | Runner único para todas as katas |
| Complexidade ciclomática | CK | 0.7.0 (tag `ck-0.7.0`, compilado do fonte) | Única ferramenta de WMC para Java citada no enunciado |
| Duplicação de código | PMD / PMD-CPD | 7.27.0 | Ferramenta de duplicação citada no enunciado |
| IDE | VS Code | — | Igual nos dois tratamentos; sem autocomplete de IA (Copilot etc.) ativo em nenhum dos dois |
| Assistente de IA | Claude Code (CLI/agente) | **não registrada sistematicamente** (ver §4.3) | Único assistente, usado da mesma forma pelos 3 integrantes em todo trial `com-ia` |
| Ambiente containerizado | Docker (`maven:3.9.9-eclipse-temurin-21` + Python 3) | — | Elimina divergência de JDK/Maven/Python entre as 3 máquinas |
| Scripts de suporte | Python | — | Orquestram `mvn test`, CK e PMD como processos externos; independente da linguagem das katas |

Estrutura de diretórios: cada trial (kata × tratamento × integrante) é isolado em
`trials/<integrante>/<kata>/<tratamento>/`, partindo de um template limpo do kata (enunciado + testes, sem
solução) e sem histórico de chat de trials anteriores — uma sessão nova do Claude Code por trial `com-ia`.
Detalhe completo em `docs/ambiente-experimento.md`.

**Reprodução do ambiente:**
```
docker build -t lab02-experimento .
docker run -it -v "${PWD}:/workspace" lab02-experimento
```

### 2.4 Variáveis dependentes e métricas coletadas

| Variável | Operacionalização | RQ | Fonte |
|---|---|---|---|
| Tempo até *time-to-green* | Segundos do início do trial até todos os testes de aceitação passarem, ou 2100 s se censurado | RQ1 | `scripts/cronometragem.py` |
| Censura do trial | `true` se o trial atingiu o time-box sem passar todos os testes | RQ1 | idem |
| Taxa de sucesso | `testes_passando / testes_total` ao final do trial | RQ2 | idem (via relatórios Surefire) |
| WMC (complexidade ciclomática somada) | Soma de `wmc` por classe, via CK | RQ3a | `scripts/metricas_estaticas.py` |
| % de linhas duplicadas | Linhas duplicadas / LOC, via PMD-CPD (mínimo 50 tokens) | RQ3b | idem |
| LOC | Linhas de código do trial final, via CK | RQ3 (controle de verbosidade) | idem |

Justificativa completa de cada escolha (entre as métricas candidatas do enunciado) em
`docs/hipoteses-e-metricas.md`, §3.

### 2.5 Execução

Cada integrante executou os 6 trials previstos na Tabela 1, individualmente, usando o mesmo script de
cronometragem (`scripts/cronometragem.py start|check|watch|stop`) nos dois tratamentos — o cronômetro apenas
mede início→fim do trial e roda `mvn test`; a diferença entre tratamentos está em como o integrante resolve
o problema, não em como o tempo é medido. Ao final de cada trial, `scripts/metricas_estaticas.py` foi
executado sobre o código final para coletar WMC, LOC e duplicação. Os resultados brutos consolidados estão em
`resultados/tempos.csv` (RQ1/RQ2) e `resultados/metricas-estaticas.csv` (RQ3).

Nenhum dos 18 trials planejados foi descartado; todos completaram dentro do time-box (nenhuma censura).

---

## 3. Resultados por RQ

Análises completas, com tabelas por integrante e discussão de cada teste, estão em `docs/analise-rq1-rq2.md`
(issue #19) e `docs/analise-rq3.md` (issue #20), geradas por `scripts/analise_rq1_rq2.py` e
`scripts/analise_rq3.py` a partir dos CSVs brutos. Esta seção resume os resultados finais por RQ.

### 3.1 Nota sobre o pareamento

`docs/hipoteses-e-metricas.md` previa o par do Wilcoxon como "mesmo integrante, mesma kata, com-IA vs.
manual" — o que pressuporia cada integrante resolvendo cada kata duas vezes. Na execução real (S02), por
desenho, cada integrante resolveu cada kata **uma única vez**, contrabalanceado entre integrantes (Tabela 1).
O pareamento foi então adaptado para **por integrante**: mediana das 3 katas com-IA de cada integrante vs.
mediana das suas 3 katas manuais — resultando em **N = 3 pares**, dentro do espírito *within-subject*, mas com
poder estatístico menor do que os 4–6 pares originalmente previstos. Essa adaptação é uma ameaça à validade de
conclusão estatística e é discutida em §4.2.

### 3.2 RQ1 — Tempo até *time-to-green*

**Estatística descritiva:**

| Tratamento | N | Tempo — mediana (s) | Tempo — IQR (s) | Trials censurados |
|---|---|---|---|---|
| com-ia | 9 | 40,68 | 84,33 | 0 |
| manual | 9 | 1380,00 | 374,72 | 0 |

**Pares por integrante (mediana das 3 katas de cada tratamento):**

| Integrante | Com IA (s) | Manual (s) |
|---|---|---|
| integrante-1 (Arlindo) | 41,76 | 1380,00 |
| integrante-2 (Arthur) | 34,09 | 1243,36 |
| integrante-3 (Camila) | 118,41 | 1458,59 |

**Wilcoxon signed-rank:** estatística = 0,0; **p = 0,25** (bilateral, N = 3).

**Resposta a RQ1:** a mediana do tempo com IA (~41 s) é mais de **30× menor** que a mediana manual (~23 min),
e os 3 integrantes foram mais rápidos com IA **sem exceção** — efeito grande, consistente e na mesma direção
para todo o grupo. Com N = 3 pares, porém, o menor p bilateral possível no teste exato de Wilcoxon é 0,25:
mesmo um efeito perfeito não alcança significância convencional (p < 0,05) por pura limitação de amostra. A
hipótese nula H0₁ não pode ser formalmente rejeitada com os dados atuais, mas isso reflete **falta de poder
estatístico**, não ausência de diferença real — não deve ser lido como "IA não fez diferença".

### 3.3 RQ2 — Defeitos (taxa de sucesso)

| Integrante | Com IA | Manual |
|---|---|---|
| integrante-1 | 1,0 | 1,0 |
| integrante-2 | 1,0 | 1,0 |
| integrante-3 | 1,0 | 1,0 |

Todos os 18 trials terminaram com **8/8 testes de aceitação passando** (taxa de sucesso = 1,0 em 100% dos
casos, nos dois tratamentos). As diferenças pareadas são todas zero — o teste de Wilcoxon não é aplicável
(sem variância a testar).

**Resposta a RQ2:** dentro do time-box de 35 min, tanto com quanto sem IA, todos os integrantes resolveram
corretamente as 6 katas. Para katas deste porte (pequenas, bem definidas, dimensionadas para caber com folga
no time-box manual), a IA **não teve efeito mensurável sobre taxa de erro** — o ganho observado em RQ1 está
concentrado inteiramente em tempo, não em corretude.

### 3.4 RQ3 — Estrutura do código (complexidade e duplicação)

**Estatística descritiva:**

| Tratamento | N | WMC — mediana | WMC — IQR | LOC — mediana | LOC — IQR | WMC/LOC — mediana | % duplicação — mediana |
|---|---|---|---|---|---|---|---|
| com-ia | 9 | 10,0 | 11,0 | 42,0 | 21,0 | 0,333 | 0,0 |
| manual | 9 | 11,0 | 5,0 | 45,0 | 16,0 | 0,267 | 0,0 |

**RQ3a — Complexidade ciclomática (WMC), pares por integrante:**

| Integrante | WMC com-ia | WMC manual |
|---|---|---|
| integrante-1 | 10,0 | 8,0 |
| integrante-2 | 13,0 | 13,0 |
| integrante-3 | 9,0 | 11,0 |

Wilcoxon: estatística = 1,5; **p = 1,0**. Repetindo com WMC/LOC (controle de verbosidade): estatística = 1,0;
**p = 0,5**.

**Resposta a RQ3a:** diferente de RQ1, aqui **não há direção consistente** entre os 3 integrantes (um WMC
maior com IA, um empatado, um menor) — evidência descritiva, não só falta de poder estatístico, de que a IA
**não alterou sistematicamente** a complexidade ciclomática nestas katas.

**RQ3b — Duplicação de código:** todos os 18 trials (com-IA e manual) tiveram **0% de linhas duplicadas** — o
teste de Wilcoxon não é aplicável. Esperado pelo desenho: cada trial é um único método pequeno e isolado, sem
outro código no projeto contra o qual o PMD-CPD pudesse comparar (limitação de escopo desta métrica neste
desenho, não "a IA nunca duplica código" — ver `docs/ameacas-validade.md`, §3).

**Resposta a RQ3:** nem a complexidade ciclomática, nem a duplicação foram alteradas de forma sistemática pelo
uso de IA nestas katas; LOC também ficou parecido entre tratamentos (controle de verbosidade sem indício de
código sistematicamente mais extenso com IA).

---

## 4. Discussão

### 4.1 Síntese entre RQs

Para este conjunto de katas — pequenas, autorais, bem definidas, com bordas claras e sem componente
algorítmico "de concurso" —, o principal efeito observável do assistente de IA (Claude Code) neste experimento
está concentrado em **velocidade de desenvolvimento** (RQ1): ganho grande (~30×) e consistente entre os 3
integrantes, embora não estatisticamente significativo dado N = 3. Esse ganho **não veio acompanhado** de
custo em corretude (RQ2: 100% de sucesso em ambos os tratamentos) nem de alteração sistemática de complexidade
estrutural (RQ3a) ou duplicação (RQ3b, sem variância a medir). Em outras palavras: dentro deste desenho, a IA
ajudou o grupo a chegar ao mesmo resultado correto e estruturalmente equivalente, mais rápido — não trocou
velocidade por qualidade nem por corretude.

### 4.2 Limitações e ameaças à validade

Tratamento completo em `docs/ameacas-validade.md` (categorias de Wohlin et al.: conclusão estatística, interna,
construto, externa). Pontos centrais para interpretar os resultados acima:

- **N pequeno / poder estatístico baixo (conclusão).** 3 integrantes × 6 katas = 18 trials, mas o pareamento
  por integrante (§3.1) reduz o teste inferencial a **N = 3 pares** — insuficiente para significância
  convencional mesmo com efeito grande e consistente (RQ1). Mitigado parcialmente por Wilcoxon (não
  paramétrico) e mediana/IQR, mas a limitação de poder permanece e é a razão central pela qual RQ1 não atinge
  p < 0,05 apesar da direção do efeito ser unânime.
- **Pareamento adaptado (conclusão/construto).** O par originalmente previsto (mesmo integrante, mesma kata,
  nos dois tratamentos) não existe nos dados reais, porque cada integrante resolveu cada kata uma única vez —
  desvio de desenho documentado em `docs/analise-rq1-rq2.md`, §1.
- **Censura tratada como valor único.** Não se manifestou nesta coleta (0 censuras), mas o desenho aceito
  (2100 s fixo para qualquer censura) tornaria o teste conservador a favor de H0 caso um tratamento acumulasse
  mais censuras que o outro.
- **Efeito de aprendizado e fadiga (interna).** Mitigado pelo crossover contrabalanceado (Tabela 1); fadiga em
  sessões longas é uma ameaça residual não totalmente controlada.
- **Familiaridade prévia desigual com Claude Code (interna).** Mesmo assistente para os 3 integrantes reduz
  variação de ferramenta, mas não elimina diferença de habilidade prévia entre pessoas — mitigada parcialmente
  pelo desenho within-subject (compara cada integrante consigo mesmo).
- **Testes de aceitação como proxy de corretude (construto).** 8 testes por kata cobrem um conjunto finito de
  casos; RQ2 = 100% nos dois tratamentos mede ausência de defeitos *cobertos pelos testes fornecidos*, não
  ausência de defeitos em geral.
- **Duplicação não informativa neste desenho (construto).** Cada trial é isolado (um método por diretório),
  então o PMD-CPD nunca tem outro código para comparar — resultado de 0% em todos os trials é esperado pelo
  desenho, não evidência de que IA nunca duplica código.
- **Amostra, katas e ferramenta pouco generalizáveis (externa).** 3 estudantes de graduação, katas pequenas e
  autocontidas (não representam manutenção de bases grandes), um único assistente (Claude Code) e uma única
  linguagem (Java, fixada pela exigência de CK/PMD). Katas deliberadamente pouco indexadas para reduzir risco
  de memorização pela IA — trade-off que favorece validade de construto (medir assistência de fato) em
  detrimento de validade externa (o ganho de produtividade da IA em problemas comuns/bem indexados pode ser
  diferente do observado aqui).

### 4.3 Pendências e desvios registrados (transparência)

Ao consolidar este relatório a partir do estado atual do repositório, dois pontos ficaram sem 100% de
conformidade com o desenho original e merecem registro explícito em vez de serem omitidos:

- **Versão do Claude Code não registrada.** `docs/ambiente-experimento.md` (§4) previa registrar a saída de
  `claude --version` de cada integrante para reprodutibilidade; isso não foi feito sistematicamente durante os
  trials. Recomenda-se ao grupo completar essa informação (mesmo que aproximada, a partir do histórico de
  instalação de cada integrante) antes da entrega final, já que a versão exata do assistente é parte do que o
  enunciado pede explicitamente na metodologia ("assistente de IA e versão").
- **Dashboard de visualização (Passo 6) ainda pendente.** A issue #21 ("Montagem do dashboard — Pandas +
  Matplotlib/Seaborn") segue aberta no momento da redação deste relatório; os resultados acima são reportados
  em tabelas (consistente com mediana/IQR recomendados para N pequeno), mas o dashboard gráfico comparando os
  tratamentos — entregável formal da S03 — ainda não foi commitado. Deve ser priorizado separadamente deste
  Relatório Final.

### 4.4 Conclusão

Dentro das condições deste experimento — katas pequenas e autorais, time-box de 35 min, Claude Code como único
assistente —, o uso de IA reduziu drasticamente o tempo de resolução (RQ1), de forma consistente entre os três
integrantes, sem custo observável em corretude (RQ2) ou em complexidade/duplicação estruturais (RQ3). A falta
de significância estatística formal em RQ1 e RQ3 decorre do tamanho amostral (N = 3 pares), não de ausência de
efeito — a direção do resultado em RQ1 é unânime e de grande magnitude. Os resultados não devem ser
generalizados além do escopo descrito em §4.2 (katas pequenas, baixa indexação, um único assistente e
linguagem, amostra de 3 estudantes).

---

## 5. Processo, rastreabilidade e GitHub Projects

Todos os trials (kata × tratamento × integrante) e as entregas de cada sprint foram registrados como Issues
individuais no GitHub Projects do grupo, atribuídas ao integrante responsável e referenciadas por número nos
commits correspondentes (ver `docs/issues-planejadas.md` para o checklist completo por sprint).

| Sprint | Entregável | Issues principais |
|---|---|---|
| Lab02S01 | Desenho do experimento + preparação | #1–#6 |
| Lab02S02 | Execução (18 trials) + testes unitários | #7–#18, #22–#42 |
| Lab02S03 | Análise estatística (RQ1/RQ2), análise estrutural (RQ3), dashboard | #19, #20, #21 |
| Relatório Final | Este documento | #45 |

**Link do repositório:** <https://github.com/ArlindoSPJr/LAB02-Expertimentacao-Software>

**Link do GitHub Projects:**

> _[link a preencher pelo grupo]_

---

## Referências

- `docs/enunciado.md` — enunciado original do LAB02 (RQs, GQM, métricas candidatas, etapas por sprint)
- `docs/entendimento-e-planejamento.md` — entendimento compartilhado do trabalho
- `docs/hipoteses-e-metricas.md` — hipóteses H0/H1, variáveis e métricas escolhidas
- `docs/ambiente-experimento.md` — ambiente fixado (linguagem, IDE, assistente de IA, Docker)
- `docs/katas.md` — seleção e validação dos 6 katas
- `docs/scripts-metricas.md` — escopo técnico dos scripts de coleta
- `docs/ameacas-validade.md` — ameaças à validade (conclusão, interna, construto, externa)
- `docs/analise-rq1-rq2.md` — análise estatística RQ1/RQ2 (issue #19)
- `docs/analise-rq3.md` — análise estrutural RQ3 (issue #20)
- `docs/issues-planejadas.md` — issues planejadas por sprint
- `resultados/tempos.csv`, `resultados/metricas-estaticas.csv` — dados brutos coletados
- `scripts/cronometragem.py`, `scripts/metricas_estaticas.py`, `scripts/analise_rq1_rq2.py`,
  `scripts/analise_rq3.py` — scripts de coleta e análise
