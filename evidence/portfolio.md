# Candidate portfolio — compare, don't funnel
Status as of 2026-09-17. Broad collection PAUSED at 120 raw hits. No winner yet.

## P1 — Backblaze-style backup verification [REJECTED for hackathon, kept as pain ref]
- Evidence: 203pts/230c, explicit vendor "no hash compare implemented", millions of files.
- Status: pain supported; conventional solution exists (rclone/restic manifest diff).
- Next falsifiable Q: none for hackathon. Keep as negative example.

## P2 — Small-host UGC triage [CANDIDATE, gap unmeasured]
- Evidence: Ask HN 36pts/42c, blocklist misses advanced phishing + porn, manual review every site.
- Status: potential residual gap; baseline untested.
- Next falsifiable Q: does SafeBrowsing + PhishTank + Sightengine/Hive still miss cloaked kits on 20 phishing + 20 clean static sites? Measure false-negatives + cost before any model talk.

## P3 — Windows settings drift [PARKED, disputed pain]
- Evidence: 51pts/14c, "mysteriously re-enabled" vs "hasn't happened to me in 3+ years".
- Existing: ShutUp10 / Tripwire / Intune baselines.
- Next falsifiable Q: find 3+ independent post-24H2 revert reports with KB id + key path, or park stays.

## P4 — Scattered/evolving engineering knowledge [WEAK; needs narrower task]
- Evidence: Engineering.fyi is a functioning aggregator with weekly digest; the 2013 paper thread has only 5 points/3 comments and a bookmark/search workaround; the RAG thread has concrete failures (negation, multi-hop, fuzzy filtering) but is about retrieval quality, not merely discovery.
- Why distinct: task = answer a constrained question across changing sources, not moderate or verify backups.
- Current finding: one practitioner reports production failure modes (negation, multi-hop, fuzzy filtering), but the paper-discovery thread is only 5pts/3c and Engineering.fyi is an existing aggregator. Evidence supports failure modes, not recurring unmet pain. Do not promote yet.
- Next falsifiable Q: find 3+ independent current reports for one narrow failure (e.g. version-sensitive API answer across docs), then compare keyword, hybrid-search, and reranking baselines. See `evidence/verification-pass-20260917.md`.

## P5 — Long-video event detection [UNVALIDATED]
- Evidence: OCR of hundreds of hours (125pts/17c) and 24h processing (77pts/37c) demonstrate technical demand/solutions, but are not independent complaint reports. Search hits are mostly showcases, not unmet pain.
- Why distinct: input constraint = continuous footage; possible output = precise timestamps + evidence.
- Current finding: insufficient pain evidence. Do not treat popularity or compute volume as validation.
- Next falsifiable Q: find 3+ reports from a defined operator group needing one specific event timestamped, with current-tool failures and consequence.

## P6 — Agent-output verification [REJECT CURRENT FORMULATION]
- Evidence: qckfx explicitly ships local record/replay + visual diffs and states "No AI in the loop at runtime"; other hits mix unrelated agent failures (hallucination, directory drift, babysitting).
- Why distinct: task = catch one specific failure ordinary tests/review miss.
- Current finding: exact iOS visual-regression pain already has a direct conventional solution; evidence does not establish one shared missed-failure class.
- Next falsifiable Q: only reopen if 3+ independent reports identify the same failure that qckfx/Playwright/Appium/XCUITest cannot detect.

## P7 — Systematic-review screening misses buried eligibility evidence [INVESTIGATING]
- Evidence: independent HN meta-analysis researcher reports a relevant study missed by existing search and eligibility facts buried deep in text; separate Zotero issue reports repeating analysis across dozens/hundreds of papers manually; older literature-management report describes growing management burden.
- Status: strongest new research lead, but existing tools and model necessity are untested. High risk of becoming a generic paper-analysis wrapper.
- Next falsifiable Q: on one published review protocol, do conventional search + Rayyan/Covidence/ASReview/Zotero workflows miss the same eligible studies or buried criteria? Measure recall, false exclusions, extraction agreement, citation traceability, and time.

## Decision after inspection
- P1 remains a rejected pain reference.
- P2 remains a candidate, but should not be run as the default winner.
- P3 remains parked pending independent evidence.
- P4/P5 are research leads, not opportunities yet.
- P6 is rejected in its current broad form.
- P7 is investigating, not validated and not yet an idea.
- **Next research action:** validate P0004 and P0005 against conventional baselines. Generate a hackathon concept only after one residual gap is reproducible.

## Rule
No candidate becomes default winner. Advance only on answered falsifiable Q + measured residual gap. NVIDIA/Nebius feasibility is step 6, never a reason to preserve a weak problem.
