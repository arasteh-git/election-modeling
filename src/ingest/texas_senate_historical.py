"""Collect a historical Texas Senate inventory, without analytical poll selection.

Standard library only. Run from the repository root. --snapshot replays saved
sources offline, retaining their original retrieval timestamps and checksums.
"""
import argparse
import csv
import hashlib
import io
import json
import math
import re
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from texas_tracker import Tables

ARCHIVE_REVISION = "d3d0c6be4e35945e59c1cb574b4050ca1787a2bc"
ARCHIVE_URL = f"https://raw.githubusercontent.com/khristel26/Senate/{ARCHIVE_REVISION}/senate_polls_historical.csv"
TRACKER_URL = "https://texaspolitics.utexas.edu/blog/texas-2024-us-senate-poll-tracker"
SOURCE_URLS = {
    "senate_polls_historical.csv": ARCHIVE_URL,
    "texas_2024_source.html": TRACKER_URL,
    "fivethirtyeight_README.md": "https://raw.githubusercontent.com/fivethirtyeight/data/master/README.md",
    "fivethirtyeight_polls_README.md": "https://raw.githubusercontent.com/fivethirtyeight/data/master/polls/README.md",
}
FIELDS = [
    "source", "source_rows", "cycle", "race_id", "poll_id", "question_id",
    "poll_label", "pollster_id", "sponsors", "start_date", "end_date",
    "election_date", "sample_size", "population", "population_raw",
    "population_full", "dem_candidate", "rep_candidate", "dem_pct", "rep_pct",
    "candidate_answers_json", "field_dates_raw", "moe_raw", "spread_raw",
    "release_url", "created_at_raw", "notes", "methodology", "tracking",
    "internal", "partisan", "primary_verification", "flags",
]
EXPECTED_MATCHUPS = {
    "2018": ("Beto O'Rourke", "Ted Cruz"),
    "2020": ("Mary Jennings Hegar", "John Cornyn"),
    "2024": ("Colin Allred", "Ted Cruz"),
}


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def number(value, field, flags):
    if not value.strip():
        flags.append("missing_" + field)
        return ""
    result = float(value.replace(",", "").removesuffix("%"))
    if not math.isfinite(result):
        raise ValueError(f"Non-finite {field}: {value!r}")
    if field == "sample_size":
        if result <= 0 or not result.is_integer():
            raise ValueError(f"Invalid sample_size: {value!r}")
        return int(result)
    if not 0 <= result <= 100:
        raise ValueError(f"Invalid {field}: {value!r}")
    return result


def archive_date(value):
    return datetime.strptime(value, "%m/%d/%y").date().isoformat()


def archive_records(body):
    reader = csv.DictReader(io.StringIO(body.decode("utf-8-sig")))
    required = {"poll_id", "question_id", "race_id", "cycle", "state", "stage", "office_type",
                "pollster", "start_date", "end_date", "population", "sample_size", "party",
                "candidate_name", "candidate_id", "pct", "url", "created_at", "election_date"}
    if not required.issubset(reader.fieldnames or []):
        raise ValueError("Historical archive headers changed or response is not a CSV")
    selected, groups = [], defaultdict(list)
    source_count = 0
    for source_count, raw in enumerate(reader, 1):
        if None in raw or any(v is None for v in raw.values()):
            raise ValueError(f"Malformed archive row {source_count}")
        if raw["state"] != "Texas" or raw["cycle"] not in {"2018", "2020"}:
            continue
        if raw["office_type"] != "U.S. Senate" or raw["stage"] != "general":
            raise ValueError("Unexpected Texas stage/office; inspect before changing scope")
        row = {"source_row": source_count, **raw}
        selected.append(row)
        key = tuple(row[f] for f in ("cycle", "poll_id", "question_id", "race_id"))
        if any(not part for part in key):
            raise ValueError("Missing grouping identifier")
        groups[key].append(row)
    if {r["cycle"] for r in selected} != {"2018", "2020"}:
        raise ValueError("Archive does not contain both requested older cycles")
    questions_per_poll = Counter((k[0], k[1]) for k in groups)
    normalized = []
    for (cycle, poll_id, question_id, race_id), candidates in groups.items():
        first = candidates[0]
        for field in ("pollster", "display_name", "start_date", "end_date", "election_date",
                      "population", "population_full", "sample_size", "url", "created_at"):
            if len({r[field] for r in candidates}) != 1:
                raise ValueError(f"Inconsistent {field} within question {question_id}")
        flags = ["mirror_not_verified_against_original", "publication_date_unverified"]
        out = dict.fromkeys(FIELDS, "")
        out.update(source="538_archive", source_rows=";".join(str(r["source_row"]) for r in candidates),
                   cycle=cycle, race_id=race_id, poll_id=poll_id, question_id=question_id,
                   poll_label=first["display_name"] or first["pollster"],
                   pollster_id=first.get("pollster_id", ""), sponsors=first.get("sponsors", ""),
                   start_date=archive_date(first["start_date"]), end_date=archive_date(first["end_date"]),
                   election_date=archive_date(first["election_date"]),
                   sample_size=number(first["sample_size"], "sample_size", flags),
                   population=first["population"].upper(), population_raw=first["population"],
                   population_full=first["population_full"], release_url=first["url"],
                   created_at_raw=first["created_at"], notes=first.get("notes", ""),
                   methodology=first.get("methodology", ""), tracking=first.get("tracking", ""),
                   internal=first.get("internal", ""), partisan=first.get("partisan", ""),
                   primary_verification="pending")
        if not out["population"]:
            flags.append("missing_population")
        elif out["population"] not in {"LV", "RV", "A"}:
            flags.append("nonstandard_population")
        if not out["release_url"]:
            flags.append("missing_release_url")
        if out["start_date"] > out["end_date"]:
            raise ValueError(f"Reversed field dates for question {question_id}")
        answers = []
        for r in candidates:
            number(r["pct"], "candidate_pct", flags)
            answers.append({f: r[f] for f in ("candidate_id", "candidate_name", "party", "pct")})
        out["candidate_answers_json"] = json.dumps(answers, ensure_ascii=False)
        for party, prefix in (("DEM", "dem"), ("REP", "rep")):
            party_rows = [r for r in candidates if r["party"] == party]
            if len(party_rows) == 1:
                out[prefix + "_candidate"] = party_rows[0]["candidate_name"]
                out[prefix + "_pct"] = number(party_rows[0]["pct"], prefix + "_pct", flags)
            else:
                flags.append("ambiguous_or_missing_" + prefix + "_candidate")
        if (out["dem_candidate"], out["rep_candidate"]) != EXPECTED_MATCHUPS[cycle]:
            flags.append("hypothetical_or_unexpected_matchup")
        if questions_per_poll[(cycle, poll_id)] > 1:
            flags.append("multiple_questions_same_poll")
        if len({r["candidate_id"] for r in candidates}) != len(candidates):
            flags.append("duplicate_candidate_id")
        out["flags"] = ";".join(dict.fromkeys(flags))
        normalized.append(out)
    return selected, normalized, source_count


class HistoricalTables(Tables):
    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if tag == "a" and self.cell is not None and dict(attrs).get("href"):
            self.cell["links"][-1] = urljoin(TRACKER_URL, dict(attrs)["href"])


def tracker_records(body):
    parser = HistoricalTables()
    parser.feed(body.decode("utf-8"))
    headers = ["Poll", "Field Dates", "Sample Size", "Sample", "MOE", "Cruz", "Allred", "Spread"]
    matches = [t for t in parser.tables if t and [c["text"] for c in t[0]] == headers]
    if len(matches) != 1:
        raise ValueError("Expected one 2024 table with the documented headers")
    extracted, normalized, footnotes = [], [], []
    for index, cells in enumerate(matches[0][1:], 1):
        if len(cells) == 1 and cells[0]["text"] == "* Result includes force for undecideds":
            footnotes.append(cells[0]["text"])
            continue
        if len(cells) != len(headers):
            raise ValueError(f"Unexpected 2024 row {index}")
        raw = dict(zip(headers, (c["text"] for c in cells)))
        raw.update(tracker_row=index, release_url=cells[0]["links"][0] if cells[0]["links"] else "")
        extracted.append(raw)
        flags = ["publication_date_unavailable"]
        out = dict.fromkeys(FIELDS, "")
        out.update(source="ut_tracker_2024", source_rows=str(index), cycle="2024",
                   poll_label=raw["Poll"], sample_size=number(raw["Sample Size"], "sample_size", flags),
                   population=raw["Sample"], population_raw=raw["Sample"],
                   dem_candidate="Colin Allred", rep_candidate="Ted Cruz",
                   dem_pct=number(raw["Allred"], "dem_pct", flags),
                   rep_pct=number(raw["Cruz"], "rep_pct", flags),
                   field_dates_raw=raw["Field Dates"], moe_raw=raw["MOE"], spread_raw=raw["Spread"],
                   release_url=raw["release_url"], primary_verification="pending")
        # Only parse an unambiguous, explicitly dated source interval. A known
        # slash typo stays unresolved; do not silently repair its dates.
        match = re.fullmatch(r"(\d{1,2})/(\d{1,2})-(\d{1,2})/(\d{1,2})/(\d{4})", raw["Field Dates"])
        if match:
            sm, sd, em, ed, year = map(int, match.groups())
            out["start_date"] = date(year, sm, sd).isoformat()
            out["end_date"] = date(year, em, ed).isoformat()
            if out["start_date"] > out["end_date"]:
                raise ValueError(f"Reversed 2024 dates in row {index}")
        else:
            flags.append("unparsed_field_dates")
        if out["population"] not in {"LV", "RV", "A"}:
            flags.append("nonstandard_population")
        if not out["release_url"]:
            flags.append("missing_release_url")
        if not out["moe_raw"]:
            flags.append("missing_moe")
        if "*" in raw["Poll"]:
            flags.append("forced_undecided_source_note")
        spread = raw["Spread"]
        if spread.lower() == "tie":
            reported = 0.0
        else:
            match = re.fullmatch(r"(Cruz|Allred)\s*\+\s*([\d.]+)", spread)
            if not match:
                raise ValueError(f"Unrecognized 2024 spread in row {index}")
            reported = float(match[2]) * (1 if match[1] == "Allred" else -1)
        if out["dem_pct"] != "" and out["rep_pct"] != "" and abs(out["dem_pct"] - out["rep_pct"] - reported) > 0.01:
            flags.append("spread_mismatch")
        out["flags"] = ";".join(flags)
        normalized.append(out)
    if not normalized:
        raise ValueError("No 2024 rows")
    link_labels = defaultdict(set)
    for r in normalized:
        if r["release_url"]:
            link_labels[r["release_url"]].add(r["poll_label"])
    for r in normalized:
        if r["release_url"] and len(link_labels[r["release_url"]]) > 1:
            r["flags"] += ";release_url_shared_across_labels"
    return extracted, normalized, footnotes


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--snapshot", type=Path, help="Existing snapshot for offline replay")
    ap.add_argument("--output-root", type=Path, default=Path("data/raw/texas_senate_historical"))
    args = ap.parse_args()
    bodies, sources = {}, {}
    if args.snapshot:
        original = json.loads((args.snapshot / "manifest.json").read_text())
        for filename in SOURCE_URLS:
            body = (args.snapshot / filename).read_bytes()
            if hashlib.sha256(body).hexdigest() != original["sources"][filename]["sha256"]:
                raise ValueError(f"Snapshot checksum mismatch: {filename}")
            bodies[filename] = body
            sources[filename] = original["sources"][filename]
        stamp = original["retrieved_at"]
    else:
        for filename, url in SOURCE_URLS.items():
            with urlopen(Request(url, headers={"User-Agent": "ElectionLearningProject/0.1"}), timeout=30) as response:
                bodies[filename] = response.read()
                sources[filename] = {"url": url, "final_url": response.geturl(),
                                     "retrieved_at": datetime.now(timezone.utc).isoformat(),
                                     "sha256": hashlib.sha256(bodies[filename]).hexdigest()}
        stamp = datetime.now(timezone.utc).isoformat()
    candidate_rows, older, source_count = archive_records(bodies["senate_polls_historical.csv"])
    tracker_rows, newer, footnotes = tracker_records(bodies["texas_2024_source.html"])
    rows = older + newer
    issues = [{"source": r["source"], "cycle": r["cycle"], "source_rows": r["source_rows"],
               "poll_id": r["poll_id"], "question_id": r["question_id"], "flags": r["flags"].split(";")}
              for r in rows if r["flags"]]
    counts = {c: {"records": sum(r["cycle"] == c for r in rows),
                  "lv_records": sum(r["cycle"] == c and r["population"] == "LV" for r in rows),
                  "flagged_matchups": sum(r["cycle"] == c and "hypothetical_or_unexpected_matchup" in r["flags"] for r in rows)}
              for c in ("2018", "2020", "2024")}
    metadata = {
        "retrieved_at": stamp, "sources": sources, "archive_revision": ARCHIVE_REVISION,
        "attribution": {"538_archive": "FiveThirtyEight / ABC News; preserved by khristel26/Senate on GitHub",
                        "ut_tracker_2024": "Texas 2024 U.S. Senate Poll Tracker; Texas Politics Project at the University of Texas at Austin"},
        "permissions": {"538_archive": "FiveThirtyEight repository states CC BY 4.0 unless otherwise noted; saved READMEs. Mirror identity has not been verified byte-for-byte against original.",
                        "ut_tracker_2024": "Republishing guidelines in saved HTML: attribution, unchanged original, no resale, honor change/removal requests. CSVs are labeled mechanical derivatives."},
        "archive_candidate_rows_all_states": source_count, "texas_archive_candidate_rows": len(candidate_rows),
        "row_count": len(rows), "counts_by_cycle": counts, "tracker_footnotes": footnotes,
        "selection": "Archive: state Texas, cycle 2018 or 2020. All selected rows must be U.S. Senate general-election stage. Tracker: every 2024 table data row, including early matchups. No population, recency, partisan, or quality exclusions.",
        "transformations": "Archive candidate rows grouped by cycle/poll_id/question_id/race_id; single DEM and REP shares copied with their names, all candidate answers retained as JSON. Dates converted to ISO; population codes uppercased; percentages parsed, never rescaled. Tracker whitespace collapsed, relative links resolved, unambiguous explicit dates parsed; malformed dates left blank and flagged. Repeat/hypothetical/ambiguous observations preserved.",
        "verification": "Extraction and mechanical validation only. No individual primary releases verified. No election results collected. created_at is archive entry time, not verified publication time; 2024 publication dates unavailable. Historical availability remains unresolved.",
        "limitations": "2018/2020 use a third-party preserved 538 file; 2024 uses UT's tracker last updated October 30, 2024 and may omit later polls. Coverage is not an exhaustive or consistently sampled census across cycles. Question records are not independent surveys. Some 2020 questions use hypothetical Democratic candidates. Source rounding/forced undecided treatment is retained.",
    }
    folder = args.output_root / datetime.fromisoformat(stamp).astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    folder.mkdir(parents=True, exist_ok=False)
    for filename, body in bodies.items():
        (folder / filename).write_bytes(body)
    write_csv(folder / "texas_538_candidate_rows.csv", candidate_rows, list(candidate_rows[0]))
    write_csv(folder / "texas_2024_tracker.csv", tracker_rows, list(tracker_rows[0]))
    write_csv(folder / "normalized.csv", rows, FIELDS)
    for cycle in counts:
        write_csv(folder / f"texas_{cycle}.csv", [r for r in rows if r["cycle"] == cycle], FIELDS)
    (folder / "manifest.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (folder / "issues.json").write_text(json.dumps(issues, indent=2) + "\n")
    print(json.dumps({"folder": str(folder), "counts": counts, "rows": len(rows)}))


if __name__ == "__main__":
    main()
