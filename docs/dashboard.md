# Dashboard de Visualização (S03 — Passo 6)

Deliverable do Passo 6 (`docs/enunciado.md`): "Importe os dados do experimento
e gere gráficos (Pandas + Matplotlib/Seaborn) comparando tempo, taxa de
sucesso e métricas estáticas entre os tratamentos." Gerado por
`scripts/dashboard.py` a partir de `resultados/tempos.csv` (RQ1/RQ2) e
`resultados/metricas-estaticas.csv` (RQ3), o mesmo pareamento por integrante
(N=3) usado em `docs/analise-rq1-rq2.md` e `docs/analise-rq3.md`.

Imagem: `resultados/dashboard/dashboard.png`
Resumo numérico: `resultados/dashboard/resumo-dashboard.csv`

## Como ler o painel

Os 8 gráficos estão organizados em duas linhas. A primeira linha cobre os
itens **obrigatórios** pelo enunciado (RQ1, RQ2, RQ3a e a métrica de controle
LOC); a segunda linha cobre RQ3b (também obrigatório) e dois complementos
opcionais que aprofundam a leitura.

Todos os gráficos usam a mesma paleta fixa: **azul (`#2a78d6`) = com-ia**,
**laranja (`#eb6834`) = manual** — nunca invertida entre os painéis. Os
boxplots agrupam os 18 trials (9 por tratamento) para dar uma leitura rápida
por tratamento; isso é uma visão *descritiva* pooled. A inferência estatística
real (teste de Wilcoxon anotado abaixo de cada gráfico) é pareada **por
integrante** (N=3 pares — cada integrante contribui a mediana das suas 3
katas com-ia vs. a mediana das suas 3 katas manual), não pelos 18 pontos
como se fossem independentes — ver a nota de pareamento em
`docs/analise-rq1-rq2.md`, seção 1. Os dois últimos gráficos existem
justamente para deixar esse pareamento visível.

## 1. RQ1 — Tempo até time-to-green

**Tipo:** boxplot (escala logarítmica no eixo Y) + pontos individuais dos 18
trials.

Compara o tempo (em segundos) até passar em todos os testes de aceitação,
com-ia vs. manual. A escala log é necessária porque a diferença é enorme:
mediana de ~41s com IA contra ~1380s (23 min) manual — mais de 30× menor. Sem
log, o boxplot com-ia ficaria visualmente esmagado perto de zero. A anotação
mostra `Wilcoxon p=0.250 (N=3 pares/integrante)`: com N=3, esse é o menor
p-valor bilateral possível no teste exato, mesmo com um efeito perfeito (os 3
integrantes foram mais rápidos com IA, sem exceção) — não deve ser lido como
"sem diferença", e sim como falta de poder estatístico (`docs/analise-rq1-rq2.md`,
seção 3).

## 2. RQ2 — Taxa de sucesso dos testes

**Tipo:** barras (mediana por tratamento) com rótulo percentual.

Mostra a % de testes de aceitação passando ao final do trial. Os dois
tratamentos ficaram em 100% — todos os 18 trials (com-ia e manual) passaram
nos 8/8 testes dentro do time-box de 35 min. A anotação diz
`Wilcoxon: sem variância (diffs=0)`: como não há nenhuma diferença entre os
pares, o teste não é aplicável (não há variância a testar) — o próprio dado
(zero defeitos nos dois tratamentos) já é a resposta descritiva de RQ2 aqui.

## 3. RQ3a — Complexidade ciclomática (WMC)

**Tipo:** boxplot + pontos individuais.

Compara o WMC (Weighted Methods per Class, via CK) do código final de cada
trial. As medianas são próximas (10.0 com-ia vs. 11.0 manual) e a anotação
mostra `Wilcoxon p=1.000`: ao contrário do tempo, aqui não há direção
consistente entre os 3 integrantes (um teve WMC maior com IA, um empatou, um
teve menor) — evidência descritiva de que a IA não alterou a complexidade de
forma sistemática nestas katas (`docs/analise-rq3.md`, seção 2). O outlier
visível no com-ia (WMC ≈ 26) é a kata6-senha do integrante-1.

## 4. LOC (métrica de controle)

**Tipo:** boxplot + pontos individuais.

LOC é reportado sempre ao lado de complexidade/duplicação porque código
gerado por IA pode ser mais verboso — o enunciado marca essa métrica como
obrigatória sempre que WMC/duplicação são reportados. Aqui as medianas
também são próximas (42 com-ia vs. 45 manual), sem verbosidade adicional
sistemática da IA. O outlier no manual (~78 LOC) é a kata6-senha do
integrante-2.

## 5. RQ3b — Duplicação de código

**Tipo:** barras (mediana por tratamento).

Compara o % de linhas duplicadas (via PMD-CPD). Ambos os tratamentos ficaram
em 0.0% em todos os 18 trials — esperado pelo desenho do experimento (cada
trial é um método pequeno e isolado, sem outro código no projeto contra o
qual detectar duplicação; ver limitação em `docs/analise-rq3.md`, seção 3).
Como não há variância, `Wilcoxon: sem variância (diffs=0)` novamente — não é
"a IA nunca duplica código", é uma limitação de escopo desta métrica neste
desenho específico.

## 6. Complemento — densidade WMC/LOC

**Tipo:** boxplot + pontos individuais. *(item opcional/complementar)*

Normaliza WMC por linha de código, para isolar complexidade "de verdade" do
efeito de verbosidade (já que LOC absoluto pode inflar WMC absoluto). A
densidade é um pouco maior no com-ia (mediana 0.333 vs. 0.267) — ou seja,
quando a IA reduz levemente o WMC absoluto, ela reduz o LOC proporcionalmente
mais, então o código com IA tende a ser ligeiramente mais denso em
complexidade por linha, não mais verboso. `Wilcoxon p=0.500`: direção mista
entre os 3 integrantes, sem indício forte de efeito sistemático.

## 7. Complemento — tempo pareado por integrante

**Tipo:** gráfico de linhas pareadas (com-ia → manual), uma linha por
integrante (P1/P2/P3), escala log no eixo Y. *(item opcional/complementar)*

Este é o gráfico que sustenta visualmente o teste de Wilcoxon de RQ1: em vez
de pool-ar os 18 trials, mostra o par real usado na inferência — a mediana
das 3 katas com-ia de cada integrante contra a mediana das suas 3 katas
manual. As 3 linhas sobem da esquerda (com-ia, rápido) para a direita
(manual, lento) na mesma direção, sem exceção — é essa consistência visual
que justifica dizer que o efeito é grande e real mesmo com p=0.250.

## 8. Complemento — WMC pareado por integrante

**Tipo:** gráfico de linhas pareadas (com-ia → manual), uma linha por
integrante (P1/P2/P3). *(item opcional/complementar)*

Mesma lógica do gráfico 7, mas para WMC. Aqui as 3 linhas **não** seguem a
mesma direção: P2 sobe (WMC maior no com-ia), P3 desce (WMC maior no manual)
e P1 fica praticamente empatado — o contraste visual com o gráfico 7 (onde as
3 linhas concordam) é o ponto central: tempo tem um efeito consistente entre
integrantes, complexidade estrutural não tem.

## Referências

- `scripts/dashboard.py` — script que gera o painel e o resumo
- `docs/analise-rq1-rq2.md` — análise estatística de RQ1/RQ2 e nota de pareamento (seção 1)
- `docs/analise-rq3.md` — análise estrutural de RQ3
- `resultados/tempos.csv`, `resultados/metricas-estaticas.csv` — dados brutos
