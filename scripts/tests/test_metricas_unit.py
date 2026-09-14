"""Testes unitarios (Nivel 1) de scripts/metricas_estaticas.py.

Nao chamam `java -jar ck.jar` nem `pmd cpd` de verdade - o subprocess.run e
substituido (monkeypatch) e as fixtures em scripts/tests/fixtures/ simulam a
saida real dessas ferramentas. Ver plans/testes-unitarios-katas-e-scripts.md.
"""

import argparse
import csv
from pathlib import Path

import pytest

import metricas_estaticas as met

FIXTURES = Path(__file__).parent / "fixtures"


class _ResultadoFake:
    def __init__(self, returncode, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_rodar_ck_soma_wmc_e_loc(tmp_path, monkeypatch):
    monkeypatch.setattr(met.subprocess, "run", lambda *a, **k: None)
    saida_dir = tmp_path / "saida-ck"
    saida_dir.mkdir()
    (saida_dir / "class.csv").write_text(
        (FIXTURES / "ck_class.csv").read_text(encoding="utf-8"), encoding="utf-8"
    )

    wmc, loc = met._rodar_ck(tmp_path, "ck.jar", saida_dir)

    assert wmc == 8   # 5 + 3
    assert loc == 35  # 20 + 15


def test_rodar_ck_sem_class_csv_gerado(tmp_path, monkeypatch):
    monkeypatch.setattr(met.subprocess, "run", lambda *a, **k: None)
    saida_dir = tmp_path / "saida-ck"
    saida_dir.mkdir()

    assert met._rodar_ck(tmp_path, "ck.jar", saida_dir) == (0, 0)


def test_rodar_pmd_cpd_com_duplicacao(tmp_path, monkeypatch):
    conteudo = (FIXTURES / "cpd_com_duplicacao.xml").read_text(encoding="utf-8")
    monkeypatch.setattr(
        met.subprocess, "run", lambda *a, **k: _ResultadoFake(4, stdout=conteudo)
    )

    total = met._rodar_pmd_cpd(tmp_path, "pmd")

    assert total == 20  # 12 + 8 linhas duplicadas na fixture


def test_rodar_pmd_cpd_sem_duplicacao(tmp_path, monkeypatch):
    conteudo = (FIXTURES / "cpd_sem_duplicacao.xml").read_text(encoding="utf-8")
    monkeypatch.setattr(
        met.subprocess, "run", lambda *a, **k: _ResultadoFake(0, stdout=conteudo)
    )

    assert met._rodar_pmd_cpd(tmp_path, "pmd") == 0


def test_rodar_pmd_cpd_stdout_vazio(tmp_path, monkeypatch):
    monkeypatch.setattr(
        met.subprocess, "run", lambda *a, **k: _ResultadoFake(0, stdout="")
    )

    assert met._rodar_pmd_cpd(tmp_path, "pmd") == 0


def test_rodar_pmd_cpd_falha_real_da_ferramenta(tmp_path, monkeypatch):
    monkeypatch.setattr(
        met.subprocess, "run", lambda *a, **k: _ResultadoFake(1, stdout="", stderr="boom")
    )

    with pytest.raises(SystemExit):
        met._rodar_pmd_cpd(tmp_path, "pmd")


def test_cmd_coletar_calcula_pct_duplicadas(tmp_path, monkeypatch):
    monkeypatch.setattr(met, "_rodar_ck", lambda trial_dir, ck_jar, saida_dir: (10, 100))
    monkeypatch.setattr(met, "_rodar_pmd_cpd", lambda trial_dir, pmd_bin: 25)
    saida = tmp_path / "metricas.csv"
    args = argparse.Namespace(
        trial_dir=str(tmp_path), integrante="integrante-1", kata="kata1-placas",
        tratamento="manual", saida=str(saida), ck_jar="ck.jar", pmd_bin="pmd",
    )

    met.cmd_coletar(args)

    linha = next(csv.DictReader(saida.open(encoding="utf-8")))
    assert linha["wmc"] == "10"
    assert linha["loc"] == "100"
    assert linha["linhas_duplicadas"] == "25"
    assert linha["pct_linhas_duplicadas"] == "0.25"


def test_cmd_coletar_loc_zero_nao_gera_zero_division(tmp_path, monkeypatch):
    monkeypatch.setattr(met, "_rodar_ck", lambda trial_dir, ck_jar, saida_dir: (0, 0))
    monkeypatch.setattr(met, "_rodar_pmd_cpd", lambda trial_dir, pmd_bin: 0)
    saida = tmp_path / "metricas.csv"
    args = argparse.Namespace(
        trial_dir=str(tmp_path), integrante="integrante-1", kata="kata1-placas",
        tratamento="manual", saida=str(saida), ck_jar="ck.jar", pmd_bin="pmd",
    )

    met.cmd_coletar(args)

    linha = next(csv.DictReader(saida.open(encoding="utf-8")))
    assert linha["pct_linhas_duplicadas"] == "0.0"


def test_gravar_resultado_grava_cabecalho_uma_unica_vez(tmp_path):
    saida = tmp_path / "metricas.csv"
    linha = {campo: "x" for campo in met.CSV_FIELDS}

    met._gravar_resultado(saida, linha)
    met._gravar_resultado(saida, linha)

    linhas = saida.read_text(encoding="utf-8").splitlines()
    assert linhas[0] == ",".join(met.CSV_FIELDS)
    assert len(linhas) == 3  # 1 cabecalho + 2 linhas de dados
