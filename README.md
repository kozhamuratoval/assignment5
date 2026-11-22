# Expense Tracker

A small command-line tool to track personal expenses and see totals by category.

## Install

```
pip install -r requirements.txt
```

## Usage

```
python main.py add 12.50 food "lunch"
python main.py list
python main.py report
python main.py export expenses.csv
```

Data is stored in `expenses.json`.

## Tests

```
pytest
```
