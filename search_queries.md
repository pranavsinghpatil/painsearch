# Search for pain, not ideas
Combine pain-phrase x domain. Run manually first, then via collect.py.

## Pain phrases
- "takes me hours to"
- "time-consuming process"
- "tedious but necessary"
- "we do this every week"
- "manually checking"
- "I wish there was a way"
- "takes hours" developer
- "Ask HN" tedious
- "failed tool" workflow
- "we gave up on" automation

## Starter queries (copy-paste)
- site:reddit.com "manually checking" workflow
- site:reddit.com "I wish there was a way" engineering
- site:github.com/issues "takes hours" developer
- site:news.ycombinator.com "Ask HN" tedious
- site:lobste.rs "tedious" workflow

## HN Algolia (automated, allowed)
- tedious workflow
- tedious but necessary
- manual review every week
- takes hours video / logs / documents

## GitHub Issues (automated, allowed via API)
- "takes hours" + label:bug
- "manual workaround" + state:open + comments:>5
- "missing capability" + reactions:>10

## Domains to try (one at a time, keep micro)
video timestamps / CCTV review / research papers / code review misses / doc reconciliation / logs / meeting notes / invoices / sensor data

## Rule
Stop after 20-30 raw hits. Do NOT auto-scrape Reddit. If a subreddit looks rich, note it for Day 2 targeted manual read.
