"""Output formats for reports and exports (Strategy pattern).

Each format is one class implementing the same two methods, so adding a
format means adding one class here instead of editing branches in cli.py.
"""
import csv
import io
import json

EXPORT_FIELDS = ["id", "spent_on", "category", "amount", "description"]


class Formatter:
    def report(self, by_category: dict[str, float], total: float) -> str:
        raise NotImplementedError

    def export(self, rows: list[dict]) -> str:
        raise NotImplementedError


class TextFormatter(Formatter):
    def report(self, by_category, total):
        lines = [f"{cat:<10} {amount:>9.2f}" for cat, amount in sorted(by_category.items())]
        lines.append(f"{'TOTAL':<10} {total:>9.2f}")
        return "\n".join(lines) + "\n"

    def export(self, rows):
        return "\n".join(
            f"{r['id']} {r['spent_on']} {r['category']} {r['amount']} {r['description']}"
            for r in rows
        ) + "\n"


class CsvFormatter(Formatter):
    def _write(self, header, body):
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(header)
        writer.writerows(body)
        return buf.getvalue()

    def report(self, by_category, total):
        body = [[cat, amount] for cat, amount in sorted(by_category.items())]
        body.append(["TOTAL", total])
        return self._write(["category", "amount"], body)

    def export(self, rows):
        return self._write(EXPORT_FIELDS, [[r[f] for f in EXPORT_FIELDS] for r in rows])


class JsonFormatter(Formatter):
    def report(self, by_category, total):
        return json.dumps({"by_category": by_category, "total": total}, indent=2) + "\n"

    def export(self, rows):
        return json.dumps(rows, indent=2) + "\n"


FORMATTERS: dict[str, Formatter] = {
    "text": TextFormatter(),
    "csv": CsvFormatter(),
    "json": JsonFormatter(),
}


def get_formatter(name: str) -> Formatter:
    try:
        return FORMATTERS[name]
    except KeyError:
        raise ValueError(f"unknown format: {name}") from None
