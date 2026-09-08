# Entendimento do Trabalho e Planejamento Inicial

Este documento resume as duas conversas iniciais de alinhamento sobre o LAB02, antes do início da execução. Serve como registro de entendimento compartilhado pelo grupo, ainda sem divisão de responsabilidades entre integrantes.

## 1. Resumo do trabalho

O LAB02 é um **experimento controlado** para comparar, de forma quantitativa, o uso de **assistente de IA** vs. **codificação manual** na resolução de exercícios de programação (katas). O objetivo não é opinar sobre a IA, mas coletar dados reais para responder três perguntas de pesquisa:

- **RQ1 — Tempo:** o uso de IA reduz o tempo até passar em todos os testes de aceitação ("time-to-green")?
- **RQ2 — Defeitos:** o uso de IA reduz a quantidade de testes falhando ao final do tempo?
- **RQ3 — Estrutura do código:** o uso de IA altera a complexidade ciclomática ou a duplicação do código produzido?

## 2. O que é um kata

Um **kata** é um exercício de programação pequeno e autocontido, com **testes automatizados de aceitação** que determinam objetivamente se a solução está correta. É similar a exercícios de LeetCode/HackerRank/Codewars, mas o enunciado recomenda **evitar exercícios muito conhecidos/indexados**: se a IA já "viu" a solução no treinamento dela, ela pode reproduzi-la de memória em vez de efetivamente ajudar a resolver o problema — o que invalidaria a comparação do experimento.

O grupo deve escolher **4 ou 6 katas de dificuldade equivalente** (número par, para dividir exatamente metade dos katas com IA e metade sem, por integrante).

## 3. Como funciona a execução do experimento

- Cada um dos 3 integrantes resolve **todos os katas escolhidos**, individualmente.
- Para cada integrante, **metade dos katas é resolvida com IA habilitada** e a **outra metade sem IA**.
- A ordem entre katas/tratamentos é **contrabalanceada** entre os integrantes, para que nenhum kata específico favoreça sempre o mesmo tratamento (evita viés de "esse kata era mais fácil").
- Cada tentativa individual (kata + tratamento) é um **"trial"**, com **time-box fixo de 35 minutos** (só pode ser reduzido, nunca aumentado).
  - Se os testes passarem antes de 35 min → registra o tempo real (time-to-green).
  - Se não passarem → o trial é encerrado aos 35 min e registrado como **censurado** (não é descartado, apenas marcado como não concluído no prazo).
- Para cada trial, registra-se: tempo até passar nos testes (ou até o time-box), número de testes passando ao final, e métricas estáticas do código final (CK/PMD para Java, ou Radon/jscpd para outras linguagens).

### Como cronometrar (com IA e sem IA)

A lógica de cronometragem **é a mesma para os dois tratamentos** — o cronômetro apenas mede do início ao fim do trial; a diferença entre tratamentos está em como a pessoa resolve o problema (usando ou não IA), não em como o tempo é medido.

Por trial, é preciso registrar:
- Timestamp de início (quando a pessoa começa a ler o kata e programar).
- Timestamp de fim (quando os testes passam todos, ou quando bate o time-box de 35 min).
- Duração total = fim − início.
- Flag indicando se o trial terminou com sucesso ou foi censurado pelo time-box.

Abordagem recomendada: um **script padronizado de cronometragem**, usado por todos os integrantes da mesma forma, com comandos do tipo:
1. `start_trial` — inicia o cronômetro e salva o timestamp de início (recebendo como parâmetro o kata e o tratamento: com_ia ou sem_ia).
2. Execução dos testes a qualquer momento durante o trial, sem parar o cronômetro.
3. `stop_trial` — ao passar todos os testes, registra o timestamp de fim, calcula a duração e salva os dados (kata, tratamento, tempo, nº de testes passando).
4. Um aviso/alarme para os 35 minutos, encerrando o trial mesmo sem sucesso (registrado como censurado).

Esse script não interage com a IA nem restringe o uso dela — apenas mede tempo e roda os testes, de forma idêntica nos dois tratamentos, para manter a comparação justa entre os trials.

## 4. Ordem de execução das sprints

### S01 — Desenho do Experimento + Preparação (5 pts)
O que fazer:
- Definir hipóteses nula e alternativa, variáveis dependentes (tempo, nº de testes passando, métricas estáticas) e independente (uso ou não de IA).
- Escolher os katas (4 ou 6, dificuldade equivalente, baixa indexação).
- Definir o ambiente: linguagem de programação, IDE, assistente de IA único a ser usado em todos os trials.
- Escrever o script de cronometragem/coleta de tempo.
- Escrever o script de coleta de métricas estáticas (CK/PMD ou Radon, conforme a linguagem escolhida).
- Documentar ameaças à validade (efeito aprendizado, memorização de solução pela IA, familiaridade prévia com a ferramenta, etc.).
- Registrar tudo no GitHub Projects (cartões de desenho e preparação).

### S02 — Execução do Experimento + Coleta de Dados (5 pts)
O que fazer:
- Cada integrante resolve todos os katas, metade com IA e metade sem, em ordem contrabalanceada, respeitando o time-box de 35 minutos por trial.
- Registrar, por trial: tempo até passar nos testes (ou censura em 35 min), nº de testes passando ao final, e rodar CK/PMD/Radon sobre o código final.
- Criar uma Issue individual no GitHub Projects para cada kata/tratamento, atribuída ao integrante responsável, e referenciar o número da issue nos commits daquele trial.

### S03 — Análise de Resultados + Dashboard (5 pts)
O que fazer:
- Aplicar teste estatístico de Wilcoxon (pareado, within-subject) para responder RQ1 (tempo) e RQ2 (defeitos/taxa de sucesso), usando mediana e IQR como métricas descritivas.
- Analisar as métricas estruturais (complexidade ciclomática, duplicação, LOC) para responder RQ3.
- Montar um dashboard em Python (Pandas + Matplotlib/Seaborn) com gráficos comparando tempo, taxa de sucesso e métricas estáticas entre os tratamentos.

### Relatório Final (5 pts)
O que fazer:
- Redigir o documento final com: introdução e hipóteses, metodologia detalhada (reproduzível: ambiente, katas usados, assistente de IA e versão), resultados por RQ com as respostas estatísticas, discussão final, e o link do repositório/GitHub Projects do grupo.

## 5. Regras de processo que valem para todas as sprints
- Em toda sprint (S01, S02, S03), cada um dos 3 integrantes precisa ser Assignee de pelo menos uma Issue com artefato de código commitado (script, notebook, gráfico ou trial de kata) — a ausência disso zera a parcela individual daquele integrante na sprint.
- Todos os trials devem ser registrados como Issues individuais no GitHub Projects (uma por kata/tratamento), atribuídas ao integrante responsável.
- Commits sem referência ao número da Issue correspondente não são considerados na correção.
- Até 10% de desconto na nota da sprint por qualidade insuficiente do uso do GitHub Projects (WIP não respeitado, Issues sem Assignee, cartões desatualizados, ausência de evolução semanal).
