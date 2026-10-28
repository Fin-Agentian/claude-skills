# Workflow details

## G0 brief: ask on day one

- Length, aspect ratio, resolution, frame rate, file size and format limits of the upload.
- Contest or platform rules: is AI allowed, is disclosure required, are logos/brand marks required or banned, deadline (with time zone).
- Brand musts: real products and props (cup type, packaging, uniform), colours, real location photos, things never to show.
- Who watches it and where (phone in a messenger? big screen?). This decides the preview size and the caption size.
- Voices: real people available for dialogue? Language(s) for captions?
- Budget for cloud tools, and whether local-only is a requirement.
- What "good" looks like: ask for 2–3 reference films or stills **and say which part of each to borrow**
  (pacing and transitions only? style too?). In the source project the reference was "borrow the flow, not the style".

## Back-planning a deadline

Plan backwards from the deadline and keep a **fallback film** that is always deliverable (the
previous approved cut). Rough budget on the local route, one GPU job at a time:

| Step | Time measured on the local route |
|---|---|
| Keyframe candidate (FLUX.2-klein, 1344×768, 4 steps) | ~30–40 s each |
| Animatic clip (LTX, 512×288) | ~60–70 s each |
| Final clip (H3, 768×448, 20 steps) | ~130–160 s per second of video |
| 16 clips / ~76 s of material | ~3.2 h |
| Music (Music3, one seed) | ~3 min |

Rules of thumb:
- Put the risky shots (hand-offs, wide multi-person, climax) at the **front** of the queue.
- Budget at least 2 takes per key shot (or ≥ 50 % more material than the cut needs). 76 s of single-take
  material for a 60 s cut (27 % extra) was not enough: four clips had to be trimmed hard.
- Leave the last day for edit, sound and QC only.
- Do the work that doesn't depend on decisions while waiting for sign-off: collect location
  photos, test the upload, set up the edit script, prepare the fallback.

## Multi-model roles that worked

- A strong model writes the script and storyboard; a different model reviews it (logic holes,
  brand claims, "can the model render this", seconds per line). Re-review after the fixes.
- Cheaper models do data plumbing (JSON from tables, file moves).
- A separate review of the rough cut with measurements (loudness per 0.25 s window, gaps,
  continuity) found problems the maker missed, such as digital silence between lines.
