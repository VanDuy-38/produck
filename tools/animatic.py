#!/usr/bin/env python3
"""Automatic animatic builder: storyboard shot list -> MP4 with scratch VO, music, SFX, subtitles.

    python3 tools/animatic.py episodes/EP01_POV_Snowed_In_With_Your_Crush/animatic/shots.py
    python3 tools/animatic.py <shots.py> --only 4.1,4.2      # render a few shots (preview)
    python3 tools/animatic.py <shots.py> --stills            # contact sheet only, no video
    python3 tools/animatic.py <shots.py> --mux               # re-mix audio + re-mux from existing clips

Pipeline per shot: compose SVG panels (background + cast + props) and a HUD layer
(counter, cards, letterbox) -> PNG via headless Chromium -> camera move in PIL ->
H.264 clip. Audio: Kokoro TTS lines (cached), procedural music beds, synthesized
SFX, ducking, loudness-normalised to -14 LUFS in the final mux.

Shot spec keys (all optional except id/bg):
  id, bg=(SET_KEY, {kwargs}), cast=[...], props=[(svg,x,y,s)], props_front=[...],
  counter="DAY 1", card="7 DAYS" | (text, x, y, size), letterbox=bool,
  cam=dict(z0,z1,cx0,cy0,cx1,cy1,shake), panels=[{"at":0.5, ...overrides}],
  vo=[(SPEAKER, text), ...], vo_at=seconds, sfx=[(name, t)], music="comedy|tense|heart|swell|hero|none|keep"
Cast item: dict(who="bo|rae|ff|raincoat", pose, face, mood|tail, x, s=1.7, y=None, flip, rot,
  head=True (head only, y = head centre), shirt="#hex", extra=svg, opacity)
"""
import hashlib
import importlib.util
import json
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bo  # noqa: E402
import rae  # noqa: E402
import ep01_sets as sets  # noqa: E402
from backgrounds import STAGE_LINE  # noqa: E402

W, H = 1920, 1080
OW, OH = 1280, 720          # animatic output size
FPS = 24
SR = 24000
INK = "#1F2A44"
LETTERBOX = round((H - W / 2.39) / 2)

VOICES = {"NARR": ("am_michael", 1.0), "BO": ("am_puck", 1.08), "RAE": ("af_bella", 1.05),
          "PLOW": ("am_onyx", 0.95), "FIREFIGHTER": ("am_fenrir", 1.0), "RADIO": ("am_eric", 1.0)}
TTS_DIR = os.environ.get("KOKORO_DIR", "/root/tts")


# ============================================================ composition
def _char_svg(c):
    who = c.get("who", "bo")
    if who == "bo":
        if c.get("view"):
            svg = bo.turnaround(c["view"])
        elif c.get("head"):
            svg = bo.head(c.get("face", "neutral"), "front", c.get("mood"))
        else:
            svg = bo.body(c.get("pose", "idle"), c.get("face"), c.get("mood"))
        if c.get("shirt"):
            svg = svg.replace(bo.JACKET, c["shirt"])
    elif who == "rae":
        svg = rae.head(c.get("face", "neutral"), "front", c.get("tail")) if c.get("head") else \
            rae.body(c.get("pose", "idle"), c.get("face"), c.get("tail"))
        if c.get("wrapped"):  # Bo's red jacket over her hoodie
            svg = svg.replace(rae.HOODIE, bo.JACKET).replace(rae.HOODIE_SHADE, "#E85A5A")
    elif who == "ff":
        svg = sets.firefighter(c.get("face", "neutral"), c.get("pose", "idle"))
    elif who == "raincoat":
        return sets.grey_raincoat(c["x"], c.get("y", 1000), c.get("s", 1.0), c.get("opacity", 1.0))
    else:
        raise ValueError(who)
    svg += c.get("extra", "")
    s = c.get("s", 1.7)
    if c.get("head"):
        y = c.get("y", 540)
    else:
        y = c.get("y") if c.get("y") is not None else c["stage"] - 194 * s
    fx = -1 if c.get("flip") else 1
    rot = c.get("rot", 0)
    op = c.get("opacity", 1)
    return (f'<g transform="translate({c["x"]},{y}) rotate({rot}) scale({s * fx},{s})" opacity="{op}">{svg}</g>')


def _place(items):
    out = []
    for it in items or []:
        svg, x, y = it[0], it[1], it[2]
        s = it[3] if len(it) > 3 else 1
        out.append(f'<g transform="translate({x},{y}) scale({s})">{svg}</g>')
    return "".join(out)


def scene_svg(spec):
    key, kw = spec["bg"] if isinstance(spec["bg"], tuple) else (spec["bg"], {})
    svg = sets.SETS[key](**kw)
    stage = STAGE_LINE.get(key, 930)
    cast = []
    for c in spec.get("cast", []):
        c = dict(c)
        c.setdefault("stage", stage)
        cast.append(_char_svg(c))
    insert = _place(spec.get("props")) + "".join(cast) + _place(spec.get("props_front"))
    marker = '<g id="layer-fg">'
    i = svg.find(marker)
    svg = svg[:i] + insert + svg[i:] if i >= 0 else svg.replace("</svg>", insert + "</svg>")
    if spec.get("overlay"):
        svg = svg.replace("</svg>", spec["overlay"] + "</svg>")
    if spec.get("dark"):
        svg = svg.replace("</svg>", f'<rect width="{W}" height="{H}" fill="#000" opacity="{spec["dark"]}"/></svg>')
    return svg


def _caps(t, x, y, size, fill="#FFFFFF"):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial Rounded MT Bold, Arial, Helvetica, sans-serif" '
            f'font-size="{size}" font-weight="900" fill="{fill}" stroke="{INK}" stroke-width="{max(6, size // 8)}" '
            f'stroke-linejoin="round" paint-order="stroke">{t}</text>')


def hud_svg(spec, shot_label):
    s = []
    top = LETTERBOX if spec.get("letterbox") else 0
    if spec.get("counter"):
        t = spec["counter"]
        w = 40 + 30 * len(t)
        s.append(f'<g transform="translate(48,{top + 40})"><rect width="{w}" height="84" rx="16" fill="#FFD23F" '
                 f'stroke="{INK}" stroke-width="6"/>'
                 f'<text x="{w / 2}" y="60" text-anchor="middle" font-family="Arial Rounded MT Bold, Arial, Helvetica, sans-serif" '
                 f'font-size="48" font-weight="900" fill="{INK}">{t}</text></g>')
    card = spec.get("card")
    if card:
        if isinstance(card, str):
            card = (card, 960, 880 if not spec.get("letterbox") else 860, 120)
        s.append(_caps(*card))
    if spec.get("title"):
        s.append(f'<rect width="{W}" height="{H}" fill="#1B2350"/>' + _caps(spec["title"], 960, 600, 200, "#FFD23F"))
    s.append(f'<text x="{W - 28}" y="{H - 24 - (LETTERBOX if spec.get("letterbox") else 0)}" text-anchor="end" '
             f'font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="700" fill="#FFFFFF" opacity=".55">'
             f'ANIMATIC · {shot_label}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{"".join(s)}</svg>'


class Renderer:
    def __init__(self):
        from playwright.sync_api import sync_playwright
        self._p = sync_playwright().start()
        self.browser = self._p.chromium.launch()
        self.page = self.browser.new_page(viewport={"width": W, "height": H})

    def png(self, svg, path, transparent=False):
        bg = "transparent" if transparent else "#000"
        self.page.set_content(f'<html><body style="margin:0;background:{bg}">{svg}</body></html>')
        self.page.screenshot(path=path, omit_background=transparent)

    def close(self):
        self.browser.close()
        self._p.stop()


# ============================================================ audio: TTS
_kokoro = None


def tts(text, speaker, cache):
    voice, speed = VOICES[speaker]
    h = hashlib.sha1(f"{voice}|{speed}|{text}".encode()).hexdigest()[:16]
    path = os.path.join(cache, f"{speaker}_{h}.npy")
    if os.path.exists(path):
        return np.load(path)
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(os.path.join(TTS_DIR, "kokoro.onnx"), os.path.join(TTS_DIR, "voices.bin"))
    clean = text.replace("*", "").replace("—", ", ").replace("…", "...")
    samples, sr = _kokoro.create(clean, voice=voice, speed=speed, lang="en-us")
    assert sr == SR
    samples = samples.astype(np.float32)
    peak = np.max(np.abs(samples)) or 1
    samples = samples / peak * 0.8
    np.save(path, samples)
    return samples


# ============================================================ audio: synth
def _t(sec):
    return np.arange(int(sec * SR)) / SR


def _env(n, a=0.005, r=0.1):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nr and nr < n:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def _noise(sec, seed=0):
    return np.random.default_rng(seed).standard_normal(int(sec * SR))


def _lp(x, k=0.05):
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):  # small one-pole filter
        acc += k * (v - acc)
        y[i] = acc
    return y


def _lp_fast(x, width=40):
    return np.convolve(x, np.ones(width) / width, mode="same")


def _pluck(f, sec=0.35):
    t = _t(sec)
    return (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 9)


def _keys(f, sec=2.2):
    t = _t(sec)
    x = sum(a * np.sin(2 * np.pi * f * m * t) for m, a in ((1, 1), (2, .4), (3, .15), (4, .08)))
    return x * np.exp(-t * 1.6) * _env(len(t), .01, .3)


def _pad(fs, sec):
    t = _t(sec)
    x = sum(np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.003 * t) for f in fs)
    return x / len(fs) * _env(len(t), .4, .4)


NOTE = {n: 440 * 2 ** ((i - 9) / 12) for i, n in enumerate("C C# D D# E F F# G G# A A# B".split())}


def _f(name, octave):
    return NOTE[name] * 2 ** (octave - 4)


def music_bed(kind, sec, seed=0):
    n = int(sec * SR)
    out = np.zeros(n + SR * 8)   # headroom: notes may ring past the end
    if kind == "comedy":
        prog = [("C", "E", "G"), ("G", "B", "D"), ("A", "C", "E"), ("F", "A", "C")]
        step = 60 / 112 / 2
        i = 0
        while i * step < sec:
            ch = prog[(i // 8) % 4]
            note = ch[[0, 1, 2, 1][i % 4]]
            p = _pluck(_f(note, 4 if i % 4 else 3))
            k = int(i * step * SR)
            out[k:k + len(p)] += p * (.55 if i % 4 == 0 else .35)
            i += 1
    elif kind == "tense":
        t = _t(sec)
        out[:n] += (np.sin(2 * np.pi * 55 * t) * .5 + np.sin(2 * np.pi * 82.4 * t) * .3) * (.75 + .25 * np.sin(2 * np.pi * .2 * t))
        out[:n] += _lp_fast(_noise(sec, seed), 200) * 2.5
        out[:n] *= _env(n, 1.5, 1.0)
    elif kind in ("heart", "swell", "hero"):
        prog = {"heart": [("A", 2, "C", "E"), ("F", 2, "A", "C"), ("C", 3, "E", "G"), ("G", 2, "B", "D")],
                "swell": [("D", 2, "F", "A"), ("A#", 1, "D", "F"), ("F", 2, "A", "C"), ("C", 3, "E", "G")],
                "hero": [("C", 3, "E", "G"), ("G", 2, "B", "D"), ("A", 2, "C", "E"), ("F", 2, "A", "C")]}[kind]
        bar = 2.4 if kind == "heart" else 2.0
        i = 0
        while i * bar < sec:
            root, octv, a, b = prog[i % 4]
            k = int(i * bar * SR)
            if kind == "heart":
                for j, nn in enumerate((root, a, b, a)):
                    p = _keys(_f(nn, octv + (1 if j else 0)))
                    kk = k + int(j * bar / 4 * SR)
                    out[kk:kk + len(p)] += p * .3
            else:
                p = _pad([_f(root, octv), _f(a, octv + 1), _f(b, octv + 1), _f(root, octv + 1)], bar + .5)
                out[k:k + len(p)] += p * .45
            i += 1
        if kind == "swell":
            out[:n] *= np.linspace(.25, 1.2, n)
    out = out[:n]
    return out / (np.max(np.abs(out)) or 1)


def sfx(name, seed=0):
    if name == "wind":
        x = _lp_fast(_noise(6, seed), 120) * 6
        t = _t(6)
        return x * (.6 + .4 * np.sin(2 * np.pi * .3 * t)) * _env(len(t), 1, 1)
    if name == "tap":
        click = np.sin(2 * np.pi * 1600 * _t(.03)) * np.exp(-_t(.03) * 120)
        out = np.zeros(int(1.4 * SR))
        out[:len(click)] += click
        out[int(.14 * SR):int(.14 * SR) + len(click)] += click
        sting = _pad([_f("C", 4), _f("G", 4), _f("E", 5)], 1.0) * .5
        out[int(.3 * SR):int(.3 * SR) + len(sting)] += sting
        return out
    if name == "bwomp":
        t = _t(.6)
        return np.sin(2 * np.pi * np.cumsum(np.linspace(200, 60, len(t))) / SR) * np.exp(-t * 4)
    if name == "logo":
        a = sfx("tap")[:int(.4 * SR)]
        b = sfx("bwomp") * 1.2
        return np.concatenate([a, b, np.zeros(SR // 2)])
    if name == "whoosh":
        t = _t(.5)
        return _lp_fast(_noise(.5, seed), 8) * np.sin(np.pi * t / .5) * 1.5
    if name == "blip":
        t = _t(.12)
        return np.sin(2 * np.pi * 1250 * t) * _env(len(t), .003, .05)
    if name == "thud":
        t = _t(.4)
        return np.sin(2 * np.pi * 70 * t) * np.exp(-t * 12) * 1.4
    if name == "scratch":
        t = _t(.45)
        return _lp_fast(_noise(.45, seed), 4) * np.sin(2 * np.pi * np.cumsum(np.linspace(900, 200, len(t))) / SR) * 1.2
    if name == "chime":
        t = _t(1.6)
        return (np.sin(2 * np.pi * 1320 * t) + .6 * np.sin(2 * np.pi * 1760 * t)) * np.exp(-t * 3) * .7
    if name == "static":
        x = _noise(2.5, seed) - _lp_fast(_noise(2.5, seed), 6)
        return x * .35 * _env(len(x), .05, .3)
    if name == "crank":
        out = np.zeros(int(3 * SR))
        click = np.sin(2 * np.pi * 2400 * _t(.015)) * np.exp(-_t(.015) * 200)
        for k in range(0, len(out) - len(click), int(.09 * SR)):
            out[k:k + len(click)] += click * .6
        return out
    if name == "heartbeat":
        out = np.zeros(int(4 * SR))
        beat = np.sin(2 * np.pi * 55 * _t(.18)) * np.exp(-_t(.18) * 18)
        for k in np.arange(0, 3.6, .9):
            for d in (0, .22):
                i = int((k + d) * SR)
                out[i:i + len(beat)] += beat * (1 if d == 0 else .7)
        return out * 1.4
    if name == "trombone":
        out = []
        for f in (_f("A#", 3), _f("A", 3), _f("G#", 3), _f("G", 3)):
            t = _t(.32 if f != _f("G", 3) else .8)
            out.append(np.sign(np.sin(2 * np.pi * f * t)) * .25 * _env(len(t), .01, .08))
        return _lp_fast(np.concatenate(out), 10)
    if name == "chalk":
        x = _noise(1.0, seed) - _lp_fast(_noise(1.0, seed), 3)
        return x * .25 * (np.sin(np.pi * _t(1.0)) ** 2)
    if name == "electric":
        out = np.zeros(int(2.4 * SR))
        hit = np.sin(2 * np.pi * 60 * _t(.25)) * np.exp(-_t(.25) * 14) * 1.3
        for k in (0, .7, 1.4):
            i = int(k * SR)
            out[i:i + len(hit)] += hit
        return out
    if name == "lowhit":
        t = _t(2)
        return np.sin(2 * np.pi * 41 * t) * np.exp(-t * 1.5) * 1.5
    if name == "beach":  # cheesy "wrong song" from the headphones
        step = .15
        notes = ["C", "E", "G", "E", "A", "G", "E", "C", "D", "F", "A", "F", "G", "E", "C", "G"]
        out = np.zeros(int(len(notes) * step * SR + SR))
        for i, nn in enumerate(notes):
            p = _pluck(_f(nn, 5), .3) * .6 + _pluck(_f(nn, 4), .3) * .3
            k = int(i * step * SR)
            out[k:k + len(p)] += p
        return out
    if name == "heist":
        out = np.zeros(int(2.6 * SR))
        for i, nn in enumerate(["E", "E", "G", "E", "D", "C", "B", "C"]):
            p = _pluck(_f(nn, 3), .25)
            k = int(i * .3 * SR)
            out[k:k + len(p)] += p
        return out
    if name == "ticks":
        out = np.zeros(int(2 * SR))
        tick = np.sin(2 * np.pi * 3000 * _t(.01)) * np.exp(-_t(.01) * 300)
        for k in range(0, len(out) - 300, int(.16 * SR)):
            out[k:k + len(tick)] += tick * .5
        return out
    raise ValueError(name)


# ============================================================ timing
def tc(s):
    m, sec = s.split(":")
    return int(m) * 60 + float(sec)


def plan(shots, end_tc, cache):
    """Attach start/duration/VO samples to each shot. VO overflow extends the shot."""
    t = 0.0
    for i, sh in enumerate(shots):
        nominal = (tc(shots[i + 1]["tc"]) if i + 1 < len(shots) else tc(end_tc)) - tc(sh["tc"])
        lines = []
        cursor = sh.get("vo_at", 0.35)
        for spk, txt in sh.get("vo", []):
            if spk == "PAUSE":
                cursor += float(txt)
                continue
            a = tts(txt, spk, cache)
            lines.append((cursor, spk, txt, a))
            cursor += len(a) / SR + 0.28
        sh["_lines"] = lines
        sh["dur"] = max(nominal, cursor + 0.3)
        sh["start"] = t
        t += sh["dur"]
    return t


# ============================================================ video
def _ease(x):
    return x * x * (3 - 2 * x)


def render_clip(sh, frames_dir, out_path):
    dur = sh["dur"]
    n = max(1, round(dur * FPS))
    cam = {"z0": 1.0, "z1": 1.0, "cx0": 960, "cy0": 540, "cx1": None, "cy1": None, "shake": 0}
    cam.update(sh.get("cam", {}))
    cam["cx1"] = cam["cx0"] if cam["cx1"] is None else cam["cx1"]
    cam["cy1"] = cam["cy0"] if cam["cy1"] is None else cam["cy1"]
    panels = sh["_panels"]   # [(at_fraction, scene_img, hud_img, letterbox)]
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                             "-crf", "20", "-pix_fmt", "yuv420p", out_path], stdin=subprocess.PIPE)
    rng = np.random.default_rng(7)
    cache = {}
    for f in range(n):
        x = f / max(1, n - 1)
        e = _ease(x)
        z = cam["z0"] + (cam["z1"] - cam["z0"]) * e
        cx = cam["cx0"] + (cam["cx1"] - cam["cx0"]) * e
        cy = cam["cy0"] + (cam["cy1"] - cam["cy0"]) * e
        if cam["shake"]:
            amp = cam["shake"] * max(0, 1 - x * 3)
            cx += rng.uniform(-amp, amp)
            cy += rng.uniform(-amp, amp)
        pi = 0
        for k, p in enumerate(panels):
            if x >= p[0] - 1e-9:
                pi = k
        _, scene, hud, lb = panels[pi]
        w, h = W / z, H / z
        x0 = min(max(cx - w / 2, 0), W - w)
        y0 = min(max(cy - h / 2, 0), H - h)
        frame = scene.transform((OW, OH), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BICUBIC)
        frame.paste(hud, (0, 0), hud)
        if lb:
            d = ImageDraw.Draw(frame)
            b = round(LETTERBOX * OH / H)
            d.rectangle([0, 0, OW, b], fill=(0, 0, 0))
            d.rectangle([0, OH - b, OW, OH], fill=(0, 0, 0))
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    proc.wait()


def prepare_panels(sh, rend, frames_dir):
    base = {k: v for k, v in sh.items() if not k.startswith("_") and k != "panels"}
    specs = [(0.0, base)]
    for p in sh.get("panels", []):
        spec = dict(specs[-1][1])
        spec.update({k: v for k, v in p.items() if k != "at"})
        specs.append((p["at"], spec))
    out = []
    for k, (at, spec) in enumerate(specs):
        sp = os.path.join(frames_dir, f"{sh['id']}_{k}.png")
        hp = os.path.join(frames_dir, f"{sh['id']}_{k}_hud.png")
        rend.png(scene_svg(spec), sp)
        rend.png(hud_svg(spec, f"EP01 · {sh['id']}"), hp, transparent=True)
        scene = Image.open(sp).convert("RGB")
        hud = Image.open(hp).convert("RGBA").resize((OW, OH), Image.LANCZOS)
        out.append((at, scene, hud, bool(spec.get("letterbox"))))
    sh["_panels"] = out
    sh["_stills"] = [os.path.join(frames_dir, f"{sh['id']}_{k}.png") for k in range(len(specs))]


# ============================================================ audio mix
def mix(shots, total, out_wav):
    n = int((total + 1) * SR)
    vo = np.zeros(n)
    mus = np.zeros(n)
    fx = np.zeros(n)
    # music: contiguous runs of the same bed
    runs = []
    cur = None
    for sh in shots:
        m = sh.get("music", "keep")
        if m == "keep":
            m = cur[0] if cur else "none"
        if cur and cur[0] == m:
            cur[2] = sh["start"] + sh["dur"]
        else:
            if cur:
                runs.append(cur)
            cur = [m, sh["start"], sh["start"] + sh["dur"]]
    runs.append(cur)
    for i, (kind, a, b) in enumerate(runs):
        if kind == "none":
            continue
        bed = music_bed(kind, b - a + 0.6, seed=i)
        k = int(a * SR)
        bed = bed[:n - k]
        fade = min(len(bed), int(.6 * SR))
        bed[-fade:] *= np.linspace(1, 0, fade)
        mus[k:k + len(bed)] += bed * .2
    for sh in shots:
        for (t, spk, txt, a) in sh["_lines"]:
            k = int((sh["start"] + t) * SR)
            vo[k:k + len(a)] += a[:n - k]
        for name, t in sh.get("sfx", []):
            s = sfx(name, seed=hash(sh["id"]) % 1000)
            k = int((sh["start"] + t) * SR)
            s = s[:n - k]
            lvl = {"wind": .25, "beach": .5, "heist": .45, "static": .5, "crank": .5}.get(name, .6)
            fx[k:k + len(s)] += s * lvl
    # duck music under VO
    env = _lp_fast((np.abs(vo) > .02).astype(float), int(.25 * SR))
    mus *= 1 - .65 * np.clip(env * 3, 0, 1)
    out = vo + mus + fx
    out = out / max(1.0, np.max(np.abs(out)) / .95)
    pcm = (out * 32767).astype(np.int16)
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def write_srt(shots, path):
    def fmt(s):
        h, r = divmod(s, 3600)
        m, r = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(r):02d},{int((r - int(r)) * 1000):03d}"
    i = 1
    lines = []
    for sh in shots:
        for (t, spk, txt, a) in sh["_lines"]:
            st = sh["start"] + t
            label = "" if spk == "NARR" else f"{spk}: "
            lines.append(f"{i}\n{fmt(st)} --> {fmt(st + len(a) / SR)}\n{label}{txt.replace('*', '')}\n")
            i += 1
    open(path, "w").write("\n".join(lines))


# ============================================================ main
def load(path):
    spec = importlib.util.spec_from_file_location("shots", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    shots_path = sys.argv[1]
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    mod = load(shots_path)
    ep_dir = os.path.dirname(os.path.abspath(shots_path))
    build = os.path.join(ep_dir, "build")
    frames = os.path.join(build, "frames")
    clips = os.path.join(build, "clips")
    cache = os.path.join(build, "tts_cache")
    for d in (frames, clips, cache):
        os.makedirs(d, exist_ok=True)
    shots = mod.SHOTS
    print(f"{len(shots)} shots · planning VO…", flush=True)
    total = plan(shots, mod.END_TC, cache)
    print(f"runtime {total / 60:.2f} min", flush=True)
    todo = [s for s in shots if only is None or s["id"] in only]
    mux_only = "--mux" in sys.argv   # re-mix audio / re-mux using existing clips
    if not mux_only:
        rend = Renderer()
        for sh in todo:
            prepare_panels(sh, rend, frames)
        rend.close()
    if "--stills" in sys.argv:
        contact(todo, os.path.join(build, "stills_contact.png"))
        return
    if mux_only:
        todo = []
    from concurrent.futures import ThreadPoolExecutor
    def job(sh):
        p = os.path.join(clips, f"{sh['id']}.mp4")
        render_clip(sh, frames, p)
        return p
    with ThreadPoolExecutor(max_workers=2) as ex:
        for i, p in enumerate(ex.map(job, todo)):
            print(f"  clip {i + 1}/{len(todo)}", flush=True)
    if todo:
        contact(todo, os.path.join(build, "stills_contact.png"))
    if only:
        print("preview clips in", clips)
        return
    listf = os.path.join(build, "clips.txt")
    open(listf, "w").write("".join(f"file '{os.path.join(clips, s['id'] + '.mp4')}'\n" for s in shots))
    wav = os.path.join(build, "mix.wav")
    mix(shots, total, wav)
    episode = os.path.dirname(ep_dir)          # outputs live next to STORYBOARD.md
    srt = os.path.join(episode, f"{mod.SLUG}_animatic.srt")
    write_srt(shots, srt)
    out = os.path.join(episode, f"{mod.SLUG}_animatic.mp4")
    # two-pass loudness normalisation to -14 LUFS / -1.5 dBTP
    target = "I=-14:TP=-1.5:LRA=11"
    comp = wav.replace(".wav", "_comp.wav")   # tame peaks so linear gain can reach the target
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af",
                    "acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,alimiter=limit=0.6:level=false",
                    comp], check=True)
    wav = comp
    probe = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", f"loudnorm={target}:print_format=json",
                            "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    af = (f"loudnorm={target}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listf, "-i", wav,
                    "-c:v", "copy", "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    json.dump([{"id": s["id"], "start": round(s["start"], 2), "dur": round(s["dur"], 2)} for s in shots],
              open(os.path.join(build, "timing.json"), "w"), indent=1)
    print("wrote", out)


def contact(shots, path):
    thumbs = []
    for sh in shots:
        im = sh["_panels"][0][1].resize((320, 180))
        im.paste(sh["_panels"][0][2].resize((320, 180)), (0, 0), sh["_panels"][0][2].resize((320, 180)))
        ImageDraw.Draw(im).text((6, 4), sh["id"], fill=(255, 255, 0))
        thumbs.append(im)
    cols = 8
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 320, rows * 180), "black")
    for i, t in enumerate(thumbs):
        sheet.paste(t, ((i % cols) * 320, (i // cols) * 180))
    sheet.save(path)


if __name__ == "__main__":
    main()
