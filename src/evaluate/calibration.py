"""Historical polling-error calibration (Decisions 012, 013 and 016).

Moved from Rahan's notebook (notebooks/data-pulls.ipynb at ccb41c0) without
changing the calculation. Error = actual margin - poll average (D minus R,
points) at fixed horizons before Election Day; sigma = RMSE of those errors.
"""
from pathlib import Path

import numpy as np
import pandas as pd

from src.model.polling_average import add_margins_polls, add_margins_results, weighted_avg

ROOT = Path(__file__).resolve().parents[2]
CALIBRATION_SNAPSHOT = ROOT / 'data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1'
HORIZONS = (7, 14, 28, 42)


def results_wide(base=CALIBRATION_SNAPSHOT):
    """One row per eligible contest: D/R/other valid votes, shares and margin."""
    results = pd.read_csv(f'{base}/candidate_results.csv',
                          dtype=str, keep_default_na=False)
    rows = results[
        (results['contest_status'] == 'eligible') &
        (results['valid_vote'] == 'true')
    ].copy()
    rows['votes'] = rows['votes'].astype(int)

    wide = rows.pivot_table(
        index='contest_id',
        columns='side',
        values='votes',
        aggfunc='sum',
        fill_value=0
    ).rename(columns={'D': 'dem_votes', 'R': 'rep_votes', 'other': 'other_votes'})

    wide['valid_votes'] = wide.sum(axis=1)
    wide['dem_pct'] = wide['dem_votes'] / wide['valid_votes'] * 100
    wide['rep_pct'] = wide['rep_votes'] / wide['valid_votes'] * 100
    wide = wide.rename_axis(columns='election')
    return add_margins_results(wide)


def polls_wide(base=CALIBRATION_SNAPSHOT):
    """One row per selected poll question: D/R/other shares, margin and question metadata."""
    poll_results = pd.read_csv(f'{base}/poll_candidate_rows.csv', dtype=str, keep_default_na=False)
    poll_rows = poll_results[poll_results['question_status'] == 'selected'].copy()
    poll_rows['pct'] = poll_rows['pct'].astype(float)

    wide_polls = poll_rows.pivot_table(
        index='question_key',
        columns='side',
        values='pct',
        aggfunc='sum',
        fill_value=0
    ).rename(columns={'D': 'dem_pct', 'R': 'rep_pct', 'other': 'other_pct'})
    wide_polls = add_margins_polls(wide_polls).reset_index()

    poll_questions = pd.read_csv(f'{base}/poll_questions.csv', dtype=str, keep_default_na=False)
    return wide_polls.merge(poll_questions, on='question_key',
                            how='left', validate='one_to_one')


def merge_historical(wide_polls, wide):
    """Attach each poll's contest result; result columns get the `_result` suffix."""
    historical = wide_polls.merge(wide, on='contest_id', how='left', validate='many_to_one',
                                  suffixes=('', '_result'))
    historical['election_date'] = pd.to_datetime(historical['election_date'])
    historical['end_date'] = pd.to_datetime(historical['end_date'])
    return historical


def calibration_errors(historical, halflife, horizons=HORIZONS):
    """Polling error for every contest x horizon.

    Returns (errors, dropped). `errors` has cycle, contest_id, horizon, error,
    avg and neff; `dropped` lists contest/horizon pairs with no poll ending on
    or before the horizon date.
    """
    contests = sorted(historical['contest_id'].unique())
    records = []
    dropped = []

    for contest in contests:
        contest_data = historical[historical['contest_id'] == contest]
        for horizon in horizons:
            horizon_date = contest_data['election_date'].iloc[0] - pd.Timedelta(days=horizon)
            avg, neff = weighted_avg(contest_data, horizon_date, halflife)
            if avg is None:
                dropped.append({'contest_id': contest, 'horizon': horizon})
                continue
            error = contest_data['margin_result'].values[0] - avg
            records.append({'cycle': contest_data['cycle'].iloc[0],
                            'contest_id': contest,
                            'horizon': horizon, 'error': error,
                            'avg': avg, 'neff': neff})

    return pd.DataFrame(records), pd.DataFrame(dropped, columns=['contest_id', 'horizon'])


def error_summary(errors, by='horizon'):
    """Races, mean signed error and RMSE (sigma) grouped by `by`."""
    errors = errors.copy()
    errors['squared_error'] = errors['error'] ** 2
    grouped = errors.groupby(by)
    return pd.DataFrame({
        'races': grouped['error'].count(),
        'mean_error': grouped['error'].mean(),
        'rmse': np.sqrt(grouped['squared_error'].mean()),
    })


def run_calibration(halflife, base=CALIBRATION_SNAPSHOT, horizons=HORIZONS):
    """Build the historical table and return (errors, dropped)."""
    historical = merge_historical(polls_wide(base), results_wide(base))
    return calibration_errors(historical, halflife, horizons)
