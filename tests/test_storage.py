from expense_tracker import storage
from expense_tracker.models import make_expense


def test_roundtrip(tmp_path):
    path = tmp_path / "data.json"
    items = [make_expense(1, "3.20", "transport", "bus", "2026-11-01")]
    storage.save(items, str(path))
    loaded = storage.load(str(path))
    assert loaded == items


def test_missing_file_is_empty(tmp_path):
    assert storage.load(str(tmp_path / "nope.json")) == []


def test_next_id():
    items = [make_expense(4, "1", "fun", "x", "2026-11-01")]
    assert storage.next_id(items) == 5
    assert storage.next_id([]) == 1
