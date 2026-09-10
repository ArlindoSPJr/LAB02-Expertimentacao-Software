# Ameaças à Validade

Este documento cobre o item (H) do Passo 1 — Desenho do Experimento (`docs/enunciado.md`,
linha 49): ameaças à validade do experimento, junto das mitigações já adotadas (ou a
adotar) pelo grupo. Complementa `docs/hipoteses-e-metricas.md` (hipóteses e métricas) e
`docs/ambiente-experimento.md` (ambiente fixado) — aqui o foco é o que pode invalidar ou
enviesar a comparação entre os tratamentos `com-ia` e `manual`.

Classificação adotada (Wohlin et al., padrão em experimentos de Engenharia de Software):
validade de conclusão estatística, interna, de construto e externa.

## 1. Validade de Conclusão Estatística

Diz respeito a se a relação observada entre tratamento e variável dependente é real (não
ruído/acaso).

- **Tamanho amostral pequeno.** Cada integrante roda apenas 4–6 trials (2–3 por
  tratamento), e o N total do grupo (3 integrantes) fica na casa de 12–18 trials — poder
  estatístico baixo para detectar efeitos pequenos ou moderados. *Mitigação:* uso do teste
  de Wilcoxon signed-rank (não paramétrico, adequado a N pequeno) em vez de testes que
  assumem normalidade, e mediana/IQR em vez de média/desvio-padrão nas estatísticas
  descritivas (`docs/hipoteses-e-metricas.md`, seção 4). Isso reduz o risco de conclusões
  incorretas, mas não resolve a limitação de poder — o Relatório Final deve declarar essa
  limitação explicitamente ao interpretar um resultado não significativo.
- **Confiabilidade da medição do tempo.** Cronometragem manual (esquecer de rodar
  `start`/`stop` no instante certo, ou de registrar o time-box) introduziria ruído
  sistemático. *Mitigação:* script único e padronizado (`scripts/cronometragem.py`,
  issue #5) usado da mesma forma pelos 3 integrantes, eliminando a variação de
  processo manual de cronometragem.
- **Censura tratada como valor único.** Trials censurados em 35 min entram na análise
  como exatamente 2100 s, misturando um trial que faltavam segundos para passar com um
  que mal começou. Isso é uma limitação conhecida e aceita (ver `docs/enunciado.md`,
  linha 31: descartar distorceria a comparação a favor do tratamento com mais falhas) —
  o teste fica conservador a favor de H0 quando um tratamento acumula mais censuras, o
  que deve ser mencionado na discussão dos resultados (S03).

## 2. Validade Interna

Diz respeito a se o tratamento (uso de IA) é de fato a causa do efeito observado, e não
alguma variável de confusão não controlada.

- **Efeito de aprendizado entre katas.** Ao longo da sessão, o integrante naturalmente
  fica mais rápido/familiarizado com o processo (ler enunciado, rodar testes, usar o
  ambiente), independente do tratamento — os últimos katas tenderiam a ser mais rápidos
  mesmo sem IA. *Mitigação:* desenho crossover contrabalanceado — a ordem
  com-IA/sem-IA é alternada entre os integrantes (`docs/ambiente-experimento.md`,
  `docs/entendimento-e-planejamento.md`, seção 3), de forma que o efeito de aprendizado
  se distribui igualmente entre os dois tratamentos ao longo do grupo, em vez de
  favorecer sistematicamente um deles.
- **Efeito de fadiga.** Se todos os trials de um integrante forem executados em uma
  única sessão longa, o cansaço pode degradar o desempenho nos últimos trials
  independentemente do tratamento, na direção oposta ao efeito de aprendizado acima.
  *Mitigação a adotar:* recomendar pausas entre trials e, quando possível, distribuir os
  trials de cada integrante em mais de uma sessão — a ser registrado no Relatório Final
  como parte da metodologia.
- **Familiaridade prévia desigual com a ferramenta de IA.** Os 3 integrantes podem ter
  níveis diferentes de experiência prévia com Claude Code, confundindo "efeito da IA"
  com "habilidade de usar a IA". *Mitigação:* mesmo assistente para todos
  (`docs/ambiente-experimento.md`, seção 4) reduz a variação entre ferramentas, mas não
  elimina a diferença de familiaridade entre pessoas — essa diferença deve ser
  registrada no Relatório Final (experiência prévia de cada integrante com o Claude
  Code) como covariável qualitativa na discussão, já que o desenho within-subject
  compara cada integrante consigo mesmo (mitiga parcialmente, pois a familiaridade afeta
  igualmente os trials com IA de um mesmo integrante).
- **Contaminação entre integrantes.** Se um integrante comentar com os outros como
  resolveu um kata antes de todos terminarem seus próprios trials daquele kata, quem
  ouve por último resolve mais rápido por já conhecer a solução — efeito independente do
  tratamento. *Mitigação a adotar:* regra de processo — não discutir a solução de um
  kata com os colegas até que os 3 integrantes tenham concluído seus trials daquele
  kata (com e sem IA).
- **Vazamento de solução dentro do próprio integrante.** Não se aplica entre os dois
  tratamentos de um mesmo integrante: pelo desenho (`docs/entendimento-e-planejamento.md`,
  seção 3), cada integrante resolve cada kata **uma única vez** (ou com IA, ou sem IA) —
  não há repetição do mesmo kata pelo mesmo integrante nos dois tratamentos, então não há
  "segunda tentativa já sabendo a resposta" dentro do próprio integrante.
- **Ambiente físico desigual entre integrantes.** O container Docker fixa
  JDK/Maven/Python (`docs/ambiente-experimento.md`, seção 1.1), mas não fixa hardware
  (CPU/RAM da máquina de cada integrante) nem latência de rede até o serviço de IA —
  variações aí afetam o tempo de build/teste e a responsividade do assistente,
  adicionando ruído ao tempo medido, ainda que igualmente distribuído entre os dois
  tratamentos de um mesmo integrante (não enviesa a comparação pareada, mas aumenta a
  variância geral).
- **Interrupções não controladas durante o trial** (notificações, mensagens) —
  *mitigação a adotar:* recomendar aos integrantes silenciar notificações durante os 35
  minutos do trial.

## 3. Validade de Construto

Diz respeito a se as métricas coletadas realmente medem os conceitos que as RQs
pretendem avaliar (produtividade, defeitos, qualidade estrutural).

- **Time-to-green como proxy de "produtividade".** Mede apenas até quando os testes de
  aceitação passam, não a qualidade do processo (ex.: um trial pode passar nos testes
  com uma solução frágil ou pouco legível e ser contado igual a uma solução limpa).
  *Mitigação:* RQ3 (complexidade/duplicação/LOC) existe justamente para capturar a
  dimensão de qualidade estrutural que o tempo sozinho não cobre — mas nenhuma métrica
  aqui avalia legibilidade/manutenibilidade subjetiva.
- **Nº de testes passando como proxy de "defeitos".** Testes de aceitação de um kata
  pequeno cobrem um conjunto finito e possivelmente incompleto de casos — passar em
  todos os testes não garante ausência de defeitos, só ausência de defeitos *cobertos
  pelos testes fornecidos*. Além disso, katas com poucos testes têm granularidade
  grosseira (ex.: 3 testes → só é possível marcar 0%, 33%, 66% ou 100%), então a taxa de
  sucesso é menos sensível a diferenças pequenas em katas com poucos testes.
- **Complexidade ciclomática e duplicação como proxy de "qualidade estrutural".** WMC
  (CK) e % de duplicação (PMD-CPD) são métricas estáticas objetivas, mas não capturam
  nomeação, organização ou legibilidade — código com baixa complexidade ciclomática pode
  ainda ser mal estruturado. *Mitigação:* LOC como métrica de controle obrigatória
  (`docs/hipoteses-e-metricas.md`, seção 3) evita que a comparação seja distorcida só
  pela verbosidade do código gerado com IA.
- **Time-box de 35 min como proxy de "capacidade de resolver a tarefa".** Um trial
  censurado aos 35 min pode estar a segundos de passar ou ter mal começado — o desenho
  atual (censura = 2100 s fixo) não distingue os dois casos na métrica primária. A
  variável `testes_passando/testes_total` no momento da censura (RQ2) parcialmente
  compensa isso ao registrar o quão perto o trial chegou de passar.

## 4. Validade Externa

Diz respeito a se os resultados generalizam além das condições específicas deste
experimento.

- **Amostra pequena e não representativa.** Apenas 3 integrantes, todos estudantes de
  graduação da mesma turma/disciplina — os resultados não generalizam para
  desenvolvedores profissionais, seniores, ou com formação muito diferente.
- **Katas pequenos e autocontidos.** Exercícios curtos, resolvidos do zero, não
  representam tarefas reais de manutenção em bases de código grandes/legadas, onde
  entender código existente pesa mais que escrever código novo — cenário em que o
  comportamento de um assistente de IA pode ser bem diferente do observado aqui.
- **Um único assistente de IA (Claude Code).** Resultados são específicos a essa
  ferramenta/modelo; não generalizam para outros assistentes (GitHub Copilot, ChatGPT,
  Gemini), que têm interfaces, modelos e modos de interação diferentes.
- **Uma única linguagem (Java).** Fixada para habilitar CK/PMD (RQ3,
  `docs/ambiente-experimento.md`, seção 1) — os resultados podem não generalizar para
  outras linguagens, especialmente as mais ou menos representadas nos dados de
  treinamento do assistente de IA.
- **Katas pouco indexados/autorais, por desenho.** Escolhidos deliberadamente para
  reduzir o risco de memorização pela IA (`docs/enunciado.md`, linha 49, e
  `docs/entendimento-e-planejamento.md`, seção 2) — mas isso é uma faca de dois gumes
  para a validade externa: a maioria dos problemas de programação do mundo real *são*
  bem representados nos dados de treinamento de um assistente de IA, então este
  experimento pode subestimar o ganho de produtividade da IA em cenários comuns, em
  troca de isolar melhor o efeito de "assistência" (em vez de "memorização de
  solução") — um trade-off deliberado entre validade de construto (medir assistência
  de fato) e validade externa (generalizar para o uso cotidiano), que deve ser discutido
  explicitamente no Relatório Final.

## 5. Resumo

| Ameaça | Categoria | Mitigação |
|---|---|---|
| N pequeno / poder estatístico baixo | Conclusão | Wilcoxon + mediana/IQR; limitação declarada no relatório |
| Ruído na cronometragem manual | Conclusão | Script único de cronometragem (`scripts/cronometragem.py`) |
| Censura como valor único (2100s) | Conclusão | Registrada, não descartada; discutida na análise |
| Efeito de aprendizado entre katas | Interna | Crossover contrabalanceado entre integrantes |
| Fadiga em sessões longas | Interna | Pausas/múltiplas sessões (a adotar) |
| Familiaridade prévia desigual com a IA | Interna | Mesmo assistente para todos; registrar experiência prévia no relatório |
| Contaminação entre integrantes | Interna | Não discutir solução até todos concluírem o kata (a adotar) |
| Ambiente físico (hardware/rede) desigual | Interna | Docker fixa JDK/Maven/Python; hardware/rede fora de controle |
| Interrupções durante o trial | Interna | Silenciar notificações (a adotar) |
| Testes de aceitação incompletos / granularidade grosseira | Construto | RQ3 como métrica complementar de qualidade |
| Complexidade/duplicação não capturam legibilidade | Construto | LOC como controle obrigatório |
| Amostra pequena e pouco representativa | Externa | Declarada como limitação do relatório |
| Katas pequenos/autocontidos vs. manutenção real | Externa | Fora do escopo deste laboratório |
| Assistente e linguagem únicos | Externa | Fixados por restrição de ferramentas (CK/PMD); declarado no relatório |
| Katas pouco indexados vs. uso cotidiano da IA | Externa | Trade-off deliberado; discutido no relatório |

## Referências

- `docs/enunciado.md` — item (H) do Passo 1, ameaças citadas no enunciado original
- `docs/entendimento-e-planejamento.md` — entendimento geral do experimento
- `docs/ambiente-experimento.md` — ambiente fixado (linguagem, IDE, assistente de IA)
- `docs/hipoteses-e-metricas.md` — hipóteses e métricas por RQ
- `docs/scripts-metricas.md` — dados brutos coletados por trial
