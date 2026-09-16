## Source
- URL: https://news.ycombinator.com/item?id=42830018
- Platform: HN (Ask HN)
- Date posted: 2025-01-28
- Author: jhunter1016
- Engagement: 36 pts, 42 comments

## What is the person trying to do?
Moderate UGC on a small static-site hosting platform (phishing + porn they can't host).

## Exact quoted pain
> "we wrote a very simple script that checks for common phishing attempts and alerts us. However, this simple script does not catch some of the more advance phishing sites and it doesn't catch other types of content that we can't support on our platform like porn."
> "We're still going to be manually reviewing sites because we haven't reached a scale that makes that impossible. But automation is nice."

## How often / how many people?
- Continuous ops burden (every new site). 42 comments with tips = shared small-host pain.
- Consequence: phishing outage / abuse, legal risk, manual review queue grows with users.

## Current workaround
- Regex/blocklist script for common phishing + manual review of every site.

## Why does the workaround fail?
- Blocklist misses advanced/cloaked phishing (kit rotation, obfuscated JS, brand-lookalike).
- No image/video understanding → porn slips through.
- Manual review doesn't scale; reviewer fatigue → misses.

## What remains unsolved?
Bounded triage with evidence: for each new static site, produce *checkable* verdict (phishing / porn / clean) + timestamped evidence (which page, which screenshot region, which string) a human can audit in seconds, running cheaply on every upload.

## Existing tools / non-AI check (do first)
- Google Safe Browsing API, PhishTank, SpamHaus; AWS Rekognition / Sightengine / Hive for NSFW; ClamAV for malware.
- Simple stack may already cover 80%: SafeBrowsing + NSFW classifier + link-age heuristics — must test false-positive rate and cost before claiming gap.
- Capability gap TBD: cloaked phishing that renders clean to bots but dirty to humans; multi-page static sites with obfuscated assets. Needs measurement, not assumption.
- NVIDIA/Nebius relevance is LATER gate — do not preserve on AI appeal alone.

## Verdict
Worth clustering (small-host trust & safety). Next: sample 20 public phishing kits + 20 clean static sites, test SafeBrowsing+Sightengine baseline, measure what still slips.
