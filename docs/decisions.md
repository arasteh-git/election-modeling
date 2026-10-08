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

Deferred 2026-10-05: Rahan considered down-weighting RV polls instead of excluding them and kept LV only for now. Including RV polls, likely via an estimated RV-minus-LV shift rather than down-weighting alone, will be revisited with house effects in the next tier (Decision 010).

### Affected files

docs/methodology.md, PROJECT.md, STATUS.md

### Evidence / review

Directed by Rahan in a Claude Code session on 2026-09-29, after Claude review.

## Decision 010: Minimum deliverable and tiers

### Decision

- Output: P(Democrat wins) for each modeled race; ideally also P(Democrats win the Senate).
- Minimum: Texas only, using a recency-weighted likely-voter average plus an error model calibrated on past Senate polling error. The model form is normal (Decision 015).
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

## Decision 011: Historical Texas polling corrections and matchup exclusion

### Date

2026-10-05 (America/New_York)

### Rahan's choice

- Set the election date for all 37 historical 2024 records to November 5, 2024 (`2024-11-05` in ISO format).
- Tag 2018 and 2020 observations using the source's partisan and internal-poll classifications; preserve the original fields. A party flag or internal-poll flag indicates partisan. A blank party flag with internal false is labeled `not_flagged_partisan`, rather than independently verified nonpartisan. Missing/unrecognized metadata stays `unknown`; the 2024 tracker does not supply these fields.
- Exclude the 12 hypothetical 2020 challenger matchups from the derived dataset. These questions name a Democratic challenger other than M.J. Hegar against John Cornyn. Missing or otherwise ambiguous candidate names are not automatically excluded.
- Preserve the raw snapshot and record excluded observations and corrections in the derived dataset's audit files. Tagging does not authorize excluding partisan polls.

### Affected records and limits

The derived inventory retains 137 records: 49 for 2018, 51 for 2020, and 37 for 2024. Partisan tags cover 15 retained 2018 questions and 9 retained 2020 questions. All populations remain available in this preparation step; it does not implement weighting, deduplication, uncertainty, or evaluation.

### Affected files

`src/clean/prepare_texas_history.py`, `data/processed/texas_senate_historical/20261006T024116Z/`, tests, and relevant documentation.

### Evidence / review

Rahan instructed Codex to fill the 2024 date with 11/5/24, tag partisan historical polls, and drop the 12 hypothetical 2020 matchups in this session. Partisanship describes the archived source classification; individual primary releases have not been independently checked.

## Decision 012: Error-model calibration rules

### Decision

- Polling error for a past race = actual margin minus the poll average, both D minus R, in percentage points. Positive means the Democrat beat the polls. The average uses the same rules as the live model (Decision 009: LV only, fieldwork end date, h = 14) and only polls that ended by the horizon date.
- Exclude polls tagged partisan or internal (Decision 011 tags) from calibration. Polls tagged `not_flagged_partisan`, and UT tracker polls (nonpartisan by source policy), are retained. Partisan polls are revisited with house effects.
- Compute σ at several fixed horizons before Election Day (working set: 7, 14, 28, and 42 days). Each run uses the horizon closest to its days-to-election.
- σ is the root-mean-square of the errors at each horizon, √(Σ eᵢ² / n): spread around zero (consistent with the mean-zero assumption), dividing by n, not n − 1 (added 2026-10-05).
- Assume mean error is zero when converting to probability, but measure and report the mean error by cycle.
- A race enters calibration at a given horizon if at least one eligible poll ended by then. Record n_eff per race and log every race dropped for having no polls.
- Codex to propose an election-results source for all 2018/2020 Senate races and Texas 2024, with licensing terms, for Rahan's approval.

### Date

2026-10-05

### Context and alternatives

- Partisan polls: include or exclude.
- Horizon: σ at several horizons, one fixed horizon, or σ as a smooth function of days to election.
- Mean error: assume zero or subtract the historical mean.
- Minimum polls: 1 or a higher threshold.
- Results scope: 2018/2020 plus Texas 2024, or also broader 2022/2024 polling.

### Rahan's choice

As listed above. A smooth σ(days) function is preferred long term but deferred beyond the minimum deliverable.

### Reasoning and tradeoffs

- Calibration should match the 2026 input, which contains only nonpartisan public polls. Partisan polls are released selectively (often for fundraising), a selection bias that house-effect correction cannot fix.
- Error grows with time to the election, so a single σ would be too wide or too narrow at some point in the run-up; a small horizon table is simple and honest.
- With 2–3 cycles, a persistent polling bias cannot be distinguished from a one-cycle miss.
- Logging dropped races avoids silent drops and allows checking whether thinly polled races have larger errors.
- Limitation: about 64 races come from only two cycles (2018, 2020), so error shared across states within a cycle is sampled only twice.

### Affected files

docs/methodology.md, PROJECT.md, STATUS.md

### Evidence / review

Directed by Rahan in a Claude Code session on 2026-10-05, after Claude review.

## Decision 013: Calibration race-format rules

### Decision

- An independent who caucuses with Democrats is the Democratic side (e.g., Maine and Vermont 2018). If a separate Democrat also runs, that candidate counts as other.
- Same-party general elections (California 2018) are excluded from calibration.
- Margin = sum of all Democratic-side candidates − sum of all Republican-side candidates, measured in the same round for polls and results. For ordinary races this reduces to D − R. It applies to jungle first rounds and ranked-choice races (using first-choice numbers in both polls and results).
- Special elections and runoffs are included. Each poll is matched to the result of the round it asked about.
- Added 2026-10-05 (approving Claude's recommendations on Codex's open cases):
  - Races without both a Democratic-side and a Republican-side candidate (e.g., Arkansas 2020) are excluded.
  - Each round for a seat (jungle first round, runoff) counts as a separate race; rounds for the same seat are not independent.
  - Result vote shares use all valid votes, including third-party and write-in votes.
  - LIB and `REP,REF` partisan flags count as partisan, so those polls are excluded from calibration.
  - Outside Texas, exclude a question if any candidate it compares was not on that round's actual ballot. Missing or uncertain identities stay pending.
  - One observation per poll per round. Where a poll has several LV questions, prefer the full-ballot question.

### Date

2026-10-05

### Context and alternatives

Raised by the Decision 012 handoff and Codex's calibration preparation plan. Alternatives considered:

- Independents: exclude, or use official affiliation only.
- Same-party races: keep with incumbent-as-Democrat labeling.
- Multi-candidate rounds: top-two head-to-head only.

### Rahan's choice

As listed above.

### Reasoning and tradeoffs

- Democratic-caucusing independents play the Democratic role in these races.
- Same-party races behave differently: many voters of the other party are undecided or skip the race, and the sign convention loses meaning. Excluding California 2018 costs one race.
- Summing by party gives one rule for ordinary, jungle, and ranked-choice rounds.
- The added rules close the cases Codex's plan left open. Counting rounds separately adds observations that share a seat, so they are not fully independent.

### Affected files

docs/methodology.md, STATUS.md

### Evidence / review

Directed by Rahan in a Claude Code session on 2026-10-05, after Claude review.

## Decision 014: Election-results source approval

### Date

2026-10-05 (America/New_York)

### Rahan's choice

Approve the proposed MIT Election Data and Science Lab U.S. Senate statewide returns, Harvard Dataverse DOI `10.7910/DVN/PEJ5QU`, version 8.0, as the main election-results source for 2018, 2020, and 2024. Preserve the versioned source, metadata, attribution, license, retrieval times, and checksums; audit actual coverage before analytical preparation.

### Scope and limits

This authorizes collection and mechanical inventory of returns for all three years. Decision 012's initial polling calibration scope remains all 2018/2020 Senate races plus Texas 2024. Decision 013, including its subsequent approved additions, governs analytical preparation; this source approval adds no new modeling rule. Actual dates, round coverage, candidate identities, ballot-line aggregation, unofficial flags and first-choice return definitions still need verification. Official-source crosschecks remain proposed separately.

### Evidence / review

Rahan in this Codex session: "you have approval on the election results source for 2018/20/24!"

## Decision 015: Error distribution

### Decision

The minimum deliverable uses a normal error distribution: P(Democrat wins) = Φ(average / σ), with σ the calibrated RMSE at the nearest horizon (Decision 012). A t-distribution is tested in the sensitivity analysis.

### Date

2026-10-06

### Context and alternatives

Normal versus t-distribution with ν degrees of freedom (heavier tails; reduces to the normal as ν grows).

### Rahan's choice

Normal for the minimum version; test t in sensitivity analysis.

### Reasoning and tradeoffs

The normal is simplest. Its tails are thin, so it understates the chance of a large industry-wide polling miss, and σ itself is estimated from only two to three cycles. Both are arguments for t.

For the sensitivity test, match t's standard deviation to the RMSE: scale = σ · √((ν − 2) / ν). A t with the same SD is more confident on moderate leads and less confident on large ones. Toy example, average +3.32 and σ = 5: normal 74.7%, t(ν = 5) 78.5%.

### Affected files

docs/methodology.md

### Evidence / review

Directed by Rahan in a Claude Code session on 2026-10-06, after Claude review.

## Decision 016: No bias correction; σ stays RMSE

### Decision

Keep σ = RMSE of calibration errors (Decision 012) and do not shift the poll average by the historical mean error.

### Date

2026-10-07

### Context and alternatives

The first calibration run found a mean error of about −3 to −4 points (polls overstated Democrats): roughly −0.1 to −1.8 in 2018 and −5 to −6.5 in 2020. RMSE² = mean² + SD², so about a third of σ² at 28 days is this lean. Alternatives:

- σ = SD with no shift (assumes no bias; overconfident).
- Shift the average by the mean error and use σ = SD (assumes the 2018/2020 lean repeats).

On the 2026 Texas average (+3.32), these give about 68% (RMSE), 71% (SD, no shift) and 46% (shift plus SD) for the Democrat.

### Rahan's choice

σ = RMSE, no shift.

### Reasoning and tradeoffs

The direction of the next cycle's polling bias cannot be predicted, so it is treated as another source of randomness, which RMSE includes. Shifting would bet heavily on two cycles of history. The cost is a wider σ if the lean does repeat.

### Affected files

docs/methodology.md, STATUS.md

### Evidence / review

Directed by Rahan in a Claude Code session on 2026-10-07, after Claude review: "let's keep RMSE as our sigma."

## Decision 017: Expand Senate calibration to 2022/2024

### Decision

Approve the two FiveThirtyEight historical Senate CSV captures in [the source proposal](polling_sources_2022_2024_proposal.md): Internet Archive `20230427025758` for cycle 2022 and `20250118200335` for cycle 2024. Authorize immutable collection and coverage inventory, then extend mechanical preparation under existing Decisions 012/013. Expand Decision 012's historical calibration scope to all-state 2018/2020/2022/2024, retaining the current Texas 2024 tracker inputs and source exception; new 538 Texas 2024 observations are overlap inventory, not additional active polls.

Extend Decision 014's MEDSL V8.0 approval to 2022, using the unchanged already-preserved original CSV. Preserve prior snapshots. Provide wide working tables alongside detailed audit outputs. Ambiguous round mappings, independent sides, ballot membership, missing fields and denominator/first-choice evidence stay pending; approval adds no new inclusion, adjustment or model rule.

### Date

2026-10-08

### Evidence / review

Rahan replied “approved!” to Codex's explicit request to approve the two archives, MEDSL 2022 use and all-state 2022/2024 calibration expansion. The proposal and source checks document access, permission evidence, field coverage and unresolved questions. Rahan retains core model implementation and final methodological decisions.

### Affected files

docs/data_sources.md, docs/methodology.md, STATUS.md, collection/preparation code, new immutable raw/processed snapshots and their documentation. No notebook or core-model change authorized by this approval.

## Future decision template

### Decision

### Date

### Context and alternatives

### Rahan's choice

### Reasoning and tradeoffs

### Affected files

### Evidence / review
