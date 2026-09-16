# Discovery Test — kill fast
For each clustered pattern (5-8), score 0-5 with a link as proof. Kill if any zero.

1. **Exact pain**: What task fails / costs too much / neglected? Who pays? How often?
2. **Existing alternatives**: How solved today? Link to product / OSS / script. What did you try prompting in ChatGPT and where did it fail?
3. **Capability gap**: What can NVIDIA open models do that others struggle with? Must be central, not UI. Name family: Nemotron-3-Ultra/Nano/Super, Cosmos, GROOT, Sonic, Nemo.
4. **Verifiable result**: How to measure? (precision/recall on timestamps, caught failures vs tests, discrepancy F1, latency/cost on Nebius). Need ground truth dataset for demo.
5. **Hackathon feasibility**: Can 2-4 people demo in <3min video + live endpoint? Needs: data access, Token Factory model available, Serverless Endpoint/Job fit.

Weak -> Strong examples (directions only, not ideas):
- summarize hours of video -> detect specific event across continuous footage, precise timestamps + evidence
- chat with papers -> narrowly defined inconsistency across evolving evidence
- coding agent -> catch specific failure ordinary tests/review miss
- analyze docs -> reconcile conflicting changing records, verifiable discrepancy
- general assistant -> bounded task where correctness independently checked

Gate: if solvable by prompt alone, or NVIDIA is just interface, or Nebius does nothing — drop.
