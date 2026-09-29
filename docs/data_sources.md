# Data sources

## Approved current polling sources

Rahan approved starting with the [Texas 2026 U.S. Senate Poll Tracker](https://texaspolitics.utexas.edu/blog/texas-2026-u-s-senate-poll-tracker) on 2026-09-29.
Author: Texas Politics Project. Publisher: Texas Politics Project at the University of Texas at Austin.

Approval is for collection, not automatic inclusion of every row in the model. This source describes its coverage as nonpartisan public polling since the Republican primary concluded in May. It is not an exhaustive census of all public polls.

## Approved historical polling sources

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

