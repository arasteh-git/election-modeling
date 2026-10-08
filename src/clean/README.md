# Mechanical cleaning

## Wide working tables from prepared v1 inputs

`prepare_calibration_wide.py` exports one result row per contest/round and one poll row per selected question. It sums existing side-classified votes/percentages mechanically, retains unknown vote counts and all result statuses, and computes no margins or model quantities. Parent output hashes are verified; existing outputs are never overwritten.

```bash
python3 -B src/clean/prepare_calibration_wide.py --output outputs/calibration_wide_replay
```

Default parent is the original v1 prepared snapshot; `--snapshot PATH` must use its supported schema/rule version. Saved wide files are in `data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1_wide/`. See [fields, loading and limits](../../data/processed/senate_calibration/README.md). These are the existing 2018/2020/Texas 2024 inputs; expanded 2022/2024 preparation remains blocked on polling retrieval.

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

## National Senate calibration preparation

`prepare_senate_calibration.py` applies Decisions 012–014 to the saved all-state 2018/2020 archive, MEDSL results and prepared Texas 2024 tracker. It creates contest/date/round mappings, explicit candidate sides, integral votes and valid-vote categories; applies approved LV/partisan/non-ballot filters and the unique full-ballot preference; retains ambiguous cases as pending. No core modeling logic is implemented.

```bash
python3 -B src/clean/prepare_senate_calibration.py --output outputs/calibration_replay
```

Default inputs are the 20261006T024116Z historical polls, 20261006T035630Z results and existing prepared Texas inventory. Default output is the saved `data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1/`; use a fresh `--output` for replay. Inputs are hash-checked and existing outputs cannot be overwritten. `--created-at` allows byte-identical manifest replay. [The processed README](../../data/processed/senate_calibration/README.md) documents all 12 outputs, loading and limits; [the reference README](calibration_references/README.md) documents the explicit JSON and factual extraction workflow. [The review](../../docs/calibration_preparation_review.md) lists pending source issues.
