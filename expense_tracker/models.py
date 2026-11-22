"""Domain model for expenses."""
import math
from dataclasses import dataclass, asdict
from datetime import date


CATEGORIES = ["food", "transport", "rent", "fun", "other"]


@dataclass
class Expense:
    id: int
    amount: float
    category: str
    description: str
    spent_on: str  # ISO date, YYYY-MM-DD

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        return Expense(
            id=int(data["id"]),
            amount=float(data["amount"]),
            category=data["category"],
            description=data["description"],
            spent_on=data["spent_on"],
        )


def make_expense(next_id, amount, category, description, spent_on=None):
    """Build a new Expense from raw user input."""
    amount = float(amount)
    if not math.isfinite(amount) or amount <= 0:
        raise ValueError(f"amount must be a positive number, got {amount}")
    category = category.lower()
    if category not in CATEGORIES:
        raise ValueError(f"unknown category: {category}")
    if spent_on is None:
        spent_on = date.today().isoformat()
    else:
        date.fromisoformat(spent_on)  # validate format
    return Expense(next_id, amount, category, description, spent_on)


def total(expenses):
    return sum(e.amount for e in expenses)


def totals_by_category(expenses):
    result = {}
    for e in expenses:
        result[e.category] = result.get(e.category, 0) + e.amount
    return result
