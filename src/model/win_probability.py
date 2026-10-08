"""Normal-error win probability (Decision 015).

Moved from Rahan's notebook (notebooks/data-pulls.ipynb at ccb41c0).
"""
from scipy.stats import norm


def p_dem_win(avg, sigma):
    """P(Democrat wins) = Phi(avg / sigma), with avg as D minus R in points."""
    prob = norm.cdf(avg / sigma)
    return prob
