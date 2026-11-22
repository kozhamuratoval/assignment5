"""Command line interface for the expense tracker."""
import argparse
import csv
import io
import json
import sys

from . import storage
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
    by_cat = totals_by_category(expenses)
    if args.format == "text":
        for cat, amount in sorted(by_cat.items()):
            print(f"{cat:<10} {amount:>9.2f}")
        print(f"{'TOTAL':<10} {total(expenses):>9.2f}")
    elif args.format == "csv":
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["category", "amount"])
        for cat, amount in sorted(by_cat.items()):
            w.writerow([cat, amount])
        w.writerow(["TOTAL", total(expenses)])
        print(buf.getvalue(), end="")
    elif args.format == "json":
        print(json.dumps({"by_category": by_cat, "total": total(expenses)}, indent=2))
    else:
        print(f"unknown format {args.format}")
        sys.exit(1)


def cmd_export(args):
    expenses = storage.load()
    rows = [e.to_dict() for e in expenses]
    if args.format == "text":
        out = "\n".join(
            f"{r['id']} {r['spent_on']} {r['category']} {r['amount']} {r['description']}"
            for r in rows
        ) + "\n"
    elif args.format == "csv":
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["id", "spent_on", "category", "amount", "description"])
        for r in rows:
            w.writerow([r["id"], r["spent_on"], r["category"], r["amount"], r["description"]])
        out = buf.getvalue()
    elif args.format == "json":
        out = json.dumps(rows, indent=2) + "\n"
    else:
        print(f"unknown format {args.format}")
        sys.exit(1)
    with open(args.output, "w") as f:
        f.write(out)
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
    r.add_argument("--format", default="text")
    r.set_defaults(func=cmd_report)

    ex = sub.add_parser("export", help="export all expenses to a file")
    ex.add_argument("output")
    ex.add_argument("--format", default="csv")
    ex.set_defaults(func=cmd_export)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
