# Raw data

Original source inputs, saved as timestamped snapshots with provenance and checksums. Raw files are tracked in Git (Decision 005). Preserve original snapshots, and check source redistribution permissions before committing files.

| Folder | Contents |
| --- | --- |
| [texas_tracker/](texas_tracker/README.md) | Timestamped snapshots of the 2026 Texas Senate tracker. Each holds the original webpage, extracted table, a mechanically standardized copy, provenance, and discrepancy flags. The standardized copy stays with its source and is not model-ready until analytical rules are agreed. |
| [texas_senate_historical/](texas_senate_historical/README.md) | 2018/2020 FiveThirtyEight candidate data from a pinned mirror and the 2024 UT tracker, with mechanical CSVs, retrieval details, checksums, and unresolved issue flags. |
| [senate_results/](senate_results/README.md) | The approved MEDSL V8.0 original CSV, metadata, codebook, source listing and mechanical inventories for 2018/2020/2024, plus separate Georgia 2021 runoff rows. Coverage audits retain unofficial flags, blank names, noncandidate categories and ballot lines; these are not calibrated model inputs. |
| [senate_poll_archives/](senate_poll_archives/README.md) | Collector target for the approved 2022/2024 Senate archives (Decision 017). Internet Archive connection failures have prevented a complete snapshot; do not treat the documentation folder or synthetic tests as real polling coverage. |

`.gitkeep` is an empty directory marker. See [the complete file guide](../../docs/file_guide.md).
