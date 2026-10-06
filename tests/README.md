# Tests

Future data validation and meaningful checks belong here.

`test_prepare_texas_history.py` checks the exact 12 historical exclusions, preservation of all other original fields, 37 election-date corrections, partisan/internal/unknown classifications, retention of ambiguous candidates, conflicting-date rejection, provenance hashes, unchanged raw files, and overwrite protection.

Run from the repository root, standard library only:

```bash
python -B -m unittest discover -s tests -p 'test_prepare_texas_history.py' -v
```

The regression fixture is the saved 20261006T024116Z inventory; integration outputs go in a temporary directory and are removed by the tests. No network or statistical-model validation is involved.
