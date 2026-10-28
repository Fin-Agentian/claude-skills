# Editing and sound with ffmpeg

## Cut each shot from its gen

```sh
ffmpeg -ss $TRIM_IN -t $DUR -i gen.mp4 \
  -vf "${FIX_VF:+$FIX_VF,}fps=24,setpts=PTS-STARTPTS" \
  -af "volume=0:enable='lt(t,${MUTE_HEAD:-0})',asetpts=PTS-STARTPTS" \
  -c:v libx264 -crf 14 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k shot.mp4
```

- `mute_head` silences the mumbled speech some models add at the start of a clip.
- Garbled text in the frame can be blurred locally: `crop=w:h:x:y,boxblur=6:3` for small areas
  (14:7 for large ones; a large radius on a 32 px crop fails with "Invalid argument"), then overlay it back.

## Per-shot render (one filter_complex per shot)

- Upscale and pad: `fps=24,scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,setsar=1,tpad=stop_mode=clone:stop_duration=$D,trim=duration=$D`
- Lock the frame count with `-frames:v round(D*24)` so the concatenated shots never drift.
- Render the clean and the captioned version in the same pass (`split=2`).
- A missing clip becomes a black "(TBD)" placeholder instead of an abort, so the cut stays reviewable.

## Text without drawtext/libass

Render each caption or title card with PIL as a transparent PNG (white text, black outline,
line-breaking rules, file named by content hash) and composite it:

- caption: `overlay=(W-w)/2:H-h-64:enable='between(t,A,B)'`
- title card: `format=rgba,fade=in:st=0:d=0.3:alpha=1,fade=out:st=X:d=0.3:alpha=1` then overlay

Keep production notes out of on-screen strings. A note like "(flash at end of segment)" made it into a final card.
Export clock/time cards also as an editable SRT plus a transparent PNG layer, so the client can retype them.

## Sound

1. Per shot: the clip's own audio at `ambient_db` (−18 under dialogue, −6 otherwise) + each voice line
   placed with `adelay=ms|ms`, `amix=normalize=0`, then `apad` and `atrim` to the shot length (`anullsrc` if the clip has no audio).
2. Under everything: a room tone, e.g. brown noise with `lowpass=500,highpass=60` at ~−35 dBFS. Gaps measured −66 dB
   (sounds like a broken file) before, −38 dB after. Leave true silence only where it is a deliberate beat.
3. Music bed ducked under dialogue:
   `sidechaincompress=threshold=0.02:ratio=6:attack=30:release=500`, bed at −14 dB, fade in 1.5 s / out 2.5 s.
   Bring the music in at the emotional turn rather than wall-to-wall. A deliberate drop to silence at the reveal lands harder.
4. Two-pass `loudnorm` to −16 LUFS, TP −1.5, LRA 11 (measure with `print_format=json`, then apply
   `measured_*` with `linear=true`).
5. Pitch-match music pieces from different seeds (`rubberband`) before crossfading.

## Assemble and deliver

- Concat the shot files with `-c:v copy`, mux the mixed audio (AAC 192k), `-movflags +faststart`, `-shortest`.
- Add the disclosure end card (2 s) when licences require it; abort the build if its font lacks a glyph.
- Deliver: 1080p master (with and without captions) + a 720p preview under the messenger's size limit
  (a 68 MB master did not fit a 30 MB limit; the 720p was 8.5 MB).
- Check the preview **with sound** before sending it. A "there is no sound" report wasted a round trip.

## Edit rhythm (measured on a reference film: 127 shots)

Average ~4.2 s per shot, median 3 s, 87 % hard cuts, almost no dissolves. The flow comes from cut
points and continuous sound. Jump one or two shot sizes at a time, keep left/right in shot–reverse-shot,
cut on action, and cover continuity seams with inserts (hands, props). J- and L-cuts are done in the edit;
models won't produce them from prompts.
