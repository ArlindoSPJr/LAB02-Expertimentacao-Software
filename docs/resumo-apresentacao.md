# IA vs. Codificação Manual — Resumo para Apresentação

## 1. Contexto

Assistentes de IA generativa (como o Claude Code) prometem acelerar a
programação, mas ainda é pouco claro se esse ganho de velocidade vem
acompanhado de custos em correção ou em qualidade estrutural do código. Este
trabalho investiga essa troca de forma controlada, comparando diretamente
codificação assistida por IA e codificação manual na resolução de exercícios
de programação (katas).

Cada um dos 3 integrantes do grupo resolveu 6 katas de dificuldade equivalente, metade com assistência de IA e metade manualmente, em ordem contrabalanceada para neutralizar efeito de aprendizado. Isso resulta em **18 execuções** (9 com IA, 9 manuais). Cada execução teve um **limite rígido de 35 minutos**; nenhuma das 18 execuções atingiu esse limite sem terminar.

## 2. Objetivo do estudo (GQM)

> **Analisar** o uso de assistentes de IA generativa na resolução de tarefas
> de programação, **com o propósito de** comparar seu efeito frente à
> codificação manual, **com respeito a** tempo de resolução, qualidade
> funcional (defeitos) e qualidade estrutural do código produzido, **do
> ponto de vista** do grupo pesquisador, **no contexto de** katas de
> dificuldade equivalente resolvidas por estudantes de graduação sob
> condições controladas.

## 3. Tecnologias utilizadas

- **Katas:** Java, com testes de aceitação automatizados (JUnit).
- **Script de Cronometragem e Coleta de Métricas:** Coletas automatizada utilizando script em Python
- **Assistência de IA:** Claude Code
- **Ambiente de desenvolvimento:** Docker para garantir mesmo ambiente para os 3 integrantes
- **Análise estática do código:** Ferramentas dedicadas para complexidade
  ciclomática e para detecção de duplicação de código.

## 4. Perguntas de pesquisa, hipóteses e conclusões

### RQ1 — O uso de IA reduz o tempo de resolução?

**Hipótese inicial:** O tempo será bastante reduzido comparado a codificação manual

**Conclusão:** Ganho de tempo grande e consistente entre todos os
integrantes com o uso de IA.

### RQ2 — O uso de IA reduz a quantidade de defeitos?

**Hipótese inicial:** Acreditamos que não

**Conclusão:** dentro do tempo disponível, a IA não trouxe nem prejuízo nem
ganho de correção — o benefício observado se concentra em velocidade, não em
qualidade funcional.

### RQ3 — O uso de IA altera a complexidade ou a duplicação do código?

**Hipótese inicial:** De maneira geral acreditamos que a IA possa aumentar um pouco a complexidade e a duplicação, mas isso irá depender da forma como cada integrante utiliza a IA

**Conclusão:** nenhuma alteração sistemática na estrutura do código —
diferente do tempo, aqui não há um padrão que se repita entre os
integrantes.

## 5. Métricas exigidas — IA vs. manual (visão geral)

| RQ | Métrica | Com IA | Manual |
|---|---|---|---|
| RQ1 | Tempo até time-to-green (mediana) | 41 s | 1380 s (23 min) |
| RQ1 | Tempo até time-to-green (IQR) | 84 s | 375 s |
| RQ1 | Execuções censuradas (time-box 35 min) | 0 | 0 |
| RQ2 | Taxa de sucesso nos testes (mediana) | 100% | 100% |
| RQ2 | Testes falhando ao final (absoluto) | 0 | 0 |
| RQ3 | Complexidade ciclomática — WMC (mediana) | 10,0 | 11,0 |
| RQ3 | Complexidade ciclomática — WMC (IQR) | 11,0 | 5,0 |
| RQ3 | Duplicação de código (mediana) | 0% | 0% |
| RQ3 | Linhas de código — LOC (mediana) | 42 | 45 |
| RQ3 | Linhas de código — LOC (IQR) | 21 | 16 |
| RQ3 | Complexidade por linha — WMC/LOC (mediana) | 0,33 | 0,27 |

## 6. Limitações a destacar

- **Amostra pequena:** a comparação estatística formal se apoia em apenas 3
  pares de observações (um por integrante), o que limita a confiança
  estatística mesmo diante de efeitos grandes e consistentes, como o de
  tempo (RQ1). Isso deve ser apresentado como limitação de poder estatístico,
  não como ausência de efeito.
- **Ausência de variação em duas métricas:** tanto a taxa de sucesso quanto
  a duplicação de código deram o mesmo resultado (100% e 0%, respectivamente)
  em todas as 18 execuções, o que torna o teste estatístico formal não
  aplicável a essas duas métricas — a conclusão nesses casos vem diretamente
  da observação dos dados, não de um teste de hipótese.
- **Escopo das katas:** por serem exercícios pequenos e isolados, os
  resultados podem não se generalizar diretamente para tarefas de
  manutenção em bases de código maiores e mais complexas, nem para outros
  assistentes de IA ou linguagens de programação.
