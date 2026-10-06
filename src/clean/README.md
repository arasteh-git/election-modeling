# Mechanical cleaning

Mechanical formatting and cleaning code for approved rules belongs here.

`prepare_texas_history.py` implements Decision 011 using saved historical Texas Senate inputs. It sets all 2024 election dates to `2024-11-05`, adds source-based partisan tags, and excludes clearly identified 2020 challengers other than M.J. Hegar against Cornyn. Missing/ambiguous candidate names remain available for review. It preserves raw snapshots and outputs retained records, exclusions, a change audit, and provenance hashes.

From the repository root, standard library only, no network:

```bash
python src/clean/prepare_texas_history.py
```

Default input: `data/raw/texas_senate_historical/20261006T024116Z/`. Default output: `data/processed/texas_senate_historical/20261006T024116Z/`. Existing outputs are never overwritten. For a fresh replay after the default output exists:

```bash
python src/clean/prepare_texas_history.py --output-root outputs/history_preparation_replay
```

`--snapshot PATH` accepts another saved inventory with the original schema. The script verifies original source hashes and records input/output hashes. CSVs are deterministic, while the manifest records the current processing time. Partisanship follows source flags, with unknown metadata preserved; no partisan/population exclusion, deduplication, weighting, or uncertainty model is implemented. See [outputs and limitations](../../data/processed/texas_senate_historical/README.md).
