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

Uma Issue por kata/tratamento, atribuída a quem executa o trial. Cada integrante resolve os 6 katas (3 com IA, 3 sem, em ordem contrabalanceada entre integrantes — nenhum kata tem o mesmo tratamento para todos). Katas e matriz de tratamento definidas em `docs/katas.md`; caminho do trial correspondente em `trials/<integrante>/<kata>/<tratamento>/`.

**Matriz de tratamento por integrante**

| Kata | Integrante 1 | Integrante 2 | Integrante 3 |
|---|---|---|---|
| Kata 1 — Placas | Com IA | Manual | Com IA |
| Kata 2 — Bicicletário | Manual | Com IA | Manual |
| Kata 3 — Sensor | Com IA | Manual | Manual |
| Kata 4 — SKU | Manual | Com IA | Com IA |
| Kata 5 — Chamados | Manual | Com IA | Manual |
| Kata 6 — Senha | Com IA | Manual | Com IA |

**Integrante 1**
- [ ] `[Trial] Integrante 1 — Kata 1 (Placas) — Com IA`
- [ ] `[Trial] Integrante 1 — Kata 2 (Bicicletário) — Manual`
- [ ] `[Trial] Integrante 1 — Kata 3 (Sensor) — Com IA`
- [ ] `[Trial] Integrante 1 — Kata 4 (SKU) — Manual`
- [ ] `[Trial] Integrante 1 — Kata 5 (Chamados) — Manual`
- [ ] `[Trial] Integrante 1 — Kata 6 (Senha) — Com IA`

**Integrante 2**
- [ ] `[Trial] Integrante 2 — Kata 1 (Placas) — Manual`
- [ ] `[Trial] Integrante 2 — Kata 2 (Bicicletário) — Com IA`
- [ ] `[Trial] Integrante 2 — Kata 3 (Sensor) — Manual`
- [ ] `[Trial] Integrante 2 — Kata 4 (SKU) — Com IA`
- [ ] `[Trial] Integrante 2 — Kata 5 (Chamados) — Com IA`
- [ ] `[Trial] Integrante 2 — Kata 6 (Senha) — Manual`

**Integrante 3**
- [ ] `[Trial] Integrante 3 — Kata 1 (Placas) — Com IA`
- [ ] `[Trial] Integrante 3 — Kata 2 (Bicicletário) — Manual`
- [ ] `[Trial] Integrante 3 — Kata 3 (Sensor) — Manual`
- [ ] `[Trial] Integrante 3 — Kata 4 (SKU) — Com IA`
- [ ] `[Trial] Integrante 3 — Kata 5 (Chamados) — Manual`
- [ ] `[Trial] Integrante 3 — Kata 6 (Senha) — Com IA`

Total: 18 Issues (9 Com IA, 9 Manual).

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
