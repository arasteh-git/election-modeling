# Notebooks

Rahan's exploration and learning work.

- texas_forecast.ipynb (formerly data-pulls.ipynb): Rahan's Texas forecast notebook. It imports the model and calibration functions from `src/model/` and `src/evaluate/`, loads the 2026 Texas snapshot, computes the recency-weighted LV average, runs the historical calibration, and converts the average to P(Democrat wins). Install packages with `pip install -r requirements.txt` (plus Jupyter); the notebook no longer installs them itself. Saved outputs are from a 2026-10-08 run.
- .gitkeep: empty directory marker.

Use [the file guide](../docs/file_guide.md) and [data dictionary](../docs/data_dictionary.md) when exploring the Texas CSVs. Paths depend on the notebook's working directory; from notebooks/, the snapshot is under ../data/raw/texas_tracker/.

## Election-results inventory

The approved raw MEDSL source is saved without model margins. The separate prepared crosswalk is described below. From a kernel working in `notebooks/`:

```python
returns_2024 = pd.read_csv('../data/raw/senate_results/20261006T035630Z/returns_2024.csv')
texas_returns_2024 = returns_2024[returns_2024['state_po'] == 'TX']
```

2018/2020 subsets are alongside it; Georgia's January runoffs remain in a separate 2021 file. [The results README](../data/raw/senate_results/README.md) documents fields, exact-string loading, replay and limits. Decision 013 approves a valid-vote denominator including third-party/write-in votes; [source flags](../docs/senate_results_review.md), ballot lines and round definitions still need verification before computing it.

## Historical inventory

From a kernel working in `notebooks/`, load the prepared historical data (Decision 011) with:

```python
history = pd.read_csv('../data/processed/texas_senate_historical/20261006T024116Z/normalized.csv')
```

Per-cycle files `texas_2018.csv`, `texas_2020.csv`, and `texas_2024.csv` are beside it. The prepared inventory has 137 records, all 37 confirmed 2024 election dates, and `partisan_status`/`partisan_party` tags; the 12 hypothetical 2020 matchups are in a separate exclusion audit. If your kernel works from the repository root, omit `../`. Review populations, flags, and multiple questions per poll before choosing a historical modeling sample. See [prepared files and classification limits](../data/processed/texas_senate_historical/README.md) and [original sources](../data/raw/texas_senate_historical/README.md); the inventory has no election results or error-model implementation.

## Prepared calibration crosswalk

Use [the national prepared README](../data/processed/senate_calibration/README.md) for copyable loading examples and [the dictionary](../docs/data_dictionary.md#prepared-national-calibration-inputs-decisions-012014) for join keys. `poll_questions.csv` identifies selected questions, `poll_candidate_rows.csv` retains every answer, and `candidate_results.csv` retains every ballot line with side and valid-vote fields. Join by exact `contest_id`; keep unknowns/pending cases out until reviewed. Georgia 2021 returns map to cycle 2020; Mississippi first-round polls remain pending rather than matched to runoff votes.

Rahan wrote the margin functions and calibration loop; they now live in `src/model/polling_average.py` and `src/evaluate/calibration.py`.
