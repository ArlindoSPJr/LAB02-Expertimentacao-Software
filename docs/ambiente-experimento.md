# Ambiente do Experimento

Este documento fixa o ambiente usado em todos os trials do LAB02 (Passo 2 — Preparação do Experimento, `docs/enunciado.md`), para que os três integrantes executem sob as mesmas condições e para que o Relatório Final tenha metodologia reprodutível ("ambiente, katas usados, assistente de IA e versão").

Essas decisões são vinculantes para todos os trials da S02: mudar linguagem, IDE ou assistente de IA no meio do experimento invalidaria a comparação entre tratamentos.

## 1. Linguagem e versão

- **Linguagem das katas: Java.** Escolhida para habilitar diretamente as ferramentas de métricas estáticas citadas em primeiro lugar no enunciado (RQ3): **CK** (complexidade ciclomática / WMC) e **PMD / PMD-CPD** (duplicação de código).
- **Versão do JDK: 21 (LTS)**, fixada via imagem Docker (seção 1.1) — não depende da instalação individual de cada integrante.
- **Build/test runner:** Maven 3.9.9, com JUnit 5.10 para os testes de aceitação de cada kata (ver `pom.xml` na raiz). Usar o mesmo `pom.xml`/estrutura de projeto para todos os katas, para que o script de coleta de métricas (Python) e o CK/PMD rodem sobre um layout previsível.

### 1.1 Ambiente containerizado (Docker)

Para eliminar divergência de versões de JDK/Maven/Python entre as máquinas dos 3 integrantes, o ambiente roda em um container Docker único, definido em `Dockerfile` na raiz do repositório: imagem base `maven:3.9.9-eclipse-temurin-21` (JDK 21 + Maven 3.9.9) com Python 3 instalado por cima. Java e Python ficam na **mesma** imagem/container — não em containers separados — porque os scripts Python de cronometragem/métricas precisam invocar `mvn`, CK e PMD como subprocessos locais.

Uso básico:
```
docker build -t lab02-experimento .
docker run -it -v "${PWD}:/workspace" lab02-experimento
```
Dentro do container: `mvn test`, `python3 --version`, etc. já disponíveis. A integração com VS Code (Dev Containers) e um `docker-compose.yml` de conveniência ficam para uma etapa seguinte — por ora o container é usado via `docker run` manual.

## 2. Linguagem dos scripts de suporte

Os scripts de cronometragem e de coleta de métricas estáticas (issues separadas da S01, de outro integrante) são escritos em **Python**. Isso é ortogonal à linguagem das katas: os scripts Python orquestram a execução — cronometram o trial, disparam `mvn test`, invocam CK e PMD como processos externos (ex. via `subprocess`) sobre o código Java, e consolidam os resultados (tempo, nº de testes passando, complexidade, duplicação, LOC) em um formato tabular (CSV/JSON) para a análise da S03.

### Resumo por linguagem

| O quê | Linguagem | Ferramenta/framework |
|---|---|---|
| Código das katas (a solução em si) | Java | Maven + JUnit 5 |
| Testes de aceitação de cada kata | Java | JUnit 5 |
| Script de cronometragem (start/stop trial, time-box 35min) | Python | script próprio |
| Script de coleta de métricas estáticas | Python | chama CK (`.jar`) e PMD/PMD-CPD (`.jar`) como processo externo via `subprocess` |
| Análise estatística (Wilcoxon, mediana/IQR) — S03 | Python | pandas + scipy |
| Dashboard de visualização — S03 | Python | pandas + matplotlib/seaborn |

Java fica restrito ao código das katas; todo o resto (cronometragem, coleta, análise, dashboard) é Python — os scripts Python invocam CK e PMD por fora, sem que ninguém precise escrever Java além das katas.

## 3. IDE

- **VS Code**, usado nos dois tratamentos (com e sem IA) pelos 3 integrantes — manter a mesma ferramenta de edição entre tratamentos evita que o editor vire uma variável de confusão.
- Extensões recomendadas: Extension Pack for Java (Language Support for Java, Debugger, Maven, Test Runner). Nenhuma extensão de autocomplete de IA (Copilot, etc.) deve ficar ativa em nenhum dos dois tratamentos — a única fonte de assistência de IA permitida é o Claude Code, e só nos trials "com IA" (ver seção 4).

## 4. Assistente de IA

- **Assistente único: Claude Code** (CLI/agente), instalado via npm, usado da mesma forma pelos 3 integrantes em todos os trials "com IA".
- **Versão:** registrar a versão do `claude` CLI usada por cada integrante (`claude --version`) na seção 6, para reprodutibilidade — atualizações do CLI entre integrantes ou entre sprints devem ser evitadas ou, se inevitáveis, registradas.

### Regras de uso nos trials "com IA"
- Permitido: chat, leitura/edição de arquivos, execução de comandos (rodar testes, etc.) via Claude Code, dentro do time-box de 35 minutos do trial.
- Opcional (não obrigatório, mas recomendado para discussão qualitativa — enunciado, RQ1): registrar o número de prompts/interações por trial.
- O cronômetro do trial continua correndo enquanto a IA está em uso — não há pausa por causa da IA.

### Regras nos trials "sem IA" (manual)
- Claude Code não é iniciado nesse trial (nenhuma sessão aberta na pasta do kata).
- Nenhuma extensão de autocomplete de IA ativa no VS Code.
- Apenas documentação oficial/consulta manual é permitida (equivalente ao que seria permitido em qualquer ambiente de programação sem IA).

## 5. Estrutura de pastas dos trials

Cada trial (kata × tratamento × integrante) fica isolado em seu próprio diretório, para que os scripts de cronometragem/métricas rodem sobre um caminho previsível e para evitar contaminação entre tratamentos:

```
trials/<integrante>/<kata>/<tratamento>/
```

Onde `<tratamento>` é `com-ia` ou `manual`. Cada trial começa a partir de um template limpo do kata (enunciado + testes de aceitação, sem código de solução), sem histórico de chat de trials anteriores — uma sessão nova do Claude Code por trial "com IA".


## Referências

- Regras de tratamento, katas e sprints: `docs/entendimento-e-planejamento.md`
- Issues planejadas: `docs/issues-planejadas.md`
- Enunciado original: `docs/enunciado.md`
