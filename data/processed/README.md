# Processed data

Derived inputs. Data files are tracked in Git (Decision 005). Check each source's redistribution permissions before committing its files.

The [prepared historical Texas Senate inventory](texas_senate_historical/README.md) implements Decision 011: confirmed 2024 election dates, source-based partisan tags, and exclusion of 12 hypothetical 2020 matchups, with transformation/exclusion audits and hashes. It preserves all populations for review and does not implement weighting or uncertainty calibration.

The [national Senate calibration preparation](senate_calibration/README.md) implements Decisions 012–014: contest rounds/dates, candidate sides, valid-vote categories and exact poll crosswalks with approved filters/preference. All 1,950 questions remain represented: 729 selected, 873 excluded, 348 pending. Unknown identities, parties, source conflicts and tied preferences remain visible. Existing raw/prepared sources are unchanged; Rahan implements the margin and calibration calculations.

The original historical inventory and the 2026 Texas normalized.csv remain under data/raw/ beside their source evidence. Future outputs should reflect approved inclusion and cleaning rules with links to their source snapshots.

.gitkeep is an empty directory marker.
