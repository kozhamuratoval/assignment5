# Read-only AI risk review (Task 4)

**Tool / model:** Claude Opus 5.5 (claude-opus-5-5) in the Claude app's agent workspace, 2026-11-22.
**Mode:** read-only. No source file was edited during the review. Verification probes ran only against
throwaway data files (`EXPENSES_FILE=<tmp>`). Code changes came later, in separate commits (`dc332fc`, `8dce012`).
**Independence caveat:** the same assistant wrote the project, so this review is not independent.
The human verification steps in the report are what make it count.

**Prompt (summary):**
> Read `expense_tracker/*.py`, `tests/`, `README.md`, `requirements.txt`, `pyproject.toml`, `.gitignore` and
> `AGENTS.md` at commit f53c68d. Do NOT edit any file. List candidate risks in these categories: correctness,
> maintainability, security, dependency, agent operations. For each give the file/line, the suspected
> cause → event → consequence, and how it could be verified.

**Candidate list as proposed (before verification):**

| # | Category | Candidate | Proposed check |
|---|---|---|---|
| F1 | correctness | Negative/zero amounts accepted by `make_expense` | `add -25 …`, `add 0 …` |
| F2 | correctness | `nan`/`inf` accepted; poisons totals | `add nan …` then `report` |
| F3 | correctness | Float accumulation shows binary rounding in JSON report | add 0.1 + 0.2, `report --format json` |
| F4 | security | CSV export writes `=…` descriptions verbatim (formula injection) | export, inspect cell |
| F5 | maintainability | Duplicated `args.format` if/elif in report & export | read `cli.py` |
| F6 | correctness | Corrupt JSON data file crashes with traceback | write `{broken`, run `list` |
| F7 | correctness | `save()` not atomic → crash mid-write truncates data | fault injection |
| F8 | agent ops | Default `./expenses.json` not git-ignored → agent may commit personal data | run in repo, `git status` |
| F9 | dependency | `requirements.txt` unpinned; ruff/mypy/build undeclared; lint depends on tool version | read files, `ruff check` |
| F10 | agent ops / docs | README command `python main.py` does not exist | run it |
| F11 | security | `EXPENSES_FILE` allows path traversal | reason about trust boundary |
| F12 | security | `json.load` on data file allows code execution | reason about json module |
| F13 | correctness | Two concurrent `add` runs → duplicate ids / lost update | parallel runs |

Verification results and classification are in the risk register of the report
(evidence: `baseline-behaviour.log`, `final-behaviour.log`).

**Classification summary:** confirmed F1, F2, F3, F4, F5, F6, F8, F9, F10 · plausible/unverified F7, F13 ·
unsupported F11, F12.
