# Nebius x NVIDIA Hackathon — Pain-Point Discovery System
No invented ideas. Evidence first.

## Hard constraints (gate every candidate)
- One micro-problem or tightly connected set.
- No LLM wrappers, agent-layerisation, or "chat with your data".
- Not solvable by prompting ChatGPT / LLM / OpenClaw.
- No added agents/tools to fake sophistication.
- NVIDIA model must enable a *central* capability, not just UI.
- Nebius must enable meaningful inference / deployment / scaling.

## Tracks (from devpost)
1. Coding and Agentic Engineering — agents that write/run/test in Token Factory Sandboxes
2. Best Apps and Agents — Nemotron-powered, Nano/Super for fast, Ultra for reasoning; Serverless Endpoints/Jobs encouraged
3. Personal AI — always-on, private, memory + skills + tools; NemoClaw/OpenShell/Hermes + Nebius Serverless
4. Physical AI — GROOT/Cosmos/Sonic + Nemotron, Serverless Jobs for sim/synthetic/eval, Endpoints for realtime; 1-min hardware clip required

## Judging
Technological Implementation / Design / Potential Impact / Quality of Idea

## 3-day sprint
Day 1: Collect 20-30 raw complaints (this system)
Day 2: Cluster into 5-8 patterns
Day 3: Deep-research 2-3 with Discovery Test

## How to run
```bash
cd hackathon-discovery
python src/collect.py --query "takes me hours to" --limit 20
python src/collect.py --source hn --query "tedious workflow" --limit 20
python src/collect.py --source github --query "takes hours" --limit 20
# outputs to evidence/raw_*.json + evidence/cards/
```

## Rules
- Respect ToS: use official APIs only (HN Algolia, GitHub API, Lobsters API). No Reddit mass-scrape. Reddit = manual + JSON limited.
- Save source URL + quote + date for every card. No paraphrase-only.
- First deliverable is NOT an idea. It's 20-30 evidence cards.

## Your next task (do this, paste output)
1. Run: `python src/collect.py --source hn --query "tedious but necessary" --limit 10`
2. Open `evidence/raw_hn_*.json`, pick 3 complaints, fill 3 cards from `evidence_card_template.md`
3. Paste the 3 card files back here for clustering.
