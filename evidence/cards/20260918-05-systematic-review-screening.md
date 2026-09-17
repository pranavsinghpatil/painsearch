## Source
- Primary HN URL: https://news.ycombinator.com/item?id=41071406
- Supporting GitHub issue: https://github.com/54yyyu/zotero-mcp/issues/46
- Supporting HN URL: https://news.ycombinator.com/item?id=10488028
- Platforms: HN + GitHub Issues

## Candidate problem statement
Researchers conducting systematic reviews must screen and extract structured eligibility/evidence fields across many papers, but important criteria can be buried in full text and current workflows can miss studies or require repeating the same analysis manually.

## Evidence
1. Meta-analysis researcher:
> "The second one is a study I excluded for something buried deep in the text."
> "The sixth study was entirely new to me ... my existing search processes missed."
> "It would have to advance substantially before it was my only search method for a meta-analysis."

2. Zotero MCP user:
> "systematic literature reviews require applying the same analysis to dozens or even hunderds of papers."
> "Currently, this means either: 1. Manually asking the same question about each paper through conversation 2. Building external scripts that lose Zotero MCP's benefits."

3. Literature-management user:
> "It's becoming difficult to manage them all."
> "Need to manually rename papers to a common filename format."

## Workarounds
- Search databases and manually screen papers.
- Use an AI paper-search tool, then manually verify inclusion/exclusion decisions.
- Ask the same extraction question paper-by-paper or write an external batch script.
- Use Zotero/Paperpile/Calibre for organization.

## Why they fail
- Search can miss relevant gray literature and criteria buried in full text.
- Batch extraction is not a reproducible decision record by itself.
- Existing organization tools do not solve eligibility reconciliation.
- AI search results still require human verification before a review can rely on them.

## Existing alternatives to check
Undermind, semantic scholarly search, Zotero, Rayyan, Covidence, ASReview, DistillerSR, and conventional database queries. The exact residual gap is not yet measured.

## Falsifiable validation question
For one review protocol, can existing search + screening tools identify the same eligible/ineligible studies and extract the same fields with source-page evidence? Measure recall, false exclusions, extraction agreement, citation traceability, and reviewer time.

## Status
**Investigating lead, not a validated hackathon opportunity.** It is promising because the failure is not "summarize papers"; it is missed eligibility evidence and inconsistent, auditable screening. It remains at risk of becoming a generic LLM wrapper, so the model-centrality gate is deferred and strict.
