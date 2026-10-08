# Handoff

## Author and intended reviewer

Claude Code → Rahan.

## Task / issue

Portfolio cleanup so the repository can be linked from Rahan's resume: fix fresh-clone test failures, add a pinned environment, move Rahan's model code from the notebook into `src/` (mechanical refactor), rewrite the README as a front page, organize process docs, add one chart, and add a TODO placeholder for bias-shift sensitivity. Constraint: no changes to methodology, poll rules, weights, σ or forecast numbers.

## Branch and commit

Branch `cleanup/portfolio`, based on `main` at `ccb41c0`. **Not pushed and no PR yet:** `git push` failed because github.com:443 was unreachable from this machine (`gh` itself was logged in). The PR description is ready; see Requested next action. **Not merged.** Work was done in a separate worktree (`../election-modeling-portfolio`), so the uncommitted edits in the main working copy (see Open questions) were not touched.

## Data snapshot / checksum

Data content unchanged; only line-ending bytes were restored (below). Forecast inputs: tracker `data/raw/texas_tracker/20261008T042800Z/`, calibration `data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1/`.

## Relevant files

**Fresh-clone fix**

- Added `.gitattributes`.
- Restored bytes in 28 files:
  - `data/raw/senate_results/20261006T035630Z/`: `candidate_rows.csv`, `coverage.csv`, `returns_2018.csv`, `returns_2020.csv`, `returns_2021.csv`, `returns_2024.csv`, `sources.csv`.
  - `data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1/`: `candidate_results.csv`, `candidate_side_map.csv`, `changes.csv`, `contests.csv`, `crosswalk.csv`, `excluded.csv`, `pending.csv`, `poll_candidate_rows.csv`, `poll_questions.csv`, `race_crosswalk.csv`, `race_inventory.csv`.
  - `data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1_wide/`: `polls_wide.csv`, `results_wide.csv`.
  - `data/processed/senate_results_2022/20261006T035630Z_decision017_v1/`: `coverage.csv`, `returns_2022.csv`.
  - `data/processed/texas_senate_historical/20261006T024116Z/`: `changes.csv`, `excluded.csv`, `normalized.csv`, `texas_2018.csv`, `texas_2020.csv`, `texas_2024.csv`.

**Environment**

- Added `requirements.txt` and `pyproject.toml` (pytest settings only).

**Refactor**

- Added `src/__init__.py`, `src/model/__init__.py` and `src/evaluate/__init__.py` (all empty).
- Added `src/model/polling_average.py`, `src/model/win_probability.py`, `src/model/run_texas.py` and `src/evaluate/calibration.py`.
- Replaced `notebooks/data-pulls.ipynb` with `notebooks/texas_forecast.ipynb`. Git records this as a delete plus an add because the cells changed. The original is in history at `ccb41c0`.
- Added `tests/test_texas_model.py`.
- Edited `tests/test_prepare_senate_calibration.py`: only the notebook path in its preservation check changed.

**Chart**

- Added `src/evaluate/plot_calibration.py` and `docs/img/calibration_errors.png`.

**Docs**

- Rewrote `README.md`.
- Added `docs/data_pipeline.md` (collector paragraphs moved from the README) and `docs/process/README.md`.
- Moved, with link fixes only:
  - `PROJECT.md` → `docs/process/PROJECT.md`
  - `NEXT_STEPS.md` → `docs/process/NEXT_STEPS.md`
  - `docs/handoffs/` → `docs/process/handoffs/`
- `CLAUDE.md` and `AGENTS.md` stay at the root; their "Read PROJECT.md" line now points to `docs/process/PROJECT.md`.
- Link updates in `docs/README.md`, `docs/calibration_preparation_plan.md`, `docs/calibration_preparation_review.md`, `docs/polling_sources_2022_2024_proposal.md`, `data/raw/senate_poll_archives/README.md` and the moved handoffs.
- `docs/methodology.md`: added a bias-shift sensitivity TODO subsection.
- `docs/file_guide.md`, `notebooks/README.md`, `src/model/README.md`, `src/evaluate/README.md`, `tests/README.md`: updated for the new and moved files.
- `STATUS.md`: new Completed entry, the sensitivity TODO, and the environment item removed from Not yet done.
- This handoff.

## What changed

1. **Fresh-clone hash failures.** Python's `csv` writer emits CRLF. When these files were committed, Git (`core.autocrlf=input`) stored LF, so every clone got bytes that no longer matched the manifest SHA-256. The problem was wider than `sources.csv`: 28 hashed files were affected. Your local working copies still held the original CRLF bytes. Each file was copied from there only after its SHA-256 matched the manifest (or, for the Texas historical CSVs, the `output_sha256` the preparer checks) exactly. `.gitattributes` now marks `data/raw/**` and `data/processed/**` as `-text`.
2. **Refactor.** Logic is copied unchanged, including h = 14, σ from the 28-day horizon, and no bias shift. The only edits:
   - `weighted_avg` uses `.copy()` after the date filter and no longer prints "No polls found".
   - `p_dem_win` returns without printing.
   - The calibration loop returns `(errors, dropped)`.
   - `error_summary` reproduces the notebook's groupby mean error / RMSE and adds a race count.
3. **Notebook.** The notebook imports from `src/`, the `%pip install` cell is gone, and it was re-executed in a clean venv. Its outputs contain no local paths. Two exploratory cells were dropped because the functions already do their work: the manual `for` loop/n_eff cell duplicating `weighted_avg`, and the `p_dem_win(3.32, 5)` test. Both are still in history.
4. **README.** Every number comes from STATUS.md, docs/methodology.md or the code output. Nothing new is claimed.

## Decisions already approved by Rahan

All modeling choices are unchanged: Decisions 009, 010, 012, 013, 015, 016, 017, 018. Rahan explicitly requested this refactor of his core code in this session.

## Checks performed and observed results

- **Hash audit.** Every 64-hex value in every `data/**/manifest.json` was compared with every tracked file's bytes. Before the fix, 28 tracked files mismatched on a fresh checkout. After it, all 45 tracked hashes match. Nine recorded hashes have no tracked file, and that's expected:
  - six `reference_sources` stored under the ignored `outputs/` folder (FEC/ME/WY/AK/Senate reference downloads), never tracked;
  - three `src/clean/calibration_references/*.json` files, which do match (they sit outside `data/`, so the audit didn't scan them).
- **Fresh clone.** Cloned `cleanup/portfolio` into a new directory, created a new Python 3.14.5 venv and ran `pip install -r requirements.txt`. Results:
  - `python -m pytest`: **34 passed** (29 existing + 5 new).
  - `python -B -m unittest discover -s tests`: **34 OK**.
  - `git status` clean afterwards.
- **Refactor vs notebook.** `python -m src.model.run_texas` prints:
  - average +3.952 (full precision 3.9519617448017574, identical to the notebook's saved output);
  - n_eff 6.705 (6.705115664083077);
  - σ(28) 7.030;
  - P(D) 0.713 (0.7130040229861502);
  - RMSE 6.50 / 6.80 / 7.03 / 6.45;
  - races 50 / 50 / 50 / 47 and 11 dropped contest-horizons.

  `tests/test_texas_model.py` asserts all of these, plus mean error by horizon and selected by-cycle values.
- **Warnings.** `run_texas` runs with `-W error::Warning` and raises no SettingWithCopy or other warnings.
- **Links.** All relative Markdown links resolve except four inside `data/raw/texas_senate_historical/20261006T024116Z/fivethirtyeight_polls_README.md`. That file is upstream evidence, and those links were already broken before this change.
- **Notebook.** Validated with `nbformat`. Saved outputs searched for `/Users`, `/private`, `/tmp`, `site-packages`: none.
- **Chart.** Rendered and inspected visually.

## Checks not performed

- The old notebook was not re-run; expected values come from its saved outputs at `ccb41c0`.
- The fresh clone came from the local branch (file://), not from GitHub, because the push failed. Repeat it from GitHub after pushing.
- No check on Python versions other than 3.14.5.

## Open questions / concerns

- **Uncommitted edits in the main working copy.** `STATUS.md`, `docs/README.md` and `docs/handoffs/2026-10-08-codex-to-rahan-and-claude-archive-collection.md` have uncommitted notes about the download deferral. They are not in this branch. After merging, that handoff lives at `docs/process/handoffs/…`, and STATUS.md will conflict. Commit or stash them first and expect a small merge.
- **Unhashed CRLF files.** Seventeen other CSVs in your working copy are CRLF while Git stores LF. Examples are the `texas_tracker/*/tracker.csv` and `normalized.csv` files and the raw `texas_senate_historical` CSVs. No manifest records their hashes, so there was nothing to verify them against, and they were left as committed (LF). With `-text` now set, your local copies will show as modified after you merge. Decide whether to commit the CRLF originals or check out the LF versions; content is identical either way.
- **Pre-fix baseline, measured.** A fresh clone of `main` at `ccb41c0` with the same clean venv gives pytest 4 failed + 9 errors (13 of 29), matching the reported failure. Unittest shows 5 errors because its class setup fails before the individual tests run. The first mismatch reported is `sources.csv`; the Texas historical CSVs would have failed next, because `verified_inputs` stops at the first mismatch.

## Requested next action

Push and open the PR once GitHub is reachable: `git push -u origin cleanup/portfolio`, then `gh pr create --base main --head cleanup/portfolio --title "Portfolio cleanup: fresh-clone fix, src/ refactor, README" --body-file <saved description>`. Review and merge when satisfied (not merged by Claude). Then implement the bias-shift sensitivity check (TODO in README.md and docs/methodology.md).

## What Rahan should implement or explain

- Bias-shift sensitivity: P(D) with no shift versus with the average shifted by the calibration mean error.
- Confirm the README wording on the division of labor.
