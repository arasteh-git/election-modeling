# Decision log

Only record agreed decisions. Unresolved choices belong in issues or review notes.

## Decision 001: Learning ownership

Rahan writes the core modeling and evaluation code. AI provides scaffolding, tutoring, review, and authorized menial implementation. This preserves the project's learning purpose.

## Decision 002: Responsibilities

ChatGPT/Codex supports project management, collection, mechanical cleaning, and infrastructure. Claude supports math, probability, audits, debugging, and bias evaluation. Rahan makes final decisions.

## Decision 003: Shared context

Use repository files for durable project context. Discuss work in chat interfaces and inspect code with Codex and Claude Code. The GitHub repository is the shared workspace; Claude chat reads it through a read-only Project sync, and Codex repository access is now confirmed through the GitHub connector.

## Decision 004: Claude tutoring and review workflow

### Decision

Claude's default hint level is 2 (explain the concept) on a four-level ladder. Bias evaluation covers both the model's systematic forecast error and pollster house effects.

### Date

2026-09-27

### Context and alternatives

Hint levels: (1) flag symptom/location, (2) explain concept, (3) pseudocode, (4) code on explicit request. Bias evaluation scope options: forecast error only, house effects only, or both.

### Rahan's choice

Default level 2; bias evaluation covers both.

### Reasoning and tradeoffs

Level 2 explains the underlying concept without supplying the solution; level 1 or 3 is available on request.

### Affected files

CLAUDE.md

### Evidence / review

Agreed in Claude chat on 2026-09-27.

## Decision 005: Data storage in Git

### Decision

All of data/ is tracked in Git. The PROJECT.md rule still applies: check each source's redistribution permissions before committing its files. outputs/ remains ignored.

### Date

2026-09-27

### Context and alternatives

The initial .gitignore kept data/raw and data/processed local until storage and redistribution were agreed, and did not cover other folders under data/. Alternatives: keep all data local, track only processed data, or track all of data/.

### Rahan's choice

Track all of data/.

### Reasoning and tradeoffs

### Affected files

.gitignore, README.md, data/raw/README.md, data/processed/README.md

### Evidence / review

Directed by Rahan in a Claude Code session on 2026-09-27.

## Decision 006: Senate focus

### Date

2026-09-27 (America/New_York)

### Rahan's choice

Focus on 2026 U.S. Senate races for now. Defer House modeling because its scope is too broad for the initial project.

### Open choice

Texas and Georgia are candidates for the first race. ChatGPT recommends Texas first, but Rahan has not yet selected a race. Statistical assumptions and the minimum deliverable remain undecided.

### Evidence / review

Directed by Rahan in ChatGPT: "let's make senate races the main focus for now (house is too all over the place)".

## Future decision template

### Decision

### Date

### Context and alternatives

### Rahan's choice

### Reasoning and tradeoffs

### Affected files

### Evidence / review
