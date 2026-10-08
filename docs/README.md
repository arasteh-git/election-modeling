# Project documentation

Methodology, decisions, data documentation and reviews for the project. [PROJECT.md](process/PROJECT.md) and [STATUS.md](../STATUS.md) record the shared context across Rahan, Codex, and Claude, since conversation histories are not shared; read them before starting work.

| Document | How to use it |
| --- | --- |
| [Methodology](methodology.md) | Read approved modeling assumptions and formulas; blank sections are undecided. |
| [Decisions](decisions.md) | Record consequential choices after Rahan approves them. |
| [Data sources](data_sources.md) | Check approved sources, proposed crosschecks, access/redistribution terms, and snapshot provenance; MEDSL is approved under Decision 014. |
| [Data dictionary](data_dictionary.md) | Understand implemented fields, units, keys, missing values and flags, including national calibration outputs. |
| [Data pipeline](data_pipeline.md) | Collection and preparation commands and repository layout. |
| [File guide](file_guide.md) | Navigate the repository and understand individual files. |
| [Calibration preparation plan](calibration_preparation_plan.md) | Original national preparation design, approved-rule updates and links to the implemented workflow. |
| [Calibration preparation review](calibration_preparation_review.md) | Implemented contest/side/crosswalk outputs, observed counts, factual checks, pending cases and tests. |
| [Results review](senate_results_review.md) | V8.0 coverage, preserved source flags, denominator/round limits and observed checks. |
| [Texas tracker review](texas_tracker_review.md) | Source discrepancies and primary-verification limits. |
| [2022/2024 polling source proposal](polling_sources_2022_2024_proposal.md), [initial checks](polling_source_checks_2022_2024.json) and [collection attempts](senate_archive_collection_attempts_2026_10_08.json) | Sources and scope approved by Decision 017. The collector is implemented, but complete polling retrieval is blocked by connection failures (see [the collection handoff](process/handoffs/2026-10-08-codex-to-rahan-and-claude-archive-collection.md)), so expanded polling collection and preparation are incomplete. Review schema/license evidence and remaining preparation work. |
| [Process documents](process/README.md) | Project agreement, setup checklist and dated handoffs between Rahan and the assistants. |
| [Handoff template](handoff_template.md) and [handoffs](process/handoffs/) | Transfer scoped work with branch/commit, source snapshots, observed checks, limits, and next actions. |

Run national preparation offline with `python3 -B src/clean/prepare_senate_calibration.py --output outputs/calibration_replay`, using a fresh output directory. [The prepared README](../data/processed/senate_calibration/README.md) documents outputs, loading, replay and limits. Other collection and preparation commands are in the root and source-folder READMEs.
