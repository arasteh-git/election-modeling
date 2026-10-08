# Handoff

## Author and intended reviewer

Author: Claude Code. Intended reviewer: Codex. Rahan approves all changes and must confirm before Codex acts on this note.

## Task / issue

Prepare the calibration inputs for the error model under Decision 012:

- Propose an election-results source.
- Extend the historical preparation from Texas to all 2018/2020 Senate races in the saved 538 archive.

## Branch and commit

main at cebf48b. Decision 012 and its doc updates (docs/decisions.md, docs/methodology.md, PROJECT.md, STATUS.md) and this handoff are uncommitted; Rahan is committing them.

## Data snapshot / checksum

- 2026 Texas: data/raw/texas_tracker/20261006T023757Z/ (18 rows; SHA-256 e7639190f46d65fc36ff723810a35fa2f2b271b70bf89177c455b85b52e7b1da, matches manifest).
- Historical: data/raw/texas_senate_historical/20261006T024116Z/, including the full senate_polls_historical.csv (4,593 candidate rows, 64 general-election races across 2018 and 2020), and data/processed/texas_senate_historical/20261006T024116Z/.

## Relevant files

docs/decisions.md (Decisions 009, 011, 012), docs/methodology.md, src/clean/prepare_texas_history.py, tests/test_prepare_texas_history.py.

## What changed

Rahan approved Decision 012 (error-model calibration rules):

- Error = actual margin − poll average (D − R, points); positive means the Democrat beat the polls.
- The average uses live rules (LV only, fieldwork end date, h = 14) and only polls ended by the horizon.
- Polls tagged partisan or internal are excluded from calibration. `not_flagged_partisan` and UT tracker polls are retained.
- σ is computed at horizons of 7, 14, 28, and 42 days before Election Day; each run uses the closest horizon.
- Mean error is assumed zero but reported by cycle.
- A race needs at least one eligible poll; n_eff is recorded per race and dropped races are logged.

## Decisions already approved by Rahan

Decisions 001–012. Nothing in this note is a new methodological decision.

## Checks performed and observed results

Claude Code audited the 10-05 Codex work with read-only scripts:

- 2026 snapshot: 18 rows; no rows lost or changed versus 09-29; two new LV polls (Fox News +2, NYT/Siena +6).
- Historical: 149 raw records; the 538 party mapping is correct in every row; no poll ends after its election date; after LV filtering and Decision 011, no poll has more than one LV question.
- Observations for the record:
  - Fox News 9/24–9/28 sums to 100 (no undecided; likely forced choice).
  - Label variants across snapshots: "New York Times/Sienna" vs. "NY Times/Siena", "Fox News" vs. "FOX News".
  - 10 historical polls report both RV and LV versions, which will be useful later for estimating an RV−LV shift.

## Checks not performed

- Neither ingest script was rerun, and prepare_texas_history.py and its tests were not run or reviewed in detail.
- No primary releases were verified.
- Mirror-vs-original 538 provenance is still unverified.

## Open questions / concerns

Edge cases in the full 2018/2020 archive need Rahan's rules. Flag them, do not resolve them:

- Who counts as "Democrat" where an independent runs instead (e.g., Maine 2018, Vermont 2018).
- Same-party general elections (California 2018 top-two).
- Special and jungle elections (e.g., Mississippi 2018 special, Georgia 2020 special, Louisiana 2020) and runoffs: which round is the "result".
- Ranked-choice races (Maine 2020; note the archive's `ranked_choice_reallocated` field).
- Identifying hypothetical matchups outside Texas: the Texas rule named specific challengers. A general rule would keep only questions matching the actual general-election nominees, which depends on the results source.

## Requested next action

For Codex, after Rahan confirms:

1. Propose an election-results source covering all 2018 and 2020 Senate races and Texas 2024, with access method, licensing/redistribution terms, and fields (candidate, party, votes, total). MIT Election Data and Science Lab Senate returns and official state canvass reports are candidates. Do not collect until Rahan approves it in docs/data_sources.md.
2. Propose how to extend the Decision 011 preparation to all 2018/2020 states: election dates, partisan/internal tags, and a general rule for excluding non-nominee matchups. Flag the edge cases above for Rahan rather than resolving them.
3. Keep raw snapshots unchanged; log exclusions and corrections; update READMEs per the documentation-maintenance rule.

Do not compute poll averages, errors, σ, or probabilities. Those are Rahan's (Decision 001).

## What Rahan should implement or explain

- After the results are approved and prepared: compute each race's average and error at the Decision 012 horizons, then σ by horizon and mean error by cycle.
- Then choose the distribution form (normal vs. t) after looking at the error distribution.
- Optionally, add the 13-poll Texas average for the 10-05 snapshot to the notebook (check value: +3.32, n_eff 6.26 at reference date 10/5, h = 14).
