"""Command line interface for the expense tracker."""
import argparse

from . import storage
from .formatters import FORMATTERS, get_formatter
from .models import make_expense, total, totals_by_category


def cmd_add(args):
    expenses = storage.load()
    exp = make_expense(storage.next_id(expenses), args.amount, args.category,
                       args.description, args.date)
    expenses.append(exp)
    storage.save(expenses)
    print(f"Added expense #{exp.id}: {exp.amount:.2f} ({exp.category})")


def cmd_list(args):
    expenses = storage.load()
    if args.category:
        expenses = [e for e in expenses if e.category == args.category]
    for e in expenses:
        print(f"{e.id:>3}  {e.spent_on}  {e.category:<10} {e.amount:>9.2f}  {e.description}")


def cmd_report(args):
    expenses = storage.load()
    formatter = get_formatter(args.format)
    print(formatter.report(totals_by_category(expenses), total(expenses)), end="")


def cmd_export(args):
    expenses = storage.load()
    rows = [e.to_dict() for e in expenses]
    with open(args.output, "w") as f:
        f.write(get_formatter(args.format).export(rows))
    print(f"Exported {len(rows)} expenses to {args.output}")


def build_parser():
    p = argparse.ArgumentParser(prog="expense-tracker")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="add an expense")
    a.add_argument("amount")
    a.add_argument("category")
    a.add_argument("description")
    a.add_argument("--date", default=None)
    a.set_defaults(func=cmd_add)

    ls = sub.add_parser("list", help="list expenses")
    ls.add_argument("--category", default=None)
    ls.set_defaults(func=cmd_list)

    r = sub.add_parser("report", help="totals by category")
    r.add_argument("--format", default="text", choices=sorted(FORMATTERS))
    r.set_defaults(func=cmd_report)

    ex = sub.add_parser("export", help="export all expenses to a file")
    ex.add_argument("output")
    ex.add_argument("--format", default="csv", choices=sorted(FORMATTERS))
    ex.set_defaults(func=cmd_export)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
