"""RAE — the crush. Geometry, faces and poses, in the same "Bo units" as bo.py.

Origin = centre of the head. Same head box as Bo (92 x 84, r 40), same 5 px ink
outline, same single-stroke limbs, no nose / fingers / neck.

Silhouette identifiers (readable at thumbnail size):
  * high ponytail with an ORANGE SCRUNCHIE (the series' "Rae colour")
  * oversized MINT hoodie: longer hem, thick sleeve strokes, kangaroo pocket
  * side-swept fringe, tiny eyelash flicks

Emotion meter: the PONYTAIL. up = alert/scared, neutral, droop = sad/tired.
It is cheap to animate (one rotation around the scrunchie) and does for Rae
what the headphone mood light does for Bo.
"""
import bo

INK = bo.INK
SKIN = bo.SKIN
BLUSH = bo.BLUSH
HAIR = "#5A3B2E"
HAIR_SHADE = "#47302A"
HOODIE = "#7FDDC0"
HOODIE_SHADE = "#5FC4A6"
SCRUNCHIE = "#FF9F43"
SHOE = "#FFFFFF"
TEAR = bo.TEAR

_p = bo._p
_pl = bo._pl

# ponytail rotation (degrees) around the scrunchie
TAIL = {"up": -22, "neutral": 0, "droop": 0}  # droop uses its own hanging shape


# --------------------------------------------------------------------------
# FACES
# --------------------------------------------------------------------------
def _lashes(y=4, dx=15):
    """Tiny outer-corner flick on each eye."""
    return _p(f"M {-dx - 5} {y - 1} L {-dx - 10} {y - 3}", w=3) + _p(f"M {dx + 5} {y - 1} L {dx + 10} {y - 3}", w=3)


def _dots(y=7, r=4.5, px=0):
    return (f'<circle cx="{-15 + px}" cy="{y}" r="{r}" fill="{INK}"/>'
            f'<circle cx="{15 + px}" cy="{y}" r="{r}" fill="{INK}"/>')


def _whites(py=0, px=0, pr=3.5):
    return (f'<circle cx="-15" cy="6" r="10" fill="#fff" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="15" cy="6" r="10" fill="#fff" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="{-15 + px}" cy="{6 + py}" r="{pr}" fill="{INK}"/>'
            f'<circle cx="{15 + px}" cy="{6 + py}" r="{pr}" fill="{INK}"/>')


# name: (ponytail state, svg)
FACES = {
    "neutral": ("neutral", _dots() + _lashes() + _p("M -8 29 Q 0 32 8 29")),
    "unimpressed": ("neutral", _dots(y=8) + _p("M -24 3 L -7 3", w=4.5) + _p("M 7 3 L 24 3", w=4.5)
                    + _p("M -9 30 L 7 30")),
    "smirk": ("neutral", _dots() + _lashes() + _p("M 7 -10 Q 15 -16 24 -11") + _p("M -24 -6 L -8 -6")
              + _p("M -6 30 Q 6 32 14 23")),
    "eyeroll": ("neutral", _whites(py=-5, px=3, pr=3.2) + _p("M -9 31 Q 0 28 9 31")),
    "happy": ("neutral", _p("M -24 9 Q -15 -1 -6 9") + _p("M 6 9 Q 15 -1 24 9") + _lashes(y=8)
              + _p("M -12 25 Q 0 40 12 25 Z", fill=INK)),
    "laughing": ("up", _p("M -24 2 L -14 8 L -24 13") + _p("M 24 2 L 14 8 L 24 13")
                 + _p("M -15 22 Q 0 48 15 22 Z", fill=INK)
                 + '<path d="M -7 35 Q 0 29 7 35 Q 0 43 -7 35 Z" fill="#FF7A8A"/>'),
    "determined": ("neutral", _dots(y=8, r=5) + _lashes(y=6) + _p("M -25 -6 L -7 -1", w=5) + _p("M 25 -6 L 7 -1", w=5)
                   + _p("M -8 30 L 8 30")),
    "thinking": ("neutral", _dots(y=3, px=4) + _lashes(y=1) + _p("M 7 -12 Q 15 -17 24 -13") + _p("M -24 -9 L -8 -9")
                 + _p("M 0 30 L 11 28")),
    "shocked": ("up", _whites() + _lashes(y=0, dx=19) + f'<ellipse cx="0" cy="31" rx="6" ry="8" fill="{INK}"/>'),
    "scared": ("up", _whites(py=2, pr=2.5) + _p("M -26 -12 L -8 -6") + _p("M 26 -12 L 8 -6")
               + _p("M -12 32 Q -8 27 -4 32 Q 0 37 4 32 Q 8 27 12 32", w=3.5) + bo._sweat(38, -14)),
    "sad": ("droop", _dots(y=9) + _lashes(y=7) + _p("M -24 -4 L -8 -9") + _p("M 24 -4 L 8 -9")
            + _p("M -9 32 Q 0 25 9 32")),
    "blush": ("neutral", _dots(y=8, r=4, px=9) + _lashes(y=6) + _p("M -2 30 Q 4 27 10 30 Q 15 33 19 29", w=3.5)
              + f'<ellipse cx="-28" cy="21" rx="10" ry="6" fill="{BLUSH}"/>'
              + f'<ellipse cx="29" cy="21" rx="10" ry="6" fill="{BLUSH}"/>'
              + _p("M -36 12 L -32 17", w=2.5) + _p("M -30 11 L -27 16", w=2.5)),
}

FACE_ORDER = ["neutral", "unimpressed", "smirk", "eyeroll", "happy", "laughing",
              "determined", "thinking", "blush", "shocked", "scared", "sad"]


# --------------------------------------------------------------------------
# HAIR
# --------------------------------------------------------------------------
def _ponytail(root_x, root_y, direction=1, state="neutral"):
    """A teardrop of hair rising from the scrunchie. direction=+1 sweeps right."""
    d = direction
    if state == "droop":
        # hangs down past the side of the head instead of rising
        tail = (f'<path d="M {-6 * d} 0 Q {54 * d} -20 {74 * d} 18 Q {86 * d} 52 {70 * d} 88 '
                f'Q {58 * d} 58 {46 * d} 34 Q {28 * d} 10 {8 * d} 6 Z" '
                f'fill="{HAIR}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<path d="M {14 * d} -2 Q {56 * d} 4 {68 * d} 50" fill="none" stroke="{HAIR_SHADE}" stroke-width="4" stroke-linecap="round"/>')
        return f'<g transform="translate({root_x},{root_y}) scale(.72)">{tail}</g>'
    rot = TAIL[state] * d
    tail = (f'<path d="M {-10 * d} 0 Q {-14 * d} -46 {22 * d} -62 Q {54 * d} -70 {62 * d} -44 '
            f'Q {40 * d} -54 {26 * d} -38 Q {14 * d} -22 {12 * d} 0 Z" '
            f'fill="{HAIR}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M {4 * d} -6 Q {4 * d} -36 {28 * d} -50" fill="none" stroke="{HAIR_SHADE}" stroke-width="4" stroke-linecap="round"/>')
    return (f'<g transform="translate({root_x},{root_y}) rotate({rot}) scale(.72)">{tail}</g>')


def _scrunchie(x, y, rot=0):
    bumps = "".join(f'<circle cx="{bx}" cy="{by}" r="5.5" fill="{SCRUNCHIE}" stroke="{INK}" stroke-width="3"/>'
                    for bx, by in [(-12, 1), (-4, -3), (4, -3), (12, 1)])
    return (f'<g transform="translate({x},{y}) rotate({rot})">'
            f'<rect x="-17" y="-6" width="34" height="13" rx="6.5" fill="{SCRUNCHIE}" stroke="{INK}" stroke-width="4"/>'
            f'{bumps}</g>')


def _hair_front():
    # cap over the top of the head + side-swept fringe (sweeps to Rae's left = screen right)
    cap = (f'<path d="M -49 12 Q -54 -52 0 -52 Q 54 -52 49 12 Q 46 -6 40 -14 '
           f'Q 22 -4 2 -12 Q -14 -20 -22 -8 Q -32 -2 -40 -12 Q -46 -4 -49 12 Z" '
           f'fill="{HAIR}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    strands = _p("M 16 -40 Q 24 -26 30 -12", w=3.5, color=HAIR_SHADE) + _p("M -14 -42 Q -22 -28 -30 -14", w=3.5, color=HAIR_SHADE)
    return cap + strands


# --------------------------------------------------------------------------
# HEAD
# --------------------------------------------------------------------------
def head(face="neutral", view="front", tail=None):
    state = tail or FACES[face][0]
    out = []
    if view == "front":
        out.append(_ponytail(14, -50, 1, state))
        out.append(f'<rect x="-46" y="-40" width="92" height="84" rx="40" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>')
        if face not in ("blush",):
            out.append(f'<circle cx="-28" cy="22" r="5" fill="{BLUSH}"/><circle cx="28" cy="22" r="5" fill="{BLUSH}"/>')
        out.append(FACES[face][1])
        out.append(_hair_front())
        out.append(_scrunchie(14, -50, 12))
    elif view == "three_quarter":
        out.append(_ponytail(-10, -48, -1, state))
        out.append(f'<rect x="-46" y="-40" width="90" height="84" rx="40" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>')
        out.append(f'<circle cx="-14" cy="22" r="5" fill="{BLUSH}"/><circle cx="34" cy="21" r="4" fill="{BLUSH}"/>')
        out.append(f'<circle cx="-2" cy="7" r="4.5" fill="{INK}"/><circle cx="24" cy="7" r="4" fill="{INK}"/>')
        out.append(_p("M -8 2 L -12 -3", w=3) + _p("M 29 2 L 33 -3", w=3))
        out.append(_p("M 3 29 Q 11 32 18 29"))
        out.append(f'<path d="M -49 14 Q -56 -52 -2 -53 Q 46 -52 45 6 Q 34 -12 18 -8 Q 2 -18 -12 -10 '
                   f'Q -26 -4 -32 -14 Q -42 -2 -49 14 Z" fill="{HAIR}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
        out.append(_scrunchie(-10, -50, -14))
    elif view == "side":
        out.append(_ponytail(-22, -42, -1, state))
        out.append(f'<rect x="-40" y="-40" width="80" height="84" rx="38" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>')
        out.append(f'<circle cx="24" cy="7" r="4.5" fill="{INK}"/>' + _p("M 29 2 L 33 -3", w=3))
        out.append(f'<circle cx="20" cy="22" r="5" fill="{BLUSH}"/>')
        out.append(_p("M 26 29 Q 32 31 37 27"))
        out.append(f'<path d="M -42 12 Q -48 -50 4 -50 Q 40 -50 42 -10 Q 30 -18 20 -10 Q 10 -20 -2 -16 '
                   f'Q -10 -8 -18 -4 Q -32 0 -42 12 Z" fill="{HAIR}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
        out.append(_scrunchie(-22, -44, -40))
    elif view == "back":
        out.append(f'<rect x="-46" y="-40" width="92" height="84" rx="40" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>')
        out.append(f'<path d="M -49 22 Q -54 -52 0 -52 Q 54 -52 49 22 Q 30 34 0 34 Q -30 34 -49 22 Z" '
                   f'fill="{HAIR}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
        out.append(_p("M 0 -30 Q -18 -8 -26 22", w=3.5, color=HAIR_SHADE) + _p("M 0 -30 Q 18 -8 26 22", w=3.5, color=HAIR_SHADE))
        out.append(_ponytail(0, -46, 1, state))
        out.append(_scrunchie(0, -46, 0))
    return "".join(out)


# --------------------------------------------------------------------------
# BODY
# --------------------------------------------------------------------------
HEM = 140


def hoodie(view="front"):
    if view == "side":
        return (f'<path d="M -20 46 L 18 46 Q 30 104 22 {HEM} L -22 {HEM} Q -30 104 -20 46 Z" '
                f'fill="{HOODIE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<path d="M -20 50 Q -34 48 -30 70 Q -24 60 -12 58" fill="{HOODIE_SHADE}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    s = (f'<path d="M -28 46 L 28 46 Q 42 104 32 {HEM} L -32 {HEM} Q -42 104 -28 46 Z" '
         f'fill="{HOODIE}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
         f'<line x1="-30" y1="{HEM - 9}" x2="30" y2="{HEM - 9}" stroke="{INK}" stroke-width="3"/>')
    if view == "back":
        s += (f'<path d="M -26 46 Q -30 82 0 88 Q 30 82 26 46 Z" fill="{HOODIE_SHADE}" stroke="{INK}" '
              f'stroke-width="4" stroke-linejoin="round"/>')
        return s
    cx = 0 if view == "front" else 8
    # hood rim + drawstrings + kangaroo pocket
    s += (f'<path d="M {cx - 24} 46 Q {cx} 62 {cx + 24} 46" fill="{HOODIE_SHADE}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
          f'<line x1="{cx - 6}" y1="56" x2="{cx - 8}" y2="80" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
          f'<line x1="{cx + 6}" y1="56" x2="{cx + 8}" y2="80" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
          f'<path d="M {cx - 20} 126 L {cx - 14} 104 L {cx + 14} 104 L {cx + 20} 126" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')
    return s


def sleeve(points):
    """Oversized sleeve: thick mint stroke with ink outline, cuff, then hand."""
    d = " ".join(f"{x},{y}" for x, y in points)
    hx, hy = points[-1]
    px, py = points[-2]
    # stop the sleeve a little before the hand
    t = 0.78
    cx, cy = px + (hx - px) * t, py + (hy - py) * t
    d_sleeve = " ".join(f"{x},{y}" for x, y in points[:-1]) + f" {cx:.1f},{cy:.1f}"
    return (f'<polyline points="{d}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<polyline points="{d_sleeve}" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<polyline points="{d_sleeve}" fill="none" stroke="{HOODIE}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{hx}" cy="{hy}" r="8" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>')


def shoe(x, y, rot=0, rx=20, ry=10):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{SHOE}" stroke="{INK}" stroke-width="5" '
            f'transform="rotate({rot} {x} {y})"/>'
            f'<line x1="{x - 8}" y1="{y - 4}" x2="{x + 8}" y2="{y - 4}" stroke="{SCRUNCHIE}" stroke-width="3" '
            f'stroke-linecap="round" transform="rotate({rot} {x} {y})"/>')


IDLE_ARMS = [[(-28, 62), (-56, 100), (-60, 118)], [(28, 62), (56, 100), (60, 118)]]
IDLE_LEGS = [[(-10, HEM - 4), (-12, 174)], [(10, HEM - 4), (12, 174)]]
IDLE_SHOES = [(-19, 184, 0), (19, 184, 0)]

_FLASH = ('<g transform="translate(96,70) rotate(-6)">'
          '<path d="M 14 -6 L 150 -46 L 150 46 L 14 6 Z" fill="#FFF3B0" opacity=".55"/>'
          f'<rect x="-14" y="-7" width="30" height="14" rx="4" fill="#4A5675" stroke="{INK}" stroke-width="4"/>'
          f'<rect x="14" y="-10" width="8" height="20" rx="2" fill="#FFD23F" stroke="{INK}" stroke-width="3.5"/></g>')

POSES = {
    "idle": dict(face="neutral", arms=IDLE_ARMS, legs=IDLE_LEGS, shoes=IDLE_SHOES),
    # signature pose (EP01 shot 1.2: "sits on a desk, arms crossed")
    "arms_crossed": dict(face="unimpressed", arms=[],
                         front_arms=[[(-28, 62), (-20, 96), (24, 86)], [(28, 62), (18, 100), (-22, 92)]],
                         legs=[[(-10, HEM - 4), (-8, 174)], [(10, HEM - 4), (20, 172)]],
                         shoes=[(-14, 184, 0), (28, 182, -8)]),
    "walk": dict(face="neutral",
                 arms=[[(-28, 62), (-44, 92), (-46, 116)], [(28, 62), (50, 90), (66, 104)]],
                 legs=[[(-10, HEM - 4), (-18, 156), (-22, 174)], [(10, HEM - 4), (22, 154), (26, 168)]],
                 shoes=[(-28, 184, 0), (34, 177, -14)]),
    "point": dict(face="determined",
                  arms=[IDLE_ARMS[0], [(28, 62), (64, 62), (100, 56)]],
                  legs=[[(-10, HEM - 4), (-18, 174)], [(10, HEM - 4), (18, 174)]],
                  shoes=[(-26, 184, 0), (26, 184, 0)]),
    "shrug": dict(face="eyeroll",
                  arms=[[(-28, 62), (-58, 88), (-74, 62)], [(28, 62), (58, 88), (74, 62)]],
                  legs=IDLE_LEGS, shoes=IDLE_SHOES),
    # EP01 shot 4.14: the flashlight catches Bo stealing chocolate
    "flashlight": dict(face="smirk",
                       arms=[IDLE_ARMS[0], [(28, 62), (60, 78), (92, 72)]],
                       legs=[[(-10, HEM - 4), (-16, 174)], [(10, HEM - 4), (16, 174)]],
                       shoes=[(-24, 184, 0), (24, 184, 0)], after=_FLASH),
    # EP01 shot 8.2: copies Bo's "tap-tap" on the side of her head
    "head_tap": dict(face="smirk",
                     arms=[IDLE_ARMS[0]],
                     front_arms=[[(28, 62), (70, 44), (54, 10)]],
                     legs=[[(-10, HEM - 4), (-14, 174)], [(10, HEM - 4), (16, 172)]],
                     shoes=[(-22, 184, 0), (24, 182, -6)],
                     after=f'<g stroke="{INK}" stroke-width="4" stroke-linecap="round" fill="none">'
                           '<path d="M 74 -6 q 8 6 6 16"/><path d="M 84 -18 q 12 10 10 26"/></g>'),
    # afraid of the dark: knees up, arms around them
    # afraid of the dark: hoodie pulled over the knees, arms wrapped around them
    "hug_knees": dict(face="scared", lift=40, shoes_front=True,
                      arms=[],
                      front_arms=[[(-28, 62), (-46, 98), (-6, 112)], [(28, 62), (46, 98), (6, 112)]],
                      legs=[[(-10, HEM - 6), (-14, 146)], [(10, HEM - 6), (14, 146)]],
                      shoes=[(-17, 148, 0), (17, 148, 0)],
                      ground='<ellipse cx="0" cy="194" rx="60" ry="8" fill="#1F2A44" opacity=".15"/>'),
}

POSE_ORDER = ["idle", "arms_crossed", "walk", "point", "shrug", "flashlight", "head_tap", "hug_knees"]


def body(pose="idle", face=None, tail=None):
    p = POSES[pose]
    face = face or p["face"]
    lift = p.get("lift", 0)
    out = [p.get("ground", ""), f'<g transform="translate(0,{lift})">', p.get("behind", "")]
    legs = "".join(_pl(leg, 7) for leg in p["legs"])
    shoes = "".join(shoe(x, y, r) for x, y, r in p["shoes"])
    out.append(legs)
    if not p.get("shoes_front"):
        out.append(shoes)
    for arm in p["arms"]:
        out.append(sleeve(arm))
    out.append(hoodie("front"))
    if p.get("shoes_front"):
        out.append(shoes)
    out.append(head(face, "front", tail))
    for arm in p.get("front_arms", []):
        out.append(sleeve(arm))
    out.append(p.get("after", ""))
    out.append("</g>")
    return "".join(out)


def turnaround(view):
    if view == "front":
        return body("idle")
    if view == "side":
        return "".join([
            _pl([(-2, HEM - 4), (-2, 174)], 7), _pl([(4, HEM - 4), (6, 174)], 7),
            shoe(10, 184, rx=23), hoodie("side"),
            sleeve([(0, 62), (4, 98), (6, 116)]),
            head(view="side"),
        ])
    if view == "three_quarter":
        return "".join([
            _pl([(-6, HEM - 4), (-10, 174)], 7), _pl([(12, HEM - 4), (14, 172)], 7),
            shoe(-14, 184), shoe(22, 181, rx=17),
            sleeve([(28, 62), (50, 98), (52, 116)]),
            hoodie("three_quarter"),
            sleeve([(-26, 62), (-52, 100), (-56, 118)]),
            head(view="three_quarter"),
        ])
    # back
    return "".join([
        _pl(IDLE_LEGS[0], 7), _pl(IDLE_LEGS[1], 7),
        "".join(shoe(x, y, r) for x, y, r in IDLE_SHOES),
        sleeve(IDLE_ARMS[0]), sleeve(IDLE_ARMS[1]),
        hoodie("back"), head(view="back"),
    ])
