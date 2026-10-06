"""Regression checks for approved mapping and preparation, not model logic."""
import csv
import importlib.util
import json
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("calibration", ROOT / "src/clean/prepare_senate_calibration.py")
calibration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calibration)


class CalibrationPreparation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temp.name) / "prepared"
        cls.notebook = calibration.sha(ROOT / "notebooks/data-pulls.ipynb")
        cls.manifest = calibration.prepare(output=cls.output, created_at="2026-10-06T12:00:00+00:00")
        cls.tables = {name: calibration.read_csv(cls.output / name) for name in cls.manifest["outputs"]}
        cls.results = cls.tables["candidate_results.csv"]
        cls.contests = {r["contest_id"]: r for r in cls.tables["contests.csv"]}

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_all_source_rows_and_fields_survive(self):
        source = calibration.read_csv(calibration.RESULT_SNAPSHOT / "candidate_rows.csv")
        self.assertEqual(len(source), 508)
        for raw, prepared in zip(source, self.results):
            self.assertEqual(raw, {k: prepared[k] for k in raw})
        archive = calibration.read_csv(calibration.POLL_SNAPSHOT / "senate_polls_historical.csv")
        prepared = self.tables["poll_candidate_rows.csv"][:len(archive)]
        self.assertEqual(len(archive), 4593)
        for raw, prepared_row in zip(archive, prepared):
            self.assertEqual(raw, {k: prepared_row[k] for k in raw})
        self.assertEqual(len(self.tables["candidate_side_map.csv"]), 5175)
        self.assertEqual(len(self.tables["poll_questions.csv"]), 1950)
        self.assertEqual(len(self.tables["race_crosswalk.csv"]), 72)
        self.assertEqual(calibration.sha(ROOT / "notebooks/data-pulls.ipynb"), self.notebook)
        for path, checksum in self.manifest["inputs_sha256"].items():
            self.assertEqual(calibration.sha(ROOT / path), checksum)

    def test_approved_sides_and_fusion_lines(self):
        def rows(cid, name):
            return [r for r in self.results if r["contest_id"] == cid and r["candidate"] == name]
        for cid, name, side in (
            ("2018-ME-ordinary-general", "ANGUS S. KING, JR.", "D"),
            ("2018-ME-ordinary-general", "ZAK RINGELSTEIN", "other"),
            ("2018-VT-ordinary-general", "BERNIE SANDERS", "D"),
            ("2020-WY-ordinary-general", "CYNTHIA M. LUMMIS", "R"),
            ("2020-WY-ordinary-general", "MERAV BEN DAVID", "D"),
            ("2020-AK-ordinary-general", "AL GROSS", "D")):
            self.assertEqual([r["side"] for r in rows(cid, name)], [side])
        for name, side in (("KIRSTEN E. GILLIBRAND", "D"), ("CHELE CHIAVACCI FARLEY", "R")):
            matches = rows("2018-NY-ordinary-general", name)
            self.assertGreater(len(matches), 1)
            self.assertEqual({r["side"] for r in matches}, {side})
            self.assertEqual(len({r["canonical_candidate_id"] for r in matches}), 1)
        wy = rows("2020-WY-ordinary-general", "MERAV BEN DAVID")[0]
        self.assertIn("blank_detailed_party", wy["preparation_flags"])
        self.assertEqual(wy["reference_check"], "state_confirms_medsl")
        self.assertEqual(wy["votes"], "72766")
        sanders = rows("2018-VT-ordinary-general", "BERNIE SANDERS")[0]
        self.assertEqual(sanders["fec_reference_votes"], "183649")
        self.assertEqual(sanders["reference_check"], "conflict")

    def test_exact_rounds_and_missing_results(self):
        ms = self.contests["2018-MS-special-runoff"]
        self.assertEqual(ms["election_date"], "2018-11-27")
        first = self.contests["2018-MS-special-first"]
        self.assertEqual(first["result_rows"], "0")
        self.assertEqual(first["status"], "pending")
        self.assertEqual(len(json.loads(first["ballot_candidate_ids_json"])), 4)
        crosswalk = {r["race_id"]: r for r in self.tables["race_crosswalk.csv"]}
        self.assertEqual(crosswalk["130"]["contest_id"], "2018-MS-special-first")
        self.assertEqual(crosswalk["6209"]["contest_id"], "2018-MS-special-runoff")
        self.assertEqual(crosswalk["8737"]["contest_id"], "2020-GA-ordinary-runoff")
        self.assertEqual(crosswalk["7781"]["contest_id"], "2020-GA-special-runoff")
        self.assertEqual(crosswalk["7780"]["contest_id"], "2020-GA-special-first")
        self.assertEqual(self.contests["2020-GA-special-runoff"]["election_date"], "2021-01-05")
        self.assertEqual(crosswalk["7787"]["contest_id"], "")
        self.assertEqual(crosswalk["7787"]["status"], "pending")
        self.assertNotIn("2020-LA-ordinary-runoff", self.contests)
        first_questions = [q for q in self.tables["poll_questions.csv"] if q["race_id"] == "130"]
        self.assertTrue(any(q["status"] == "pending" for q in first_questions))
        self.assertTrue(all(q["status"] != "selected" for q in first_questions))

    def test_valid_denominators_and_first_choice(self):
        for cid, invalid in (("2020-IA-ordinary-general", 28302), ("2020-ME-ordinary-general", 9122), ("2020-MA-ordinary-general", 93869), ("2020-WY-ordinary-general", 6566)):
            contest = self.contests[cid]
            self.assertEqual(int(contest["noncandidate_votes"]), invalid)
            self.assertEqual(int(contest["reported_total"]) - int(contest["valid_vote_total"]), invalid)
        self.assertEqual(self.contests["2020-ME-ordinary-general"]["valid_vote_total"], "819183")
        self.assertEqual(self.contests["2018-NV-ordinary-general"]["valid_vote_total"], "")
        self.assertIn("ballot_option_denominator_pending", self.contests["2018-NV-ordinary-general"]["reasons"])
        unknown = [r for r in self.results if r["side"] == "unknown" and r["valid_vote"] == "true"]
        self.assertTrue(any(r["candidate"] == "RICARDO TURULLOLS-BONILLA" for r in unknown))
        self.assertEqual(self.contests["2020-TX-ordinary-general"]["status"], "pending")
        self.assertEqual(self.contests["2018-CA-ordinary-general"]["status"], "excluded")
        self.assertEqual(self.contests["2020-AR-ordinary-general"]["status"], "excluded")
        rcv = [q for q in self.tables["poll_questions.csv"] if q["question_id"] == "85932"]
        self.assertEqual(len(rcv), 1)
        self.assertEqual(rcv[0]["status"], "excluded")
        self.assertIn("RCV_reallocated_question", rcv[0]["reasons"])

    def test_candidate_filters_and_unique_observation(self):
        questions = self.tables["poll_questions.csv"]
        selected = [q for q in questions if q["status"] == "selected"]
        keys = [(q["source"], q["poll_key"], q["contest_id"]) for q in selected]
        self.assertEqual(len(keys), len(set(keys)))
        for q in selected:
            self.assertEqual(q["population"], "LV")
            self.assertEqual(q["partisan_raw"], "")
            self.assertIn(q["internal_raw"].lower(), ("false", ""))
            self.assertEqual(self.contests[q["contest_id"]]["status"], "eligible")
        nonballot = [m for m in self.tables["candidate_side_map.csv"] if m["membership"] == "confirmed_nonballot"]
        self.assertTrue(any(m["candidate"] == "Doug Collins" and m["contest_id"].endswith("runoff") for m in nonballot))
        self.assertTrue(any(m["candidate"] == "Chris McDaniel" and m["contest_id"] == "2018-MS-special-runoff" for m in nonballot))
        tx_hypothetical = [q for q in questions if q["cycle"] == "2020" and q["state_po"] == "TX" and "confirmed_nonballot_candidate" in q["reasons"]]
        self.assertEqual(len(tx_hypothetical), 12)
        for q in questions:
            if q["partisan_raw"] in {"LIB", "REP,REF"}:
                self.assertEqual(q["status"], "excluded")
                self.assertIn("partisan_or_internal", q["reasons"])

    def test_preference_requires_unique_full_ballot(self):
        def q(key, full):
            return {"question_key": key, "source": "archive", "poll_key": "1", "contest_id": "c", "status": "eligible", "full_ballot": full, "reasons": ""}
        qs = [q("headtohead", "false"), q("full", "true")]
        calibration.choose_questions(qs)
        self.assertEqual([x["status"] for x in qs], ["excluded", "selected"])
        for full in ("true", "false"):
            qs = [q("a", full), q("b", full)]
            calibration.choose_questions(qs)
            self.assertEqual([x["status"] for x in qs], ["pending", "pending"])

    def test_replay_and_overwrite_protection(self):
        replay = Path(self.temp.name) / "replay"
        calibration.prepare(output=replay, created_at=self.manifest["created_at"])
        for path in self.output.iterdir():
            self.assertEqual(path.read_bytes(), (replay / path.name).read_bytes())
        with self.assertRaisesRegex(ValueError, "never overwritten"):
            calibration.prepare(output=self.output)

    def test_input_tampering_rejected(self):
        copy = Path(self.temp.name) / "tampered"
        shutil.copytree(calibration.RESULT_SNAPSHOT, copy)
        (copy / "candidate_rows.csv").write_bytes((copy / "candidate_rows.csv").read_bytes() + b"\n")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            calibration.prepare(results=copy, output=Path(self.temp.name) / "bad")
        self.assertFalse((Path(self.temp.name) / "bad").exists())

    def test_counts_reconcile_and_no_model_outputs(self):
        counts = self.manifest["counts"]
        self.assertEqual(sum(counts["question_status"].values()), 1950)
        self.assertEqual(sum(counts["contest_status"].values()), 108)
        for y, statuses in counts["by_cycle"].items():
            self.assertEqual(sum(statuses.values()), sum(q["cycle"] == y for q in self.tables["poll_questions.csv"]))
        for rows in self.tables.values():
            for row in rows:
                self.assertFalse({"margin", "average", "rmse", "sigma", "probability"}.intersection(row))


if __name__ == "__main__":
    unittest.main()
