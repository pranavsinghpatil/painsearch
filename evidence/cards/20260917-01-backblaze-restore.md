## Source
- URL: https://news.ycombinator.com/item?id=29533753
- Platform: HN
- Date posted: 2021-12-12
- Author: cloogshicer
- Engagement: 203 pts, 230 comments

## What is the person trying to do?
Verify home-computer backup is intact after "Safety Freeze" inconsistency error.

## Exact quoted pain
> "The only official solution is to manually check all files (millions in my case)."
> "I also can't download a full backup since Backblaze only allows downloads of up to 500GB at once."
> Support: "this [=manually checking all files] would in fact be the only sure fire way... There wouldn't be a way to compare hashes the way you describe in this case as that mechanism is simply not implemented"

## How often / how many people?
- 230 comments = repeated pattern, not singleton. Thread includes other restore horror stories.
- Frequency: rare per-user (restore-time) but catastrophic cost when it hits.

## Current workaround
- Manual file-by-file check (millions), or $189+customs (~300€ in EU) full HDD restore — which still doesn't say *which* files were corrupted.
- Split downloads into <500GB chunks.

## Why does the workaround fail?
- Doesn't scale: millions of files × manual = abandoned.
- Paid restore doesn't answer verifiability question (which files missing/corrupt?).
- Vendor confirms no local-vs-server hash cross-reference exists.

## What remains unsolved?
Verifiable discrepancy list: given local tree + remote manifest, produce exact diff (missing / mismatched / orphaned) without full download. Deterministic problem — hashes + manifest compare.

## Existing tools / non-AI check (do first)
- rclone check, restic check, Kopia, Arq, Borg — all do manifest-vs-local verification. Backblaze Personal lacks it.
- Simple solution likely deterministic software, not AI: expose server manifest + local hash walk.
- Do NOT claim AI needed. NVIDIA/Nebius gate later — no obvious model centrality here. Likely REJECT for this hackathon unless reframed to a model-central variant (not forced).

## Verdict
Strong pain, weak hackathon fit per hard constraints (deterministic fix, no central model capability). Keep as negative example / cluster reference.
