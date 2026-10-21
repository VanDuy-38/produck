# EP01 — automatic animatic

`shots.py` is the storyboard (`../STORYBOARD.md`) as data: 58 shots with set, cast, poses, faces, mood light / ponytail state, props, camera move, HUD (day counter, cards, letterbox), scratch VO, SFX and music cue. `tools/animatic.py` turns it into a video.

## Build

```bash
# one-time: scratch TTS voice (Kokoro, runs offline on CPU)
pip install kokoro-onnx soundfile playwright pillow numpy
mkdir -p /root/tts && cd /root/tts
curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
curl -L -o kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
# (or set KOKORO_DIR to wherever those two files live)

python3 tools/animatic.py episodes/EP01_POV_Snowed_In_With_Your_Crush/animatic/shots.py            # full video
python3 tools/animatic.py episodes/EP01_POV_Snowed_In_With_Your_Crush/animatic/shots.py --only 4.1,4.2   # preview shots
python3 tools/animatic.py episodes/EP01_POV_Snowed_In_With_Your_Crush/animatic/shots.py --stills    # contact sheet only
```

Outputs (in `../`): `EP01_animatic.mp4` (1280×720, 24 fps, −14 LUFS) and `EP01_animatic.srt`. Working files go to `animatic/build/` (git-ignored; TTS is cached there, so re-runs only re-voice lines you changed).

## What it is / isn't

- **Is:** a locked-timing animatic for checking story, pacing, VO length, joke timing and shot coverage. Timecodes follow the storyboard; a shot only grows if its VO overflows.
- **Isn't:** final animation. Poses are held key poses with face/light swaps and camera moves. Voices are scratch TTS (narrator `am_michael`, Bo `am_puck`, Rae `af_bella`). Music and SFX are synthesized placeholders. Replace all three before publishing (see `docs/03_PRODUCTION_2D.md §4`, steps 5–7).

## Voices (`tools/animatic.py → VOICES`)

| Speaker | Kokoro voice | Speed |
|---|---|---|
| NARR | am_michael | 1.0 |
| BO | am_puck | 1.08 |
| RAE | af_bella | 1.05 |
| RADIO / PLOW / FIREFIGHTER | am_eric / am_onyx / am_fenrir | ~1.0 |

## New sets used (from `tools/ep01_sets.py`)

BG09 library + fort · BG09I inside the fort · BG10 gym (dark) · BG11 front doors buried · BG12 window (storm / field / dawn, snow fill 0–1) · BG13 science room + emergency shelf · BG14 hallway, power out, vending machine · BG04D school at dawn + snowplow · chalkboard math · 8 science graphics · firefighter guest · Grey Raincoat.
