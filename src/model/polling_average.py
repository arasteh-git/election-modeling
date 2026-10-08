"""Poll margins and the recency-weighted polling average (Decision 009).

Moved from Rahan's notebook (notebooks/data-pulls.ipynb at ccb41c0) without
changing the calculation.
"""
import numpy as np
import pandas as pd


def add_margins_polls(raw_poll):
    """Add `margin` = dem_pct - rep_pct (points, D minus R) to a poll table."""
    raw_poll['margin'] = raw_poll['dem_pct'] - raw_poll['rep_pct']
    return raw_poll


def add_margins_results(wide_results):
    """Add `margin` = dem_pct - rep_pct (points, D minus R) to a results table."""
    wide_results['margin'] = wide_results['dem_pct'] - wide_results['rep_pct']
    return wide_results


def weighted_avg(polls, ref_date, halflife):
    """Recency-weighted average margin of polls ending on or before `ref_date`.

    weight = 0.5 ** (age_days / halflife), where age_days = ref_date - end_date.
    Returns (average, n_eff) with n_eff = (sum w)^2 / sum(w^2), or (None, None)
    when no poll ended on or before `ref_date`.
    """
    polls = polls[pd.to_datetime(polls['end_date']) <= ref_date].copy()
    if polls.empty:
        return None, None
    polls['age_days'] = (ref_date - pd.to_datetime(polls['end_date'])).dt.days
    polls['weight'] = 0.5 ** ((polls['age_days'] / halflife))
    avg = np.average(polls['margin'], weights=polls['weight'])
    n_eff = (polls['weight']).sum()**2 / (polls['weight']**2).sum()
    return avg, n_eff
