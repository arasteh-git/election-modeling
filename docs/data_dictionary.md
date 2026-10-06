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
