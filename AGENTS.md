# AGENTS.md — Expense Tracker

Instructions for AI coding agents (and humans) working in this repository.
Read this whole file before changing anything.

## Purpose
A small, offline, single-user command-line tool that records personal expenses
in a local JSON file and prints totals by category. There is no server, no network
access and no production deployment.

## Architecture
| Path | Responsibility |
|---|---|
| `expense_tracker/cli.py` | argparse commands (`add`, `list`, `report`, `export`); I/O only |
| `expense_tracker/formatters.py` | Output formats (`text`, `csv`, `json`) behind one `Formatter` interface (Strategy) |
| `expense_tracker/models.py` | `Expense` dataclass, input validation, totals (pure functions, no I/O) |
| `expense_tracker/storage.py` | Load/save JSON file; path from `EXPENSES_FILE` env var, default `./expenses.json` |
| `tests/` | pytest suite; `tests/test_cli.py` covers acceptance criteria AC1–AC5 |
| `docs/` | Acceptance criteria and recorded check output (`docs/evidence/`) |

Dependency direction: `cli → formatters`, `cli → models`, `cli → storage → models`.
`models.py` must stay free of file, console and environment access.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```
Requires Python ≥ 3.10. The app has no runtime dependencies.

## Safe commands (may run without asking)
```bash
python -m pytest -q                      # full test suite (must pass before any commit)
ruff check .                             # lint (read-only; do NOT use --fix without review)
mypy expense_tracker                     # type check
python -m build --wheel                  # build into dist/ (git-ignored)
EXPENSES_FILE=$(mktemp) python -m expense_tracker <command>   # manual runs on a throwaway file
git status / git diff / git log          # read-only git
```

## Coding conventions
- Python 3.10+, standard library only for runtime code.
- Keep functions small; validation lives in `models.make_expense`, formatting in `formatters.py`.
- New output format = new `Formatter` subclass registered in `FORMATTERS`; never add `if format == ...` branches in `cli.py`.
- Raise `ValueError` with a clear message for bad user input; `cli.main` prints `error: ...` and exits with code 2.
- Any text written to CSV must go through `formatters.safe_cell` (formula-injection guard).
- No new top-level modules without updating the architecture table above.

## Test expectations
- Every behaviour change ships with a test in `tests/`; every bug fix starts with a failing test.
- Tests must use `tmp_path` / `monkeypatch.setenv("EXPENSES_FILE", ...)`; never touch `./expenses.json`.
- Acceptance criteria AC1–AC5 in `docs/acceptance-criteria.md` must keep passing.
- Report the exact command and pass/fail totals in your change summary. Never claim a result you did not run.

## Forbidden actions
- **No secrets or personal data**: never create, read or commit `.env`, tokens, keys or a real `expenses.json`.
- **No deployment / publishing**: no `twine upload`, no `git push` to `main`, no tags, no releases.
- **No destructive commands**: no `rm -rf` outside `dist/`, `build/`, `.pytest_cache/`; no `git reset --hard`, `git push --force`, `git clean -fdx`, history rewrites or branch deletion.
- **No unreviewed dependency changes**: do not add, remove or upgrade packages in `requirements.txt` / `pyproject.toml` without a human approving the diff.
- **No network access** from code or tests.
- Do not disable, skip or weaken tests or lint rules to make a check pass.

## Review gates
1. Work on a feature branch (`agent/<topic>`), never on `main`.
2. Before asking for review: tests pass, `ruff check .` shows no *new* findings, mypy clean.
3. A human reviews the full diff and the test log and approves before merge.
4. Changes to `AGENTS.md`, dependency files or `storage.py` always need explicit human approval.

## Known limitations (do not "fix" silently — open an issue first)
- Amounts are `float`; totals can show binary rounding in JSON output.
- `save()` is not atomic and there is no file locking.
- Two pre-existing ruff findings in `models.py` (I001, DTZ011) are accepted for now.
