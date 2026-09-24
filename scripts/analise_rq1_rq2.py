#!/usr/bin/env python3
"""Analise estatistica de RQ1 (tempo) e RQ2 (defeitos), issue #19.

Le resultados/tempos.csv (saida do scripts/cronometragem.py) e produz:
  - estatistica descritiva (mediana/IQR) por tratamento, para tempo e
    taxa de sucesso dos testes;
  - teste de Wilcoxon signed-rank pareado por integrante (cada um dos
    3 integrantes contribui um par: mediana das katas com-ia dele vs
    mediana das katas manual dele) para H1_1 (tempo) e H1_2 (taxa de
    sucesso).

Nota de desenho (ver docs/hipoteses-e-metricas.md): o documento original
descreve o par como "mesmo integrante, mesma kata, com IA vs sem IA",
mas cada integrante resolveu cada kata uma unica vez (nunca as duas
formas) - o pareamento real possivel e por integrante (N=3), nao por
kata. Essa adaptacao esta documentada aqui e deve ser citada no
Relatorio Final.

Uso: python scripts/analise_rq1_rq2.py [--csv resultados/tempos.csv]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import wilcoxon


def carregar(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["taxa_sucesso"] = df["testes_passando"] / df["testes_total"]
    return df


def descritiva_por_tratamento(df: pd.DataFrame) -> pd.DataFrame:
    def iqr(s: pd.Series) -> float:
        return s.quantile(0.75) - s.quantile(0.25)

    return df.groupby("tratamento").agg(
        n=("tempo_segundos", "count"),
        tempo_mediana=("tempo_segundos", "median"),
        tempo_iqr=("tempo_segundos", iqr),
        taxa_sucesso_mediana=("taxa_sucesso", "median"),
        taxa_sucesso_iqr=("taxa_sucesso", iqr),
        trials_censurados=("censurado", "sum"),
    )


def pares_por_integrante(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    """Um par por integrante: mediana(com-ia) vs mediana(manual)."""
    agregado = df.groupby(["integrante", "tratamento"])[coluna].median().unstack("tratamento")
    return agregado.dropna()


def testar_wilcoxon(pares: pd.DataFrame, label: str) -> None:
    print(f"\n--- {label} ---")
    print(pares.to_string())

    com_ia = pares["com-ia"]
    manual = pares["manual"]
    diffs = com_ia - manual

    if (diffs == 0).all():
        print(
            "Todas as diferencas pareadas sao zero (sem variancia entre "
            "tratamentos) - Wilcoxon nao e aplicavel; nao ha evidencia de "
            "diferenca a testar."
        )
        return

    try:
        estatistica, p_valor = wilcoxon(com_ia, manual, alternative="two-sided")
        print(f"Wilcoxon signed-rank: estatistica={estatistica:.4f}, p-valor={p_valor:.4f}")
    except ValueError as exc:
        print(f"Wilcoxon nao pode ser calculado: {exc}")

    print(
        f"N de pares = {len(pares)} (um por integrante) - poder estatistico "
        "muito baixo com N=3; ver docs/ameacas-validade.md."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default="resultados/tempos.csv")
    args = parser.parse_args()

    df = carregar(Path(args.csv))

    print("=== Estatistica descritiva por tratamento (RQ1 e RQ2) ===")
    print(descritiva_por_tratamento(df).to_string())

    pares_tempo = pares_por_integrante(df, "tempo_segundos")
    testar_wilcoxon(pares_tempo, "RQ1 - Tempo ate time-to-green (H1_1)")

    pares_taxa = pares_por_integrante(df, "taxa_sucesso")
    testar_wilcoxon(pares_taxa, "RQ2 - Taxa de sucesso dos testes (H1_2)")


if __name__ == "__main__":
    main()
