# Evaluation

Rahan's evaluation code, refactored out of the forecast notebook. `tests/test_texas_model.py` checks that it reproduces the notebook's saved results.

| File | Purpose |
| --- | --- |
| `calibration.py` | Builds contest-level results (`results_wide`) and selected poll questions (`polls_wide`) from the prepared calibration snapshot, merges them (`merge_historical`), computes error = actual margin − poll average for every contest at 7/14/28/42 days (`calibration_errors`), and summarizes races, mean error and RMSE (`error_summary`). `run_calibration(halflife)` runs the whole chain. Decisions 012, 013 and 016 define the rules. |
| `plot_calibration.py` | Draws `docs/img/calibration_errors.png` from the same calculation. |

Run from the repository root:

```bash
python -m src.evaluate.plot_calibration
```
