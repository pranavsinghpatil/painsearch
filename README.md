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
- `src/registry.py` — validate and safely update the reusable problem registry
- `registry/schema/problem-registry-v1.json` — strict versioned registry contract
- `registry/registry.json` — structured problems, evidence, provenance, investigations, and audit history
- `requirements.txt` — JSON Schema validator dependency
- `tests/test_registry.py` — malformed-data, provenance, and transition tests
- `evidence/raw_*.json` — raw hits with source URLs
- `evidence/cards/` — human-readable evidence cards
- `evidence/portfolio.md` — candidate comparison without a default winner

## Quickstart
```bash
python src/collect.py --source hn --query "manually checking" --limit 15
python src/collect.py --source github --query "manual workaround" --limit 20
python src/registry.py validate
python src/registry.py list
python src/registry.py show P0002
# Controlled status update: actor + reason are mandatory and history is appended
python src/registry.py transition P0002 --to unresolved --actor your-name --reason "Baseline still missing"
```
Fill cards from `evidence_card_template.md`, then migrate durable records into `registry/registry.json`.

## License
MIT — see LICENSE.
