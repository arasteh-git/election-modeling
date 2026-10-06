# Handoff

## Author and intended reviewer

Author: Claude Code. Intended reviewer: Codex. Rahan approves all changes and must confirm before Codex acts on this note.

## Task / issue

Build the candidate-to-side mapping and poll/result crosswalk needed for calibration. Claude Code's audit of the MEDSL snapshot found that party labels cannot be used to assign Democratic/Republican sides under Decision 013.

## Branch and commit

main at fb4e919. Only Rahan's notebook is modified; this handoff is uncommitted.

## Data snapshot / checksum

- Results: data/raw/senate_results/20261006T035630Z/ (senate_returns.csv SHA-256 6f745db1b4a0026ad837e74428f9ed6f3f77fa51eb6f858b58ebdbc186fdb3bd; all output hashes match manifest.json).
- Polls: data/raw/texas_senate_historical/20261006T024116Z/senate_polls_historical.csv and data/processed/texas_senate_historical/20261006T024116Z/.

## Relevant files

docs/decisions.md (Decisions 012–015), docs/calibration_preparation_plan.md (proposed crosswalk.csv and contests.csv), docs/senate_results_review.md.

## What changed

Nothing in the repository; this is an audit and a request.

## Decisions already approved by Rahan

Decisions 001–015. Most relevant is Decision 013:

- A Democratic-caucusing independent is the Democratic side; a separate Democrat on the ballot counts as other.
- Same-party races and races without both sides are excluded.
- Margin = sum of D-side − sum of R-side, same round for polls and results.
- Each round is a separate race.
- All valid candidate votes form the denominator.
- One observation per poll per round, preferring the full-ballot LV question.

## Checks performed and observed results

Read-only checks on senate_returns.csv for 2018–2024:

- 508 rows in 107 year/state/special groups. Candidate votes sum exactly to totalvotes in every group. All votes are integers.
- `party_simplified` conflicts with Decision 013 sides:
  - Maine 2018 Angus King and Vermont 2018 Bernie Sanders are `OTHER`. Under Decision 013 they are the D side; Maine's Ringelstein (DEMOCRAT) becomes other.
  - Wyoming 2020: both Lummis (R) and Ben-David (D) have blank `party_detailed` and are `OTHER`.
  - Groups lacking a DEMOCRAT or REPUBLICAN label: CA 2018 (same-party, excluded), VT 2018 (Sanders), AR 2020 (no D, excluded), WY 2020 (labels missing), NE 2024 and VT 2024 (outside current scope).
- Mississippi 2018 special: only Hyde-Smith/Espy rows exist (the November 27 runoff, labeled `gen`). The November 6 three-way first round is absent. First-round polls must not be matched to these returns.
- Noncandidate rows inside totals: IA 2020 over/under votes, ME 2020 blank votes, MA 2020 blank votes (93,869), WY 2020 over/under votes. Per Decision 013, the denominator excludes these.
- Formats: 2024 uses `GEN`/`TOTAL` while 2018/2020 use `gen`/`total`. Votes are stored as decimal strings (e.g., "344575.0").
- Texas D − R margins (all valid votes) for later checking: 2018 −2.57, 2020 −9.64, 2024 −8.50. Check values only; Rahan computes margins.

## Checks not performed

No official crosschecks of returns. No poll-side party labels audited beyond noting that 538 labels King `IND`. No scripts or tests run.

## Open questions / concerns

- Rahan must approve the explicit list of Democratic-side independents (proposed: King ME 2018, Sanders VT 2018; confirm Alaska 2020 Al Gross, an independent who won the Democratic nomination and is labeled DEMOCRAT in MEDSL).
- Other missing or ambiguous party labels found while building the mapping should be listed for Rahan, not inferred.
- Mississippi 2018 first-round returns: obtain from an approved official source, or exclude first-round polls (Rahan's call).

## Requested next action

For Codex, after Rahan confirms:

1. Build `contests.csv`: one row per contest round (state, cycle, actual election date, ordinary/special, round), including unpolled contests and Texas 2024. Assign status from Decision 013 (eligible or excluded with reason).
2. Build a candidate side mapping for each contest round, covering every result row and every poll candidate. Fields: candidate, source identifiers, side (D/R/other), and the basis for the side. Base sides on Decision 013 and the approved independents list, never on `party_simplified` alone. Flag every row where the side differs from the source party label, and every blank label.
3. Build the poll-to-contest crosswalk matching each LV question to its exact round. Apply the Decision 013 non-nominee rule and the full-ballot preference. Leave ambiguous matches pending.
4. Normalize mechanically in the prepared outputs (case of `stage`/`mode`, numeric votes) without altering the raw snapshot. Report counts in, out, and pending at each step.

Do not compute margins, averages, errors, σ, or probabilities. Rahan writes the margin function and calibration (Decision 001).

## What Rahan should implement or explain

- Fix `p_dem_win` to return a probability (0–1).
- Make `weighted_avg` handle zero eligible polls, return the number of polls used, and drop the print.
- After Codex delivers the mapping: write the margin function (side sums from the mapping, valid votes only, same round), then the calibration loop.
