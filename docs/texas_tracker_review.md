# Texas tracker review — 2026-09-29

## Snapshot

Source: [Texas 2026 U.S. Senate Poll Tracker](https://texaspolitics.utexas.edu/blog/texas-2026-u-s-senate-poll-tracker), Texas Politics Project, University of Texas at Austin.
Snapshot: data/raw/texas_tracker/20260929T222648Z/.

16 rows extracted; all have release links. No rows excluded or corrected. This is a source inventory, not a fully verified model input.

## Findings

- Row 6, AARP: tracker shows Talarico 49 and Paxton 44, but its Spread column says Talarico +4. The arithmetic gives +5. The linked DDHQ page was inaccessible to the web retrieval tool, so the discrepancy remains unresolved; no replacement value was invented.
- Row 3, Emerson/Nexstar: original release checked on 2026-09-29. It corroborates September 12–14, n=1,000 likely voters, Talarico 47, Paxton 46, Brown 2, and undecided 4. Its methodology calls the +/-3 measure a credibility interval. Full questionnaire and respondent data have not been audited. Release: https://emersoncollegepolling.com/texas-2026-poll-talarico-and-paxton-in-dead-heat-abbott-maintains-edge/
- Remaining 14 release links have been retained but not individually verified in this initial extraction. All machine-generated primary_verification values stay pending; this note records the narrower Emerson spot-check.
- Some reported shares/categories do not sum exactly to 100. Do not normalize them to 100 or treat Other as exclusively undecided. Rounding and category definitions need original-release review.
- Population varies between RV and LV; candidate options vary. Source names mix sponsors and pollsters. These require explicit modeling rules later.
- The source's latest-update label is September 23; a September 29 download does not prove there were no later polls elsewhere.

## Checks performed

Live fetch and extraction; 16 rows carried into both CSVs; 16 distinct release URLs; cross-month date parsing; detected the row-6 spread discrepancy; deliberately changed table header rejected. Original HTML SHA-256 recorded in manifest.

## Next review

Prioritize AARP's original report, then verify the remaining releases and record publication dates. Rahan and Claude decide population, question-version, and inclusion rules before averaging. No methodological decisions made here.

