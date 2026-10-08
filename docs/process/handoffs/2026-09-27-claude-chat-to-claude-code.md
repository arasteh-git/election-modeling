# Handoff

## Author and intended reviewer

Author: Claude (claude.ai chat, Project "election modeling?"). Intended reviewer: Claude Code. Rahan approves all changes.

## Task / issue

Onboard Claude Code to the repository (NEXT_STEPS.md step 4) and audit the scaffold. No modeling code exists yet, and none should be written in this session.

## Branch and commit

main: ef798e7

## Data snapshot / checksum

None. No data has been acquired.

## Relevant files

PROJECT.md, STATUS.md, CLAUDE.md, AGENTS.md, NEXT_STEPS.md, docs/decisions.md, docs/methodology.md, docs/data_sources.md, docs/data_dictionary.md, docs/handoff_template.md, .gitignore

## What changed

- CLAUDE.md: filled in Claude's workflow, math review, code audit, and bias evaluation protocols. "Commands and environment" left blank.
- docs/decisions.md: added Decision 004 (default hint level 2; bias evaluation covers both forecast bias and pollster house effects).
- STATUS.md: marked repo creation and the Claude chat connection done; added the open timeline decision.

## Decisions already approved by Rahan

- Decisions 001-004 in docs/decisions.md.
- Nothing else. Scope, timeline, methodology, data sources, and environment are all undecided.

## Checks performed and observed results

- Claude chat read the repository files through a read-only Project sync and wrote the three files above for Rahan to commit.

## Checks not performed

- Nothing was run. No environment exists.
- Claude chat has not seen .gitignore or the directory marker files, and has not confirmed the committed state matches the files it wrote.
- Codex's connection to the repository has not been confirmed.

## Open questions / concerns

- Timeline: Rahan prefers a forecast before the November 3, 2026 midterms but would accept backtest-first (2022/2024 backtest, 2026 scored after the fact). Not yet decided.
- Discussed in chat but NOT approved: a go/no-go checkpoint around October 18; a minimal v1 of Senate only, a simple poll average per race, sigma calibrated on past cycles, and a correlated simulation, with house effects and fundamentals deferred. Treat these as suggestions, not methodology.
- Scope and minimum deliverable (NEXT_STEPS step 6) are Rahan's next decision.

## Requested next action

1. Read PROJECT.md, STATUS.md, CLAUDE.md, and AGENTS.md. Before editing anything, summarize back to Rahan: your role, the learning boundaries, and what you will not do.
2. Audit the scaffold and report findings. Do not fix anything without Rahan's go-ahead:
   - Do the committed CLAUDE.md, docs/decisions.md, and STATUS.md match this handoff?
   - Are the docs consistent with each other (roles, boundaries, what is marked done or pending)?
   - Does .gitignore keep data/raw, data/processed, outputs, and secrets (.env, keys) out of Git while keeping the directory marker files?
3. Stop there. Environment setup belongs to Codex. Scope belongs to Rahan. Core modeling code belongs to Rahan.

## What Rahan should implement or explain

- Fill in "Branch and commit" above.
- Make the scope and minimum-deliverable decision in PROJECT.md (NEXT_STEPS step 6).
- Decide the timeline (pre-November forecast vs. backtest-first) and record it in PROJECT.md.
