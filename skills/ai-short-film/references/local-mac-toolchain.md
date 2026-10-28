# Local route on a 32 GB Apple Silicon Mac

Measured on a 32 GB Mac mini (M-series). Keep all models under one folder (`$MODELS`, e.g. `~/AI`)
and run **one GPU job at a time** through a lock:

```sh
#!/bin/bash
# gpu_run.sh LABEL cmd...: mkdir is atomic, so it works as a lock
: "${MODELS:?set MODELS to the models folder}"
LOCK="$MODELS/.gpu.lock"
until mkdir "$LOCK" 2>/dev/null; do
  # a SIGKILLed holder leaves the lock behind: clear it when its PID is gone
  pid=$(cat "$LOCK/pid" 2>/dev/null)
  if [ -n "$pid" ] && ! kill -0 "$pid" 2>/dev/null; then rm -rf "$LOCK"; continue; fi
  sleep 15
done
echo $$ > "$LOCK/pid"
trap 'rm -rf "$LOCK"' EXIT
caffeinate -i "${@:2}"
```

Use absolute paths everywhere (relative `--out-dir`s got nested, and concat lists broke), and write
outputs to `.part` first, renaming them only once ffprobe can read them, so interrupted runs can resume.

## Keyframes: FLUX.2-klein-4B (mflux, MLX, Apache-2.0)

- `mflux-generate-flux2-edit`, q8, 4 steps, `--low-ram` (footprint ~26.8 GB → ~11.7 GB), 1344×768, ~30–40 s.
- Image 1 = base (real location still), images 2+ = character sheets.
- Make the H3 input by scaling and cropping to fill the frame:
  `scale=768:448:force_original_aspect_ratio=increase:flags=lanczos,crop=768:448`. Never stretch.

## Final clips: MiniMax H3 (open weights, `h3.c` Metal port)

```sh
h3 -d $MODEL -p "<prompt>" --width 768 --height 448 --frames N --steps 20 --seed 42 \
   --reuse 2 --ssd-streaming --first-frame first.png [--last-frame last.png] [--ref-image ref.png ...] -o out.mp4
```

- `--ssd-streaming` is required on 32 GB. Peak ~10–11 GiB, no swap.
- Frames must be `5 + 17n`: round the needed count up (4 s → 107, 4.5 s → 124, 5.5 s → 141, 6.5 s → 158 at 24 fps).
  Width and height must be multiples of 32.
- Speed: ~130–160 s per second of video at 768×448/20 steps (fl2va); ref2va is ~170 s. `--reuse 1` is ~1.6× slower.
- Modes: fl2va (first frame alone is enough; skip the last frame unless you need it), ref2va (1–3 refs
  as `<Picture N>`), t2v.
- If the port only enables its fast path for a specific chip name, check the GPU source for chip-name
  checks before assuming your chip is slow. Patching them on a newer chip gave ~14 % in the source project.
- Download only the subfolder you need (`hf download ... --include "FL2VA/*"`; repeat `--include` per pattern).
- Licence: check territory exclusions and disclosure requirements; add an AI-disclosure end card.
- Watchdog worth copying: sample swap and memory pressure every 10 s, kill the job when swap grows
  ≥ 6 GB or pressure is critical three times in a row, log per run (seconds per video-second, peak RSS),
  retry with seed + 1000, and skip shots that can't finish before a deadline based on the measured rate.

## Motion preview: LTX-2.5 (community MLX CLI)

- `ltx-2-mlx generate --distilled --low-ram -W 768 -H 448 -f FRAMES --frame-rate 24 [--image first.png 0 1.0]`
- Frames `8n + 1`, max 241 (~10 s) on 32 GB. 768×448 runs at ~32 s per second of video (~22 GB peak). Native 1080p is not feasible.
- Use it for the animatic only: bodies and eyes are unstable. Do **not** feed its last frame into the
  final model as a last-frame anchor, because it carries wrong props and light back in.

## Music: MiniMax-Music3 (6-bit, mlx_audio)

```sh
python -m mlx_audio.music.generate --model $MODELS/minimax-music3/MiniMax-Music3-6bit \
  --caption "..." --lyrics "[instrumental]" --duration 75 --steps 30 --seed S --output inst_sS.wav
```

~3 min per seed; one result is often only 13–29 s long. Run several seeds (3, 5, 9, 13), check each
for vocals, and crossfade them into a bed. Commercial use needs the credit/disclosure in its licence.

## Voice: Kokoro-82M (mlx_audio)

- 24 kHz, fast (RTF ~0.25). Mandarin voices `zf_*` / `zm_*` with `lang_code="z"` (needs misaki zh, jieba,
  pypinyin, cn2an); English `af_*` / `am_*`.
- Trim edge silence, and speed a line up at most 1.15× to fit its shot; beyond that, shorten the line.
- Elderly and emotional voices sound young and flat. Record real people for those.

## Vocal check: Whisper (mlx_whisper, large-v3-turbo)

Run on every music piece and on generated clips: `--condition-on-previous-text False`. Pure music
often "hallucinates" short phrases like "Thank you." Treat a hit as vocals only when real words appear.

## ffmpeg on Homebrew

The default build may lack `drawtext` and `subtitles` (no freetype/libass). Render text with PIL
into transparent PNGs and `overlay` them (see `editing.md`), or install an ffmpeg build with libass.
Check the font for missing glyphs before rendering (STHeiti lacked "・" and "✌"; PingFang may be absent).
