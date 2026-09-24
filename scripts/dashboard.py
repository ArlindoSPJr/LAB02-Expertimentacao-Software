#!/usr/bin/env python3
"""Dashboard de visualizacao (Passo 6), issue do S03 "montar dashboard".

Le resultados/tempos.csv (RQ1/RQ2) e resultados/metricas-estaticas.csv (RQ3),
e gera um painel unico consolidando as comparacoes com-ia vs. manual pedidas
no enunciado (docs/enunciado.md, Passo 6): tempo, taxa de sucesso e metricas
estaticas (WMC, LOC, duplicacao).

Alem dos itens obrigatorios, o painel inclui dois complementos discutidos em
docs/analise-rq1-rq2.md e docs/analise-rq3.md:
  - densidade de complexidade WMC/LOC por tratamento (controle de verbosidade);
  - grafico pareado por integrante (tempo e WMC, com-ia -> manual), que deixa
    visivel o desenho within-subject por tras do teste de Wilcoxon (N=3
    pares) - os boxplots principais agrupam os 18 trials (9 por tratamento)
    para leitura facil, mas a inferencia estatistica real e pareada por
    integrante, e pool-los sem esse painel seria enganoso (ver nota de
    pareamento em docs/analise-rq1-rq2.md, secao 1).

Paleta fixa (docs/analise-rq1-rq2.md / docs/analise-rq3.md usam sempre a
mesma ordem com-ia -> manual): azul para com-ia, laranja para manual - par
validado contra confusao de daltonismo (skill dataviz, references/palette.md).

Uso: python scripts/dashboard.py
     [--tempos resultados/tempos.csv]
     [--metricas resultados/metricas-estaticas.csv]
     [--saida resultados/dashboard]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import wilcoxon

TRATAMENTOS = ["com-ia", "manual"]
COR = {"com-ia": "#2a78d6", "manual": "#eb6834"}
COR_INK = "#0b0b0b"
COR_MUTED = "#898781"
COR_GRID = "#e1e0d9"
COR_SURFACE = "#fcfcfb"


def iqr(s: pd.Series) -> float:
    return s.quantile(0.75) - s.quantile(0.25)


def carregar_tempos(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["taxa_sucesso"] = df["testes_passando"] / df["testes_total"]
    return df


def carregar_metricas(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["wmc_por_loc"] = df["wmc"] / df["loc"]
    return df


def pares_por_integrante(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    """Um par por integrante: mediana(com-ia) vs mediana(manual) - mesmo
    esquema de pareamento de scripts/analise_rq1_rq2.py e scripts/analise_rq3.py."""
    agregado = df.groupby(["integrante", "tratamento"])[coluna].median().unstack("tratamento")
    return agregado.dropna()


def p_valor_wilcoxon(pares: pd.DataFrame) -> float | None:
    diffs = pares["com-ia"] - pares["manual"]
    if (diffs == 0).all():
        return None
    _, p = wilcoxon(pares["com-ia"], pares["manual"], alternative="two-sided")
    return p


def anotar_wilcoxon(ax: plt.Axes, pares: pd.DataFrame) -> None:
    p = p_valor_wilcoxon(pares)
    texto = "Wilcoxon: sem variancia (diffs=0)" if p is None else f"Wilcoxon p={p:.3f} (N={len(pares)} pares/integrante)"
    ax.text(
        0.5, -0.14, texto, transform=ax.transAxes,
        ha="center", va="top", fontsize=8, color=COR_MUTED,
    )


def estilizar_eixo(ax: plt.Axes, titulo: str) -> None:
    ax.set_title(titulo, fontsize=11, color=COR_INK, loc="left", pad=8)
    ax.set_facecolor(COR_SURFACE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COR_GRID)
    ax.spines["bottom"].set_color(COR_GRID)
    ax.tick_params(colors=COR_MUTED, labelsize=8)
    ax.xaxis.label.set_color(COR_MUTED)
    ax.yaxis.label.set_color(COR_MUTED)
    ax.grid(axis="y", color=COR_GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def boxplot_tratamento(ax: plt.Axes, df: pd.DataFrame, coluna: str, titulo: str, ylabel: str, log_y: bool = False) -> None:
    sns.boxplot(
        data=df, x="tratamento", y=coluna, order=TRATAMENTOS,
        hue="tratamento", palette=COR, legend=False,
        width=0.5, linewidth=1.5, fliersize=0, ax=ax,
    )
    sns.stripplot(
        data=df, x="tratamento", y=coluna, order=TRATAMENTOS,
        color=COR_INK, alpha=0.6, size=4, jitter=0.08, ax=ax,
    )
    if log_y:
        ax.set_yscale("log")
    estilizar_eixo(ax, titulo)
    ax.set_xlabel("")
    ax.set_ylabel(ylabel, fontsize=9)


def barra_tratamento(ax: plt.Axes, df: pd.DataFrame, coluna: str, titulo: str, ylabel: str, fmt: str = "{:.2f}") -> None:
    medianas = df.groupby("tratamento")[coluna].median().reindex(TRATAMENTOS)
    cores = [COR[t] for t in TRATAMENTOS]
    barras = ax.bar(TRATAMENTOS, medianas.values, color=cores, width=0.5, zorder=3)
    for barra, valor in zip(barras, medianas.values):
        ax.text(
            barra.get_x() + barra.get_width() / 2, barra.get_height(),
            fmt.format(valor), ha="center", va="bottom", fontsize=9, color=COR_INK,
        )
    estilizar_eixo(ax, titulo)
    ax.set_ylabel(ylabel, fontsize=9)
    topo = medianas.max()
    ax.set_ylim(0, (topo if topo > 0 else 1) * 1.3)


def grafico_pareado(ax: plt.Axes, pares: pd.DataFrame, titulo: str, ylabel: str, log_y: bool = False) -> None:
    ordem = pares["manual"].sort_values().index
    for posicao, integrante in enumerate(ordem):
        linha = pares.loc[integrante]
        ax.plot(
            TRATAMENTOS, [linha["com-ia"], linha["manual"]],
            color=COR_MUTED, linewidth=1, marker="o", markersize=0, zorder=2,
        )
        deslocamento_y = (posicao - (len(ordem) - 1) / 2) * 9
        ax.annotate(
            integrante.replace("integrante-", "P"), (1, linha["manual"]),
            textcoords="offset points", xytext=(6, deslocamento_y), fontsize=7, color=COR_MUTED, va="center",
        )
    for tratamento in TRATAMENTOS:
        ax.scatter(
            [tratamento] * len(pares), pares[tratamento],
            color=COR[tratamento], s=45, zorder=3, edgecolor=COR_SURFACE, linewidth=0.8,
        )
    if log_y:
        ax.set_yscale("log")
    estilizar_eixo(ax, titulo)
    ax.set_xlim(-0.3, 1.5)
    ax.set_ylabel(ylabel, fontsize=9)
    anotar_wilcoxon(ax, pares)


def montar_dashboard(tempos: pd.DataFrame, metricas: pd.DataFrame, saida: Path) -> None:
    saida.mkdir(parents=True, exist_ok=True)
    sns.set_style("white")
    plt.rcParams["font.family"] = "sans-serif"

    fig, eixos = plt.subplots(2, 4, figsize=(20, 9), facecolor=COR_SURFACE)
    fig.suptitle(
        "Assistente de IA vs. codificacao manual - dashboard do experimento (RQ1-RQ3)",
        fontsize=15, color=COR_INK, x=0.02, y=0.985, ha="left", fontweight="bold",
    )
    fig.text(
        0.02, 0.945,
        "Boxplots agrupam os 18 trials (9 por tratamento); paineis pareados (canto inferior direito) mostram os N=3 pares por integrante usados no teste de Wilcoxon.",
        fontsize=9, color=COR_MUTED,
    )

    pares_tempo = pares_por_integrante(tempos, "tempo_segundos")
    pares_taxa = pares_por_integrante(tempos, "taxa_sucesso")
    pares_wmc = pares_por_integrante(metricas, "wmc")
    pares_loc = pares_por_integrante(metricas, "loc")
    pares_dup = pares_por_integrante(metricas, "pct_linhas_duplicadas")
    pares_wmc_loc = pares_por_integrante(metricas, "wmc_por_loc")

    # Linha 1: itens obrigatorios (RQ1, RQ2, RQ3a, LOC de controle)
    boxplot_tratamento(eixos[0, 0], tempos, "tempo_segundos", "RQ1 - Tempo ate time-to-green", "segundos (escala log)", log_y=True)
    anotar_wilcoxon(eixos[0, 0], pares_tempo)

    barra_tratamento(eixos[0, 1], tempos, "taxa_sucesso", "RQ2 - Taxa de sucesso dos testes", "proporcao (0-1)", fmt="{:.0%}")
    anotar_wilcoxon(eixos[0, 1], pares_taxa)

    boxplot_tratamento(eixos[0, 2], metricas, "wmc", "RQ3a - Complexidade (WMC)", "WMC (CK)")
    anotar_wilcoxon(eixos[0, 2], pares_wmc)

    boxplot_tratamento(eixos[0, 3], metricas, "loc", "LOC (metrica de controle)", "linhas de codigo")
    anotar_wilcoxon(eixos[0, 3], pares_loc)

    # Linha 2: RQ3b + complementos (item 9 e item 10)
    barra_tratamento(eixos[1, 0], metricas, "pct_linhas_duplicadas", "RQ3b - Duplicacao de codigo", "% linhas duplicadas", fmt="{:.1f}%")
    anotar_wilcoxon(eixos[1, 0], pares_dup)

    boxplot_tratamento(eixos[1, 1], metricas, "wmc_por_loc", "Complemento - densidade WMC/LOC", "WMC por linha de codigo")
    anotar_wilcoxon(eixos[1, 1], pares_wmc_loc)

    grafico_pareado(eixos[1, 2], pares_tempo, "Complemento - tempo pareado por integrante", "segundos (escala log)", log_y=True)
    grafico_pareado(eixos[1, 3], pares_wmc, "Complemento - WMC pareado por integrante", "WMC")

    legenda = [
        plt.Line2D([0], [0], marker="o", color="none", markerfacecolor=COR["com-ia"], markersize=9, label="com-ia"),
        plt.Line2D([0], [0], marker="o", color="none", markerfacecolor=COR["manual"], markersize=9, label="manual"),
    ]
    fig.legend(handles=legenda, loc="upper right", bbox_to_anchor=(0.995, 1.0), frameon=False, fontsize=10)

    fig.tight_layout(rect=(0, 0, 1, 0.90))
    caminho = saida / "dashboard.png"
    fig.savefig(caminho, dpi=150, facecolor=COR_SURFACE)
    plt.close(fig)
    print(f"Dashboard salvo em {caminho}")


def exportar_resumo(tempos: pd.DataFrame, metricas: pd.DataFrame, saida: Path) -> None:
    resumo_tempo = tempos.groupby("tratamento").agg(
        n=("tempo_segundos", "count"),
        tempo_mediana_s=("tempo_segundos", "median"),
        tempo_iqr_s=("tempo_segundos", iqr),
        taxa_sucesso_mediana=("taxa_sucesso", "median"),
        taxa_sucesso_iqr=("taxa_sucesso", iqr),
        trials_censurados=("censurado", "sum"),
    )
    resumo_metricas = metricas.groupby("tratamento").agg(
        wmc_mediana=("wmc", "median"),
        wmc_iqr=("wmc", iqr),
        loc_mediana=("loc", "median"),
        loc_iqr=("loc", iqr),
        wmc_por_loc_mediana=("wmc_por_loc", "median"),
        wmc_por_loc_iqr=("wmc_por_loc", iqr),
        pct_dup_mediana=("pct_linhas_duplicadas", "median"),
        pct_dup_iqr=("pct_linhas_duplicadas", iqr),
    )
    resumo = resumo_tempo.join(resumo_metricas)
    caminho = saida / "resumo-dashboard.csv"
    resumo.to_csv(caminho)
    print(f"Resumo descritivo salvo em {caminho}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tempos", default="resultados/tempos.csv")
    parser.add_argument("--metricas", default="resultados/metricas-estaticas.csv")
    parser.add_argument("--saida", default="resultados/dashboard")
    args = parser.parse_args()

    tempos = carregar_tempos(Path(args.tempos))
    metricas = carregar_metricas(Path(args.metricas))
    saida = Path(args.saida)

    montar_dashboard(tempos, metricas, saida)
    exportar_resumo(tempos, metricas, saida)


if __name__ == "__main__":
    main()
