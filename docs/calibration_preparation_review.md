# Calibration preparation review — 2026-10-06

Rahan's “go” authorized the latest Claude mapping/crosswalk handoff. The offline preparer and [processed snapshot](../data/processed/senate_calibration/README.md) implement Decisions 011–014, preserve all inputs, and hold ambiguities for review. No margins, D/R vote sums, weighting, errors, RMSE, σ or probabilities are calculated.

## Observed coverage and filters

All 508 MEDSL rows, 4,593 archive candidate answers, 37 tracker records and 1,950 questions are represented. The side map contains 5,175 rows. The registry contains 108 rounds: 74 in scope and 34 excluded outside-scope 2024 rounds. In-scope status: 56 eligible, two excluded, 16 pending. Selected questions span 52 eligible rounds.

| Cycle | Input questions | Selected | Excluded | Pending |
| --- | ---: | ---: | ---: | ---: |
| 2018 | 879 | 333 | 408 | 138 |
| 2020 | 1,034 | 373 | 451 | 210 |
| Texas 2024 | 37 | 23 | 14 | 0 |
| Total | 1,950 | 729 | 873 | 348 |

There are 1,433 LV questions. Flags/reasons overlap: 509 known non-LV questions, 381 source-partisan/internal questions, 109 confirmed non-ballot questions, one RCV-reallocated question, 11 alternative questions displaced by a unique full-ballot question. The 109 include exactly the previously approved 12 Texas 2020 hypotheticals. Missing population stays unknown; three otherwise-unexcluded questions remain pending for it.

Of the 348 pending questions, 243 have pending contests, 91 have tied/ambiguous LV question preferences, and two otherwise-selectable questions have pending siblings. Identity/side and missing-population issues overlap these counts. Logs preserve all reasons; no highest-ID, largest-sample, or arbitrary tied-question choice is implemented. Louisiana race 7787 remains unmapped even though its question is independently excluded by a partisan flag.

## Identities, sides and round evidence

- Decision 013 explicitly places King and Sanders on the D side and Ringelstein on other. The [Senate party-division history](https://www.senate.gov/history/partydiv.htm) supplies caucus context; the side overrides retain their original source affiliations.
- Al Gross is mapped as the Democratic nominee, rather than a caucusing-incumbent exception. The [2020 FEC workbook](https://www.fec.gov/documents/4228/federalelections2020.xlsx), Senate sheet row 17, labels him `N(D)/D` and explains the nonpartisan Democratic-primary arrangement.
- [Wyoming's official summary](https://sos.wyo.gov/Elections/Docs/2020/Results/General/2020_General_Statewide_Candidates_Summary.pdf), page 2, confirms Lummis R and Ben-David D where MEDSL detailed labels are blank. It agrees with MEDSL's 72,766 Ben-David votes; FEC lists 73,766. The conflict is logged as state-confirmed MEDSL, with no replacement.
- Identical named candidates on multiple party lines retain every row and share a canonical identity/side. This includes New York 2018 and Connecticut Murphy lines. Canonical IDs are round-specific; separate rounds stay separate observations.
- Mississippi's MEDSL special `gen` rows are mapped to **November 27, 2018 runoff**. [FEC 2018](https://www.fec.gov/documents/2706/federalelections2018.xlsx), rows 248–251 and candidate notes, confirms November 6 had **four** candidates: Hyde-Smith, Espy, McDaniel, Bartee. This corrects the prior handoff's three-way description. First-round membership is referenced, but FEC votes are not imported; missing MEDSL first-round returns remain pending.
- Georgia source-year 2021 runoffs map to cycle 2020, January 5, 2021. Ordinary and special seats and their November first rounds remain distinct. [FEC 2020](https://www.fec.gov/documents/4228/federalelections2020.xlsx), rows 84/92 and 97/98, explicitly supplies runoff dates and counts.
- Louisiana's apparent 2020 runoff has no verified date/actual round. No registry outcome is invented and no November result is substituted.

Every blank source party and side disagreement is flagged. Result detailed labels are blank on 71 rows; 59 result sides differ from detailed labels and 34 from simplified labels. There are 61 poll-side disagreements with source affiliations, plus 74 tracker shares with no supplied party label. None of these flags alter raw labels. Sixty-three mappings retain `unknown` sides; 39 poll answers retain unknown membership.

## Valid votes and first choice

Fourteen noncandidate rows are retained but marked `valid_vote=false`, including additional 2024 UNDER/OVER/VOID/SPOILED categories absent from the earlier spaced-label audit. All valid candidate/write-in votes remain in mechanical totals. No D/R totals or vote shares are calculated.

| Contest | Noncandidate votes excluded from denominator |
| --- | ---: |
| Iowa 2020 | 28,302 |
| Maine 2020 | 9,122 |
| Massachusetts 2020 | 93,869 |
| Wyoming 2020 | 6,566 |

[Maine's official 2020 Senate workbook](https://www.maine.gov/sos/sites/maine.gov.sos/files/content/assets/ussenator1120.xlsx), `US Senator` row 554, matches all four MEDSL named candidate counts, 228 other/write-in votes, and 9,122 blank ballots. Its valid-vote total is 819,183. These are initial candidate selections. Maine 2018 candidate counts agree with the FEC table and King has an outright first-choice majority, so a later elimination round is unnecessary. The archive's one explicitly reallocated question is excluded. A false archive reallocation flag does not independently verify a primary poll release.

Nevada's “None of These Candidates” is an actual ballot option, not an under/over vote. Decision 013 does not explicitly settle its denominator treatment: it remains pending and Nevada's valid-vote total is blank. No other independent is added to the Democratic-side exception list.

## Pending contests and remaining review

| Contest(s) | Why held |
| --- | --- |
| Mississippi 2018 special first round | Missing main-source returns; approve an official supplemental collection or an explicit exclusion. |
| Nevada 2018 | Ballot-option denominator treatment unresolved. |
| Ohio 2018; Vermont 2018; New Jersey 2020 | MEDSL/FEC vote-count disagreements. |
| West Virginia 2018; both Georgia 2020-cycle runoffs | Unofficial source flag plus FEC vote disagreements. |
| South Dakota 2020 | Unofficial source flag. |
| Illinois, Kentucky, Massachusetts, Michigan, Nebraska, Tennessee, Texas 2020 | Named candidate/write-in detailed parties missing or unconfirmed. No affiliation imputed. |

Fifteen result rows have FEC count conflicts, including the resolved Wyoming discrepancy. Comparing exact names misses some middle-name variants; the explicit Sanders/Zupan/King FEC aliases add inspected comparisons. This is a partial crosscheck, not verification of every result. MEDSL counts remain unchanged, and unresolved discrepancies hold the entire contest. The logs identify source rows and original/reference values.

Named blank-party cases include Ricardo Turullols-Bonilla in Texas, Shiva Ayyadurai in Massachusetts, Preston Love Jr. in Nebraska and named write-ins elsewhere. A generic FEC `W` label establishes write-in status, not Democratic/Republican affiliation, so it does not resolve their side. Outside-scope 2024 blank parties are also retained without inference.

The primary polling releases, archive mirror identity, complete ballot slates and every certification flag have not been independently verified. The implemented full-ballot preference uses named non-write-in result slates, with exact aliases and explicit non-ballot evidence. Remaining ambiguities stay pending. Rahan must create horizon-specific no-poll logs, not use registry counts as the calibration sample size.

## Reproducibility and checks

Nine new regression tests cover full source-field preservation, side overrides/fusion lines, exact rounds/missing returns, valid-vote categories, first-choice exclusion, non-ballot filters, unique observations/ties, deterministic replay, tamper rejection and overwrite protection. All 20 repository tests passed. Final replay verifies byte-identical output using the recorded processing timestamp.

The 47 pre-existing raw/prepared data files in the initial preservation baseline are unchanged. Rahan edited/committed the notebook during this task; Codex did not edit or execute it. Tests preserve the notebook's current bytes. Factual references record actual URLs/retrieval times/hashes in [reference JSON](../src/clean/calibration_references/README.md); whole downloaded reference documents stay in the ignored local cache. The output manifest preserves source attribution and license/permission receipts.

[The handoff](handoffs/2026-10-06-codex-to-rahan-and-claude-calibration.md) records the concrete files, observed checks and next steps. No new methodology decision is recorded by this preparation.
