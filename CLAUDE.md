# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository state

This repository is currently empty of source code — it contains the assignment brief and S01 planning docs under `docs/` (`enunciado.md`, `entendimento-e-planejamento.md`, `issues-planejadas.md`, `ambiente-experimento.md`) and no kata code or scripts yet. There is no build system, test suite, or source tree to document beyond what's fixed in "Fixed environment" below. Treat this as a greenfield project: the structure should be created as the work progresses, not assumed to already exist.

## What this repository is for

This is coursework for **Laboratório de Experimentação de Software** (Engenharia de Software). The deliverable is a controlled, within-subject crossover experiment comparing AI-assisted coding vs. manual coding on programming katas, plus the analysis and report of the results. Read `docs/enunciado.md` in full before starting any sprint work — it is the authoritative spec for hypotheses, metrics, and process rules.

### Research questions (RQ1–RQ3)
- **RQ1**: Does AI assistance reduce time-to-green (time until all acceptance tests pass)?
- **RQ2**: Does AI assistance reduce defects (failing acceptance tests)?
- **RQ3**: Does AI assistance change cyclomatic complexity or code duplication?

### Experiment design constraints (must be respected by any scripts/tooling built here)
- **Within-subject crossover**: each team member solves half the katas with AI assistance, half without, in counterbalanced order.
- **Time-box: 35 minutes per trial, hard ceiling.** It may only be reduced (with justification in the report), never increased. A trial that hits the time-box without passing is recorded as **censored at 35 min**, not discarded.
- **Even number of katas** (4 or 6) split exactly in half between treatments.
- Prefer low-indexed/original katas over well-known ones (e.g. classic LeetCode/HackerRank problems) to avoid the AI reproducing a memorized solution rather than genuinely assisting.
- Same AI assistant used across all trials within the group, for comparability.
- Language choice must match the static-analysis tooling: **Java → CK** for complexity/WMC and **PMD/PMD-CPD** for duplication; if not Java, use an equivalent (e.g. **Radon** for Python: `radon cc` for complexity, `radon mi` for maintainability index; jscpd or similar for duplication).
- LOC must always be reported alongside complexity/duplication as a control metric (AI-generated code may be more verbose).
- Statistics: use **median and IQR** for descriptive stats (small N), and the **Wilcoxon signed-rank test** for inferential analysis (paired, within-subject design).

### Fixed environment (already decided — see `docs/ambiente-experimento.md` for full detail)
- **Kata language: Java** (Maven + JUnit 5) — locks in CK/PMD for RQ3, per the constraint above.
- **Support scripts (timing, static-metrics collection) are written in Python**, orchestrating the Java toolchain — invoking `mvn test`, CK, and PMD as external processes and consolidating results (time, tests passing, complexity, duplication, LOC) into CSV/JSON for the S03 analysis. This is independent of the kata language.
- **AI assistant: Claude Code** (CLI/agent), same install/usage across all three members in every "with AI" trial.
- **IDE: VS Code**, same for both treatments (with and without AI) — no AI autocomplete extension (e.g. Copilot) active in either treatment; Claude Code is the only AI assistance, and only in "with AI" trials.
- Trials are isolated per `trials/<member>/<kata>/<treatment>/`, each starting from a clean kata template with no carried-over chat history.

### Expected artifacts by sprint
- **S01 (Lab02S01)**: Experiment design (hypotheses, dependent/independent variables, treatments, chosen katas, threats to validity) + environment prep (timing script, static-metrics script for CK/PMD or Radon).
- **S02 (Lab02S02)**: Execution — each member runs all katas (half with AI, half without), counterbalanced; time and test-pass data collected per trial.
- **S03 (Lab02S03)**: Statistical analysis (Wilcoxon for RQ1/RQ2, static metrics for RQ3) + a Pandas/Matplotlib/Seaborn dashboard comparing treatments.
- **Final report**: introduction with hypotheses, reproducible methodology, per-RQ results, discussion, link to the GitHub Projects board.

### Process rules tied to grading
- Every trial must be tracked as an individual GitHub Projects Issue (one per kata × treatment), assigned to the responsible member, and referenced by its issue number in the corresponding commit(s) — commits without an issue reference are not considered for grading.
- Each of the three team members must be the Assignee of at least one Issue with a committed code artifact (script, notebook, chart, or kata trial) in every sprint (S01, S02, S03) — not only kata-execution issues in S02.
- Kanban hygiene (WIP limits, Issue assignment, up-to-date cards, weekly progress) factors into the grade (up to 10% deduction per sprint for insufficient use of GitHub Projects).
