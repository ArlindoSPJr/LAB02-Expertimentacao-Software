# Ambiente único do experimento: JDK 21 + Maven (para as katas) + Python 3 (para
# cronometragem e coleta de métricas). Ver docs/ambiente-experimento.md.
FROM maven:3.9.9-eclipse-temurin-21

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    git \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# CK 0.7.0 (complexidade ciclomática/WMC para RQ3): sem jar publicado em Releases,
# construido a partir do codigo-fonte na tag fixada (docs/ambiente-experimento.md).
RUN git clone --branch ck-0.7.0 --depth 1 https://github.com/mauricioaniche/ck.git /opt/ck-src \
    && cd /opt/ck-src \
    && mvn -q -B -DskipTests package \
    && mkdir -p /opt/ck \
    && cp target/ck-0.7.0-jar-with-dependencies.jar /opt/ck/ck.jar \
    && rm -rf /opt/ck-src ~/.m2/repository/com/github/mauricioaniche

# PMD 7.27.0 (modulo CPD para % de linhas duplicadas, RQ3).
RUN curl -fsSL -o /tmp/pmd-dist.zip \
    https://github.com/pmd/pmd/releases/download/pmd_releases%2F7.27.0/pmd-dist-7.27.0-bin.zip \
    && unzip -q /tmp/pmd-dist.zip -d /opt \
    && mv /opt/pmd-bin-7.27.0 /opt/pmd \
    && rm /tmp/pmd-dist.zip

ENV CK_JAR=/opt/ck/ck.jar
ENV PMD_BIN=/opt/pmd/bin/pmd

WORKDIR /workspace

# Baixa as dependências Maven antes de copiar o resto, para cachear a camada.
COPY pom.xml .
RUN mvn -B dependency:go-offline

COPY . .

CMD ["bash"]
