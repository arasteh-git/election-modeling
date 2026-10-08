"""Offline collector checks using explicitly synthetic archive fixtures."""
import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src/ingest"))
import senate_poll_archives as archive


def fixtures():
    checks = json.loads((ROOT / "docs/polling_source_checks_2022_2024.json").read_text())["receipts"]
    bodies = {"publisher_README.md": b"Synthetic fixture: CC BY 4.0\n",
              "publisher_polls_README.md": b"Synthetic publisher documentation fixture\n"}
    for y, schema in (("2022", "archive_2023_header"), ("2024", "archive_january_header")):
        fields = checks[schema]["header"]
        rows = []
        for cycle, race, question in ((y, "1", "100"), ("2018", "2", "200")):
            for candidate, party in (("Fixture Democrat", "DEM"), ("Fixture Republican", "REP")):
                r = dict.fromkeys(fields, "")
                r.update(cycle=cycle, race_id=race, question_id=question, poll_id="10", state="Georgia", stage="general", seat_name="Class III", seat_number="1", candidate_id=party, candidate_name=candidate, answer=candidate, party=party, pct="40", start_date="11/1/22", end_date="11/2/22", election_date="11/8/22", population="lv", sample_size="500", internal="false", partisan="", ranked_choice_reallocated="false")
                rows.append(r)
        bodies[f"senate_polls_{y}_source.csv"] = archive.results.encoded_csv(rows, fields)
    return bodies


class SenateArchives(unittest.TestCase):
    def test_designated_cycles_and_all_source_fields_preserved(self):
        bodies = fixtures()
        candidates, questions, races, summary = archive.inventory(bodies)
        self.assertEqual(len(candidates), 4)
        self.assertEqual(len(questions), 2)
        self.assertEqual(len(races), 2)
        for y in archive.CAPTURES:
            rows = list(csv.DictReader(io.StringIO(bodies[f"senate_polls_{y}_source.csv"].decode())))[:2]
            prepared = [r for r in candidates if r["cycle"] == y]
            self.assertEqual(rows, [{k: r[k] for k in rows[0]} for r in prepared])
            self.assertEqual(summary["designated_cycle_counts"][y]["questions"], 1)
            self.assertEqual(summary["full_source_rows_by_cycle"][f"senate_polls_{y}_source.csv"]["2018"], 2)

    def test_bad_schema_rejected_and_ambiguous_answers_retained(self):
        bodies = fixtures()
        bad = dict(bodies)
        bad["senate_polls_2022_source.csv"] = b"<html>not csv</html>"
        with self.assertRaisesRegex(ValueError, "schema"):
            archive.inventory(bad)
        original = bodies["senate_polls_2022_source.csv"]
        reader = csv.DictReader(io.StringIO(original.decode()));rows=list(reader)
        rows[1]["candidate_id"] = rows[0]["candidate_id"]
        rows[1]["pct"] = "NaN"
        bodies["senate_polls_2022_source.csv"] = archive.results.encoded_csv(rows, reader.fieldnames)
        candidates, questions, _, _ = archive.inventory(bodies)
        self.assertEqual(len(candidates), 4)
        self.assertIn("duplicate_candidate_answer", questions[0]["flags"])
        self.assertIn("invalid_candidate_percentage", questions[0]["flags"])
        self.assertEqual(candidates[1]["pct"], "NaN")

    def test_byte_identical_replay_overwrite_and_tampering(self):
        bodies = fixtures()
        def fake_fetch(url):
            name = next(n for n, u in archive.SOURCE_URLS.items() if u == url)
            b = bodies[name]
            return b, {"url": url, "resolved_url": url, "status": 200, "content_type": "text/csv" if name.endswith(".csv") else "text/plain", "retrieved_at": "2026-10-08T12:00:00+00:00", "bytes": len(b), "sha256": archive.results.digest(b)}
        with tempfile.TemporaryDirectory() as d:
            with patch.object(archive, "fetch", side_effect=fake_fetch):
                target, manifest = archive.collect(Path(d)/"first")
            with patch.object(archive, "fetch", side_effect=AssertionError("Offline replay must not use network")):
                replay, _ = archive.collect(Path(d)/"replay", snapshot=target)
            self.assertEqual({p.name:p.read_bytes() for p in target.iterdir()}, {p.name:p.read_bytes() for p in replay.iterdir()})
            with self.assertRaises(FileExistsError):
                archive.collect(Path(d)/"first", snapshot=target)
            self.assertEqual(manifest["summary"]["results_2022"]["candidate_rows"], 168)
            (target/"senate_polls_2022_source.csv").write_bytes(b"tampered")
            with self.assertRaisesRegex(ValueError, "receipt mismatch"):
                archive.collect(Path(d)/"bad", snapshot=target)
            self.assertFalse((Path(d)/"bad").exists())

    def test_network_failure_creates_no_snapshot(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d)/"failed"
            with patch.object(archive, "fetch", side_effect=archive.URLError("fixture network failure")):
                with self.assertRaises(archive.URLError):
                    archive.collect(output)
            self.assertFalse(output.exists())

    def test_html_wrong_capture_and_license_fail_closed(self):
        bodies=fixtures()
        for failure in ("html", "capture", "license"):
            def fake_fetch(url):
                name=next(n for n,u in archive.SOURCE_URLS.items() if u==url)
                b=bodies[name]
                if failure=="license" and name=="publisher_README.md":b=b"No license"
                return b,{"url":url,"resolved_url":url+"?other" if failure=="capture" else url,"status":200,"content_type":"text/html" if failure=="html" else "text/csv","retrieved_at":"2026-10-08T12:00:00+00:00","bytes":len(b),"sha256":archive.results.digest(b)}
            with tempfile.TemporaryDirectory() as d,patch.object(archive,"fetch",side_effect=fake_fetch):
                output=Path(d)/"failed"
                with self.assertRaises(ValueError):archive.collect(output)
                self.assertFalse(output.exists())

    def test_2022_results_fields_rounds_and_replay(self):
        body = (archive.RESULT_SNAPSHOT/"senate_returns.csv").read_bytes()
        raw = list(csv.DictReader(io.StringIO(body.decode("utf-8-sig"))))
        with tempfile.TemporaryDirectory() as d:
            first, second = Path(d)/"first", Path(d)/"second"
            manifest = archive.inventory_results_2022(first)
            archive.inventory_results_2022(second)
            self.assertEqual({p.name:p.read_bytes() for p in first.iterdir()}, {p.name:p.read_bytes() for p in second.iterdir()})
            with (first/"returns_2022.csv").open(newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows),168)
            self.assertEqual({r["year"] for r in rows},{"2022"})
            for r in rows:self.assertEqual({k:r[k] for k in raw[0]},raw[int(r["source_row"])-1])
            self.assertEqual({r["stage"] for r in rows if r["state_po"]=="GA"},{"GEN","GEN RUNOFF"})
            self.assertEqual(manifest["summary"]["inventory_groups"],36)
            with self.assertRaisesRegex(ValueError,"never overwritten"):archive.inventory_results_2022(first)


if __name__ == "__main__":
    unittest.main()
