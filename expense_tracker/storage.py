"""JSON file storage."""
import json
import os

from .models import Expense

DEFAULT_FILE = "expenses.json"


def data_file():
    return os.environ.get("EXPENSES_FILE", DEFAULT_FILE)


def load(path=None):
    path = path or data_file()
    if not os.path.exists(path):
        return []
    with open(path) as f:
        raw = json.load(f)
    return [Expense.from_dict(item) for item in raw]


def save(expenses, path=None):
    path = path or data_file()
    with open(path, "w") as f:
        json.dump([e.to_dict() for e in expenses], f, indent=2)


def next_id(expenses):
    return max((e.id for e in expenses), default=0) + 1
