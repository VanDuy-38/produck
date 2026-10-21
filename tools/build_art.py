#!/usr/bin/env python3
"""Build every SVG asset for the series (and PNG previews with --png).

    python3 tools/build_art.py          # SVGs only
    python3 tools/build_art.py --png    # SVGs + PNG previews (needs: pip install playwright)

Outputs go to art/. Edit tools/bo.py / tools/rae.py (characters) or tools/backgrounds.py
(locations) and re-run; never hand-edit the generated SVGs.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import bo  # noqa: E402
import rae  # noqa: E402
import backgrounds as bgs  # noqa: E402
import ep01_sets  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ART = os.path.join(ROOT, "art")
FONT = 'font-family="Arial, Helvetica, sans-serif"'


def write(path, svg):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return path


def doc(vb, inner, w=None, h=None, bg=None):
    x, y, ww, hh = vb
    size = f' width="{w}" height="{h}"' if w else ""
    back = f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {ww} {hh}"{size}>{back}{inner}</svg>'


def label(x, y, text, size=22, weight=700, color=bo.INK, anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" {FONT} font-size="{size}" font-weight="{weight}" fill="{color}">{text}</text>'


def place(svg, x, y, s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})">{svg}</g>'


def build_bo():
    out = os.path.join(ART, "characters", "bo")
    files = []
    for name in bo.FACE_ORDER:
        files.append(write(os.path.join(out, "expressions", f"bo_face_{name}.svg"),
                           doc((-90, -90, 180, 160), bo.head(name), 360, 320)))
    for name in bo.POSE_ORDER:
        files.append(write(os.path.join(out, "poses", f"bo_pose_{name}.svg"),
                           doc((-130, -110, 260, 320), bo.body(name), 520, 640)))
    for view in ("front", "three_quarter", "side", "back"):
        files.append(write(os.path.join(out, "turnaround", f"bo_{view}.svg"),
                           doc((-110, -80, 220, 290), bo.turnaround(view), 440, 580)))

    # ---- model sheet
    W, H = 1800, 2200
    s = [f'<rect width="{W}" height="{H}" fill="#F4F7FB"/>',
         label(60, 80, "BO — MODEL SHEET", 46, 900, anchor="start"),
         label(60, 118, "Lead character · \"You\" in every episode · 2D flat, 5 px navy outline", 22, 400, "#5B6785", "start")]

    def section(y, title):
        s.append(f'<line x1="60" y1="{y}" x2="{W - 60}" y2="{y}" stroke="#C9D2E3" stroke-width="3"/>')
        s.append(label(60, y + 40, title, 26, 900, anchor="start"))

    section(150, "TURNAROUND")
    for i, (view, name) in enumerate([("front", "FRONT"), ("three_quarter", "3/4"), ("side", "SIDE"), ("back", "BACK")]):
        x = 190 + i * 290
        s.append(place(bo.turnaround(view), x, 290))
        s.append(label(x, 520, name, 22))
    # proportion guides
    for y, t in [(232, "top of headband"), (290, "head centre"), (334, "chin"), (414, "hem"), (484, "ground")]:
        s.append(f'<line x1="90" y1="{y}" x2="1270" y2="{y}" stroke="#9AA5BE" stroke-width="1.5" stroke-dasharray="6 6"/>')
        s.append(label(1280, y + 6, t, 16, 400, "#5B6785", "start"))
    s.append(label(1470,240, "Height ≈ 2.7 heads", 20, 700, anchor="start"))
    s.append(label(1470,270, "Head = 92 × 84, corner r 40", 18, 400, "#5B6785", "start"))
    s.append(label(1470,298, "Limbs = single 7 px strokes", 18, 400, "#5B6785", "start"))
    s.append(label(1470,326, "No neck, no fingers, no nose", 18, 400, "#5B6785", "start"))
    s.append(label(1470,354, "Eyes stay inside the cheeks", 18, 400, "#5B6785", "start"))

    section(560, "EXPRESSIONS (18)")
    for i, name in enumerate(bo.FACE_ORDER):
        col, row = i % 6, i // 6
        x = 190 + col * 284
        y = 700 + row * 210
        s.append(place(bo.head(name), x, y, 1.15))
        s.append(label(x, y + 92, name.upper(), 18))

    section(1240, "KEY POSES (12)")
    for i, name in enumerate(bo.POSE_ORDER):
        col, row = i % 6, i // 6
        x = 190 + col * 284
        y = 1360 + row * 300
        s.append(place(bo.body(name), x, y, 0.82))
        s.append(label(x, y + 190, name.replace("_", " ").upper(), 18))

    section(1950, "HEADPHONE MOOD LIGHT — Bo's emotion meter")
    for i, (k, c) in enumerate(bo.MOOD.items()):
        x = 110 + i * 175
        s.append(f'<circle cx="{x}" cy="2045" r="20" fill="{c}" stroke="{bo.INK}" stroke-width="4"/>')
        s.append(label(x + 32, 2052, k, 20, 700, anchor="start"))
    s.append(label(60, 2110, "Palette:", 20, 900, anchor="start"))
    for i, (n, c) in enumerate([("skin", bo.SKIN), ("jacket", bo.JACKET), ("headphones", bo.HEADPHONE),
                                ("shoes", bo.SHOE), ("blush", bo.BLUSH), ("ink", bo.INK)]):
        x = 170 + i * 260
        s.append(f'<rect x="{x}" y="2088" width="34" height="34" rx="6" fill="{c}" stroke="{bo.INK}" stroke-width="3"/>')
        s.append(label(x + 44, 2112, f"{n} {c}", 18, 400, anchor="start"))
    files.append(write(os.path.join(out, "bo_model_sheet.svg"), doc((0, 0, W, H), "".join(s), W, H)))
    return files


def build_rae():
    out = os.path.join(ART, "characters", "rae")
    files = []
    for name in rae.FACE_ORDER:
        files.append(write(os.path.join(out, "expressions", f"rae_face_{name}.svg"),
                           doc((-110, -130, 220, 200), rae.head(name), 440, 400)))
    for name in rae.POSE_ORDER:
        files.append(write(os.path.join(out, "poses", f"rae_pose_{name}.svg"),
                           doc((-130, -150, 300, 360), rae.body(name), 600, 720)))
    for view in ("front", "three_quarter", "side", "back"):
        files.append(write(os.path.join(out, "turnaround", f"rae_{view}.svg"),
                           doc((-120, -130, 240, 340), rae.turnaround(view), 480, 680)))

    W, H = 1800, 2300
    s = [f'<rect width="{W}" height="{H}" fill="#F4F7FB"/>',
         label(60, 80, "RAE — MODEL SHEET", 46, 900, anchor="start"),
         label(60, 118, "The crush · dry, competent, secretly afraid of the dark · same build rules as Bo", 22, 400, "#5B6785", "start")]

    def section(y, title):
        s.append(f'<line x1="60" y1="{y}" x2="{W - 60}" y2="{y}" stroke="#C9D2E3" stroke-width="3"/>')
        s.append(label(60, y + 40, title, 26, 900, anchor="start"))

    section(150, "TURNAROUND")
    for i, (view, name) in enumerate([("front", "FRONT"), ("three_quarter", "3/4"), ("side", "SIDE"), ("back", "BACK")]):
        x = 190 + i * 290
        s.append(place(rae.turnaround(view), x, 330))
        s.append(label(x, 560, name, 22))
    for y, t in [(330, "head centre"), (374, "chin"), (470, "hem (longer than Bo)"), (524, "ground")]:
        s.append(f'<line x1="90" y1="{y}" x2="1270" y2="{y}" stroke="#9AA5BE" stroke-width="1.5" stroke-dasharray="6 6"/>')
        s.append(label(1280, y + 6, t, 16, 400, "#5B6785", "start"))
    notes = ["Identifiers:", "High ponytail + orange scrunchie", "Oversized mint hoodie, long hem",
             "Thick sleeves, kangaroo pocket", "Side-swept fringe, lash flicks", "No nose, no fingers, no neck"]
    for i, t in enumerate(notes):
        s.append(label(1470, 240 + i * 30, t, 20 if i == 0 else 18, 700 if i == 0 else 400,
                       bo.INK if i == 0 else "#5B6785", "start"))

    section(600, "EXPRESSIONS (12)")
    for i, name in enumerate(rae.FACE_ORDER):
        col, row = i % 6, i // 6
        x = 190 + col * 284
        y = 780 + row * 250
        s.append(place(rae.head(name), x, y, 1.15))
        s.append(label(x, y + 92, name.upper(), 18))

    section(1290, "KEY POSES (8)")
    for i, name in enumerate(rae.POSE_ORDER):
        col, row = i % 4, i // 4
        x = 200 + col * 400
        y = 1430 + row * 330
        s.append(place(rae.body(name), x, y, 0.82))
        s.append(label(x, y + 196, name.replace("_", " ").upper(), 18))

    section(2050, "PONYTAIL METER — Rae's emotion meter (rotate around the scrunchie)")
    for i, (st, txt) in enumerate([("up", "UP · alert / scared / laughing"), ("neutral", "NEUTRAL · default"),
                                   ("droop", "DROOP · sad / tired")]):
        x = 140 + i * 560
        s.append(place(rae.head("neutral", tail=st), x, 2190, 0.75))
        s.append(label(x + 70, 2198, txt, 19, 700, anchor="start"))
    pal = [("skin", rae.SKIN), ("hair", rae.HAIR), ("hoodie", rae.HOODIE), ("scrunchie", rae.SCRUNCHIE), ("ink", rae.INK)]
    for i, (n, c) in enumerate(pal):
        x = 120 + i * 330
        s.append(f'<rect x="{x}" y="2250" width="30" height="30" rx="6" fill="{c}" stroke="{bo.INK}" stroke-width="3"/>')
        s.append(label(x + 40, 2272, f"{n} {c}", 17, 400, anchor="start"))
    files.append(write(os.path.join(out, "rae_model_sheet.svg"), doc((0, 0, W, H), "".join(s), W, H)))

    # Bo + Rae line-up
    lu = [f'<rect width="900" height="560" fill="#F4F7FB"/>', label(40, 56, "BO + RAE — SCALE LINE-UP", 30, 900, anchor="start"),
          place(bo.body("idle"), 320, 230, 1.2), place(rae.body("arms_crossed"), 600, 230, 1.2),
          '<line x1="80" y1="460" x2="840" y2="460" stroke="#9AA5BE" stroke-width="2" stroke-dasharray="6 6"/>',
          label(320, 520, "BO", 22), label(600, 520, "RAE", 22)]
    files.append(write(os.path.join(ART, "characters", "bo_rae_lineup.svg"), doc((0, 0, 900, 560), "".join(lu), 900, 560)))
    return files


def build_two_shots():
    """EP01 framing tests: Bo + Rae in the school hallway and classroom."""
    files = []
    for code, slug, title, fn in bgs.BACKGROUNDS:
        if code not in ("BG02", "BG03"):
            continue
        svg = fn()
        stage = bgs.STAGE_LINE[code]
        k = 1.7
        chars = (place(bo.body("idle", face="nervous", mood="crush"), 820, stage - 194 * k, k)
                 + place(rae.body("arms_crossed"), 1120, stage - 194 * k, k))
        fg_at = svg.find('<g id="layer-fg">')
        svg = svg[:fg_at] + chars + svg[fg_at:]
        files.append(write(os.path.join(ART, "previews", "_scene_tests", f"{code}_{slug}_with_bo_rae.svg"), svg))
    return files


def build_backgrounds():
    files = []
    for code, slug, title, fn in bgs.BACKGROUNDS:
        files.append(write(os.path.join(ART, "backgrounds", f"{code}_{slug}.svg"), fn()))
    # season 1 / EP01 sets (Tier B/C) from tools/ep01_sets.py
    for code, slug, fn in ep01_sets.EXPORT:
        files.append(write(os.path.join(ART, "backgrounds", f"{code}_{slug}.svg"), fn()))
    return files


def build_scene_tests():
    """Bo dropped onto each background at standard medium-wide scale (1.7)."""
    files = []
    for code, slug, title, fn in bgs.BACKGROUNDS:
        svg = fn()
        stage = bgs.STAGE_LINE[code.rstrip("N")]
        bo_svg = place(bo.body("idle"), 960, stage - 194 * 1.7, 1.7)
        fg_at = svg.find('<g id="layer-fg">')
        svg = svg[:fg_at] + bo_svg + svg[fg_at:]
        files.append(write(os.path.join(ART, "previews", "_scene_tests", f"{code}_{slug}_with_bo.svg"), svg))
    return files


def render_png(svg_paths, out_dir):
    from playwright.sync_api import sync_playwright
    os.makedirs(out_dir, exist_ok=True)
    pngs = []
    with sync_playwright() as p:
        exe = "/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None
        try:
            browser = p.chromium.launch(executable_path=exe) if exe and os.path.isfile(exe) else p.chromium.launch()
        except Exception:
            browser = p.chromium.launch()
        page = browser.new_page()
        for path in svg_paths:
            page.goto("file://" + path)
            el = page.locator("svg").first
            png = os.path.join(out_dir, os.path.splitext(os.path.basename(path))[0] + ".png")
            el.screenshot(path=png)
            pngs.append(png)
        browser.close()
    return pngs


if __name__ == "__main__":
    bo_files = build_bo()
    bg_files = build_backgrounds()
    rae_files = build_rae()
    tests = build_scene_tests() + build_two_shots()
    print(f"{len(bo_files)} Bo files, {len(rae_files)} Rae files, {len(bg_files)} backgrounds, {len(tests)} scene tests")
    if "--png" in sys.argv:
        sheet = [f for f in bo_files + rae_files if f.endswith(("_model_sheet.svg", "_lineup.svg"))]
        pngs = render_png(sheet + bg_files + tests, os.path.join(ART, "previews"))
        print(f"{len(pngs)} PNG previews")
