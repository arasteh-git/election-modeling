# Data sources

## Approved current polling sources

Rahan approved starting with the [Texas 2026 U.S. Senate Poll Tracker](https://texaspolitics.utexas.edu/blog/texas-2026-u-s-senate-poll-tracker) on 2026-09-29.
Author: Texas Politics Project. Publisher: Texas Politics Project at the University of Texas at Austin.

Approval is for collection, not automatic inclusion of every row in the model. This source describes its coverage as nonpartisan public polling since the Republican primary concluded in May. It is not an exhaustive census of all public polls.

## Approved historical polling sources

No named historical source has yet been approved for model inclusion. Rahan requested historical Texas Senate collection on 2026-10-05; the following inventory was collected under that request and remains subject to source review:

- 2018 and 2020: preserved FiveThirtyEight Senate candidate-row file in `khristel26/Senate`, pinned to commit `d3d0c6be4e35945e59c1cb574b4050ca1787a2bc`. [Archive file](https://raw.githubusercontent.com/khristel26/Senate/d3d0c6be4e35945e59c1cb574b4050ca1787a2bc/senate_polls_historical.csv). Mirror identity is not independently verified against original bytes. Original [publisher polling documentation](https://github.com/fivethirtyeight/data/blob/master/polls/README.md) links to CSV endpoints that now return ABC webpages.
- 2024: [Texas Politics Project tracker](https://texaspolitics.utexas.edu/blog/texas-2024-us-senate-poll-tracker), author/publisher Texas Politics Project at UT Austin, last updated October 30, 2024; may omit later polls.

Snapshot: `data/raw/texas_senate_historical/20261006T024116Z/`. The manifest records each source's URL, retrieval time, SHA-256, transformations, and limits. Run `python src/ingest/texas_senate_historical.py`; replay instructions and all file descriptions are in [the historical inventory README](../data/raw/texas_senate_historical/README.md). No population, quality, partisan, or hypothetical-matchup exclusions were applied to the requested source scope.

FiveThirtyEight's [repository](https://github.com/fivethirtyeight/data) states CC BY 4.0 for datasets unless otherwise noted; publisher README copies are saved. Attribution: FiveThirtyEight / ABC News, with preservation credit to the mirror. The 2024 UT page includes the same attributed republication guidelines described below; its HTML is unchanged and CSVs are labeled mechanical derivatives. No linked reports have been downloaded.

## Approved election-result sources

## Access method and update frequency

Run `python src/ingest/texas_tracker.py` from the repository root. Standard library only; no additional packages. Each run fetches one public page and saves a new UTC-stamped directory. Updates are manual for now.

## Attribution and redistribution permissions

The source page's Republishing Guidelines allow attributed republication, require preserving the column, prohibit resale, and require honoring removal/change requests. The source HTML snapshot is unchanged. Extracted tables are separately labeled mechanical derivatives, not an edited original article. Keep attribution and source links with every copy. These guidelines do not grant rights to republish every linked poll report; no linked PDFs are committed in this change.

## Snapshot location and checksum convention

`data/raw/texas_tracker/20260929T222648Z/` contains the unchanged HTML, original-cell CSV, mechanically normalized CSV, manifest, and automatic issue log. The manifest gives the retrieval time and SHA-256 of the original bytes. Normalized data stays with this source snapshot until analytical rules are approved.

## Retrieval and revision tracking

The first snapshot contains 16 tracker rows; source last-updated label is September 23, 2026. Fieldwork runs from June 1 through September 20. Retrieval date is not publication date. Never use the snapshot retrieval date as historical poll availability.

See docs/texas_tracker_review.md for verification limits and outstanding discrepancies.

