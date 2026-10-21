# 03 — 2D PRODUCTION

> Goal: build once, reuse forever. A new episode should need only ~20–30% new assets.

---

## 1. Asset tiers

```
TIER A — PERMANENT (build once)
 ├─ Bo: puppet rig + 18 face swaps + mood-light colour control + 12 key poses
 ├─ Recurring cast: Rae, Juno, Mr. Pickett, Mom, The Grey Raincoat
 ├─ Crowd kit: 1 generic body + 8 colour sets + 6 accessories
 ├─ Core backgrounds: BG01–BG08 (this repo)
 ├─ Graphics: DAY/HOUR counter, RULE/PROBLEM cards, letterbox, end card, logo sting
 └─ Audio: tap-tap SFX, 2 s sting, 3 music beds (comedy / tense / heartfelt)

TIER B — SEASONAL (4–8 episodes)
 ├─ Season locations (e.g. snowed-in school interior variants)
 └─ Grey Raincoat clue props

TIER C — PER EPISODE
 ├─ Unique sets/props (bunker cans, giant crumbs…)
 ├─ Science infographics
 └─ Power VFX (What If episodes)
```

## 2. Character assets (in this repo)

| Path | What |
|---|---|
| `art/characters/bo/bo_model_sheet.svg` | Master reference: turnaround, 18 expressions, 12 poses, mood light, palette |
| `art/characters/bo/expressions/bo_face_*.svg` | 18 head swaps, origin = head centre (import as a switch/swap layer) |
| `art/characters/bo/poses/bo_pose_*.svg` | 12 key poses (for thumbnails, storyboards and pose-to-pose animation) |
| `art/characters/bo/turnaround/bo_*.svg` | Front, 3/4, side, back |

**Rigging Bo (cut-out / puppet style):**
- Head = one group with a **face switch layer** (18 faces) + a **mood light colour** control on both cups.
- Limbs are single strokes → rig as 2-bone IK (shoulder–elbow–hand, hip–knee–foot).
- Torso is one shape; squash & stretch it for jumps and impacts.
- Tools that do this well: **Moho** (Smart Bones), **Toon Boom Harmony**, **After Effects + Duik Angela / Joysticks 'n Sliders**, **Cavalry**. Free: **OpenToonz**, **Synfig**, **Blender Grease Pencil**.

**Regenerating art:** all SVGs come from `tools/` (`bo.py`, `backgrounds.py`). Edit the Python and run:
```bash
python3 tools/build_art.py          # SVG only
python3 tools/build_art.py --png    # + PNG previews (pip install playwright pillow)
```

## 3. Backgrounds (1920×1080, layered for parallax)

Each SVG has layers `layer-sky`, `layer-far`, `layer-mid`, `layer-fg` (+ `layer-night-grade` where present). Split them for parallax.

| Code | File | Stage line (y px) | Used for |
|---|---|---|---|
| BG01 | `BG01_bedroom_day.svg` | 900 | Cold opens, epilogues, What If origins |
| BG01N | `BG01N_bedroom_night.svg` | 900 | Night scenes, insomnia, secrets |
| BG02 | `BG02_school_hallway.svg` | 930 | School POVs, chases, locker gags |
| BG03 | `BG03_classroom.svg` | 860 | Mr. Pickett's Lab (F8), science explainers |
| BG04 | `BG04_school_blizzard_night.svg` | 940 | EP01 snowed-in exterior |
| BG05 | `BG05_bunker.svg` | 900 | Bunker / survival POVs |
| BG06 | `BG06_abandoned_mall.svg` | 940 | Locked-in / apocalypse POVs |
| BG07 | `BG07_forest_night.svg` | 920 | Lost / camping / spooky POVs |
| BG08 | `BG08_kitchen_macro.svg` | 860 | Shrink episodes (ant scale) |

**Character scale:** Bo is 250 units tall in his source files.
- Medium-wide (standard): **scale 1.7** (≈ 425 px tall), feet on the stage line.
- Medium: 2.6 · Close-up (head only): 5.0 · Thumbnail face: 7–8.
- Previews of Bo placed on every background: `art/previews/*_with_bo.png` and `backgrounds_contact_sheet.png`.

**Night scenes:** put the `layer-night-grade` (navy #1B2350, multiply/45%) **above** characters too, so they sit in the same light. Add a warm rim on Bo if he gets lost.

## 4. Pipeline (per episode)

| Step | Tool (suggested) | Output |
|---|---|---|
| 1. Episode card + facts | `01_STORY_ENGINE.md §5`, `02_QA_CHECKLIST.md §5` | Filled card, fact table |
| 2. Storyboard + VO script | Markdown in `episodes/EPxx_*/` | `STORYBOARD.md`, `VO_SCRIPT.txt` |
| 3. Scratch VO | TTS (e.g. ElevenLabs) | Timing track |
| 4. Animatic | Storyboard Pro / Krita / poses from `art/` on a timeline | Locked-length animatic (±5%) |
| 5. Animation | Moho / Harmony / AE | Shots |
| 6. Final VO | Human VO or tuned TTS (one voice, whole series) | 48 kHz WAV |
| 7. Edit + text + SFX | DaVinci Resolve / Premiere / CapCut | 16:9 master |
| 8. Shorts | Reframe 9:16 from ✂️ points | 5 Shorts |

## 5. Delivery folder convention
```
episodes/EP01_POV_Snowed_In_With_Your_Crush/
  STORYBOARD.md   VO_SCRIPT.txt
  shots/          1.1.mp4, 1.2.mp4 …   (named by storyboard shot number)
  vo/             NARR_B1.wav … BO_3.4.wav, RAE_4.2.wav
  music/          comedy.mp3, tense.mp3, heartfelt.mp3
  sfx/            tap_tap.wav, bwomp.wav …
  thumbs/         A.png B.png C.png
```

## 6. 14-day schedule (one episode)

| Day | Task | Check |
|---|---|---|
| 1–2 | Pick idea, fill the episode card, research + verify facts | QA §5 |
| 3–4 | Storyboard + VO script | QA §1 |
| 5 | Scratch VO + animatic | Length ±5% |
| 6–10 | Animation | QA §2 |
| 11 | Final VO, music, SFX | QA §3 |
| 12 | Edit, text, letterbox, end card | Full watch-through |
| 13 | 3 thumbnails, 3 titles, 5 Shorts | QA §4 |
| 14 | Publish long-form + schedule Shorts | |

## 7. Release & growth

| When | Action |
|---|---|
| T−3 days | Short #1 (hook) as a teaser: "Full episode Saturday" |
| T0 (Sat, ~10:00 ET) | Long-form live. Pin a comment with the double question |
| T+1 → T+5 | One Short per day (#2–#5), each linked to the long-form via "Related video" |
| T+7 | Community poll: "Next POV: who are you trapped with?" (4 options) |
| Always | Reply to comments "as Bo" sometimes; heart every Grey Raincoat theory |

**Targets:** CTR ≥ 6% · 30-second retention ≥ 70% · AVD ≥ 45% · Shorts → long-form ≥ 2%.

## 8. Rough budget per episode (lean, 1–2 people)

| Item | Estimate |
|---|---|
| Animation software | $0 (OpenToonz/Blender) – $60/month |
| TTS voice | $10–30/month |
| Music/SFX licence | $0 (YouTube Audio Library) – $15/month |
| Time | 40–70 person-hours |

> Prices change often, so check current pricing before subscribing.
