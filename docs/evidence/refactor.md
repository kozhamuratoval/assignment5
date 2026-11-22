# Refactor evidence

## Structure (wc -l)
```
before (baseline-v0.1.0):
   1 expense_tracker/__init__.py
   3 expense_tracker/__main__.py
 108 expense_tracker/cli.py
  52 expense_tracker/models.py
  30 expense_tracker/storage.py
 194 total

after:
   1 expense_tracker/__init__.py
   3 expense_tracker/__main__.py
  72 expense_tracker/cli.py
  70 expense_tracker/formatters.py
  52 expense_tracker/models.py
  30 expense_tracker/storage.py
 228 total
```

## Branches on output format in cli.py
```
before: 6 occurrences of 'args.format ==' (lines: 32 36 44 54 59 66 )
after:  0 occurrences
```

## Golden output comparison
```
$ diff golden-before.txt golden-after.txt
(no differences, 63 lines compared)
```

Intentional behaviour change: an unknown --format is now rejected by argparse (exit 2, before reading data) instead of after loading data (exit 1).
