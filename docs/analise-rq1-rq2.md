# Análise Estatística — RQ1 e RQ2 (S03)

Deliverable da issue **#19 — Análise estatística RQ1/RQ2 (Wilcoxon pareado — tempo e
taxa de sucesso)**. Cobre o Passo 4 (`docs/enunciado.md`) para as hipóteses **H1₁**
(tempo) e **H1₂** (taxa de sucesso), definidas em `docs/hipoteses-e-metricas.md`.
Gerado por `scripts/analise_rq1_rq2.py` a partir de `resultados/tempos.csv` (18
trials: 3 integrantes × 6 katas, 9 com-ia / 9 manual).

## 1. Nota sobre o pareamento (desvio do desenho original)

`docs/hipoteses-e-metricas.md` descreve o par do teste de Wilcoxon como "mesmo
integrante, mesma kata, com IA vs. sem IA" — o que pressupõe que cada integrante
resolveria cada kata **duas vezes**, uma vez em cada tratamento. Na execução real
(S02), cada integrante resolveu cada kata **uma única vez** (contrabalanceado entre
integrantes — ver `docs/katas.md`), então esse pareamento exato não existe nos dados.

**Adaptação adotada:** o par passa a ser **por integrante** (não por kata): para
cada um dos 3 integrantes, agregamos a mediana do tempo (e da taxa de sucesso) das
suas 3 katas com-ia contra a mediana das suas 3 katas manual. Isso resulta em
**N = 3 pares** para o teste de Wilcoxon signed-rank — dentro do espírito
within-subject (mesma pessoa nos dois tratamentos), mas com poder estatístico ainda
mais baixo do que os 4-6 pares originalmente previstos. Essa limitação é discutida
na seção 4 e deve constar no Relatório Final como ameaça à validade de conclusão
(complementa `docs/ameacas-validade.md`).

## 2. Estatística descritiva por tratamento

| Tratamento | N | Tempo — mediana (s) | Tempo — IQR (s) | Taxa de sucesso — mediana | Taxa de sucesso — IQR | Trials censurados |
|---|---|---|---|---|---|---|
| com-ia | 9 | 40.68 | 84.33 | 1.0 | 0.0 | 0 |
| manual | 9 | 1380.00 | 374.72 | 1.0 | 0.0 | 0 |

A mediana do tempo com IA (~41s) é **mais de 30× menor** que a mediana manual
(~23 min). Nenhum trial foi censurado (todos passaram os 8 testes de aceitação
dentro do time-box de 35 min), então a métrica primária de RQ1 (time-to-green) não
tem nenhum valor substituído por censura.

## 3. RQ1 — Tempo até time-to-green (H1₁)

Par por integrante (mediana das katas com-ia vs. mediana das katas manual):

| Integrante | Com IA (s) | Manual (s) |
|---|---|---|
| integrante-1 | 41.76 | 1380.00 |
| integrante-2 | 34.09 | 1243.36 |
| integrante-3 | 118.41 | 1458.59 |

**Resultado:** Wilcoxon signed-rank, estatística = 0.0, **p = 0.25** (bilateral).

**Interpretação:** com N = 3 pares, o menor p-valor bilateral possível no teste
exato de Wilcoxon é 0.25 — ou seja, **mesmo com um efeito perfeito** (os 3
integrantes foram mais rápidos com IA, sem uma única exceção), o teste não alcança
significância estatística convencional (p < 0.05) por pura limitação de amostra.
Não se deve interpretar p = 0.25 como "sem efeito": a direção do efeito é
**consistente e grande** nos 3 pares (com-ia sempre dezenas de vezes mais rápido);
a hipótese nula (H0₁) não pode ser formalmente rejeitada com os dados atuais, mas
isso reflete falta de poder estatístico, não ausência de diferença real. Isso deve
ser discutido explicitamente no Relatório Final, e não citado como "IA não fez
diferença".

## 4. RQ2 — Taxa de sucesso dos testes (H1₂)

| Integrante | Com IA | Manual |
|---|---|---|
| integrante-1 | 1.0 | 1.0 |
| integrante-2 | 1.0 | 1.0 |
| integrante-3 | 1.0 | 1.0 |

**Resultado:** todos os 18 trials terminaram com **8/8 testes passando** (taxa de
sucesso = 1.0 em 100% dos casos, com ou sem IA). As diferenças pareadas são todas
zero — o teste de Wilcoxon não é aplicável (não há variância a testar).

**Interpretação:** dentro do time-box de 35 min, tanto com quanto sem IA, todos os
integrantes conseguiram resolver corretamente as 6 katas propostas. Isso sugere que,
para katas deste nível de dificuldade (C2/C6 em `docs/katas.md`: dimensionadas para
caber "com folga" no time-box manual), a IA não teve efeito mensurável sobre **taxa
de erro** — o ganho observado (seção 3) está inteiramente concentrado em **tempo**,
não em corretude. Isso é consistente com katas pequenas e bem definidas (baixa
ambiguidade de requisito); RQ2 poderia ter resultado diferente em tarefas mais
longas ou ambíguas — ponto para a discussão de validade externa
(`docs/ameacas-validade.md`).

## 5. Limitações desta análise

- **N = 3 pares** (adaptação da seção 1): poder estatístico insuficiente para
  significância convencional mesmo com efeito grande e consistente (RQ1).
- **RQ2 sem variância**: taxa de sucesso 100% em todos os trials impede qualquer
  teste inferencial válido — o dado em si (nenhum defeito, nos dois tratamentos) já
  é a resposta descritiva a RQ2 para este experimento.
- Nenhum trial censurado: a métrica de tempo não foi afetada por substituições de
  35 min, então a comparação de RQ1 é sobre tempos reais em toda a amostra.

## Referências

- `docs/hipoteses-e-metricas.md` — hipóteses H1₁/H1₂ e variáveis originais
- `docs/ameacas-validade.md` — ameaças à validade de conclusão estatística
- `resultados/tempos.csv` — dados brutos (saída de `scripts/cronometragem.py`)
- `scripts/analise_rq1_rq2.py` — script que gera esta análise
