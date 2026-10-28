# Data formats

Keep the plan as data that scripts read. Edits then mean changing one row and re-running.

## gens.json: one row per generated clip

```json
{
  "title": "...", "fps": 24, "width": 768, "height": 448,
  "gens": [
    {
      "id": "A",
      "duration_sec": 4.5,
      "used_by": ["S01", "S07", "S15"],
      "anchor_first": "keyframes/A.png",
      "anchor_last": null,
      "mode": "fl2va",
      "refs": [],
      "prompt_en": "Scene: ... Characters: ... Action: ... Camera: ... Look: ... Audio: ... no music, no speech.",
      "preview_prompt_en": "...",
      "takes": 2
    }
  ]
}
```

`mode`: `t2v` (text only), `fl2va` (first frame, optional last frame), `ref2va` (1–3 reference
images, referenced in the prompt as `<Picture N>`).

## shots.json: one row per edit shot

```json
{
  "title": "...", "fps": 24, "width": 1920, "height": 1080, "end_card_sec": 2,
  "shots": [
    {
      "id": "S01", "beat": "1a", "start_sec": 0.0, "duration_sec": 3.0,
      "gen_id": "A", "trim_in_sec": 0.6,
      "mute_head_sec": 0.0,
      "fix_vf": "",
      "ambient_db": -6,
      "overlay_text_zh": "06:45",
      "dialogue": [{"speaker": "GRANDMA", "zh": "...", "en": "...", "start_offset_sec": 0.4}]
    }
  ]
}
```

- `start_sec` is cumulative. Generate it from a short row table in Python instead of typing it.
- `trim_in_sec` lets one gen feed several shots and skip a bad opening, such as a head leaving the frame.
- `fix_vf` is an ffmpeg filter applied while cutting, e.g. a local `crop+boxblur` over garbled text.
- `ambient_db`: −18 under dialogue, −6 without, so the clip's own sound keeps the gaps alive.
- Validate before editing: unique ids, duration > 0, start_sec equals the running total, every
  line fits `duration - start_offset` at the measured voice length.

## Storyboard table (for humans)

`# | time | beat | shot size | angle | camera move (type + speed) | picture / action | dialogue | sound | on-screen text | transition | refs | continuity notes | risk / fallback`

Add a fixed "location bible" next to it: sign position, counter direction, window/light side,
chair colours, table props, and the 180° line. Plus a "face light level 1–5" column if the story
arc is about light.

## Camera plan

1. Top-down ASCII floor plan with the 180° line and numbered camera positions.
2. Camera table: position, equivalent focal length, height, which shots use it.
3. Per-shot table: camera, size, move, reference technique.
4. Rhythm notes: which shots repeat the same framing on purpose (the same empty shot on each new day).

Keep screen direction constant: a character moving toward their goal always moves the same way
across the frame. Keep the light source on one side.

## Script layout

Logline → characters (fixed one-line look, reused verbatim in every prompt) → locations →
beats (setup / development / turn / payoff) → dialogue table (time | who | line | note) →
on-screen text list → light/colour rules.

Review report layout: verdict → must-fix (problem / fix) → should-fix → keep → feasibility
table (risk | where | handling) → seconds before/after.
