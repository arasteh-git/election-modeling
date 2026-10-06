# Notebooks

Rahan's exploration and learning work.

- data-pulls.ipynb: Rahan's Jupyter notebook installs/imports matplotlib, plotnine, pandas, and NumPy, loads the 2026 Texas snapshot, filters LV polls, computes D minus R margins, and calculates a recency-weighted average and effective poll count. Saved output reflects an earlier run, not verification of today's environment.
- .gitkeep: empty directory marker.

Use [the file guide](../docs/file_guide.md) and [data dictionary](../docs/data_dictionary.md) when exploring the Texas CSVs. Paths depend on the notebook's working directory; from notebooks/, the snapshot is under ../data/raw/texas_tracker/.

## Historical inventory

From a kernel working in `notebooks/`, load the prepared historical data (Decision 011) with:

```python
history = pd.read_csv('../data/processed/texas_senate_historical/20261006T024116Z/normalized.csv')
```

Per-cycle files `texas_2018.csv`, `texas_2020.csv`, and `texas_2024.csv` are beside it. The prepared inventory has 137 records, all 37 confirmed 2024 election dates, and `partisan_status`/`partisan_party` tags; the 12 hypothetical 2020 matchups are in a separate exclusion audit. If your kernel works from the repository root, omit `../`. Review populations, flags, and multiple questions per poll before choosing a historical modeling sample. See [prepared files and classification limits](../data/processed/texas_senate_historical/README.md) and [original sources](../data/raw/texas_senate_historical/README.md); the inventory has no election results or error-model implementation.
