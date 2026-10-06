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

The approved derived inventory is under `data/processed/texas_senate_historical/20261006T024116Z/`. It fills the 2024 election date from Rahan's confirmation, tags 2018/2020 partisanship from archived `partisan` and `internal` fields, and removes the 12 hypothetical 2020 matchups from the active CSVs. Original inputs stay unchanged. See [the processed README](../data/processed/texas_senate_historical/README.md) for outputs, transformation/exclusion audits, input and output hashes, and limitations. `not_flagged_partisan` describes the archive's flags; `unknown` applies where metadata is absent, including all 2024 rows. Election results and primary-release partisanship verification have not been collected.

## Approved election-result sources

No election-result source has been approved yet.

## Proposed election-result sources (2026-10-05; awaiting Rahan)

Recommend **MIT Election Data and Science Lab, U.S. Senate statewide 1976–2024**, [Harvard Dataverse DOI 10.7910/DVN/PEJ5QU](https://doi.org/10.7910/DVN/PEJ5QU), published version **8.0**, released `2026-05-11T16:13:52Z`. Public API metadata identifies unrestricted tabular file `13887039` (`1976-2024-senate-state.tab`, original CSV name `1976-2024-senate-state.csv`) and an explicit [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) license. Proposed original-CSV download: `https://dataverse.harvard.edu/api/access/datafile/13887039?format=original`.

Use this consistent main source for 2018/2020 and Texas 2024; use [FEC 2018](https://www.fec.gov/introduction-campaign-finance/election-results-and-voting-information/federal-elections-2018/) / [2020](https://www.fec.gov/introduction-campaign-finance/election-results-and-voting-information/federal-elections-2020/), [House Clerk election statistics](https://history.house.gov/Institution/Election-Statistics/) (including a listed 2024 PDF), and [Texas SOS](https://www.sos.state.tx.us/elections/historical/elections-results-archive.shtml) as official crosschecks. FEC/Clerk federal compilations are generally federal works; no explicit dataset license was found. Texas-source redistribution permission remains unestablished. These are not additional approved collection sources.

Metadata, the MEDSL codebook, official source landing pages, and the FEC 2018 PDF were inspected during source research. No result dataset was saved or candidate vote counts verified; workbook schemas remain uninspected. The MEDSL catalog/codebook descriptions lag the dataset's 2024 version, so actual headers, coverage, ballot lines, modes, round definitions, and certification flags must be checked after approval. See [the preparation plan](calibration_preparation_plan.md) for access details, documented fields, permissions, source limitations, race-format choices, proposed outputs, and validation. Approval will be recorded here before results collection, as requested in [the Claude-to-Codex handoff](handoffs/2026-10-05-claude-code-to-codex.md).

## Access method and update frequency

Run `python src/ingest/texas_tracker.py` from the repository root. Standard library only; no additional packages. Each run fetches one public page and saves a new UTC-stamped directory. Updates are manual for now.

## Attribution and redistribution permissions

The source page's Republishing Guidelines allow attributed republication, require preserving the column, prohibit resale, and require honoring removal/change requests. The source HTML snapshot is unchanged. Extracted tables are separately labeled mechanical derivatives, not an edited original article. Keep attribution and source links with every copy. These guidelines do not grant rights to republish every linked poll report; no linked PDFs are committed in this change.

## Snapshot location and checksum convention

`data/raw/texas_tracker/20260929T222648Z/` contains the unchanged HTML, original-cell CSV, mechanically normalized CSV, manifest, and automatic issue log. The manifest gives the retrieval time and SHA-256 of the original bytes. Normalized data stays with this source snapshot until analytical rules are approved.

## Retrieval and revision tracking

The first snapshot contains 16 tracker rows; source last-updated label is September 23, 2026. Fieldwork runs from June 1 through September 20. Retrieval date is not publication date. Never use the snapshot retrieval date as historical poll availability.

See docs/texas_tracker_review.md for verification limits and outstanding discrepancies.
