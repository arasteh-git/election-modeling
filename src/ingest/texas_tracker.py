"""Collect the UT Texas Senate tracker; no poll selection or modeling.

Run from the repository root: python src/ingest/texas_tracker.py
Offline replay: add --html PATH --retrieved-at ISO_UTC_TIMESTAMP.
Uses only the Python standard library. Each run writes a new snapshot folder.
"""
import argparse
import csv
import hashlib
import json
import re
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

URL = "https://texaspolitics.utexas.edu/blog/texas-2026-u-s-senate-poll-tracker"
HEADERS = ["Poll", "Field Dates", "Sample Size", "Sample Type", "MOE", "Paxton", "Talarico", "Other", "Spread"]


class Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.table = None
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.table = []
        elif self.table is not None:
            if tag == "tr":
                self.row = []
            elif tag in ("td", "th"):
                self.cell = {"text": "", "links": []}
            elif tag == "a" and self.cell is not None:
                href = dict(attrs).get("href")
                if href:
                    self.cell["links"].append(urljoin(URL, href))

    def handle_data(self, data):
        if self.cell is not None:
            self.cell["text"] += data

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.cell["text"] = " ".join(self.cell["text"].split())
            self.row.append(self.cell)
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            self.tables.append(self.table)
            self.table = None


def extract(html):
    parser = Tables()
    parser.feed(html)
    matches = [t for t in parser.tables if t and [c["text"] for c in t[0]] == HEADERS]
    if len(matches) != 1:
        raise ValueError("Expected one table with the approved headers; inspect source changes.")
    records = []
    for index, cells in enumerate(matches[0][1:], 1):
        if len(cells) != len(HEADERS):
            raise ValueError(f"Unexpected cell count in row {index}")
        record = dict(zip(HEADERS, [c["text"] for c in cells]))
        record["tracker_row"] = index
        record["release_url"] = cells[0]["links"][0] if cells[0]["links"] else ""
        records.append(record)
    if not records:
        raise ValueError("No polls found")
    return records


def normalize(records):
    output = []
    issues = []
    for r in records:
        i = r["tracker_row"]
        start, end = re.split(r"\s*[-–]\s*", r["Field Dates"])
        # This source is explicitly the 2026 election tracker and omits the year.
        start, end = [date(2026, *map(int, d.split("/"))).isoformat() for d in (start, end)]
        n = int(r["Sample Size"].replace(",", ""))
        dem, rep = float(r["Talarico"]), float(r["Paxton"])
        if start > end or n <= 0 or not (0 <= dem <= 100 and 0 <= rep <= 100):
            raise ValueError(f"Invalid dates, sample, or percentages in row {i}")
        if r["Sample Type"] not in ("LV", "RV", "A"):
            raise ValueError(f"Unknown population in row {i}")
        spread = r["Spread"]
        reported = 0.0 if spread.lower() == "even" else float(re.search(r"\+\s*([\d.]+)", spread).group(1)) * (1 if spread.startswith("Talarico") else -1)
        flags = []
        if abs(dem - rep - reported) > 0.01:
            flags.append("spread_mismatch")
            issues.append({"tracker_row": i, "flag": "spread_mismatch", "detail": f"Candidate shares imply {dem-rep:+g}; tracker spread is {spread}. No correction applied."})
        if not r["release_url"]:
            flags.append("missing_release_url")
        output.append({"tracker_row": i, "race_id": "2026-TX-US-SENATE-GENERAL", "poll_label": r["Poll"], "start_date": start, "end_date": end, "sample_size": n, "population": r["Sample Type"], "dem_pct": dem, "rep_pct": rep, "other_raw": r["Other"], "moe_raw": r["MOE"], "spread_raw": spread, "release_url": r["release_url"], "primary_verification": "pending", "flags": ";".join(flags)})
    return output, issues


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--html", type=Path)
    ap.add_argument("--retrieved-at")
    ap.add_argument("--output-root", type=Path, default=Path("data/raw/texas_tracker"))
    args = ap.parse_args()
    if args.html and not args.retrieved_at:
        ap.error("Offline snapshots require --retrieved-at; do not substitute replay time.")
    if args.html:
        body = args.html.read_bytes()
    else:
        with urlopen(Request(URL, headers={"User-Agent": "ElectionLearningProject/0.1"}), timeout=30) as response:
            body = response.read()
    retrieved = args.retrieved_at or datetime.now(timezone.utc).isoformat()
    stamp = datetime.fromisoformat(retrieved)
    if stamp.utcoffset() is None:
        ap.error("retrieved-at must contain a timezone")
    html = body.decode("utf-8")
    records = extract(html)
    normalized, issues = normalize(records)
    folder = args.output_root / stamp.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    folder.mkdir(parents=True, exist_ok=False)
    (folder / "source.html").write_bytes(body)
    write_csv(folder / "tracker.csv", records)
    write_csv(folder / "normalized.csv", normalized)
    (folder / "issues.json").write_text(json.dumps(issues, indent=2) + "\n")
    update = re.search(r"Updated\s+([A-Za-z]+ \d{1,2}, 2026)", html)
    metadata = {"source_url": URL, "title": "Texas 2026 U.S. Senate Poll Tracker", "author": "Texas Politics Project", "publisher": "Texas Politics Project at the University of Texas at Austin", "retrieved_at": retrieved, "source_last_updated": update.group(1) if update else None, "sha256": hashlib.sha256(body).hexdigest(), "row_count": len(records), "normalization": "Whitespace collapsed; relative links resolved; field dates assigned 2026 from tracker context; samples and candidate shares parsed as numbers. No corrections, exclusions, imputation, or weighting.", "verification": "Tracker extraction only; linked primary releases require separate review."}
    (folder / "manifest.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps({"folder": str(folder), "rows": len(records), "issues": issues}))


if __name__ == "__main__":
    main()
