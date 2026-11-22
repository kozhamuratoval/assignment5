# Expense Tracker

A small, offline command-line tool to track personal expenses and see totals by category.

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # test tools
pip install -e .                  # installs the `expense-tracker` command
```

Requires Python 3.10+. The app itself has no third-party dependencies.

## Usage

```bash
python -m expense_tracker add 12.50 food "lunch" --date 2026-11-01
python -m expense_tracker list [--category food]
python -m expense_tracker report [--format text|csv|json]
python -m expense_tracker export expenses.csv [--format csv|json|text]
```

After `pip install -e .` you can type `expense-tracker` instead of `python -m expense_tracker`.

Categories: `food`, `transport`, `rent`, `fun`, `other`.

Data is stored in `./expenses.json` (git-ignored). Set `EXPENSES_FILE=/path/to/file.json`
to use another file, e.g. a temporary file when experimenting.

## Checks

```bash
python -m pytest -q        # tests, incl. acceptance criteria (docs/acceptance-criteria.md)
ruff check .               # lint
mypy expense_tracker       # types
python -m build --wheel    # package build
```

## For AI agents

See [AGENTS.md](AGENTS.md) for allowed commands, forbidden actions and review gates.
