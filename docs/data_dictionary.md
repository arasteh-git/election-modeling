# Data dictionary

## Observation grain

One row from the Texas Politics Project tracker. A tracker row is not yet an adjudicated independent survey or approved modeling observation.

## Identifiers and keys

Snapshot path plus tracker_row identifies a source row. Row numbers may change in later snapshots; do not join different snapshots by row number. race_id is 2026-TX-US-SENATE-GENERAL.

## Fields, types, units, and allowed values

| File / field | Meaning |
| --- | --- |
| tracker.csv: original nine titled columns | Source cell text, with whitespace collapsed; original HTML preserves exact bytes |
| tracker_row | 1-based source table row within this snapshot |
| release_url | First link from poll-label cell; relative links made absolute; may point to an intermediary |
| normalized.csv: poll_label | Source label; may combine sponsor and pollster, not a canonical pollster ID |
| start_date, end_date | ISO fieldwork dates; year 2026 supplied from tracker context |
| sample_size | Positive integer from source, not an adjusted effective sample |
| population | LV likely voters; RV registered voters; A adults; preserve source classification |
| dem_pct, rep_pct | Reported Talarico and Paxton percentages on a 0–100 scale, not fractions |
| other_raw | Unsplit source text; may combine other candidates, undecided, and nonvoting responses |
| moe_raw | Original uncertainty text; do not assume all pollsters use identical error definitions |
| spread_raw | Original tracker spread, retained even when inconsistent |
| primary_verification | pending: extraction does not establish primary-source verification; consult review notes |
| flags | Semicolon-separated mechanical QC flags, not exclusion decisions |

## Date and timezone conventions

Fieldwork dates are calendar dates. manifest.json retrieved_at is timezone-aware UTC. Publication dates are not populated because the table does not provide a reliable field for each poll.

## Missing-value conventions

Empty source cells remain empty in tracker.csv. Required numeric/date parsing failures stop extraction rather than silently impute. Blank flags means no implemented check flagged the row; it does not mean verified or model-ready.

## Validation rules

Require one table with the expected nine headers, nonempty rows, nine cells per row, valid ordered dates, positive samples, known population codes, and candidate percentages from 0 through 100. Flag inconsistent displayed spread without correcting values. These are limited format checks, not a complete survey-quality audit.

## Derived fields

Date and numeric conversions only. The script uses subtraction solely to flag a source discrepancy; it does not output model weights, averages, or probabilities.

