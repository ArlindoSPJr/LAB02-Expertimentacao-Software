"""Testes unitarios (Nivel 1) de scripts/cronometragem.py.

Nao chamam `mvn` de verdade - so testam a logica de parsing/calculo, usando
fixtures gravadas em scripts/tests/fixtures/. Ver plans/testes-unitarios-katas-e-scripts.md.
"""

import argparse
import csv
import time
from pathlib import Path

import pytest

import cronometragem as cron

FIXTURES = Path(__file__).parent / "fixtures"


def _colocar_surefire(trial_dir: Path, fixture_nome: str) -> None:
    reports = trial_dir / "target" / "surefire-reports"
    reports.mkdir(parents=True, exist_ok=True)
    conteudo = (FIXTURES / fixture_nome).read_text(encoding="utf-8")
    (reports / "TEST-Exemplo.xml").write_text(conteudo, encoding="utf-8")


def test_ler_resultado_surefire_tudo_passando(tmp_path):
    _colocar_surefire(tmp_path, "surefire_ok.xml")

    passando, total = cron._ler_resultado_surefire(tmp_path)

    assert total == 4
    assert passando == total


def test_ler_resultado_surefire_com_falhas(tmp_path):
    _colocar_surefire(tmp_path, "surefire_falhas.xml")

    passando, total = cron._ler_resultado_surefire(tmp_path)

    assert total == 6
    assert passando == 3  # 6 - (1 failure + 1 error + 1 skipped)


def test_ler_resultado_surefire_pasta_inexistente(tmp_path):
    assert cron._ler_resultado_surefire(tmp_path) == (0, 0)


def test_start_recusa_timebox_acima_do_maximo(tmp_path):
    args = argparse.Namespace(
        integrante="integrante-1",
        kata="kata1-placas",
        tratamento="manual",
        trial_dir=str(tmp_path),
        timebox=cron.TIMEBOX_PADRAO_MIN + 1,
    )

    with pytest.raises(SystemExit):
        cron.cmd_start(args)


def test_start_aceita_timebox_reduzido(tmp_path):
    args = argparse.Namespace(
        integrante="integrante-1",
        kata="kata1-placas",
        tratamento="manual",
        trial_dir=str(tmp_path),
        timebox=10.0,
    )

    cron.cmd_start(args)

    assert (tmp_path / cron.STATE_FILENAME).exists()


def test_gravar_resultado_grava_cabecalho_uma_unica_vez(tmp_path):
    saida = tmp_path / "tempos.csv"
    linha = {campo: "x" for campo in cron.CSV_FIELDS}

    cron._gravar_resultado(saida, linha)
    cron._gravar_resultado(saida, linha)

    linhas = saida.read_text(encoding="utf-8").splitlines()
    assert linhas[0] == ",".join(cron.CSV_FIELDS)
    assert len(linhas) == 3  # 1 cabecalho + 2 linhas de dados


def test_cmd_stop_censurado_quando_timebox_estourado(tmp_path, monkeypatch):
    monkeypatch.setattr(cron, "_rodar_mvn_test", lambda trial_dir: None)
    _colocar_surefire(tmp_path, "surefire_falhas.xml")
    state = cron.TrialState(
        integrante="integrante-1", kata="kata1-placas", tratamento="manual",
        inicio_ts=time.time() - 40 * 60, timebox_min=35.0,
    )
    cron._salvar_state(tmp_path, state)
    saida = tmp_path / "tempos.csv"
    args = argparse.Namespace(trial_dir=str(tmp_path), saida=str(saida), censurado=False)

    cron.cmd_stop(args)

    linha = next(csv.DictReader(saida.open(encoding="utf-8")))
    assert linha["censurado"] == "True"
    assert not (tmp_path / cron.STATE_FILENAME).exists()


def test_cmd_stop_nao_censurado_dentro_do_timebox(tmp_path, monkeypatch):
    monkeypatch.setattr(cron, "_rodar_mvn_test", lambda trial_dir: None)
    _colocar_surefire(tmp_path, "surefire_ok.xml")
    state = cron.TrialState(
        integrante="integrante-1", kata="kata1-placas", tratamento="com-ia",
        inicio_ts=time.time() - 5, timebox_min=35.0,
    )
    cron._salvar_state(tmp_path, state)
    saida = tmp_path / "tempos.csv"
    args = argparse.Namespace(trial_dir=str(tmp_path), saida=str(saida), censurado=False)

    cron.cmd_stop(args)

    linha = next(csv.DictReader(saida.open(encoding="utf-8")))
    assert linha["censurado"] == "False"
    assert linha["testes_passando"] == linha["testes_total"]


def test_cmd_stop_forca_censurado_via_flag(tmp_path, monkeypatch):
    monkeypatch.setattr(cron, "_rodar_mvn_test", lambda trial_dir: None)
    _colocar_surefire(tmp_path, "surefire_ok.xml")
    state = cron.TrialState(
        integrante="integrante-1", kata="kata1-placas", tratamento="manual",
        inicio_ts=time.time() - 5, timebox_min=35.0,
    )
    cron._salvar_state(tmp_path, state)
    saida = tmp_path / "tempos.csv"
    args = argparse.Namespace(trial_dir=str(tmp_path), saida=str(saida), censurado=True)

    cron.cmd_stop(args)

    linha = next(csv.DictReader(saida.open(encoding="utf-8")))
    assert linha["censurado"] == "True"
