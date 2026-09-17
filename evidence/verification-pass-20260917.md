# Verification pass — 2026-09-17

Broad collection remains paused. This pass tested P4 and P5 falsifiable questions; it did not generate an idea.

## P4 — retrieval / evolving knowledge

### Evidence inspected
1. [HN: RAG failure modes](https://news.ycombinator.com/item?id=42299349)
   - One practitioner reports reviewing thousands of production queries.
   - Concrete failure classes: negated queries, multi-hop queries, and fuzzy filtering across chunks.
   - This is useful technical evidence, but one thread is not independent validation of a recurring buyer pain.
2. [HN: staying current with papers](https://news.ycombinator.com/item?id=6711453)
   - A user asks how to avoid manually checking journals worldwide.
   - Only 5 points / 3 comments; suggested workaround is advanced search + bookmarks and an existing service.
3. [Engineering.fyi](https://engineering.fyi/)
   - Existing aggregator offers company/topic filtering and a weekly digest.

### Result
**Do not promote P4.** The evidence currently establishes retrieval failure modes and existing aggregation, not a narrow recurring unmet task.

### Next falsifiable question
Find three independent current reports about one defined task, such as answering a version-sensitive API question across changing documentation. Then construct a small benchmark and compare keyword search, hybrid search, and reranking. Do not add an LLM until a measured residual gap exists.

## P5 — long-video event detection

### Evidence inspected
1. [HN: OCR hundreds of hours](http://waldo.jaquith.org/blog/2011/02/ocr-video/)
   - Demonstrates a historical processing workflow, not a current complaint.
2. [HN: 24 hours of video in ten minutes](https://sievedata.com/)
   - Demonstrates an existing product, not unmet demand.
3. [Spot AI: retail investigation](https://www.spot.ai/blog/ai-video-search-retail)
   - Describes retail teams scrubbing hundreds of hours to find short evidence clips.
4. [Greater Manchester Police case study](https://www.bedroq.co.uk/case-studies/greater-manchester-police-transforming-over-7-months-of-cctv-data-in-just-2-days-into-court-ready-evidence/)
   - Reports a real high-volume use case: 5,832 hours processed in 16 hours.
5. [TwelveLabs annotation](https://www.twelvelabs.io/blog/automated-video-data-labeler)
   - Existing timestamped video annotation product.
6. [NeedleInAVidStack](https://github.com/ALucek/NeedleInAVidStack)
   - Existing open-source project for extracting and timestamping specific content.

### Result
**Do not promote P5 yet.** There is credible operational demand and substantial existing competition, but the collected evidence does not identify a residual failure or a defined operator group whose problem remains unsolved.

### Next falsifiable question
Collect three first-person reports from one operator group (for example, legal investigators, retail loss prevention, or documentary editors) that name the same event-detection failure, its consequence, and why current search/annotation tools miss it.

## Decision
P4 and P5 are both research leads, not opportunities. No UGC baseline or prototype yet. The next pass should be a targeted source search for one operator group and one failure, not another generic query.
