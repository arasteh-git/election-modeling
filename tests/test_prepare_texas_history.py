"""Regression checks for Rahan's historical-data corrections (standard library)."""
import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src/clean/prepare_texas_history.py"
SNAPSHOT = ROOT / "data/raw/texas_senate_historical/20261006T024116Z"
spec = importlib.util.spec_from_file_location("prepare_texas_history", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class HistoricalPreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (SNAPSHOT / "normalized.csv").open(newline="", encoding="utf-8") as stream:
            cls.rows = list(csv.DictReader(stream))
        cls.retained, cls.excluded, cls.audit = module.prepare(cls.rows)

    def test_exact_exclusions_and_retained_values(self):
        expected_ids = {
            "125294", "125287", "125288", "124960", "122511", "114141",
            "114142", "114144", "114145", "100819", "100817", "100814",
        }
        self.assertEqual({r["question_id"] for r in self.excluded}, expected_ids)
        self.assertEqual(len(self.excluded), 12)
        self.assertEqual(Counter(r["cycle"] for r in self.retained), {"2018": 49, "2020": 51, "2024": 37})
        originals = {(r["source"], r["source_rows"]): r for r in self.rows}
        for row in self.retained + self.excluded:
            original = originals[(row["source"], row["source_rows"])]
            for field, value in original.items():
                expected = "2024-11-05" if field == "election_date" and row["cycle"] == "2024" else value
                self.assertEqual(row[field], expected, (row["source_rows"], field))
        self.assertEqual(len(self.audit), 149)
        self.assertEqual(sum(r["election_date_before"] != r["election_date_after"] for r in self.audit), 37)

    def test_partisanship_counts_and_unknowns(self):
        older = [r for r in self.retained if r["cycle"] in {"2018", "2020"}]
        self.assertEqual(Counter(r["partisan_status"] for r in older), {"partisan": 24, "not_flagged_partisan": 76})
        self.assertEqual(Counter(r["partisan_party"] for r in older if r["partisan_status"] == "partisan"), {"DEM": 17, "REP": 7})
        self.assertTrue(all(r["partisan_status"] == "unknown" for r in self.retained if r["cycle"] == "2024"))
        blank = {"source": "538_archive", "cycle": "2020", "partisan": "", "internal": ""}
        self.assertEqual(module.classify_partisanship(blank)[0], "unknown")
        self.assertEqual(module.classify_partisanship({**blank, "internal": "true"})[:2], ("partisan", ""))
        self.assertEqual(module.classify_partisanship({**blank, "internal": "false"})[0], "not_flagged_partisan")
        self.assertEqual(module.classify_partisanship({**blank, "partisan": "unexpected"})[0], "unknown")

    def test_missing_candidates_are_not_silently_excluded(self):
        row = dict(next(r for r in self.rows if r["cycle"] == "2020"))
        row["dem_candidate"] = ""
        retained, excluded, _ = module.prepare([row])
        self.assertEqual(len(retained), 1)
        self.assertEqual(excluded, [])

    def test_conflicting_election_date_requires_review(self):
        row = dict(next(r for r in self.rows if r["cycle"] == "2024"))
        row["election_date"] = "2024-11-06"
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            module.prepare([row])

    def test_cli_provenance_and_overwrite_protection(self):
        before = {p.name: module.sha256(p) for p in SNAPSHOT.iterdir() if p.is_file()}
        with tempfile.TemporaryDirectory() as root:
            command = [sys.executable, "-B", str(SCRIPT), "--snapshot", str(SNAPSHOT), "--output-root", root]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            summary = json.loads(result.stdout)
            self.assertEqual((summary["retained"], summary["excluded"]), (137, 12))
            folder = Path(summary["folder"])
            manifest = json.loads((folder / "manifest.json").read_text())
            self.assertEqual(manifest["input_sha256"]["normalized.csv"], before["normalized.csv"])
            for name, digest in manifest["output_sha256"].items():
                self.assertEqual(module.sha256(folder / name), digest)
            retry = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(retry.returncode, 0)
            self.assertIn("FileExistsError", retry.stderr)
        self.assertEqual(before, {p.name: module.sha256(p) for p in SNAPSHOT.iterdir() if p.is_file()})


if __name__ == "__main__":
    unittest.main()
