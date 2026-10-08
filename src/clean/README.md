# Mechanical cleaning

Mechanical formatting and cleaning code that applies approved rules to saved raw snapshots. All scripts use the Python standard library, run offline, verify input hashes, and never overwrite existing outputs. None implements core modeling logic.

| Script | Output |
| --- | --- |
| `prepare_texas_history.py` | [Prepared historical Texas Senate polling](../../data/processed/texas_senate_historical/README.md) (Decision 011) |
| `prepare_senate_calibration.py` | [Prepared Senate calibration inputs](../../data/processed/senate_calibration/README.md) (Decisions 012–014) |
| `prepare_calibration_wide.py` | Wide working tables from the prepared v1 calibration inputs |
| [`calibration_references/`](calibration_references/README.md) | Reviewed factual JSON used by `prepare_senate_calibration.py` |

## Historical Texas Senate preparation

`prepare_texas_history.py` applies Decision 011 to the saved historical Texas Senate inventory. It sets all 2024 election dates to `2024-11-05`, adds source-based partisan tags, and excludes clearly identified 2020 challengers other than M.J. Hegar against Cornyn. Missing or ambiguous candidate names stay available for review. It preserves raw snapshots and outputs retained records, exclusions, a change audit, and provenance hashes.

From the repository root:

```bash
python src/clean/prepare_texas_history.py
```

Default input: `data/raw/texas_senate_historical/20261006T024116Z/`. Default output: `data/processed/texas_senate_historical/20261006T024116Z/`. Because the default output exists, replay into a fresh location:

```bash
python src/clean/prepare_texas_history.py --output-root outputs/history_preparation_replay
```

`--snapshot PATH` accepts another saved inventory with the original schema. The script verifies original source hashes and records input/output hashes. CSVs are deterministic; the manifest records the current processing time. Partisanship follows source flags, with unknown metadata preserved. There is no partisan/population exclusion, deduplication, weighting, or uncertainty model. See [outputs and limitations](../../data/processed/texas_senate_historical/README.md).

## National Senate calibration preparation

`prepare_senate_calibration.py` applies Decisions 012–014 to the saved all-state 2018/2020 archive, MEDSL results and prepared Texas 2024 tracker. It creates contest/date/round mappings, explicit candidate sides, integral votes and valid-vote categories; applies the approved LV/partisan/non-ballot filters and the unique full-ballot preference; and keeps ambiguous cases as pending.

```bash
python3 -B src/clean/prepare_senate_calibration.py --output outputs/calibration_replay
```

Default inputs are the 20261006T024116Z historical polls, the 20261006T035630Z results and the prepared Texas inventory. The default output is the saved `data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1/`; use a fresh `--output` for replay. `--created-at` allows a byte-identical manifest replay. [The processed README](../../data/processed/senate_calibration/README.md) documents all 12 outputs, loading and limits; [the reference README](calibration_references/README.md) documents the explicit JSON and factual extraction workflow; [the review](../../docs/calibration_preparation_review.md) lists pending source issues.

## Wide working tables

`prepare_calibration_wide.py` exports one result row per contest/round and one poll row per selected question from the prepared v1 snapshot. It sums existing side-classified votes and percentages mechanically, keeps unknown vote counts and all result statuses, and computes no margins or model quantities. Parent output hashes are verified.

```bash
python3 -B src/clean/prepare_calibration_wide.py --output outputs/calibration_wide_replay
```

The default parent is the original v1 prepared snapshot; `--snapshot PATH` must use its supported schema/rule version. Saved wide files are in `data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1_wide/`. See [fields, loading and limits](../../data/processed/senate_calibration/README.md). These tables cover the existing 2018/2020/Texas 2024 inputs; expanded 2022/2024 preparation is blocked on polling retrieval.
