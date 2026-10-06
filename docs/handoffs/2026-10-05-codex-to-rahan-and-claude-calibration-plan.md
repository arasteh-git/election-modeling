# Handoff

## Author and intended reviewer

Author: Codex. Reviewers: Rahan for source selection and preparation decisions; Claude for comparison definitions, inclusion implications, and statistical review.

## Task / issue

Rahan requested election-result sources and a preparation plan following the Decision 012 handoff. Propose sources for all 2018/2020 Senate contests and Texas 2024, and explain how to extend the existing Texas preparation without implementing Rahan's model.

## Branch and commit

`main` at `be97bf86c01e77b35514b5245e67635225a8a7d0`; this documentation change is uncommitted. The notebook had pre-existing Rahan edits and was preserved.

## Data snapshot / checksum

- Full polling archive: `data/raw/texas_senate_historical/20261006T024116Z/senate_polls_historical.csv`; SHA-256 `f781e2dad7b5fa0b0f9b3d453c35ae0efb2ce431b38573d2aa3164aa9d8808dd`.
- Existing prepared Texas: `data/processed/texas_senate_historical/20261006T024116Z/`, 137 records (49/51/37), unchanged.
- Latest 2026 tracker: `data/raw/texas_tracker/20261006T023757Z/`, 18 rows per manifest. Original HTML SHA-256 per manifest: `e7639190f46d65fc36ff723810a35fa2f2b271b70bf89177c455b85b52e7b1da` (not independently recomputed in this turn).
- No election-results data snapshot yet. Proposed MEDSL dataset DOI `10.7910/DVN/PEJ5QU`, V8.0, file `13887039`; inspected metadata does not establish row-level coverage or vote-count validity.
- Notebook SHA-256 before/after this work: `b85b0f9c3330b1f59946ef16e9efd18ae86b1189f70e7f403fb0576a3a7a12ee`.

## Relevant files

- [Preparation plan](../calibration_preparation_plan.md): source comparison, pinned metadata, actual inventory, proposed workflow/outputs, open rules, and validation.
- [Data sources](../data_sources.md): proposal kept separate from the unapproved result-source section.
- [Documentation README](../README.md), [root README](../../README.md), [file guide](../file_guide.md), and [status](../../STATUS.md): navigation and current progress.
- Prior [Claude-to-Codex handoff](2026-10-05-claude-code-to-codex.md): scope and source-approval requirement.

## What changed

Recommended MEDSL statewide Senate returns V8.0 as the consistent CC0 main source, with FEC/House Clerk/Texas SOS official crosschecks. Wrote a staged preparation proposal covering provenance, candidate/ballot-line/mode preservation, reviewed contest/candidate crosswalks, all-state poll inventories, auditable filtering, and inputs for Rahan.

Corrected the prior handoff's approximate general-race count in the current proposal/status: there are 65 general race IDs plus seven jungle/runoff IDs. These are stage groups, not 72 independent outcomes. The proposal also flags national partisan labels outside the Texas whitelist, RCV-reallocated observations in Maine 2018, and the undated Louisiana apparent-runoff question. Historical handoff text and approved decisions were left as history.

## Decisions already approved by Rahan

Decisions 001–012 apply. Decision 011's Texas corrections and 12 exclusions remain unchanged. Decision 012 establishes LV/partisan/internal rules, h=14, horizons 7/14/28/42, error sign, mean-error reporting, minimum one eligible poll, n_eff and dropped-race logs. This turn adds no approved source, denominator, comparison mapping, or national matchup rule.

## Checks performed and observed results

- Read actual project/status/methodology/dictionary/decisions/latest handoff and inspected Git state.
- Read public MEDSL metadata/codebook and source landing pages; verified dataset V8.0/release/file IDs, unrestricted metadata, explicit CC0, FEC-linked Excel publications, and the House Clerk 2024 listing. The catalog/codebook body contain stale coverage descriptions.
- Read-only standard-library CSV inspection confirmed 4,593 candidate rows (2018: 2,019; 2020: 2,574), 1,913 questions, and the 33/32 general plus 1/2 jungle plus 1/3 runoff stage counts. Candidate-row partisan labels include LIB and `REP,REF`; three Maine 2018 rows have a true RCV-reallocation flag. Two missing election-date rows belong to one Louisiana question (`7787`/`68124`/`132277`).
- Checked documentation diffs for whitespace errors and local Markdown links. Git reports no raw/processed changes; all six prepared output byte hashes match the saved manifest, and the notebook matches its pre-work SHA-256. A direct processed-CSV comparison to HEAD required accounting for Git's CRLF-to-LF normalization (`core.autocrlf=input`).

## Checks not performed

- No MEDSL main file or FEC workbook downloaded, results dataset saved/prepared, or candidate returns verified. The FEC 2018 PDF was viewed during source research; this was not a row-level results audit. Exact MEDSL round coverage, unofficial flags, and Texas portal export remain to verify after approval.
- No collector/preparer execution, regression suite, averages, horizon calculations, errors, σ, or probabilities run in this documentation-only change.
- No primary poll releases checked; mirror identity remains unverified.

## Open questions / concerns

Rahan must select the result source. Further choices include independent/no-DEM/same-party comparisons, special/jungle/runoff scope and dependence, RCV comparison round, generalized hypothetical exclusions, duplicate question adjudication, unknown partisanship metadata, extended party-flag classification, and the valid-vote denominator. Recommendations are explicitly proposals. Source approval does not resolve these inclusion decisions.

The undated Louisiana apparent runoff must not be assigned November returns or an invented runoff date. Preserve actual election dates separately from cycle for Georgia's January 2021 runoffs. Preserve candidate ballots and totals without double counting modes or party lines.

## Requested next action

Rahan reviews the source proposal and approves the chosen source in `docs/data_sources.md`. Codex can then collect an immutable snapshot and audit actual coverage while unresolved analytical cases stay pending. Rahan/Claude review the proposed preparation choices; Codex implements only approved rules and documents exact commands/schemas/audits.

## What Rahan should implement or explain

After preparation: horizon-specific averages, n_eff, actual D−R margins under the chosen comparison/denominator, errors, σ, cycle mean errors, and dropped-race logs. Rahan and Claude choose normal versus t and evaluate dependence/leakage limits. Core logic stays in Rahan's hands.
