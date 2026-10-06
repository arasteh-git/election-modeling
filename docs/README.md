# Shared project documentation

Read [PROJECT.md](../PROJECT.md) and [STATUS.md](../STATUS.md) before starting work. These files record shared context across Rahan, Codex, and Claude; conversation histories are not automatically shared.

| Document | How to use it |
| --- | --- |
| [Calibration preparation plan](calibration_preparation_plan.md) | Review the proposed election-result sources, observed 2018/2020 archive inventory, unresolved race rules, planned outputs, and validation. This is a proposal, not an implemented collector/preparer or approved methodology. |
| [Data sources](data_sources.md) | Check approved sources, proposed sources, access and redistribution terms, and snapshot provenance. Proposed result sources require Rahan's selection before collection. |
| [Methodology](methodology.md) | Read approved modeling assumptions and formulas; blank sections remain undecided. |
| [Decisions](decisions.md) | Record consequential choices after Rahan approves them. |
| [Data dictionary](data_dictionary.md) | Understand implemented fields, units, keys, missing values, and flags. Proposed national output schemas will be added when implemented. |
| [File guide](file_guide.md) | Navigate the repository and understand individual files. |
| [Texas tracker review](texas_tracker_review.md) | Review source discrepancies and primary-verification limits. |
| [Handoff template](handoff_template.md) and [handoffs](handoffs/) | Transfer scoped work with branch/commit, source snapshots, observed checks, limits, and next actions. |

There is no command to run these plans. Existing collection/preparation commands are in the root and source-folder READMEs. After source/rule approval, implementation must document its commands, actual schemas, immutable snapshots, and generated outputs in the relevant folders.
