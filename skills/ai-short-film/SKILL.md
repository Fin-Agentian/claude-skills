---
name: ai-short-film
description: Produce a short AI-generated film (15–120 s, ads, micro-films, contest entries) end to end — script, storyboard, character and location lock, keyframes, image-to-video generation, edit, sound, QC and delivery — with sign-off gates so the client approves the look before hours of generation are spent. Distilled from a real 60-second production on a 32 GB Apple Silicon Mac (local FLUX.2-klein, MiniMax H3, LTX-2.5, MiniMax-Music3, Kokoro, Whisper, ffmpeg) plus research on cloud tools (Kling, Seedance/Jimeng, Veo, Runway, Hailuo).
when_to_use: AI video, AI short film, micro-film, AI 短片, AI 微電影, 產影片, 做影片, 影片製作, 分鏡, 運鏡, 腳本, 劇本, storyboard, shot list, camera moves, image-to-video, 圖生影片, text-to-video, keyframes, 首幀, 角色一致, character consistency, H3, LTX, Kling, 可靈, Seedance, 即夢, Veo, Runway, Hailuo, 海螺, FLUX, 配樂, 配音, 字幕, ffmpeg 剪接
---

# ai-short-film — lock the look first, then generate

Generation is the expensive step (a local 60 s film is 3+ hours of GPU time; cloud tools cost credits).
Every hour lost in the source production came from generating before the client had approved what
the film should look like. So the workflow is a sequence of **gates**: nothing downstream starts
until the gate above it is signed off.

## The gates (ask, then wait — never "proceed with my recommendation")

| Gate | Show the client | Sign-off needed before |
|---|---|---|
| G0 Brief | Rules (length, aspect, AI policy, logo/brand rules, deadline, upload size), brand musts (props, colours, real shop photos), audience, where it will be watched | writing anything |
| G1 Story | Logline + beat sheet + dialogue list, and a "model can't do this" check (see below) | storyboard |
| G2 Look | **One** style, character sheets (front/side, fixed outfit), location stills, 3–5 key frames | any video generation |
| G3 Animatic | Cheap motion preview or still-frame animatic with temp sound, timed to the final length | full-quality generation |
| G4 Rough cut | Low-res cut with sound already audible | final mix, grade, captions |

If the client says "I'll send you what I want it to look like", wait for it. Do not run the
pipeline on your own pick. Changing style after generation means regenerating everything
(the source project went through three looks, which meant two full redos, each after hours of generation).

## Write the story for what models can actually render

Before G1, strike or rewrite anything on this list. Each item either failed in production or is a
documented weak spot of current video models:

- Readable text in the frame (signs, cards, menus, screens): it comes out garbled. Add text in post.
- Exact counts ("two plates on the tray"): unreliable. Make the count an action (she sets a second plate down).
- Hand-offs and body contact between two people (passing a tray, holding hands): limbs merge or a
  duplicate appears. Cut to a hand/prop close-up instead.
- Small figures in wide shots, crowds, 3+ people in frame: identity drifts, people duplicate.
  Keep one or two people per shot.
- A character walking toward the camera: the head leaves frame and comes back as someone else.
- Several actions or camera moves in one shot. Rule: **one shot = one action = one camera move**.
- Story turns carried only by dialogue. Tell the turn in pictures, keep dialogue to a few lines.
- Putting the film's emotional climax on one of the risky shots above. If you must, generate it
  first, with extra takes and a fallback angle (back view + prop close-up).
- Claims that speak for the brand (a "policy" the brand never announced).

## Production order

1. **Brief & rules** (G0): see `references/workflow.md` for the question list.
2. **Script** (G1): logline, characters with fixed one-line looks, beats, dialogue table,
   on-screen text list. Dialogue budget about 2.5 Chinese characters per second; it must fit the shot.
   Have a second model review it for logic holes, brand risk and feasibility.
3. **Storyboard & shot list**: two layers, kept as data, not prose (`references/formats.md`):
   - *gens*: one row per generated clip (duration, first/last frame, mode, refs, prompt).
   - *shots*: one row per edit shot (which gen, trim-in, duration, dialogue, overlay text, ambience level).
   One generated clip can feed 2–3 edit shots. Reusing clips saves generation time, and repetition
   can work as a storytelling device.
4. **Look lock** (G2): character sheets and location stills, then first frames, produced as
   2+ candidates per frame. The client or you pick one, and the pick is written back into the data.
   Fix the first frame (props, light, people count) **before** turning it into video, because the
   first frame decides colour and light. Prompting "cold light" over a warm first frame does nothing.
5. **Animatic** (G3): fast low-res motion preview or timed stills.
6. **Generate**: image-to-video from the locked first frames, one GPU job at a time, logged and
   resumable, writing to `.part` first. Budget 2+ takes for key shots. Templates are in `references/prompts.md`.
7. **QC every clip** before editing: `scripts/qc_sheet.py clips/*.mp4` builds contact sheets and
   flags mid-clip scene changes (composition drift or duplicates). Fix order: trim out the bad
   part, then regenerate with a changed prompt. Changing only the seed rarely fixes a structural
   problem. See `references/qc.md`.
8. **Edit** (G4): cut on action, mostly hard cuts, vary shot length, insert close-ups over
   continuity gaps. Sound comes before polish (`references/editing.md`).
9. **Sound**: dialogue (prefer real voices for elderly or emotional lines; TTS sounds young and flat),
   ambience or room tone under every gap (digital silence reads as a broken file), music ducked
   under speech, loudness-normalised to −16 LUFS.
10. **Deliver**: 1080p master, a no-captions version, a small preview that fits the messenger's size
    limit, and an AI-disclosure end card when the model licences require it.

## Tool choice

- Prefer image-to-video over text-to-video, and keep one video tool per character for consistency.
- Local Apple Silicon route (works on 32 GB): see `references/local-mac-toolchain.md` for exact
  commands, frame rules, memory switches and measured speeds.
- Cloud tools: A/B-test them on the same three locked first frames (single face, hand-off,
  two-person wide) before committing. Pick on pass rate and cost per usable second, not on demo reels.
- Check licences when you choose the tools, not at delivery: territory limits, commercial use,
  disclosure text.

## Report to the user at each gate

One short message: what is ready to look at (paths or a preview under the upload limit), the
decision you need, and what you will generate after they answer, with time or cost. Then stop and
wait for the answer.

## References

- `references/workflow.md`: gate questions, schedule back-planning, fallback film
- `references/formats.md`: gens/shots JSON, storyboard columns, camera plan, script layout
- `references/prompts.md`: LLM script and storyboard prompts, image-to-video and keyframe prompt templates
- `references/local-mac-toolchain.md`: FLUX.2-klein, MiniMax H3, LTX-2.5, Music3, Kokoro, Whisper on a 32 GB Mac
- `references/editing.md`: ffmpeg recipes (cut, scale, captions without libass, ducking, loudnorm)
- `references/qc.md`: per-clip checklist, QC tooling, review pass
- `references/pitfalls.md`: everything that broke, with fixes
