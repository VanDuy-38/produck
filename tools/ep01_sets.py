"""EP01 sets, props and graphics: "Snowed In at School With Your Crush".

Same contract as backgrounds.py: 1920x1080, layers sky/far/mid/fg, no outlines
on backgrounds, lower saturation than the characters. Props are fragments in
their own local coordinates (origin = bottom-centre unless noted) so the
animatic compositor can place them anywhere.
"""
import math
import random

from backgrounds import W, H, INK, STAGE_LINE, _svg, rect, grad, hallway, classroom, blizzard
import bo

FONT = 'font-family="Arial Rounded MT Bold, Arial, Helvetica, sans-serif"'
CHALK = 'font-family="Comic Sans MS, Chalkboard, Arial, sans-serif" fill="#F4F4F4"'
NIGHT = "#1B2350"


def text(x, y, s, size=40, fill="#FFFFFF", weight=900, anchor="middle", extra=""):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" {FONT} font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" {extra}>{s}</text>')


def snow_specks(seed, n=200, area=(0, 0, W, H), op=(.5, .7, .9), sizes=(2, 3, 3, 4, 6)):
    random.seed(seed)
    x0, y0, w, h = area
    return "".join(f'<circle cx="{random.randint(x0, x0 + w)}" cy="{random.randint(y0, y0 + h)}" '
                   f'r="{random.choice(sizes)}" fill="#FFFFFF" opacity="{random.choice(op)}"/>' for _ in range(n))


# =============================================================== PROPS
def vending_machine(count=37, glow=True):
    """Origin bottom-centre, 300 wide x 560 tall."""
    s = []
    if glow:
        s.append('<ellipse cx="0" cy="-280" rx="300" ry="330" fill="#BFE8FF" opacity=".16"/>')
    s.append(rect(-150, -560, 300, 560, "#C8454B", rx=14))
    s.append(rect(-130, -530, 190, 380, "#DDF3FF", rx=8))
    random.seed(count)
    cols = ["#FFB703", "#FB8500", "#8ECAE6", "#E76F51", "#90BE6D", "#F94144", "#577590", "#F9C74F"]
    left = count
    for r in range(5):
        for c in range(4):
            if left <= 0 or random.random() < 0.18:
                continue
            left -= 1
            s.append(rect(-120 + c * 46, -515 + r * 72, 36, 52, random.choice(cols), rx=5))
        s.append(rect(-130, -460 + r * 72, 190, 6, "#9BB8CC"))
    s.append(rect(76, -530, 56, 200, "#9E3237", rx=6))
    for i in range(6):
        s.append(f'<circle cx="{92 + (i % 2) * 24}" cy="{-500 + (i // 2) * 34}" r="8" fill="#F4F4F4"/>')
    s.append(rect(80, -300, 48, 36, "#1F2A44", rx=4))
    s.append(text(104, -274, str(count), 24, "#7CFF9B"))
    s.append(rect(-130, -120, 190, 60, "#2B3550", rx=6))
    s.append(rect(-160, -12, 320, 12, "#000000", extra='opacity=".18"'))
    return "".join(s)


def crank_radio(scale=1.0):
    """Origin bottom-centre, ~220 wide."""
    return (f'<g transform="scale({scale})">'
            + rect(-110, -130, 220, 130, "#E86A33", rx=18)
            + rect(-92, -112, 110, 80, "#2B3550", rx=8)
            + "".join(f'<circle cx="{-72 + i * 22}" cy="{-72 + j * 22}" r="5" fill="#556080"/>' for i in range(4) for j in range(2))
            + '<circle cx="62" cy="-72" r="26" fill="#F4F4F4"/><circle cx="62" cy="-72" r="10" fill="#C24E1E"/>'
            + '<rect x="98" y="-82" width="40" height="12" rx="6" fill="#6B7590"/><circle cx="140" cy="-76" r="10" fill="#6B7590"/>'
            + rect(-70, -152, 140, 22, "#C24E1E", rx=10)
            + rect(30, -24, 22, 12, "#1F2A44", rx=2) + text(41, -2, "USB", 12, "#1F2A44", anchor="middle")
            + '</g>')


def walkie(led=False, scale=1.0):
    on = "#7CFF9B" if led else "#3A4560"
    glow = f'<circle cx="-26" cy="-196" r="22" fill="#7CFF9B" opacity=".35"/>' if led else ""
    return (f'<g transform="scale({scale})">'
            + rect(-20, -250, 14, 70, "#2B3550", rx=6)
            + rect(-44, -190, 88, 190, "#3B4A6B", rx=14)
            + rect(-30, -170, 60, 46, "#9FB5C9", rx=6)
            + "".join(f'<line x1="-26" y1="{-104 + i * 12}" x2="26" y2="{-104 + i * 12}" stroke="#2B3550" stroke-width="5" stroke-linecap="round"/>' for i in range(5))
            + glow + f'<circle cx="-26" cy="-196" r="8" fill="{on}"/>'
            + '</g>')


def emergency_shelf(with_items=True):
    """Origin bottom-centre, 640 wide x 520 tall (wall shelf)."""
    s = [rect(-320, -520, 640, 26, "#8C6A54", rx=6), rect(-320, -260, 640, 26, "#8C6A54", rx=6),
         rect(-300, -494, 20, 494, "#7A5A45"), rect(280, -494, 20, 494, "#7A5A45"),
         rect(-230, -720, 460, 64, "#FFF7D6", rx=6),
         text(0, -677, "DO NOT TOUCH (YES, YOU)", 32, "#C0392B")]
    if with_items:
        s.append(f'<g transform="translate(-120,-260)">{crank_radio(.9)}</g>')
        s.append(f'<g transform="translate(160,-260)">{walkie(False, .8)}</g>')
        s.append(rect(-260, -520 + 26 - 120 - 26, 60, 94, "#9AD1D4", rx=6))
        s.append(rect(-180, -520 + 26 - 100 - 26, 50, 74, "#F2CC8F", rx=6))
        s.append(rect(60, -390, 150, 104, "#E9EEF5", rx=6) + text(135, -330, "FIRST AID", 20, "#C0392B"))
        s.append('<path d="M 130 -470 l 12 0 l 0 -14 l 14 0 l 0 14 l 12 0 l 0 14 l -12 0 l 0 14 l -14 0 l 0 -14 l -12 0 Z" fill="#C0392B"/>')
    return "".join(s)


def fort(open_side=True):
    """Gym-mat + encyclopedia fort. Origin bottom-centre, ~760 wide x 380 tall."""
    s = ['<ellipse cx="0" cy="0" rx="420" ry="26" fill="#000" opacity=".15"/>']
    mats = ["#3E6FB0", "#2F5E9E", "#4A7CBF"]
    # back mat (roof, tilted)
    s.append('<path d="M -360 -300 L 360 -300 L 330 -380 L -330 -380 Z" fill="#335F9C"/>')
    for i in range(6):
        s.append(f'<line x1="{-330 + i * 132}" y1="-380" x2="{-360 + i * 144}" y2="-300" stroke="#2A4F85" stroke-width="5"/>')
    # side walls of mats
    for i, x in enumerate((-380, -260)):
        s.append(rect(x, -300, 120, 300, mats[i % 3], rx=10))
        for y in (-220, -140, -60):
            s.append(f'<line x1="{x + 8}" y1="{y}" x2="{x + 112}" y2="{y}" stroke="#2A4F85" stroke-width="4"/>')
    for i, x in enumerate((140, 260)):
        s.append(rect(x, -300, 120, 300, mats[(i + 1) % 3], rx=10))
        for y in (-220, -140, -60):
            s.append(f'<line x1="{x + 8}" y1="{y}" x2="{x + 112}" y2="{y}" stroke="#2A4F85" stroke-width="4"/>')
    # doorway (dark) + encyclopedia stacks as insulation
    s.append(rect(-140, -300, 280, 300, "#1B2130" if open_side else "#3E6FB0"))
    spines = ["#8E3B46", "#3D5A80", "#2A9D8F", "#E9C46A", "#6D597A", "#B5651D"]
    random.seed(5)
    for side in (-1, 1):
        x0 = -470 if side < 0 else 380
        y = 0
        for k in range(9):
            hgt = random.choice([22, 26, 30])
            s.append(rect(x0 + random.randint(-6, 6), y - hgt, 90, hgt, random.choice(spines), rx=3))
            y -= hgt
    return "".join(s)


def gym_mat(x, y, w=380, h=60, color="#3E6FB0"):
    return rect(x - w / 2, y - h, w, h, color, rx=14) + rect(x - w / 2, y - 14, w, 14, "#2A4F85", rx=7)


def water_bottle(x, y, s=1.0, frozen=True):
    fill = "#DDEFFF" if frozen else "#9FD3FF"
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="-22" y="-110" width="44" height="110" rx="14" fill="{fill}" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="-12" y="-130" width="24" height="22" rx="4" fill="#5DA9FF" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="-14" y="-74" width="28" height="40" rx="6" fill="#FFFFFF" opacity=".7"/></g>')


def granola(x, y, s=1.0, half=False):
    w = 70 if half else 140
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="{-w / 2}" y="-34" width="{w}" height="34" rx="8" fill="#E9C46A" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{-w / 2 + 10}" y="-26" width="{w - 20}" height="18" rx="4" fill="#F4A261"/></g>')


def chocolate(x, y, s=1.0, label=True):
    t = text(0, -18, "EMERGENCY", 15, "#FFFFFF") if label else ""
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="-70" y="-40" width="140" height="40" rx="6" fill="#6B3E26" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="-50" y="-34" width="100" height="26" rx="3" fill="#C0392B"/>{t}</g>')


def snowplow(x, y, s=1.0, lights=True):
    beam = ('<circle cx="-150" cy="-300" r="40" fill="#FF9F1C" opacity=".35"/>'
            '<circle cx="-60" cy="-300" r="40" fill="#FF9F1C" opacity=".35"/>') if lights else ""
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<ellipse cx="0" cy="0" rx="360" ry="24" fill="#000" opacity=".15"/>'
            '<rect x="-200" y="-250" width="420" height="170" rx="20" fill="#F28C28"/>'
            '<rect x="-40" y="-380" width="220" height="150" rx="18" fill="#F28C28"/>'
            '<rect x="-20" y="-360" width="90" height="80" rx="8" fill="#BFE3F7"/>'
            '<rect x="85" y="-360" width="75" height="80" rx="8" fill="#BFE3F7"/>'
            '<rect x="-180" y="-400" width="150" height="22" rx="10" fill="#FFB703"/>'
            + beam +
            '<circle cx="-150" cy="-300" r="14" fill="#FFE066"/><circle cx="-60" cy="-300" r="14" fill="#FFE066"/>'
            '<path d="M -380 -40 L -250 -200 L -200 -200 L -200 -20 Z" fill="#E9C46A"/>'
            '<path d="M -400 -10 Q -330 -90 -250 -200" fill="none" stroke="#C99A2E" stroke-width="10"/>'
            '<circle cx="-110" cy="-70" r="62" fill="#2B3550"/><circle cx="-110" cy="-70" r="24" fill="#8C97B0"/>'
            '<circle cx="140" cy="-70" r="62" fill="#2B3550"/><circle cx="140" cy="-70" r="24" fill="#8C97B0"/>'
            + text(70, -170, "COUNTY 7", 38, "#1F2A44") + '</g>')


def grey_raincoat(x, y, s=1.0, opacity=1.0):
    """The series mystery. Tall, long grey coat, hat brim, face never seen. Origin = feet."""
    return (f'<g transform="translate({x},{y}) scale({s})" opacity="{opacity}">'
            '<ellipse cx="0" cy="0" rx="50" ry="8" fill="#000" opacity=".2"/>'
            '<path d="M -40 -250 Q -54 -120 -58 -18 L 58 -18 Q 54 -120 40 -250 Z" fill="#8A8F98"/>'
            '<path d="M 0 -250 L 0 -30" stroke="#6E737C" stroke-width="5"/>'
            '<rect x="-34" y="-20" width="24" height="20" rx="6" fill="#3A3F48"/><rect x="10" y="-20" width="24" height="20" rx="6" fill="#3A3F48"/>'
            '<path d="M -40 -250 L -64 -140" stroke="#7B8089" stroke-width="22" stroke-linecap="round"/>'
            '<path d="M 40 -250 L 64 -140" stroke="#7B8089" stroke-width="22" stroke-linecap="round"/>'
            '<ellipse cx="0" cy="-292" rx="34" ry="40" fill="#2E323A"/>'
            '<path d="M -40 -250 Q 0 -232 40 -250 L 30 -268 Q 0 -256 -30 -268 Z" fill="#9AA0A9"/>'
            '<ellipse cx="0" cy="-322" rx="62" ry="12" fill="#5C616A"/>'
            '<path d="M -34 -324 Q -30 -366 0 -368 Q 30 -366 34 -324 Z" fill="#5C616A"/>'
            '</g>')


def firefighter(face="neutral", pose_arms="idle"):
    """Guest: generic crowd body in turnout gear. Same build as Bo, Bo units."""
    coat, trim, helmet = "#F2B632", "#E8EEF8", "#C0392B"
    arms = {"idle": [[(-24, 62), (-60, 98)], [(24, 62), (60, 98)]],
            "camera": [[(-24, 62), (-30, 96), (10, 96)], [(24, 62), (40, 96), (28, 92)]]}[pose_arms]
    out = [bo._pl([(-9, 124), (-12, 174)], 9), bo._pl([(9, 124), (12, 174)], 9),
           f'<ellipse cx="-20" cy="184" rx="22" ry="11" fill="#2B3550" stroke="{INK}" stroke-width="5"/>',
           f'<ellipse cx="20" cy="184" rx="22" ry="11" fill="#2B3550" stroke="{INK}" stroke-width="5"/>']
    for a in arms:
        out.append(bo._pl(a, 9, INK))
        out.append(f'<circle cx="{a[-1][0]}" cy="{a[-1][1]}" r="9" fill="#2B3550" stroke="{INK}" stroke-width="5"/>')
    out.append(f'<path d="M -26 48 L 26 48 Q 34 100 22 130 L -22 130 Q -34 100 -26 48 Z" fill="{coat}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    out.append(f'<rect x="-28" y="100" width="56" height="9" fill="{trim}"/>')
    if pose_arms == "camera":
        out.append(f'<rect x="-8" y="78" width="50" height="34" rx="6" fill="#2B3550" stroke="{INK}" stroke-width="4"/>'
                   f'<rect x="-2" y="84" width="30" height="22" rx="3" fill="#FF7A3D"/>')
    out.append(f'<rect x="-46" y="-40" width="92" height="84" rx="40" fill="{bo.SKIN}" stroke="{INK}" stroke-width="5"/>')
    out.append(f'<circle cx="-28" cy="22" r="5" fill="{bo.BLUSH}"/><circle cx="28" cy="22" r="5" fill="{bo.BLUSH}"/>')
    out.append(bo.FACES[face][1])
    out.append(f'<path d="M -56 -10 Q -54 -66 0 -66 Q 54 -66 56 -10 Z" fill="{helmet}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
               f'<path d="M -66 -8 L 66 -8" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
               f'<rect x="-14" y="-58" width="28" height="30" rx="5" fill="#FFD23F" stroke="{INK}" stroke-width="3"/>')
    return "".join(out)


# =============================================================== SETS
def library(night=True, with_fort=True):
    STAGE_LINE["BG09"] = 930
    far = [rect(0, 0, W, 820, "#D8D2C4"), rect(0, 780, W, 40, "#BFB6A3")]
    spines = ["#9C4F57", "#4E6E91", "#4F8F86", "#C9A55C", "#7A6A8C", "#B07A4F", "#5E7D5A"]
    random.seed(21)
    for bx in (60, 420, 1500):
        far.append(rect(bx, 120, 340, 660, "#8C6A54", rx=6))
        for sy in range(150, 760, 120):
            far.append(rect(bx + 16, sy + 96, 308, 14, "#7A5A45"))
            x = bx + 20
            while x < bx + 310:
                w = random.choice([16, 20, 24, 28])
                h = random.choice([70, 80, 88, 94])
                far.append(rect(x, sy + 96 - h, w, h, random.choice(spines), rx=2))
                x += w + 3
    # tall window (snow-blocked lower half)
    far.append(rect(820, 120, 560, 520, "#2E3770" if night else "#BFE3F7", rx=10))
    far.append('<path d="M 820 640 L 820 470 Q 900 430 1000 470 T 1200 460 T 1380 470 L 1380 640 Z" fill="#E8EEF8"/>')
    far.append(snow_specks(4, 40, (830, 130, 540, 330)))
    far.append(f'<rect x="820" y="120" width="560" height="520" rx="10" fill="none" stroke="#EDE6D6" stroke-width="16"/>'
               '<line x1="1100" y1="120" x2="1100" y2="640" stroke="#EDE6D6" stroke-width="12"/>')
    far.append(rect(860, 60, 480, 40, "#2F5D50", rx=6) + text(1100, 92, "LIBRARY", 28, "#F4F4F4"))
    floor = [rect(0, 820, W, 260, "#8F7A9C")]
    floor.append('<ellipse cx="960" cy="960" rx="760" ry="80" fill="#9F8BAC"/>')
    mid = []
    if with_fort:
        mid.append(f'<g transform="translate(960,930)">{fort()}</g>')
    layers = [("sky", ""), ("far", "".join(far) + "".join(floor)), ("mid", "".join(mid)), ("fg", "")]
    if night:
        layers.append(("night-grade", rect(0, 0, W, H, NIGHT, extra='opacity=".5"')))
    return _svg(layers)


def fort_inside(night=True):
    """Close set inside the fort: an encyclopedia wall behind, slanted gym mats left/right,
    mat ceiling, and a warm pool of light from Bo's headphone nightlight."""
    STAGE_LINE["BG09I"] = 1000
    far = [rect(0, 0, W, H, "#2A3350")]
    spines = ["#9C4F57", "#4E6E91", "#4F8F86", "#C9A55C", "#7A6A8C", "#B07A4F", "#5E7D5A", "#C46A4E"]
    random.seed(9)
    y = 900
    while y > 60:
        hgt = random.choice([34, 40, 46])
        x = -random.randint(0, 120)
        while x < W:
            w = random.choice([260, 300, 340])
            c = random.choice(spines)
            far.append(rect(x + 3, y - hgt, w - 6, hgt - 4, c, rx=4))
            far.append(rect(x + 20, y - hgt / 2 - 3, 40, 6, "#F2E6C9", rx=3, extra='opacity=".55"'))
            x += w
        y -= hgt
    # mat ceiling
    far.append('<path d="M 0 0 L 1920 0 L 1920 70 L 1500 150 L 420 150 L 0 70 Z" fill="#2F5E9E"/>')
    # slanted mats left / right
    for pts in ("0,60 430,150 330,1080 0,1080", "1920,60 1490,150 1590,1080 1920,1080"):
        far.append(f'<polygon points="{pts}" fill="#3E6FB0"/>')
    for k in range(1, 4):
        far.append(f'<line x1="{430 - k * 100 * .25:.0f}" y1="{150 + k * 230}" x2="0" y2="{60 + k * 250}" stroke="#2F5E9E" stroke-width="6"/>')
        far.append(f'<line x1="{1490 + k * 100 * .25:.0f}" y1="{150 + k * 230}" x2="1920" y2="{60 + k * 250}" stroke="#2F5E9E" stroke-width="6"/>')
    floor = [rect(0, 900, W, 180, "#355E96"), rect(0, 900, W, 14, "#2A4F85"),
             '<ellipse cx="960" cy="1000" rx="620" ry="70" fill="#4A72A8"/>']
    layers = [("sky", ""), ("far", "".join(far)), ("mid", "".join(floor)), ("fg", "")]
    if night:
        layers.append(("night-grade", rect(0, 0, W, H, NIGHT, extra='opacity=".42"')))
        layers.append(("glow", '<ellipse cx="960" cy="660" rx="820" ry="520" fill="url(#nightlight)"/>'))
    defs = ('<radialGradient id="nightlight"><stop offset="0" stop-color="#FFF1C9" stop-opacity=".26"/>'
            '<stop offset="1" stop-color="#FFF1C9" stop-opacity="0"/></radialGradient>')
    return _svg(layers, defs)


def gym(night=True, mats=True):
    STAGE_LINE["BG10"] = 920
    far = [rect(0, 0, W, 700, "#A9B4C2"), rect(0, 640, W, 60, "#8E99A8")]
    # high windows, snow-filled
    for wx in range(120, W, 360):
        far.append(rect(wx, 70, 240, 120, "#E8EEF8", rx=6))
        far.append(f'<rect x="{wx}" y="70" width="240" height="120" rx="6" fill="none" stroke="#7D8899" stroke-width="10"/>')
    # folded bleachers left
    for i in range(6):
        far.append(rect(40 + i * 10, 300 + i * 56, 560 - i * 20, 50, "#9A7B5C" if i % 2 else "#8A6C4F", rx=4))
    # hoop
    far.append(rect(1460, 200, 300, 200, "#F4F7FB", rx=8) + rect(1560, 280, 100, 80, "none", extra='stroke="#C0392B" stroke-width="8"'))
    far.append(rect(1598, 400, 24, 300, "#5C6779"))
    far.append('<ellipse cx="1610" cy="420" rx="70" ry="16" fill="none" stroke="#E67E22" stroke-width="10"/>')
    far.append(rect(860, 120, 220, 70, "#C0392B", rx=8) + text(970, 170, "GO WOLVES", 30, "#F4F4F4"))
    floor = [rect(0, 700, W, 380, "#C9A06A")]
    for y in (760, 840, 940, 1050):
        floor.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#B88E5B" stroke-width="3"/>')
    floor.append('<path d="M 260 1080 Q 960 720 1660 1080" fill="none" stroke="#F4F4F4" stroke-width="8" opacity=".8"/>')
    floor.append('<line x1="960" y1="700" x2="960" y2="1080" stroke="#F4F4F4" stroke-width="8" opacity=".8"/>')
    mid = [gym_mat(960, 930, 420, 50)] if mats else []
    layers = [("sky", ""), ("far", "".join(far) + "".join(floor)), ("mid", "".join(mid)), ("fg", "")]
    if night:
        layers.append(("night-grade", rect(0, 0, W, H, NIGHT, extra='opacity=".62"')))
    return _svg(layers)


def front_doors(night=True):
    STAGE_LINE["BG11"] = 930
    far = [rect(0, 0, W, 860, "#C9C2B4"), rect(0, 820, W, 40, "#AFA796")]
    far.append(rect(560, 150, 800, 680, "#6B7686", rx=8))
    for dx in (590, 970):
        far.append(rect(dx, 180, 360, 640, "#F2F5FA", rx=4))  # snow wall right behind the glass
        random.seed(dx)
        for _ in range(26):
            far.append(f'<ellipse cx="{dx + random.randint(10, 350)}" cy="{random.randint(200, 800)}" rx="{random.randint(20, 60)}" ry="{random.randint(8, 20)}" fill="#DCE4EF"/>')
        far.append(f'<rect x="{dx}" y="180" width="360" height="640" rx="4" fill="none" stroke="#5A6474" stroke-width="18"/>')
        far.append(rect(dx + 40, 470, 280, 22, "#9AA3B0", rx=11))
    far.append(rect(880, 60, 160, 64, "#2E7D32", rx=8) + text(960, 106, "EXIT", 38, "#FFFFFF"))
    floor = [rect(0, 860, W, 220, "#9AA3B0"), rect(0, 860, W, 14, "#7F8896")]
    for xx in range(0, W, 140):
        floor.append(f'<line x1="{xx}" y1="874" x2="{xx - 70}" y2="1080" stroke="#8A93A0" stroke-width="3"/>')
    layers = [("sky", ""), ("far", "".join(far) + "".join(floor)), ("mid", ""), ("fg", "")]
    if night:
        layers.append(("night-grade", rect(0, 0, W, H, NIGHT, extra='opacity=".35"')))
    return _svg(layers)


def window_view(outside="storm", fill=0.0, night=True):
    """Interior wall with a big window. outside: storm | field | dawn. fill = 0..1 snow piled up the glass."""
    STAGE_LINE["BG12"] = 1000
    skies = {"storm": ("#0F1630", "#3A4B7A"), "field": ("#0F1630", "#2E3B66"), "dawn": ("#F6B48F", "#FBE3C4")}
    defs = grad("wsky", *skies[outside])
    far = [rect(0, 0, W, H, "#CFC6B2")]
    far.append(rect(300, 90, 1320, 820, "url(#wsky)", rx=10))
    out = []
    out.append('<path d="M 300 760 Q 700 700 1000 740 T 1620 730 L 1620 910 L 300 910 Z" fill="#E9EFF8"/>')
    if outside != "dawn":
        out.append(snow_specks(31, 160, (300, 90, 1320, 820)))
        random.seed(32)
        for _ in range(40):
            x, y = random.randint(300, 1600), random.randint(100, 880)
            out.append(f'<line x1="{x}" y1="{y}" x2="{x - 50}" y2="{y + 20}" stroke="#FFFFFF" stroke-width="2" opacity=".4"/>')
    if fill > 0:
        top = 910 - 820 * fill
        out.append(f'<path d="M 300 910 L 300 {top + 40} Q 600 {top - 20} 900 {top + 20} T 1620 {top} L 1620 910 Z" fill="#F2F5FA"/>')
        out.append(f'<path d="M 300 910 L 300 {top + 120} Q 700 {top + 60} 1100 {top + 110} T 1620 {top + 90} L 1620 910 Z" fill="#DCE4EF"/>')
    far.append("".join(out))
    far.append('<rect x="300" y="90" width="1320" height="820" rx="10" fill="none" stroke="#EDE6D6" stroke-width="26"/>'
               '<line x1="960" y1="90" x2="960" y2="910" stroke="#EDE6D6" stroke-width="18"/>'
               '<line x1="300" y1="500" x2="1620" y2="500" stroke="#EDE6D6" stroke-width="18"/>')
    far.append(rect(260, 910, 1400, 40, "#BDB29A", rx=8))
    layers = [("sky", ""), ("far", "".join(far)), ("mid", ""), ("fg", "")]
    if night and outside != "dawn":
        layers.append(("night-grade", rect(0, 0, W, H, NIGHT, extra='opacity=".35"')))
    return _svg(layers, defs)


def science_room(night=True):
    STAGE_LINE["BG13"] = 900
    far = [rect(0, 0, W, 820, "#D6E2DA"), rect(0, 780, W, 40, "#B9C8BE")]
    far.append(rect(80, 140, 420, 260, "#2F5D50", rx=8) + f'<text x="110" y="220" font-size="36" {CHALK}>PV = nRT</text>')
    far.append('<circle cx="1700" cy="300" r="110" fill="#E9EEF5"/><path d="M 1640 250 h 120 v 100 h -120 Z" fill="#9AD1D4" opacity=".6"/>')
    far.append(text(1700, 460, "SAFETY FIRST", 26, "#4C6A5C"))
    floor = [rect(0, 820, W, 260, "#A9B8AE")]
    for xx in range(0, W, 180):
        floor.append(f'<line x1="{xx}" y1="820" x2="{xx - 90}" y2="1080" stroke="#97A69C" stroke-width="3"/>')
    mid = [f'<g transform="translate(980,800) scale(1.25)">{emergency_shelf()}</g>']
    # lab bench foreground left
    fg = [rect(-20, 940, 560, 40, "#4C5A6B", rx=6), rect(20, 980, 30, 120, "#3C4757"), rect(470, 980, 30, 120, "#3C4757"),
          '<path d="M 200 940 L 230 860 L 270 860 L 300 940 Z" fill="#9AD1D4" opacity=".8"/>', rect(222, 840, 56, 24, "#BFD9DC", rx=4)]
    layers = [("sky", ""), ("far", "".join(far) + "".join(floor)), ("mid", "".join(mid)), ("fg", "".join(fg))]
    if night:
        layers.append(("night-grade", rect(0, 0, W, H, NIGHT, extra='opacity=".42"')))
    return _svg(layers)


def hallway_dark(vending=True, count=37, tally=None):
    """BG02 with the power out + the vending machine glowing at the end."""
    STAGE_LINE["BG14"] = 930
    svg = hallway()
    mid = ""
    if vending:
        tally_svg = ""
        if tally is not None:
            tally_svg = (f'<g transform="translate(1440,560)"><rect x="-56" y="-40" width="112" height="56" rx="6" fill="#FFF7D6" opacity=".9"/>'
                         + text(0, 2, str(tally), 40, "#C0392B") + '</g>')
        mid = f'<g transform="translate(1500,900)">{vending_machine(count)}</g>{tally_svg}'
    svg = svg.replace('<g id="layer-fg">', f'<g id="layer-props">{mid}</g><g id="layer-fg">', 1)
    grade = rect(0, 0, W, H, NIGHT, extra='opacity=".62"')
    glow = ('<ellipse cx="1500" cy="620" rx="330" ry="360" fill="#BFE8FF" opacity=".10"/>' if vending else "")
    return svg.replace("</svg>", f'<g id="layer-night-grade">{grade}</g><g id="layer-glow">{glow}</g></svg>')


def classroom_night():
    STAGE_LINE["BG03N"] = 860
    svg = classroom()
    grade = rect(0, 0, W, H, NIGHT, extra='opacity=".38"')
    return svg.replace("</svg>", f'<g id="layer-night-grade">{grade}</g></svg>')


def school_dawn(plow=False, doors_dug=False):
    """BG04 at dawn: blizzard over, warm sky, lights off."""
    STAGE_LINE["BG04D"] = 940
    svg = blizzard()
    svg = svg.replace('stop-color="#0F1630"', 'stop-color="#F7B58C"').replace('stop-color="#3A4B7A"', 'stop-color="#FCE6C8"')
    svg = svg.replace('fill="#FFD98A"', 'fill="#7C8FB0"')
    # drop the falling snow (fg layer) for a clear morning
    i = svg.find('<g id="layer-fg">')
    j = svg.find('</g>', i)
    svg = svg[:i] + '<g id="layer-fg">' + svg[j:]
    extra = '<circle cx="1640" cy="230" r="80" fill="#FFF1C9" opacity=".9"/>'
    if doors_dug:
        extra += rect(880, 560, 160, 190, "#3D2B2B", rx=4) + rect(860, 740, 200, 30, "#C9D3E3", rx=8)
    if plow:
        extra += snowplow(1300, 960, .9)
    return svg.replace('<g id="layer-fg">', f'<g id="layer-extra">{extra}</g><g id="layer-fg">', 1)


def blizzard_field_with_figure(show_figure=True, footprints=False):
    """Seen through the window at night (6.4/6.5)."""
    svg = window_view("field", 0.15)
    add = ""
    if show_figure:
        add += grey_raincoat(1220, 780, .9)
    if footprints:
        for k in range(9):
            x = 1180 - k * 70
            y = 780 + k * 8
            add += f'<ellipse cx="{x}" cy="{y}" rx="14" ry="6" fill="#B9C6DA"/><ellipse cx="{x - 26}" cy="{y + 12}" rx="14" ry="6" fill="#B9C6DA"/>'
    return svg.replace('<g id="layer-mid">', f'<g id="layer-figure">{add}</g><g id="layer-mid">', 1)


# =============================================================== GRAPHICS (full-frame)
GFX_BG = "#1B2350"


def _gfx(inner, bg=GFX_BG):
    return _svg([("sky", rect(0, 0, W, H, bg)), ("far", inner), ("mid", ""), ("fg", "")])


def gfx_rule_of_threes(highlight=None):
    items = [("AIR", "3 MIN", "#8ECAE6"), ("SHELTER", "3 HRS", "#FFB703"), ("WATER", "3 DAYS", "#5DA9FF"), ("FOOD", "3 WKS", "#90BE6D")]
    s = [text(960, 150, "THE RULE OF THREES", 64, "#FFD23F")]
    for i, (name, t, c) in enumerate(items):
        x = 300 + i * 440
        op = "1" if highlight is None or highlight == i else ".35"
        s.append(f'<g opacity="{op}">')
        s.append(f'<circle cx="{x}" cy="480" r="150" fill="{c}"/>')
        icon = {0: '<path d="M -70 0 q 30 -40 60 0 t 60 0 t 40 0" fill="none" stroke="#1F2A44" stroke-width="14" stroke-linecap="round"/>',
                1: '<path d="M -80 30 L 0 -60 L 80 30 Z" fill="#1F2A44"/><rect x="-55" y="30" width="110" height="60" fill="#1F2A44"/>',
                2: '<path d="M 0 -80 Q 60 10 0 70 Q -60 10 0 -80 Z" fill="#1F2A44"/>',
                3: '<rect x="-70" y="-10" width="140" height="60" rx="14" fill="#1F2A44"/><path d="M -60 -10 Q 0 -90 60 -10 Z" fill="#1F2A44"/>'}[i]
        s.append(f'<g transform="translate({x},470)">{icon}</g>')
        s.append(text(x, 720, name, 44, "#F4F4F4"))
        s.append(text(x, 800, t, 60, "#FFD23F"))
        s.append('</g>')
    return _gfx("".join(s))


def gfx_light_bulbs():
    s = [text(960, 140, "≈ 100 W EACH", 70, "#FFD23F")]
    for x in (660, 1260):
        s.append(f'<circle cx="{x}" cy="520" r="260" fill="#FFD23F" opacity=".18"/>')
        s.append(f'<circle cx="{x}" cy="520" r="170" fill="#FFD23F" opacity=".28"/>')
        s.append(f'<g transform="translate({x},640) scale(2.2)" opacity=".95">'
                 f'<rect x="-46" y="-140" width="92" height="84" rx="40" fill="#FFE9A8"/>'
                 f'<path d="M -28 -50 L 28 -50 Q 36 0 22 28 L -22 28 Q -36 0 -28 -50 Z" fill="#FFE9A8"/></g>')
    s.append(text(960, 960, "1 PERSON ≈ 1 OLD LIGHT BULB", 44, "#F4F4F4"))
    return _gfx("".join(s))


def gfx_snow_cost():
    s = [text(960, 140, "EATING SNOW", 70, "#FFD23F")]
    s.append(f'<g transform="translate(700,580) scale(2.4)">{bo.body("idle", face="nervous", mood="panic")}</g>')
    s.append('<circle cx="700" cy="690" r="44" fill="#F2F5FA" stroke="#1F2A44" stroke-width="6"/>')
    # thermometer
    s.append('<rect x="1250" y="260" width="70" height="520" rx="35" fill="#F4F4F4"/>'
             '<circle cx="1285" cy="800" r="70" fill="#5DA9FF"/><rect x="1265" y="560" width="40" height="240" fill="#5DA9FF"/>')
    s.append('<path d="M 1380 360 L 1380 640 M 1350 600 L 1380 650 L 1410 600" fill="none" stroke="#FF4D4D" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(text(1300, 960, "YOUR HEAT MELTS IT", 44, "#F4F4F4"))
    return _gfx("".join(s))


def gfx_fuel_gauge(level=0.8):
    s = [text(960, 140, "SHIVERING BURNS FUEL", 64, "#FFD23F")]
    s.append(f'<g transform="translate(560,560) scale(2.4)">{bo.body("cower", face="sad", mood="sad")}</g>')
    cx, cy = 1300, 620
    s.append(f'<path d="M {cx - 260} {cy} A 260 260 0 0 1 {cx + 260} {cy}" fill="none" stroke="#3A4B7A" stroke-width="60"/>')
    s.append(f'<path d="M {cx - 260} {cy} A 260 260 0 0 1 {cx - 200} {cy - 170}" fill="none" stroke="#FF4D4D" stroke-width="60"/>')
    a = math.pi * (1 - level)
    s.append(f'<line x1="{cx}" y1="{cy}" x2="{cx - 220 * math.cos(a):.0f}" y2="{cy - 220 * math.sin(a):.0f}" stroke="#F4F4F4" stroke-width="16" stroke-linecap="round"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="24" fill="#F4F4F4"/>' + text(cx - 260, cy + 70, "E", 50, "#FF4D4D") + text(cx + 260, cy + 70, "F", 50, "#F4F4F4"))
    s.append(text(1300, 900, "UP TO 5× NORMAL", 48, "#F4F4F4"))
    return _gfx("".join(s))


def gfx_brain_frost():
    s = [text(960, 140, "MILD HYPOTHERMIA", 64, "#FFD23F")]
    s.append('<path d="M 760 640 Q 640 600 660 480 Q 640 360 780 330 Q 840 240 960 270 Q 1080 230 1150 320 Q 1290 340 1270 470 Q 1300 600 1170 640 Q 1100 720 960 690 Q 830 720 760 640 Z" fill="#FF9AA2"/>')
    s.append('<path d="M 960 280 L 960 690 M 800 420 q 60 30 0 80 M 1120 420 q -60 30 0 80" fill="none" stroke="#C96A78" stroke-width="12" stroke-linecap="round"/>')
    s.append('<path d="M 700 560 Q 760 500 840 560 Q 900 500 980 560 Q 1060 500 1130 560 Q 1200 500 1250 560 L 1270 640 Q 1100 720 960 690 Q 830 720 700 640 Z" fill="#DDF3FF" opacity=".9"/>')
    s.append(text(960, 860, "SLOWER THINKING · WORSE CHOICES", 48, "#F4F4F4"))
    return _gfx("".join(s))


def gfx_temp_line(stop_shiver=True):
    s = [text(960, 140, "WHEN SHIVERING STOPS", 64, "#FFD23F")]
    s.append('<line x1="300" y1="820" x2="1660" y2="820" stroke="#5B6785" stroke-width="6"/><line x1="300" y1="260" x2="300" y2="820" stroke="#5B6785" stroke-width="6"/>')
    s.append('<path d="M 300 330 Q 700 360 1000 520 T 1640 760" fill="none" stroke="#5DA9FF" stroke-width="16" stroke-linecap="round"/>')
    s.append(text(240, 340, "98.6°F", 32, "#F4F4F4", anchor="end") + text(240, 760, "86°F", 32, "#F4F4F4", anchor="end"))
    s.append('<line x1="1120" y1="260" x2="1120" y2="820" stroke="#FF4D4D" stroke-width="5" stroke-dasharray="16 12"/>')
    s.append(text(700, 300, "SHIVERING ON", 40, "#90BE6D") + text(1400, 300, "SHIVERING OFF" if stop_shiver else "", 40, "#FF4D4D"))
    s.append(text(960, 950, "NOT WARM. RUNNING OUT.", 48, "#F4F4F4"))
    return _gfx("".join(s))


def gfx_town_map():
    s = [rect(0, 0, W, H, "#E8EEF8")]
    random.seed(41)
    for _ in range(70):
        x, y = random.randint(40, 1860), random.randint(40, 1020)
        s.append(rect(x, y, 34, 30, "#C9D3E3", rx=4))
    s.append('<path d="M 0 540 L 1920 520 M 640 0 L 700 1080 M 1300 0 L 1240 1080 M 0 230 Q 900 300 1920 200" stroke="#FFFFFF" stroke-width="40" fill="none"/>')
    s.append(rect(1480, 760, 60, 50, "#8B5E54", rx=6) + '<circle cx="1510" cy="785" r="70" fill="none" stroke="#FF4D4D" stroke-width="6" stroke-dasharray="10 10"/>')
    s.append(text(1510, 880, "YOU ARE HERE", 34, "#1F2A44"))
    s.append(text(400, 120, "WESTBROOK", 56, "#5B6785"))
    s.append('<circle cx="500" cy="480" r="140" fill="#FFD23F" opacity=".25"/>' + text(500, 490, "EVERYONE ELSE", 30, "#5B6785"))
    return _svg([("sky", ""), ("far", "".join(s)), ("mid", ""), ("fg", "")])


def gfx_thermal():
    s = [rect(0, 0, W, H, "#120B2E")]
    s.append(rect(160, 120, 1600, 840, "#1E1250", rx=20))
    for x, y, r in [(760, 600, 150), (1000, 610, 140), (1420, 470, 120)]:
        s.append(f'<circle cx="{x}" cy="{y}" r="{r * 1.5}" fill="#B11E4F" opacity=".6"/>'
                 f'<circle cx="{x}" cy="{y}" r="{r}" fill="#F25F2A"/><circle cx="{x}" cy="{y}" r="{r * .55}" fill="#FFE066"/>')
    s.append(text(260, 200, "THERMAL", 40, "#FFE066", anchor="start") + text(1680, 200, "3", 70, "#FFE066", anchor="end"))
    s.append('<line x1="960" y1="500" x2="960" y2="700" stroke="#FFFFFF" stroke-width="3" opacity=".5"/><line x1="860" y1="600" x2="1060" y2="600" stroke="#FFFFFF" stroke-width="3" opacity=".5"/>')
    return _svg([("sky", ""), ("far", "".join(s)), ("mid", ""), ("fg", "")])


def chalk_math(step=1):
    """BG03 with the snack math on the board (4.11–4.12)."""
    STAGE_LINE["BG03M"] = 860
    svg = classroom()
    # wipe the board text, then write the math
    for t in ("F = m × a", "H₂O → ice @ 0°C"):
        svg = svg.replace(f">{t}</text>", "></text>")
    svg = svg.replace('<path d="M 1100 240 q 80 -60 160 0 t 160 0" fill="none" stroke="#F4F4F4" stroke-width="5" opacity=".8"/>', "")
    svg = svg.replace('<circle cx="1260" cy="420" r="70" fill="none" stroke="#F4F4F4" stroke-width="5" opacity=".8"/>', "")
    lines = ["37 snacks ÷ 2 people = ? days"]
    if step >= 2:
        lines += ["37 × ~250 = ~9,250 kcal", "2 × 2,000 = 4,000 / day"]
    board = "".join(f'<text x="480" y="{250 + i * 90}" font-size="52" {CHALK}>{l}</text>' for i, l in enumerate(lines))
    if step >= 2:
        board += f'<text x="1200" y="520" font-size="72" {CHALK} fill="#FFD23F">≈ 2 DAYS</text>'
    svg = svg.replace('<g id="layer-mid">', f'<g id="layer-board">{board}</g><g id="layer-mid">', 1)
    grade = rect(0, 0, W, H, NIGHT, extra='opacity=".3"')
    return svg.replace("</svg>", f'<g id="layer-night-grade">{grade}</g></svg>')


# registry used by the animatic + build_art
SETS = {
    "BG02": hallway,
    "BG03": classroom,
    "BG03N": classroom_night,
    "BG04": blizzard,
    "BG04D": school_dawn,
    "BG09": library,
    "BG09I": fort_inside,
    "BG10": gym,
    "BG11": front_doors,
    "BG12": window_view,
    "BG13": science_room,
    "BG14": hallway_dark,
    "MATH": chalk_math,
    "FIELD": blizzard_field_with_figure,
    "GFX_THREES": gfx_rule_of_threes,
    "GFX_BULBS": gfx_light_bulbs,
    "GFX_SNOW": gfx_snow_cost,
    "GFX_FUEL": gfx_fuel_gauge,
    "GFX_BRAIN": gfx_brain_frost,
    "GFX_TEMP": gfx_temp_line,
    "GFX_MAP": gfx_town_map,
    "GFX_THERMAL": gfx_thermal,
}

STAGE_LINE.update({"BG09": 930, "BG09I": 1000, "BG10": 920, "BG11": 930, "BG12": 1000, "BG13": 900,
                   "BG14": 930, "BG04D": 940, "BG03N": 860, "MATH": 860, "FIELD": 1000})

# what build_art.py exports as reusable season sets
EXPORT = [
    ("BG09", "library_fort_night", lambda: library(True, True)),
    ("BG09I", "fort_inside_night", lambda: fort_inside(True)),
    ("BG10", "gym_dark", lambda: gym(True)),
    ("BG11", "front_doors_snowed_in", lambda: front_doors(True)),
    ("BG12", "window_blizzard_interior", lambda: window_view("storm", 0.4)),
    ("BG13", "science_room_emergency_shelf", lambda: science_room(True)),
    ("BG14", "hallway_power_out_vending", lambda: hallway_dark(True)),
    ("BG04D", "school_dawn_snowplow", lambda: school_dawn(True, True)),
]
