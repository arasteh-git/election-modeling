# Methodology

## Forecast target

Each candidate's win probability in the 2026 Texas U.S. Senate general election (Decision 008).

## Scope and exclusions

Texas U.S. Senate first (Decision 006). Georgia and Michigan are tentative later races, not yet approved. House modeling is deferred.

## Outcome definition and units

Poll margin is dem_pct minus rep_pct, in percentage points; positive means the Democrat leads. The tracker's Spread column is not used (Decision 009).

## Poll inclusion and deduplication

Decision 009:

- Poll labels are kept as reported. The same firm with a different sponsor is a separate label.
- Repeat polls from the same label are separate observations.
- No further deduplication rules have been decided.

## Population selection

Likely-voter (LV) polls only (Decision 009). Registered-voter and adult polls are excluded.

Open: whether to use a release's LV numbers when the tracker shows only RV.

## Missing values and undecided voters

Undecided and other responses are left as reported: no allocation and no normalization to 100 (Decision 009).

## Baseline

## Weighting

Exponential recency weighting (Decision 009): weight = 0.5^(age_days / h), where age_days is the reference date minus the fieldwork end date. Working half-life h = 14 days, to be recalibrated on historical Senate data.

Weighted average = Σ(weight × margin) / Σ(weight). Report the effective number of polls alongside it: n_eff = (Σ weight)² / Σ(weight²). n_eff assumes independent, equal-variance polls, so it is an upper bound on independent information.

## Uncertainty and probability model

Convert the poll average into P(Democrat wins) using an error model calibrated on past Senate polling error (Decision 010). The model form is undecided.

## Historical evaluation and leakage prevention

## Bias evaluation

## Sensitivity analysis

Half-life, Texas first snapshot (reference date 2026-09-29, 11 LV polls):

| h (days) | Weighted D − R | n_eff |
| --- | --- | --- |
| 7 | +2.40 | 4.03 |
| 14 | +2.64 | 5.48 |
| 30 | +2.52 | 7.69 |
| Unweighted | +1.73 | 11 |

## Known limitations