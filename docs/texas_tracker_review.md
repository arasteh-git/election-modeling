# Texas tracker review — 2026-09-29

## Snapshot

Source: [Texas 2026 U.S. Senate Poll Tracker](https://texaspolitics.utexas.edu/blog/texas-2026-u-s-senate-poll-tracker), Texas Politics Project, University of Texas at Austin.
Snapshot: data/raw/texas_tracker/20260929T222648Z/.

16 rows extracted; all have release links. No rows excluded or corrected. This is a source inventory, not a fully verified model input.

## Findings

- Row 6, AARP: tracker shows Talarico 49 and Paxton 44, but its Spread column says Talarico +4. The arithmetic gives +5. The linked DDHQ page was inaccessible to the web retrieval tool, so the discrepancy remains unresolved; no replacement value was invented. Update 2026-09-29: Rahan accepted this as normal rounding (unrounded shares can round to 49 and 44 while their difference rounds to 4). Margins are computed as dem_pct minus rep_pct, so the tracker Spread is not used (Decision 009). The original AARP report has not been opened, and the spread_mismatch flag stays in the snapshot.
- Row 3, Emerson/Nexstar: original release checked on 2026-09-29. It corroborates September 12–14, n=1,000 likely voters, Talarico 47, Paxton 46, Brown 2, and undecided 4. Its methodology calls the +/-3 measure a credibility interval. Full questionnaire and respondent data have not been audited. Release: https://emersoncollegepolling.com/texas-2026-poll-talarico-and-paxton-in-dead-heat-abbott-maintains-edge/
- Row 14, UT/Texas Politics Project (June): Rahan checked the original release on 2026-09-29. It confirms Paxton 43 and Talarico 42 (D minus R = −1), so dem_pct and rep_pct are correct. The release shows Libertarian 3, someone else 3, and undecided 10, which sums to 101 with rounding. The tracker's Other column ("Brown 3, Unsure/someone else 7") understates non-major-candidate responses: 16 in the release versus 10 in the tracker. The snapshot is unchanged. Row 14 is RV, so it is excluded under Decision 009.
- Remaining 13 release links have been retained but not individually verified. All machine-generated primary_verification values stay pending; this note records the narrower Emerson and UT/TPP June checks.
- Some reported shares/categories do not sum exactly to 100. Do not normalize them to 100 or treat Other as exclusively undecided. Rounding and category definitions need original-release review.
- Population varies between RV and LV; candidate options vary. Source names mix sponsors and pollsters. First rules are now recorded in Decision 009 (LV only; labels as reported).
- The source's latest-update label is September 23; a September 29 download does not prove there were no later polls elsewhere.

## Checks performed

Live fetch and extraction; 16 rows carried into both CSVs; 16 distinct release URLs; cross-month date parsing; detected the row-6 spread discrepancy; deliberately changed table header rejected. Original HTML SHA-256 recorded in manifest.

## Next review

Verify the remaining releases and record publication dates. Rahan and Claude decide population, question-version, and inclusion rules before averaging. No methodological decisions made here.

