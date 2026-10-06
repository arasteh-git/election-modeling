# Historical Texas Senate polling

Inventory for the 2018, 2020, and 2024 Texas U.S. Senate general elections. Collected at Rahan's request on 2026-10-05. This original snapshot preserves source review data. [The prepared inventory](../../processed/texas_senate_historical/README.md) applies Rahan's later approved corrections and hypothetical-matchup exclusion (Decision 011); broader calibration choices remain undecided.

First snapshot: `20261006T024116Z/`.

| Cycle | Major-party matchup | Records | LV records |
| --- | --- | ---: | ---: |
| 2018 | Beto O'Rourke / Ted Cruz | 49 | 29 |
| 2020 | M.J. Hegar / John Cornyn, plus flagged hypothetical matchups | 63 | 40 |
| 2024 | Colin Allred / Ted Cruz | 37 | 23 |

Records are 538 questions for 2018/2020 and UT tracker rows for 2024. LV counts describe the inventory, not an approved historical modeling sample. Texas had no regularly scheduled U.S. Senate election in 2022.

## Files in each snapshot

- `senate_polls_historical.csv`: unchanged full candidate-row CSV from a pinned [GitHub mirror](https://github.com/khristel26/Senate/blob/d3d0c6be4e35945e59c1cb574b4050ca1787a2bc/senate_polls_historical.csv) of FiveThirtyEight. Original endpoints currently redirect to ABC pages. Mirror provenance is not verified byte-for-byte against the original.
- `texas_2024_source.html`: unchanged [Texas 2024 U.S. Senate Poll Tracker](https://texaspolitics.utexas.edu/blog/texas-2024-us-senate-poll-tracker), Texas Politics Project at the University of Texas at Austin; last update October 30, 2024.
- `fivethirtyeight_README.md`, `fivethirtyeight_polls_README.md`: saved original publisher license statement and polling download documentation. FiveThirtyEight states CC BY 4.0 unless otherwise noted. UT republication guidelines are in the saved HTML: attribution, unchanged original, no resale, honor change/removal requests. CSVs here are labeled mechanical derivatives, not altered original articles. Linked primary reports are not downloaded.
- `texas_538_candidate_rows.csv`: all 262 Texas candidate rows from the older archive, preserving every original field plus a source row number (1-based data row, excluding header).
- `texas_2024_tracker.csv`: all 37 original-cell tracker records and links. One footnote is recorded separately in the manifest, not counted as a poll.
- `normalized.csv`: all 149 records in one mechanical schema; candidate percentages are not rescaled, corrected, allocated, or weighted.
- `texas_2018.csv`, `texas_2020.csv`, `texas_2024.csv`: cycle subsets of the same schema.
- `manifest.json`: URLs, per-source retrieval timestamps and SHA-256 hashes, immutable mirror revision, attribution, transformations, counts, footnotes, permissions, and limitations.
- `issues.json`: all flagged records; universal provenance/publication flags are included, so this file is not a list of automatic exclusions.

## Collect or replay

From the repository root, standard library only:

```bash
python src/ingest/texas_senate_historical.py
python src/ingest/texas_senate_historical.py --snapshot data/raw/texas_senate_historical/20261006T024116Z --output-root outputs/history_replay
```

Runs create a new UTC-stamped directory and never overwrite an existing snapshot. Replay uses saved bytes and original timestamps, verifies source hashes, and requires a fresh output location. The collector imports the existing `texas_tracker.py` HTML parser.

## Load in your notebook

For the corrected active inventory, use [the prepared CSV](../../processed/texas_senate_historical/README.md). To inspect the original 149-row inventory for audit instead, from a kernel working in `notebooks/`:

```python
history = pd.read_csv('../data/raw/texas_senate_historical/20261006T024116Z/normalized.csv')
```

If the kernel works from the repository root, omit `../`. Start by inspecting `cycle`, `population`, candidate names, `poll_id`, `question_id`, and `flags`. See [the data dictionary](../../../docs/data_dictionary.md).

## Review before modeling

- Hypothetical 2020 Democratic challengers remain present and flagged. No matchup or population rows were dropped from the collection.
- Decision 011 excludes those 12 hypothetical questions only in the processed inventory. Its 37 2024 election dates are `2024-11-05`, while this original snapshot preserves the absent source date. Partisan tags and audits are also in processed outputs.
- Several questions can belong to one poll. `multiple_questions_same_poll` flags all affected records; their duplication/population/undecided treatment needs review before averaging.
- The 2024 date `8/24/8/29/2024` is unresolved: both normalized field dates are blank and the source text is preserved. No date was invented.
- Missing sample/population/release links and tracker MOEs are flagged. Spread discrepancies retain source shares and displayed spreads. Shared links across different labels are flagged, including an Activote row linked to Morning Consult. The Marist asterisk records source-forced undecided treatment.
- `created_at_raw` is 538 entry time, with unverified timezone, not a verified poll publication date. UT does not supply per-poll publication dates. Retrieval in 2026 does not establish historical availability.
- 2024 tracker coverage ends with its October 30 update and can omit later polls; source coverage differs between cycles. No individual primary releases were verified in this collection.
- Election results have not been collected. Three Texas races alone are too few independent race outcomes for a reliable general Senate error calibration; a broader approved historical sample is still needed.
