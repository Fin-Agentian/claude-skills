# Pitfalls and fixes (from a real production)

## Process

| What happened | Fix |
|---|---|
| Three looks (realistic → American 2D → manhwa) meant two full redos, each after hours of generation | Gate G2: one style, signed off on stills before any video |
| The client promised "what I expect it to look like", it never came, and the pipeline ran on the AI's own pick | Wait, or ask with 2–3 concrete options; don't proceed on silence |
| Brand prop (cup type), contest rules and AI policy were checked mid-production | G0 on day one |
| Sound design came last, and the client reported "no sound" | Plan sound in the storyboard; preview with sound at G4 |
| Script had logic holes and implied a brand policy | Second-model script review before storyboard |
| Fixed version shipped without a second review | Re-review after fixes |
| Master too big for the messenger | Ask the viewing channel at G0; always make a small preview |

## Picture

| Symptom | Fix |
|---|---|
| Clip switches composition or shows a duplicate mid-way (4 of 16 clips) | `qc_sheet.py` → trim; split one gen into 2–3 edit shots |
| Climax shot cut from 3.0 s to 1.2 s because of a duplicate | Don't rest the climax on a risky shot; generate it first, with takes and a fallback angle |
| Character walking toward camera loses the head, then returns as another person | Change the direction in the prompt (back to camera, stays mid-frame); a new seed doesn't help |
| First 0.6 s has the head out of frame | `trim_in_sec` |
| "Two plates" renders one | Make it an action (sets down a second plate) |
| Garbled signs, cards and boards | No text in prompts ("no readable text anywhere"); blur/crop; add text in post |
| Wrong cup or prop keeps returning | Fix it in the first frame; use reference images (ref2va); name the banned props in the prompt |
| "Cold light" prompt ignored | The first frame decides the light: relight the keyframe |
| Preview model's last frame used as an anchor drags wrong props back in | Use only the corrected first frame for the final model |
| Hair, skin or uniform drift across shots | Fixed character line verbatim in every prompt; one video tool per character; accept or regenerate |
| 768×448 upscaled to 1080p looks soft | Known ceiling of the local route; use cloud tools for hero shots if the budget allows |

## Sound

| Symptom | Fix |
|---|---|
| −66 dB digital silence between lines | Clip ambience + room tone (~−35 dBFS) |
| Model adds mumbled speech to clips with dialogue | `mute_head_sec`, low `ambient_db` under VO, "no music, no speech" in the prompt |
| Music sings when given section tags | `[instrumental]` only + "no vocals, no singing, no humming" in the caption |
| Music ends after 13–29 s | Several seeds, crossfade, pitch-match |
| Whisper "hears" words in pure music | Count only real words as vocals |
| TTS grandma sounds young | Real voice recording |

## Environment

| Symptom | Fix |
|---|---|
| ffmpeg has no drawtext/subtitles | PIL PNG overlays |
| Font missing "・", "✌" | Glyph check; swap the character or the font |
| Relative paths nested or broke concat lists | Absolute paths everywhere |
| Two GPU jobs at once → swap storm | One lock-guarded queue; watchdog |
| Interrupted runs leave half files | Write `.part`, verify with ffprobe, rename; skip existing on resume |
| Shared output names overwrote an earlier version | One folder per version |
| System Python couldn't load PIL | Run each tool in its own venv with `python -I` |
| `pgrep -f "python3 x.py"` misses the process | Match on the script name, or wait on the PID |
