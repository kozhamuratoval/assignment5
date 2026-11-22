# Evidence files

| File | What it is |
|---|---|
| `baseline-checks.log` | pytest, ruff, mypy, build, pip-audit on the baseline |
| `baseline-behaviour.log` | CLI probes that reproduce the risk findings on the baseline |
| `golden-before.txt` / `golden-after.txt` | Same CLI command sequence before/after the refactor (byte-identical) |
| `refactor.md` | Before/after structure and the golden-output diff |
| `mitigation-red.log` | New R-01/R-02 tests failing before the fixes (red phase) |
| `final-checks.log`, `final-pytest-verbose.log` | All checks on the final version |
| `final-behaviour.log` | The same probes on the final version |
| `ai-risk-review.md` | Read-only AI review prompt and the candidate list |

All logs are unedited command output, except that temporary paths are replaced with `<tmp>`.

## Commit hash mapping

The logs were captured before AI co-author trailers were added to the commit messages, which
rewrote the hashes. The code in each commit is unchanged.

| In logs | Final commit | Commit |
|---|---|---|
| 8379df8 | fd34c05 (tag `baseline-v0.1.0`) | Baseline |
| 53889c1 | 7dbcdec | AGENTS.md, README, acceptance tests |
| f53c68d | 2df479b | Strategy refactor |
| c16430e | dc332fc | R-01 fix |
| 284faf0 | 8dce012 | R-02 fix (state of `final-*.log`) |
