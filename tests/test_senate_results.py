"""Provenance, row preservation, audit flags, and immutable offline replay."""
import csv
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("senate_results", ROOT / "src/ingest/senate_results.py")
results = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(results)
SNAPSHOT = ROOT / "data/raw/senate_results/20261006T035630Z"


class SenateResultsTests(unittest.TestCase):
    def setUp(self):
        self.bodies = {name: (SNAPSHOT / name).read_bytes() for name in results.SOURCE_URLS}

    def test_preserves_exact_source_fields_and_all_requested_rows(self):
        raw = list(csv.DictReader(io.StringIO(self.bodies["senate_returns.csv"].decode())))
        rows, groups, issues = results.audit(self.bodies["senate_returns.csv"])
        self.assertEqual(len(raw), 3945)
        self.assertEqual(issues["summary"]["inventoried_rows_by_source_year"],
                         {"2018": 152, "2020": 204, "2021": 4, "2024": 148})
        expected_ids = {i for i, r in enumerate(raw, 1) if r["year"] in {"2018", "2020", "2024"}
                        or (r["year"] == "2021" and r["state_po"] == "GA" and r["stage"] == "runoff")}
        self.assertEqual({r["source_row"] for r in rows}, expected_ids)
        for row in rows:
            self.assertEqual({f: row[f] for f in results.SOURCE_FIELDS}, raw[row["source_row"] - 1])
        self.assertEqual(sum(g["row_count"] for g in groups), len(rows))
        self.assertTrue(all(g["sum_minus_reported_total"] == 0 for g in groups))

    def test_keeps_year_round_and_special_groups_separate(self):
        rows, groups, _ = results.audit(self.bodies["senate_returns.csv"])
        ga = [g for g in groups if g["state_po"] == "GA" and g["year"] in {"2020", "2021"}]
        self.assertEqual(len(ga), 4)
        self.assertEqual(len({g["inventory_id"] for g in ga}), 4)
        self.assertEqual({(g["year"], g["stage"], g["special"]) for g in ga},
                         {("2020", "gen", "false"), ("2020", "gen", "true"),
                          ("2021", "runoff", "false"), ("2021", "runoff", "true")})
        for row in rows:
            if row["year"] == "2021":
                self.assertEqual(row["selection_basis"], "supplemental_GA_2021_runoff")
                self.assertIn("supplemental_2021_runoff_cycle_unassigned", row["flags"])
        ms = next(g for g in groups if g["year"] == "2018" and g["state_po"] == "MS" and g["special"] == "true")
        self.assertEqual(ms["stage"], "gen")
        self.assertIn("round_definition_unverified", ms["flags"])

    def test_flags_anomalies_without_dropping_or_imputing(self):
        rows, groups, issues = results.audit(self.bodies["senate_returns.csv"])
        self.assertEqual(issues["summary"]["row_flag_counts"]["unofficial_return"], 19)
        self.assertEqual(issues["summary"]["row_flag_counts"]["missing_candidate_name"], 30)
        self.assertEqual(issues["summary"]["row_flag_counts"]["noncandidate_vote_category"], 6)
        self.assertEqual(sum("repeated_candidate_name_review_ballot_lines" in g["flags"] for g in groups), 3)
        fixture = [{f: r[f] for f in results.SOURCE_FIELDS} for r in rows]
        fixture[0].update(candidatevotes="NaN", totalvotes="1", unofficial="", candidate="")
        broken, coverage, _ = results.audit(results.encoded_csv(fixture, results.SOURCE_FIELDS))
        self.assertEqual(len(broken), len(fixture))
        self.assertEqual(broken[0]["candidatevotes"], "NaN")
        for flag in ("invalid_candidatevotes", "possible_uncontested_sentinel", "unknown_unofficial", "missing_candidate_name"):
            self.assertIn(flag, broken[0]["flags"])
        group = next(g for g in coverage if g["inventory_id"] == broken[0]["inventory_id"])
        self.assertEqual(group["sum_source_row_votes"], "")
        self.assertIn("inconsistent_or_invalid_totalvotes", group["flags"])
        fixture[0] = {f: rows[0][f] for f in results.SOURCE_FIELDS}
        fixture[0]["candidatevotes"] = str(int(float(fixture[0]["candidatevotes"])) + 1)
        _, coverage, _ = results.audit(results.encoded_csv(fixture, results.SOURCE_FIELDS))
        self.assertTrue(any("source_row_sum_differs_from_total" in g["flags"] for g in coverage))

    def test_offline_replay_byte_identity_and_overwrite_rejection(self):
        original = {p.name: p.read_bytes() for p in SNAPSHOT.iterdir() if p.is_file()}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target, manifest = results.collect(root, SNAPSHOT)
            self.assertEqual({p.name: p.read_bytes() for p in target.iterdir()}, original)
            self.assertEqual(manifest["sources"], json.loads(original["manifest.json"])["sources"])
            with self.assertRaises(FileExistsError):
                results.collect(root, SNAPSHOT)
            self.assertEqual({p.name: p.read_bytes() for p in target.iterdir()}, original)
        self.assertEqual({p.name: p.read_bytes() for p in SNAPSHOT.iterdir() if p.is_file()}, original)

    def test_replay_rejects_tampering_before_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            shutil.copytree(SNAPSHOT, source)
            csv_path = source / "senate_returns.csv"
            csv_path.write_bytes(csv_path.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "receipt mismatch"):
                results.collect(root / "output", source)
            self.assertFalse((root / "output").exists())

    def test_rejects_schema_and_metadata_changes(self):
        with self.assertRaisesRegex(ValueError, "schema changed"):
            results.audit(b"<html>not a CSV</html>")
        results.validate_sources(self.bodies)
        for field, value in (("versionNumber", 9), ("datasetPersistentId", "doi:other"),
                             ("versionState", "DRAFT"), ("license", {"rightsIdentifier": "OTHER"})):
            metadata = json.loads(self.bodies["metadata.json"])
            metadata["data"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                results.validate_sources({**self.bodies, "metadata.json": results.encoded_json(metadata)})
        metadata = json.loads(self.bodies["metadata.json"])
        metadata["data"]["files"][0]["restricted"] = True
        with self.assertRaisesRegex(ValueError, "restricted"):
            results.validate_sources({**self.bodies, "metadata.json": results.encoded_json(metadata)})
        changed_codebook = b"X" + self.bodies["codebook.md"][1:]
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            results.validate_sources({**self.bodies, "codebook.md": changed_codebook})


if __name__ == "__main__":
    unittest.main()
