#!/usr/bin/env python3
"""Analise estrutural de RQ3 (WMC / duplicacao / LOC), issue #20.

Le resultados/metricas-estaticas.csv (saida do scripts/metricas_estaticas.py)
e produz:
  - estatistica descritiva (mediana/IQR) por tratamento, para WMC, LOC,
    densidade de complexidade (WMC/LOC) e % de linhas duplicadas;
  - teste de Wilcoxon signed-rank pareado por integrante (mesmo esquema de
    pareamento adotado em scripts/analise_rq1_rq2.py - ver a nota de desenho
    la e em docs/analise-rq1-rq2.md) para H1_3a (WMC) e H1_3b (duplicacao).

LOC e reportado sempre junto de WMC como metrica de controle
(docs/hipoteses-e-metricas.md): codigo mais verboso naturalmente acumula
WMC absoluto maior, entao a densidade WMC/LOC tambem e calculada para
isolar esse efeito.

Uso: python scripts/analise_rq3.py [--csv resultados/metricas-estaticas.csv]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import wilcoxon


def carregar(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["wmc_por_loc"] = df["wmc"] / df["loc"]
    return df


def descritiva_por_tratamento(df: pd.DataFrame) -> pd.DataFrame:
    def iqr(s: pd.Series) -> float:
        return s.quantile(0.75) - s.quantile(0.25)

    return df.groupby("tratamento").agg(
        n=("wmc", "count"),
        wmc_mediana=("wmc", "median"),
        wmc_iqr=("wmc", iqr),
        loc_mediana=("loc", "median"),
        loc_iqr=("loc", iqr),
        wmc_por_loc_mediana=("wmc_por_loc", "median"),
        wmc_por_loc_iqr=("wmc_por_loc", iqr),
        pct_dup_mediana=("pct_linhas_duplicadas", "median"),
        pct_dup_iqr=("pct_linhas_duplicadas", iqr),
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
    parser.add_argument("--csv", default="resultados/metricas-estaticas.csv")
    args = parser.parse_args()

    df = carregar(Path(args.csv))

    print("=== Estatistica descritiva por tratamento (RQ3) ===")
    print(descritiva_por_tratamento(df).to_string())

    pares_wmc = pares_por_integrante(df, "wmc")
    testar_wilcoxon(pares_wmc, "RQ3a - Complexidade ciclomatica / WMC (H1_3a)")

    pares_wmc_loc = pares_por_integrante(df, "wmc_por_loc")
    testar_wilcoxon(pares_wmc_loc, "RQ3a (normalizado) - WMC por LOC")

    pares_dup = pares_por_integrante(df, "pct_linhas_duplicadas")
    testar_wilcoxon(pares_dup, "RQ3b - Duplicacao de codigo (H1_3b)")


if __name__ == "__main__":
    main()
