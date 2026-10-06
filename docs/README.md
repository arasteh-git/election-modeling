# Shared project documentation

Read [PROJECT.md](../PROJECT.md) and [STATUS.md](../STATUS.md) before starting work. These files record shared context across Rahan, Codex, and Claude; conversation histories are not automatically shared.

| Document | How to use it |
| --- | --- |
| [Calibration preparation plan](calibration_preparation_plan.md) | Original national preparation design, approved-rule updates and links to the implemented workflow. |
| [Calibration preparation review](calibration_preparation_review.md) | Implemented contest/side/crosswalk outputs, observed counts, factual checks, pending cases and tests. |
| [Results review](senate_results_review.md) | Read the collected V8.0 coverage, preserved source flags, denominator/round limits and checks observed. |
| [Data sources](data_sources.md) | Check approved sources, proposed crosschecks, access/redistribution terms, and snapshot provenance; MEDSL is approved under Decision 014. |
| [Methodology](methodology.md) | Read approved modeling assumptions and formulas; blank sections remain undecided. |
| [Decisions](decisions.md) | Record consequential choices after Rahan approves them. |
| [Data dictionary](data_dictionary.md) | Understand implemented fields, units, keys, missing values and flags, including national calibration outputs. |
| [File guide](file_guide.md) | Navigate the repository and understand individual files. |
| [Texas tracker review](texas_tracker_review.md) | Review source discrepancies and primary-verification limits. |
| [Handoff template](handoff_template.md) and [handoffs](handoffs/) | Transfer scoped work with branch/commit, source snapshots, observed checks, limits, and next actions. |

Run national preparation offline with `python3 -B src/clean/prepare_senate_calibration.py --output outputs/calibration_replay`, using a fresh output directory. [The prepared README](../data/processed/senate_calibration/README.md) documents outputs/loading/replay and limits. Existing collection/preparation commands are in the root and source-folder READMEs.
