"""Export audited side sums from prepared v1 inputs; no margins or model logic.

One result row per contest/round; one poll row per selected question. Unknown
votes stay in an explicit column, and all pending/excluded contests stay visible.
"""
import argparse
import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

import prepare_senate_calibration as prepared

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1"


def prepare(snapshot, output):
    if output.exists():
        raise ValueError("Existing outputs are never overwritten")
    parent = json.loads((snapshot / "manifest.json").read_text())
    if parent.get("rule_version") != "Decisions 011–014 / calibration-preparation-v1":
        raise ValueError("Unsupported prepared schema/rule version")
    hashes = {"manifest.json": prepared.sha(snapshot / "manifest.json")}
    for name, receipt in parent["outputs"].items():
        if Path(name).name != name or prepared.sha(snapshot / name) != receipt["sha256"]:
            raise ValueError(f"Parent output hash mismatch: {name}")
        hashes[name] = receipt["sha256"]
    contests = prepared.read_csv(snapshot / "contests.csv")
    returns = prepared.read_csv(snapshot / "candidate_results.csv")
    questions = prepared.read_csv(snapshot / "poll_questions.csv")
    candidates = prepared.read_csv(snapshot / "poll_candidate_rows.csv")
    result_groups, poll_groups = defaultdict(list), defaultdict(list)
    for r in returns:
        result_groups[r["contest_id"]].append(r)
    for r in candidates:
        poll_groups[r["question_key"]].append(r)
    result_rows, poll_rows = [], []
    for c in contests:
        rows = result_groups[c["contest_id"]]
        sums = dict.fromkeys(("D", "R", "other", "unknown"), 0)
        pending_valid = False
        for r in rows:
            if r["valid_vote"] == "pending":
                pending_valid = True
            elif r["valid_vote"] == "true":
                if r["side"] not in sums:
                    raise ValueError("Unrecognized result side")
                sums[r["side"]] += prepared.integer(r["votes"])
            elif r["valid_vote"] != "false":
                raise ValueError("Unrecognized valid-vote classification")
        if c["valid_vote_total"] and sum(sums.values()) != prepared.integer(c["valid_vote_total"]):
            raise ValueError(f"Side sums differ from parent valid-vote total: {c['contest_id']}")
        # Blank, rather than invented zero counts, for a contest lacking returns.
        result_rows.append({**c, "dem_votes": sums["D"] if rows else "",
                            "rep_votes": sums["R"] if rows else "",
                            "other_votes": sums["other"] if rows else "",
                            "unknown_votes": sums["unknown"] if rows else "",
                            "side_counts_complete": str(bool(rows) and not pending_valid and not any(r["side"] == "unknown" and r["valid_vote"] == "true" for r in rows)).lower(),
                            "source_record_keys_json": json.dumps([r["record_key"] for r in rows])})
    for q in questions:
        if q["status"] != "selected":
            continue
        rows = poll_groups[q["question_key"]]
        if not rows or {r["side"] for r in rows}.difference({"D", "R", "other"}) or not {"D", "R"}.issubset({r["side"] for r in rows}):
            raise ValueError("Selected question lacks complete known D/R mapping")
        sums = dict.fromkeys(("D", "R", "other"), Decimal(0))
        for r in rows:
            if r["question_status"] != "selected":
                raise ValueError("Candidate/question selection mismatch")
            pct = Decimal(r["pct"])
            if not pct.is_finite() or not 0 <= pct <= 100:
                raise ValueError("Invalid selected candidate percentage")
            sums[r["side"]] += pct
        poll_rows.append({**q, "dem_pct": str(sums["D"]), "rep_pct": str(sums["R"]),
                          "other_pct": str(sums["other"]),
                          "source_record_keys_json": json.dumps([r["record_key"] for r in rows])})
    if len({r["contest_id"] for r in result_rows}) != len(result_rows) or len({r["question_key"] for r in poll_rows}) != len(poll_rows):
        raise ValueError("Duplicate wide-table join key")
    output.mkdir(parents=True, exist_ok=False)
    tables = {"results_wide.csv": result_rows, "polls_wide.csv": poll_rows}
    for name, rows in tables.items():
        prepared.write_csv(output / name, rows)
    try:
        parent_path = str(snapshot.relative_to(ROOT))
    except ValueError:
        parent_path = str(snapshot)
    manifest = {"schema_version": 1, "rule_version": "Decision 017 / mechanical wide export v1",
                "parent_snapshot": parent_path, "parent_files_sha256": hashes,
                "authorization": "Decision 017 / Rahan approved 2026-10-08",
                "outputs": {name: {"rows": len(rows), "sha256": prepared.sha(output / name)} for name, rows in tables.items()},
                "transformations": ["Sum existing valid result votes by approved side within each contest/round; retain unknown votes separately", "Sum reported candidate percentages by approved side within each selected question; retain original question metadata", "Preserve all contest statuses; do not include pending/excluded questions in the poll working table"],
                "limitations": ["Existing v1 sample only; new 2022/2024 polling unavailable at creation", "Result eligibility and pending reasons must still be respected", "Other percentage sums reported other-candidate answers only, not undecided or an inferred complement", "Incomplete side counts are explicit; missing returns stay blank", "No margins, shares from votes, recency weights, averages, errors, uncertainty or probability calculations"]}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    for name, checksum in hashes.items():
        if prepared.sha(snapshot / name) != checksum:
            raise ValueError("Parent input changed during export")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, default=SNAPSHOT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.snapshot, args.output)["outputs"], indent=2))


if __name__ == "__main__":
    main()
