"""Extract factual FEC reference cells from unchanged, locally cached workbooks.

No votes are replaced in the MEDSL input. Standard library XLSX reader; no Excel
files are authored. Reads cached receipts; exports JSON facts with cell locators.
"""
import argparse
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath

NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def sheet_rows(path, match):
    with zipfile.ZipFile(path) as archive:
        strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            strings = ["".join(s.itertext()) for s in ET.fromstring(archive.read("xl/sharedStrings.xml")).findall("s:si", NS)]
        relations = {r.attrib["Id"]: r.attrib["Target"] for r in ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))}
        sheets = ET.fromstring(archive.read("xl/workbook.xml")).find("s:sheets", NS)
        selected = [s for s in sheets if match in s.attrib["name"]]
        if len(selected) != 1:
            raise ValueError("Expected one Senate reference sheet")
        sheet = selected[0]
        target = relations[sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]]
        member = target.lstrip("/") if target.startswith("/") else str(PurePosixPath("xl") / target)
        for row in ET.fromstring(archive.read(member)).findall("s:sheetData/s:row", NS):
            cells = {}
            for cell in row:
                value = cell.find("s:v", NS)
                text = "" if value is None else value.text or ""
                if cell.attrib.get("t") == "s":
                    text = strings[int(text)]
                elif cell.attrib.get("t") == "inlineStr":
                    text = "".join(cell.find("s:is", NS).itertext())
                cells[re.sub(r"\d", "", cell.attrib["r"])] = text
            yield sheet.attrib["name"], int(row.attrib["r"]), cells


def extract(cache):
    receipts = json.loads((cache / "receipts.json").read_text())
    candidates, totals = [], []
    for year in (2018, 2020):
        name = f"fec_{year}.xlsx"
        body = (cache / name).read_bytes()
        if hashlib.sha256(body).hexdigest() != receipts[name]["sha256"]:
            raise ValueError(f"Reference hash mismatch: {name}")
        for sheet, row, cells in sheet_rows(cache / name, "US Senate Results by State"):
            state, district = cells.get("B", ""), cells.get("D", "")
            if not re.fullmatch("[A-Z]{2}", state) or not district.startswith("S"):
                continue
            special = "UNEXPIRED" in district
            locator = {"reference_id": name, "sheet": sheet, "row": row,
                       "url": receipts[name]["url"], "source_sha256": receipts[name]["sha256"]}
            if cells.get("J") == "Total State Votes:":
                totals.append({"cycle": str(year), "state_po": state, "special": special,
                               "general_total_raw": cells.get("P", ""),
                               "runoff_total_raw": cells.get("R", ""), **locator})
            elif cells.get("I", "").strip():
                candidates.append({"cycle": str(year), "state_po": state, "special": special,
                                   "name": (cells.get("G", "") + " " + cells.get("H", "")).strip(),
                                   "source_name": cells["I"], "fec_id": cells.get("E", ""),
                                   "party": cells.get("K", ""), "general_votes_raw": cells.get("P", ""),
                                   "runoff_votes_raw": cells.get("R", ""),
                                   "note": cells.get("W" if year == 2018 else "X", ""), **locator})
    return {"schema_version": 1, "purpose": "Factual ballot/party/round references; not replacement results",
            "sources": receipts, "candidates": candidates, "totals": totals}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=Path("outputs/calibration_reference_research"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    facts = extract(args.cache)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        stream.write(json.dumps(facts, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(f"{len(facts['candidates'])} candidate reference rows; {len(facts['totals'])} totals")


if __name__ == "__main__":
    main()
