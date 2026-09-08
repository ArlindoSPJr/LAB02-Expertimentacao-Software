# Issues Planejadas por Sprint

Checklist de referência para criação das Issues no GitHub Projects, com responsáveis já divididos entre os 3 integrantes. Cada trial da S02 deve ser referenciado pelo número da Issue nos commits correspondentes (commits sem essa referência não são considerados na correção).

## S01 — Desenho do Experimento + Preparação (Lab02S01)

| Issue | Responsável |
|---|---|
| Definir hipóteses e variáveis do experimento (H0/H1, variáveis dependentes/independentes) | Integrante 3 |
| Documentar ameaças à validade (efeito aprendizado, memorização pela IA, familiaridade prévia) | Integrante 3 |
| Selecionar e validar os katas (dificuldade equivalente, baixa indexação) — `docs/katas.md` | Integrante 1 |
| Definir e documentar o ambiente do experimento (linguagem, IDE, assistente de IA único) | Integrante 1 |
| Escrever script de cronometragem/coleta de tempo | Integrante 2 |
| Escrever script de coleta de métricas estáticas (CK/PMD ou Radon) | Integrante 2 |

## S02 — Execução do Experimento + Coleta de Dados (Lab02S02)

Uma Issue por kata/tratamento, atribuída a quem executa o trial. Cada integrante resolve os 6 katas (3 com IA, 3 sem, em ordem contrabalanceada entre integrantes — nenhum kata deve ter o mesmo tratamento para todos).

**Integrante 1**
- [ ] `[Trial] Integrante 1 — Kata 1 (Palíndromo) — <Com IA|Manual>`
- [ ] `[Trial] Integrante 1 — Kata 2 (Contagem de Ocorrências de Caractere) — <Com IA|Manual>`
- [ ] `[Trial] Integrante 1 — Kata 3 (Contagem de Sequências Crescentes) — <Com IA|Manual>`
- [ ] `[Trial] Integrante 1 — Kata 4 — <Com IA|Manual>`
- [ ] `[Trial] Integrante 1 — Kata 5 — <Com IA|Manual>`
- [ ] `[Trial] Integrante 1 — Kata 6 — <Com IA|Manual>`

**Integrante 2**
- [ ] `[Trial] Integrante 2 — Kata 1 — <Com IA|Manual>`
- [ ] `[Trial] Integrante 2 — Kata 2 — <Com IA|Manual>`
- [ ] `[Trial] Integrante 2 — Kata 3 — <Com IA|Manual>`
- [ ] `[Trial] Integrante 2 — Kata 4 — <Com IA|Manual>`
- [ ] `[Trial] Integrante 2 — Kata 5 — <Com IA|Manual>`
- [ ] `[Trial] Integrante 2 — Kata 6 — <Com IA|Manual>`

**Integrante 3**
- [ ] `[Trial] Integrante 3 — Kata 1 — <Com IA|Manual>`
- [ ] `[Trial] Integrante 3 — Kata 2 — <Com IA|Manual>`
- [ ] `[Trial] Integrante 3 — Kata 3 — <Com IA|Manual>`
- [ ] `[Trial] Integrante 3 — Kata 4 — <Com IA|Manual>`
- [ ] `[Trial] Integrante 3 — Kata 5 — <Com IA|Manual>`
- [ ] `[Trial] Integrante 3 — Kata 6 — <Com IA|Manual>`

> Preencher `<Com IA|Manual>` conforme a matriz de contrabalanceamento definida no Desenho do Experimento (S01), garantindo que cada kata seja resolvido com IA e sem IA por integrantes diferentes.

Total: 18 Issues.

## S03 — Análise de Resultados + Dashboard (Lab02S03)

| Issue | Responsável |
|---|---|
| Análise estatística RQ1/RQ2 (Wilcoxon pareado — tempo e taxa de sucesso) | Integrante 1 |
| Análise estrutural RQ3 (complexidade, duplicação, LOC) | Integrante 3 |
| Montagem do dashboard (Pandas + Matplotlib/Seaborn) consolidando os resultados | Integrante 2 |

## Relatório Final

| Issue | Responsável |
|---|---|
| Redigir o Relatório Final (introdução, metodologia, resultados por RQ, discussão, link do board) | A dividir por seção entre os 3 integrantes |
