# Handoff

## Author and intended reviewer

Author: Codex. Intended reviewers: Rahan and Claude. This is a source proposal; Rahan makes approval and methodology decisions.

## Task / issue

Respond to [Claude's 2022/2024 source request](2026-10-08-claude-code-to-codex.md), authorized by Rahan's “go do your work!” on 2026-10-08. Inspect public source documentation, archive metadata and bounded CSV prefixes; propose sources and preparation work without collecting full new polling datasets or computing model quantities.

## Branch and commit

`main`, HEAD `faa65b0` at inspection. Proposal changes are uncommitted. STATUS.md and the notebook had concurrent user changes when work resumed; those were retained. No commit or push performed.

## Data snapshot / checksum

No new polling snapshot. Proposed original-URL captures:

- 2022: `20230427025758`, historical Senate CSV.
- 2024: `20250118200335`, historical Senate CSV.

Capture URLs and bounded-prefix receipts are in the proposal/check JSON. Prefix hashes are not full-file identities. Existing MEDSL original remains SHA-256 `6f745db1b4a0026ad837e74428f9ed6f3f77fa51eb6f858b58ebdbc186fdb3bd`.

## Relevant files

- [Source proposal](../../polling_sources_2022_2024_proposal.md): access/license, schema, observed coverage, alternatives, exceptional races, future preparer and wide-table plan, approvals.
- [Inspection receipts](../../polling_source_checks_2022_2024.json): metadata/header evidence, actual check times, response-prefix hash scope and local results inventory.
- [Data sources](../../data_sources.md), [STATUS.md](../../../STATUS.md), [root README](../../../README.md), [docs README](../../README.md), [file guide](../../file_guide.md) and [handoff index](README.md): aligned documentation.

## What changed

Recommended two dated FiveThirtyEight exports preserved at their original URLs by Internet Archive. Keep original 2018/2020 inputs and Texas 2024 tracker source for continuity; do not append overlapping Texas archive polls. Proposed all-state 2022/2024 scope and MEDSL 2022 use remain unapproved. No pipeline or notebook implementation changed.

## Decisions already approved by Rahan

Decisions 001–016 remain in force. Rahan authorized proposal research, not new source approval or a scope change. No new decision has been entered as approved.

## Checks performed and observed results

- Both proposed archive links returned HTTP 200, CSV content types and required fields. Bounded prefixes show 2022 in the 43-column older schema and 2024 in the 52-column newer schema.
- Publisher dataset-license notice and CC BY 4.0 attribution requirements inspected. Linked poll-report republication permission was not inferred.
- Current original endpoints initially resolved to ABC HTML; subsequent retries failed at the transport layer. Accessible archive headers do not guarantee continuous availability.
- Local unchanged MEDSL original: 2022 has 168 source rows, 36 state/special/stage groups, 33 states; 2024 has 148 rows, 35 groups, 33 states. Georgia 2022 includes both general and `GEN RUNOFF` rows. Counts establish source inventory, not calibration eligibility.
- Static preparer inspection found pinned schemas/hashes, hardcoded initial scope and older special/round/date mappings that require extension. Notebook loop uses contest IDs dynamically, but its snapshot path will need updating for new inputs.
- SHA-256 preservation check passed for all 62 baseline paths under raw/processed data, including their READMEs. The notebook changed through concurrent user work relative to the initial baseline; Codex neither edited nor executed it. It remains unchanged from the subsequent observed user version, SHA-256 `cceb19f9a79e9c52f2b4928e5735d7ac744774eac94853776fd9044109733a0d`.
- Evidence JSON parses; assertions confirm observed schemas, required field presence and intended cycles. All 78 local Markdown targets checked exist. `git diff --check` passed. These are documentation/evidence checks, not regression tests or new-dataset validation.

## Checks not performed

No full new polling file retrieval, full-cycle poll/question counts, comprehensive all-state polling coverage, missing-field rates, original-release verification, expanded preparation, model calculations, notebook execution or regression-test run. Approximate full-cycle poll counts requested in Claude's handoff remain unresolved rather than inferred from small prefixes or compressed archive record lengths.

## Open questions / concerns

First approved collection must inventory coverage and duplicate candidates/questions before preparation. Rahan/Claude should review McMullin/Osborn side-rule applicability, exact ordinary/special question mappings, Alaska/Maine first-choice evidence, and current-cycle King/Sanders mapping. Unknown cases stay pending. Existing v1 pending cases and thin-race/horizon decisions remain unchanged.

## Requested next action

Rahan approves or revises the concrete proposal: the two designated-cycle archive captures, MEDSL 2022 use, and all-state 2022/2024 calibration scope while preserving the Texas 2024 source. Record approval in `docs/data_sources.md` and a new decision before full collection, as required by Claude's handoff. Codex then performs immutable collection/inventory and extends preparation within approved rules, reporting coverage and affected records.

## What Rahan should implement or explain

Continue automatic horizon selection and sensitivity checks. After compatible new inputs exist, update the notebook snapshot path and rerun with Claude's review. No core modeling implementation was delegated to Codex by this source task.
