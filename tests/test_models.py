import pytest

from expense_tracker.models import make_expense, total, totals_by_category


def test_make_expense_basic():
    e = make_expense(1, "12.50", "Food", "lunch", "2026-11-01")
    assert e.amount == 12.5
    assert e.category == "food"
    assert e.spent_on == "2026-11-01"


def test_unknown_category_rejected():
    with pytest.raises(ValueError):
        make_expense(1, "5", "gadgets", "phone case")


def test_bad_date_rejected():
    with pytest.raises(ValueError):
        make_expense(1, "5", "food", "snack", "01/11/2026")


def test_totals():
    items = [
        make_expense(1, "10", "food", "a", "2026-11-01"),
        make_expense(2, "5", "food", "b", "2026-11-02"),
        make_expense(3, "20", "rent", "c", "2026-11-03"),
    ]
    assert total(items) == 35
    assert totals_by_category(items) == {"food": 15, "rent": 20}


@pytest.mark.parametrize("bad", ["-25", "0", "nan", "inf", "-inf", "abc"])
def test_r01_invalid_amount_rejected(bad):
    with pytest.raises(ValueError):
        make_expense(1, bad, "food", "x", "2026-11-01")
