"""BO — character geometry, faces and poses.

All coordinates are in "Bo units" with the origin at the centre of the head.
Bo is ~250 units tall (top of headband -58 → bottom of shoes +194).
Import this module from build_art.py; nothing here writes files.
"""

INK = "#1F2A44"          # outline navy
SKIN = "#FFE0C2"
JACKET = "#FF6B6B"
HEADPHONE = "#FFC83D"
SHOE = "#FFFFFF"
BLUSH = "#FF9AA2"
TEAR = "#5DA9FF"

# Headphone "mood light" — Bo's emotion meter (small light on each ear cup)
MOOD = {
    "calm": "#FFFFFF",
    "idea": "#6BE38A",
    "panic": "#FF4D4D",
    "sad": "#5DA9FF",
    "crush": "#FF7EC8",
    "focus": "#B08CFF",
    "off": "#3A4560",   # dead light (EP01: cable cut)
}


def _pl(points, width=7, color=INK):
    d = " ".join(f"{x},{y}" for x, y in points)
    return (f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


# --------------------------------------------------------------------------
# FACES (head-local coordinates; eyes ≈ y 6, mouth ≈ y 28)
# --------------------------------------------------------------------------
def _dot_eyes(dx=15, y=6, r=4.5):
    return (f'<circle cx="{-dx}" cy="{y}" r="{r}" fill="{INK}"/>'
            f'<circle cx="{dx}" cy="{y}" r="{r}" fill="{INK}"/>')


def _white_eyes(py=1, r=10, pr=3.5, px=0):
    return (f'<circle cx="-15" cy="5" r="{r}" fill="#fff" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="15" cy="5" r="{r}" fill="#fff" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="{-15 + px}" cy="{5 + py}" r="{pr}" fill="{INK}"/>'
            f'<circle cx="{15 + px}" cy="{5 + py}" r="{pr}" fill="{INK}"/>')


def _p(d, w=4, fill="none", color=INK):
    return (f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _sweat(x=40, y=-18):
    return (f'<path d="M {x} {y} Q {x + 9} {y + 14} {x} {y + 18} Q {x - 9} {y + 14} {x} {y} Z" '
            f'fill="{TEAR}" stroke="{INK}" stroke-width="2.5"/>')


def _heart(cx, cy, s=1.0, fill="#FF4F8B"):
    return (f'<path transform="translate({cx},{cy}) scale({s})" '
            f'd="M 0 6 C -12 -4 -8 -14 0 -8 C 8 -14 12 -4 0 6 Z" fill="{fill}" '
            f'stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')


def _star(cx, cy, r=10, fill="#FFD23F"):
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return (f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" '
            f'stroke-width="2.5" stroke-linejoin="round"/>')


FACES = {
    "neutral": ("calm", _dot_eyes() + _p("M -9 28 Q 0 33 9 28")),
    "happy": ("calm", _p("M -24 9 Q -15 -1 -6 9") + _p("M 6 9 Q 15 -1 24 9")
              + _p("M -12 25 Q 0 42 12 25 Z", fill=INK)),
    "laughing": ("idea", _p("M -24 2 L -14 8 L -24 13") + _p("M 24 2 L 14 8 L 24 13")
                 + _p("M -15 22 Q 0 50 15 22 Z", fill=INK)
                 + '<path d="M -7 36 Q 0 30 7 36 Q 0 44 -7 36 Z" fill="#FF7A8A"/>'
                 + f'<path d="M -34 14 q -4 8 0 12" fill="none" stroke="{TEAR}" stroke-width="3" stroke-linecap="round"/>'),
    "shocked": ("panic", _white_eyes() + f'<ellipse cx="0" cy="31" rx="6" ry="9" fill="{INK}"/>'),
    "scared": ("panic", _white_eyes(py=2, pr=2.5)
               + _p("M -26 -12 L -8 -6") + _p("M 26 -12 L 8 -6")
               + _p("M -12 32 Q -8 27 -4 32 Q 0 37 4 32 Q 8 27 12 32", w=3.5) + _sweat()),
    "sad": ("sad", _dot_eyes(y=8) + _p("M -24 -4 L -8 -9") + _p("M 24 -4 L 8 -9")
            + _p("M -9 32 Q 0 25 9 32")),
    "crying": ("sad", _p("M -24 6 Q -15 12 -6 6") + _p("M 6 6 Q 15 12 24 6")
               + _p("M -24 -6 L -8 -11") + _p("M 24 -6 L 8 -11")
               + _p("M -12 34 Q 0 22 12 34 Z", fill=INK)
               + f'<path d="M -18 10 L -20 40" stroke="{TEAR}" stroke-width="6" stroke-linecap="round"/>'
               + f'<path d="M 18 10 L 20 40" stroke="{TEAR}" stroke-width="6" stroke-linecap="round"/>'),
    "angry": ("panic", _dot_eyes(y=8) + _p("M -26 -8 L -7 0", w=5) + _p("M 26 -8 L 7 0", w=5)
              + f'<rect x="-12" y="24" width="24" height="10" rx="3" fill="#fff" stroke="{INK}" stroke-width="3.5"/>'
              + f'<line x1="-12" y1="29" x2="12" y2="29" stroke="{INK}" stroke-width="2.5"/>'),
    "smug": ("focus", _dot_eyes(y=8) + _p("M -23 4 L -7 4") + _p("M 7 4 L 23 4")
             + _p("M 8 -10 Q 15 -16 24 -12") + _p("M -6 30 Q 6 33 14 24")),
    "nervous": ("panic", _dot_eyes(r=3.8) + _p("M -24 -8 L -9 -12") + _p("M 24 -8 L 9 -12")
                + _p("M -12 30 L -6 27 L 0 30 L 6 27 L 12 30", w=3.5) + _sweat()),
    "crush": ("crush", _heart(-15, 6, 1.2) + _heart(15, 6, 1.2)
              + f'<ellipse cx="-29" cy="22" rx="9" ry="6" fill="{BLUSH}"/>'
              + f'<ellipse cx="29" cy="22" rx="9" ry="6" fill="{BLUSH}"/>'
              + _p("M -7 28 Q 0 33 7 28")),
    "confused": ("focus", f'<circle cx="-15" cy="7" r="4.5" fill="{INK}"/><circle cx="15" cy="6" r="6" fill="{INK}"/>'
                 + _p("M -24 -4 L -7 -4") + _p("M 7 -12 Q 15 -18 24 -10")
                 + _p("M -10 30 Q -5 25 0 30 Q 5 35 10 30", w=3.5)
                 + f'<text x="56" y="-28" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="900" fill="{INK}">?</text>'),
    "sleepy": ("calm", _p("M -23 8 L -7 8") + _p("M 7 8 L 23 8")
               + f'<ellipse cx="0" cy="30" rx="4" ry="5" fill="{INK}"/>'
               + f'<text x="46" y="-32" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="900" fill="{INK}">z</text>'
               + f'<text x="60" y="-50" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="900" fill="{INK}">Z</text>'),
    "determined": ("focus", _dot_eyes(y=8, r=5) + '<circle cx="-13" cy="6" r="1.6" fill="#fff"/><circle cx="17" cy="6" r="1.6" fill="#fff"/>'
                   + _p("M -25 -6 L -7 -1", w=5) + _p("M 25 -6 L 7 -1", w=5) + _p("M -9 30 L 9 30")),
    "disgusted": ("sad", _p("M -24 4 L -8 8 L -24 12") + _p("M 24 4 L 8 8 L 24 12")
                  + _p("M -24 -6 L -8 -2") + _p("M 24 -6 L 8 -2")
                  + _p("M -12 30 Q -6 26 0 30 Q 6 34 12 28")
                  + '<path d="M 4 31 Q 10 42 15 33" fill="#FF7A8A" stroke="#1F2A44" stroke-width="2.5"/>'),
    "thinking": ("idea", f'<circle cx="-12" cy="2" r="4.5" fill="{INK}"/><circle cx="18" cy="2" r="4.5" fill="{INK}"/>'
                 + _p("M 7 -12 Q 15 -17 24 -13") + _p("M -24 -9 L -8 -9") + _p("M 2 30 L 12 28")),
    "starstruck": ("idea", _star(-15, 6, 11) + _star(15, 6, 11) + _p("M -14 23 Q 0 44 14 23 Z", fill=INK)),
    "deadpan": ("calm", f'<path d="M -23 4 L -7 4 L -7 8 Q -15 13 -23 8 Z" fill="{INK}"/>'
                f'<path d="M 7 4 L 23 4 L 23 8 Q 15 13 7 8 Z" fill="{INK}"/>' + _p("M -8 30 L 8 30")),
}

FACE_ORDER = ["neutral", "happy", "laughing", "starstruck", "crush", "smug",
              "thinking", "determined", "confused", "deadpan", "sleepy", "nervous",
              "shocked", "scared", "sad", "crying", "angry", "disgusted"]


# --------------------------------------------------------------------------
# BODY
# --------------------------------------------------------------------------
def head(face="neutral", view="front", mood=None):
    """Head incl. headphones, front/three_quarter/side/back."""
    m = MOOD[mood or FACES[face][0]]
    out = []
    if view == "front":
        out.append(f'<rect x="-46" y="-40" width="92" height="84" rx="40" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>')
        out.append(f'<path d="M -48 -2 Q -48 -54 0 -54 Q 48 -54 48 -2" fill="none" stroke="{HEADPHONE}" stroke-width="9" stroke-linecap="round"/>')
        for x in (-58, 44):
            out.append(f'<rect x="{x}" y="-14" width="14" height="30" rx="7" fill="{HEADPHONE}" stroke="{INK}" stroke-width="5"/>')
            out.append(f'<circle cx="{x + 7}" cy="1" r="3.2" fill="{m}"/>')
        if face not in ("crush",):
            out.append(f'<circle cx="-28" cy="22" r="5" fill="{BLUSH}"/><circle cx="28" cy="22" r="5" fill="{BLUSH}"/>')
        out.append(FACES[face][1])
    elif view == "three_quarter":
        out.append(f'<rect x="40" y="-12" width="10" height="26" rx="5" fill="{HEADPHONE}" stroke="{INK}" stroke-width="5"/>')
        out.append(f'<rect x="-46" y="-40" width="90" height="84" rx="40" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>')
        out.append(f'<path d="M -50 -2 Q -50 -54 -6 -55 Q 36 -54 42 -8" fill="none" stroke="{HEADPHONE}" stroke-width="9" stroke-linecap="round"/>')
        out.append(f'<rect x="-60" y="-15" width="17" height="32" rx="8" fill="{HEADPHONE}" stroke="{INK}" stroke-width="5"/>')
        out.append(f'<circle cx="-51.5" cy="1" r="3.4" fill="{m}"/>')
        out.append(f'<circle cx="-14" cy="22" r="5" fill="{BLUSH}"/><circle cx="34" cy="21" r="4" fill="{BLUSH}"/>')
        out.append(f'<circle cx="-2" cy="6" r="4.5" fill="{INK}"/><circle cx="24" cy="6" r="4" fill="{INK}"/>')
        out.append(_p("M 3 28 Q 11 33 18 28"))
    elif view == "side":
        out.append(f'<rect x="-40" y="-40" width="80" height="84" rx="38" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>')
        out.append(f'<path d="M -6 -16 Q -7 -36 -6 -44" fill="none" stroke="{HEADPHONE}" stroke-width="12" stroke-linecap="round"/>')
        out.append(f'<rect x="-16" y="-16" width="20" height="34" rx="10" fill="{HEADPHONE}" stroke="{INK}" stroke-width="5"/>')
        out.append(f'<circle cx="-6" cy="1" r="3.6" fill="{m}"/>')
        out.append(f'<circle cx="24" cy="6" r="4.5" fill="{INK}"/>')
        out.append(f'<circle cx="20" cy="22" r="5" fill="{BLUSH}"/>')
        out.append(_p("M 26 29 Q 32 31 37 27"))
    elif view == "back":
        out.append(f'<rect x="-46" y="-40" width="92" height="84" rx="40" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>')
        out.append(f'<path d="M -48 -2 Q -48 -54 0 -54 Q 48 -54 48 -2" fill="none" stroke="{HEADPHONE}" stroke-width="9" stroke-linecap="round"/>')
        for x in (-58, 44):
            out.append(f'<rect x="{x}" y="-14" width="14" height="30" rx="7" fill="{HEADPHONE}" stroke="{INK}" stroke-width="5"/>')
    return "".join(out)


def torso(view="front"):
    if view == "side":
        return (f'<path d="M -14 48 L 14 48 Q 22 100 14 126 L -14 126 Q -20 100 -14 48 Z" '
                f'fill="{JACKET}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    zip_x = {"front": 0, "three_quarter": 8, "back": None}[view]
    s = (f'<path d="M -22 48 L 22 48 Q 30 100 18 126 L -18 126 Q -30 100 -22 48 Z" '
         f'fill="{JACKET}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    if zip_x is not None:
        s += f'<line x1="{zip_x}" y1="56" x2="{zip_x}" y2="126" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    else:
        s += f'<path d="M -16 52 Q 0 66 16 52" fill="none" stroke="{INK}" stroke-width="3"/>'
    return s


def hand(x, y):
    return f'<circle cx="{x}" cy="{y}" r="8" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>'


def shoe(x, y, rx=21, ry=10, rot=0):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{SHOE}" stroke="{INK}" '
            f'stroke-width="5" transform="rotate({rot} {x} {y})"/>')


# Poses: arms/legs as polylines (shoulder→elbow→hand / hip→knee→ankle).
# "front_arms" are drawn over the head (hand-to-face poses).
# shoes: (x, y, rot). lift: raises the whole body (jumps). extras: svg drawn behind/after.
IDLE_ARMS = [[(-24, 62), (-62, 96)], [(24, 62), (62, 96)]]
IDLE_LEGS = [[(-9, 124), (-12, 174)], [(9, 124), (12, 174)]]
IDLE_SHOES = [(-20, 184, 0), (20, 184, 0)]

POSES = {
    "idle": dict(face="neutral", arms=IDLE_ARMS, legs=IDLE_LEGS, shoes=IDLE_SHOES),
    "walk": dict(face="happy",
                 arms=[[(-24, 62), (-40, 84), (-46, 108)], [(24, 62), (48, 82), (66, 92)]],
                 legs=[[(-9, 124), (-16, 150), (-20, 174)], [(9, 124), (20, 146), (24, 166)]],
                 shoes=[(-28, 184, 0), (32, 174, -14)]),
    "run": dict(face="determined",
                arms=[[(-24, 62), (-54, 72), (-62, 46)], [(24, 62), (44, 92), (68, 102)]],
                legs=[[(-9, 124), (-30, 150), (-22, 176)], [(9, 124), (26, 144), (48, 152)]],
                shoes=[(-30, 186, 0), (58, 158, -30)],
                behind='<g stroke="#9AA5BE" stroke-width="5" stroke-linecap="round">'
                       '<line x1="-150" y1="40" x2="-95" y2="40"/><line x1="-160" y1="80" x2="-100" y2="80"/>'
                       '<line x1="-140" y1="120" x2="-95" y2="120"/></g>'),
    "wave": dict(face="happy",
                 arms=[IDLE_ARMS[0], [(24, 62), (52, 40), (60, 2)]],
                 legs=IDLE_LEGS, shoes=IDLE_SHOES,
                 after='<g stroke="#1F2A44" stroke-width="4" stroke-linecap="round" fill="none">'
                       '<path d="M 76 -14 q 8 6 6 16"/><path d="M 86 -26 q 12 10 10 26"/></g>'),
    "point": dict(face="determined",
                  arms=[IDLE_ARMS[0], [(24, 62), (60, 60), (98, 56)]],
                  legs=[[(-9, 124), (-18, 174)], [(9, 124), (18, 174)]],
                  shoes=[(-26, 184, 0), (28, 184, 0)]),
    "cheer": dict(face="starstruck", lift=-24,
                  arms=[[(-24, 62), (-50, 30), (-60, -8)], [(24, 62), (50, 30), (60, -8)]],
                  legs=[[(-9, 124), (-26, 146), (-16, 168)], [(9, 124), (26, 146), (16, 168)]],
                  shoes=[(-24, 178, 10), (24, 178, -10)],
                  ground='<ellipse cx="0" cy="196" rx="46" ry="7" fill="#1F2A44" opacity=".15"/>'),
    "panic": dict(face="scared",
                  arms=[[(-24, 62), (-58, 50), (-72, 16)], [(24, 62), (62, 42), (70, 8)]],
                  legs=[[(-9, 124), (-26, 174)], [(9, 124), (26, 174)]],
                  shoes=[(-34, 184, -8), (34, 184, 8)],
                  after='<g stroke="#1F2A44" stroke-width="4" stroke-linecap="round">'
                        '<line x1="-96" y1="-6" x2="-84" y2="4"/><line x1="-100" y1="20" x2="-86" y2="20"/>'
                        '<line x1="96" y1="-10" x2="84" y2="0"/><line x1="100" y1="16" x2="86" y2="16"/></g>'),
    "think": dict(face="thinking",
                  arms=[[(-24, 62), (-44, 92), (-8, 100)]],
                  front_arms=[[(24, 62), (52, 84), (22, 50)]],
                  legs=IDLE_LEGS, shoes=IDLE_SHOES),
    "shrug": dict(face="deadpan",
                  arms=[[(-24, 62), (-54, 82), (-70, 56)], [(24, 62), (54, 82), (70, 56)]],
                  legs=IDLE_LEGS, shoes=IDLE_SHOES),
    "cower": dict(face="scared",
                  arms=[], front_arms=[[(-24, 62), (-56, 62), (-44, 34)], [(24, 62), (56, 62), (44, 34)]],
                  legs=[[(-9, 124), (-2, 150), (-20, 174)], [(9, 124), (2, 150), (20, 174)]],
                  shoes=[(-26, 184, -10), (26, 184, 10)]),
    "sit": dict(face="sleepy", lift=24,
                arms=[[(-24, 62), (-46, 96), (-54, 128)], [(24, 62), (46, 96), (54, 128)]],
                legs=[[(-9, 124), (-54, 136), (-40, 160)], [(9, 124), (54, 136), (40, 160)]],
                shoes=[(-46, 168, -20), (46, 168, 20)],
                ground='<ellipse cx="0" cy="196" rx="80" ry="8" fill="#1F2A44" opacity=".15"/>'),
    "crush_shy": dict(face="crush",
                      arms=[[(-24, 62), (-30, 92), (-6, 112)], [(24, 62), (30, 92), (6, 112)]],
                      legs=[[(-9, 124), (-2, 174)], [(9, 124), (14, 168)]],
                      shoes=[(-8, 184, 0), (26, 178, -18)],
                      after='<g transform="translate(70,-60)">'
                            '<path d="M 0 6 C -12 -4 -8 -14 0 -8 C 8 -14 12 -4 0 6 Z" fill="#FF4F8B" stroke="#1F2A44" stroke-width="2.5"/></g>'
                            '<g transform="translate(90,-30) scale(.7)">'
                            '<path d="M 0 6 C -12 -4 -8 -14 0 -8 C 8 -14 12 -4 0 6 Z" fill="#FF4F8B" stroke="#1F2A44" stroke-width="2.5"/></g>'),
}

POSE_ORDER = ["idle", "walk", "run", "wave", "point", "cheer",
              "panic", "think", "shrug", "cower", "sit", "crush_shy"]


def body(pose="idle", face=None, mood=None):
    p = POSES[pose]
    face = face or p["face"]
    lift = p.get("lift", 0)
    out = [p.get("ground", ""), f'<g transform="translate(0,{lift})">', p.get("behind", "")]
    shoes = "".join(shoe(x, y, rot=r) for x, y, r in p["shoes"])
    for leg in p["legs"]:
        out.append(_pl(leg, 7))
    if not p.get("shoes_behind"):
        out.append(shoes)
    for arm in p["arms"]:
        out.append(_pl(arm, 7))
        out.append(hand(*arm[-1]))
    out.append(torso("front"))
    if p.get("shoes_behind"):
        out.append(shoes)
    out.append(head(face, "front", mood))
    for arm in p.get("front_arms", []):
        out.append(_pl(arm, 7))
        out.append(hand(*arm[-1]))
    out.append(p.get("after", ""))
    out.append("</g>")
    return "".join(out)


def turnaround(view):
    if view == "side":
        return ("".join([
            _pl([(-2, 124), (-2, 174)], 7), _pl([(4, 124), (6, 174)], 7),
            shoe(10, 184, rx=24), torso("side"),
            _pl([(0, 62), (6, 104)], 7), hand(6, 108),
            head(view="side"),
        ]))
    if view == "three_quarter":
        return "".join([
            _pl([(-6, 124), (-10, 174)], 7), _pl([(12, 124), (14, 172)], 7),
            shoe(-14, 184), shoe(22, 181, rx=18),
            _pl([(26, 62), (52, 94)], 7), hand(55, 98),
            torso("three_quarter"),
            _pl([(-22, 62), (-56, 98)], 7), hand(-59, 102),
            head(view="three_quarter"),
        ])
    if view == "back":
        return "".join([
            _pl(IDLE_LEGS[0], 7), _pl(IDLE_LEGS[1], 7),
            "".join(shoe(x, y) for x, y, _ in IDLE_SHOES),
            _pl(IDLE_ARMS[0], 7), hand(-66, 100), _pl(IDLE_ARMS[1], 7), hand(66, 100),
            torso("back"), head(view="back"),
        ])
    return body("idle")
