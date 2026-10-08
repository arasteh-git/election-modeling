# Reviewed calibration references

JSON files that make the offline calibration preparer's exceptional dates, sides, aliases and factual checks inspectable. They contain factual excerpts and locators, not replacement election returns or modeling rules.

| File | Purpose |
| --- | --- |
| `fec_facts.json` | 885 candidate rows and 64 total-row locators from the FEC 2018/2020 Senate sheets, including primary candidates needed for non-ballot checks. Original strings, workbook URL/hash, sheet and row retained. Extraction is partial, not a certified replacement dataset. |
| `poll_aliases.json` | 290 explicit cycle/candidate-ID identities: 239 result-name matches/aliases, 27 FEC-row identities, one approved Texas non-ballot exception and 23 unresolved identities. Runtime fuzzy matching is never used. |
| `round_facts.json` | General-election dates, exceptional runoff dates, explicit King/Sanders/Ringelstein/Gross/Wyoming sides, selected result-to-FEC aliases, Maine first-choice checks and Wyoming's resolved FEC conflict. Each downloaded reference has a URL, actual retrieval timestamp, SHA-256 and byte size. |
| `extract_fec.py` | Standard-library XLSX reader/extractor for unchanged locally cached workbooks; verifies cached receipt hashes and refuses to overwrite JSON. No Excel workbook is authored. |

## Matching rules

The preparer normalizes punctuation, case and accents only when comparing explicit identities. Middle names, nicknames and materially different spellings require a recorded alias. Unconfirmed matches stay pending. An empty general/runoff cell establishes non-ballot membership only after the candidate has been explicitly identified in that official contest's table; absence from a search result is not evidence.

## Reference cache

Official downloaded reference bytes are cached locally under the Git-ignored `outputs/calibration_reference_research/`, alongside `receipts.json`. The cache is not required to replay preparation. It includes FEC workbooks, Wyoming's state summary, Maine's Senate workbook, Senate party-division history and an Alaska results landing page. Whole state documents are not redistributed in this repository, and no blanket permission for third-party/state-source material is assumed. FEC factual cell excerpts retain attribution and locators.

`fec_facts.json` was extracted before the Maine workbook was downloaded, so its receipt collection does not include Maine; `round_facts.json` does.

## Regenerate

To regenerate the FEC factual extraction from the cache into a fresh file:

```bash
python3 -B src/clean/calibration_references/extract_fec.py \
  --cache outputs/calibration_reference_research \
  --output outputs/fec_facts_replay.json
```

The cache reader does not make policy or alias choices. Inspect proposed changes and keep factual provenance when updating the explicit files. Applying changes requires a new snapshot and updated documentation; existing outputs stay immutable.

## Sources

[FEC 2018 workbook](https://www.fec.gov/documents/2706/federalelections2018.xlsx), [FEC 2020 workbook](https://www.fec.gov/documents/4228/federalelections2020.xlsx), [Wyoming 2020 summary](https://sos.wyo.gov/Elections/Docs/2020/Results/General/2020_General_Statewide_Candidates_Summary.pdf), [Maine 2020 Senate table](https://www.maine.gov/sos/sites/maine.gov.sos/files/content/assets/ussenator1120.xlsx), [Senate party division](https://www.senate.gov/history/partydiv.htm). Checks are partial; conflicting counts stay visible and MEDSL votes are retained. See [the preparation review](../../../docs/calibration_preparation_review.md).
