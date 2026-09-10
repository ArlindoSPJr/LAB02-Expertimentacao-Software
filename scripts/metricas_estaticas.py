#!/usr/bin/env python3
"""Script de coleta de metricas estaticas de um trial (RQ3: WMC / duplicacao / LOC).

Fluxo (docs/scripts-metricas.md, secao 2), executado sobre o codigo final de um
trial ja encerrado (docs/ambiente-experimento.md, secao 5):
  trials/<integrante>/<kata>/<tratamento>/

  1. Roda o CK (`ck.jar`) sobre a pasta do trial -> le `class.csv` e soma as
     colunas `wmc` e `loc` de todas as classes.
  2. Roda o PMD CPD sobre a mesma pasta -> le o XML de saida e soma as linhas
     de cada bloco de duplicacao encontrado.
  3. Calcula `pct_linhas_duplicadas = linhas_duplicadas / loc` (loc vem do CK,
     unica fonte de verdade - nao ha contagem de LOC em paralelo).
  4. Grava uma linha (CSV) em resultados/metricas-estaticas.csv.

Ferramentas e versoes fixadas no Dockerfile (docs/ambiente-experimento.md):
  CK_JAR (env, default /opt/ck/ck.jar) e PMD_BIN (env, default /opt/pmd/bin/pmd).
"""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

CK_JAR_PADRAO = "/opt/ck/ck.jar"
PMD_BIN_PADRAO = "/opt/pmd/bin/pmd"
CPD_MINIMO_TOKENS = 50

CSV_FIELDS = [
    "integrante",
    "kata",
    "tratamento",
    "wmc",
    "loc",
    "linhas_duplicadas",
    "pct_linhas_duplicadas",
]


def _rodar_ck(trial_dir: Path, ck_jar: str, saida_dir: Path) -> tuple[int, int]:
    """Roda o CK sobre trial_dir e retorna (wmc_total, loc_total).

    Se nao houver classes Java (ou o CK nao gerar class.csv), retorna (0, 0).
    """
    subprocess.run(
        [
            "java", "-jar", ck_jar,
            str(trial_dir),
            "false",  # use jars
            "0",      # max files per partition (0 = automatico)
            "false",  # variables and fields metrics
            str(saida_dir) + os.sep,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    class_csv = saida_dir / "class.csv"
    if not class_csv.exists():
        return 0, 0

    wmc_total = 0
    loc_total = 0
    with class_csv.open(newline="", encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            wmc_total += int(float(linha["wmc"] or 0))
            loc_total += int(float(linha["loc"] or 0))
    return wmc_total, loc_total


def _rodar_pmd_cpd(trial_dir: Path, pmd_bin: str) -> int:
    """Roda o PMD CPD sobre trial_dir e retorna o total de linhas duplicadas.

    CPD sai com codigo 4 quando ACHA duplicacao (nao e erro do script) e 0
    quando nao acha nenhuma - so codigos 1/2/5 sao falha real da ferramenta.
    """
    resultado = subprocess.run(
        [
            pmd_bin, "cpd",
            "--minimum-tokens", str(CPD_MINIMO_TOKENS),
            "--dir", str(trial_dir),
            "--language", "java",
            "--format", "xml",
        ],
        capture_output=True,
        text=True,
    )
    if resultado.returncode not in (0, 4):
        sys.exit(
            f"PMD CPD falhou (codigo {resultado.returncode}): {resultado.stderr.strip()}"
        )
    if not resultado.stdout.strip():
        return 0

    root = ET.fromstring(resultado.stdout)
    # O XML do CPD usa namespace (xmlns="https://pmd-code.org/schema/cpd-report"),
    # entao "duplication" sem qualificar o namespace nao daria match.
    ns = {"cpd": root.tag.split("}")[0].strip("{")} if root.tag.startswith("{") else {}
    tag = "cpd:duplication" if ns else "duplication"
    return sum(int(dup.get("lines", 0)) for dup in root.findall(tag, ns))


def _gravar_resultado(saida_csv: Path, linha: dict) -> None:
    saida_csv.parent.mkdir(parents=True, exist_ok=True)
    arquivo_novo = not saida_csv.exists()
    with saida_csv.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if arquivo_novo:
            writer.writeheader()
        writer.writerow(linha)


def cmd_coletar(args: argparse.Namespace) -> None:
    trial_dir = Path(args.trial_dir).resolve()
    saida_csv = Path(args.saida)
    ck_jar = args.ck_jar
    pmd_bin = args.pmd_bin

    with tempfile.TemporaryDirectory() as ck_saida_dir:
        wmc_total, loc_total = _rodar_ck(trial_dir, ck_jar, Path(ck_saida_dir))

    linhas_duplicadas = _rodar_pmd_cpd(trial_dir, pmd_bin)
    pct_duplicadas = round(linhas_duplicadas / loc_total, 4) if loc_total else 0.0

    linha = {
        "integrante": args.integrante,
        "kata": args.kata,
        "tratamento": args.tratamento,
        "wmc": wmc_total,
        "loc": loc_total,
        "linhas_duplicadas": linhas_duplicadas,
        "pct_linhas_duplicadas": pct_duplicadas,
    }
    _gravar_resultado(saida_csv, linha)
    print(f"[metricas] trial coletado: {linha}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Coleta metricas estaticas (WMC/CK, duplicacao/PMD-CPD, LOC) de um trial."
    )
    parser.add_argument("--trial-dir", required=True, help="Diretorio do trial (codigo Java final).")
    parser.add_argument("--integrante", required=True)
    parser.add_argument("--kata", required=True)
    parser.add_argument("--tratamento", required=True, choices=["com-ia", "manual"])
    parser.add_argument("--saida", default="resultados/metricas-estaticas.csv")
    parser.add_argument(
        "--ck-jar", default=os.environ.get("CK_JAR", CK_JAR_PADRAO),
        help="Caminho do ck.jar (default: $CK_JAR ou " + CK_JAR_PADRAO + ").",
    )
    parser.add_argument(
        "--pmd-bin", default=os.environ.get("PMD_BIN", PMD_BIN_PADRAO),
        help="Caminho do binario `pmd` (default: $PMD_BIN ou " + PMD_BIN_PADRAO + ").",
    )
    parser.set_defaults(func=cmd_coletar)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
