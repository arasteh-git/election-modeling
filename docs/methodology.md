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

Historical Texas preparation (Decision 011, 2026-10-05): exclude the 12 clearly identified 2020 hypothetical Democratic challengers against Cornyn, retaining Hegar–Cornyn questions. Preserve the exclusions with source identifiers and reasons. Tag the older polls using 538 partisan/internal metadata, without excluding partisan polls. The processed inventory retains all populations and existing duplicate-question flags for subsequent review; it is not a completed calibration sample.

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

Calibration rules (Decision 012):

- Error = actual margin − poll average (D − R, points), with the average computed under live rules at a fixed horizon before Election Day.
- σ at horizons of 7, 14, 28, and 42 days; each run uses the closest horizon. σ = RMSE of errors, √(Σ eᵢ² / n).
- Race formats (Decision 013): Democratic-caucusing independents count as the Democratic side; same-party races are excluded; margin = sum of D-side − sum of R-side in the same round for polls and results; specials and runoffs are included, matched by round.
- Mean error is assumed zero but reported by cycle.
- Partisan- and internal-tagged polls are excluded.
- Races need at least one eligible poll; n_eff and dropped races are logged.

## Historical evaluation and leakage prevention

When computing a past race's average at a horizon, use only polls whose fieldwork ended on or before the horizon date (Decision 012). Fieldwork end date stands in for availability, because publication dates are not used (Decision 009); a poll fielded before the horizon but released after it can still leak.

## Bias evaluation

Report mean signed polling error by cycle for the calibration sample (Decision 012).

## Sensitivity analysis

Half-life, Texas first snapshot (reference date 2026-09-29, 11 LV polls):

| h (days) | Weighted D − R | n_eff |
| --- | --- | --- |
| 7 | +2.40 | 4.03 |
| 14 | +2.64 | 5.48 |
| 30 | +2.52 | 7.69 |
| Unweighted | +1.73 | 11 |

## Known limitations
