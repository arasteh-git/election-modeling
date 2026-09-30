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

Tracking data lets every collaborator reading GitHub (Codex, Claude chat's Project sync, Claude Code) see the exact snapshot that code and results refer to, which supports PROJECT.md's rule that versioned code identify its data snapshot. Tradeoffs: every committed source must permit redistribution, and large or frequent snapshots grow the repository.

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

Resolved 2026-09-29: Rahan selected Texas as the first race (Claude Code session). Georgia and Michigan are tentative next races, not yet approved. The minimum deliverable remains undecided; first poll rules are in Decision 009.

### Evidence / review

Directed by Rahan in ChatGPT: "let's make senate races the main focus for now (house is too all over the place)".

## Decision 007: Start Texas collection with UT tracker

### Date

2026-09-29 (America/New_York)

### Rahan's choice

Start with the Texas Politics Project Senate tracker for the initial Texas polling inventory.

### Scope

Collect and mechanically standardize the tracker with provenance and discrepancy flags. Poll inclusion, weighting, uncertainty, and other model rules remain undecided.

### Evidence / review

Rahan in ChatGPT: "sure, let's start from the texas politics project senate tracker".

## Decision 008: Forecast target and timeline

### Decision

The forecast target is each candidate's win probability. The goal is a Texas Senate forecast before Election Day (November 3, 2026); a backtest-first project is an acceptable fallback.

### Date

2026-09-29

### Context and alternatives

Targets considered: vote margin, vote share, or win probability. Timeline options: pre-election forecast or backtest-first (2022/2024 backtest, 2026 scored afterward).

### Rahan's choice

Win probability; pre-election forecast preferred, backtest acceptable.

### Reasoning and tradeoffs

Win probability requires an explicit uncertainty model, not only a poll average, and that uncertainty should be calibrated against past polling error. If the project falls back to a backtest, poll release dates become relevant for leakage prevention even though they are not used in the live forecast.

### Affected files

PROJECT.md, docs/methodology.md, STATUS.md, NEXT_STEPS.md

### Evidence / review

Directed by Rahan in a Claude Code session on 2026-09-29, after Claude review.

## Decision 009: Texas poll rules

### Decision

- Include likely-voter (LV) polls only.
- Keep poll labels as reported; the same firm with a different sponsor is a separate label.
- Treat repeat polls from the same label as separate observations.
- Leave undecided and other responses as reported; no allocation and no normalization to 100.
- Compute each poll's margin as dem_pct minus rep_pct, in percentage points. The tracker's Spread column is not used (added 2026-09-29 after the row 6 AARP review).
- Date each poll by its fieldwork end date. Publication dates are not used.
- Weight polls by recency, measured from the fieldwork end date. Updated 2026-09-29: exponential decay, weight = 0.5^(age_days / h), with a working half-life of h = 14 days, to be recalibrated once historical Senate data is available.

### Date

2026-09-29

### Context and alternatives

Populations in the first snapshot: 11 LV and 5 RV of 16 rows. Alternatives reviewed: all populations, or LV preferred with RV as fallback; a firm-level pollster ID alongside labels; pollster caps or latest-poll-only for repeat polls; proportional or two-party undecided allocation; start date or midpoint dating.

### Rahan's choice

As listed above.

### Reasoning and tradeoffs

LV screens are preferred close to the election. On the first snapshot, an unweighted illustration gives mean D minus R of +1.7 for LV polls versus +3.2 for RV polls, so the rule shifts the picture toward Paxton and drops the most recent poll (NPR/Marist, RV). Treating repeat polls as separate lets a frequent pollster dominate; recency weighting reduces this for old polls but not for several recent polls from one firm. Leaving undecided voters as reported implicitly assumes they split evenly; with a win-probability target, a high undecided share should be reflected in uncertainty.

Half-life sensitivity on the first snapshot (reference date 2026-09-29, 11 LV polls): h = 7 gives +2.40 (n_eff 4.03), h = 14 gives +2.64 (n_eff 5.48), h = 30 gives +2.52 (n_eff 7.69), and unweighted gives +1.73. The average is insensitive to h within 7–30 days; applying recency weighting at all matters more.

Open: whether to use a release's LV numbers when the tracker shows only RV.

### Affected files

docs/methodology.md, PROJECT.md, STATUS.md

### Evidence / review

Directed by Rahan in a Claude Code session on 2026-09-29, after Claude review.

## Decision 010: Minimum deliverable and tiers

### Decision

- Output: P(Democrat wins) for each modeled race; ideally also P(Democrats win the Senate).
- Minimum: Texas only, using a recency-weighted likely-voter average plus an error model calibrated on past Senate polling error. The model form is undecided.
- Next level: fundamentals and pollster house effects.
- Final level: correlation between states, covering the full 2026 Senate landscape.
- Runs on demand, whenever Rahan runs it.

### Date

2026-09-29

### Context and alternatives

Choices included output (per-race win probability, chamber control, or both), races (Texas only through the full Senate map), method floor, and run frequency (one-off, on demand, or scheduled).

### Rahan's choice

As listed above.

### Reasoning and tradeoffs

P(Democrats win the Senate) depends on every seat, including unpolled races, and on correlation between states, so it belongs in the final tier. The calibration step needs historical Senate poll averages and results, computed with the same likely-voter and recency rules.

### Affected files

PROJECT.md, STATUS.md, NEXT_STEPS.md, docs/methodology.md

### Evidence / review

Directed by Rahan in a Claude Code session on 2026-09-29, after Claude review.

## Future decision template

### Decision

### Date

### Context and alternatives

### Rahan's choice

### Reasoning and tradeoffs

### Affected files

### Evidence / review

