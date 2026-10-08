"""Reproduce the current Texas Senate forecast.

Run from the repository root:

    python -m src.model.run_texas

Uses the 20261008T042800Z tracker snapshot, LV polls only, half-life h = 14,
reference date 2026-10-08, and sigma = calibration RMSE at the 28-day horizon
with no bias shift (Decisions 009, 012, 015, 016).
"""
from pathlib import Path

import pandas as pd

from src.evaluate.calibration import error_summary, run_calibration
from src.model.polling_average import add_margins_polls, weighted_avg
from src.model.win_probability import p_dem_win

ROOT = Path(__file__).resolve().parents[2]
TEXAS_SNAPSHOT = ROOT / 'data/raw/texas_tracker/20261008T042800Z'
SET_DATE = pd.to_datetime('2026-10-08')
HALFLIFE = 14
SIGMA_HORIZON = 28  # set manually; automatic horizon selection is not implemented yet


def load_texas_lv(snapshot=TEXAS_SNAPSHOT):
    """LV polls from a tracker snapshot, with `margin` added."""
    raw = pd.read_csv(f'{snapshot}/normalized.csv')
    texas = raw[raw['population'] == 'LV'].copy()
    return add_margins_polls(texas)


def forecast(snapshot=TEXAS_SNAPSHOT, set_date=SET_DATE, halflife=HALFLIFE,
             sigma_horizon=SIGMA_HORIZON):
    """Return a dict with the Texas average, n_eff, sigma, P(D) and calibration tables."""
    texas = load_texas_lv(snapshot)
    texas_avg, texas_neff = weighted_avg(texas, set_date, halflife)
    errors, dropped = run_calibration(halflife)
    by_horizon = error_summary(errors, 'horizon')
    sigma = by_horizon.loc[sigma_horizon, 'rmse']
    return {
        'n_polls': len(texas),
        'avg': texas_avg,
        'n_eff': texas_neff,
        'sigma': sigma,
        'p_dem': p_dem_win(texas_avg, sigma),
        'errors': errors,
        'dropped': dropped,
        'by_horizon': by_horizon,
        'by_cycle': error_summary(errors, ['cycle', 'horizon']),
    }


def main():
    f = forecast()
    print(f"Snapshot: {TEXAS_SNAPSHOT.name}  reference date: {SET_DATE.date()}  h = {HALFLIFE}")
    print(f"LV polls: {f['n_polls']}  average (D - R): {f['avg']:+.3f}  n_eff: {f['n_eff']:.3f}")
    print(f"sigma ({SIGMA_HORIZON}-day RMSE): {f['sigma']:.3f}")
    print(f"P(Democrat wins): {f['p_dem']:.3f}")
    print(f"\nCalibration by horizon ({len(f['dropped'])} contest-horizons dropped, no polls):")
    print(f['by_horizon'].round(2).to_string())


if __name__ == '__main__':
    main()
