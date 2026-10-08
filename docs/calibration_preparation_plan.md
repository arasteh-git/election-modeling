# Historical Senate calibration preparation proposal

Prepared 2026-10-05 (America/New_York) for Rahan and Claude; updated after Decisions 013/014 and implementation on 2026-10-06. **National preparation is implemented:** see [the prepared README](../data/processed/senate_calibration/README.md) for commands/schemas and [the preparation review](calibration_preparation_review.md) for observed counts, official references and pending cases. The original design below records the intended workflow; current behavior and limits are documented in those implementation files. MEDSL V8.0 remains the approved main source. No model calculations are implemented.

## Approved results source and proposed crosschecks

Use MIT Election Data and Science Lab (MEDSL), **U.S. Senate statewide 1976–2024**, Harvard Dataverse DOI [10.7910/DVN/PEJ5QU](https://doi.org/10.7910/DVN/PEJ5QU), as the main results source for all 2018/2020 Senate contests and Texas 2024. Use official federal compilations and state returns to check candidate identities, election dates, exceptional rounds, and discrepancies.

MEDSL offers a consistent tabular source and an explicit **CC0 1.0** license. V8.0 metadata and original files are saved in `data/raw/senate_results/20261006T035630Z/`. Headers, source-year coverage and vote sums have been audited; actual election dates, round coverage and certification still need verification.

| Source | Proposed role and access | Fields / format | Redistribution and verification limits |
| --- | --- | --- | --- |
| [MEDSL Senate statewide](https://doi.org/10.7910/DVN/PEJ5QU) | Approved main source. Public unrestricted downloads, explicitly pinned V8.0. | Original CSV saved: candidate, party, votes, reported total, state, year, stage, special, mode, unofficial and revision fields; no election dates. | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) validated from saved metadata. Mechanical coverage audited; official/round verification pending. |
| [FEC Federal Elections 2018](https://www.fec.gov/introduction-campaign-finance/election-results-and-voting-information/federal-elections-2018/) and [2020](https://www.fec.gov/introduction-campaign-finance/election-results-and-voting-information/federal-elections-2020/) | Official crosschecks; publicly linked [2018 Excel](https://www.fec.gov/documents/2706/federalelections2018.xlsx) and [2020 Excel](https://www.fec.gov/documents/4228/federalelections2020.xlsx). | Candidate, party, vote counts/percentages, contest totals and election dates across general, primary/runoff and special tables. | FEC describes a compilation of certified state results. No explicit dataset license located; federal agency-produced work generally falls under [17 USC 105](https://www.copyright.gov/title17/92chap1.html), which does not establish rights for every third-party item. Workbook schemas not inspected. |
| [House Clerk election statistics](https://history.house.gov/Institution/Election-Statistics/) | Official federal reference, including a listed 2024 PDF, for Texas 2024 and discrepancies in older cycles. | Published candidate/party/vote-count tables; PDF extraction requires review. | Landing page and 2024 listing checked, individual 2024 tables not inspected. Federal-work scope as above; no blanket third-party license asserted. |
| [Texas SOS results archive](https://www.sos.state.tx.us/elections/historical/elections-results-archive.shtml) | Official Texas crosscheck. Follow its 2019–2024 link to [the results portal](https://results.texas-election.com/); older 2018 returns use the separate 1992–2019 portal. | Election-specific statewide Senate returns; exact 2024 export and certification status still to verify. | No explicit redistribution license established in [site policies](https://www.sos.state.tx.us/policies.shtml). Federal public-domain rules do not establish state-source permissions. |

During the original source research the FEC index listed congressional compilations through 2022 and a separate 2024 presidential publication. That presidential workbook is not a Senate source. MEDSL's CC0 file is the approved redistributable main dataset; official references do not replace correction provenance.

### MEDSL version and collected receipt

Collector's pinned public metadata endpoint:
`https://dataverse.harvard.edu/api/datasets/3072248/versions/8.0`

- Dataset ID: `3072248`; published version **8.0**, released `2026-05-11T16:13:52Z`.
- Main file ID: `13887039`; hosted filename `1976-2024-senate-state.tab`, original filename `1976-2024-senate-state.csv`. Metadata marks the file unrestricted.
- Original CSV collected: `https://dataverse.harvard.edu/api/access/datafile/13887039?format=original`; 530,501 unchanged bytes. SHA-256 `6f745db1b4a0026ad837e74428f9ed6f3f77fa51eb6f858b58ebdbc186fdb3bd`.
- Metadata MD5 for the hosted file: `0f8b51cf0f77a2ef0bff992f7a64d1b4`. It is not compared with original CSV; receipt SHA-256 and original size are checked.
- Codebook file `6708560` and original source-list CSV `4304792` are saved and inspected; codebook publisher MD5 verified. Supporting documentation is older than the main file.

The [MEDSL catalog](https://electionlab.mit.edu/data) still labels this Senate series through 2020. The codebook filename says 2024 while its body describes older coverage through 2018. The versioned dataset metadata is newer, but the stale documentation makes inspecting headers, certification flags, and exceptional-round semantics a required first check. The Dataverse landing page displayed a JavaScript/bot challenge; the documented public API returned normally. No access controls were bypassed.

## What the saved polling file actually contains

Input: `data/raw/texas_senate_historical/20261006T024116Z/senate_polls_historical.csv`.
SHA-256: `f781e2dad7b5fa0b0f9b3d453c35ae0efb2ce431b38573d2aa3164aa9d8808dd`.

Read-only inspection found **4,593 candidate rows**, **1,913 questions** keyed by `(cycle, race_id, poll_id, question_id)`, and **72 race/stage groups**:

| Cycle | Candidate rows | General race IDs | Jungle-primary IDs | Runoff IDs |
| --- | ---: | ---: | ---: | ---: |
| 2018 | 2,019 | 33 | 1 | 1 |
| 2020 | 2,574 | 32 | 2 | 3 |
| Total | 4,593 | 65 | 3 | 4 |

This corrects the handoff's approximate count of 64 general races. The 72 groups are not 72 independent seat outcomes: several stages concern the same seat, and a source stage label is not proof that a round happened. All-state collection is already present in the raw CSV, so no polling re-fetch is needed to extend preparation.

Other checks and preparation implications:

- Candidate-row partisanship labels: blank 3,658; DEM 495; REP 414; LIB 19; IND 5; `REP,REF` 2. These are row counts, not counts of independent polls. Preserve the raw values; the Texas preparer's DEM/REP/IND whitelist cannot classify every national label.
- Internal flags: 294 true and 4,299 false candidate rows. The inspected question groups agree internally on partisanship, internal flag, population, sample size, and election date.
- Missing candidate-row metadata: sample size 12, population 18, URL 16, election date 2. Missing values stay blank and flagged.
- Population labels include LV, RV, V, A, and blanks. Only LV qualifies under Decision 012; do not reinterpret V as LV.
- The two missing election dates belong to one Louisiana 2020 runoff question: race `7787`, poll `68124`, question `132277`, Adrian Perkins/Bill Cassidy, fieldwork August 6–12. Verify whether this was a hypothetical round; do not fill a date or join it to November results from its state/cycle alone.
- Three `ranked_choice_reallocated=true` candidate rows occur in **Maine 2018**, race `103`. Maine 2020 rows are all false, which does not establish the absence of ranked-choice voting. Verify each contest's official round definition.
- Archive `seat_number` is often 0 and sometimes 2 in ordinary races. It must not be treated as a Senate class without a reviewed crosswalk. Preserve `seat_name`, special status, and stage as evidence.

Texas 2024 continues to use the existing prepared 37 tracker rows with `2024-11-05` election dates. Its malformed fieldwork interval remains blank and flagged. The approved Texas inventory has 137 retained rows (49/51/37); this proposal does not change it.

## National preparation workflow and current progress

1. **Approval recorded.** Decision 014 and `data_sources.md` approve MEDSL; Decisions 012/013 approve calibration/preparation rules. Keep factual ambiguities in a pending log rather than inventing identities or dates.
2. **Immutable snapshot collected.** `data/raw/senate_results/20261006T035630Z/` contains original files, provenance and a mechanical audit of 508 rows/107 source groups. Collector/replay commands are in [the results README](../data/raw/senate_results/README.md). This is not a verified round registry or an analytically filtered calibration dataset.
3. **Prepare candidate returns mechanically.** Preserve source-row identity, candidate name, detailed and simplified party labels, ballot line, voting mode, stage, special, source year, and official-status flags. Retain all candidates and write-ins, not only D/R. Distinguish ordinary/special seats and each round. Take a repeated contest total once; never sum it over candidate rows or add a `total` mode to its components. Where the same candidate has several ballot lines, preserve the lines and aggregate only with an explicit reviewed identity/aggregation rule. The codebook's vote-total-1 encoding for uncontested races is a sentinel to flag, not a factual count to feed calibration. Hold unofficial or incomplete returns for review.
4. **Create a contest registry and explicit crosswalk.** Register all requested 2018/2020 result contests, including unpolled contests, plus Texas 2024. Keep `cycle` separate from actual election date/year (a 2020-cycle runoff can occur in 2021). Proposed key components are state, seat/ordinary-or-special identifier, cycle, round, and election date, with a stable local contest ID. Map archive race IDs and candidate IDs to these reviewed IDs; MEDSL names do not share 538 identifiers. Use a documented alias table, with source evidence and unresolved matches; never silently accept fuzzy name matches, substitute a winner, or derive nominees by vote rank.
5. **Extend polling preparation using the existing archive.** Keep a long candidate-row inventory and one question-level inventory, preserving source indices, IDs, candidate answers, populations, dates, raw partisan/internal labels, stage/seat fields, and RCV flag. Avoid prematurely collapsing California's two Democrats or multicandidate jungle questions into a single D/R row. Reuse the Texas formatting/audit approach, with a broader explicitly approved partisanship-label map. Unknown metadata stays unknown; raw flags remain intact. Candidate-specific and question-specific missing data remain visible.
6. **Apply approved filters and matchup rules, with reasons.** Decision 012 excludes non-LV and partisan/internal polls, retaining `not_flagged_partisan` and the UT source exception. Decision 013 also treats LIB/`REP,REF` flags as partisan, excludes confirmed non-ballot questions, and selects one observation per poll/round, preferring full-ballot LV questions. Preserve original flags and source eligibility basis; unknowns, uncertain identities and ambiguous/tied question choices remain pending. Do not relabel all UT observations as independently verified nonpartisan.
7. **Deliver preparation outputs for Rahan.** Produce the files below, with counts by cycle/contest and an audit of every correction, exclusion, and unresolved record. Rahan then computes horizon cutoffs, eligible averages, n_eff, errors, per-horizon σ, and no-poll exclusions under Decision 012. Codex does not implement those calculations in this preparation task.

### Original output design (implemented files documented in the prepared README)

Folder: `data/processed/senate_calibration/<snapshot ID>/`. Exact schema will be documented in the data dictionary alongside implementation.

| File | Intended purpose |
| --- | --- |
| `candidate_results.csv` | Candidate/ballot-line returns, source IDs, reviewed identity, votes and totals, with mode/round/status flags preserved. |
| `contests.csv` | Result-contest universe, actual dates, seat/round identifiers, candidate slate, denominator basis, and approved/pending scope status; includes contests without archived polls. |
| `crosswalk.csv` | Explicit archive race/candidate mappings and name aliases, evidence links, review status, and ambiguity reasons. |
| `poll_candidate_rows.csv` | All archived candidate answers with source indices and mechanically normalized fields. |
| `poll_questions.csv` | Question-level inventory with candidate answers and eligibility prerequisites; D/R fields only where the approved mapping is unambiguous. Texas 2024 retains its tracker-based provenance. |
| `excluded.csv`, `pending.csv`, `changes.csv` | Exact record keys, original values, actions, reasons, and rule/source basis; multiple applicable flags preserved. |
| `race_inventory.csv` | Poll/question counts and preparation status per contest, including zero-poll contests. It is not Rahan's horizon-specific dropped-race report. |
| `manifest.json` | Source hashes, processing time, schema/rule version, approvals, output hashes, counts, and limitations. |

The national preparer supports fresh output and offline replay: `python3 -B src/clean/prepare_senate_calibration.py --output outputs/calibration_replay`. The results collector remains `python src/ingest/senate_results.py`. Actual national schemas are in the dictionary, with `candidate_side_map.csv` and `race_crosswalk.csv` added to the original output design. See the prepared README for all files and limits.

## Approved choices and factual review still needed

Decisions 012/013 supersede the original suggested scope: use the approved Democratic/Republican sides, sum all same-round candidates on each side, and include specials/runoffs as separate rounds. Exclude same-party contests and races missing a side. Preserve all source records and log analytical exclusions. Actual identities, ballot slates, dates, certification and round definitions still need verification.

| Case present in the archive | Approved rule / remaining review |
| --- | --- |
| Maine 2018 (King IND), Vermont 2018 (Sanders IND); Alaska 2020 (Gross labeled DEM in polls) | Democratic-caucusing independents count as the D side; a separate Democrat counts as other. Preserve official/polling affiliation separately and verify specific identities/role evidence. |
| California 2018, Feinstein/de León both DEM | Exclude same-party contests from calibration; preserve raw candidate rows and exclusion reason. |
| Arkansas 2020, Cotton REP/Harrington LIB, no DEM | Exclude contests without both approved sides. |
| Minnesota 2018 ordinary/special; Mississippi 2018 ordinary/special; Arizona 2020 special | Assign separate reviewed seat IDs. Ordinary and special contests in the same state/year must never be merged. |
| Mississippi 2018 special jungle/runoff; Georgia 2020 ordinary/runoff and special jungle/runoff; Louisiana 2020 jungle and apparent runoff | Include specials/runoffs, exact round/slate matching; each round counts separately, with dependence acknowledged. Georgia cycle 2020 runoff dates belong to 2021. Mississippi first-round coverage and Louisiana's undated apparent runoff remain verification tasks. |
| Maine 2018/2020 ranked-choice contests | Use first-choice numbers in both polls and results. Preserve reallocation flags; verify source round and hold mixed/unclear definitions pending. |
| Non-nominee/hypothetical questions beyond Texas | Exclude questions with any compared candidate confirmed absent from that round's ballot. Missing/uncertain identities stay pending. Decision 011's 12 Texas exclusions remain in force. |
| Several eligible questions/populations/versions from one poll | One observation per poll/round; prefer full-ballot LV question. Preserve all versions and record selection reasons; tied or uncertain full-ballot choices remain pending. |
| Unrecognized partisan flags, unknown metadata outside UT, unofficial returns, source sentinels | LIB/`REP,REF` are partisan and excluded from calibration. Preserve exact labels. Unknown metadata, unofficial returns and sentinels remain pending for factual review. |

### Approved vote-share denominator

Decision 013 approves total valid candidate votes **including third-party and write-in votes**. Preserve official totals and ballot-line details and document residuals; do not count blank/under/over votes as valid candidate votes. The collected source includes explicit noncandidate categories in four 2020 state groups, so reported `totalvotes` is not automatically the approved denominator. Verify first-choice RCV returns and totals. Rahan computes the same-round D-side minus R-side result margin.

## Validation and handoff before modeling

- Confirm source snapshots and Rahan's notebook remain unchanged; receipt SHA-256 values must match the actual bytes. Verify fresh-output offline replay and refusal to overwrite existing data.
- Check schema, unique contest/round keys, dates, candidate identity and party mappings, valid votes, official-status flags, and result coverage. Check totals/modes/ballot lines without double counting; report source inconsistencies and sentinel values instead of inventing replacements.
- Reconcile every polling candidate row/question to kept, excluded, or pending status. Validate approved exclusions by exact source keys, including the existing 12 Texas hypotheticals. Preserve missing/ambiguous data and every applied reason.
- Verify no ordinary/special or first-round/runoff joins cross seats/rounds. Track source cycle separately from election year. Compare Texas returns and exceptional contests with official references; record disagreements, rather than claiming all primary sources verified.
- Give Rahan a complete registry with zero-poll contests and enough metadata to apply each horizon. He implements the one-eligible-poll rule, per-horizon dropped-race log, n_eff, averages, errors and σ.

Decision 012 uses LV polls, fieldwork end dates, half-life 14, and horizons 7/14/28/42. Publication-time leakage remains possible because end date stands in for availability. Stages for the same seat and states in the same cycle are not independent observations; the normal-versus-t choice and statistical evaluation remain Rahan/Claude's work.

## Next action

Proceed from the collected [results audit](senate_results_review.md) to verifying dates, round coverage, candidate/ballot-line identities and first-choice returns for national preparation. Implement Decisions 012/013 with exclusions and pending ambiguities logged. Rahan computes averages, errors, RMSE and probabilities. The [original proposal handoff](process/handoffs/2026-10-05-codex-to-rahan-and-claude-calibration-plan.md) remains historical context; the new collection handoff records the implemented snapshot.
