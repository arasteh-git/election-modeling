# Handoff

## Author and intended reviewer

Author: Codex. Intended reviewers: Rahan and Claude. Rahan authorized the latest Claude handoff with “go”; this implementation adds no new methodology decision.

## Task / issue

Prepare contest rounds, candidate sides, exact poll/result crosswalks and approved mechanical/inclusion rules. Preserve sources and notebook, retain ambiguous cases, and leave all core modeling to Rahan.

## Branch and commit

`main` at `c3dc654159ab96672456c330dd671ec6043dc6f8` observed during work. New code, JSON references, prepared snapshot, tests and documentation remain uncommitted. Rahan committed notebook changes during the task. Codex did not commit, push, edit or execute the notebook.

## Data snapshot / checksum

- Poll archive: `data/raw/texas_senate_historical/20261006T024116Z/senate_polls_historical.csv`, SHA-256 `f781e2dad7b5fa0b0f9b3d453c35ae0efb2ce431b38573d2aa3164aa9d8808dd`.
- Main results: `data/raw/senate_results/20261006T035630Z/senate_returns.csv`, SHA-256 `6f745db1b4a0026ad837e74428f9ed6f3f77fa51eb6f858b58ebdbc186fdb3bd`, MEDSL V8.0/CC0.
- Texas 2024: existing prepared Decision 011 inventory, unchanged.
- New output: `data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1/`, actual processing time `2026-10-06T05:46:25.131726+00:00`. All input/reference/output hashes and original permission/attribution receipts are in its manifest.
- Factual reference JSON records official URLs, retrieval timestamps, SHA-256 and workbook/sheet/row or page locators. Whole reference downloads remain in ignored `outputs/calibration_reference_research/`, not additional redistributed raw sources.

## Relevant files

- [Prepared README](../../../data/processed/senate_calibration/README.md): every output, counts, notebook loading, offline replay and limits.
- [Preparation review](../../calibration_preparation_review.md): official facts, discrepancies, pending cases and checks.
- `src/clean/prepare_senate_calibration.py`: offline preparer, immutable outputs, manifest validation.
- [Reference README](../../../src/clean/calibration_references/README.md): `fec_facts.json`, `poll_aliases.json`, `round_facts.json`, `extract_fec.py`.
- `tests/test_prepare_senate_calibration.py`: nine new regression tests.
- Dictionary, STATUS, PROJECT, root/clean/processed/notebook/test/docs READMEs, source documentation and file guide updated to match behavior.

## What changed

All 508 result rows and 4,667 poll candidate answers remain available, with 5,175 side-map rows, 1,950 question crosswalks and 72 archive race mappings. The registry has 108 rounds: 74 in scope (56 eligible, two excluded, 16 pending) plus 34 excluded outside-scope 2024 rounds.

| Cycle | Questions | Selected | Excluded | Pending |
| --- | ---: | ---: | ---: | ---: |
| 2018 | 879 | 333 | 408 | 138 |
| 2020 | 1,034 | 373 | 451 | 210 |
| Texas 2024 | 37 | 23 | 14 | 0 |
| Total | 1,950 | 729 | 873 | 348 |

Selected questions span 52 eligible rounds before horizon cutoffs. Excluded/pending inventories retain original fields, and audit logs identify exact keys. Status counts are exclusive; reasons overlap.

Explicit overrides handle King/Sanders D, Ringelstein other, Gross as Democratic nominee and Wyoming's missing D/R labels. Fusion ballot lines retain their own votes but share a canonical candidate side. Stage/mode case and decimal-string votes normalize only in added columns. Fourteen noncandidate rows remain preserved but outside valid-vote totals; Nevada's ballot-option semantics remain pending.

Mississippi's special MEDSL `gen` rows map to November 27 runoff. The November 6 **four-candidate** first round is registered as missing returns; first-round polls never use runoff results. Georgia January 5, 2021 runoffs map to cycle 2020 with distinct ordinary/special IDs. Louisiana's apparent runoff remains unverified/unmapped. All exceptional dates carry official references.

Approved LV, source-partisan/internal, confirmed non-ballot and RCV-reallocated exclusions are logged. Unique full-ballot LV alternatives are preferred; 91 ambiguous/tied questions remain pending and two otherwise-selectable questions have pending siblings. Tracker rows remain separate observations under Decision 009, retaining source/shared-link flags. No arbitrary tie resolution or source vote replacement.

## Decisions already approved by Rahan

Decisions 001–015. Preparation implements 011–014; Decision 015's normal error form remains for Rahan's model. “Go” authorizes the handoff work and factual checks; no new independent-side exception, supplemental vote source, question tie-breaker or denominator rule is invented.

## Checks performed and observed results

- All 20 repository tests passed, including the nine new preparation tests.
- Tests verify every original result/poll field, approved sides and fusion lines, exact exceptional rounds, missing/unverified returns, valid-vote/RCV classifications, exact 12 Texas hypotheticals, LIB/REP,REF partisan treatment, unique observations, unresolved ties, count reconciliation, tamper rejection and overwrite refusal.
- Final offline replay into a fresh temporary directory matches all 12 saved files byte-for-byte using the recorded processing timestamp.
- All 47 pre-existing data files in the initial preservation baseline retain their SHA-256 values. The original notebook baseline differs because Rahan edited/committed it; Codex did not touch it, and tests/replay preserve its current bytes.
- Selected official checks: Wyoming party labels/Ben-David count; Maine first-choice counts/blank ballots; explicit FEC runoff dates and first-round membership; Gross nomination; Senate caucus context. Fifteen rows have FEC vote conflicts, one resolved by Wyoming's official summary; MEDSL counts stay unchanged.

## Checks not performed

No margins, D/R side sums, poll weighting, averages, horizon cutoffs, errors, RMSE, sigma or probabilities. No notebook execution, complete primary-poll audit, exhaustive official-return/certification validation, complete named write-in affiliation review, or mirror-byte verification.

## Open questions / concerns

Sixteen in-scope contests remain pending:

- Mississippi special first round: choose an approved supplemental result collection or explicit exclusion.
- Nevada 2018: decide “None of These Candidates” denominator treatment.
- Ohio/Vermont 2018 and New Jersey 2020: unresolved MEDSL/FEC counts.
- West Virginia 2018 and both Georgia runoffs: unofficial source flags plus count disagreements; South Dakota 2020: unofficial flag.
- Illinois, Kentucky, Massachusetts, Michigan, Nebraska, Tennessee, Texas 2020: named blank-party candidates/write-ins unresolved. Texas's pending candidate is Ricardo Turullols-Bonilla; no affiliation inferred from a generic FEC `W`.

Other pending questions concern identities, missing populations and full-ballot ties. References are partial. The “full ballot” flag uses named non-write-in source-result slates and explicit aliases; it is not a claim that every primary questionnaire has been verified. Horizon-specific missing-poll drops are still Rahan's responsibility.

## Requested next action

Review the prepared README and pending logs with Claude; resolve factual cases and approve any consequential inclusion/denominator/supplemental-source choices before generating a fresh snapshot. Use selected questions and eligible valid-vote result rows for learning/implementation; do not include pending records wholesale.

Offline replay:

```bash
python3 -B src/clean/prepare_senate_calibration.py --output outputs/calibration_replay
python3 -B -m unittest discover -s tests -v
```

## What Rahan should implement or explain

Write the result/poll margin function from explicit same-round sides and valid votes, keeping fusion lines and third-party/write-in denominator counts. Then write the horizon loop, no-poll handling/counts, averages/n_eff, signed errors and RMSE under Decision 012.

The current notebook already returns a 0–1 `p_dem_win` probability and checks emptiness after the date cutoff in `weighted_avg`; the prior handoff's requests on those points are stale. Returning the number of polls and removing display prints remain Rahan's choices. Codex has left all core functions alone.
