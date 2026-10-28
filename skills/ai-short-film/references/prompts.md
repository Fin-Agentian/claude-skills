# Prompt templates

## LLM: script

```
Write a {length}-second {aspect} short film for {brand/purpose}. Audience: {who}.
Constraints:
- 3-second hook, situation clear by 7 s, a payoff or turn before 21 s, the turn at or before the midpoint.
- At most 2 main characters on screen at once, at most 2 locations, dialogue under {n} lines,
  about 2.5 Chinese characters (or 2–3 English words) per second.
- The turn must be visible in pictures, not only said.
- Avoid: readable text in frame, exact object counts, hand-offs between people, crowds,
  people walking toward camera, screens/phones, brand claims the brand has not made.
Output: logline; characters with ONE fixed visual line each; beats; dialogue table (time, speaker, line);
on-screen text list; a feasibility table listing every risky shot and its safer alternative.
```

## LLM: storyboard to data

```
Turn this script into two JSON lists:
gens: one generated clip per row: id, duration_sec (≤ 6), anchor description, mode (fl2va/ref2va),
      prompt_en using Scene/Characters/Action/Camera/Look/Audio, used_by.
shots: one edit shot per row: id, beat, duration_sec, gen_id, trim_in_sec, dialogue, overlay_text.
Rules: one action and one camera move per gen; reuse a gen for several shots where the framing repeats;
total shots duration = {length} s; 3–5 s per shot, emotional shots up to 8 s; mostly hard cuts.
```

## Image-to-video prompt (natural sentences, one move)

```
Scene: {location, time of day, light}.
Characters: {fixed character line, verbatim every time}; the same characters as in the first frame.
Action: For the first second {state}. Then {one action}, {where in frame}.
Camera: {one move with size and speed}, e.g. "The camera pushes in slowly with small amplitude toward her face."
Look: {style constant}, consistent on-model design, no readable text anywhere, no letters on signs, cards or bags.
Audio: {ambience}, no music, no speech.
```

- Write timing as "for the first N seconds … then …". Do not use "then/接著" chains of several actions.
- Say where people are and where they face; forbid the failure explicitly:
  "his whole body including his head stays inside the frame", "never comes closer to the camera than the table".
- The H3-style open models take plain English camera sentences. Bracket syntax like `[Push in]` belongs to
  other products (older Hailuo); check each tool's own guide.
- Stable moves: locked-off, slow push in, pull out, single pan or tilt, follow, slow orbit.
  Fragile: stacked moves, handheld shake on faces, whip pans, fast push-ins, contradictory instructions.
- Negative prompts: short, aimed only at defects that keep recurring. They do not fix identity drift.

## Keyframe edit prompt (FLUX.2-style edit with reference images)

```
Redraw image 1 in {style}. Use the girl from image 2 and the man from image 3.
Exactly two people only. Keep the counter, the window and the camera angle exactly the same.
Do not add any extra people, cups, text or signs. {One change only: relight / swap the cup / remove the person}.
```

Reliable: relighting, swapping a prop, removing a person, restyling. Unreliable: adding a second
item, putting a specific face into a shadowed figure (it may draw the person twice).
Make 2 candidates per frame (seeds 42 and 7), pick one, and write the pick back into the data.

## Style constant example (manhwa)

```
Korean webtoon (manhwa) animation style, clean thin lineart, soft cel shading with airbrushed gradients,
luminous skin, big expressive eyes with highlights, warm pastel palette, soft bloom, consistent on-model character design
```

Lock one style constant and paste it into every prompt verbatim.

## Music prompt (MiniMax-Music3 style)

```
--caption "Warm acoustic guitar and soft piano, 92 BPM, hopeful morning mood. Purely instrumental, no vocals, no singing, no humming."
--lyrics "[instrumental]"
```

Section tags such as `[intro][verse]` make it sing. A single `[instrumental]` tag can end early,
so run several seeds and crossfade the pieces into a bed.
