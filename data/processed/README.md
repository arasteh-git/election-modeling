# Processed data

Inputs derived from the raw snapshots under approved cleaning and inclusion rules, with links back to their source snapshots. Data files are tracked in Git (Decision 005); check each source's redistribution permissions before committing its files.

| Folder | Contents |
| --- | --- |
| [texas_senate_historical/](texas_senate_historical/README.md) | Prepared historical Texas Senate inventory (Decision 011): confirmed 2024 election dates, source-based partisan tags, and exclusion of 12 hypothetical 2020 matchups, with transformation and exclusion audits and hashes. All populations are kept for review. |
| [senate_calibration/](senate_calibration/README.md) | National Senate calibration preparation (Decisions 012–014): contest rounds and dates, candidate sides, valid-vote categories, and exact poll crosswalks with the approved filters and preference. All 1,950 questions are represented: 729 selected, 873 excluded, 348 pending. Unknown identities, parties, source conflicts and tied preferences stay visible. |
| [senate_calibration/ wide tables](senate_calibration/README.md#wide-working-tables-existing-v1-inputs) | The v1 sample as 108 contest/round rows and 729 selected-question rows, with audited side sums and explicit unknown counts. |
| [senate_results_2022/](senate_results_2022/README.md) | 2022 MEDSL source inventory (Decision 017): 168 unchanged rows in 36 source groups, built from the preserved original. Not side-mapped calibration data. |

The original historical inventory and the 2026 Texas `normalized.csv` stay under `data/raw/` beside their source evidence. `.gitkeep` is an empty directory marker.

## Limitations

- These files contain no weighting, margins or uncertainty calibration. Rahan implements those calculations.
- The wide tables cover the existing v1 inputs only; they include no 2022/2024 polling.
