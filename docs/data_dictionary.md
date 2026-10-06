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


## Historical Texas Senate inventory

Applies to `data/raw/texas_senate_historical/<timestamp>/`. This schema differs from the 2026 tracker; they should not be joined by row numbers.

| Field | Meaning |
| --- | --- |
| source | `538_archive` or `ut_tracker_2024`; preserves source differences |
| source_rows | Semicolon-separated 1-based archive candidate data rows, or UT table data row; identifies records only within the specific snapshot/source |
| cycle | Election cycle, not necessarily fieldwork year; some fieldwork is in the preceding year |
| race_id, poll_id, question_id, pollster_id | Original 538 identifiers, blank where UT has none. A poll can contain several questions/populations. Keys need source plus snapshot; `question_id` is not a separate independent survey |
| poll_label, sponsors | 538 display label (pollster fallback) and sponsor text, or original UT poll label; no canonical firm mapping |
| start_date, end_date | ISO fieldwork dates from explicit source dates; blank for the malformed 2024 interval, with `unparsed_field_dates` |
| election_date | Original 538 date converted to ISO; blank for UT, which provides no date column |
| sample_size | Parsed positive integer; source missing values stay blank, never imputed |
| population, population_raw, population_full | Uppercased source code, original code, and source full population label. LV/RV/A as before; V is kept without reinterpretation and flagged, blanks preserved |
| dem_candidate, rep_candidate | Candidate names actually present in that question, not an assumed mapping to the eventual nominees; hypothetical/unexpected matchups flagged |
| dem_pct, rep_pct | Single DEM/REP candidate's source share, 0–100. Ambiguous/missing party answers stay blank and flagged. No undecided allocation or rescaling |
| candidate_answers_json | All original candidate answers for each 538 question (names, IDs, parties, percentages as source text). Blank for UT, which only lists the major-party candidates |
| field_dates_raw, moe_raw, spread_raw | UT original date interval, error text, and displayed spread; blank where not available. Spreads do not replace candidate shares |
| release_url | Source link, possibly an intermediary, stale, missing, or shared/mislabeled; not evidence of primary verification |
| created_at_raw | 538 database entry timestamp, original text and unverified timezone. Not verified publication/release time; blank for UT |
| notes, methodology, tracking, internal, partisan | Original 538 metadata, blank where unavailable; does not establish analytical inclusion or exclusion |
| primary_verification | `pending` for all collected records; primary releases not individually verified |
| flags | Semicolon-separated review flags; no automatic corrections or exclusions |

`texas_538_candidate_rows.csv` preserves the original archive fields plus `source_row`. `texas_2024_tracker.csv` preserves original table cell text plus row number and absolute link. The full source CSV/HTML remain unchanged. Source rows are counted excluding the archive header; the UT footnote is preserved in the manifest rather than counted as a poll.

Missing values are empty CSV fields (pandas reads these as NaN by default). Required schema/identifier failures and inconsistent metadata within a 538 question stop extraction. Missing numeric values and ambiguous dates are retained with flags; malformed numeric values stop extraction. No `other` or undecided share is inferred as the complement of major-party shares.

## MEDSL results inventory (Decision 014)

Applies to `data/raw/senate_results/20261006T035630Z/`. `senate_returns.csv` preserves the full original CSV bytes. `candidate_rows.csv` and `returns_<year>.csv` preserve all 19 source columns and source strings for 2018/2020/2024, with Georgia 2021 runoffs retained separately for review. Missing names/values remain empty CSV fields; pandas may infer NaN/types unless loaded with `dtype=str, keep_default_na=False`.

| Field | Meaning |
| --- | --- |
| `source_row` | 1-based data-row index in this snapshot's full MEDSL CSV; not stable across versions. |
| `selection_basis` | `requested_source_year` or `supplemental_GA_2021_runoff`; describes inventory selection, not calibration eligibility. |
| `inventory_id` | Snapshot-local source-group ID; not a reviewed contest ID, Senate class, or polling race ID. |
| `year` | Original source election year; Georgia 2021 runoffs retain 2021. No cycle assignment or date is inferred. |
| `state`, `state_po`, `state_fips`, `state_cen`, `state_ic` | Original state identifiers/strings. |
| `office`, `district` | Source `US SENATE` / `statewide`. |
| `stage`, `special`, `mode` | Original stage, special flag and voting mode. Stage labels require actual-round verification; modes are not combined. |
| `candidate`, `party_detailed`, `party_simplified`, `writein` | Original answer/ballot-line identity, party labels and write-in flag. Blank names, noncandidate categories and repeated ballot lines remain retained; no D-side mapping. |
| `candidatevotes`, `totalvotes` | Original vote-count strings (often `.0`). Candidate votes apply to a source row/party line. Total is repeated across rows; do not sum it over rows. May include blank/under/over votes, so not automatically the Decision 013 valid-vote denominator. |
| `unofficial`, `version` | Publisher certification flag and source revision string; source flags are not independent certification checks. |
| `flags` | Semicolon-separated mechanical warnings; not corrections or exclusion decisions. |

`coverage.csv` groups by year/state_po/office/district/stage/special/mode, lowercasing stage/special/mode only in this audit file. It adds `source_rows`, `row_count`, `named_candidate_count` (distinct nonblank source labels, not adjudicated candidates), `candidate_names_json`, `party_labels_json` (detailed labels), `reported_totals_json` (distinct original strings), and `unofficial_values_json`. `sum_source_row_votes` sums exact nonnegative integer counts over all source categories/ballot lines within a group. `reported_total` takes one consistent repeated total; `sum_minus_reported_total` checks arithmetic. Invalid/missing/inconsistent values leave derived numeric fields blank with flags. No result vote share or margin is derived.

All groups carry `election_date_unavailable` and `round_definition_unverified`. Other flags cover unofficial/unknown booleans, missing fields/names, whitespace, noncandidate categories, repeated names, invalid counts, possible total-1 sentinels, votes exceeding total, sum mismatches and supplemental runoff cycle assignment. `issues.json` contains summary counts and flagged source-row IDs; `manifest.json` records sources, retrieval times, byte sizes, SHA-256, license, approval, transformations and output hashes. See [the results README](../data/raw/senate_results/README.md) and [review](senate_results_review.md).

## Prepared historical Texas dataset (Decision 011)

Applies to `data/processed/texas_senate_historical/20261006T024116Z/`. Original inventory fields retain their meaning, with one documented correction: `election_date` is `2024-11-05` for all 37 2024 rows. These fields describe the correction and partisan classification:

| Field | Meaning |
| --- | --- |
| election_date_basis | `538 archive election_date` for older rows; Rahan-confirmed general-election date for 2024. This is election day, not poll publication or fieldwork |
| partisan_status | `partisan` when 538 supplies a recognized party flag or marks an internal poll; `not_flagged_partisan` when the older archive has blank partisan and internal false; `unknown` for absent/unrecognized metadata, including 2024 |
| partisan_party | Original 538 party classification: DEM, REP, or IND when recognized; blank for unspecified or unknown party. It is separate from the candidates' parties |
| partisanship_basis | Identifies the source flag or reason no classification could be made. No party affiliation is inferred from a pollster's name |

`partisan` and `internal` continue to preserve the original source values. A `not_flagged_partisan` tag is not independent verification that the organization or sponsor is nonpartisan. No partisan polls are excluded by this preparation step.

`normalized.csv` and per-cycle CSVs contain 137 retained records (49/51/37). `excluded.csv` contains the 12 hypothetical 2020 questions, all original fields plus derived tags and `exclusion_reason`. `changes.csv` audits all 149 inputs using source keys, election dates before/after, date basis, original partisan/internal values, derived classifications, and kept/excluded action/reason. `manifest.json` records approval/rule version, source provenance, input/output SHA-256 hashes, counts, and limitations. Original source flags—including multiple questions within one poll—remain intact and describe the original inventory.

## Prepared national calibration inputs (Decisions 012–014)

Applies to `data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1/`. Original result/archive columns retain their meanings and values. Load with `dtype=str, keep_default_na=False` to preserve empty strings/identifiers; convert numeric columns explicitly as needed. Dates are ISO `YYYY-MM-DD`; blank means unknown. Percentages remain 0–100, without rescaling or margin calculation.

| Field | Meaning |
| --- | --- |
| `record_key` | `medsl:<original row>`, `538-row:<original row>`, or `ut2024:<tracker row>:D/R`; snapshot-local row identity. |
| `question_key` | `538:<cycle>:<race_id>:<poll_id>:<question_id>` or `ut2024:<row>`; joins inventories/crosswalks to candidate answers. |
| `contest_id` | Reviewed `<cycle>-<state_po>-ordinary/special-general/first/runoff`. Exact-round join key. Actual date is explicit; blank for unverified rounds. |
| `mapped_round_id` | Proposed source seat/stage mapping, retained even for an unverified round. Louisiana has this diagnostic ID but no registered `contest_id` or invented date. |
| `canonical_candidate_id` | Contest ID plus explicitly matched normalized name. Identical named fusion lines share it; unnamed aggregates retain distinct source-row keys. Does not combine votes. |
| `side` | `D`, `R`, `other`, `unknown`. Detailed affiliation, explicit approved exceptions/nominee evidence, official missing-label facts, or the identical candidate's major-party ballot line supply the basis. Never derived from simplified party alone. |
| `side_basis`, `basis`, reference URL fields | Explain identity/side evidence. JSON aliases preserve alternate spellings and source locators. Generic write-in status does not establish affiliation. |
| `membership` | Poll answer: `confirmed`, `confirmed_nonballot`, `unknown` in that exact round. Result mapping: `source_result_row`. |
| `status` | Contests: `eligible`, `excluded`, `pending`. Questions/crosswalks: `selected`, `excluded`, `pending`. Approved exclusion takes precedence over concurrent unknowns; all reasons remain visible. |
| `reasons`, flags | Semicolon-separated overlapping reasons/warnings. Source flags and new preparation flags are separate. Exclusive status counts differ from overlapping reason counts. |
| `cycle`, `election_date` | Source-year 2021 Georgia runoffs have cycle 2020 and date 2021-01-05. Mississippi special `gen` returns map to November 27, 2018 runoff. |
| `stage_normalized`, `mode_normalized` | Lowercase original labels. They do not replace raw columns or the verified registry round. |
| `votes`, `reported_total` | Exact nonnegative integral conversions of decimal-string source counts. Repeated totals must not be summed over candidate rows. |
| `valid_vote` | String `true` for candidate/write-in counts, `false` for BLANK/UNDER/OVER/VOID/SPOILED, `pending` for Nevada's ballot option. Result rows remain retained; blank in poll side-map rows. |
| `preparation_flags` | Blank labels, unidentified aggregates, side disagreements, unofficial returns, FEC count conflicts and pending denominator treatment. |
| `fec_reference_votes`, `reference_check` | Partial official comparison. Reference count or blank; check is `not_crosschecked`, `match`, `conflict`, `state_confirms_medsl`, or `official_first_choice_match`. MEDSL values are never replaced. |
| `contest_status`, `question_status` | Parent registry/question selection status, copied onto long rows for explicit filtering. |

`candidate_results.csv` preserves all 508 source rows/columns with the added identity, integral-count, side, round, valid-vote and reference fields above. `candidate_side_map.csv` covers every result/poll candidate with `record_type`, original source row/ID/name/party/simplified party, canonical identity, side/basis/reference, membership, valid-vote indicator and flags. Every blank label and side disagreement is flagged.

`contests.csv` contains state/cycle, ordinary-or-special `seat`, exact `round`, actual date/basis/reference, source year(s), result-row count, repeated `reported_total`, mechanical `valid_vote_total`, `noncandidate_votes`, named non-write-in `ballot_candidate_ids_json`, scope/status/reasons. `valid_vote_total` includes valid third-party/write-in counts; no D/R sum, vote share or margin is derived. It is blank for missing returns or unresolved denominator semantics, but may be present for a contest pending on side/verification grounds. `scope` is `initial_calibration` or `outside_scope`; 2024 outside Texas is inventory-only.

`poll_candidate_rows.csv` preserves original archive columns/order plus source row, record/question keys, round/identity/side/membership/evidence and final question status. Texas tracker shares become two rows, with every original field in `tracker_original_json`; no source affiliation is invented.

`poll_questions.csv` retains source IDs, stage/seat fields, original election-date text, original population (`population_raw`), full population, sample size, pollster, internal/partisan flags and URL. Dates are ISO where known; `population` is uppercase. `candidate_answers_json` retains original archive IDs/names/parties/answers/shares, or the tracker pair. `candidate_rows` counts answers. `partisanship_basis` distinguishes archive source flags from the UT source exception; UT partisanship stays unknown. Missing population remains unknown/pending unless another approved exclusion applies.

`poll_key` is archive poll ID or tracker-row key. Preference groups use `(source, poll_key, contest_id)`. `full_ballot` is string `true`/`false`, or `unknown` for tracker rows lacking a complete slate. True covers every named non-write-in result candidate, not every possible write-in or a verified primary questionnaire. Unique full-ballot LV alternatives are preferred; tied full/partial questions stay pending. A pending LV sibling holds an otherwise-selected question. `preference_basis` explains selection. No D/R share totals are computed.

`crosswalk.csv` provides question IDs, round/date mapping, full-ballot/preference and final status. `race_crosswalk.csv` preserves 72 cycle/race-ID mappings and source stage/seat metadata; seat_number is never interpreted as Senate class. `race_inventory.csv` counts all/selected/excluded/pending questions per registered round and flags `unpolled_in_archive`. `horizon_drop_status` reserves horizon-specific reporting for Rahan.

`excluded.csv`/`pending.csv` fields are `record_type`, `record_key`, `contest_id`, `status`, `reasons`; logs mix questions, contests and unresolved candidate mappings. `changes.csv` fields are `record_key`, `field`, `before`, `after`, `basis` for formatting and annotations/classifications/statuses, not raw edits. `manifest.json` records hashes, original provenance/permission receipts, output row counts, actual processing time, rule/schema version and audit counts.

See [the prepared README](../data/processed/senate_calibration/README.md) for loading/replay and [the review](calibration_preparation_review.md) for pending cases. Rahan implements side aggregation/margins, horizon cutoffs, weights, averages, errors and uncertainty.
