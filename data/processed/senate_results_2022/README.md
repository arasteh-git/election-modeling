# 2022 MEDSL results inventory

Decision 017 extends MEDSL V8.0 approval to 2022. `20261006T035630Z_decision017_v1/` mechanically inventories the existing immutable original source; its name references the original retrieval, not a new network collection time.

| File | Purpose |
| --- | --- |
| `returns_2022.csv` | All 168 original 2022 source rows/strings, source-row IDs, inventory-group IDs and flags. No candidate sides or election dates inferred. |
| `coverage.csv` | 36 source groups in 33 states, separating stage/special/mode; exact row-sum versus repeated-total checks. All differences are zero. |
| `issues.json` | Retained source flags and row IDs. Includes two unofficial Missouri rows, missing simplified parties and repeated ballot-line names. |
| `manifest.json` | Existing-source path, original retrieval receipt/SHA-256, V8.0/CC0 attribution, Decision 017, counts, transformations, output hashes and limits. |

Read with pandas `dtype=str, keep_default_na=False` to preserve original strings and empty fields. Georgia `GEN` and `GEN RUNOFF` remain separate. Missing detailed parties occur on 13 source rows in AK/HI/IL/IA/NV/NH/NC; blank fields are retained. The inherited audit flags simplified-party gaps separately; detailed-party and first-choice verification still need preparation/review. No counts have been corrected, no denominator/side rule chosen and no margins calculated.

Replay offline to a fresh output directory:

```bash
python3 -B src/ingest/senate_poll_archives.py --results-only outputs/results_2022_replay
```

The collector verifies the existing original SHA-256 and license/version. Generated files are deterministic, and existing outputs are never overwritten. The full original remains in [the original MEDSL snapshot](../../raw/senate_results/README.md); original candidate strings and ballot lines remain available for audit. This inventory alone cannot extend the notebook calibration: new polling and verified preparation are still required.
