# 2026 Election Modeling

A personal learning project by Rahan Arasteh: use polling to forecast 2026 U.S. elections while developing Python, statistics, and modeling skills.

## Start here

1. Read PROJECT.md for responsibilities and learning boundaries.
2. Read STATUS.md for the current state.
3. Follow NEXT_STEPS.md to set up the repository.
4. Record approved statistical choices in docs/methodology.md.

Blank sections are intentional: they represent decisions not yet made. Suggestions from earlier chats are not approved methodology.

## Repository URL
https://github.com/arasteh-git/election-modeling

## Election scope
Eventually all 2026 U.S. Senate and Governor elections. Perhaps House elections
as well if time permits. Starting with one Senate election then implementing more.

## Python version
Python 3.14.1

## Environment setup

## Data acquisition command

## Model execution command

## Evaluation command

## Structure

- docs/: methodology, data definitions, sources, decisions, and the handoff template.
- docs/handoffs/: dated handoff notes between assistants and Rahan (YYYY-MM-DD-from-to.md), based on docs/handoff_template.md.
- data/raw/: original source inputs; tracked in Git (Decision 005).
- data/processed/: derived inputs; tracked in Git (Decision 005).
- notebooks/: Rahan's exploration and learning work.
- src/ingest/ and src/clean/: collection and mechanical cleaning.
- src/model/ and src/evaluate/: Rahan's core modeling and evaluation code.
- tests/: future data validation and meaningful checks.

No model, poll records, dependencies, or executable workflow has been implemented.
