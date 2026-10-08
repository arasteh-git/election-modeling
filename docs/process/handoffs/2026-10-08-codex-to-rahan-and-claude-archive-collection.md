# Handoff

## Author and intended reviewer

Author: Codex. Reviewers: Rahan and Claude. Approval is recorded; no new source approval is needed to retry the same captures.

## Task / issue

Act on Rahan's “approved!” response to the two pinned archives, MEDSL 2022 use and all-state 2022/2024 scope. Complete authorized collection/inventory and mechanical support while preserving existing data and Rahan's model code.

## Branch and commit

`main` began at `faa65b0`; HEAD advanced during concurrent work to `bcee35b` (approval/tooling) after `dd99a4e` (tracker/forecast update). Rahan subsequently requested a commit of the completed work, including the new future-model direction. This handoff is included in that documentation commit; `bcee35b` is its parent. No push requested. Concurrent notebook/tracker work is preserved.

## Data snapshot / checksum

- **No complete new polling snapshot.** Both approved captures failed to connect; the raw archive folder contains README documentation only.
- New 2022 result inventory: `data/processed/senate_results_2022/20261006T035630Z_decision017_v1/`. Derived offline from existing original SHA-256 `6f745db1b4a0026ad837e74428f9ed6f3f77fa51eb6f858b58ebdbc186fdb3bd`; manifest retains original retrieval receipt and CC0 license.
- Wide existing-v1 inputs: `data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1_wide/`. Results SHA-256 `3c11a2d2c42d3940f864e470eb0cf16045f2732102f96bdfd40a904f62c0cd60`; polls SHA-256 `09f08badf7456ecf738d14da2cd31002cea26a32053e374bc3ec0d177b783513`. Parent and output hashes are recorded.

## Relevant files

- `src/ingest/senate_poll_archives.py`: approved-source collector/replay and offline 2022 results inventory; [ingest README](../../../src/ingest/README.md) and [raw-folder README](../../../data/raw/senate_poll_archives/README.md) give commands/files/limits.
- `src/ingest/senate_results.py`: optional requested-year set in the audit helper; original collection/replay defaults unchanged.
- `src/clean/prepare_calibration_wide.py`: audited wide export, documented in [clean README](../../../src/clean/README.md) and [prepared README](../../../data/processed/senate_calibration/README.md).
- [Results README](../../../data/processed/senate_results_2022/README.md), [attempt receipts](../../senate_archive_collection_attempts_2026_10_08.json), [decisions](../../decisions.md), [sources](../../data_sources.md), [methodology](../../methodology.md), [dictionary](../../data_dictionary.md), [file guide](../../file_guide.md), [STATUS.md](../../../STATUS.md).
- `tests/test_senate_poll_archives.py`, `tests/test_calibration_wide.py`; [tests README](../../../tests/README.md).

## What changed

Recorded Decision 017. Implemented immutable archive collection with designated-cycle inventory, original-column retention, CSV/capture/license validation, actual retrieval receipts, no partial snapshot on network failure, and hash-verified deterministic offline replay. The network-free 2022 results inventory is complete. Added the approved wide tables for the current v1 sample; kept unknown votes explicit, retained all contest statuses and source keys, and computed no margins or model quantities.

Recorded Decision 018 at Rahan's request: future national and generic-ballot inputs to individual state predictions, with lower weight than state-specific polls and adjustment for state partisan lean, alongside more states, pollster house effects and correlated state effects. Numerical weights, lean/translation method, sources and validation remain undecided; no core code changed.

## Decisions already approved by Rahan

Decisions 001–018. Decision 018 approves future direction only. New source/scope approval does not resolve McMullin/Osborn sides, overlapping special-election question mappings, first-choice evidence, older v1 pending cases or the thin-race choice. Preserve Texas 2024's existing active tracker source and source exception.

## Checks performed and observed results

- Real approved archive attempts: connection/SSL timeouts and “No route to host”; final per-URL failures are in attempt receipts. Pinned publisher README and polling README returned HTTP 200 with hashes. Browser fallback returned no available browser connection. This is observed access failure from this environment, not proof the archive is permanently unavailable.
- Real 2022 MEDSL inventory: 168 rows, 36 source groups, 33 states; every group sum matches its reported total. Separate Georgia general/runoff groups; 13 source rows have blank detailed parties across AK/HI/IL/IA/NV/NH/NC; two Missouri candidate rows are unofficial. All source strings, categories and ballot lines remain intact.
- Wide outputs: 108 unique contest/round rows and 729 unique selected-question rows. Side counts reconcile with the parent valid total when defined; absent returns remain blank and unknown votes/count completeness are explicit. Other poll percentage is only reported other-candidate answers.
- All 29 repository tests passed with `python3 -B -m unittest discover -s tests -v`. Six new collector checks use explicitly synthetic polling fixtures and real existing MEDSL bytes; three wide checks use the real existing prepared snapshot. Old 20 tests still pass, including byte-identical original collector/preparer replay.
- Preservation check: all 55 pre-existing raw/processed snapshot files in the baseline remain byte-identical. The notebook changed through concurrent work; Codex neither edited nor executed it. The subsequent observed notebook SHA-256 is `186364347b83b9deef44afcffaf5b9f2fff5db1f39c250584028e1713d35f941`.
- Documentation validation: all 173 local Markdown targets checked existed, new manifests/attempt receipts parsed, the raw archive folder contained only its README, and `git diff --check` passed. Final roadmap edits are documentation only; the 29-test run above covers the unchanged implementation.

## Checks not performed

No successful full archive retrieval, real 2022/2024 polling counts/coverage, expanded preparer implementation or expanded calibration output. No comprehensive new-cycle ballot/date/RCV verification, notebook edits/execution, margins, averages, errors, uncertainty or probabilities by Codex. Synthetic tests establish collector behavior, not real polling completeness.

## Open questions / concerns

Public archive connectivity is the current blocker. Do not fill a new sample using header prefixes, synthetic fixtures or a different unapproved mirror. The existing v1 calibration remains the active dataset. New-cycle mapping requires actual source content and evidence before selection; uncertain records stay pending. Missing source party fields, unofficial returns, first-choice definitions and denominator categories must be reviewed during that extension.

## Requested next action

Later session update (2026-10-08): Rahan also reports trouble accessing the web through Python for poll downloads and will retry later. Defer further downloads until he resumes; retain the existing approval and incomplete-work status.

When archive connectivity is restored, run `python3 -B src/ingest/senate_poll_archives.py`. No further approval is required for the two pinned capture URLs. Inventory real candidate rows, polls/questions, states/rounds, field gaps and overlaps; then extend `prepare_senate_calibration.py` with the approved schemas/cycles, explicit round/date/candidate evidence and pending-case logs, producing a fresh expanded snapshot. Preserve all original snapshots and the current wide export. Source changes or new analytical rules require Rahan's separate decision.

## What Rahan should implement or explain

Continue the notebook's automatic horizon selection and sensitivity work. The current wide files can replace repeated pivoting if useful, with eligible-result filtering. A new calibration run should wait for actual expanded prepared inputs; no notebook path change to a nonexistent expanded snapshot is needed.
