# Handoff

## Author and intended reviewer

Codex to Rahan and Claude. Rahan approves modeling decisions; this file does not invoke Claude.

## Task / issue

Rahan requested historical Texas Senate polling data on 2026-10-05. Collect recent completed cycles with raw evidence, provenance, mechanical CSVs, and issue flags.

## Branch and commit

main at 087740e97f71b1663a25b82a9d4e14aee6565ce8 before this work; changes uncommitted.

## Data snapshot / checksum

`data/raw/texas_senate_historical/20261006T024116Z/`. Per-source retrieval times and SHA-256 hashes are in manifest.json. Older archive SHA-256: `f781e2dad7b5fa0b0f9b3d453c35ae0efb2ce431b38573d2aa3164aa9d8808dd`. UT HTML SHA-256: `7354a80bec6ae6fbcd00918e3a323c14e142c1f9fae4026ee3a13f30d2a7d7b2`.

## Relevant files

`src/ingest/texas_senate_historical.py`, historical raw README/snapshot, `docs/data_sources.md`, `docs/data_dictionary.md`, folder READMEs, root README/file guide, STATUS.md. Rahan's notebook is unchanged.

## What changed

- 2018: 49 question records, 29 LV; 2020: 63 question records, 40 LV; 2024: 37 tracker rows, 23 LV. LV totals are descriptive, not a selected sample.
- Preserved 262 original Texas candidate rows from the pinned mirror and all 37 tracker rows. Grouped candidate rows by source question without dropping alternate populations/questions/hypotheticals.
- Added combined/per-cycle mechanical CSVs, manifest, issues, original source bytes and publisher license documentation; standard-library collection and offline replay.
- Corrected stale notebook README/root descriptions and active commit in STATUS.md while documenting the new inventory.

## Decisions already approved by Rahan

Standing Decisions 001–010 remain applicable. Rahan's current request authorizes historical Texas data collection. Specific historical analytical source/inclusion, uncertainty, calibration, and availability rules remain unapproved; no new modeling decision was recorded.

## Checks performed and observed results

Live source retrieval and mechanical validation succeeded. 149 output records; 262 candidate answers preserved in both the older extract and grouped JSON. Unique source/snapshot row keys. Every primary verification stays pending. The malformed 2024 `8/24/8/29/2024` interval yields blank dates and a flag. Offline replay regenerated all snapshot files byte-for-byte, preserved source hashes/retrieval times, and refused overwrite. HTML posing as CSV and changed tracker headers rejected.

Flag counts: `{"forced_undecided_source_note": 1, "hypothetical_or_unexpected_matchup": 12, "mirror_not_verified_against_original": 112, "missing_moe": 3, "missing_population": 1, "missing_release_url": 1, "missing_sample_size": 1, "multiple_questions_same_poll": 35, "nonstandard_population": 8, "publication_date_unavailable": 37, "publication_date_unverified": 112, "release_url_shared_across_labels": 4, "spread_mismatch": 3, "unparsed_field_dates": 1}`. Generated checks/replay files are in ignored outputs/, not model code.

## Checks not performed

No individual historical primary release verification, original-versus-mirror byte comparison, poll deduplication adjudication, historical release-time verification, election-result retrieval, historical averages, uncertainty calibration, or notebook rerun. Local environment reproducibility is still unresolved.

## Open questions / concerns

2018/2020 archive is preserved by a third party at a pinned 2022 revision; exact identity with original 538 bytes is unverified. 2024 uses UT's tracker ending with its October 30 update, so source coverage differs and later polls may be missing. Hypothetical 2020 candidates, multiple questions per poll, and forced-undecided source treatment need review. Publication dates are unavailable/unverified; created_at is not a substitute. 2024 spread mismatches, missing MOEs/links, and a link shared across Activote and Morning Consult remain flagged and unchanged. Three Texas elections are too few independent race outcomes for a reliable general Senate error calibration.

## Requested next action

Rahan and Claude: review candidate matchups, duplicate questions, source-forced undecided values, historical population rules, forecast cutoff/availability, and the uncertainty model. Approve historical results and a broader Senate sample before calibration.

## What Rahan should implement or explain

Load `normalized.csv` into pandas using the historical README example. Explain the difference between candidate rows, questions, tracker rows, and independent surveys before choosing the modeling observations. Core averaging, error-model, and evaluation work remains Rahan's.
