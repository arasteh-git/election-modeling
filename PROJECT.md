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

First collection target: Texas U.S. Senate, starting with the Texas Politics Project Senate tracker (approved 2026-09-29). Georgia remains a possible later race. Model inclusion rules and the minimum forecast deliverable remain undecided.

## Forecast target and units

## Minimum viable deliverable

## Time commitment

## Timeline

## Data budget

## Definition of done

