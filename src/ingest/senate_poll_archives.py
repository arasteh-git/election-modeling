"""Collect Decision 017's pinned Senate archives and mechanical coverage inventory.

Standard library only; raw source bytes and all designated-cycle answers retained.
No eligibility adjudication, imputation, margins, weights or model calculations.
"""
import argparse
import csv
import io
import json
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

import senate_results as results

ROOT = Path(__file__).resolve().parents[2]
RESULT_SNAPSHOT = ROOT / "data/raw/senate_results/20261006T035630Z"
MEDSL_SHA = "6f745db1b4a0026ad837e74428f9ed6f3f77fa51eb6f858b58ebdbc186fdb3bd"
CAPTURES = {"2022": "20230427025758", "2024": "20250118200335"}
ORIGINAL_URL = "https://projects.fivethirtyeight.com/polls-page/data/senate_polls_historical.csv"
SOURCE_URLS = {f"senate_polls_{y}_source.csv": f"https://web.archive.org/web/{stamp}id_/{ORIGINAL_URL}" for y, stamp in CAPTURES.items()}
SOURCE_URLS.update({
    "publisher_README.md": "https://raw.githubusercontent.com/fivethirtyeight/data/b366fada304fcf8068ba7789745fe15a61ed6e3d/README.md",
    "publisher_polls_README.md": "https://raw.githubusercontent.com/fivethirtyeight/data/b366fada304fcf8068ba7789745fe15a61ed6e3d/polls/README.md",
})
QUESTION_FIELDS = ["cycle", "state", "race_id", "poll_id", "question_id", "pollster", "pollster_id", "display_name", "sponsor_ids", "sponsors", "start_date", "end_date", "election_date", "sample_size", "population", "population_full", "subpopulation", "internal", "partisan", "stage", "seat_name", "seat_number", "ranked_choice_reallocated", "ranked_choice_round", "url"]
REQUIRED_FIELDS = set(QUESTION_FIELDS + ["candidate_id", "candidate_name", "party", "answer", "pct"])


def fetch(url):
    with urlopen(Request(url, headers={"User-Agent": "election-modeling/1.0 (approved public archive collection)"}), timeout=45) as r:
        body = r.read()
        if r.headers.get("Content-Length") and len(body) != int(r.headers["Content-Length"]):
            raise ValueError(f"Incomplete HTTP response: {url}")
        receipt = {"url": url, "resolved_url": r.url, "status": r.status,
                   "content_type": r.headers.get("Content-Type", ""),
                   "retrieved_at": datetime.now(timezone.utc).isoformat(),
                   "bytes": len(body), "sha256": results.digest(body)}
    return body, receipt


def inventory(bodies):
    candidates, questions, races = [], [], []
    full_counts = {}
    for cycle in CAPTURES:
        name = f"senate_polls_{cycle}_source.csv"
        reader = csv.DictReader(io.StringIO(bodies[name].decode("utf-8-sig")))
        fields = reader.fieldnames
        if not fields or len(fields) != len(set(fields)) or not REQUIRED_FIELDS.issubset(fields):
            raise ValueError(f"Unexpected archive CSV schema: {name}")
        groups, cycle_counts = defaultdict(list), Counter()
        for index, raw in enumerate(reader, 1):
            if None in raw or None in raw.values():
                raise ValueError(f"Malformed source row: {name}:{index}")
            cycle_counts[raw["cycle"]] += 1
            if raw["cycle"] != cycle:
                continue
            if any(not raw[k] for k in ("poll_id", "question_id", "race_id", "state")):
                raise ValueError(f"Missing inventory identifier: {name}:{index}")
            key = f"538-{cycle}-{CAPTURES[cycle]}:{raw['race_id']}:{raw['poll_id']}:{raw['question_id']}"
            row = {**raw, "archive_source": name, "source_row": index,
                   "source_snapshot": CAPTURES[cycle], "inventory_question_key": key}
            candidates.append(row)
            groups[key].append(row)
        if not groups:
            raise ValueError(f"No requested-cycle rows: {cycle}")
        full_counts[name] = dict(sorted(cycle_counts.items()))
        for key, rows in groups.items():
            raw = rows[0]
            flags = ["primary_verification_pending"]
            inconsistent = [f for f in QUESTION_FIELDS if len({r[f] for r in rows}) > 1]
            flags.extend("inconsistent_" + f for f in inconsistent)
            flags.extend("missing_" + f for f in ("end_date", "election_date", "sample_size", "population", "url") if not raw[f])
            if len({r["candidate_id"] for r in rows}) != len(rows):
                flags.append("duplicate_candidate_answer")
            if any(not r["candidate_id"] or not r["candidate_name"] for r in rows):
                flags.append("missing_candidate_identity")
            if any(not r["party"] for r in rows):
                flags.append("missing_candidate_party")
            if any(not r["pct"] for r in rows):
                flags.append("missing_candidate_percentage")
            for r in rows:
                if r["pct"]:
                    try:
                        pct = Decimal(r["pct"])
                        if not pct.is_finite() or not 0 <= pct <= 100:
                            raise InvalidOperation
                    except InvalidOperation:
                        flags.append("invalid_candidate_percentage")
            if raw["population"].lower() not in {"lv", "rv", "a", "v", ""}:
                flags.append("unrecognized_population")
            questions.append({"inventory_question_key": key, "archive_source": name,
                              "source_snapshot": CAPTURES[cycle], **{f: raw[f] for f in QUESTION_FIELDS},
                              "source_rows": ";".join(str(r["source_row"]) for r in rows),
                              "candidate_rows": len(rows), "candidate_answers_json": json.dumps([{f: r[f] for f in ("candidate_id", "candidate_name", "party", "answer", "pct")} for r in rows]),
                              "flags": ";".join(dict.fromkeys(flags))})
    race_groups = defaultdict(list)
    for q in questions:
        race_groups[(q["cycle"], q["race_id"])].append(q)
    for (cycle, race), qs in sorted(race_groups.items()):
        races.append({"cycle": cycle, "race_id": race,
                      **{f: json.dumps(sorted({q[f] for q in qs})) for f in ("state", "stage", "seat_name", "seat_number", "election_date")},
                      "questions": len(qs), "poll_ids": len({q["poll_id"] for q in qs}),
                      "candidate_rows": sum(q["candidate_rows"] for q in qs),
                      "LV_questions": sum(q["population"].lower() == "lv" for q in qs),
                      "round_mapping": "pending_exact_round_crosswalk"})
    summary = {"full_source_rows_by_cycle": full_counts, "designated_cycle_counts": {y: {
        "candidate_rows": sum(r["cycle"] == y for r in candidates),
        "questions": sum(q["cycle"] == y for q in questions),
        "poll_ids": len({q["poll_id"] for q in questions if q["cycle"] == y}),
        "states": len({q["state"] for q in questions if q["cycle"] == y}),
        "race_ids": sum(r["cycle"] == y for r in races),
        "questions_by_stage": dict(Counter(q["stage"] for q in questions if q["cycle"] == y)),
        "questions_by_population": dict(Counter(q["population"] for q in questions if q["cycle"] == y)),
        "question_flag_counts": dict(Counter(f for q in questions if q["cycle"] == y for f in q["flags"].split(";") if f)),
    } for y in CAPTURES}}
    return candidates, questions, races, summary


def collect(output_root, snapshot=None, result_snapshot=RESULT_SNAPSHOT):
    if snapshot:
        original = json.loads((snapshot / "manifest.json").read_text())
        if original.get("schema_version") != 1 or original.get("approval") != "Decision 017 / Rahan approved 2026-10-08":
            raise ValueError("Unsupported archive receipt")
        bodies = {n: (snapshot / n).read_bytes() for n in SOURCE_URLS}
        receipts = original["sources"]
        for name, body in bodies.items():
            r = receipts[name]
            if r["url"] != SOURCE_URLS[name] or r["sha256"] != results.digest(body) or r["bytes"] != len(body):
                raise ValueError(f"Source receipt mismatch: {name}")
        snapshot_id, retrieved_at = original["snapshot_id"], original["retrieved_at"]
    else:
        with ThreadPoolExecutor(max_workers=4) as pool:
            fetched = dict(zip(SOURCE_URLS, pool.map(fetch, SOURCE_URLS.values())))
        bodies = {n: pair[0] for n, pair in fetched.items()}
        receipts = {n: pair[1] for n, pair in fetched.items()}
        retrieved_at = max(r["retrieved_at"] for r in receipts.values())
        snapshot_id = datetime.fromisoformat(retrieved_at).strftime("%Y%m%dT%H%M%SZ")
    if Path(snapshot_id).name != snapshot_id or snapshot_id in {"", ".", ".."}:
        raise ValueError("Invalid snapshot ID")
    for y in CAPTURES:
        receipt = receipts[f"senate_polls_{y}_source.csv"]
        if receipt["status"] != 200 or "text/csv" not in receipt["content_type"]:
            raise ValueError("Archive response is not CSV")
        if receipt["resolved_url"] != SOURCE_URLS[f"senate_polls_{y}_source.csv"]:
            raise ValueError("Archive redirected away from the approved capture")
    if b"CC BY 4.0" not in bodies["publisher_README.md"]:
        raise ValueError("Publisher license notice missing")
    medsl_body = (result_snapshot / "senate_returns.csv").read_bytes()
    if results.digest(medsl_body) != MEDSL_SHA:
        raise ValueError("MEDSL source hash mismatch")
    medsl_manifest = json.loads((result_snapshot / "manifest.json").read_text())
    if medsl_manifest["dataset_version"] != "8.0" or medsl_manifest["license"]["rightsIdentifier"] != "CC0-1.0":
        raise ValueError("MEDSL version/license mismatch")
    candidates, questions, races, summary = inventory(bodies)
    result_rows, coverage, result_issues = results.audit(medsl_body, requested_years={"2022"})
    result_rows = [r for r in result_rows if r["year"] == "2022"]
    coverage = [r for r in coverage if r["year"] == "2022"]
    summary["results_2022"] = {"candidate_rows": len(result_rows), "source_groups": len(coverage)}
    tables = {"poll_candidate_rows.csv": candidates, "poll_questions.csv": questions, "race_inventory.csv": races,
              "results_2022.csv": result_rows, "results_2022_coverage.csv": coverage}
    outputs = {n: results.encoded_csv(rows, list(dict.fromkeys(k for r in rows for k in r))) for n, rows in tables.items()}
    outputs["issues.json"] = results.encoded_json({"summary": summary, "flagged_questions": [{"question_key": q["inventory_question_key"], "flags": q["flags"].split(";")} for q in questions],
                                                  "results_2022_flags": [r for r in result_issues["flagged_rows"] if r["source_row"] in {x["source_row"] for x in result_rows}]})
    manifest = {"schema_version": 1, "snapshot_id": snapshot_id, "retrieved_at": retrieved_at,
                "approval": "Decision 017 / Rahan approved 2026-10-08", "sources": receipts,
                "original_poll_url": ORIGINAL_URL, "designated_captures": CAPTURES,
                "license": "CC BY 4.0, publisher dataset policy unless otherwise specified",
                "license_url": "https://creativecommons.org/licenses/by/4.0/",
                "attribution": "FiveThirtyEight / ABC News; preserved by Internet Archive. Inventories are mechanical derivatives.",
                "results_provenance": medsl_manifest["sources"]["senate_returns.csv"],
                "results_license": medsl_manifest["license"], "summary": summary,
                "outputs": {n: {"sha256": results.digest(b), "bytes": len(b)} for n, b in outputs.items()},
                "transformations": ["Preserve complete original archive CSVs, including other cycles", "Inventory only designated-cycle rows; preserve original columns and strings", "Add source row/snapshot and question keys; flag missing/inconsistent metadata without removing answers", "Inventory unchanged 2022 MEDSL rows from the existing pinned original; preserve source group flags"],
                "limitations": ["Inventory is not an eligible calibration sample", "No primary releases, candidates, round mappings or RCV definitions comprehensively verified", "No poll inclusion, duplicate adjudication, candidate-side adjustment, imputation or model calculations", "Archive capture and database creation times are not historical release times"]}
    if snapshot and manifest != original:
        raise ValueError("Replay inventory/manifest differs")
    target = output_root / snapshot_id
    target.mkdir(parents=True, exist_ok=False)
    for n, b in {**bodies, **outputs, "manifest.json": results.encoded_json(manifest)}.items():
        with (target / n).open("xb") as stream:
            stream.write(b)
    return target, manifest


def inventory_results_2022(output):
    """Inventory the approved existing results bytes without network or side rules."""
    if output.exists():
        raise ValueError("Existing outputs are never overwritten")
    body = (RESULT_SNAPSHOT / "senate_returns.csv").read_bytes()
    if results.digest(body) != MEDSL_SHA:
        raise ValueError("MEDSL source hash mismatch")
    parent = json.loads((RESULT_SNAPSHOT / "manifest.json").read_text())
    if parent["dataset_version"] != "8.0" or parent["license"]["rightsIdentifier"] != "CC0-1.0":
        raise ValueError("MEDSL version/license mismatch")
    rows, coverage, issues = results.audit(body, requested_years={"2022"})
    outputs = {"returns_2022.csv": results.encoded_csv(rows, results.ROW_FIELDS),
               "coverage.csv": results.encoded_csv(coverage, results.INVENTORY_FIELDS),
               "issues.json": results.encoded_json(issues)}
    manifest = {"schema_version": 1, "rule_version": "Decision 017 / 2022 source inventory v1",
                "source_path": str((RESULT_SNAPSHOT / "senate_returns.csv").relative_to(ROOT)),
                "source": parent["sources"]["senate_returns.csv"], "license": parent["license"],
                "attribution": parent["attribution"], "approval": "Decision 017 / Rahan approved 2026-10-08",
                "summary": issues["summary"], "outputs": {n: {"sha256": results.digest(b), "bytes": len(b)} for n, b in outputs.items()},
                "transformations": ["Select unchanged source strings for year 2022; retain source-row IDs", "Mechanical stage/special/mode group audit; no analytical exclusions"],
                "limitations": ["No verified dates, side mapping, denominator selection, round crosswalk or modeling quantities", "GA GEN and GEN RUNOFF remain separate source groups", "Original retrieval time belongs to preserved MEDSL source, not this offline derivative"]}
    output.mkdir(parents=True, exist_ok=False)
    for n, b in {**outputs, "manifest.json": results.encoded_json(manifest)}.items():
        with (output / n).open("xb") as stream:
            stream.write(b)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=ROOT / "data/raw/senate_poll_archives")
    parser.add_argument("--snapshot", type=Path, help="Replay saved source bytes offline")
    parser.add_argument("--results-only", type=Path, metavar="FRESH_OUTPUT", help="Inventory 2022 from existing MEDSL bytes offline; do not fetch polling")
    args = parser.parse_args()
    if args.results_only:
        if args.snapshot:
            parser.error("--results-only and --snapshot cannot be combined")
        manifest = inventory_results_2022(args.results_only)
        print(args.results_only)
        print(json.dumps(manifest["summary"], indent=2))
        return
    try:
        target, manifest = collect(args.output_root, args.snapshot)
    except (URLError, TimeoutError) as e:
        parser.exit(1, f"Approved source unavailable; no snapshot written: {e}\n")
    print(target)
    print(json.dumps(manifest["summary"]["designated_cycle_counts"], indent=2))


if __name__ == "__main__":
    main()
