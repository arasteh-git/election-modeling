# Prepared Senate calibration inputs

Contest, candidate-side and poll-crosswalk tables for the historical polling-error calibration, prepared under Decisions 011–014. They combine the saved 2018/2020 polling archive, the prepared Texas 2024 tracker, and MEDSL V8.0 results; original sources are preserved unchanged.

| Snapshot | Contents |
| --- | --- |
| `20261006T024116Z_20261006T035630Z_v1/` | Detailed long-format preparation: every source row, mapping and status. |
| `20261006T024116Z_20261006T035630Z_v1_wide/` | Wide working tables derived from the v1 snapshot. |

## Detailed preparation (v1)

| File | Purpose |
| --- | --- |
| `contests.csv` | 108 contest rounds, including unpolled contests, a missing-results Mississippi first round, and 34 outside-scope 2024 contests. Dates, seat/round, valid-vote counts, status and reasons. |
| `candidate_results.csv` | All 508 source rows/ballot lines and original columns, plus integral votes, mapped round, canonical identity, D/R/other/unknown side, valid-vote flag and source/reference warnings. |
| `candidate_side_map.csv` | All 5,175 mappings: 508 result rows, 4,593 archive candidate answers and 74 Texas tracker shares. Includes evidence, missing labels, disagreements and unresolved identities. |
| `poll_candidate_rows.csv` | All 4,667 poll candidate answers. Archive columns are unchanged; tracker shares are expanded into two rows with the original tracker JSON. |
| `poll_questions.csv` | All 1,950 questions/tracker rows, original answer JSON, normalized dates/populations, partisanship basis, exact round and final selection status. |
| `crosswalk.csv` | Question-to-contest mapping and eligibility/preference reasons; same question keys and final statuses as the question inventory. |
| `race_crosswalk.csv` | 72 archive race IDs and their reviewed seat/round mappings; Louisiana's unverified runoff is unmapped. |
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

The initial calibration scope has 74 contests: 56 eligible, two excluded (California 2018 and Arkansas 2020), and 16 pending. The selected questions cover 52 eligible rounds.

Status values:

- `selected`: preparation prerequisites pass. This does not mean the poll passes a later horizon cutoff.
- `excluded`: an approved exclusion applies; other warnings may coexist.
- `pending`: review is needed.

All records stay in the inventories. "Full ballot" means all named, non-write-in candidates in that round's results; tied LV alternatives stay pending. Tracker rows are separate observations under Decision 009, with shared-link flags retained.

### Run

From the repository root, Python 3 standard library, offline (no network access, no notebook execution):

```bash
python3 -B src/clean/prepare_senate_calibration.py
```

The default output directory already exists and cannot be overwritten, so replay into a fresh directory:

```bash
python3 -B src/clean/prepare_senate_calibration.py --output outputs/calibration_replay
```

For a byte-identical replay including the manifest, pass `--created-at 2026-10-06T05:46:25.131726+00:00`. The CLI also accepts `--poll-snapshot`, `--result-snapshot`, `--texas-snapshot`, and `--references`; inputs must be the reviewed source versions and match the manifest hashes.

### Load

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

Join rules:

- Join by `contest_id` and `canonical_candidate_id`; keep separate ballot lines and their votes. Never join by state/year alone.
- The stable local contest key separates state, cycle, ordinary/special seat and round; actual dates are explicit columns.
- Georgia's January 2021 rows belong to cycle 2020. Mississippi 2018 first-round polls cannot use the November 27 runoff returns.
- Use `valid_vote_total` rather than the repeated `reported_total` when the latter contains blank/under/over votes.

## Wide working tables (existing v1 inputs)

`20261006T024116Z_20261006T035630Z_v1_wide/` contains `results_wide.csv` (108 rows, one per contest/round), `polls_wide.csv` (729 rows, one per selected question) and a parent/output hash manifest.

- **Results** add `dem_votes`, `rep_votes`, `other_votes`, `unknown_votes` and `side_counts_complete` to the original contest metadata, including `valid_vote_total`, `status` and `reasons`. Counts sum only existing `valid_vote=true` candidate rows. Unknown sides go to `unknown_votes`; pending valid-vote categories mark counts incomplete. Missing returns stay blank. All pending and excluded contests are retained, so filter to `status == 'eligible'` before modeling.
- **Polls** keep the original selected-question metadata and add `dem_pct`, `rep_pct`, `other_pct` and `source_record_keys_json`. `other_pct` sums only reported other-candidate answers; it is not undecided and is not inferred as `100 − dem_pct − rep_pct`. Source answers and mapping evidence stay in the long tables.

Replay offline to a fresh output:

```bash
python3 -B src/clean/prepare_calibration_wide.py --output outputs/calibration_wide_replay
```

Load with `pd.read_csv(f'{wide_base}/results_wide.csv', dtype=str, keep_default_na=False)` and the corresponding `polls_wide.csv`, where `wide_base` is `../data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1_wide`. Convert numeric columns explicitly.

## Limitations

- These files contain no margins, result shares, horizon selection, averages, weighting, errors or calibration. Rahan implements those calculations.
- The wide tables cover only the existing 2018/2020/Texas 2024 inputs. No 2022/2024 polling has been added; approved archive collection is blocked on connectivity.
- Scope and registry eligibility do not guarantee polls at Rahan's chosen horizon.
- Named candidates with unresolved parties stay pending; no party is imputed. Nevada's "None of These Candidates" denominator treatment is pending.
- Unofficial returns and unresolved official-reference discrepancies are held for review, with MEDSL counts unchanged.
- Original questionnaires have not been comprehensively checked.

[The review](../../../docs/calibration_preparation_review.md) lists pending cases and source evidence. [The dictionary](../../../docs/data_dictionary.md#prepared-national-calibration-inputs-decisions-012014) describes fields. [The reference README](../../../src/clean/calibration_references/README.md) explains the factual JSON.
