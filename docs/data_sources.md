# Data sources

## Approved current polling sources

Rahan approved starting with the [Texas 2026 U.S. Senate Poll Tracker](https://texaspolitics.utexas.edu/blog/texas-2026-u-s-senate-poll-tracker) on 2026-09-29.
Author: Texas Politics Project. Publisher: Texas Politics Project at the University of Texas at Austin.

Approval is for collection, not automatic inclusion of every row in the model. This source describes its coverage as nonpartisan public polling since the Republican primary concluded in May. It is not an exhaustive census of all public polls.

## Approved historical polling sources

Historical sources remain subject to source review for calibration. Rahan requested collection on 2026-10-05 and subsequently approved the specific corrections and hypothetical-matchup exclusion in Decision 011:

- 2018 and 2020: preserved FiveThirtyEight Senate candidate-row file in `khristel26/Senate`, pinned to commit `d3d0c6be4e35945e59c1cb574b4050ca1787a2bc`. [Archive file](https://raw.githubusercontent.com/khristel26/Senate/d3d0c6be4e35945e59c1cb574b4050ca1787a2bc/senate_polls_historical.csv). Mirror identity is not independently verified against original bytes. Original [publisher polling documentation](https://github.com/fivethirtyeight/data/blob/master/polls/README.md) links to CSV endpoints that now return ABC webpages.
- 2024: [Texas Politics Project tracker](https://texaspolitics.utexas.edu/blog/texas-2024-us-senate-poll-tracker), author/publisher Texas Politics Project at UT Austin, last updated October 30, 2024; may omit later polls.

Snapshot: `data/raw/texas_senate_historical/20261006T024116Z/`. The manifest records each source's URL, retrieval time, SHA-256, transformations, and limits. Run `python src/ingest/texas_senate_historical.py`; replay instructions and all file descriptions are in [the historical inventory README](../data/raw/texas_senate_historical/README.md). No population, quality, partisan, or hypothetical-matchup exclusions were applied to the requested source scope.

FiveThirtyEight's [repository](https://github.com/fivethirtyeight/data) states CC BY 4.0 for datasets unless otherwise noted; publisher README copies are saved. Attribution: FiveThirtyEight / ABC News, with preservation credit to the mirror. The 2024 UT page includes the same attributed republication guidelines described below; its HTML is unchanged and CSVs are labeled mechanical derivatives. No linked reports have been downloaded.

The approved derived inventory is under `data/processed/texas_senate_historical/20261006T024116Z/`. It fills the 2024 election date from Rahan's confirmation, tags 2018/2020 partisanship from archived `partisan` and `internal` fields, and removes the 12 hypothetical 2020 matchups from the active CSVs. Original inputs stay unchanged. See [the processed README](../data/processed/texas_senate_historical/README.md) for outputs, audits, hashes, and limitations. `not_flagged_partisan` describes the archive's flags; `unknown` applies where metadata is absent, including all 2024 rows. Primary-release partisanship verification remains incomplete; the separate results snapshot is described below.

## Approved 2022/2024 polling expansion (Decision 017)

Rahan approved the two dated polling archives, all-state 2022/2024 calibration expansion and MEDSL V8.0 use for 2022 on 2026-10-08. Collection and mechanical preparation under existing rules are authorized. Preserve the Texas 2024 tracker source and retain overlapping 538 Texas questions only for inventory. This supersedes the pending-approval language in the original proposal; no ambiguous independent-side or duplicate rule has been approved.

Rahan authorized source-proposal research on 2026-10-08. [The proposal](polling_sources_2022_2024_proposal.md) recommends dated Internet Archive captures of FiveThirtyEight's historical Senate CSV: [2023-04-27 for 2022](https://web.archive.org/web/20230427025758id_/https://projects.fivethirtyeight.com/polls-page/data/senate_polls_historical.csv) and [2025-01-18 for 2024](https://web.archive.org/web/20250118200335id_/https://projects.fivethirtyeight.com/polls-page/data/senate_polls_historical.csv). Both returned CSV headers with required fields and the intended cycle in bounded prefixes. [Receipts](polling_source_checks_2022_2024.json) record actual inspection times and limits. Full-cycle poll counts and all-state polling coverage remain unverified; no complete new polling file was collected.

Approved redistribution basis is FiveThirtyEight's CC BY 4.0 dataset notice, with publisher/archive attribution, license links and transformation notices. The proposal documents alternative-source limits and the exact-round/independent/RCV questions to review during preparation. Preserve the existing Texas 2024 tracker source and audit overlap rather than appending duplicate 538 observations.

`src/ingest/senate_poll_archives.py` implements the approved collector and offline replay. Actual collection attempts failed to connect to both archive captures; [attempt receipts](senate_archive_collection_attempts_2026_10_08.json) record the failures and successful pinned GitHub documentation checks. No complete new polling snapshot or expanded calibration output exists yet. See [collector commands and limits](../data/raw/senate_poll_archives/README.md). Retrying the approved URLs needs no new source approval.

The [2022 MEDSL inventory](../data/processed/senate_results_2022/README.md) is complete offline: 168 unchanged source rows, 36 stage/special/mode groups, 33 states. All group row sums match reported totals. Georgia's general and runoff rows remain separate; missing parties and unofficial returns remain unresolved. This is an inventory, not prepared calibration input.

## Approved election-result sources

Decision 017 extends the following MEDSL V8.0 source approval to 2022. The original Decision 014 collection and snapshots described below remain unchanged; 2022 is inventoried separately from those preserved bytes.

Rahan approved the proposed MEDSL Senate returns source for **2018, 2020, and 2024** in this Codex session on 2026-10-05 (Decision 014). Use the versioned V8.0 download described below; preserve the full source and inventory all three requested years. The initial polling calibration still covers all 2018/2020 races plus Texas 2024 (Decision 012); collecting all-state 2024 returns does not expand the approved polling sample.

Approval covers results collection and mechanical coverage auditing; Decision 013 and its additions separately approve analytical preparation. Rahan's 2026-10-06 “go” authorized the mapping/crosswalk handoff and factual reference checks. Official references below are used for facts, not imported replacement returns; their access and redistribution limits remain applicable.

## Approved main source and proposed official crosschecks

Approved main source: **MIT Election Data and Science Lab, U.S. Senate statewide 1976–2024**, [Harvard Dataverse DOI 10.7910/DVN/PEJ5QU](https://doi.org/10.7910/DVN/PEJ5QU), published version **8.0**, released `2026-05-11T16:13:52Z`. Public API metadata identifies unrestricted file `13887039` (`1976-2024-senate-state.tab`, original CSV `1976-2024-senate-state.csv`) and [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Original-CSV download: `https://dataverse.harvard.edu/api/access/datafile/13887039?format=original`. Collector metadata is explicitly pinned to `https://dataverse.harvard.edu/api/datasets/3072248/versions/8.0`.

Use this consistent main source for 2018/2020 and Texas 2024; use [FEC 2018](https://www.fec.gov/introduction-campaign-finance/election-results-and-voting-information/federal-elections-2018/) / [2020](https://www.fec.gov/introduction-campaign-finance/election-results-and-voting-information/federal-elections-2020/), [House Clerk election statistics](https://history.house.gov/Institution/Election-Statistics/) (including a listed 2024 PDF), and [Texas SOS](https://www.sos.state.tx.us/elections/historical/elections-results-archive.shtml) as official crosschecks. FEC/Clerk federal compilations are generally federal works; no explicit dataset license was found. Texas-source redistribution permission remains unestablished. These are not additional approved collection sources.

Collected snapshot: `data/raw/senate_results/20261006T035630Z/`. Original CSV SHA-256: `6f745db1b4a0026ad837e74428f9ed6f3f77fa51eb6f858b58ebdbc186fdb3bd`. The manifest records unchanged source bytes, per-file URLs/retrieval times/hashes, V8.0 metadata, codebook and source listing, attribution, CC0 and transformations. Inventoried rows: 152/204/148 for 2018/2020/2024 plus four separately labeled Georgia 2021 runoff rows. The initial calibration scope remains Decision 012's scope.

The collector audited schema, arithmetic coverage, flags and receipts. A separate 2026-10-06 preparer now supplies side/round/date mappings, valid-vote categories and approved question filtering. FEC 2018/2020 Senate workbook schemas and selected official state references were inspected; checks are partial, with disagreements and uncertain cases pending. [The preparation review](calibration_preparation_review.md) records exact evidence and limitations. [The results README](../data/raw/senate_results/README.md) documents original collection; [the prepared README](../data/processed/senate_calibration/README.md) documents the derived workflow.

Factual reference receipts and excerpt/alias files are under [src/clean/calibration_references/](../src/clean/calibration_references/README.md). Downloads remain in ignored `outputs/calibration_reference_research/`; whole state PDFs/workbooks are not committed. References include [FEC 2018 Excel](https://www.fec.gov/documents/2706/federalelections2018.xlsx), [FEC 2020 Excel](https://www.fec.gov/documents/4228/federalelections2020.xlsx), [Wyoming's 2020 summary](https://sos.wyo.gov/Elections/Docs/2020/Results/General/2020_General_Statewide_Candidates_Summary.pdf), [Maine's 2020 Senate table](https://www.maine.gov/sos/sites/maine.gov.sos/files/content/assets/ussenator1120.xlsx), and [Senate party division](https://www.senate.gov/history/partydiv.htm). Each receipt records actual retrieval time, URL, SHA-256 and bytes. MEDSL votes remain unchanged; adding Mississippi first-round returns requires Rahan's supplemental-source decision.

## Access method and update frequency

Run `python src/ingest/texas_tracker.py` from the repository root. Standard library only; no additional packages. Each run fetches one public page and saves a new UTC-stamped directory. Updates are manual for now.

## Attribution and redistribution permissions

The source page's Republishing Guidelines allow attributed republication, require preserving the column, prohibit resale, and require honoring removal/change requests. The source HTML snapshot is unchanged. Extracted tables are separately labeled mechanical derivatives, not an edited original article. Keep attribution and source links with every copy. These guidelines do not grant rights to republish every linked poll report; no linked PDFs are committed in this change.

## Snapshot location and checksum convention

`data/raw/texas_tracker/20260929T222648Z/` contains the unchanged HTML, original-cell CSV, mechanically normalized CSV, manifest, and automatic issue log. The manifest gives the retrieval time and SHA-256 of the original bytes. Normalized data stays with this source snapshot until analytical rules are approved.

## Retrieval and revision tracking

The first snapshot contains 16 tracker rows; source last-updated label is September 23, 2026. Fieldwork runs from June 1 through September 20. Retrieval date is not publication date. Never use the snapshot retrieval date as historical poll availability.

See docs/texas_tracker_review.md for verification limits and outstanding discrepancies.
