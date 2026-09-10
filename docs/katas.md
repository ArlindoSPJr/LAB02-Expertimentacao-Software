# Seleção e Validação das Katas

Deliverable da issue **#3 — Selecionar e validar as 4 katas** (Passo 2 — Preparação do Experimento, `docs/enunciado.md`; papel do Integrante 1 na S01).

Define os **objetos experimentais** do LAB02: os 4 exercícios (katas) resolvidos por cada integrante, metade com IA e metade sem. Registra *o que* é cada kata, *por que* foram escolhidos e *como* foram validados contra os critérios do enunciado.

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

**Por que 4 e não 6:** 4 katas × 3 integrantes = 12 trials (6 com IA, 6 manual), suficiente para o Wilcoxon pareado; 6 katas × 2 tratamentos dentro de 35 min elevaria a fadiga (ameaça à validade) sem ganho estatístico dado o N fixo de 3 participantes.

## 2. Katas selecionados

Todas têm a **mesma forma**: um único método `public static` puro (sem I/O, determinístico), entrada estruturada → saída estruturada, **8 testes de aceitação** (caminho feliz + bordas + entrada inválida). Solução de referência estimada em 30–55 LOC. As regras de negócio são **autorais do grupo** — não correspondem a nenhum exercício publicado.

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

## 3. Validação dos critérios

### C2 — Dificuldade equivalente

| Dimensão | Kata 1 | Kata 2 | Kata 3 | Kata 4 |
|---|---|---|---|---|
| Forma | 1 método `static` puro | 1 método `static` puro | 1 método `static` puro | 1 método `static` puro |
| Entrada | `List<String>` | `int` | `int[]` + `int` | `String` |
| Núcleo | normalização + dedup | faixas condicionais + aritmética | varredura linear com estado | parsing por posição + checksum |
| Bordas exigidas | vazio, inválido, `null`, duplicata | zero, limites de faixa, teto, negativo | vazio, unitário, tol 0, negativo | `null`/vazio, cada classe de char, DV |
| Nº de testes | 8 | 8 | 8 | 8 |
| LOC de referência (est.) | ~45–55 | ~25–35 | ~35–45 | ~35–45 |
| Algoritmo "de concurso"? | não | não | não | não |
| Tempo manual estimado | 20–30 min | 12–20 min | 20–30 min | 20–30 min |

Todas exigem o mesmo tipo de trabalho (ler entrada → aplicar regras autorais → tratar bordas), o mesmo número de testes e nenhum conhecimento algorítmico especializado. A Kata 2 é a mais curta; concentra lógica de faixas + teto + exceção para manter o tempo de raciocínio comparável. **Equivalência final a confirmar por piloto** (§4).

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

- [x] C1 — número par (4), divisível pela metade por tratamento.
- [x] C2 — equivalência de forma/algoritmo/nº de testes documentada (§3).
- [ ] C2 — **piloto**: um integrante resolve as 4 katas manualmente e registra o tempo; nenhuma deve estourar 35 min nem ficar abaixo de ~10 min.
- [x] C3 — regras autorais, nenhuma kata clássica (§3).
- [ ] C3 — **busca de indexação** executada (frases-chave dos 4 enunciados); resultado colado aqui.
- [ ] C4 — 4 classes de teste JUnit 5 implementadas (8 casos cada) e rodando via `mvn test`.
- [x] C5 — Java (`docs/ambiente-experimento.md`).
- [x] C6 — estimativas dentro do time-box (§3); confirmação depende do piloto.
- [x] C7 — sem algoritmo de concurso.

## Referências

- `docs/enunciado.md` — Passos 1–2, ameaça de memorização (H)
- `docs/hipoteses-e-metricas.md` — hipóteses, variáveis, matriz de tratamento/ordem
- `docs/ambiente-experimento.md` — Java/Maven/JUnit, estrutura `trials/`
- `docs/issues-planejadas.md` — Issues da S02
