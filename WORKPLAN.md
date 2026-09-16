# Nebius x NVIDIA Hackathon — Pain-Point Discovery System
No invented ideas. Evidence first. Revised flow 2026-09-17: portfolio over pipeline.

## Hard constraints (gate late, not early)
- One micro-problem or tightly connected set.
- No LLM wrappers, agent-layerisation, or "chat with your data".
- Not solved by prompting ChatGPT / OpenClaw alone — but that alone proves nothing; deterministic software / better data / conventional algo may be the right answer.
- NVIDIA open model must enable a central capability (step 6 gate, not a reason to preserve weak problems).
- Nebius must enable meaningful inference / deployment / scaling (step 6 gate).

## Tracks (from devpost)
1. Coding and Agentic Engineering — agents that write/run/test in Token Factory Sandboxes
2. Best Apps and Agents — Nemotron-powered, Nano/Super for fast, Ultra for reasoning; Serverless Endpoints/Jobs encouraged
3. Personal AI — always-on, private, memory + skills + tools; NemoClaw/OpenShell/Hermes + Nebius Serverless
4. Physical AI — GROOT/Cosmos/Sonic + Nemotron, Serverless Jobs for sim/synthetic/eval, Endpoints for realtime; 1-min hardware clip required

## Judging
Technological Implementation / Design / Potential Impact / Quality of Idea

## Revised flow (7 steps, 2026-09-17)
1. **Collect raw** — PAUSED at 120 hits. Preserve links + context. No more broad queries until portfolio gaps demand them.
2. **Extract patterns** — cluster by user x task x failure x consequence, not keywords. See `evidence/portfolio.md` P1-P6.
3. **Verify pain** — independent reports, workarounds, frequency, consequence. Mark weak/disputed evidence (P3).
4. **Map existing solutions** — test conventional tools first. Record exact residual gap.
5. **Test residual gap** — reproduce + measure (counts, false-negatives, cost). Does it matter enough to someone?
6. **Hackathon feasibility gate** — only now: open-model necessity, Nebius relevance, buildability, track/judging fit.
7. **Prototype vs best baseline** — compare against best existing tool, not against doing nothing.

## How to run
```bash
python src/collect.py --source hn --query "takes me hours to" --limit 20
# outputs to evidence/raw_*.json + evidence/cards/
```

## Rules
- Respect ToS: official APIs only (HN Algolia, GitHub API, Lobsters). No Reddit mass-scrape.
- Save source URL + quote + date for every card. No paraphrase-only.
- Deliverable is NOT an idea. It's the portfolio with answered falsifiable Qs.

## Status
- 120 raw hits mined. 3 cards done. 6-pattern portfolio written. Next: answer P4/P5/P6 falsifiable Qs, then baseline P2.
