# Seleção e Validação das Katas

Deliverable da issue **#3 — Selecionar e validar as katas** (Passo 2 — Preparação do Experimento, `docs/enunciado.md`; papel do Integrante 1 na S01). Katas 5 e 6 adicionadas posteriormente para expandir o desenho de 4 para 6 katas (ver justificativa na seção 1).

Define os **objetos experimentais** do LAB02: os 6 exercícios (katas) resolvidos por cada integrante, metade com IA e metade sem. Registra *o que* é cada kata, *por que* foram escolhidos e *como* foram validados contra os critérios do enunciado.

> Estas especificações são a fonte da verdade para os templates de kata (`trials/<integrante>/<kata>/<tratamento>/`) e para os testes de aceitação JUnit 5. A matriz de tratamento/ordem e a lista de Issues da S02 ficam em `docs/hipoteses-e-metricas.md` e `docs/issues-planejadas.md`.

---

## 1. Critérios de seleção

| # | Critério | Fonte |
|---|---|---|
| C1 | **Número par**, dividido exatamente pela metade entre tratamentos | Passo 2 |
| C2 | **Dificuldade equivalente** entre as katas | Passo 1 (E), Passo 2 |
| C3 | **Baixa indexação / autorais** — evitar clássicos de LeetCode/HackerRank/Codewars/Project Euler, para a IA não reproduzir solução memorizada | Passo 1 (H) |
| C4 | **Testes automatizados de aceitação** que decidem objetivamente se a solução está correta | Passo 2 |
| C5 | Linguagem **Java** (habilita CK + PMD para RQ3) | `docs/ambiente-experimento.md` |
| C6 | Resolúvel **dentro do time-box de 35 min** no tratamento manual | Passo 3 |
| C7 | Sem algoritmo "de concurso" (DP, grafos, geometria) — foco em **parsing + aplicação de regras + casos de borda** | Passo 1 (H), C2 |

**Por que 6 (revisado de 4):** a proposta inicial fixava 4 katas (12 trials) para conter a fadiga do time-box. O grupo decidiu expandir para **6 katas × 3 integrantes = 18 trials (9 com IA, 9 manual)**, ainda um número par dividido exatamente pela metade por integrante (C1) e por todo o desenho, dando mais poder ao Wilcoxon pareado sem violar C6 — cada kata continua dimensionada para caber com folga no time-box de 35 min (§3). A fadiga (ameaça à validade) segue documentada em `docs/ameacas-validade.md`; mitigação recomendada é não rodar os 6 trials de um integrante em uma única sessão contínua.

## 2. Katas selecionados

Todas têm a **mesma forma**: um único método `public static` puro (sem I/O, determinístico), entrada estruturada → saída estruturada, **8 testes de aceitação** (caminho feliz + bordas + entrada inválida). Solução de referência estimada em 25–55 LOC. As regras de negócio são **autorais do grupo** — não correspondem a nenhum exercício publicado.

### Kata 1 — Normalização e Deduplicação de Placas de Pátio

**Contexto.** Um pátio registra placas digitadas por operadores em formatos inconsistentes. Padronizar e remover duplicatas.

**Assinatura.** `List<String> PlacaNormalizer.normalizar(List<String> brutas)`

**Regras (autorais).**
1. Normalizar cada entrada: remover espaços, hífens e pontos; converter para maiúsculas.
2. Placa canônica = 7 caracteres alfanuméricos, em um de dois padrões:
   - **Antigo:** 3 letras + 4 dígitos (`ABC1234`)
   - **Mercosul:** 3 letras + 1 dígito + 1 letra + 2 dígitos (`ABC1D23`)
3. Entradas que não batem nenhum padrão após normalização são **descartadas**.
4. Cada placa canônica aparece **uma única vez**, na ordem da **primeira ocorrência**.
5. Elemento `null` ou string vazia na lista é ignorado (não quebra).

**Testes de aceitação (8).**
1. Lista vazia → lista vazia.
2. Placa já canônica (formato antigo) → inalterada.
3. Placa com espaços e minúsculas (`"abc 1234"`) → `"ABC1234"`.
4. Placa com hífen (`"ABC-1234"`) → `"ABC1234"`.
5. Placa Mercosul minúscula (`"abc1d23"`) → `"ABC1D23"`.
6. Mesma placa em dois formatos brutos → aparece só uma vez.
7. Placa inválida (6 caracteres; ou letra onde deveria haver dígito) → descartada.
8. Mistura de válidas + inválidas + `null` + duplicata → apenas as válidas únicas, na ordem de primeira ocorrência.

---

### Kata 2 — Tarifa de Bicicletário

**Contexto.** Cálculo do valor a cobrar pelo uso de uma bicicleta compartilhada, dada a duração.

**Assinatura.** `int TarifaBicicletario.calcularCentavos(int minutos)`

**Regras (autorais).**
1. `minutos` de 0 a 20: **grátis** (0).
2. `minutos` de 21 a 60: **R$ 3,00** (300 centavos), fixo.
3. `minutos` acima de 60: `300 + 150 × (blocos de 30 min iniciados após a 1ª hora)`.
   Ex.: 61 min → 1 bloco → 450; 90 min → 1 bloco → 450; 91 min → 2 blocos → 600.
4. **Teto diário:** o valor nunca ultrapassa **R$ 20,00** (2000 centavos).
5. `minutos == 0` → 0.
6. `minutos` negativo → `IllegalArgumentException`.

**Testes de aceitação (8).**
1. `0` → `0`.
2. `20` → `0` (limite superior do grátis).
3. `21` → `300`.
4. `60` → `300` (limite superior da faixa fixa).
5. `61` → `450` (primeiro bloco após 1h iniciado).
6. `91` → `600` (segundo bloco iniciado).
7. Valor alto (`5000`) → `2000` (teto aplicado).
8. `-1` → lança `IllegalArgumentException`.

---

### Kata 3 — Compactação de Leituras de Sensor

**Contexto.** Um sensor emite leituras inteiras em sequência. Compactar leituras estáveis em faixas para reduzir o volume armazenado.

**Assinatura.** `List<String> SensorCompactador.compactar(int[] leituras, int tolerancia)`

**Regras (autorais).**
1. Percorrer as leituras da esquerda para a direita. A faixa corrente é aberta pela primeira leitura ainda não agrupada; seu valor é o **valor de abertura**.
2. A leitura atual entra na faixa corrente se `|leitura - valorDeAbertura| <= tolerancia`. Caso contrário, a faixa corrente é fechada e uma **nova faixa** começa na leitura atual.
3. Cada faixa fechada é formatada como `"i-j:min..max"`, onde `i` e `j` são os índices (0-based) inicial e final, e `min`/`max` os valores extremos observados na faixa.
4. As faixas retornadas cobrem todos os índices do array, de forma contígua e sem sobreposição.
5. Array vazio → lista vazia.
6. Uma única leitura de valor `v` → `["0-0:v..v"]`.
7. `tolerancia` negativa → `IllegalArgumentException`.

**Testes de aceitação (8).**
1. Array vazio → lista vazia.
2. `[5]`, tol `0` → `["0-0:5..5"]`.
3. `[7,7,7]`, tol `0` → `["0-2:7..7"]`.
4. `[10,11,9,10]`, tol `2` → `["0-3:9..11"]` (todas dentro da tolerância; min/max corretos).
5. `[10,20]`, tol `2` → `["0-0:10..10","1-1:20..20"]` (salto além da tolerância).
6. `[4,4,5,4]`, tol `0` → `["0-1:4..4","2-2:5..5","3-3:4..4"]`.
7. Sequência com 3+ faixas → índices contíguos cobrindo todo o array, na ordem.
8. `tolerancia = -1` → lança `IllegalArgumentException`.

---

### Kata 4 — Validador de Código de Inventário (SKU interno)

**Contexto.** Validação do código interno de SKU usado no inventário, com dígito verificador próprio.

**Assinatura.** `String SkuValidator.validar(String codigo)` — retorna `"OK"`, `"FORMATO"` ou `"DV"`.

**Regras (autorais).**
1. Formato esperado: `LLL-NNNN-D`
   - `LLL`: exatamente 3 letras maiúsculas `A`–`Z` (categoria).
   - `NNNN`: exatamente 4 dígitos `0`–`9` (sequencial).
   - `D`: exatamente 1 dígito (verificador).
   - Hífens exatamente nas posições 4 e 9 (1-based); comprimento total 10.
2. Se o layout, o comprimento, os separadores ou as classes de caracteres não batem → retorna `"FORMATO"`. Isso inclui `codigo` `null` ou vazio.
3. Dígito verificador (regra autoral): seja `S = Σ (dígito_k × k)` para `k = 1..4` sobre `NNNN`, mais `Σ valorLetra` sobre `LLL` (`A=1, B=2, …, Z=26`). O verificador correto é `S mod 10`.
4. Se o formato está correto mas `D` ≠ `S mod 10` → retorna `"DV"`.
5. Caso contrário → `"OK"`.

**Testes de aceitação (8).**
1. Código válido calculado à mão (`"ABC-0000-6"` → letras `1+2+3=6`, sequencial `0` ⇒ DV `6`) → `"OK"`.
2. Segundo código válido com sequencial não nulo (`"ABC-1234-6"` → `1×1+2×2+3×3+4×4 = 30`, letras `6` ⇒ `S = 36`, DV `6`) → `"OK"`.
3. Letras minúsculas (`"abc-0000-6"`) → `"FORMATO"`.
4. Sequencial com 3 dígitos (`"ABC-000-6"`) → `"FORMATO"`.
5. Sem hífens (`"ABC00006"`) → `"FORMATO"`.
6. Formato correto, DV errado (`"ABC-0000-7"`) → `"DV"`.
7. `null` → `"FORMATO"`.
8. String vazia → `"FORMATO"`.

---

### Kata 5 — Resumo de Chamados por Prioridade

**Contexto.** Uma central de suporte registra chamados como linhas de texto `"PRIORIDADE:CODIGO"`. Consolidar quantos chamados válidos existem por prioridade.

**Assinatura.** `List<String> ChamadoResumo.resumir(List<String> chamados)`

**Regras (autorais).**
1. Cada item válido tem o formato `"PRIORIDADE:CODIGO"`, com exatamente um separador `:`.
2. `PRIORIDADE` é comparada sem diferenciar maiúsculas/minúsculas e normalizada para maiúsculas; deve ser uma de `ALTA`, `MEDIA`, `BAIXA`. Qualquer outro valor descarta a linha.
3. `CODIGO` deve ser não vazio; se vazio, a linha é descartada.
4. Linhas sem `:` ou com mais de um `:` são descartadas.
5. Elemento `null` é ignorado.
6. A saída é uma lista com uma entrada `"PRIORIDADE:contagem"` por prioridade que teve **pelo menos 1** chamado válido, na ordem fixa `ALTA`, `MEDIA`, `BAIXA` (prioridades com contagem zero não aparecem).

**Testes de aceitação (8).**
1. Lista vazia → lista vazia.
2. Um chamado válido (`"ALTA:A1"`) → `["ALTA:1"]`.
3. Mistura de prioridades → contagem por prioridade, `BAIXA` ausente por contagem zero.
4. Mesma prioridade em cases diferentes (`"alta"`, `"ALTA"`, `"Alta"`) → agregada em uma única contagem.
5. Prioridade desconhecida (`"URGENTE:X1"`) → descartada.
6. Formato malformado (sem `:` ou com mais de um `:`) → descartado.
7. `CODIGO` vazio (`"ALTA:"`) → descartado.
8. Mistura completa de válidos, inválidos, `null` e todas as regras de descarte → contagem correta na ordem fixa.

---

### Kata 6 — Classificador de Senha de Cofre

**Contexto.** Validar e classificar a força de uma senha alfanumérica segundo regras internas de composição.

**Assinatura.** `String SenhaValidator.classificar(String senha)` — retorna `"FORTE"`, `"MEDIA"`, `"FRACA"` ou `"INVALIDA"`.

**Regras (autorais).**
1. `senha` `null`, ou comprimento fora de `[6, 12]`, ou contendo qualquer caractere que não seja letra (`a`-`z`, `A`-`Z`) ou dígito (`0`-`9`) → `"INVALIDA"`.
2. Contar quantas das 3 classes de caractere estão presentes: minúscula, maiúscula, dígito (`classes` de 1 a 3).
3. Verificar se existe repetição de caractere idêntico em posições **adjacentes** (case-sensitive).
4. `score = max(1, classes − (1 se houver repetição adjacente, senão 0))`.
5. `score == 3` → `"FORTE"`; `score == 2` → `"MEDIA"`; `score == 1` → `"FRACA"`.

**Testes de aceitação (8).**
1. `null` → `"INVALIDA"`.
2. String vazia → `"INVALIDA"`.
3. Senha curta (< 6 caracteres) → `"INVALIDA"`.
4. Senha longa (> 12 caracteres) → `"INVALIDA"`.
5. Caractere fora de letras/dígitos (ex.: `"!"`) → `"INVALIDA"`.
6. 3 classes de caractere, sem repetição adjacente → `"FORTE"`.
7. 3 classes de caractere, com repetição adjacente (rebaixa uma categoria) → `"MEDIA"`.
8. Apenas 1 classe de caractere (só minúsculas) → `"FRACA"`.

---

## 3. Validação dos critérios

### C2 — Dificuldade equivalente

| Dimensão | Kata 1 | Kata 2 | Kata 3 | Kata 4 | Kata 5 | Kata 6 |
|---|---|---|---|---|---|---|
| Forma | 1 método `static` puro | 1 método `static` puro | 1 método `static` puro | 1 método `static` puro | 1 método `static` puro | 1 método `static` puro |
| Entrada | `List<String>` | `int` | `int[]` + `int` | `String` | `List<String>` | `String` |
| Núcleo | normalização + dedup | faixas condicionais + aritmética | varredura linear com estado | parsing por posição + checksum | parsing de tokens + agrupamento/contagem | contagem de classes de caractere + adjacência |
| Bordas exigidas | vazio, inválido, `null`, duplicata | zero, limites de faixa, teto, negativo | vazio, unitário, tol 0, negativo | `null`/vazio, cada classe de char, DV | `null`, formato malformado, código vazio, prioridade desconhecida | `null`/vazio, curta, longa, char inválido |
| Nº de testes | 8 | 8 | 8 | 8 | 8 | 8 |
| LOC de referência (est.) | ~45–55 | ~25–35 | ~35–45 | ~35–45 | ~30–40 | ~30–40 |
| Algoritmo "de concurso"? | não | não | não | não | não | não |
| Tempo manual estimado | 20–30 min | 12–20 min | 20–30 min | 20–30 min | 15–25 min | 15–25 min |

Todas exigem o mesmo tipo de trabalho (ler entrada → aplicar regras autorais → tratar bordas), o mesmo número de testes e nenhum conhecimento algorítmico especializado. A Kata 2 é a mais curta; concentra lógica de faixas + teto + exceção para manter o tempo de raciocínio comparável. Katas 5 e 6 replicam o mesmo padrão de forma/complexidade das katas 1–4, com núcleos distintos (agrupamento por chave e composição de caracteres) para não sobrepor os núcleos já cobertos. **Equivalência final a confirmar por piloto** (§4).

### C3 — Baixa indexação

- As **regras de negócio são inventadas** (tarifas, placa com dois padrões, formato `"i-j:min..max"`, checksum posicional próprio). Não reproduzem enunciado de LeetCode, HackerRank, Codewars, Exercism, Project Euler ou AdventOfCode.
- Nenhuma kata é clássica (FizzBuzz, Roman Numerals, String Calculator, Bowling, Palindrome, Anagram, Two Sum, Fibonacci, etc.).
- Os sub-problemas isolados são triviais (normalizar string, somar com pesos), mas a IA precisa combinar as **regras específicas do enunciado** — que não estão memorizadas —, que é exatamente o "efetivamente ajudar" que o experimento quer medir.
- **Verificação a executar antes de congelar:** buscar frases-chave de cada enunciado nos buscadores e catálogos acima; nenhuma deve retornar correspondência direta.

### C4 / C5 / C6 / C7

- **C4/C5:** cada kata terá uma classe de teste JUnit 5 (`src/test/java/.../<Kata>Test.java`) com os 8 casos acima, preferencialmente como `@ParameterizedTest`.
- **C6:** estimativas de piloto folgadamente abaixo de 35 min no tratamento manual.
- **C7:** nenhuma kata exige DP, grafos, geometria ou estruturas avançadas.

## 4. Checklist de validação (S01)

- [x] C1 — número par (6), divisível pela metade por tratamento (9 com-ia / 9 manual em 18 trials).
- [x] C2 — equivalência de forma/algoritmo/nº de testes documentada (§3), incluindo katas 5 e 6.
- [ ] C2 — **piloto**: um integrante resolve as 6 katas manualmente e registra o tempo; nenhuma deve estourar 35 min nem ficar abaixo de ~10 min.
- [x] C3 — regras autorais, nenhuma kata clássica (§3).
- [ ] C3 — **busca de indexação** executada (frases-chave dos 6 enunciados); resultado colado aqui.
- [ ] C4 — 6 classes de teste JUnit 5 implementadas (8 casos cada) e rodando via `mvn test` — katas 1–4 ainda pendentes de execução real, katas 5–6 recém-adicionadas (ver `trials/`).
- [x] C5 — Java (`docs/ambiente-experimento.md`).
- [x] C6 — estimativas dentro do time-box (§3); confirmação depende do piloto.
- [x] C7 — sem algoritmo de concurso.

## Referências

- `docs/enunciado.md` — Passos 1–2, ameaça de memorização (H)
- `docs/hipoteses-e-metricas.md` — hipóteses, variáveis, matriz de tratamento/ordem
- `docs/ambiente-experimento.md` — Java/Maven/JUnit, estrutura `trials/`
- `docs/issues-planejadas.md` — Issues da S02
