# Prepared Senate calibration inputs

Snapshot: `20261006T024116Z_20261006T035630Z_v1/`, prepared 2026-10-06. Implements Decisions 011–014 and Rahan's approval of the Claude mapping/crosswalk handoff. It combines the saved 2018/2020 polling archive, prepared Texas 2024 tracker, and MEDSL V8.0 results. Original sources and notebook are preserved.

## Wide working tables (existing v1 inputs)

`20261006T024116Z_20261006T035630Z_v1_wide/` contains `results_wide.csv` (108 rows, one per contest/round), `polls_wide.csv` (729 rows, one per selected question) and a parent/output hash manifest. No additional 2022/2024 polling or expanded calibration inputs exist yet; approved archive collection is blocked on connectivity.

Results add `dem_votes`, `rep_votes`, `other_votes`, `unknown_votes` and `side_counts_complete` to the original contest metadata, including `valid_vote_total`, `status` and `reasons`. Counts sum only existing `valid_vote=true` candidate rows. Unknown sides stay in `unknown_votes`; pending valid-vote categories mark counts incomplete. Missing returns remain blank. All pending/excluded contests are retained: filter to `status == 'eligible'` before modeling.

Polls retain original selected-question metadata and add `dem_pct`, `rep_pct`, `other_pct` and `source_record_keys_json`. `other_pct` sums only reported other-candidate answers; it is not undecided and is not inferred as `100 − dem_pct − rep_pct`. Source answers and mapping evidence remain in the original long tables. No margins, result shares, weighting or calibration are calculated.

Replay offline to a fresh output:

```bash
python3 -B src/clean/prepare_calibration_wide.py --output outputs/calibration_wide_replay
```

Load from a notebook using `pd.read_csv(f'{wide_base}/results_wide.csv', dtype=str, keep_default_na=False)` and the corresponding `polls_wide.csv`, where `wide_base` is `../data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1_wide`. Convert numeric columns explicitly. Existing v1 files remain unchanged.

## Original detailed preparation

From the repository root, Python 3 standard library, offline:

```bash
python3 -B src/clean/prepare_senate_calibration.py
```

The default directory already exists and cannot be overwritten. Replay into a fresh directory:

```bash
python3 -B src/clean/prepare_senate_calibration.py --output outputs/calibration_replay
```

For byte-identical replay including the manifest, pass `--created-at 2026-10-06T05:46:25.131726+00:00`. The CLI also accepts `--poll-snapshot`, `--result-snapshot`, `--texas-snapshot`, and `--references`; inputs must be the reviewed source versions and satisfy manifest hashes. No network access or notebook execution occurs.

| File | Purpose |
| --- | --- |
| `contests.csv` | 108 contest rounds, including unpolled contests, a missing-results Mississippi first round, and 34 outside-scope 2024 contests. Dates, seat/round, valid-vote counts, status and reasons. |
| `candidate_results.csv` | All 508 source rows/ballot lines and original columns, plus integral votes, mapped round, canonical identity, D/R/other/unknown side, valid-vote flag and source/reference warnings. |
| `candidate_side_map.csv` | All 5,175 mappings: 508 result rows, 4,593 archive candidate answers and 74 Texas tracker shares. Includes evidence, missing labels, disagreements and unresolved identities. |
| `poll_candidate_rows.csv` | All 4,667 poll candidate answers. Archive columns remain unchanged; tracker shares are explicitly expanded into two rows with original tracker JSON. |
| `poll_questions.csv` | All 1,950 questions/tracker rows, original answer JSON, normalized dates/populations, partisanship basis, exact round and final selection status. |
| `crosswalk.csv` | Question-to-contest mapping and eligibility/preference reasons; same question keys and final statuses as the question inventory. |
| `race_crosswalk.csv` | 72 archive race IDs and their reviewed seat/round mappings; Louisiana's unverified runoff remains unmapped. |
| `race_inventory.csv` | Counts per registry contest, including zero-poll contests. This is not the horizon-specific dropped-race report. |
| `excluded.csv`, `pending.csv` | Exact keys/reasons for questions, contests and unresolved mappings. Counts include multiple record types; do not equate log row counts with poll counts. |
| `changes.csv` | 18,481 annotations/transformations with original values, prepared values and basis. Source labels themselves are never overwritten. |
| `manifest.json` | Input/reference/output hashes, processing time, attribution, source receipts, approvals, counts and limitations. |

| Cycle | Questions | Selected | Excluded | Pending |
| --- | ---: | ---: | ---: | ---: |
| 2018 | 879 | 333 | 408 | 138 |
| 2020 | 1,034 | 373 | 451 | 210 |
| Texas 2024 | 37 | 23 | 14 | 0 |
| Total | 1,950 | 729 | 873 | 348 |

There are 74 contests in the initial calibration scope: 56 eligible, two excluded (California 2018 and Arkansas 2020), and 16 pending. The selected questions cover 52 eligible rounds. Scope and registry eligibility do not guarantee polls at Rahan's chosen horizon.

`selected` means preparation prerequisites pass, not that a poll passes a later horizon cutoff. `excluded` means an approved exclusion applies; other warnings may coexist. `pending` means review is needed. All records remain in the inventories. Full ballot means all named, non-write-in candidates in that round's results; tied LV alternatives stay pending. Original questionnaires have not been comprehensively checked. Tracker rows remain separate observations under Decision 009, with shared-link flags retained.

From a notebook kernel working in `notebooks/`:

```python
from pathlib import Path
base = Path('../data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1')
questions = pd.read_csv(base / 'poll_questions.csv', dtype=str, keep_default_na=False)
poll_rows = pd.read_csv(base / 'poll_candidate_rows.csv', dtype=str, keep_default_na=False)
returns = pd.read_csv(base / 'candidate_results.csv', dtype=str, keep_default_na=False)
selected_questions = questions[questions['status'] == 'selected']
selected_poll_rows = poll_rows[poll_rows['question_key'].isin(selected_questions['question_key'])]
eligible_returns = returns[(returns['contest_status'] == 'eligible') & (returns['valid_vote'] == 'true')]
```

Join by `contest_id` and `canonical_candidate_id`; retain separate ballot lines and their votes. The stable local contest key separates state, cycle, ordinary/special seat and round; actual dates are explicit columns. Never join by state/year alone. Georgia's January 2021 rows belong to cycle 2020. Mississippi 2018 first-round polls cannot use the November 27 runoff returns.

Use `valid_vote_total`, rather than repeated `reported_total`, when the latter contains blank/under/over votes. Named candidates with unresolved parties remain pending; no party is imputed. Nevada's “None of These Candidates” denominator treatment remains pending. Unofficial returns and unresolved official-reference discrepancies are held for review, with MEDSL counts unchanged.

[The review](../../../docs/calibration_preparation_review.md) lists pending cases and source evidence. [The dictionary](../../../docs/data_dictionary.md#prepared-national-calibration-inputs-decisions-012014) describes fields. [The reference README](../../../src/clean/calibration_references/README.md) explains the factual JSON. Rahan implements margins, horizon selection, averages, errors and calibration; these files contain no such calculations.
