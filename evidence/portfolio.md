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

## P4 — Scattered engineering knowledge [NEW, from mining — needs cards]
- Evidence: Engineering.fyi 470pts/126c "manually checking individual blogs"; "How do you stay up to date with scientific papers" 5pts/3c; "RSS Reader that doesn't suck" 9pts/22c; "I looked at 1000s of RAG queries to figure out the problem with semantic search" 6pts/3c.
- Why distinct: task = reconcile conflicting/evolving records across sources, not moderate or verify backups.
- Next falsifiable Q: do 3+ independent reports show semantic search failing on the *same* narrow task (e.g. version-sensitive API answers)? Pull the RAG-queries thread + Engineering.fyi comments for concrete failure quotes.

## P5 — Long-video event detection [NEW, from mining — needs cards]
- Evidence: "How I OCR hundreds of hours of video" 125pts/17c; "Processing 24h of video in ten minutes" 77pts/37c; seal-camera hours of video; "Moderator who watched hours of traumatic videos sues TikTok".
- Why distinct: input constraint = continuous footage, output = precise timestamps + evidence. Matches promising-direction example.
- Next falsifiable Q: find 3+ reports where people need a *specific* event timestamped (not summary/montage) and existing tools (Premiere scene detect, Rekognition Video, Whisper+OCR) fail. Quote them.

## P6 — Agent-output verification [NEW, from mining — needs cards]
- Evidence: "qckfx – Stop manually checking if your AI agent broke your iOS app" 2pts; "AI hallucinate. Do you ever double check the output?" 8pts/21c; "OmoiOS – 190K lines to stop babysitting AI agents"; "Claude Code frequently loses track of directory" 86r/50c.
- Why distinct: task = catch specific failure ordinary tests/review miss. Matches promising-direction example. Risk: crowded, easy to become agent-layerisation — gate hard.
- Next falsifiable Q: find 3+ independent cases naming the *same* missed failure class (e.g. agent breaks build silently passing tests). If failures differ each time, no micro-problem.

## Rule
No candidate becomes default winner. Advance only on answered falsifiable Q + measured residual gap. NVIDIA/Nebius feasibility is step 6, never a reason to preserve a weak problem.
