# Acceptance criteria

These must remain true after every change. Each is covered by an automated test.

| ID | Criterion | Test(s) |
|---|---|---|
| AC1 | `add <amount> <category> <description> [--date]` with valid input stores an expense with the next sequential id, and `list` shows it. | `test_cli.py::test_ac1_add_then_list` |
| AC2 | An unknown category or a malformed date is rejected and nothing is written to the data file. | `test_cli.py::test_ac2_invalid_input_not_saved`, `test_models.py` |
| AC3 | `report` (text) prints per-category totals and a TOTAL equal to the sum of all amounts, with 2 decimals. | `test_cli.py::test_ac3_report_text_totals` |
| AC4 | `export` in `csv`, `json` and `text` writes every expense; CSV header is `id,spent_on,category,amount,description`. | `test_cli.py::test_ac4_export_formats` |
| AC5 | Save → load is lossless, and a missing data file loads as an empty list. | `test_storage.py` |
