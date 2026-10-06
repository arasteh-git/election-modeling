"""Apply Rahan's historical Texas data corrections and matchup exclusion.

Run from the repository root. Uses only saved inputs and the standard library.
Raw snapshots remain unchanged; outputs include an exclusion and change audit.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_SNAPSHOT = Path("data/raw/texas_senate_historical/20261006T024116Z")
EXTRA_FIELDS = [
    "election_date_basis", "partisan_status", "partisan_party", "partisanship_basis",
]
KEY_FIELDS = ["source", "cycle", "source_rows", "poll_id", "question_id"]
AUDIT_FIELDS = KEY_FIELDS + [
    "election_date_before", "election_date_after", "election_date_basis",
    "partisan_raw", "internal_raw", "partisan_status", "partisan_party",
    "partisanship_basis", "action", "reason",
]
PARTY_CODES = {"DEM": "DEM", "REP": "REP", "IND": "IND"}


def classify_partisanship(row):
    """Describe source classifications without inferring ideology from names."""
    if row["source"] != "538_archive" or row["cycle"] not in {"2018", "2020"}:
        return "unknown", "", "Source does not supply partisan/internal classifications"
    partisan = row["partisan"].strip().upper()
    internal = row["internal"].strip().lower()
    if partisan in PARTY_CODES:
        return "partisan", PARTY_CODES[partisan], "538 partisan flag"
    if partisan:
        return "unknown", "", "Unrecognized 538 partisan code; review original field"
    if internal == "true":
        return "partisan", "", "538 internal-poll flag; party unspecified"
    if internal == "false":
        return "not_flagged_partisan", "", "538 partisan blank and internal false"
    return "unknown", "", "538 partisan blank and internal missing/unrecognized"


def prepare(rows):
    """Return retained rows, excluded rows, and an audit of every input record."""
    retained, excluded, audit = [], [], []
    for original in rows:
        row = dict(original)
        if row["cycle"] == "2024":
            if row["election_date"] not in {"", "2024-11-05"}:
                raise ValueError("Conflicting 2024 election date; inspect the source")
            row["election_date"] = "2024-11-05"
            row["election_date_basis"] = "Rahan-confirmed general-election date (2026-10-05)"
        else:
            row["election_date_basis"] = "538 archive election_date"
        row["partisan_status"], row["partisan_party"], row["partisanship_basis"] = classify_partisanship(row)
        # Exclude a clearly identified alternate Democratic challenger. Missing
        # candidate names or other ambiguous matchups remain available for review.
        hypothetical = (
            row["cycle"] == "2020"
            and row["rep_candidate"] == "John Cornyn"
            and bool(row["dem_candidate"])
            and row["dem_candidate"] != "Mary Jennings Hegar"
        )
        reason = "2020 hypothetical Democratic challenger instead of M.J. Hegar" if hypothetical else ""
        event = {field: row[field] for field in KEY_FIELDS}
        event.update(
            election_date_before=original["election_date"],
            election_date_after=row["election_date"],
            election_date_basis=row["election_date_basis"],
            partisan_raw=original["partisan"], internal_raw=original["internal"],
            partisan_status=row["partisan_status"], partisan_party=row["partisan_party"],
            partisanship_basis=row["partisanship_basis"],
            action="excluded" if hypothetical else "kept", reason=reason,
        )
        audit.append(event)
        if hypothetical:
            excluded.append({**row, "exclusion_reason": reason})
        else:
            retained.append(row)
    return retained, excluded, audit


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--output-root", type=Path, default=Path("data/processed/texas_senate_historical"))
    args = parser.parse_args()
    source_manifest = json.loads((args.snapshot / "manifest.json").read_text())
    for filename, source in source_manifest["sources"].items():
        if sha256(args.snapshot / filename) != source["sha256"]:
            raise ValueError(f"Source checksum mismatch: {filename}")
    input_path = args.snapshot / "normalized.csv"
    with input_path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = list(reader.fieldnames or [])
        required = set(KEY_FIELDS + ["election_date", "partisan", "internal", "dem_candidate", "rep_candidate", "flags"])
        if not required.issubset(fields) or set(EXTRA_FIELDS).intersection(fields):
            raise ValueError("Expected the original historical inventory schema")
        rows = list(reader)
    if not rows or any(None in row or any(v is None for v in row.values()) for row in rows):
        raise ValueError("Empty or malformed inventory")
    if len({tuple(row[f] for f in KEY_FIELDS) for row in rows}) != len(rows):
        raise ValueError("Duplicate source keys require review")
    retained, excluded, audit = prepare(rows)
    fields += EXTRA_FIELDS
    folder = args.output_root / args.snapshot.name
    folder.mkdir(parents=True, exist_ok=False)
    write_csv(folder / "normalized.csv", retained, fields)
    for cycle in sorted({row["cycle"] for row in rows}):
        write_csv(folder / f"texas_{cycle}.csv", [row for row in retained if row["cycle"] == cycle], fields)
    write_csv(folder / "excluded.csv", excluded, fields + ["exclusion_reason"])
    write_csv(folder / "changes.csv", audit, AUDIT_FIELDS)
    counts = {
        cycle: {
            "input_records": sum(row["cycle"] == cycle for row in rows),
            "retained_records": sum(row["cycle"] == cycle for row in retained),
            "excluded_records": sum(row["cycle"] == cycle for row in excluded),
            "lv_records": sum(row["cycle"] == cycle and row["population"] == "LV" for row in retained),
            "partisan_status": dict(Counter(row["partisan_status"] for row in retained if row["cycle"] == cycle)),
        }
        for cycle in sorted({row["cycle"] for row in rows})
    }
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_snapshot": args.snapshot.as_posix(),
        "source_retrieved_at": source_manifest["retrieved_at"],
        "input_sha256": {"normalized.csv": sha256(input_path), "manifest.json": sha256(args.snapshot / "manifest.json")},
        "source_provenance": source_manifest["sources"],
        "attribution": source_manifest["attribution"],
        "permissions": source_manifest["permissions"],
        "rule_version": "Decision 011 / 2026-10-05",
        "rules": [
            "Set all 2024 election dates to 2024-11-05 as confirmed by Rahan; record date basis.",
            "Classify 2018/2020 using 538 partisan/internal flags; preserve original fields. Not flagged is not independent nonpartisan verification. 2024 remains unknown.",
            "Exclude 2020 questions naming a non-Hegar Democratic challenger against John Cornyn; retain exclusions with keys and reasons. Do not exclude missing/ambiguous names automatically.",
        ],
        "counts_by_cycle": counts,
        "election_date_corrections": sum(r["election_date_before"] != r["election_date_after"] for r in audit),
        "output_sha256": {path.name: sha256(path) for path in sorted(folder.glob("*.csv"))},
        "limitations": "All populations and partisan polls retained. Existing duplicate-question, field-date, source, and publication flags preserved. Primary releases, archive mirror identity, and 2024 partisanship not independently verified. No historical averaging or uncertainty calibration implemented.",
    }
    (folder / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"folder": str(folder), "retained": len(retained), "excluded": len(excluded), "counts": counts}))


if __name__ == "__main__":
    main()
