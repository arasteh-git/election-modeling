# Decision log

Only record agreed decisions. Unresolved choices belong in issues or review notes.

## Decision 001: Learning ownership

Rahan writes the core modeling and evaluation code. AI provides scaffolding, tutoring, review, and authorized menial implementation. This preserves the project's learning purpose.

## Decision 002: Responsibilities

ChatGPT/Codex supports project management, collection, mechanical cleaning, and infrastructure. Claude supports math, probability, audits, debugging, and bias evaluation. Rahan makes final decisions.

## Decision 003: Shared context

Use repository files for durable project context. Discuss work in chat interfaces and inspect code with Codex and Claude Code. GitHub connection is pending.

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

## Future decision template

### Decision

### Date

### Context and alternatives

### Rahan's choice

### Reasoning and tradeoffs

### Affected files

### Evidence / review
