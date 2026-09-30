# Handoff

## Author and intended reviewer

Author: Claude Code. Intended reviewer: Codex. Rahan approves all changes.

## Task / issue

Keep Codex current after a Claude Code session that reviewed the Texas tracker handoff (docs/handoffs/2026-09-29-codex-to-rahan-and-claude.md), recorded Rahan's scope and methodology decisions, and reviewed Rahan's first poll average.

## Branch and commit

main. Earlier work in this session is in 968d8e3 and 405e5f7. The rest (STATUS.md, docs/decisions.md, docs/methodology.md, notebooks/data-pulls.ipynb, and this handoff) is being committed by Rahan; see the commit that adds this file.

## Data snapshot / checksum

data/raw/texas_tracker/20260929T222648Z/ (source SHA-256 637b2334c5f83acb7bac115b423ae2fc2a35863fdca1e1eb05e84c1717fe1d0b, verified against manifest.json). Unchanged in this session.

## Relevant files

PROJECT.md, STATUS.md, NEXT_STEPS.md, README.md, docs/decisions.md, docs/methodology.md, docs/texas_tracker_review.md, docs/file_guide.md, notebooks/data-pulls.ipynb (Rahan's work).

## What changed

- docs/decisions.md:
  - Decision 005: reasoning filled in.
  - Decision 006: Texas selected as first race; Georgia and Michigan tentative.
  - New Decisions 008 (win-probability target; pre-election goal with backtest fallback), 009 (Texas poll rules), and 010 (minimum deliverable and tiers).
- docs/methodology.md: forecast target, scope, margin definition, inclusion, population, undecided, weighting, uncertainty (direction only), and sensitivity sections filled from Decisions 008–010. The remaining sections are blank and undecided.
- PROJECT.md: first race, forecast target, timeline, and minimum viable deliverable.
- docs/texas_tracker_review.md:
  - Row 14 verified by Rahan: candidate shares correct; the tracker's Other column understates non-major responses (16 in the release vs. 10).
  - Row 6 AARP mismatch accepted by Rahan as rounding; the original report is still unopened.
- STATUS.md, NEXT_STEPS.md, README.md, docs/file_guide.md: brought in line with the above.
- Rahan's notebook computes the first Texas average; Claude reviewed it but did not edit it.

## Decisions already approved by Rahan

Decisions 005 (reasoning), 006 (race selection), 008, 009, and 010. In brief:

- Output P(Democrat wins) per race. The minimum is Texas only; P(Democrats win the Senate) is the final tier.
- LV polls only. Labels as reported (same firm with a different sponsor is a separate label). Repeat polls are separate observations.
- Undecided left as reported. Margin = dem_pct − rep_pct (tracker Spread not used). Poll date = fieldwork end date; publication dates not used.
- Exponential recency weighting, weight = 0.5^(age_days / h), working h = 14 days.
- Error model calibrated on past Senate polling error; model form undecided.

## Checks performed and observed results

- Snapshot: 16 rows in both CSVs, 16 distinct release URLs, SHA-256 matches manifest, Talarico → dem_pct and Paxton → rep_pct in every row.
- Row sums: row 14 summed to 95% in the tracker (now explained, see above).
- Rahan's weighted average and n_eff recomputed independently by Claude from normalized.csv (reference date 2026-09-29, 11 LV polls): h = 7 gives +2.40 (n_eff 4.03), h = 14 gives +2.64 (5.48), h = 30 gives +2.52 (7.69). All match Rahan's results.

## Checks not performed

- The ingest script was read but not run; the live source was not fetched.
- Of the primary releases, only rows 3 (by Codex) and 14 (by Rahan) have been verified; 13 remain.
- Local environment: a .venv with Python 3.14 exists and the notebook runs, but no reproducible setup has been recorded.

## Open questions / concerns

- Whether to use a release's LV numbers when the tracker shows only RV (e.g., NPR/Marist). Open for Rahan.
- docs/texas_tracker_review.md "Next review" still says to record publication dates, which conflicts with Decision 009. Not yet changed.
- Undefined for later tiers: who counts as "Democrat" where an independent runs, runoff handling (Georgia), and the Senate control threshold.
- Consider a firm-level pollster ID column alongside poll_label for future house-effect work. Suggestion only; not approved.

## Requested next action

For Codex, pending Rahan's confirmation:

1. Propose candidate sources of historical Senate polls and results (e.g., 2018–2024) for calibrating polling error, with access and redistribution terms. Do not collect until Rahan approves the sources in docs/data_sources.md.
2. When environment details are confirmed, record a reproducible setup (the notebook already uses pandas, numpy, matplotlib, and plotnine in .venv).

Do not implement weighting, the error model, simulation, or evaluation; these are Rahan's (Decision 001).

## What Rahan should implement or explain

- Set h = 14 in the notebook; the last run used h = 30.
- Next: the error model. Think through where a realistic σ for Senate polling error comes from, and what historical data it needs.
