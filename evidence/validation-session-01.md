# Validation session 01 — current results

## Scope
Reddit is paused because self-serve API access is restricted behind Reddit's Responsible Builder Policy and approval process. This session used HN Algolia, GitHub Issues API, and Lobsters only. The broad collection limit is closed; these were targeted validation searches.

## Candidate comparison

| ID | Problem | Evidence status | Conventional alternatives | Decision |
|---|---|---|---|---|
| P0004 | Third-party API changes discovered after user-facing breakage | 3 ecosystem reports, but only one direct first-person frequency report | Pinning, lockfiles, Pact, Schemathesis, contract tests, synthetic checks, changelog monitoring | Continue one reproducible fixture; not validated opportunity |
| P0005 | Systematic-review screening misses buried eligibility evidence and needs repetitive extraction | 3 independent reports across HN/GitHub; concrete missed-study and manual-scale evidence | Database queries, Zotero, Rayyan, Covidence, ASReview, DistillerSR, Undermind | Strongest new lead; validate on one review protocol |
| P0002 | Small-host UGC moderation misses advanced abuse | One HN operator report; baseline not run | Safe Browsing, PhishTank, Spamhaus, NSFW classifiers, ClamAV | Keep candidate; do not make default winner |

## P0005 evidence chain

- [Meta-analysis discussion](https://news.ycombinator.com/item?id=41071406): a researcher reports a study that existing search missed and eligibility information buried deep in the text; they still require human verification.
- [Zotero MCP issue #46](https://github.com/54yyyu/zotero-mcp/issues/46): a separate user describes applying the same analysis to dozens or hundreds of papers and choosing between manual repetition or external scripts.
- [Literature management discussion](https://news.ycombinator.com/item?id=10488028): another researcher reports difficulty managing a growing paper collection and manual metadata work.

These establish a recurring workflow burden, not a finished product opportunity. They do not prove that an AI model is necessary.

## Required validation experiment

Use one publicly available systematic-review protocol and its included/excluded paper set. Create an adjudicated ground truth. Compare:

1. conventional database search;
2. Zotero organization and metadata;
3. one established screening workflow such as Rayyan, Covidence, or ASReview;
4. structured extraction with page-level citations.

Measure recall, false exclusions, extraction agreement, citation traceability, reviewer time, and cost. If conventional tools solve the task, reject P0005 for the hackathon. If a precise residual gap remains, only then test model and Nebius feasibility.

## Current conclusion
No idea is validated yet. P0005 is the strongest new lead; P0004 remains a separate lead. The next deliverable is a baseline experiment and evidence table, not a generated concept list.
