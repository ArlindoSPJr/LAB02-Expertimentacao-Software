# Ambiente único do experimento: JDK 21 + Maven (para as katas) + Python 3 (para
# cronometragem e coleta de métricas). Ver docs/ambiente-experimento.md.
FROM maven:3.9.9-eclipse-temurin-21

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Baixa as dependências Maven antes de copiar o resto, para cachear a camada.
COPY pom.xml .
RUN mvn -B dependency:go-offline

COPY . .

CMD ["bash"]
