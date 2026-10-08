"""Collect pinned MEDSL V8.0 Senate returns and a mechanical coverage audit.

Standard library only. Preserves source strings, all candidates and ballot lines.
No election dates, cycle assignments, party sides, margins or eligibility inferred.
"""
import argparse
import csv
import hashlib
import io
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.request import Request, urlopen

DOI = "doi:10.7910/DVN/PEJ5QU"
METADATA_URL = "https://dataverse.harvard.edu/api/datasets/3072248/versions/8.0"
FILE_IDS = {"senate_returns.csv": 13887039, "codebook.md": 6708560, "sources.csv": 4304792}
SOURCE_URLS = {"metadata.json": METADATA_URL, **{
    name: f"https://dataverse.harvard.edu/api/access/datafile/{file_id}"
    + ("?format=original" if name.endswith(".csv") else "")
    for name, file_id in FILE_IDS.items()
}}
REQUESTED_YEARS = {"2018", "2020", "2024"}
SOURCE_FIELDS = [
    "year", "state", "state_po", "state_fips", "state_cen", "state_ic", "office",
    "district", "stage", "special", "candidate", "party_detailed", "writein", "mode",
    "candidatevotes", "totalvotes", "unofficial", "version", "party_simplified",
]
ROW_FIELDS = ["source_row", "selection_basis", "inventory_id", *SOURCE_FIELDS, "flags"]
GROUP_FIELDS = ["year", "state_po", "office", "district", "stage", "special", "mode"]
INVENTORY_FIELDS = [
    "inventory_id", *GROUP_FIELDS, "source_rows", "row_count", "named_candidate_count",
    "candidate_names_json", "party_labels_json", "reported_totals_json",
    "sum_source_row_votes", "reported_total", "sum_minus_reported_total",
    "unofficial_values_json", "flags",
]


def digest(body):
    return hashlib.sha256(body).hexdigest()


def encoded_json(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode()


def encoded_csv(rows, fields):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def fetch(url):
    request = Request(url, headers={"User-Agent": "election-modeling/1.0 (public MEDSL collection)"})
    with urlopen(request, timeout=45) as response:
        body = response.read()
        receipt = {
            "url": url, "resolved_url": response.url,
            "content_type": response.headers.get("Content-Type", ""),
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "bytes": len(body), "sha256": digest(body),
        }
    return body, receipt


def validate_sources(bodies):
    metadata = json.loads(bodies["metadata.json"])
    version = metadata["data"]
    if metadata.get("status") != "OK" or (version["versionNumber"], version["versionMinorNumber"]) != (8, 0):
        raise ValueError("Expected published MEDSL dataset V8.0")
    if version.get("versionState") != "RELEASED" or version.get("datasetPersistentId") != DOI:
        raise ValueError("Unexpected dataset identity or unpublished version")
    license_info = version.get("license", {})
    if license_info.get("rightsIdentifier") != "CC0-1.0":
        raise ValueError("Expected explicit CC0-1.0 license")
    files = {f["dataFile"]["id"]: f for f in version["files"]}
    for name, file_id in FILE_IDS.items():
        entry = files[file_id]
        if entry.get("restricted") is not False:
            raise ValueError(f"Source is restricted or restriction metadata missing: {name}")
        info = entry["dataFile"]
        size = info["originalFileSize"] if name.endswith(".csv") else info["filesize"]
        if len(bodies[name]) != size:
            raise ValueError(f"Source byte size differs from V8.0 metadata: {name}")
        # Dataverse's tabular MD5 describes the hosted representation, not original CSV.
        if not name.endswith(".csv"):
            checksum = info["checksum"]
            if checksum["type"] != "MD5" or hashlib.md5(bodies[name]).hexdigest() != checksum["value"]:
                raise ValueError(f"Published checksum mismatch: {name}")
    return version


def vote_count(text, field, flags):
    if not text.strip():
        flags.append("missing_" + field)
        return None
    try:
        value = Decimal(text)
        if not value.is_finite() or value < 0 or value != value.to_integral_value():
            raise InvalidOperation
        return int(value)
    except InvalidOperation:
        flags.append("invalid_" + field)
        return None


def normalized_group(row):
    return tuple(row[f].strip().lower() if f in {"stage", "special", "mode"}
                 else row[f] for f in GROUP_FIELDS)


def audit(body, requested_years=None):
    requested_years = REQUESTED_YEARS if requested_years is None else set(requested_years)
    reader = csv.DictReader(io.StringIO(body.decode("utf-8-sig")))
    if reader.fieldnames != SOURCE_FIELDS:
        raise ValueError("MEDSL schema changed or response is not the expected CSV")
    selected, groups, full_counts = [], defaultdict(list), Counter()
    source_count = 0
    for source_count, raw in enumerate(reader, 1):
        if None in raw or any(v is None for v in raw.values()):
            raise ValueError(f"Malformed source row {source_count}")
        full_counts[raw["year"]] += 1
        supplemental = "2020" in requested_years and raw["year"] == "2021" and raw["state_po"] == "GA" and raw["stage"].lower() == "runoff"
        if raw["year"] not in requested_years and not supplemental:
            continue
        flags = []
        for f in ("state", "state_po", "office", "district", "stage", "special", "mode", "party_simplified"):
            if not raw[f].strip():
                flags.append("missing_" + f)
        if raw["office"] != "US SENATE" or raw["district"] != "statewide":
            raise ValueError(f"Unexpected office/district at source row {source_count}")
        for f in ("special", "writein", "unofficial"):
            if raw[f].lower() not in {"true", "false"}:
                flags.append("unknown_" + f)
        if raw["unofficial"].lower() == "true":
            flags.append("unofficial_return")
        if not raw["candidate"].strip():
            flags.append("missing_candidate_name")
        if raw["candidate"].strip().upper() in {"BLANK VOTES", "UNDER VOTES", "OVER VOTES"}:
            flags.append("noncandidate_vote_category")
        if raw["candidate"] != raw["candidate"].strip():
            flags.append("candidate_whitespace")
        candidate_votes = vote_count(raw["candidatevotes"], "candidatevotes", flags)
        total = vote_count(raw["totalvotes"], "totalvotes", flags)
        if total == 1:
            flags.append("possible_uncontested_sentinel")
        if total is not None and candidate_votes is not None and candidate_votes > total:
            flags.append("candidatevotes_exceed_total")
        if supplemental:
            flags.append("supplemental_2021_runoff_cycle_unassigned")
        row = {"source_row": source_count,
               "selection_basis": "supplemental_GA_2021_runoff" if supplemental else "requested_source_year",
               "inventory_id": "", **raw, "flags": flags}
        selected.append(row)
        groups[normalized_group(raw)].append(row)
    if not requested_years.issubset({r["year"] for r in selected}):
        raise ValueError("Missing requested results year")
    inventory, issues = [], []
    for index, (key, rows) in enumerate(sorted(groups.items()), 1):
        group_id = f"medsl-v8-group-{index:03d}"
        flags = ["election_date_unavailable", "round_definition_unverified"]
        totals, votes = [], []
        for row in rows:
            totals.append(vote_count(row["totalvotes"], "totalvotes", []))
            votes.append(vote_count(row["candidatevotes"], "candidatevotes", []))
        valid_total = totals[0] if None not in totals and len(set(totals)) == 1 else None
        votes_sum = sum(votes) if None not in votes else None
        difference = votes_sum - valid_total if votes_sum is not None and valid_total is not None else None
        if valid_total is None:
            flags.append("inconsistent_or_invalid_totalvotes")
        if difference is not None and difference != 0:
            flags.append("source_row_sum_differs_from_total")
        names = Counter(r["candidate"] for r in rows if r["candidate"].strip())
        repeated = {n for n, count in names.items() if count > 1}
        if repeated:
            flags.append("repeated_candidate_name_review_ballot_lines")
        for row in rows:
            row["inventory_id"] = group_id
            if row["candidate"] in repeated:
                row["flags"].append("repeated_candidate_name_review_ballot_lines")
            row["flags"] = ";".join(dict.fromkeys(row["flags"]))
            if row["flags"]:
                issues.append({"source_row": row["source_row"], "inventory_id": group_id,
                               "flags": row["flags"].split(";")})
        flags.extend(f for r in rows for f in r["flags"].split(";") if f)
        out = {"inventory_id": group_id, **dict(zip(GROUP_FIELDS, key)),
               "source_rows": ";".join(str(r["source_row"]) for r in rows), "row_count": len(rows),
               "named_candidate_count": len(names), "candidate_names_json": json.dumps(sorted(names)),
               "party_labels_json": json.dumps(sorted({r["party_detailed"] for r in rows})),
               "reported_totals_json": json.dumps(sorted({r["totalvotes"] for r in rows})),
               "sum_source_row_votes": "" if votes_sum is None else votes_sum,
               "reported_total": "" if valid_total is None else valid_total,
               "sum_minus_reported_total": "" if difference is None else difference,
               "unofficial_values_json": json.dumps(sorted({r["unofficial"] for r in rows})),
               "flags": ";".join(dict.fromkeys(flags))}
        inventory.append(out)
    summary = {
        "full_source_rows": source_count, "full_source_rows_by_year": dict(sorted(full_counts.items())),
        "inventoried_rows": len(selected), "inventoried_rows_by_source_year": dict(sorted(Counter(r["year"] for r in selected).items())),
        "inventory_groups": len(inventory),
        "inventory_groups_by_source_year": dict(sorted(Counter(r["year"] for r in inventory).items())),
        "row_flag_counts": dict(sorted(Counter(f for r in selected for f in r["flags"].split(";") if f).items())),
        "group_flag_counts": dict(sorted(Counter(f for r in inventory for f in r["flags"].split(";") if f).items())),
    }
    return selected, inventory, {"summary": summary, "flagged_rows": issues}


def collect(output_root, snapshot=None):
    if snapshot:
        original = json.loads((snapshot / "manifest.json").read_text())
        if original.get("schema_version") != 1 or original.get("dataset_version") != "8.0":
            raise ValueError("Unsupported source receipt")
        bodies = {name: (snapshot / name).read_bytes() for name in SOURCE_URLS}
        receipts = original["sources"]
        for name, body in bodies.items():
            receipt = receipts[name]
            if receipt["url"] != SOURCE_URLS[name] or receipt["sha256"] != digest(body) or receipt["bytes"] != len(body):
                raise ValueError(f"Replay source receipt mismatch: {name}")
        snapshot_id, retrieved_at = original["snapshot_id"], original["retrieved_at"]
    else:
        # Metadata is checked before accessing its public unrestricted data files.
        body, receipt = fetch(METADATA_URL)
        bodies, receipts = {"metadata.json": body}, {"metadata.json": receipt}
        version = json.loads(body)["data"]
        if (version["versionNumber"], version["versionMinorNumber"]) != (8, 0):
            raise ValueError("Metadata version changed")
        files = {f["dataFile"]["id"]: f for f in version["files"]}
        for name, file_id in FILE_IDS.items():
            if files[file_id].get("restricted") is not False:
                raise ValueError(f"Restricted source: {name}")
            bodies[name], receipts[name] = fetch(SOURCE_URLS[name])
        retrieved_at = receipts["senate_returns.csv"]["retrieved_at"]
        snapshot_id = datetime.fromisoformat(retrieved_at).strftime("%Y%m%dT%H%M%SZ")
    if Path(snapshot_id).name != snapshot_id or snapshot_id in {"", ".", ".."}:
        raise ValueError("Invalid snapshot ID")
    version = validate_sources(bodies)
    rows, inventory, issues = audit(bodies["senate_returns.csv"])
    outputs = {"candidate_rows.csv": encoded_csv(rows, ROW_FIELDS),
               "coverage.csv": encoded_csv(inventory, INVENTORY_FIELDS), "issues.json": encoded_json(issues)}
    for year in ("2018", "2020", "2021", "2024"):
        outputs[f"returns_{year}.csv"] = encoded_csv([r for r in rows if r["year"] == year], ROW_FIELDS)
    manifest = {
        "schema_version": 1, "dataset_doi": DOI, "dataset_version": "8.0",
        "dataset_release_time": version["releaseTime"], "snapshot_id": snapshot_id,
        "retrieved_at": retrieved_at, "license": version["license"],
        "attribution": "MIT Election Data and Science Lab, U.S. Senate statewide returns, V8.0, doi:10.7910/DVN/PEJ5QU",
        "approval": "Rahan, Decision 014, 2026-10-05", "sources": receipts,
        "summary": issues["summary"],
        "outputs": {name: {"sha256": digest(body), "bytes": len(body)} for name, body in outputs.items()},
        "transformations": ["Select unchanged source strings for years 2018/2020/2024, plus GA 2021 runoff rows separately for review",
                            "Add 1-based source data-row IDs, snapshot-local inventory groups and review flags",
                            "Group by source year/state/office/district/stage/special/mode; lowercase stage/special/mode in coverage only",
                            "Compare exact integer source-row vote sums with one consistent reported group total; do not aggregate candidates or choose a denominator"],
        "limitations": ["Coverage groups are source groups, not verified independent contests or round mappings",
                        "Source provides no election dates or poll crosswalk; 2021 runoff cycle remains unassigned",
                        "Unofficial flags, missing names, noncandidate categories and ballot lines remain retained",
                        "No official crosschecks, margins, party-side mapping, analytical exclusions or model calculations",
                        "Codebook body and source listing are older than the main file",
                        "Published tabular MD5 is not compared with original CSV; original byte sizes and codebook MD5 checked, SHA-256 recorded"],
    }
    if snapshot and manifest != original:
        raise ValueError("Replay audit or manifest differs from saved snapshot")
    target = output_root / snapshot_id
    target.mkdir(parents=True, exist_ok=False)
    for name, body in {**bodies, **outputs, "manifest.json": encoded_json(manifest)}.items():
        with (target / name).open("xb") as stream:
            stream.write(body)
    return target, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=Path("data/raw/senate_results"))
    parser.add_argument("--snapshot", type=Path, help="Replay a saved snapshot offline without changing retrieval times")
    args = parser.parse_args()
    target, manifest = collect(args.output_root, args.snapshot)
    print(target)
    print(json.dumps(manifest["summary"], indent=2))


if __name__ == "__main__":
    main()
