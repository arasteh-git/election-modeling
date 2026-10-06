# Prepared historical Texas Senate polling

Decision 011 applies Rahan's requested date correction, partisanship tagging, and hypothetical-matchup exclusion. Output folder `20261006T024116Z/` identifies the original source snapshot; processing time is separately recorded in the output manifest.

| Cycle | Retained records | Excluded | Source-tagged partisan | Not flagged partisan | Unknown |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2018 | 49 | 0 | 15 | 34 | 0 |
| 2020 | 51 | 12 | 9 | 42 | 0 |
| 2024 | 37 | 0 | 0 | 0 | 37 |

Records are questions or tracker rows, not necessarily independent surveys. All 37 2024 election dates are `2024-11-05`. All populations and all partisan polls remain present; the only exclusions are the 12 alternate 2020 Democratic challengers against Cornyn. Among retained partisan records, 2018 has 10 DEM and 5 REP flags; 2020 has 7 DEM and 2 REP flags.

## Files

- `normalized.csv`: all 137 retained records; use this for the updated historical inventory.
- `texas_2018.csv`, `texas_2020.csv`, `texas_2024.csv`: per-cycle subsets with the same schema.
- `excluded.csv`: the 12 removed hypothetical 2020 questions, retaining source keys, original fields, derived tags, and an exclusion reason.
- `changes.csv`: an audit of all 149 inputs, including election dates before/after, classification basis, original partisan/internal values, and kept/excluded action.
- `manifest.json`: source snapshot, original retrieval times/URLs and permissions, input/output hashes, approval/rule version, processing time, counts, and limits.

Original source data and the 149-row inventory remain unchanged in [the raw snapshot](../../raw/texas_senate_historical/README.md).

## Reproduce

From the repository root, standard library only and no network:

```bash
python src/clean/prepare_texas_history.py
```

The default source is `data/raw/texas_senate_historical/20261006T024116Z/`. The default output already exists after this change; the script refuses overwrite. To reproduce in a fresh location:

```bash
python src/clean/prepare_texas_history.py --output-root outputs/history_preparation_replay
```

`--snapshot PATH` selects another inventory snapshot with the original schema. Source hashes are checked before processing. Generated CSVs are deterministic; the new manifest's processing timestamp changes on rerun.

## Notebook use

From a kernel working in `notebooks/`:

```python
history = pd.read_csv('../data/processed/texas_senate_historical/20261006T024116Z/normalized.csv')
```

If the kernel works from the repository root, omit `../`. Use `partisan_status` for classification and `partisan_party` for the source's party tag. A blank original `partisan` field plus internal false becomes `not_flagged_partisan`; this does not independently establish that a poll is nonpartisan. The 2024 tracker provides no partisan/internal metadata, so those statuses remain `unknown`. Refer to [the data dictionary](../../../docs/data_dictionary.md) for the full schema.

## Limits

Existing malformed field dates, duplicate-question flags, source coverage differences, unverified publication dates, and primary-verification status remain visible. The malformed 2024 field interval still has blank fieldwork dates; filling election day does not resolve that interval. Primary reports and the archive mirror have not been independently verified. The processed inventory does not contain election results, averages, weights, or an uncertainty model.

Attribution and source permissions remain those in the original manifest: FiveThirtyEight / ABC News (preserved by khristel26/Senate) and the Texas Politics Project at the University of Texas at Austin. These CSVs are labeled derivatives; keep the source links and attribution with copies.
