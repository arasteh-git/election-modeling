# Modeling

Rahan's core modeling code, refactored out of the forecast notebook. `tests/test_texas_model.py` checks that it reproduces the notebook's saved results.

| File | Purpose |
| --- | --- |
| `polling_average.py` | `add_margins_polls` / `add_margins_results` (D − R margin) and `weighted_avg`, the recency-weighted average and n_eff (Decision 009). |
| `win_probability.py` | `p_dem_win(avg, sigma)` = Φ(avg / σ) (Decision 015). |
| `run_texas.py` | Reproduces the current Texas forecast: 20261008T042800Z snapshot, LV only, h = 14, reference date 2026-10-08, σ = 28-day calibration RMSE, no bias shift. |

Run from the repository root:

```bash
python -m src.model.run_texas
```
