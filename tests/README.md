# Tests

Data-validation and regression tests for the collection, preparation and model code. The complete suite has 34 tests. Data-pipeline tests need only the standard library, use no network, build on the saved snapshots, and write temporary outputs that they remove.

Run the full suite from the repository root:

```bash
python3 -B -m unittest discover -s tests -v
# or
python -m pytest
```

Run one file:

```bash
python -B -m unittest discover -s tests -p 'test_prepare_texas_history.py' -v
```

| File | What it checks |
| --- | --- |
| `test_prepare_texas_history.py` | Using the saved 20261006T024116Z inventory as the regression fixture: the exact 12 historical exclusions, preservation of all other original fields, 37 election-date corrections, partisan/internal/unknown classifications, retention of ambiguous candidates, conflicting-date rejection, provenance hashes, unchanged raw files, and overwrite protection. |
| `test_senate_results.py` | Six tests on the saved MEDSL 20261006T035630Z snapshot: exact candidate-row/field preservation, ordinary/special and year/round separation, anomaly retention, byte-identical offline replay, overwrite refusal, tamper rejection, and schema/version/DOI/license/restriction/checksum checks. |
| `test_prepare_senate_calibration.py` | Nine tests: complete source-field/notebook preservation, independent and nominee side mappings, fusion ballot lines, exact Mississippi/Georgia rounds, missing/unverified rounds, valid-vote/RCV handling, approved non-ballot/partisan exclusions, unique full-ballot choices/ties, audit reconciliation, byte-identical offline replay, tamper rejection and overwrite protection. |
| `test_senate_poll_archives.py` | Six tests using explicitly synthetic archived CSVs and the real MEDSL original: designated-cycle/source-field preservation, missing/duplicate/invalid-answer flags without dropping rows, schema/HTML/capture/license rejection, failure without a partial snapshot, offline byte-identical replay, tamper/overwrite rejection and exact 2022 results/stage preservation. |
| `test_calibration_wide.py` | Three tests: unique keys, equality to approved long-table side sums, missing/unknown vote preservation, complete parent-hash checks, byte-identical replay and overwrite/tamper rejection. |
| `test_texas_model.py` | Five tests that the `src/model` and `src/evaluate` code reproduces the notebook's saved results exactly: Texas average +3.952 (14 LV polls), n_eff 6.705, σ(28) 7.030, P(D) 0.713, races/mean error/RMSE by horizon, the 11 dropped contest-horizons and selected mean errors by cycle. |

## Limitations

- `test_texas_model.py` checks that the refactored code matches the earlier notebook output, not that the model is right. The data-pipeline tests do not validate the statistical model.
- The synthetic polling fixtures in `test_senate_poll_archives.py` do not establish real archive availability or counts.

See [the prepared dataset](../data/processed/senate_calibration/README.md) and [review](../docs/calibration_preparation_review.md) for the implemented rules and remaining factual limits.
