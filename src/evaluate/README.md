# Evaluation

Rahan's evaluation code. Moved from the notebook on 2026-10-08 as a mechanical refactor; results are unchanged (checked by `tests/test_texas_model.py`).

`calibration.py` builds contest-level results (`results_wide`) and selected poll questions (`polls_wide`) from the prepared calibration snapshot, merges them (`merge_historical`), computes error = actual margin − poll average for every contest at 7/14/28/42 days (`calibration_errors`), and summarizes races, mean error and RMSE (`error_summary`). `run_calibration(halflife)` runs the whole chain. Decisions 012, 013 and 016 define the rules.

`plot_calibration.py` draws `docs/img/calibration_errors.png` from the same calculation.
