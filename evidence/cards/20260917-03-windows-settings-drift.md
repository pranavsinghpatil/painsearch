## Source
- URL: https://news.ycombinator.com/item?id=45485986 (Show HN) + https://github.com/nolesapex/DidMySettingsChange
- Platform: HN + GitHub
- Date posted: 2025-10-05
- Engagement: 51 pts, 14 comments

## What is the person trying to do?
Keep Windows privacy/telemetry settings off across updates without manually re-checking each one.

## Exact quoted pain
- OP premise: "Many users find that after disabling certain settings, these settings are mysteriously re-enabled after updates or without any apparent reason."
- Tool promise: "ensuring that they stay in control of their privacy without the hassle of manually checking each setting."
- Commenter: "I've been using shutup10... being able to check settings at a glance in one place is very helpful."
- Counter-signal: "I've read so much FUD about Windows undoing settings... in 3+ years it hasn't happened to me." → disputed frequency, needs validation.

## How often / how many people?
- Per-update check (Patch Tuesday / 24H2). Audience = privacy-conscious Windows users, IT admins.
- Disputed: some never repro; others report reverts. Must quantify before building.

## Current workaround
- Manually walk Settings panels; O&O ShutUp10 / W10Privacy snapshots; OP's Python script (scan known keys + alert + logs).

## Why does the workaround fail?
- Setting inventory drifts with Windows builds (new keys, moved registry paths) → scripts rot.
- Noisy: can't distinguish user-intended change vs update-induced revert vs app flip.
- No verifiable before/after proof per update (which KB flipped which key, when).

## What remains unsolved?
Reconcile conflicting, changing records: snapshot desired-state, diff post-update actual, attribute cause (KB id / timestamp / process), produce auditable revert with evidence — not just re-apply blindly.

## Existing tools / non-AI check (do first)
- ShutUp10, W10Privacy, Tripwire-style file/reg monitors, DISM, MDM baselines (Intune), `lgpo.exe` diff.
- Almost certainly deterministic software problem (registry watcher + event log join). No model centrality evident.
- NVIDIA/Nebius gate later — likely REJECT for this hackathon on model-centrality, unless narrowed to a failure ordinary diff misses (tbd, don't force).

## Verdict
Good micro-problem for conventional software; weak hackathon fit as-is. Keep as cluster contrast: deterministic-drift vs UGC-triage.
