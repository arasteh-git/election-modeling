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

Recency weighting, with poll age measured from the fieldwork end date (Decision 009). The decay form and rate are not yet decided.

## Uncertainty and probability model

Convert the poll average into P(Democrat wins) using an error model calibrated on past Senate polling error (Decision 010). The model form is undecided.

## Historical evaluation and leakage prevention

## Bias evaluation

## Sensitivity analysis

## Known limitations