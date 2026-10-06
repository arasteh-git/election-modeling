"""Prepare immutable Senate calibration inputs; no statistical/model calculations.

Offline, standard library only. Source columns survive unchanged. Decisions
012–014 govern eligibility; uncertain identities, returns and preferences stay
pending. Explicit reference JSON supplies aliases and exceptional round facts.
"""
import argparse
import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REFERENCES = Path(__file__).with_name("calibration_references")
POLL_SNAPSHOT = ROOT / "data/raw/texas_senate_historical/20261006T024116Z"
RESULT_SNAPSHOT = ROOT / "data/raw/senate_results/20261006T035630Z"
TEXAS_SNAPSHOT = ROOT / "data/processed/texas_senate_historical/20261006T024116Z"
NONCANDIDATE = {"BLANKVOTES", "OVERVOTES", "UNDERVOTES", "VOID", "SPOILED"}
DEMOCRATIC = {"DEM", "D", "DEMOCRAT", "DEMOCRATIC", "DEMOCRATIC-FARMER-LABOR", "DEMOCRATIC-NPL", "DEMOCRATIC/WORKING FAMILIES", "N(D)/D"}
REPUBLICAN = {"REP", "R", "REPUBLICAN", "GOP", "REPUBLICAN/CONSERVATIVE"}


def norm(value):
    return re.sub(r"[^A-Z0-9]", "", unicodedata.normalize("NFKD", value).upper())


def integer(value):
    number = Decimal(value)
    if not number.is_finite() or number < 0 or number != number.to_integral_value():
        raise ValueError(f"Not a nonnegative integral vote count: {value!r}")
    return int(number)


def date(value):
    if not value:
        return ""
    for fmt in ("%Y-%m-%d", "%m/%d/%y", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    raise ValueError(f"Unrecognized date: {value!r}")


def party_side(party):
    label = party.strip().upper()
    if label in DEMOCRATIC:
        return "D"
    if label in REPUBLICAN:
        return "R"
    return "other" if label else "unknown"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError(f"Duplicate columns: {path}")
        rows = list(reader)
    if any(None in row or None in row.values() for row in rows):
        raise ValueError(f"Malformed CSV: {path}")
    return rows


def write_csv(path, rows, empty_fields=()):
    fields = list(dict.fromkeys(key for row in rows for key in row)) or list(empty_fields)
    with path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def contest_id(cycle, state, special, round_name):
    return f"{cycle}-{state}-{'special' if special else 'ordinary'}-{round_name}"


def result_contest(row):
    cycle = "2020" if row["year"] == "2021" else row["year"]
    special = row["special"].lower() == "true"
    round_name = "runoff" if row["year"] == "2021" or (cycle == "2018" and row["state_po"] == "MS" and special) else "general"
    if (cycle, row["state_po"], special, round_name) in (("2018", "MS", True, "general"), ("2020", "GA", True, "general"), ("2020", "LA", False, "general")):
        round_name = "first"
    return contest_id(cycle, row["state_po"], special, round_name)


def poll_contest(row, states):
    state = states[row["state"].upper()]
    # Reviewed exceptional seat crosswalk; source seat_number is not Senate class.
    special = ((row["cycle"], state, row["seat_name"]) in {
        ("2018", "MS", "Class II"), ("2018", "MN", "Class II"),
        ("2020", "GA", "Class III"), ("2020", "AZ", "Class III")})
    stage = row["stage"].lower()
    rounds = {"general": "general", "jungle primary": "first", "runoff": "runoff"}
    if stage not in rounds:
        return ""
    return contest_id(row["cycle"], state, special, rounds[stage])


def choose_questions(questions):
    """Apply only the approved full-ballot preference; leave all ties pending."""
    groups = defaultdict(list)
    for q in questions:
        if q["status"] == "eligible":
            groups[(q["source"], q["poll_key"], q["contest_id"])].append(q)
    for group in groups.values():
        full = [q for q in group if q["full_ballot"] == "true"]
        if len(group) == 1:
            group[0].update(status="selected", preference_basis="Only eligible LV question for this poll/round")
        elif len(full) == 1:
            for q in group:
                if q is full[0]:
                    q.update(status="selected", preference_basis="Unique full-ballot LV question (Decision 013)")
                else:
                    q.update(status="excluded", reasons="alternate_question", preference_basis="Same poll/round has a unique full-ballot LV question")
        else:
            for q in group:
                q.update(status="pending", reasons="ambiguous_question_preference", preference_basis="Multiple eligible questions; no unique full-ballot choice")


def verified_inputs(polls, results, texas, references):
    inputs = {}
    for folder, manifest_name in ((polls, "manifest.json"), (results, "manifest.json"), (texas, "manifest.json")):
        manifest = json.loads((folder / manifest_name).read_text())
        inputs[str(folder / manifest_name)] = sha(folder / manifest_name)
        entries = manifest.get("sources", {})
        entries = {**entries, **manifest.get("outputs", {})}
        entries.update({k: {"sha256": v} for k, v in manifest.get("output_sha256", {}).items()})
        for name, receipt in entries.items():
            if "sha256" in receipt:
                path = folder / name
                if sha(path) != receipt["sha256"]:
                    raise ValueError(f"Source hash mismatch: {path}")
                inputs[str(path)] = receipt["sha256"]
    if manifest["rule_version"] != "Decision 011 / 2026-10-05":
        raise ValueError("Unapproved Texas preparation version")
    result_manifest = json.loads((results / "manifest.json").read_text())
    if (result_manifest["dataset_version"] != "8.0" or result_manifest["dataset_doi"] != "doi:10.7910/DVN/PEJ5QU" or result_manifest["license"]["rightsIdentifier"] != "CC0-1.0"):
        raise ValueError("Unapproved MEDSL version, DOI or license")
    pinned = {results / "senate_returns.csv": "6f745db1b4a0026ad837e74428f9ed6f3f77fa51eb6f858b58ebdbc186fdb3bd",
              polls / "senate_polls_historical.csv": "f781e2dad7b5fa0b0f9b3d453c35ae0efb2ce431b38573d2aa3164aa9d8808dd"}
    for path, checksum in pinned.items():
        if sha(path) != checksum: raise ValueError(f"Not the reviewed source snapshot: {path}")
    for name in ("fec_facts.json", "round_facts.json", "poll_aliases.json"):
        inputs[str(references / name)] = sha(references / name)
    return inputs


def prepare(polls=POLL_SNAPSHOT, results=RESULT_SNAPSHOT, texas=TEXAS_SNAPSHOT,
            references=REFERENCES, output=None, created_at=None):
    if output is None or output.exists():
        raise ValueError("Provide a fresh output directory; existing outputs are never overwritten")
    inputs = verified_inputs(polls, results, texas, references)
    facts = json.loads((references / "fec_facts.json").read_text())
    rounds = json.loads((references / "round_facts.json").read_text())
    aliases = {f"{a['cycle']}:{a['poll_candidate_id']}": a for a in json.loads((references / "poll_aliases.json").read_text())["aliases"]}
    result_raw = read_csv(results / "candidate_rows.csv")
    poll_raw = read_csv(polls / "senate_polls_historical.csv")
    texas_raw = read_csv(texas / "texas_2024.csv")
    original_results = read_csv(results / "senate_returns.csv")
    for row in result_raw:
        original = original_results[int(row["source_row"]) - 1]
        if any(row[k] != v for k, v in original.items()):
            raise ValueError(f"Result inventory no longer matches original row {row['source_row']}")
    states = {r["state"]: r["state_po"] for r in result_raw}
    medsl_url = json.loads((results / "manifest.json").read_text())["sources"]["senate_returns.csv"]["url"]
    audits, changes, mapped, prepared_results, contests = [], [], [], [], {}

    def audit(kind, key, cid, status, reasons):
        audits.append({"record_type": kind, "record_key": key, "contest_id": cid,
                       "status": status, "reasons": reasons})

    def evidence(ref):
        return rounds["sources"][ref]["url"]

    groups = defaultdict(list)
    for row in result_raw:
        groups[result_contest(row)].append(row)
    # Explicit missing first round: the FEC table has FOUR candidates; the older
    # handoff's three-way description is inaccurate. FEC votes are not imported.
    groups["2018-MS-special-first"] = []
    for cid, rows in sorted(groups.items()):
        cycle, state, seat, round_name = cid.split("-")
        in_scope = cycle in {"2018", "2020"} or (cycle == "2024" and state == "TX")
        exception = rounds["exceptions"].get(cid)
        election_date = exception["date"] if exception else rounds["ordinary_dates"][cycle]
        date_ref = evidence(exception["reference_id"]) if exception else (evidence(f"fec_{cycle}.xlsx") if cycle != "2024" else "Decision 011 / Rahan-confirmed 2024-11-05")
        totals = {integer(r["totalvotes"]) for r in rows}
        if len(totals) > 1 or (rows and sum(integer(r["candidatevotes"]) for r in rows) != next(iter(totals))):
            raise ValueError(f"Unreconciled source total: {cid}")
        identity_sides = defaultdict(set)
        for r in rows:
            if r["candidate"]:
                side = party_side(r["party_detailed"])
                if side in {"D", "R"}:
                    identity_sides[norm(r["candidate"])].add(side)
        reasons, ballot, valid_counts = [], set(), []
        result_sides = set()
        for r in rows:
            name, label = r["candidate"], r["party_detailed"]
            canonical = norm(name) or f"UNNAMEDWRITEINS-{r['source_row']}"
            key = f"medsl:{r['source_row']}"
            flags = []
            if not label: flags.append("blank_detailed_party")
            if not r["party_simplified"]: flags.append("blank_simplified_party")
            vote_valid = "false" if canonical in NONCANDIDATE else "true"
            side, basis, url = party_side(label), "MEDSL detailed party label", medsl_url
            override = rounds["side_overrides"].get(f"{cycle}:{state}:{name}")
            fec_alias_row = rounds.get("result_fec_alias_rows", {}).get(f"{cycle}:{state}:{name}")
            reference_matches = [f for f in facts["candidates"] if f["cycle"] == cycle and f["state_po"] == state and f["special"] == (seat == "special") and (f["row"] == fec_alias_row if fec_alias_row is not None else norm(f["name"]) == canonical)]
            if override:
                side, basis, url = override["side"], override["basis"], evidence(override["reference_id"])
            elif len(identity_sides[canonical]) == 1:
                side = next(iter(identity_sides[canonical]))
                basis = "Same explicitly named candidate as major-party ballot line; Decision 013"
            elif len(identity_sides[canonical]) > 1:
                side, basis = "unknown", "Conflicting detailed-party labels on identical candidate name"
            elif not name or name in {"OTHERS", "WRITE-IN", "WRITE-INS"}:
                side, basis = "other", "Unidentified aggregate: valid votes retained without invented candidate identity"
                flags.append("unidentified_aggregate")
            elif vote_valid == "false":
                side, basis = "other", "Noncandidate ballot category; outside valid-vote denominator (Decision 013)"
            elif not label and len(reference_matches) == 1 and reference_matches[0]["party"] not in {"", "W"}:
                f = reference_matches[0]
                side, basis, url = party_side(f["party"]), f"Official FEC detailed party {f['party']}, row {f['row']}", f["url"]
            if canonical == "NONEOFTHESECANDIDATES":
                vote_valid = "pending"
                flags.append("ballot_option_denominator_pending")
            if side != party_side(label): flags.append("side_differs_detailed_party")
            if side != party_side(r["party_simplified"]): flags.append("side_differs_simplified_party")
            if side == "unknown" and vote_valid == "true": reasons.append("unresolved_result_party")
            if vote_valid == "pending": reasons.append("ballot_option_denominator_pending")
            if r["unofficial"].lower() == "true":
                reasons.append("unofficial_source_returns")
                flags.append("unofficial_source_returns")
            if integer(r["candidatevotes"]) == 1 and integer(r["totalvotes"]) == 1:
                reasons.append("uncontested_vote_sentinel")
            reference_vote, conflict_status = "", "not_crosschecked"
            if len(reference_matches) == 1:
                f = reference_matches[0]
                raw = f["runoff_votes_raw" if round_name == "runoff" else "general_votes_raw"]
                if raw.isdigit():
                    reference_vote = integer(raw)
                    conflict_status = "match" if reference_vote == integer(r["candidatevotes"]) else "conflict"
                    if conflict_status == "conflict":
                        flags.append("fec_vote_count_conflict")
                        resolved = rounds["resolved_reference_conflicts"].get(f"{cycle}:{state}:{name}")
                        if resolved and resolved["votes"] == integer(r["candidatevotes"]):
                            conflict_status = "state_confirms_medsl"
                        else:
                            reasons.append("reference_vote_count_conflict")
            if cid in rounds["first_choice_checks"] and name in rounds["first_choice_checks"][cid]["candidate_votes"]:
                if integer(r["candidatevotes"]) != rounds["first_choice_checks"][cid]["candidate_votes"][name]:
                    raise ValueError(f"First-choice reference no longer matches {cid}: {name}")
                conflict_status = "official_first_choice_match"
            if vote_valid == "true": valid_counts.append(integer(r["candidatevotes"]))
            if vote_valid == "true" and name and name != "OTHERS" and r["writein"].lower() != "true": ballot.add(canonical)
            if vote_valid == "true": result_sides.add(side)
            record = {**r, "record_key": key, "contest_id": cid, "cycle": cycle,
                      "election_date": election_date, "stage_normalized": r["stage"].lower(),
                      "mode_normalized": r["mode"].lower(), "votes": integer(r["candidatevotes"]),
                      "reported_total": integer(r["totalvotes"]), "canonical_candidate_id": f"{cid}:{canonical}",
                      "side": side, "side_basis": basis, "side_reference_url": url,
                      "valid_vote": vote_valid, "preparation_flags": ";".join(flags),
                      "fec_reference_votes": reference_vote, "reference_check": conflict_status}
            prepared_results.append(record)
            mapped.append({"record_key": key, "record_type": "result", "contest_id": cid,
                           "source_candidate_id": "", "source_row": r["source_row"],
                           "candidate": name, "source_party": label, "source_party_simplified": r["party_simplified"],
                           "canonical_candidate_id": record["canonical_candidate_id"], "side": side,
                           "basis": basis, "reference_url": url, "membership": "source_result_row",
                           "valid_vote": vote_valid, "flags": record["preparation_flags"]})
            for field, after, why in (("stage", record["stage_normalized"], "case normalization"), ("mode", record["mode_normalized"], "case normalization"), ("candidatevotes", record["votes"], "exact decimal-string to integer"), ("totalvotes", record["reported_total"], "exact decimal-string to integer"), ("side", side, basis), ("valid_vote", vote_valid, "Decision 013 valid-vote classification"), ("contest_id", cid, "Verified source-year/seat/round crosswalk"), ("election_date", election_date, date_ref)):
                changes.append({"record_key": key, "field": field, "before": r.get(field, ""), "after": after, "basis": why})
        if not rows: reasons.append("missing_first_round_results")
        if not {"D", "R"}.issubset(result_sides) and rows:
            reasons.append("missing_D_or_R_side" if "unknown" not in result_sides else "unresolved_result_sides")
        exclusions = not in_scope or ("missing_D_or_R_side" in reasons)
        status = "excluded" if exclusions else "pending" if reasons else "eligible"
        if not in_scope: reasons.insert(0, "outside_initial_calibration_scope")
        reasons = list(dict.fromkeys(reasons))
        contests[cid] = {"contest_id": cid, "state_po": state, "cycle": cycle, "seat": seat,
                         "round": round_name, "election_date": election_date,
                         "date_basis": exception["basis"] if exception else "Official general-election calendar; Texas 2024 date approved in Decision 011",
                         "date_reference": date_ref, "scope": "initial_calibration" if in_scope else "outside_scope",
                         "source_year": ";".join(sorted({r["year"] for r in rows})),
                         "result_rows": len(rows), "reported_total": next(iter(totals)) if totals else "",
                         "valid_vote_total": sum(valid_counts) if rows and "ballot_option_denominator_pending" not in reasons else "",
                         "noncandidate_votes": sum(integer(r["candidatevotes"]) for r in rows if norm(r["candidate"]) in NONCANDIDATE),
                         "ballot_candidate_ids_json": json.dumps(sorted(ballot)),
                         "status": status, "reasons": ";".join(reasons)}
        if status != "eligible": audit("contest", cid, cid, status, contests[cid]["reasons"])
    # First-round membership evidence is useful even though its returns are missing.
    first_slate = [f for f in facts["candidates"] if f["cycle"] == "2018" and f["state_po"] == "MS" and f["special"] and f["general_votes_raw"].isdigit()]
    contests["2018-MS-special-first"]["ballot_candidate_ids_json"] = json.dumps(sorted(norm(f["name"]) for f in first_slate))
    result_lookup = defaultdict(dict)
    for r in prepared_results:
        result_lookup[r["contest_id"]][norm(r["candidate"])] = r
    poll_candidates, questions = [], []
    qgroups = defaultdict(list)
    for index, raw in enumerate(poll_raw, 1):
        key = f"538:{raw['cycle']}:{raw['race_id']}:{raw['poll_id']}:{raw['question_id']}"
        qgroups[key].append((index, raw))
    for qkey, entries in qgroups.items():
        raw = entries[0][1]
        cid = poll_contest(raw, states)
        state = states[raw["state"].upper()]
        contest = contests.get(cid)
        metadata_fields = ("cycle", "race_id", "poll_id", "question_id", "state", "stage", "seat_name", "election_date", "population", "end_date", "internal", "partisan", "sample_size")
        inconsistent = [field for field in metadata_fields if len({r[field] for _, r in entries}) != 1]
        excluded, pending, flags, candidate_ids, sides = [], [], [], [], set()
        if inconsistent: pending.append("inconsistent_question_metadata"); flags.extend(inconsistent)
        if not raw["population"]: pending.append("missing_population")
        elif raw["population"].lower() != "lv": excluded.append("non_LV_population")
        if raw["internal"].lower() == "true" or raw["partisan"].strip() in {"DEM", "REP", "IND", "LIB", "REP,REF"}: excluded.append("partisan_or_internal")
        elif raw["internal"].lower() != "false" or raw["partisan"].strip(): pending.append("unknown_partisanship")
        if len({r["candidate_id"] for _, r in entries}) != len(entries):
            pending.append("duplicate_candidate_answer")
        if not contest: pending.append("unverified_round")
        elif contest["status"] != "eligible":
            (excluded if contest["status"] == "excluded" else pending).append("contest_" + contest["status"])
        if not raw["end_date"]: pending.append("missing_fieldwork_end")
        if contest and raw["election_date"] and date(raw["election_date"]) != contest["election_date"]: pending.append("election_date_conflict")
        if not raw["election_date"]: pending.append("missing_source_election_date")
        for field in ("sample_size", "population", "url"):
            if not raw[field]: flags.append("missing_" + field)
        for index, r in entries:
            a = aliases.get(f"{r['cycle']}:{r['candidate_id']}")
            if a and (a["state"] != r["state"] or norm(a["poll_name"]) != norm(r["candidate_name"])):
                raise ValueError(f"Candidate alias no longer matches its source identity: {qkey}")
            side, basis, url, membership, canonical = "unknown", "Unresolved identity", r["url"], "unknown", ""
            target = a["result_name"] if a else ""
            match = result_lookup[cid].get(norm(target)) if target else None
            if match and match["valid_vote"] == "true":
                side, basis, url = match["side"], a["basis"] + "; " + match["side_basis"], match["side_reference_url"]
                membership, canonical = "confirmed", match["canonical_candidate_id"]
            elif target:
                # Explicit identities that appear in another round of the same
                # seat can be confirmed absent from this round's named slate.
                other = [m for other_id, lookup in result_lookup.items() if other_id.rsplit("-", 1)[0] == cid.rsplit("-", 1)[0] for n, m in lookup.items() if n == norm(target)]
                if not contest:
                    # Identity is known, but the actual round/ballot is not.
                    if other:
                        side, basis, url = other[0]["side"], a["basis"] + "; round membership unresolved", other[0]["side_reference_url"]
                        canonical = f"{cid}:{norm(target)}"
                elif cid == "2018-MS-special-first":
                    f = next((f for f in first_slate if norm(f["name"]) == norm(target)), None)
                    if f:
                        membership, canonical = "confirmed", f"{cid}:{norm(target)}"
                        side = party_side(r["party"])
                        basis, url = "Explicit FEC first-round identity; source poll affiliation; returns still missing", f["url"]
                elif other:
                    membership = "confirmed_nonballot"
                    side, basis, url = other[0]["side"], a["basis"] + "; absent from actual round slate", other[0]["side_reference_url"]
                    canonical = f"{cid}:{norm(target)}"
                else:
                    refs = [f for f in facts["candidates"] if f["cycle"] == r["cycle"] and f["state_po"] == state and norm(f["name"]) == norm(target)]
                    if len(refs) == 1:
                        f = refs[0]
                        votes = f["runoff_votes_raw" if cid.endswith("runoff") else "general_votes_raw"]
                        if votes == "" or votes == "#":
                            membership, canonical = "confirmed_nonballot", f"{cid}:{norm(target)}"
                            side, basis, url = party_side(r["party"]), a["basis"] + "; FEC shows no votes in actual round", f["url"]
            elif a and a["status"] == "fec_identity":
                f = next(f for f in facts["candidates"] if f["reference_id"] == a["reference_id"] and f["row"] == a["fec_row"])
                rawvotes = f["runoff_votes_raw" if cid.endswith("runoff") else "general_votes_raw"]
                canonical, side, basis, url = f"{cid}:{norm(f['name'])}", party_side(f["party"]), a["basis"], f["url"]
                membership = "confirmed" if rawvotes.isdigit() else "confirmed_nonballot" if rawvotes == "" or rawvotes == "#" else "unknown"
            elif a and a["status"] == "texas_confirmed_nonballot":
                membership, side, basis = "confirmed_nonballot", party_side(r["party"]), a["basis"]
            if r["ranked_choice_reallocated"].lower() == "true": excluded.append("RCV_reallocated_question")
            if membership == "confirmed_nonballot": excluded.append("confirmed_nonballot_candidate")
            if membership == "unknown": pending.append("unresolved_poll_identity")
            if side == "unknown": pending.append("unresolved_poll_side")
            if membership == "confirmed":
                candidate_ids.append(canonical.split(":", 1)[1]); sides.add(side)
            if not r["pct"]: pending.append("missing_candidate_percentage")
            else:
                pct = Decimal(r["pct"])
                if not pct.is_finite() or not 0 <= pct <= 100: raise ValueError(f"Invalid percentage: {qkey}")
            rowflags = []
            if not r["party"]: rowflags.append("blank_source_party")
            if side != party_side(r["party"]): rowflags.append("side_differs_source_party")
            pkey = f"538-row:{index}"
            candidate = {**r, "record_key": pkey, "source_row": index, "question_key": qkey,
                         "contest_id": cid if contest else "", "mapped_round_id": cid,
                         "canonical_candidate_id": canonical, "side": side, "side_basis": basis,
                         "membership": membership, "mapping_reference_url": url, "mapping_flags": ";".join(rowflags)}
            poll_candidates.append(candidate)
            mapped.append({"record_key": pkey, "record_type": "poll", "contest_id": cid if contest else "",
                           "source_candidate_id": r["candidate_id"], "source_row": index, "candidate": r["candidate_name"],
                           "source_party": r["party"], "source_party_simplified": "", "canonical_candidate_id": canonical,
                           "side": side, "basis": basis, "reference_url": url, "membership": membership,
                           "valid_vote": "", "flags": ";".join(rowflags)})
        if not {"D", "R"}.issubset(sides): pending.append("question_missing_D_or_R_side")
        slate = set(json.loads(contest["ballot_candidate_ids_json"])) if contest else set()
        full = bool(slate) and set(candidate_ids) == slate and len(candidate_ids) == len(entries)
        reasons = list(dict.fromkeys(excluded + pending))
        status = "excluded" if excluded else "pending" if pending else "eligible"
        questions.append({"question_key": qkey, "source": "538_archive", "cycle": raw["cycle"], "state_po": state,
                          "race_id": raw["race_id"], "poll_id": raw["poll_id"], "question_id": raw["question_id"],
                          "poll_key": raw["poll_id"], "contest_id": cid if contest else "", "mapped_round_id": cid,
                          "source_stage": raw["stage"], "source_seat_name": raw["seat_name"], "source_seat_number": raw["seat_number"],
                          "source_election_date": raw["election_date"], "election_date": contest["election_date"] if contest else "",
                          "start_date": date(raw["start_date"]), "end_date": date(raw["end_date"]), "population": raw["population"].upper(),
                          "population_raw": raw["population"], "population_full": raw["population_full"], "sample_size": raw["sample_size"],
                          "pollster": raw["pollster"], "internal_raw": raw["internal"], "partisan_raw": raw["partisan"],
                          "partisanship_basis": "Source flags; not independent nonpartisan verification", "url": raw["url"],
                          "candidate_rows": len(entries), "candidate_answers_json": json.dumps([{k: r[k] for k in ("candidate_id", "candidate_name", "party", "answer", "pct")} for _, r in entries]),
                          "full_ballot": str(full).lower(), "status": status, "reasons": ";".join(reasons),
                          "preference_basis": "", "flags": ";".join(flags)})
    for r in texas_raw:
        cid, key = "2024-TX-ordinary-general", f"ut2024:{r['source_rows']}"
        reasons = [] if r["population"] == "LV" else ["non_LV_population"]
        if not r["end_date"]: reasons.append("missing_fieldwork_end")
        status = "excluded" if "non_LV_population" in reasons else "pending" if reasons else "eligible"
        for side, name_col, pct_col in (("D", "dem_candidate", "dem_pct"), ("R", "rep_candidate", "rep_pct")):
            m = result_lookup[cid].get(norm(r[name_col]))
            if m is None or m["side"] != side: raise ValueError("Texas 2024 candidate identity mismatch")
            pkey = key + ":" + side
            candidate = {"record_key": pkey, "source_row": r["source_rows"], "question_key": key, "cycle": "2024", "state": "Texas",
                         "candidate_name": r[name_col], "pct": r[pct_col], "contest_id": cid, "mapped_round_id": cid,
                         "canonical_candidate_id": m["canonical_candidate_id"], "side": side,
                         "side_basis": "Exact Texas tracker/result name; MEDSL detailed party", "membership": "confirmed",
                         "mapping_reference_url": medsl_url, "mapping_flags": "", "tracker_original_json": json.dumps(r, sort_keys=True)}
            poll_candidates.append(candidate)
            mapped.append({"record_key": pkey, "record_type": "poll", "contest_id": cid, "source_candidate_id": "",
                           "source_row": r["source_rows"], "candidate": r[name_col], "source_party": "", "source_party_simplified": "",
                           "canonical_candidate_id": m["canonical_candidate_id"], "side": side, "basis": candidate["side_basis"],
                           "reference_url": medsl_url, "membership": "confirmed", "valid_vote": "", "flags": "blank_source_party;Texas_tracker_party_not_supplied"})
        questions.append({"question_key": key, "source": r["source"], "cycle": "2024", "state_po": "TX", "race_id": "", "poll_id": "", "question_id": "",
                          "poll_key": key, "contest_id": cid, "mapped_round_id": cid, "source_stage": "", "source_seat_name": "", "source_seat_number": "",
                          "source_election_date": r["election_date"], "election_date": r["election_date"], "start_date": r["start_date"], "end_date": r["end_date"],
                          "population": r["population"], "population_raw": r["population_raw"], "population_full": r["population_full"], "sample_size": r["sample_size"],
                          "pollster": r["poll_label"], "internal_raw": r["internal"], "partisan_raw": r["partisan"],
                          "partisanship_basis": "UT tracker source exception (Decision 012); source partisanship remains unknown",
                          "url": r["release_url"], "candidate_rows": 2, "candidate_answers_json": json.dumps({r["dem_candidate"]: r["dem_pct"], r["rep_candidate"]: r["rep_pct"]}),
                          "full_ballot": "unknown", "status": status, "reasons": ";".join(reasons), "preference_basis": "", "flags": r["flags"]})
    choose_questions(questions)
    # A pending sibling can change the approved full-ballot choice. Hold a
    # selected question until that sibling is resolved; don't silently drop it.
    siblings = defaultdict(list)
    for q in questions: siblings[(q["source"], q["poll_key"], q["mapped_round_id"])].append(q)
    for group in siblings.values():
        if any(q["status"] == "pending" for q in group):
            for q in group:
                if q["status"] == "selected": q.update(status="pending", reasons="pending_sibling_question", preference_basis="Resolve other LV question from this poll/round before choosing")
    question_status = {q["question_key"]: q["status"] for q in questions}
    # Preserve original row order in the long inventories as well as their keys.
    prepared_results.sort(key=lambda r: int(r["source_row"]))
    poll_candidates.sort(key=lambda r: (0 if r["record_key"].startswith("538-row:") else 1, int(r["source_row"]), r["record_key"]))
    for row in poll_candidates:
        row["question_status"] = question_status[row["question_key"]]
    for row in prepared_results:
        row["contest_status"] = contests[row["contest_id"]]["status"]
    inventory = []
    for cid, c in sorted(contests.items()):
        qs = [q for q in questions if q["contest_id"] == cid]
        counts = Counter(q["status"] for q in qs)
        inventory.append({"contest_id": cid, "cycle": c["cycle"], "state_po": c["state_po"], "contest_status": c["status"],
                          "questions": len(qs), "selected_questions": counts["selected"], "excluded_questions": counts["excluded"], "pending_questions": counts["pending"],
                          "unpolled_in_archive": str(not qs).lower(), "horizon_drop_status": "Rahan computes after horizon cutoff"})
    for q in questions:
        if q["status"] != "selected": audit("question", q["question_key"], q["contest_id"], q["status"], q["reasons"])
        original = qgroups[q["question_key"]][0][1] if q["source"] == "538_archive" else next(r for r in texas_raw if f"ut2024:{r['source_rows']}" == q["question_key"])
        for field in ("start_date", "end_date", "population", "election_date"):
            changes.append({"record_key": q["question_key"], "field": field, "before": original[field], "after": q[field],
                            "basis": "Source date/population formatting or exact contest-date crosswalk; original fields retained"})
        changes.append({"record_key": q["question_key"], "field": "selection_status", "before": "", "after": q["status"],
                        "basis": q["reasons"] or q["preference_basis"]})
    for m in mapped:
        if m["side"] == "unknown" or m["membership"] == "unknown": audit("candidate_mapping", m["record_key"], m["contest_id"], "pending", "unresolved_identity_or_side")
        if m["record_type"] == "poll":
            changes.append({"record_key": m["record_key"], "field": "side", "before": m["source_party"], "after": m["side"], "basis": m["basis"]})
    race_groups = defaultdict(list)
    for q in questions:
        if q["race_id"]: race_groups[(q["cycle"], q["race_id"])].append(q)
    race_crosswalk = []
    for (cycle, rid), qs in sorted(race_groups.items()):
        ids = {q["contest_id"] for q in qs}
        if len(ids) != 1: raise ValueError("One archive race ID maps to conflicting rounds")
        q = qs[0]
        race_crosswalk.append({"cycle": cycle, "race_id": rid, "state_po": q["state_po"], "source_stage": q["source_stage"],
                               "source_seat_name": q["source_seat_name"], "source_seat_number": q["source_seat_number"],
                               "contest_id": q["contest_id"], "mapped_round_id": q["mapped_round_id"], "election_date": q["election_date"],
                               "status": "mapped" if q["contest_id"] else "pending", "basis": "Explicit exceptional seat/round crosswalk plus official date registry"})
    files = {"candidate_results.csv": prepared_results, "contests.csv": list(contests.values()),
             "candidate_side_map.csv": mapped, "poll_candidate_rows.csv": poll_candidates,
             "poll_questions.csv": questions, "crosswalk.csv": [{k: q[k] for k in ("question_key", "source", "cycle", "state_po", "race_id", "poll_id", "question_id", "contest_id", "mapped_round_id", "election_date", "full_ballot", "status", "reasons", "preference_basis")} for q in questions],
             "race_crosswalk.csv": race_crosswalk, "race_inventory.csv": inventory,
             "excluded.csv": [a for a in audits if a["status"] == "excluded"],
             "pending.csv": [a for a in audits if a["status"] == "pending"], "changes.csv": changes}
    output.mkdir(parents=True)
    for name, rows in files.items(): write_csv(output / name, rows, ("record_type", "record_key", "contest_id", "status", "reasons"))
    def portable(path):
        try: return str(Path(path).relative_to(ROOT))
        except ValueError: return str(path)
    manifest = {"schema_version": 1, "rule_version": "Decisions 011–014 / calibration-preparation-v1",
                "authorization": "Rahan: go (2026-10-06), latest Claude mapping/crosswalk handoff",
                "created_at": created_at or datetime.now(timezone.utc).isoformat(),
                "inputs_sha256": {portable(k): v for k, v in inputs.items()},
                "reference_sources": rounds["sources"],
                "source_provenance": {"polls": json.loads((polls / "manifest.json").read_text()), "results": json.loads((results / "manifest.json").read_text()), "texas": json.loads((texas / "manifest.json").read_text())},
                "counts": {"result_rows": len(result_raw), "archive_candidate_rows": len(poll_raw), "tracker_candidate_rows": 2 * len(texas_raw), "candidate_mapping_rows": len(mapped), "questions": len(questions), "contests": len(contests), "race_crosswalks": len(race_crosswalk),
                           "question_status": dict(Counter(q["status"] for q in questions)), "contest_status": dict(Counter(c["status"] for c in contests.values())),
                           "by_cycle": {y: dict(Counter(q["status"] for q in questions if q["cycle"] == y)) for y in ("2018", "2020", "2024")}},
                "audit_counts": {"question_reasons": dict(Counter(reason for q in questions for reason in q["reasons"].split(";") if reason)),
                                 "candidate_membership": dict(Counter(m["membership"] for m in mapped)),
                                 "candidate_sides": dict(Counter(m["side"] for m in mapped)),
                                 "candidate_flags": dict(Counter(flag for m in mapped for flag in m["flags"].split(";") if flag)),
                                 "result_valid_vote": dict(Counter(r["valid_vote"] for r in prepared_results)),
                                 "LV_questions": sum(q["population"] == "LV" for q in questions),
                                 "full_ballot_questions": sum(q["full_ballot"] == "true" for q in questions)},
                "outputs": {name: {"rows": len(rows), "sha256": sha(output / name)} for name, rows in files.items()},
                "limitations": ["No margins, D/R vote sums, weighting, horizon cutoffs, errors, RMSE or probabilities calculated",
                                "Official comparisons are partial: exact reference-name matches only; not every primary release or candidate vote crosschecked",
                                "Missing MS 2018 first-round returns, unofficial source returns, unresolved parties/identities, denominator ambiguity and reference conflicts remain pending",
                                "LA 2020 apparent runoff is unverified and has no registered contest/date",
                                "One observation per archive poll/round; tied questions and pending siblings held for review; tracker rows remain separate observations under Decision 009",
                                "Full ballot means all named, non-write-in source-result candidates, not every possible write-in; no primary questionnaire verification",
                                "2024 outside Texas retained as excluded source inventory, not expanded calibration scope",
                                "Valid-vote totals are mechanical counts only; do not use reported totals when they include invalid categories"]}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    for path, checksum in inputs.items():
        if sha(Path(path)) != checksum: raise ValueError(f"Input changed during preparation: {path}")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--poll-snapshot", type=Path, default=POLL_SNAPSHOT)
    parser.add_argument("--result-snapshot", type=Path, default=RESULT_SNAPSHOT)
    parser.add_argument("--texas-snapshot", type=Path, default=TEXAS_SNAPSHOT)
    parser.add_argument("--references", type=Path, default=REFERENCES)
    parser.add_argument("--output", type=Path, default=ROOT / "data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1")
    parser.add_argument("--created-at", help="Fixed UTC ISO time for byte-identical replay")
    args = parser.parse_args()
    manifest = prepare(args.poll_snapshot, args.result_snapshot, args.texas_snapshot, args.references, args.output, args.created_at)
    print(json.dumps(manifest["counts"], indent=2))


if __name__ == "__main__":
    main()
