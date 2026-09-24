# Análise Estrutural — RQ3 (S03)

Deliverable da issue **#20 — Análise estrutural RQ3 (complexidade, duplicação,
LOC)**. Cobre o Passo 4 (`docs/enunciado.md`) para as hipóteses **H1₃ₐ**
(complexidade) e **H1₃ᵦ** (duplicação), definidas em `docs/hipoteses-e-metricas.md`.
Gerado por `scripts/analise_rq3.py` a partir de `resultados/metricas-estaticas.csv`
(18 trials, coletados com `scripts/metricas_estaticas.py` via CK 0.7.0 e PMD-CPD
7.27.0 sobre o código final de cada trial).

O pareamento por integrante (N=3, em vez de "mesmo integrante + mesma kata") segue
a mesma adaptação documentada em `docs/analise-rq1-rq2.md`, seção 1 — cada
integrante resolveu cada kata uma única vez, então o par possível é
mediana(katas com-ia do integrante) vs. mediana(katas manual do integrante).

## 1. Estatística descritiva por tratamento

| Tratamento | N | WMC — mediana | WMC — IQR | LOC — mediana | LOC — IQR | WMC/LOC — mediana | % duplicação — mediana |
|---|---|---|---|---|---|---|---|
| com-ia | 9 | 10.0 | 11.0 | 42.0 | 21.0 | 0.333 | 0.0 |
| manual | 9 | 11.0 | 5.0 | 45.0 | 16.0 | 0.267 | 0.0 |

WMC e LOC absolutos são bem parecidos entre tratamentos. A densidade **WMC/LOC**
(controle de verbosidade, `docs/hipoteses-e-metricas.md`) é um pouco maior no
com-ia (0.333 vs. 0.267) — ou seja, o código com IA tende a ser **ligeiramente
mais denso em complexidade por linha**, não mais verboso. Nenhuma duplicação foi
detectada em nenhum dos 18 trials (esperado: cada trial é um único método pequeno
e autocontido, sem outro código no projeto pra duplicar contra).

## 2. RQ3a — Complexidade ciclomática / WMC (H1₃ₐ)

| Integrante | WMC com-ia | WMC manual |
|---|---|---|
| integrante-1 | 10.0 | 8.0 |
| integrante-2 | 13.0 | 13.0 |
| integrante-3 | 9.0 | 11.0 |

**Resultado:** Wilcoxon signed-rank, estatística = 1.5, **p = 1.0** (bilateral).

**Interpretação:** ao contrário de RQ1 (tempo), aqui **não há direção consistente**
entre os 3 integrantes: um teve WMC maior com IA, um ficou empatado, um teve WMC
menor com IA. Isso é evidência descritiva (não só falta de poder estatístico) de
que **a IA não alterou a complexidade ciclomática de forma sistemática** nestas
katas — diferente de RQ1, onde os 3 pares apontavam na mesma direção apesar do
p-valor alto.

Repetindo com a métrica normalizada (WMC/LOC, controle de verbosidade):

| Integrante | WMC/LOC com-ia | WMC/LOC manual |
|---|---|---|
| integrante-1 | 0.333 | 0.258 |
| integrante-2 | 0.310 | 0.333 |
| integrante-3 | 0.333 | 0.267 |

Wilcoxon: estatística = 1.0, **p = 0.5**. Direção mista de novo (2 de 3 maiores no
com-ia), sem indício forte de efeito sistemático.

## 3. RQ3b — Duplicação de código (H1₃ᵦ)

Todos os 18 trials (com-ia e manual) tiveram **0% de linhas duplicadas** — o
teste de Wilcoxon não é aplicável (diferenças pareadas todas zero).

**Interpretação:** cada trial é um único arquivo/método pequeno (25-55 LOC
estimados, `docs/katas.md`), isolado num diretório próprio, sem outro código no
projeto contra o qual o PMD-CPD pudesse detectar duplicação (limiar de 50 tokens).
Esse resultado é esperado pelo desenho do experimento (katas curtas e
independentes) e não deve ser lido como "IA nunca duplica código" — é uma
limitação de escopo desta métrica neste desenho específico, a citar na discussão
de validade de construto (`docs/ameacas-validade.md`, seção 3).

## 4. Síntese RQ3 vs. RQ1/RQ2

Comparando com `docs/analise-rq1-rq2.md`: a IA produziu um ganho de **tempo**
grande e consistente (RQ1), sem custo de **corretude** (RQ2: 100% de sucesso nos
dois tratamentos) nem alteração sistemática de **complexidade estrutural** (RQ3a)
ou **duplicação** (RQ3b, sem variação a medir). Para estas katas específicas
(pequenas, bem definidas, baixa indexação), o principal efeito observável do
assistente de IA neste experimento está concentrado em **velocidade de
desenvolvimento**, não em qualidade de código nem em taxa de erro.

## 5. Limitações desta análise

- Mesma limitação de N=3 pares da análise de RQ1/RQ2 (`docs/analise-rq1-rq2.md`,
  seção 5).
- WMC/LOC por integrante mistura katas diferentes (de complexidade nominalmente
  equivalente, `docs/katas.md` seção 3, mas não idêntica) entre tratamentos — o
  par não isola perfeitamente o efeito do tratamento do efeito da kata específica.
- Duplicação de código não é uma métrica informativa neste desenho (trials
  isolados, sem outro código para comparar) — um desenho futuro que quisesse medir
  duplicação de verdade precisaria rodar o CPD sobre o conjunto de trials de um
  mesmo integrante/tratamento, não trial a trial isoladamente.

## Referências

- `docs/hipoteses-e-metricas.md` — hipóteses H1₃ₐ/H1₃ᵦ e variáveis originais
- `docs/analise-rq1-rq2.md` — análise de RQ1/RQ2 e nota de pareamento (seção 1)
- `docs/ameacas-validade.md` — ameaças à validade
- `resultados/metricas-estaticas.csv` — dados brutos (saída de
  `scripts/metricas_estaticas.py`)
- `scripts/analise_rq3.py` — script que gera esta análise
