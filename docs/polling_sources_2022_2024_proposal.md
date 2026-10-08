# Proposed 2022/2024 Senate polling sources

Prepared by Codex on 2026-10-08 after Rahan authorized the [Claude handoff](handoffs/2026-10-08-claude-code-to-codex.md). **Proposal only: sources and expanded calibration scope are not yet approved.** No complete new polling dataset was downloaded or saved, and no preparation or model calculations were performed.

## Recommendation for Rahan

Approve these two dated Internet Archive captures of FiveThirtyEight's original historical Senate CSV, then inventory their coverage before preparing an expanded sample:

| Intended cycle | Proposed immutable capture | Observed access and schema |
| --- | --- | --- |
| 2022 | [2023-04-27 02:57:58 UTC](https://web.archive.org/web/20230427025758id_/https://projects.fivethirtyeight.com/polls-page/data/senate_polls_historical.csv) | HTTP 200, `text/csv`, 43-column header; 2022 appears in the inspected prefix. |
| 2024 | [2025-01-18 20:03:35 UTC](https://web.archive.org/web/20250118200335id_/https://projects.fivethirtyeight.com/polls-page/data/senate_polls_historical.csv) | HTTP 200, `text/csv`, 52-column header; 2024 appears in the inspected prefix. |

Both captures postdate their cycle's elections. Capture dates describe archive preservation, not poll publication or fieldwork. Use each capture only for its designated cycle; do not combine overlapping archive versions or replace the existing 2018/2020 snapshot. The November 2024 capture is less attractive because its date alone does not establish that all late poll updates had been incorporated. A [2025-03-06 capture](https://web.archive.org/web/20250306125405id_/https://projects.fivethirtyeight.com/polls-page/data/senate_polls_historical.csv) also returned a CSV header, but is a separate version, not an automatic substitute.

Recommend expanding Decision 012 to **all-state 2022 and 2024**, while retaining the existing Texas 2024 tracker inputs and source exception for continuity. Keep new 538 Texas 2024 records as an overlap inventory rather than appending them to the tracker. Changing Texas's active source would need a separate approved reconciliation rule.

Also approve using the **already-preserved MEDSL V8.0 original for 2022**. Decision 014 currently authorizes 2018/2020/2024 only. No new results download is necessary to inventory 2022 from those existing bytes.

## Access, attribution and permission evidence

FiveThirtyEight's [polling README](https://github.com/fivethirtyeight/data/blob/master/polls/README.md) identifies the original CSV endpoints. Initial checks returned HTML at ABC News rather than CSV; later retries encountered transport failures. The proposed links use public Internet Archive captures of those exact original URLs; no login, scraping around restrictions, or paid access was needed for the successful archive checks. Availability may be intermittent, so approved collection must verify content type and schema before accepting a response.

The publisher's [repository README](https://github.com/fivethirtyeight/data/blob/b366fada304fcf8068ba7789745fe15a61ed6e3d/README.md) states that datasets use CC BY 4.0 unless otherwise specified. No polling-specific alternative notice was found in the inspected polling documentation. Under the [CC BY 4.0 terms](https://creativecommons.org/licenses/by/4.0/), attributed redistribution and adaptation are permitted; retain publisher credit, source and license links, and identify transformations. Credit FiveThirtyEight / ABC News as publisher and Internet Archive for preservation. This does not establish permission to republish every linked poll report.

Save unchanged CSV bytes, publisher licensing documentation, original and capture URLs, archive timestamp, actual retrieval time, full-file SHA-256 and transformations when collection is approved. The current header-prefix hashes are **not full-file hashes** and cannot establish complete-file identity or completeness.

The machine-readable [check receipts](polling_source_checks_2022_2024.json) contain access times, content types, inspected headers, limits and hashes. They contain no candidate observations. These checks establish accessible headers and observed cycles; they do not verify every underlying poll release.

## Required field coverage

These fields appear in **both** inspected archived headers. Presence does not imply every row is populated or correctly classified.

| Needed information | Source fields | Preparation implication |
| --- | --- | --- |
| Fieldwork dates | `start_date`, `end_date` | Preserve both; apply the existing end-date rule without substituting archive dates. |
| Population and sample | `population`, `subpopulation`, `population_full`, `sample_size` | Preserve reported labels and missing values; select LV under approved rules. |
| Pollster and sponsor | `pollster`, `pollster_id`, `display_name`, `sponsors`, `sponsor_ids`, sponsor-candidate fields | Preserve source metadata; sponsorship alone is not a new exclusion rule. |
| Partisanship/internal status | `partisan`, `internal` | Preserve original values, audit recognized labels, leave unfamiliar or missing values pending. |
| Candidate shares and identity | `answer`, `candidate_name`, `candidate_id`, `party`, `pct` | Keep all candidate answers before mapping sides; confirm actual ballot membership. |
| Survey/question identity | `poll_id`, `question_id` | Namespace by source snapshot; audit multiple questions and potential duplicate surveys. |
| Exact election/round | `race_id`, `cycle`, `seat_name`, `seat_number`, `stage`, `election_date` | Crosswalk explicitly; do not assume seat number means Senate class. |
| Ranked choice | `ranked_choice_reallocated`, `ranked_choice_round` | Identify first-choice questions under Decision 013. |
| Source references | `url`, `source`, `created_at`, `notes` | Keep provenance; `created_at` is not automatically a verified publication date. |

The 2024 header adds fields such as `hypothetical`, endorsement metadata, numerical pollster ratings, and additional release URLs. The adapter must tolerate the two documented schemas while preserving original fields. Absence of a hypothetical flag in the older schema cannot establish ballot membership; candidate/round verification is still required.

## Coverage and counts: observed versus unknown

| Cycle | Existing MEDSL candidate/source rows | Existing result groups `(state_po, special, stage)` | States in returns | New archive poll/question totals |
| --- | ---: | ---: | ---: | --- |
| 2022 | 168 | 36 | 33 | Not measured; the bounded prefix contains 42 complete candidate-answer rows labeled 2022. |
| 2024 | 148 | 35 | 33 | Not measured; the bounded prefix contains 36 complete candidate-answer rows labeled 2024. |

Result counts were computed by reading the unchanged local original CSV. These are source inventories, not approved eligible-contest counts. The 2022 groups include separate Georgia general/runoff returns and separate ordinary/special California and Oklahoma returns. The 2024 groups include separate ordinary/special California and Nebraska returns.

**No defensible approximate full-cycle poll counts are established yet.** A small prefix cannot support extrapolation, and compressed Internet Archive record lengths are not row counts. The handoff forbids collection before source approval, so this proposal leaves that requested count explicitly unresolved. All-state coverage is a target to audit, not a claim that every state has eligible polling.

The first approved inventory must report, separately for each cycle: candidate rows, distinct survey IDs, distinct questions, general/runoff questions, states and exact rounds with any polling, missing required fields, and selected/excluded/pending question counts after approved preparation. Report unpolled result groups explicitly. Do not equate candidate rows with polls or guarantee that 36/35 result groups will enter calibration.

## Alternatives reviewed

| Source | Finding and why it is not the preferred input |
| --- | --- |
| [FiveThirtyEight state-of-the-polls-2024](https://github.com/fivethirtyeight/data/tree/master/state-of-the-polls-2024) | Accessible publisher article data, but lacks the required candidate-question structure. Its documented time window ends 15 days before elections and its release cutoff precedes Election Day; unsuitable for complete 7/14-day calibration inputs. No corresponding 2022 cycle file is listed. |
| [FiveThirtyEight pollster ratings](https://github.com/fivethirtyeight/data/tree/master/pollster-ratings) | `raw_polls.csv` is accessible. Its schema lacks population and complete fieldwork start/end dates; documentation describes sample-size imputation and retaining the final top two candidates. Applying current rules would require new assumptions. |
| [Jack Whitcomb's RCP-derived Senate archive](https://github.com/Jack-Whitcomb/All-US-Senate-polls-2006-2024) | 2022/2024 headers provide dates, sample size/type and wide party shares. They lack question/candidate identity, sponsor and partisan/internal metadata. The repository notes overlapping special-election ambiguity. Redistribution permission was not established; not proposed for collection. |
| [datasets/archive-fivethirtyeight](https://github.com/datasets/archive-fivethirtyeight) | Inspected repository tree preserves article files and ratings; no `senate_polls.csv` or `senate_polls_historical.csv` was found. It is not a substitute for the dynamic polling exports. |
| [Electoral-vote.com 2024 downloads](https://www.electoral-vote.com/evp2024/Info/data.html) | Publisher describes editorial poll selection and setting independent shares to zero. Required sample/population/question and partisan metadata are missing. Unsuitable for these side-mapping rules. |

## Extension plan after approval

The existing `src/clean/prepare_senate_calibration.py` is pinned to the old snapshots and initial scope. Adding files alone will not extend it. A new version would add approved, hashed inputs; normalize the two archive schemas mechanically; inventory 2022 MEDSL rows; expand the registry; and provide evidence-backed cycle/seat/round/candidate crosswalks. Its existing special-seat and date logic must be extended explicitly, including handling `GEN RUNOFF` rather than treating every 2022 row as general.

Retain Decisions 012/013's rules: LV, recognized partisan/internal exclusions, actual ballot membership, one selected question per survey/round with full-ballot preference, first-choice RCV, valid-candidate votes, and pending ambiguous identities/denominators/ties. A new cycle does not authorize a new independent-candidate or duplicate-survey rule.

| Case to audit | Required handling / decision boundary |
| --- | --- |
| Georgia 2022 | Separate November 8 general from December 6 runoff, both cycle 2022; verify dates and match each question to its exact round. Existing MEDSL contains both stages. |
| California 2022/2024; Oklahoma 2022; Nebraska 2024 | Separate ordinary and special elections. A generic matchup question must not silently be copied to both contests. Ambiguous round identification stays pending. |
| Utah 2022, Evan McMullin | MEDSL reports independent. Democratic endorsement does not by itself establish the approved Democratic-caucusing side rule. Flag for Rahan; do not invent a D-side exception. |
| Nebraska 2024 ordinary, Dan Osborn | MEDSL reports `BY PETITION`. Verify identity and rule applicability; keep unresolved side mapping pending. Exclude under the existing no-both-sides rule only when that factual classification is established. |
| Maine/Vermont 2024, King/Sanders | Apply the approved caucusing-independent rule after current-cycle factual verification. Maine's separate Democrat must not be automatically added to King's side. |
| Alaska 2022 and Maine 2024 ranked choice | Verify first-choice returns and polling. Alaska's source party fields are blank; retain and flag them. Do not compare reallocated returns with first-choice polls. |
| Same-party races; ballot lines and noncandidate categories | Check each actual slate; do not carry California 2018's exclusion forward based on state alone. Preserve separate ballot lines and audit over/undervote, spoiled and write-in categories. |

Proposed outputs retain the detailed audit tables and add convenient **wide working tables**: one row per contest/round with side vote counts and valid-vote total, and one row per selected question with side percentages and metadata. This is a proposed mechanical aggregation, not new margin or modeling code. Raw source files and v1 outputs remain intact; unresolved rows stay visible in audit logs.

Rahan's current calibration loop iterates contest IDs from the merged table rather than hardcoding cycles. Compatible new prepared inputs should therefore feed the same loop, but the notebook's `base` path must point to the new snapshot. A rerun and checks by Rahan/Claude remain necessary; no notebook execution or guaranteed unchanged results are implied.

## Approval checklist and next action

Rahan can approve the proposal as a single scoped instruction: **collect the two pinned archives for their designated cycles, extend MEDSL approval to 2022, and expand calibration scope to all-state 2022/2024 while retaining the current Texas 2024 tracker source.** Record that approval in `docs/data_sources.md` and a new decision before collection. Source inventory comes first; ambiguous cases remain pending for review.

Until then, no collector/preparer changes, new polling snapshots, independent-side exceptions, notebook changes, margins, averages, errors, uncertainty estimates or probabilities are authorized by this proposal.
