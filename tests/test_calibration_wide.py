"""Check wide exports against audited long inputs, without any model quantities."""
import json
import shutil
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src/clean"))
import prepare_calibration_wide as wide


class CalibrationWide(unittest.TestCase):
    def test_keys_side_sums_and_unknown_preservation(self):
        with tempfile.TemporaryDirectory() as d:
            output=Path(d)/"wide"
            manifest=wide.prepare(wide.SNAPSHOT, output)
            results=wide.prepared.read_csv(output/"results_wide.csv")
            polls=wide.prepared.read_csv(output/"polls_wide.csv")
            self.assertEqual(len(results),108)
            self.assertEqual(len(polls),729)
            self.assertEqual(len({r["question_key"] for r in polls}),729)
            missing=next(r for r in results if r["contest_id"]=="2018-MS-special-first")
            self.assertEqual(missing["dem_votes"],"")
            self.assertEqual(missing["side_counts_complete"],"false")
            self.assertTrue(any(r["unknown_votes"] not in {"", "0"} and r["side_counts_complete"]=="false" for r in results))
            for r in results:
                if r["valid_vote_total"]:
                    self.assertEqual(sum(int(r[f]) for f in ("dem_votes","rep_votes","other_votes","unknown_votes")),int(r["valid_vote_total"]))
            long=wide.prepared.read_csv(wide.SNAPSHOT/"poll_candidate_rows.csv")
            bykey={}
            for r in long:
                if r["question_status"]=="selected":bykey.setdefault(r["question_key"],[]).append(r)
            for r in polls:
                self.assertEqual(r["status"],"selected")
                for side,col in (("D","dem_pct"),("R","rep_pct"),("other","other_pct")):
                    self.assertEqual(Decimal(r[col]),sum((Decimal(p["pct"]) for p in bykey[r["question_key"]] if p["side"]==side),Decimal(0)))
                self.assertFalse({"margin","error","sigma","probability"}.intersection(r))

    def test_replay_and_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/"a",Path(d)/"b"
            wide.prepare(wide.SNAPSHOT,a);wide.prepare(wide.SNAPSHOT,b)
            self.assertEqual({p.name:p.read_bytes() for p in a.iterdir()},{p.name:p.read_bytes() for p in b.iterdir()})
            with self.assertRaisesRegex(ValueError,"never overwritten"):wide.prepare(wide.SNAPSHOT,a)

    def test_tampering_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/"source";shutil.copytree(wide.SNAPSHOT,source)
            (source/"candidate_results.csv").write_bytes(b"tampered")
            with self.assertRaisesRegex(ValueError,"hash mismatch"):wide.prepare(source,Path(d)/"bad")
            self.assertFalse((Path(d)/"bad").exists())


if __name__=="__main__":unittest.main()
