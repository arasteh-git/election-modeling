# Tests

Future data validation and meaningful checks belong here.

`test_prepare_texas_history.py` checks the exact 12 historical exclusions, preservation of all other original fields, 37 election-date corrections, partisan/internal/unknown classifications, retention of ambiguous candidates, conflicting-date rejection, provenance hashes, unchanged raw files, and overwrite protection.

Run from the repository root (the data-pipeline tests need only the standard library):

```bash
python -B -m unittest discover -s tests -p 'test_prepare_texas_history.py' -v
```

The regression fixture is the saved 20261006T024116Z inventory; integration outputs go in a temporary directory and are removed by the tests. No network or statistical-model validation is involved.

`test_senate_results.py` uses the saved MEDSL 20261006T035630Z snapshot to verify exact candidate-row/field preservation, ordinary/special and year/round separation, anomaly retention, byte-identical offline replay, overwrite refusal, tamper rejection, and schema/version/DOI/license/restriction/checksum checks. Six tests; temporary replay outputs are removed. No network or model calculations.

```bash
python -B -m unittest discover -s tests -p 'test_senate_results.py' -v
```

`test_prepare_senate_calibration.py` adds nine checks for complete source-field/notebook preservation, independent and nominee side mappings, fusion ballot lines, exact Mississippi/Georgia rounds, missing/unverified rounds, valid-vote/RCV handling, approved non-ballot/partisan exclusions, unique full-ballot choices/ties, audit reconciliation, byte-identical offline replay, tamper rejection and overwrite protection. Tests create temporary outputs from the saved snapshots; no network or model calculations.

```bash
python3 -B -m unittest discover -s tests -p 'test_prepare_senate_calibration.py' -v
python3 -B -m unittest discover -s tests -v
```

`test_senate_poll_archives.py` adds six tests using explicitly synthetic archived CSVs and the unchanged real MEDSL original. It checks designated-cycle/source-field preservation, missing/duplicate/invalid-answer flags without dropping rows, schema/HTML/capture/license rejection, failure without a partial snapshot, offline byte-identical replay, tamper/overwrite rejection and exact 2022 results/stage preservation. Synthetic polling fixtures do not establish real archive availability or counts.

`test_calibration_wide.py` adds three checks for unique keys, equality to approved long-table side sums, missing/unknown vote preservation, complete parent-hash checks, byte-identical replay and overwrite/tamper rejection. No core model logic is tested or implemented.

`test_texas_model.py` adds five checks that the `src/model` and `src/evaluate` code reproduces the notebook's saved results exactly: Texas average +3.952 (14 LV polls), n_eff 6.705, σ(28) 7.030, P(D) 0.713, races/mean error/RMSE by horizon, the 11 dropped contest-horizons and selected mean errors by cycle. It checks that the refactor matches the earlier notebook output, not that the model is right.

Run the full suite from the repository root with `python3 -B -m unittest discover -s tests -v` or `python -m pytest`. The complete suite contains 34 tests. See [the prepared dataset](../data/processed/senate_calibration/README.md) and [review](../docs/calibration_preparation_review.md) for the implemented rules and remaining factual limits.
