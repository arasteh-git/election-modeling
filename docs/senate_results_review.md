# MEDSL results collection review

Collected 2026-10-05 America/New_York under Decision 014. Snapshot: `data/raw/senate_results/20261006T035630Z/`. Source: MIT Election Data and Science Lab, U.S. Senate statewide returns, DOI `10.7910/DVN/PEJ5QU`, V8.0, CC0 1.0. This is a mechanical audit, not an approved calibration dataset.

## Observed coverage

Full unchanged CSV: 3,945 rows. Inventoried source years: 2018 (152 rows/35 groups), 2020 (204/35), 2024 (148/35), plus Georgia 2021 runoffs (4/2). Grouping preserves source year, stage, ordinary/special status, and mode. It does not assign Senate classes, election dates, polling race IDs, or election-cycle IDs.

All 107 source-group vote sums equal the reported total, including every ballot line and other source category. No rows were removed, names edited, candidates combined, percentages computed, or totals redefined. The original CSV size matches metadata (530,501 bytes); codebook MD5 matches; all files have SHA-256 receipts. Dataverse's main-file MD5 describes the hosted tabular representation and was not compared with the original CSV. CSV SHA-256: `6f745db1b4a0026ad837e74428f9ed6f3f77fa51eb6f858b58ebdbc186fdb3bd`.

## Findings

| Finding | Affected records | Handling / limit |
| --- | --- | --- |
| Unofficial flags | 19 rows in eight groups: WV 2018 (3); SD 2020 (2); GA 2021 ordinary/special (4); AZ 2024 (3); CA 2024 special (2); NE 2024 special (2); WA 2024 (3). | Flags preserved; current certification not independently checked. |
| Noncandidate categories | IA 2020 OVER VOTES 864 / UNDER VOTES 27,438; ME 2020 BLANK VOTES 9,122; MA 2020 BLANK VOTES 93,869; WY 2020 OVER VOTES 165 / UNDER VOTES 6,401. | Six rows retained. Reported totals include these rows; using `totalvotes` blindly would differ from a valid-candidate-vote denominator. |
| Blank names | 30 rows. | Retain votes/write-in fields; flag missing identity. |
| Repeated names | 11 rows across CT 2018, NY 2018, CT 2024. | Preserve party lines; no automatic aggregation. |
| Georgia runoffs | Four 2021 rows, separate ordinary/special groups. | Supplemental file; year not relabeled as 2020 and no November-result join. |
| Mississippi 2018 special | Only Hyde-Smith and Espy rows under `gen`; no separate multicandidate first-round group. | Verify actual round and missing first-round coverage before matching jungle polls. |
| RCV | Maine 2018/2020 round definitions not established by stage or codebook. | Decision 013 requires first-choice numbers; official verification remains. |
| Missing election dates | All 107 groups. | Explicit flags; no dates inferred. |
| Old supporting documentation | Codebook body describes 1976–2018; source list appears focused on 2020. | Originals retained; not certification proof for later cycles. |

Two rows retain trailing candidate whitespace. All inventoried votes parse as nonnegative integers; no sentinel total of 1 or sum mismatch occurs. The collector also flags invalid/missing votes and sentinels if encountered later.

## Texas source values

| Year | Candidate | Votes | Reported total |
| --- | --- | ---: | ---: |
| 2018 | BETO O'ROURKE | 4,045,632 | 8,371,655 |
| 2018 | TED CRUZ | 4,260,553 | 8,371,655 |
| 2020 | MARY "MJ" HEGAR | 4,888,764 | 11,144,040 |
| 2020 | JOHN CORNYN | 5,962,983 | 11,144,040 |
| 2024 | COLIN ALLRED | 5,031,249 | 11,291,854 |
| 2024 | TED CRUZ | 5,990,741 | 11,291,854 |

Other candidates/rows remain available. These are publisher values, not independently verified Texas returns. Decision 013 approves all valid votes including third-party/write-in votes as the denominator; verification is needed where the reported total includes noncandidate categories. Actual margins have not been computed.

## Checks observed

Live public API retrieval succeeded. Version/DOI/publication state, unrestricted metadata, CC0, original sizes and codebook MD5 validated. Six regression tests passed: exact row/field preservation; separate year/round/special groups; retained anomaly flags; byte-identical offline replay and overwrite refusal; tampered-source rejection; schema/version/identity/license/restriction/checksum rejection. Existing polling snapshots and notebook preservation are checked by hashes in the handoff. No official crosschecks or modeling calculations ran.

## Next preparation

Decisions 012/013 settle horizons/RMSE, Democratic-side independents, same-party/no-side exclusions, sum-by-side comparisons, first-choice RCV, specials/runoffs matched by round, separate outcomes per round, all-valid-vote denominators, LIB/`REP,REF` partisan classifications, confirmed non-ballot candidate exclusions, and one observation per poll/round with full-ballot LV questions preferred. These supersede the plan's earlier open versions of the choices.

Remaining preparation work is factual verification: actual election dates, unofficial flags, ballot-line identities, first-choice returns, missing round coverage and poll/result crosswalks. Unknown metadata, uncertain identities and tied/ambiguous question preferences remain pending rather than silently resolved. National preparation and Rahan's core model remain future work.
