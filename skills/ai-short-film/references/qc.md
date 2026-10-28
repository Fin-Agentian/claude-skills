# Quality control

## Per clip, before it goes into the edit

```sh
python scripts/qc_sheet.py gens/*.mp4 --out-dir qc --threshold 0.3
```

It writes one contact sheet per clip and reports scene changes. A generated clip is one shot, so any
scene change inside it is a suspect (composition switch, a duplicate person). Exit code 1 = at least
one suspect, 2 = a clip could not be read (the rest are still checked).
Look at the sheets and at 2 fps around the flagged time.

Checklist (all must pass, else trim or regenerate):

- [ ] First frame matches the approved character sheet and location still
- [ ] No composition change mid-clip (qc_sheet) and no duplicate people, extra hands, merged limbs
- [ ] One camera move, no head or body leaving frame unexpectedly
- [ ] No readable or garbled text (or it can be blurred or cropped)
- [ ] Props and counts match the neighbouring shots (food, cups, uniform, hair, skin tone)
- [ ] Usable length ≥ what the shot needs, plus a spare second
- [ ] Clip audio has no stray speech (Whisper; words, not "Thank you." hallucinations)

Fix order: **trim** the bad part (the timeline may need re-flowing), **then** regenerate with a
changed prompt (direction, framing, an explicit "stays inside the frame"). A new seed alone rarely
fixes structural drift. Regenerating cost ~13 min per clip on the local route.

Track per clip: takes, pass/fail, seconds of usable material, generation time. Pass rate and
"minutes per usable second" are how you compare tools and plan the remaining queue.

## Rough cut review (G4)

- Find silent gaps with `silencedetect=noise=-45dB:d=0.4` (or loudness per 0.25 s window) and fill the
  ones that aren't deliberate.
- Integrated loudness −16 LUFS ±1, true peak ≤ −1.5 dB.
- Every dialogue line ends inside its shot; captions match the audio.
- Continuity pass across neighbouring shots (hair, outfit, props, light direction, screen direction).
- Font glyph check for every caption and card.
- Re-run the review after fixes. The source project skipped the second review once and shipped
  known issues.
