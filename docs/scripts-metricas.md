# Escopo dos Scripts de Coleta (RQ1, RQ2, RQ3)

Este documento detalha o escopo técnico das duas issues de scripts da S01 (`docs/issues-planejadas.md`), ambas do Integrante 2, esclarecendo o que cada uma coleta e por quê. Complementa `docs/ambiente-experimento.md` (que fixa o ambiente) — aqui o foco é o que os scripts precisam produzir para cada RQ.

Nenhuma das duas issues depende da issue de hipóteses/variáveis (Integrante 3): as métricas de RQ1 e RQ3 já são fixas pelo desenho do experimento; RQ2 tem uma escolha de agregação em aberto, mas ela não muda o dado bruto a ser coletado (ver seção 2).

## 1. Script de cronometragem — cobre RQ1 e RQ2

Um único script, não dois. Para saber que "todos os testes passaram" (necessário para RQ1) o script já precisa rodar os testes e contar quantos passaram (o dado de RQ2) — então ambos saem da mesma execução.

**Fluxo por trial:**
1. `start_trial(kata, tratamento, integrante)` — marca timestamp de início.
2. Roda os testes de aceitação (`mvn test`) periodicamente ou sob comando manual durante o trial, sem parar o cronômetro.
3. Ao passar todos os testes, ou ao atingir 35 min (time-box, só pode ser reduzido, nunca aumentado):
   - marca timestamp de fim,
   - calcula duração = fim − início,
   - lê o resultado do `mvn test` (via saída do Surefire) e extrai `testes_passando` e `testes_total`,
   - marca `censurado = true/false` (true se parou por time-box sem passar todos).

**Saída por trial (ex. CSV/JSON):**

| campo | RQ que usa | observação |
|---|---|---|
| `tempo_segundos` | RQ1 | tempo até time-to-green, ou 35min se censurado |
| `censurado` | RQ1 | trial censurado não é descartado, é registrado como 35min |
| `testes_passando` | RQ2 | dado bruto |
| `testes_total` | RQ2 | dado bruto |

**Sobre RQ2 especificamente:** o script salva o dado bruto (`testes_passando`/`testes_total`), não uma métrica já agregada. A decisão de reportar como **taxa de sucesso** (`testes_passando / testes_total`) ou como **nº absoluto de falhas** (`testes_total - testes_passando`) é feita na análise da S03, a partir dessas duas colunas — não exige alterar o script depois que a escolha for formalizada pelo Integrante 3.

## 2. Script de métricas estáticas — cobre RQ3

RQ3 pede duas métricas, de duas ferramentas diferentes, mais uma métrica de controle — não é só CK.

**Fluxo por trial (executado sobre o código final do trial, ao encerrar):**
1. Chama **CK** (`.jar`) via `subprocess` sobre a pasta do trial → lê o CSV de saída (`class.csv`/`method.csv`) e extrai **WMC** (complexidade ciclomática somada por classe).
2. Chama **PMD** com o módulo **CPD** (`.jar`) via `subprocess` sobre a mesma pasta → lê o relatório de duplicação e calcula **% de linhas duplicadas** (linhas duplicadas / total de linhas).
3. Calcula **LOC** (linhas de código) — pode vir do próprio relatório do CK (que também reporta LOC por classe) ou ser somado diretamente a partir dos arquivos `.java` do trial em Python. LOC é obrigatório sempre que WMC/duplicação forem reportados (métrica de controle, código gerado por IA pode ser mais verboso).

**Saída por trial (ex. CSV/JSON):**

| campo | ferramenta | RQ que usa |
|---|---|---|
| `wmc` | CK | RQ3 (complexidade) |
| `pct_linhas_duplicadas` | PMD-CPD | RQ3 (duplicação) |
| `loc` | CK ou contagem própria | RQ3 (controle) |

## 3. Resumo

| Script | O que coleta | RQs cobertas |
|---|---|---|
| Cronometragem | tempo, censura, testes passando/total | RQ1, RQ2 |
| Métricas estáticas | WMC (CK), % duplicação (PMD-CPD), LOC | RQ3 |

## Referências

- `docs/ambiente-experimento.md` — ambiente fixado (linguagem, ferramentas, versões)
- `docs/issues-planejadas.md` — issues da S01
- `docs/enunciado.md` — métricas candidatas por RQ
