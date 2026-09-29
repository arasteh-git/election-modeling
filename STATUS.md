# Project status

## Current milestone

Collect the first Texas Senate polling inventory and prepare source review.

## Completed

- Agreed on the division of responsibilities between Rahan, ChatGPT/Codex, and Claude/Claude Code.
- Created the initial documentation and directory scaffold.
- Left unselected scope, methodology, data sources, and environment settings blank.
- Created the private GitHub repository and connected it to the Claude chat Project (read-only sync).
- Filled CLAUDE.md with the tutoring and review workflow (Decision 004).
- Onboarded Claude Code (NEXT_STEPS step 4): it summarized its boundaries and audited the scaffold against the 2026-09-27 handoff.
- Applied audit follow-ups:
  - CLAUDE.md now tells Claude to keep STATUS.md current.
  - README.md documents docs/handoffs/.
  - Decision 003 wording now reflects the repository connection.
- Tracked all of data/ in Git (Decision 005).
- .gitignore now covers key and credential files and .idea/; .idea/ was removed from tracking.

- Confirmed Codex repository access through the GitHub connector.
- Confirmed Senate races as the current focus; House modeling is deferred.

- Selected the Texas Politics Project tracker as the first Texas collection source (Decision 007).
- Extracted 16 tracker rows into a reproducible timestamped source snapshot and CSVs; recorded a spread discrepancy and primary-review limits.

- Added a file-by-file guide, expanded relevant folder READMEs, and recorded the standing README-maintenance rule.

## Not yet done

- Local Python environment setup.
- Definition of the minimum forecast deliverable.
- Timeline decision: pre-November 3 forecast vs. backtest-first.
- Approval of model methodology and data rules.
- Complete primary-source verification, analytical data cleaning, modeling, and evaluation.

## Next action

Review docs/texas_tracker_review.md, prioritize the AARP discrepancy and remaining primary releases, and agree on data inclusion rules with Claude. Confirm remaining environment details and the minimum forecast deliverable.

## Active branch / commit

The Texas ingestion PR #2 is merged. Current documentation update: codex/file-guide-readmes (see pull request for commit).

## Data snapshot

data/raw/texas_tracker/20260929T222648Z/ — 16 tracker rows; source last updated September 23, 2026. Extraction is complete; primary verification is incomplete.

## Blockers

