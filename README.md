# painsearch — evidence-first pain-point discovery

No invented ideas. Collect real complaints, cluster patterns, gate with a discovery test.

Built for Nebius x NVIDIA Global AI Hackathon prep. The system enforces:
- one micro-problem, no LLM wrappers / agent-layerisation / "chat with your data"
- not solvable by prompting ChatGPT alone
- NVIDIA open model must enable a central capability (not UI)
- Nebius must enable inference / deployment / scaling

## Layout
- `WORKPLAN.md` — 3-day sprint
- `search_queries.md` — pain-phrases x domains
- `discovery_test.md` — kill-fast gate
- `evidence_card_template.md` — evidence schema
- `src/collect.py` — permitted-APIs collector (HN Algolia, Lobsters, GitHub). No Reddit mass-scrape.
- `evidence/raw_*.json` — raw hits with source URLs
- `evidence/cards/` — one file per complaint

## Quickstart
```bash
python src/collect.py --source hn --query "manually checking" --limit 15
python src/collect.py --source github --query "manual workaround" --limit 20
```
Fill cards from `evidence_card_template.md`, cluster to 5-8 patterns, run `discovery_test.md`.

## License
MIT — see LICENSE.
