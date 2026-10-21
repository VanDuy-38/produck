"""Flat 2D background set, 1920×1080.

Every background is split into named layers (<g id="layer-...">) so it can be
separated for parallax in After Effects / Moho / Harmony:
  layer-sky  → farthest   layer-far → back wall / skyline
  layer-mid  → props      layer-fg  → foreground (in front of characters)
Characters stand on the STAGE LINE (y given per background in STAGE_LINE).

Backgrounds are deliberately lower-saturation than Bo so he always pops.
"""
import math
import random

W, H = 1920, 1080
INK = "#1F2A44"

STAGE_LINE = {}


def _svg(layers, defs=""):
    body = "".join(f'<g id="layer-{name}">{content}</g>' for name, content in layers)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<defs>{defs}</defs>{body}</svg>')


def rect(x, y, w, h, fill, rx=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'


def grad(id_, top, bottom):
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>')


# ---------------------------------------------------------------- BG01 bedroom
def bedroom(night=False):
    STAGE_LINE["BG01"] = 900
    wall, wall_d = ("#DCE6F2", "#C8D4E4")
    floor = "#C9A27E"
    sky = grad("sky", "#8EC9F5", "#D7EEFF") if not night else grad("sky", "#14183A", "#2E3770")
    far = [rect(0, 0, W, 760, wall), rect(0, 700, W, 60, wall_d)]
    # window
    far.append(rect(760, 150, 420, 330, "url(#sky)", rx=10))
    if night:
        far.append('<circle cx="1080" cy="230" r="34" fill="#FFF4C8"/>')
        random.seed(3)
        for _ in range(18):
            far.append(f'<circle cx="{random.randint(775,1165)}" cy="{random.randint(165,465)}" r="{random.choice([1.5,2,2.5])}" fill="#FFFFFF" opacity=".8"/>')
    else:
        far.append('<ellipse cx="880" cy="250" rx="70" ry="24" fill="#fff" opacity=".9"/>'
                   '<ellipse cx="1060" cy="330" rx="90" ry="26" fill="#fff" opacity=".85"/>')
    far.append(f'<rect x="760" y="150" width="420" height="330" rx="10" fill="none" stroke="#FFFFFF" stroke-width="16"/>'
               f'<line x1="970" y1="150" x2="970" y2="480" stroke="#FFFFFF" stroke-width="12"/>'
               f'<line x1="760" y1="315" x2="1180" y2="315" stroke="#FFFFFF" stroke-width="12"/>')
    far.append(rect(700, 130, 540, 22, "#8C6A54", rx=11))
    far.append('<path d="M 700 140 Q 760 320 720 500 L 690 500 Z" fill="#6C8EBF"/>'
               '<path d="M 1240 140 Q 1180 320 1220 500 L 1250 500 Z" fill="#6C8EBF"/>')
    far.append(rect(710, 488, 520, 18, "#E9EEF5", rx=6))
    # posters
    far.append(rect(220, 170, 170, 230, "#F6D365", rx=6, extra='transform="rotate(-3 305 285)"'))
    far.append('<circle cx="305" cy="270" r="50" fill="#FF8A5B"/><rect x="250" y="340" width="110" height="14" rx="7" fill="#1F2A44" opacity=".5"/>')
    far.append(rect(430, 230, 130, 160, "#9AD1D4", rx=6, extra='transform="rotate(4 495 310)"'))
    far.append('<path d="M 455 360 L 495 270 L 535 360 Z" fill="#3E7CB1" opacity=".8"/>')
    # shelf
    far.append(rect(1380, 260, 360, 18, "#8C6A54", rx=4))
    for i, (c, h) in enumerate([("#E07A5F", 70), ("#3D5A80", 84), ("#81B29A", 62), ("#F2CC8F", 78), ("#6D597A", 66)]):
        far.append(rect(1400 + i * 34, 260 - h, 28, h, c, rx=3))
    far.append('<circle cx="1640" cy="232" r="28" fill="#FFC83D"/>')  # trophy-ish ball
    floor_l = [rect(0, 760, W, 320, floor)]
    for y in (820, 900, 990):
        floor_l.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#B38B67" stroke-width="4"/>')
    floor_l.append('<ellipse cx="960" cy="930" rx="420" ry="70" fill="#E8A87C" opacity=".85"/>')
    floor_l.append('<ellipse cx="960" cy="930" rx="330" ry="50" fill="none" stroke="#F5D0B5" stroke-width="8"/>')
    mid = []
    # bed
    mid.append(rect(60, 560, 560, 260, "#8C6A54", rx=18))
    mid.append(rect(80, 600, 520, 170, "#6C8EBF", rx=24))
    mid.append(rect(90, 580, 180, 80, "#FFFFFF", rx=30))
    mid.append(rect(60, 470, 40, 360, "#7A5A45", rx=10))
    # desk + lamp + laptop
    mid.append(rect(1360, 600, 440, 26, "#8C6A54", rx=6))
    mid.append(rect(1380, 626, 26, 210, "#7A5A45"))
    mid.append(rect(1754, 626, 26, 210, "#7A5A45"))
    mid.append(rect(1460, 540, 170, 60, "#3D4A66", rx=6))
    mid.append('<path d="M 1440 600 L 1650 600 L 1630 610 L 1460 610 Z" fill="#2B3550"/>')
    mid.append('<path d="M 1710 600 L 1710 490 L 1680 450" fill="none" stroke="#3D4A66" stroke-width="10" stroke-linecap="round"/>'
               '<path d="M 1650 440 L 1710 420 L 1720 470 Z" fill="#FFC83D"/>')
    if night:
        mid.append('<path d="M 1680 460 L 1560 600 L 1760 600 Z" fill="#FFE9A8" opacity=".35"/>')
    layers = [("sky", ""), ("far", "".join(far) + "".join(floor_l)), ("mid", "".join(mid)), ("fg", "")]
    if night:
        layers.append(("night-grade", rect(0, 0, W, H, "#1B2350", extra='opacity=".45"')))
    return _svg(layers, sky)


# ---------------------------------------------------------------- BG02 hallway
def hallway():
    STAGE_LINE["BG02"] = 930
    far = [rect(0, 0, W, 300, "#F2E6C9"), rect(0, 300, W, 560, "#E6D8B8"), rect(0, 290, W, 16, "#C9B48F")]
    # ceiling lights
    for x in range(160, W, 420):
        far.append(rect(x, 30, 220, 24, "#FFFFFF", rx=12))
        far.append(f'<path d="M {x} 54 L {x - 60} 300 L {x + 280} 300 L {x + 220} 54 Z" fill="#FFF8DC" opacity=".35"/>')
    # lockers
    colors = ["#7FB3D5", "#76A9CB"]
    x = 40
    i = 0
    while x < W - 40:
        if 820 <= x <= 1080:  # door gap
            x = 1100
            continue
        far.append(rect(x, 360, 84, 470, colors[i % 2], rx=4, extra=f'stroke="{INK}" stroke-opacity=".25" stroke-width="3"'))
        for vy in (390, 404, 418):
            far.append(rect(x + 18, vy, 48, 6, "#5C8DB0", rx=3))
        far.append(rect(x + 62, 580, 8, 36, "#4A6F8C", rx=4))
        x += 88
        i += 1
    # classroom door
    far.append(rect(840, 330, 240, 500, "#A0785A", rx=6))
    far.append(rect(880, 380, 80, 120, "#CFE6F5", rx=4))
    far.append('<circle cx="1050" cy="590" r="12" fill="#FFC83D"/>')
    far.append(rect(860, 300, 200, 28, "#2F6B4F", rx=4))
    far.append('<text x="960" y="321" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="800" fill="#FFFFFF">ROOM 104</text>')
    # bulletin board
    far.append(rect(1300, 130, 380, 150, "#C89F6D", rx=6))
    for (bx, by, c) in [(1320, 145, "#FFF59D"), (1420, 160, "#B2EBF2"), (1530, 140, "#F8BBD0"), (1600, 175, "#C5E1A5")]:
        far.append(rect(bx, by, 80, 90, c, rx=3))
    floor = [rect(0, 830, W, 250, "#C5CCD6")]
    for xx in range(0, W, 120):
        floor.append(f'<line x1="{xx}" y1="830" x2="{xx - 60}" y2="1080" stroke="#AEB6C2" stroke-width="3"/>')
    floor.append(rect(0, 830, W, 14, "#9AA3B0"))
    return _svg([("sky", ""), ("far", "".join(far)), ("mid", "".join(floor)), ("fg", "")])


# ---------------------------------------------------------------- BG03 classroom
def classroom():
    STAGE_LINE["BG03"] = 860
    far = [rect(0, 0, W, 800, "#F3EBD8"), rect(0, 760, W, 40, "#D9CBAE")]
    far.append(rect(420, 160, 1080, 430, "#2F5D50", rx=10))
    far.append(f'<rect x="420" y="160" width="1080" height="430" rx="10" fill="none" stroke="#A0785A" stroke-width="18"/>')
    far.append(rect(440, 590, 1040, 16, "#A0785A"))
    chalk = 'font-family="Comic Sans MS, Chalkboard, Arial, sans-serif" fill="#F4F4F4" opacity=".9"'
    far.append(f'<text x="500" y="260" font-size="48" {chalk}>F = m × a</text>')
    far.append(f'<text x="500" y="350" font-size="40" {chalk}>H₂O → ice @ 0°C</text>')
    far.append('<path d="M 1100 240 q 80 -60 160 0 t 160 0" fill="none" stroke="#F4F4F4" stroke-width="5" opacity=".8"/>')
    far.append('<circle cx="1260" cy="420" r="70" fill="none" stroke="#F4F4F4" stroke-width="5" opacity=".8"/>')
    # clock
    far.append(f'<circle cx="1700" cy="160" r="60" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
               f'<line x1="1700" y1="160" x2="1700" y2="118" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
               f'<line x1="1700" y1="160" x2="1730" y2="172" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    # windows left
    for wy in (180,):
        for wx in (60, 220):
            far.append(rect(wx, wy, 140, 260, "#BFE3F7", rx=6, extra='stroke="#FFFFFF" stroke-width="10"'))
    floor = [rect(0, 800, W, 280, "#B9A27F")]
    for xx in range(-200, W + 200, 160):
        floor.append(f'<line x1="{xx}" y1="800" x2="{xx - 120}" y2="1080" stroke="#A68E6B" stroke-width="3"/>')
    mid = []
    # teacher desk
    mid.append(rect(1560, 620, 300, 30, "#8C6A54", rx=6))
    mid.append(rect(1580, 650, 260, 160, "#7A5A45", rx=4))
    mid.append('<circle cx="1640" cy="600" r="22" fill="#E63946"/><rect x="1636" y="574" width="8" height="10" fill="#4C9A2A"/>')
    mid.append(rect(1700, 580, 90, 40, "#F1FAEE", rx=4))
    fg = []
    # student desks foreground (cut off at bottom)
    for dx in (80, 760, 1440):
        fg.append(rect(dx, 960, 400, 34, "#C8A27A", rx=8))
        fg.append(rect(dx + 30, 994, 22, 120, "#6E7D8F"))
        fg.append(rect(dx + 348, 994, 22, 120, "#6E7D8F"))
    return _svg([("sky", ""), ("far", "".join(far) + "".join(floor)), ("mid", "".join(mid)), ("fg", "".join(fg))])


# ---------------------------------------------------------------- BG04 blizzard exterior
def blizzard():
    STAGE_LINE["BG04"] = 940
    defs = grad("sky", "#0F1630", "#3A4B7A")
    sky = [rect(0, 0, W, H, "url(#sky)")]
    far = []
    # distant hills
    far.append('<path d="M 0 640 Q 300 560 640 620 T 1300 600 T 1920 610 L 1920 1080 L 0 1080 Z" fill="#7F93BF"/>')
    # school building
    far.append(rect(340, 330, 1240, 420, "#8B5E54"))
    far.append(rect(320, 300, 1280, 44, "#E8EEF8", rx=8))  # snow on roof
    far.append(rect(860, 230, 200, 110, "#8B5E54"))
    far.append(rect(846, 214, 228, 26, "#E8EEF8", rx=8))
    far.append(f'<circle cx="960" cy="285" r="34" fill="#F6F1E3" stroke="{INK}" stroke-width="5"/>')
    far.append(rect(890, 560, 140, 190, "#3D2B2B", rx=4))
    far.append(rect(870, 540, 180, 22, "#E8EEF8", rx=6))
    random.seed(7)
    for row, wy in enumerate((380, 470)):
        for wx in range(400, 1540, 120):
            if 840 <= wx <= 1040:
                continue
            lit = random.random() < 0.45
            far.append(rect(wx, wy, 70, 60, "#FFD98A" if lit else "#2B3556", rx=4))
            if lit:
                far.append(f'<rect x="{wx - 20}" y="{wy - 20}" width="110" height="100" rx="40" fill="#FFD98A" opacity=".12"/>')
            far.append(rect(wx - 4, wy + 56, 78, 10, "#E8EEF8", rx=4))
    # buried school bus
    mid = ['<path d="M 1460 840 L 1500 760 L 1880 760 L 1900 840 Z" fill="#F2B632"/>',
           rect(1520, 774, 70, 40, "#2B3556", rx=4), rect(1610, 774, 70, 40, "#2B3556", rx=4),
           rect(1700, 774, 70, 40, "#2B3556", rx=4), rect(1790, 774, 70, 40, "#2B3556", rx=4),
           rect(1490, 742, 400, 26, "#F4F7FC", rx=13)]
    # snow ground
    mid.append('<path d="M 0 800 Q 300 760 700 800 T 1400 790 T 1920 820 L 1920 1080 L 0 1080 Z" fill="#E9EFF8"/>')
    mid.append('<path d="M 0 900 Q 500 860 960 900 T 1920 890 L 1920 1080 L 0 1080 Z" fill="#D6E0EE"/>')
    # lamp post
    mid.append(rect(220, 520, 16, 380, "#2B3556"))
    mid.append('<path d="M 200 520 L 256 520 L 244 490 L 212 490 Z" fill="#2B3556"/>')
    mid.append('<circle cx="228" cy="530" r="90" fill="#FFE8A8" opacity=".18"/><circle cx="228" cy="528" r="14" fill="#FFF2C4"/>')
    fg = []
    random.seed(11)
    for _ in range(260):
        x, y = random.randint(0, W), random.randint(0, H)
        r = random.choice([2, 3, 3, 4, 6])
        fg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity="{random.choice([.5,.7,.9])}"/>')
    for _ in range(40):
        x, y = random.randint(0, W), random.randint(0, H)
        fg.append(f'<line x1="{x}" y1="{y}" x2="{x - 60}" y2="{y + 24}" stroke="#FFFFFF" stroke-width="2" opacity=".35"/>')
    return _svg([("sky", "".join(sky)), ("far", "".join(far)), ("mid", "".join(mid)), ("fg", "".join(fg))], defs)


# ---------------------------------------------------------------- BG05 bunker
def bunker():
    STAGE_LINE["BG05"] = 900
    far = [rect(0, 0, W, 820, "#8C978A"), rect(0, 0, W, 90, "#6F7A6E")]
    for x in range(0, W, 240):
        far.append(f'<line x1="{x}" y1="90" x2="{x}" y2="820" stroke="#7B8679" stroke-width="4"/>')
    for y in (300, 560):
        far.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#7B8679" stroke-width="4"/>')
    # pipes
    far.append(rect(0, 120, W, 26, "#5E6A73", rx=13))
    far.append(rect(0, 160, W, 16, "#A2593B", rx=8))
    for x in (300, 900, 1500):
        far.append(rect(x, 112, 30, 42, "#4B555E", rx=6))
    # hatch door
    far.append(f'<circle cx="960" cy="470" r="230" fill="#5E6A73" stroke="{INK}" stroke-width="10"/>')
    far.append('<circle cx="960" cy="470" r="190" fill="#6F7B85"/>')
    far.append(f'<circle cx="960" cy="470" r="70" fill="none" stroke="#C9A227" stroke-width="16"/>')
    for a in range(0, 360, 60):
        x2 = 960 + 100 * math.cos(math.radians(a))
        y2 = 470 + 100 * math.sin(math.radians(a))
        far.append(f'<line x1="960" y1="470" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#C9A227" stroke-width="12" stroke-linecap="round"/>')
    for a in range(0, 360, 30):
        x2 = 960 + 210 * math.cos(math.radians(a))
        y2 = 470 + 210 * math.sin(math.radians(a))
        far.append(f'<circle cx="{x2:.0f}" cy="{y2:.0f}" r="8" fill="#4B555E"/>')
    # warning sign
    far.append(rect(1270, 250, 150, 150, "#F2C230", rx=10))
    far.append('<circle cx="1345" cy="325" r="12" fill="#1F2A44"/>')
    for a in (-90, 30, 150):
        a1, a2 = math.radians(a - 30), math.radians(a + 30)
        p = f"1345,325 {1345 + 55 * math.cos(a1):.0f},{325 + 55 * math.sin(a1):.0f} {1345 + 55 * math.cos(a2):.0f},{325 + 55 * math.sin(a2):.0f}"
        far.append(f'<polygon points="{p}" fill="#1F2A44" opacity=".9"/>')
    far.append('<circle cx="1345" cy="325" r="20" fill="#F2C230"/><circle cx="1345" cy="325" r="11" fill="#1F2A44"/>')
    floor = [rect(0, 820, W, 260, "#5A6358"), rect(0, 820, W, 14, "#4A5249")]
    mid = []
    # bunk bed left
    mid.append(rect(80, 420, 22, 440, "#4B555E"))
    mid.append(rect(470, 420, 22, 440, "#4B555E"))
    for by in (520, 740):
        mid.append(rect(90, by, 400, 36, "#4B555E", rx=4))
        mid.append(rect(100, by - 34, 380, 40, "#7C8F6A", rx=12))
        mid.append(rect(110, by - 50, 110, 34, "#E8E4D8", rx=14))
    # shelves of cans right
    mid.append(rect(1560, 360, 300, 500, "#6B5A48"))
    for sy in (440, 560, 680, 800):
        mid.append(rect(1560, sy, 300, 14, "#4F4234"))
        for k in range(6):
            c = ["#D9534F", "#F0AD4E", "#5BC0DE", "#E6E6E6"][(k + sy // 120) % 4]
            mid.append(rect(1574 + k * 46, sy - 70, 38, 70, c, rx=6))
            mid.append(rect(1574 + k * 46, sy - 50, 38, 20, "#FFFFFF", extra='opacity=".6"'))
    # hanging bulb + light cone
    mid.append('<line x1="960" y1="90" x2="960" y2="200" stroke="#2B2B2B" stroke-width="4"/>')
    mid.append('<circle cx="960" cy="212" r="16" fill="#FFF1B8"/>')
    mid.append('<path d="M 950 220 L 640 900 L 1280 900 L 970 220 Z" fill="#FFF1B8" opacity=".14"/>')
    return _svg([("sky", ""), ("far", "".join(far) + "".join(floor)), ("mid", "".join(mid)), ("fg", "")])


# ---------------------------------------------------------------- BG06 abandoned mall
def mall():
    STAGE_LINE["BG06"] = 940
    far = [rect(0, 0, W, 900, "#B7B3C9")]
    # skylight
    far.append(rect(560, 0, 800, 70, "#DCEBF5"))
    for x in range(560, 1361, 100):
        far.append(f'<line x1="{x}" y1="0" x2="{x}" y2="70" stroke="#8D88A6" stroke-width="8"/>')
    far.append('<path d="M 560 70 L 360 940 L 1000 940 L 1360 70 Z" fill="#FFFFFF" opacity=".18"/>')
    # upper floor
    far.append(rect(0, 120, W, 260, "#A29DB8"))
    for i, x in enumerate(range(40, W, 380)):
        far.append(rect(x, 160, 320, 200, "#5D587A", rx=4))
        for k in range(0, 200, 16):
            far.append(f'<line x1="{x}" y1="{160 + k}" x2="{x + 320}" y2="{160 + k}" stroke="#4E496A" stroke-width="3"/>')
        sign = ["#FF6FA8", "#5FD3F3", "#FFD166", "#9CF6A0", "#C7A6FF"][i % 5]
        far.append(rect(x + 60, 130, 200, 22, sign, rx=11, extra='opacity=".55"'))
    far.append(rect(0, 380, W, 26, "#8D88A6"))
    for x in range(0, W, 60):
        far.append(rect(x, 330, 6, 50, "#7A7594"))
    far.append(rect(0, 322, W, 10, "#7A7594"))
    # ground floor stores
    for i, x in enumerate(range(20, W, 400)):
        far.append(rect(x, 480, 340, 420, "#4E496A", rx=4))
        far.append(rect(x + 20, 520, 300, 260, "#2F2B45", rx=4))
        far.append(f'<path d="M {x + 40} 540 L {x + 140} 760" stroke="#6A6590" stroke-width="5"/>')
        far.append(rect(x + 40, 440, 260, 30, "#3B3656", rx=6))
    far.append('<text x="1010" y="463" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="800" fill="#FF6FA8" opacity=".85">PIZZ</text>')
    # escalator
    mid = ['<path d="M 1300 900 L 1700 400 L 1780 400 L 1380 900 Z" fill="#8D88A6"/>',
           '<path d="M 1290 880 L 1690 380" stroke="#4E496A" stroke-width="14" stroke-linecap="round"/>']
    for k in range(10):
        x = 1320 + k * 40
        y = 870 - k * 50
        mid.append(rect(x, y, 70, 8, "#6A6590"))
    # floor + dry fountain + plants
    floor = [rect(0, 900, W, 180, "#CFC9DC")]
    for xx in range(0, W, 160):
        floor.append(f'<line x1="{xx}" y1="900" x2="{xx}" y2="1080" stroke="#BDB6CE" stroke-width="3"/>')
    mid.append('<ellipse cx="760" cy="930" rx="260" ry="50" fill="#9E98B5"/>')
    mid.append('<ellipse cx="760" cy="920" rx="220" ry="36" fill="#7E7898"/>')
    mid.append(rect(740, 820, 40, 100, "#9E98B5", rx=8))
    mid.append('<ellipse cx="760" cy="818" rx="60" ry="14" fill="#B7B1CC"/>')
    for (px, s) in [(120, 1), (1860, 1.2), (560, .8)]:
        mid.append(f'<g transform="translate({px},940) scale({s})">'
                   '<path d="M 0 0 Q -60 -120 -20 -200 Q 0 -100 0 0 Z" fill="#5E8C61"/>'
                   '<path d="M 0 0 Q 60 -140 30 -230 Q 10 -100 0 0 Z" fill="#6FA672"/>'
                   '<path d="M 0 0 Q -100 -60 -110 -130 Q -40 -60 0 0 Z" fill="#4E7A52"/></g>')
    fg = []
    random.seed(5)
    for _ in range(30):
        fg.append(f'<circle cx="{random.randint(400,1300)}" cy="{random.randint(120,900)}" r="2" fill="#FFFFFF" opacity=".5"/>')
    return _svg([("sky", ""), ("far", "".join(far) + "".join(floor)), ("mid", "".join(mid)), ("fg", "".join(fg))])


# ---------------------------------------------------------------- BG07 forest night
def forest():
    STAGE_LINE["BG07"] = 920
    defs = grad("sky", "#1A1440", "#4B3B7A")
    sky = [rect(0, 0, W, H, "url(#sky)"), '<circle cx="1500" cy="200" r="80" fill="#FFF6D8"/>',
           '<circle cx="1500" cy="200" r="140" fill="#FFF6D8" opacity=".08"/>']
    random.seed(2)
    for _ in range(80):
        sky.append(f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,500)}" r="{random.choice([1,1.5,2])}" fill="#FFFFFF" opacity=".8"/>')

    def pines(color, base, hmin, hmax, step, seed):
        random.seed(seed)
        out = []
        x = -40
        while x < W + 80:
            h = random.randint(hmin, hmax)
            w = h * 0.42
            out.append(f'<path d="M {x} {base} L {x + w / 2:.0f} {base - h} L {x + w:.0f} {base} Z" fill="{color}"/>')
            x += step + random.randint(-20, 20)
        out.append(rect(0, base - 2, W, H - base + 2, color))
        return "".join(out)

    far = pines("#3A2F66", 760, 260, 380, 110, 1)
    mid_t = pines("#2A2350", 840, 320, 460, 150, 2)
    ground = [rect(0, 880, W, 200, "#1E2A3A"), '<path d="M 0 880 Q 480 850 960 880 T 1920 875 L 1920 900 L 0 900 Z" fill="#26364A"/>']
    # campfire
    ground.append('<circle cx="560" cy="900" r="170" fill="#FF9F43" opacity=".14"/>')
    ground.append('<path d="M 500 920 L 620 896 M 510 896 L 620 922" stroke="#6B4226" stroke-width="16" stroke-linecap="round"/>')
    ground.append('<path d="M 560 900 Q 520 850 548 800 Q 556 840 572 820 Q 600 860 560 900 Z" fill="#FF7A1A"/>')
    ground.append('<path d="M 560 900 Q 540 868 556 840 Q 564 866 576 860 Q 584 884 560 900 Z" fill="#FFD23F"/>')
    fg = []
    random.seed(9)
    for _ in range(26):
        x, y = random.randint(0, W), random.randint(500, 860)
        fg.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#E9FF8A" opacity=".18"/><circle cx="{x}" cy="{y}" r="2.5" fill="#F3FFB0"/>')
    fg.append('<path d="M -40 1080 L 120 520 L 280 1080 Z" fill="#141B2B"/>')
    fg.append('<path d="M 1700 1080 L 1860 460 L 2020 1080 Z" fill="#141B2B"/>')
    return _svg([("sky", "".join(sky)), ("far", far), ("mid", mid_t + "".join(ground)), ("fg", "".join(fg))], defs)


# ---------------------------------------------------------------- BG08 kitchen macro
def macro():
    STAGE_LINE["BG08"] = 860
    defs = ('<filter id="blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="18"/></filter>'
            '<filter id="blur2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>'
            + grad("wall", "#F6E7CF", "#E9D3B0")
            + '<radialGradient id="drop" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".95"/>'
              '<stop offset=".4" stop-color="#BFE6FF" stop-opacity=".55"/><stop offset="1" stop-color="#6FB7E8" stop-opacity=".55"/></radialGradient>')
    sky = [rect(0, 0, W, H, "url(#wall)")]
    random.seed(4)
    bokeh = []
    for _ in range(22):
        c = random.choice(["#FFD98A", "#FFFFFF", "#FFB4A2", "#B5E2FA"])
        bokeh.append(f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,600)}" r="{random.randint(30,90)}" fill="{c}" opacity=".35"/>')
    far = [f'<g filter="url(#blur)">{"".join(bokeh)}'
           '<rect x="80" y="120" width="420" height="520" rx="30" fill="#C98F65" opacity=".7"/>'
           '<rect x="1500" y="60" width="300" height="600" rx="140" fill="#9FC5A8" opacity=".7"/></g>']
    mid = [f'<g filter="url(#blur2)"><path d="M 1100 820 Q 1100 360 1500 330 Q 1900 360 1900 820 Z" fill="#F5F5F5"/>'
           '<path d="M 1130 420 Q 1500 300 1880 420" fill="none" stroke="#E07A5F" stroke-width="40"/></g>']
    # giant sugar cube
    mid.append('<polygon points="300,840 300,600 520,560 700,620 700,840" fill="#FFFFFF"/>'
               '<polygon points="300,600 520,560 700,620 480,660" fill="#F4F6FA"/>'
               '<polygon points="480,660 700,620 700,840 480,860" fill="#E6EAF2"/>')
    random.seed(8)
    for _ in range(60):
        mid.append(f'<circle cx="{random.randint(310,690)}" cy="{random.randint(620,840)}" r="3" fill="#E1E6EF"/>')
    # tabletop wood
    table = [rect(0, 840, W, 240, "#B7834F")]
    for y in range(860, H, 36):
        table.append(f'<path d="M 0 {y} Q 480 {y - 10} 960 {y} T 1920 {y}" fill="none" stroke="#A3723F" stroke-width="5"/>')
    # crumbs
    for (cx, cy, r) in [(900, 850, 26), (980, 870, 14), (1260, 860, 34), (180, 880, 18)]:
        table.append(f'<path d="M {cx - r} {cy} Q {cx - r} {cy - r} {cx} {cy - r * 1.1} Q {cx + r} {cy - r} {cx + r} {cy} Z" fill="#E3B26C"/>')
    # water droplet
    fg = ['<ellipse cx="820" cy="790" rx="110" ry="80" fill="url(#drop)"/>',
          '<ellipse cx="790" cy="760" rx="28" ry="16" fill="#FFFFFF" opacity=".9"/>',
          '<ellipse cx="820" cy="868" rx="100" ry="10" fill="#6FB7E8" opacity=".25"/>']
    return _svg([("sky", "".join(sky)), ("far", "".join(far)), ("mid", "".join(mid) + "".join(table)), ("fg", "".join(fg))], defs)


BACKGROUNDS = [
    ("BG01", "bedroom_day", "Bo's Bedroom — Day", lambda: bedroom(False)),
    ("BG01N", "bedroom_night", "Bo's Bedroom — Night", lambda: bedroom(True)),
    ("BG02", "school_hallway", "School Hallway", hallway),
    ("BG03", "classroom", "Classroom", classroom),
    ("BG04", "school_blizzard_night", "School Exterior — Blizzard Night", blizzard),
    ("BG05", "bunker", "Underground Bunker", bunker),
    ("BG06", "abandoned_mall", "Abandoned Mall", mall),
    ("BG07", "forest_night", "Forest — Night", forest),
    ("BG08", "kitchen_macro", "Kitchen Table — Macro (ant scale)", macro),
]
