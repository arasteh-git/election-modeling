# Project agreement

## Goal

Build a polling-based model for the 2026 U.S. elections to learn Python, statistics, and modeling. Learning and understanding are the primary objectives.

## Collaboration

Rahan uses the ChatGPT and Claude chat interfaces for discussion, planning, and explanations. Codex and Claude Code inspect the repository and perform explicitly scoped work. Important conclusions from chats must be recorded here; chat histories are not automatically shared.

| Owner | Responsibility |
| --- | --- |
| Rahan | Scope, final modeling decisions, core code implementation, understanding results, accepting changes |
| ChatGPT / Codex | Project management, web collection, mechanical data cleaning, infrastructure automation |
| Claude / Claude Code | Math and probability tutoring, code auditing, debugging guidance, model bias evaluation |

## Learning boundaries

- Rahan writes core poll weighting, uncertainty, simulation, and evaluation logic.
- AI starts with explanations, questions, hints, and reviews. Full core implementations require an explicit request.
- AI can implement collection, mechanical cleaning, and infrastructure tasks within the assigned scope.
- Keep changes small and explain their purpose and how they were checked.
- Never treat agreement between assistants as statistical validation.

## Data boundaries

Preserve raw inputs. Log transformations and exclusions. Flag ambiguities instead of silently resolving them.

Poll inclusion, population selection, duplicate-survey adjudication, undecided allocation, imputation, outlier treatment, and pollster adjustments are methodological choices. Rahan decides them with Claude's review before Codex implements them.

Keep credentials outside Git. Check data redistribution permissions before committing source datasets. Versioned code should identify the exact data snapshot used.

## Working agreement

Use GitHub as the authoritative shared workspace once connected. Work sequentially at first. If working concurrently later, use separate branches and working directories. Review changes before merging; do not automatically merge assistant changes.

Record handoffs using docs/handoff_template.md. Identify the branch, commit, data snapshot, files, checks, and outstanding questions. Read actual files rather than relying only on handoff summaries.

## Target elections / races

Current focus: 2026 U.S. Senate races, starting with one race before expanding. House modeling is deferred.

First race: Texas U.S. Senate (selected 2026-09-29), starting with the Texas Politics Project Senate tracker. Georgia and Michigan are tentative next races. First poll rules are in Decision 009; the minimum forecast deliverable remains undecided.

## Forecast target and units

Each candidate's win probability (Decision 008).

## Minimum viable deliverable

Decision 010. Tiers build on each other:

1. Minimum: P(Democrat wins) for Texas Senate, from a recency-weighted likely-voter average plus an error model calibrated on past Senate polling error (model form undecided). Run on demand by Rahan.
2. Next level: add fundamentals and pollster house effects (including how to bring RV and partisan polls back in); σ as a smooth function of days to election; extend to more races.
3. Final level: correlation between states; cover the full 2026 Senate landscape and produce P(Democrats win the Senate).

## Time commitment

## Timeline

Goal: a Texas Senate forecast before Election Day, November 3, 2026. A backtest-first project is an acceptable fallback (Decision 008).

## Data budget

## Definition of done


## Documentation maintenance

Rahan requested on 2026-09-29 that READMEs be updated whenever things are added. All contributors should update the relevant folder README and the root README or docs/file_guide.md as needed in the same change. Explain each new file, commands, outputs, and limitations.
