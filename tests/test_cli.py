"""Acceptance tests (AC1-AC4) driven through the CLI entry point."""
import csv
import json

import pytest

from expense_tracker import cli, storage


@pytest.fixture
def data_file(tmp_path, monkeypatch):
    path = tmp_path / "expenses.json"
    monkeypatch.setenv("EXPENSES_FILE", str(path))
    return path


def run(argv, capsys):
    cli.main(argv)
    return capsys.readouterr().out


def test_ac1_add_then_list(data_file, capsys):
    out = run(["add", "12.50", "food", "lunch", "--date", "2026-11-01"], capsys)
    assert "Added expense #1" in out
    run(["add", "3", "transport", "bus", "--date", "2026-11-02"], capsys)
    listing = run(["list"], capsys)
    assert "lunch" in listing and "bus" in listing
    assert [e.id for e in storage.load()] == [1, 2]


@pytest.mark.parametrize("argv", [
    ["add", "5", "gadgets", "phone case"],
    ["add", "5", "food", "snack", "--date", "01/11/2026"],
])
def test_ac2_invalid_input_not_saved(data_file, argv):
    with pytest.raises((ValueError, SystemExit)):
        cli.main(argv)
    assert not data_file.exists()


def test_ac3_report_text_totals(data_file, capsys):
    for amount, cat in [("10", "food"), ("5.25", "food"), ("20", "rent")]:
        run(["add", amount, cat, "x", "--date", "2026-11-01"], capsys)
    out = run(["report"], capsys).splitlines()
    assert out == [
        "food           15.25",
        "rent           20.00",
        "TOTAL          35.25",
    ]


def test_ac4_export_formats(data_file, tmp_path, capsys):
    run(["add", "12.50", "food", "lunch", "--date", "2026-11-01"], capsys)
    run(["add", "3", "transport", "bus", "--date", "2026-11-02"], capsys)

    csv_path = tmp_path / "out.csv"
    run(["export", str(csv_path)], capsys)
    rows = list(csv.reader(csv_path.open()))
    assert rows[0] == ["id", "spent_on", "category", "amount", "description"]
    assert [r[4] for r in rows[1:]] == ["lunch", "bus"]

    json_path = tmp_path / "out.json"
    run(["export", str(json_path), "--format", "json"], capsys)
    assert [r["id"] for r in json.loads(json_path.read_text())] == [1, 2]

    txt_path = tmp_path / "out.txt"
    run(["export", str(txt_path), "--format", "text"], capsys)
    assert txt_path.read_text().splitlines() == [
        "1 2026-11-01 food 12.5 lunch",
        "2 2026-11-02 transport 3.0 bus",
    ]


def test_report_json_and_csv(data_file, capsys):
    run(["add", "10", "food", "x", "--date", "2026-11-01"], capsys)
    data = json.loads(run(["report", "--format", "json"], capsys))
    assert data == {"by_category": {"food": 10.0}, "total": 10.0}
    assert run(["report", "--format", "csv"], capsys).splitlines() == [
        "category,amount", "food,10.0", "TOTAL,10.0",
    ]


def test_unknown_format_rejected_before_any_work(data_file, tmp_path):
    with pytest.raises(SystemExit) as exc:
        cli.main(["export", str(tmp_path / "o.xml"), "--format", "xml"])
    assert exc.value.code == 2
    assert not (tmp_path / "o.xml").exists()


@pytest.mark.parametrize("amount", ["-25", "0", "nan"])
def test_r01_cli_rejects_bad_amount_cleanly(data_file, amount, capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["add", amount, "food", "x"])
    assert exc.value.code == 2
    assert "error:" in capsys.readouterr().err
    assert not data_file.exists()

