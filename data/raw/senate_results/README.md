# MEDSL Senate election results

Rahan approved MEDSL U.S. Senate statewide returns V8.0 for 2018, 2020, and 2024 (Decision 014). Attribution: MIT Election Data and Science Lab, [U.S. Senate statewide 1976–2024](https://doi.org/10.7910/DVN/PEJ5QU), Harvard Dataverse, version 8.0, [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Saved metadata records the license and exact public file IDs.

## Collect and replay

From the repository root, using the Python standard library:

```bash
python src/ingest/senate_results.py
python src/ingest/senate_results.py --snapshot data/raw/senate_results/20261006T035630Z --output-root outputs/senate_results_replay
```

Collection downloads the explicitly pinned V8.0 metadata and its unrestricted original CSV, codebook, and source listing. Each run creates a UTC-stamped snapshot; existing folders are never overwritten. Replay verifies source hashes, recomputes the audit, and reproduces all 12 snapshot files byte-for-byte, including original receipts. Choose a fresh output root for repeated replays. Replay uses no network.

## Snapshot files

| File | Purpose |
| --- | --- |
| `senate_returns.csv` | Unchanged full original CSV, including years outside the requested scope. |
| `metadata.json` | Unchanged public V8.0 dataset response, file metadata and CC0 license. |
| `codebook.md` | Unchanged publisher codebook; its body describes older coverage. |
| `sources.csv` | Unchanged publisher source listing, apparently focused on 2020; not certification evidence for every record. |
| `candidate_rows.csv` | All 2018/2020/2024 rows plus four separately labeled Georgia 2021 runoff rows for review. All 19 source fields and their strings preserved, including ballot lines, write-ins, blank names, and noncandidate categories. |
| `returns_2018.csv`, `returns_2020.csv`, `returns_2024.csv` | Per-source-year subsets; no candidate exclusions or percentages calculated. |
| `returns_2021.csv` | Supplemental Georgia runoffs only; year remains 2021 and cycle is unassigned. |
| `coverage.csv` | Snapshot-local groups by year/state/office/district/stage/special/mode, names, totals, integer vote-sum checks, and unresolved flags. Not a reviewed contest registry. |
| `issues.json` | Summary and exact source-row IDs for flags. Group-wide date/round warnings are in coverage. |
| `manifest.json` | URLs, per-file UTC retrieval times, sizes, SHA-256, approval, license, transformations, output hashes, counts and limitations. |

## First snapshot

`20261006T035630Z/`: retrieved October 5, 2026 in New York (October 6 UTC). Full CSV: 3,945 rows; SHA-256 `6f745db1b4a0026ad837e74428f9ed6f3f77fa51eb6f858b58ebdbc186fdb3bd`.

| Source year | Inventoried rows | Source groups |
| --- | ---: | ---: |
| 2018 | 152 | 35 |
| 2020 | 204 | 35 |
| 2024 | 148 | 35 |
| 2021 Georgia runoff supplement | 4 | 2 |
| Total | 508 | 107 |

Every source-row vote sum matches the group's reported total. This arithmetic check does not establish certification, a valid-candidate-vote denominator, or round matching. Retained flags include 19 unofficial rows, 30 blank names, six noncandidate categories, and 11 repeated-name rows in three groups. Publisher tabular MD5 is not compared with original CSV; original sizes and codebook MD5 are checked, with SHA-256 recorded for every file.

## Notebook loading

From a kernel working in `notebooks/`:

```python
returns = pd.read_csv('../data/raw/senate_results/20261006T035630Z/returns_2024.csv')
texas_returns = returns[returns['state_po'] == 'TX']
```

Pandas may infer types and read empty fields as NaN. Use `dtype=str, keep_default_na=False` to preserve strings. `source_row` is a 1-based data-row position in this full CSV; retain the snapshot path with it. Result names are not yet mapped to polling names or Democratic/Republican sides.

## Limits before calibration

The CSV has no election dates. Stage labels do not establish the actual round; Mississippi 2018 special needs round/first-round coverage review. Unofficial flags and RCV first-choice definitions need official crosschecks. Repeated names may be ballot lines and are not combined. Vote sums include noncandidate categories; no denominator is chosen.

Decision 012's initial polling sample remains all 2018/2020 races plus Texas 2024. See [the review](../../../docs/senate_results_review.md) and [dictionary](../../../docs/data_dictionary.md). National poll preparation, crosswalks, analytical eligibility, margins, uncertainty, and probabilities remain unimplemented.
