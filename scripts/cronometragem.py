#!/usr/bin/env python3
"""Script de cronometragem de trials (RQ1: tempo / RQ2: testes passando).

Fluxo (docs/scripts-metricas.md, secao 1):
  1. `start`  - marca o timestamp de inicio do trial.
  2. `check`  - roda `mvn test` e reporta o status atual, sem parar o cronometro.
  3. `watch`  - roda `mvn test` periodicamente ate todos os testes passarem ou
                o time-box (default 35 min) ser atingido; finaliza sozinho.
  4. `stop`   - finaliza manualmente (ex.: todos os testes passaram durante um
                `check` e o operador decide encerrar o trial agora).

Cada trial fica isolado em seu proprio diretorio (docs/ambiente-experimento.md,
secao 5): trials/<integrante>/<kata>/<tratamento>/. O estado do cronometro em
andamento e guardado em `.trial_state.json` dentro desse diretorio; o resultado
final e uma linha (CSV) em resultados/tempos.csv (na raiz do repo).
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

TIMEBOX_PADRAO_MIN = 35.0
STATE_FILENAME = ".trial_state.json"
CSV_FIELDS = [
    "integrante",
    "kata",
    "tratamento",
    "inicio_iso",
    "fim_iso",
    "tempo_segundos",
    "censurado",
    "testes_passando",
    "testes_total",
]


@dataclass
class TrialState:
    integrante: str
    kata: str
    tratamento: str
    inicio_ts: float
    timebox_min: float


def _state_path(trial_dir: Path) -> Path:
    return trial_dir / STATE_FILENAME


def _carregar_state(trial_dir: Path) -> TrialState:
    path = _state_path(trial_dir)
    if not path.exists():
        sys.exit(
            f"Nenhum trial em andamento em {trial_dir} "
            f"(arquivo {STATE_FILENAME} nao encontrado). Rode `start` primeiro."
        )
    dados = json.loads(path.read_text(encoding="utf-8"))
    return TrialState(**dados)


def _salvar_state(trial_dir: Path, state: TrialState) -> None:
    _state_path(trial_dir).write_text(
        json.dumps(asdict(state), ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _rodar_mvn_test(trial_dir: Path) -> None:
    """Roda `mvn test` no diretorio do trial. Falha de teste nao e erro do script."""
    subprocess.run(
        ["mvn", "-q", "-B", "test"],
        cwd=trial_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _ler_resultado_surefire(trial_dir: Path) -> tuple[int, int]:
    """Extrai (testes_passando, testes_total) dos relatorios do Surefire.

    Soma tests/failures/errors/skipped de todos os TEST-*.xml. `passando` conta
    apenas o que realmente foi verde (exclui failures, errors e skipped).
    """
    relatorios_dir = trial_dir / "target" / "surefire-reports"
    if not relatorios_dir.is_dir():
        return 0, 0

    total = 0
    nao_passando = 0
    for xml_path in relatorios_dir.glob("TEST-*.xml"):
        try:
            root = ET.parse(xml_path).getroot()
        except ET.ParseError:
            continue
        tests = int(root.get("tests", 0))
        failures = int(root.get("failures", 0))
        errors = int(root.get("errors", 0))
        skipped = int(root.get("skipped", 0))
        total += tests
        nao_passando += failures + errors + skipped

    return total - nao_passando, total


def _gravar_resultado(saida_csv: Path, linha: dict) -> None:
    saida_csv.parent.mkdir(parents=True, exist_ok=True)
    arquivo_novo = not saida_csv.exists()
    with saida_csv.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if arquivo_novo:
            writer.writeheader()
        writer.writerow(linha)


def _finalizar_trial(
    trial_dir: Path, state: TrialState, saida_csv: Path, censurado: bool
) -> dict:
    _rodar_mvn_test(trial_dir)
    testes_passando, testes_total = _ler_resultado_surefire(trial_dir)

    fim_ts = time.time()
    tempo_segundos = round(fim_ts - state.inicio_ts, 3)

    linha = {
        "integrante": state.integrante,
        "kata": state.kata,
        "tratamento": state.tratamento,
        "inicio_iso": datetime.fromtimestamp(state.inicio_ts).isoformat(timespec="seconds"),
        "fim_iso": datetime.fromtimestamp(fim_ts).isoformat(timespec="seconds"),
        "tempo_segundos": tempo_segundos,
        "censurado": censurado,
        "testes_passando": testes_passando,
        "testes_total": testes_total,
    }
    _gravar_resultado(saida_csv, linha)
    _state_path(trial_dir).unlink()
    return linha


def cmd_start(args: argparse.Namespace) -> None:
    trial_dir = Path(args.trial_dir).resolve()
    trial_dir.mkdir(parents=True, exist_ok=True)

    if _state_path(trial_dir).exists():
        sys.exit(
            f"Ja existe um trial em andamento em {trial_dir}. "
            f"Rode `stop` (ou apague {STATE_FILENAME}) antes de iniciar outro."
        )
    if args.timebox > TIMEBOX_PADRAO_MIN:
        sys.exit(
            f"Time-box de {args.timebox} min excede o maximo de "
            f"{TIMEBOX_PADRAO_MIN} min (so pode ser reduzido, nunca aumentado)."
        )

    state = TrialState(
        integrante=args.integrante,
        kata=args.kata,
        tratamento=args.tratamento,
        inicio_ts=time.time(),
        timebox_min=args.timebox,
    )
    _salvar_state(trial_dir, state)
    print(
        f"[start] trial iniciado: integrante={state.integrante} kata={state.kata} "
        f"tratamento={state.tratamento} time-box={state.timebox_min}min "
        f"em {trial_dir}"
    )


def cmd_check(args: argparse.Namespace) -> None:
    trial_dir = Path(args.trial_dir).resolve()
    state = _carregar_state(trial_dir)

    _rodar_mvn_test(trial_dir)
    testes_passando, testes_total = _ler_resultado_surefire(trial_dir)
    decorrido = time.time() - state.inicio_ts
    restante = state.timebox_min * 60 - decorrido

    print(
        f"[check] decorrido={decorrido:.0f}s restante={max(restante, 0):.0f}s "
        f"testes={testes_passando}/{testes_total}"
    )
    if testes_total > 0 and testes_passando == testes_total:
        print("[check] todos os testes passaram - rode `stop` para encerrar o trial.")
    if restante <= 0:
        print("[check] time-box atingido - rode `stop` para encerrar (censurado).")


def cmd_stop(args: argparse.Namespace) -> None:
    trial_dir = Path(args.trial_dir).resolve()
    state = _carregar_state(trial_dir)
    saida_csv = Path(args.saida)

    decorrido_min = (time.time() - state.inicio_ts) / 60
    censurado = args.censurado or decorrido_min >= state.timebox_min
    linha = _finalizar_trial(trial_dir, state, saida_csv, censurado)
    print(f"[stop] trial encerrado: {linha}")


def cmd_watch(args: argparse.Namespace) -> None:
    trial_dir = Path(args.trial_dir).resolve()
    state = _carregar_state(trial_dir)
    saida_csv = Path(args.saida)

    print(
        f"[watch] acompanhando trial (poll a cada {args.intervalo}s, "
        f"time-box={state.timebox_min}min). Ctrl+C interrompe sem finalizar."
    )
    while True:
        _rodar_mvn_test(trial_dir)
        testes_passando, testes_total = _ler_resultado_surefire(trial_dir)
        decorrido = time.time() - state.inicio_ts
        print(f"[watch] decorrido={decorrido:.0f}s testes={testes_passando}/{testes_total}")

        if testes_total > 0 and testes_passando == testes_total:
            linha = _finalizar_trial(trial_dir, state, saida_csv, censurado=False)
            print(f"[watch] todos os testes passaram - trial encerrado: {linha}")
            return

        if decorrido >= state.timebox_min * 60:
            linha = _finalizar_trial(trial_dir, state, saida_csv, censurado=True)
            print(f"[watch] time-box atingido - trial encerrado (censurado): {linha}")
            return

        time.sleep(args.intervalo)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cronometra um trial do experimento (tempo + testes passando/total)."
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    p_start = sub.add_parser("start", help="Inicia o cronometro de um trial.")
    p_start.add_argument("--integrante", required=True)
    p_start.add_argument("--kata", required=True)
    p_start.add_argument("--tratamento", required=True, choices=["com-ia", "manual"])
    p_start.add_argument("--trial-dir", default=".", help="Diretorio do trial (default: cwd).")
    p_start.add_argument(
        "--timebox", type=float, default=TIMEBOX_PADRAO_MIN,
        help=f"Time-box em minutos, <= {TIMEBOX_PADRAO_MIN} (default: {TIMEBOX_PADRAO_MIN}).",
    )
    p_start.set_defaults(func=cmd_start)

    p_check = sub.add_parser(
        "check", help="Roda mvn test e mostra o status, sem parar o cronometro."
    )
    p_check.add_argument("--trial-dir", default=".")
    p_check.set_defaults(func=cmd_check)

    p_stop = sub.add_parser("stop", help="Finaliza o trial manualmente e grava o resultado.")
    p_stop.add_argument("--trial-dir", default=".")
    p_stop.add_argument("--saida", default="resultados/tempos.csv")
    p_stop.add_argument(
        "--censurado", action="store_true",
        help="Forca censurado=true (ex.: abortado antes do time-box).",
    )
    p_stop.set_defaults(func=cmd_stop)

    p_watch = sub.add_parser(
        "watch", help="Faz o polling automatico ate o trial passar ou estourar o time-box."
    )
    p_watch.add_argument("--trial-dir", default=".")
    p_watch.add_argument("--saida", default="resultados/tempos.csv")
    p_watch.add_argument("--intervalo", type=float, default=15.0, help="Segundos entre checagens.")
    p_watch.set_defaults(func=cmd_watch)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
