"""EP01 animatic shot list: machine-readable version of ../STORYBOARD.md (58 shots).

Build:  python3 tools/animatic.py episodes/EP01_POV_Snowed_In_With_Your_Crush/animatic/shots.py
Keys are documented in tools/animatic.py. Timecodes (tc) are the storyboard's;
a shot only runs longer if its scratch VO overflows.
"""
import ep01_sets as S
import rae as _rae

SLUG = "EP01"
END_TC = "12:00"

INK = "#1F2A44"


# ---------------------------------------------------------------- helpers
def B(pose="idle", face=None, mood=None, x=760, s=1.7, **kw):
    return dict(who="bo", pose=pose, face=face, mood=mood, x=x, s=s, **kw)


def R(pose="idle", face=None, tail=None, x=1160, s=1.7, **kw):
    return dict(who="rae", pose=pose, face=face, tail=tail, x=x, s=s, **kw)


def BH(face="neutral", mood=None, x=960, y=560, s=5.0, **kw):
    return dict(who="bo", head=True, face=face, mood=mood, x=x, y=y, s=s, **kw)


def RH(face="neutral", tail=None, x=960, y=600, s=5.0, **kw):
    return dict(who="rae", head=True, face=face, tail=tail, x=x, y=y, s=s, **kw)


def push(z1=1.15, cx=960, cy=540, z0=1.0, cx1=None, cy1=None):
    return dict(z0=z0, z1=z1, cx0=cx, cy0=cy, cx1=cx1, cy1=cy1)


def pan(x0, x1, z=1.15, cy=540):
    return dict(z0=z, z1=z, cx0=x0, cx1=x1, cy0=cy, cy1=cy)


SCRUNCHIE_BAND = _rae._scrunchie(0, -54, 0)

HEADPHONES = ('<path d="M -170 40 Q -170 -170 0 -170 Q 170 -170 170 40" fill="none" stroke="#FFC83D" stroke-width="34" stroke-linecap="round"/>'
              f'<rect x="-215" y="-10" width="70" height="120" rx="34" fill="#FFC83D" stroke="{INK}" stroke-width="12"/>'
              f'<rect x="145" y="-10" width="70" height="120" rx="34" fill="#FFC83D" stroke="{INK}" stroke-width="12"/>')
CABLE_CUT = (f'<path d="M -180 110 Q -200 260 -60 300" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
             f'<path d="M 30 300 Q 160 330 260 300" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
             '<g transform="translate(-10,300) rotate(-20)">'
             f'<circle cx="-40" cy="60" r="28" fill="none" stroke="#C0392B" stroke-width="12"/>'
             f'<circle cx="40" cy="60" r="28" fill="none" stroke="#C0392B" stroke-width="12"/>'
             '<path d="M -24 36 L 30 -60 M 24 36 L -30 -60" stroke="#9AA3B0" stroke-width="14" stroke-linecap="round"/></g>')
SPLICE = (f'<path d="M -320 0 Q -100 -60 100 0" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
          '<rect x="-40" y="-38" width="90" height="36" rx="6" fill="#E9EEF5" transform="rotate(-8)"/>'
          '<path d="M -10 -30 l 18 -10 M 10 -26 l 18 -10" stroke="#FF4D4D" stroke-width="6"/>')
BIN = (f'<path d="M -50 0 L -60 -120 L 60 -120 L 50 0 Z" fill="#5C6779"/>'
       '<rect x="-68" y="-136" width="136" height="20" rx="6" fill="#4A5465"/>')
WRAPPERS = '<rect x="-30" y="-150" width="22" height="14" rx="3" fill="#FB8500"/><rect x="0" y="-160" width="22" height="14" rx="3" fill="#8ECAE6"/><rect x="18" y="-146" width="22" height="14" rx="3" fill="#E76F51"/>'
RULER = '<rect x="-180" y="-12" width="360" height="24" rx="4" fill="#F2CC8F" stroke="#1F2A44" stroke-width="5"/>' + "".join(
    f'<line x1="{-170 + i * 20}" y1="-12" x2="{-170 + i * 20}" y2="{-2 if i % 5 else 4}" stroke="#1F2A44" stroke-width="3"/>' for i in range(18))

DARK = 0.0

SHOTS = [
    # ======================================================== B1 HOOK
    dict(id="1.1", tc="0:00", bg="BG04", counter="DAY 1", cam=push(1.18, 960, 470), music="none",
         vo=[("NARR", "Day one. You are snowed in at school.")], sfx=[("wind", 0)]),
    dict(id="1.2", tc="0:05", bg="BG03N", music="comedy",
         cast=[R("arms_crossed", "unimpressed", x=1350, s=1.5), B("idle", "nervous", "panic", x=700, s=2.6)],
         cam=push(1.06, 900, 520), vo=[("NARR", "The good news: you're not alone.")]),
    dict(id="1.3", tc="0:09", bg="BG03N", cast=[RH("unimpressed")], music="keep",
         vo=[("RAE", "This is your fault."), ("NARR", "The bad news: it's your crush. And she is not thrilled.")],
         panels=[dict(at=0.32, cast=[BH("crush", "crush")])], sfx=[("blip", 1.9)]),
    dict(id="1.4", tc="0:14", bg="BG03N", card="7 DAYS", music="none",
         cast=[B("panic", "shocked", "panic", x=760), R("arms_crossed", "eyeroll", x=1180)],
         cam=dict(shake=10), sfx=[("beach", 0.1), ("scratch", 2.6)],
         panels=[dict(at=0.68, cast=[B("idle", "deadpan", "panic", x=760), R("arms_crossed", "unimpressed", x=1180)])]),
    dict(id="1.5", tc="0:18", bg="BG03", title="BO &amp; YOU", music="none", sfx=[("logo", 0)]),

    # ======================================================== B2 HOW YOU GOT HERE
    dict(id="2.1", tc="0:20", bg="BG02", counter="FRI 2:45 PM", music="comedy", cam=pan(760, 1160, 1.12),
         cast=[B("walk", "confused", "focus", x=960)], sfx=[("chime", 0.1)],
         vo=[("NARR", "Friday. Two forty-five. Buses leave at three. You forgot your charger. Of course you did.")]),
    dict(id="2.2", tc="0:28", bg="BG03", music="keep", cam=push(1.08, 980, 520),
         cast=[R("idle", "determined", x=1200), B("crush_shy", "nervous", "crush", x=760)],
         vo=[("NARR", "She stayed late too. To finish a project. Different kind of problem.")]),
    dict(id="2.3", tc="0:35", bg=("BG12", dict(outside="storm", fill=0.08, night=False)), music="keep",
         sfx=[("wind", 0)], vo=[("NARR", "The forecast said, light flurries. The forecast lied.")],
         panels=[dict(at=0.33, bg=("BG12", dict(outside="storm", fill=0.45))),
                 dict(at=0.66, bg=("BG12", dict(outside="storm", fill=0.9)))]),
    dict(id="2.4", tc="0:42", bg="BG02", music="tense", cam=push(1.1),
         cast=[B("panic", "scared", "panic", x=760), R("idle", "shocked", x=1160)],
         panels=[dict(at=0.28, bg=("BG14", dict(vending=False))),
                 dict(at=0.6, bg=("BG14", dict(vending=False)), card="NO SIGNAL", dark=0.25)],
         sfx=[("electric", 2.0)],
         vo=[("NARR", "By four, the power's out. By five, the cell tower's down. By six, you realize everyone thinks you went home.")]),
    dict(id="2.5", tc="0:55", bg=("BG14", dict(vending=False)), cast=[BH("determined", "idea")], music="comedy",
         cam=push(1.08, 960, 560), sfx=[("tap", 0.3)], vo_at=1.7, vo=[("BO", "Okay. I have a plan.")]),
    dict(id="2.6", tc="1:00", bg="BG11", music="none",
         cast=[B("point", "determined", "focus", x=900, s=2.0)],
         panels=[dict(at=0.45, cast=[B("sit", "deadpan", "calm", x=900, s=2.0)])],
         sfx=[("thud", 4.4)], vo_at=5.0, vo=[("NARR", "It was not a good plan.")]),

    # ======================================================== B3 RULES
    dict(id="3.1", tc="1:10", bg="BG11", card="RULE 1", music="tense", sfx=[("whoosh", 0)],
         panels=[dict(at=0.35, bg=("BG12", dict(outside="storm", fill=1.0))),
                 dict(at=0.7, bg=("BG09", dict(with_fort=False)))],
         vo=[("NARR", "Rule one: there's no way out. Every door is under six feet of snow.")]),
    dict(id="3.2", tc="1:22", bg="BG14", card="RULE 2", music="keep", cam=push(1.45, 1180, 600, cx1=1480, cy1=560),
         cast=[B("cheer", "starstruck", "idea", x=760)], sfx=[("whoosh", 0), ("ticks", 3.0)],
         panels=[dict(at=0.45, card=("37", 1500, 300, 170))],
         vo=[("NARR", "Rule two: one vending machine. Thirty-seven snacks. That's the menu.")]),
    dict(id="3.3", tc="1:34", bg="GFX_MAP", card="RULE 3", music="none", cam=push(1.3, 960, 540, cx1=1420, cy1=720),
         sfx=[("whoosh", 0), ("lowhit", 4.0)],
         vo=[("NARR", "Rule three: nobody knows you're here. If you want to be found, you'll have to tell someone.")]),

    # ======================================================== B4 DAYS 1-3 BODY
    dict(id="4.1", tc="1:50", bg=("BG14", dict(vending=False)), counter="DAY 1", music="tense", sfx=[("wind", 0)],
         cast=[B("cower", "nervous", "panic", x=780), R("arms_crossed", "scared", x=1140)], cam=push(1.08),
         vo=[("NARR", "The first thing that tries to take you out isn't hunger. It's cold.")]),
    dict(id="4.2", tc="1:56", bg=("GFX_THREES", dict(highlight=0)), music="keep", sfx=[("ticks", 0.2)],
         panels=[dict(at=0.32, bg=("GFX_THREES", dict(highlight=1))), dict(at=0.52, bg=("GFX_THREES", dict(highlight=2))),
                 dict(at=0.72, bg=("GFX_THREES", dict(highlight=3)))],
         vo=[("NARR", "Survival experts have a rule of threes. Three minutes without air. Three hours without shelter in brutal cold. Three days without water. Three weeks without food.")]),
    dict(id="4.3", tc="2:10", bg=("BG09", dict(with_fort=False)), music="comedy", sfx=[("whoosh", 4.5)],
         cast=[B("walk", "determined", "focus", x=560), R("point", "determined", x=1380)],
         panels=[dict(at=0.45, bg="BG09", cast=[B("cheer", "starstruck", "idea", x=420), R("arms_crossed", "smirk", x=1500)])],
         vo=[("NARR", "So: shelter. You build a fort. Gym mats for walls. Encyclopedias for insulation.")]),
    dict(id="4.4", tc="2:22", bg="GFX_BULBS", music="heart", sfx=[("blip", 3.4)], cam=push(1.06),
         vo=[("NARR", "Your body gives off about a hundred watts of heat. Roughly an old light bulb. Two people in a small fort? Two light bulbs. It helps.")]),
    dict(id="4.5", tc="2:35", bg="BG09I", music="keep", cam=push(1.06, 960, 560),
         cast=[B("sit", "happy", "calm", x=720, s=2.2), R("hug_knees", "sad", "droop", x=1220, s=2.2)],
         vo=[("RAE", "Can you... leave your light on?"),
             ("NARR", "Turns out she's afraid of the dark. Turns out your headphones make a decent nightlight.")]),
    dict(id="4.6", tc="2:44", bg="BG09I", cast=[BH("nervous", "crush")], music="keep",
         panels=[dict(at=0.42, cast=[BH("nervous", "calm")])], sfx=[("blip", 0.3), ("blip", 0.6), ("blip", 3.2)],
         vo_at=1.2, vo=[("RAE", "Why'd it go pink?"), ("BO", "...Low battery.")]),
    dict(id="4.7", tc="2:52", bg=("BG12", dict(outside="storm", fill=0.7)), counter="DAY 2", music="none",
         cast=[R("point", "neutral", x=1250, s=1.5, y=None), B("panic", "shocked", "panic", x=560, s=1.5)],
         vo=[("NARR", "Day two. You're thirsty. There's snow everywhere."), ("BO", "Don't!"), ("NARR", "Do not eat the snow.")]),
    dict(id="4.8", tc="3:00", bg="GFX_SNOW", music="none", sfx=[("bwomp", 3.5)], cam=push(1.05),
         vo=[("NARR", "Your body has to spend its own heat to melt it. You'd trade being thirsty for being colder.")]),
    dict(id="4.9", tc="3:10", bg="BG09I", music="comedy",
         cast=[B("idle", "determined", "focus", x=700, s=2.2), R("idle", "determined", x=1220, s=2.2)],
         props_front=[(S.water_bottle(0, 0, 1.4), 860, 990), (S.water_bottle(0, 0, 1.4), 1060, 990)],
         vo=[("NARR", "Melt it first. Bottles inside your jacket. Slow, but it works.")]),
    dict(id="4.10", tc="3:18", bg="BG09I", music="keep", cam=dict(shake=4),
         cast=[B("cower", "deadpan", "crush", x=720, s=2.2), R("idle", "laughing", x=1220, s=2.2)],
         props_front=[(S.water_bottle(0, 0, 1.0, False), 670, 760), (S.water_bottle(0, 0, 1.0, False), 760, 770)],
         vo=[("NARR", "Is it comfortable? No. Did she laugh for the first time? Yes. Worth it.")]),
    dict(id="4.11", tc="3:28", bg=("MATH", dict(step=1)), counter="DAY 3", music="keep", sfx=[("chalk", 0.5)],
         cast=[R("point", "thinking", x=1650, s=1.5), B("think", "thinking", "focus", x=260, s=1.5)],
         vo=[("NARR", "Day three. Math class. But the math is your life.")]),
    dict(id="4.12", tc="3:38", bg=("MATH", dict(step=2)), music="none", cam=push(1.35, 960, 420),
         cast=[B("idle", "shocked", "panic", x=260, s=1.5), R("idle", "unimpressed", x=1650, s=1.5)], sfx=[("chalk", 0.3)],
         panels=[dict(at=0.6, card="2 DAYS")],
         vo=[("NARR", "A teenager needs around two thousand calories a day. Thirty-seven snacks is about nine thousand. For two people? Two days. Maybe three, if nobody eats the gummy worms.")]),
    dict(id="4.13", tc="3:58", bg="BG09I", music="comedy", cam=push(1.5, 960, 760),
         cast=[R("idle", "determined", x=960, s=2.2)],
         props_front=[(S.granola(0, 0, 2.0, True), 880, 860), (S.granola(0, 0, 2.0, True), 1040, 860), (RULER, 960, 880, 1.2)],
         vo=[("NARR", "So you ration. Half a granola bar each. Measured. With a ruler.")]),
    dict(id="4.14", tc="4:08", bg="BG14", music="none", sfx=[("heist", 0.2)],
         cast=[B("cower", "nervous", "panic", x=1250), R("flashlight", "smirk", x=520, s=1.7)],
         props_front=[(S.chocolate(0, 0, 1.0), 1250, 720)],
         panels=[dict(at=0.4, cam=None)],
         vo_at=3.0, vo=[("RAE", "Seriously?"), ("BO", "This felt like an emergency.")]),
    dict(id="4.15", tc="4:25", bg=("GFX_FUEL", dict(level=0.85)), music="tense",
         panels=[dict(at=0.45, bg=("GFX_FUEL", dict(level=0.25)))],
         vo=[("NARR", "And the cold makes it worse. Every shiver is your body burning fuel to stay warm.")]),
    dict(id="4.16", tc="4:38", bg="BG09", music="heart", cam=push(1.5, 960, 760),
         cast=[B("sit", "sleepy", "calm", x=900, s=0.9), R("hug_knees", "sleepy", x=1020, s=0.9)]),

    # ======================================================== B5 DAY 4 MIDPOINT
    dict(id="5.1", tc="5:00", bg="BG13", counter="DAY 4", music="comedy", cam=pan(600, 980, 1.25, 520),
         cast=[B("cheer", "starstruck", "idea", x=380)], sfx=[("chime", 0.4)],
         vo=[("NARR", "Day four. You find Mister Pickett's emergency shelf. A hand-crank radio. A walkie-talkie. And a note that says: Do not touch. Yes, you.")]),
    dict(id="5.2", tc="5:12", bg="BG09I", music="none", sfx=[("crank", 0), ("static", 1.0)],
         cast=[R("idle", "sad", "droop", x=1100, s=2.2), B("idle", "sad", "sad", x=600, s=2.2)],
         props_front=[(S.crank_radio(1.5), 1100, 900)],
         vo=[("RADIO", "...roads closed for at least three more days..."), ("NARR", "The radio works. The news doesn't help.")]),
    dict(id="5.3", tc="5:22", bg="BG09I", music="none", card="NO CABLE",
         cast=[B("shrug", "deadpan", "calm", x=960, s=2.4)], props_front=[(S.crank_radio(1.2), 1420, 960), (S.walkie(False, 1.2), 1650, 960)],
         sfx=[("trombone", 9.6)],
         vo=[("NARR", "The radio can charge things. You just need a cable. Like the one you came back for. Which you still don't have.")]),
    dict(id="5.4", tc="5:35", bg=("BG14", dict(count=15, tally=15)), music="none", cam=push(1.5, 1100, 600, cx1=1460, cy1=560),
         cast=[B("think", "confused", "focus", x=760)],
         panels=[dict(at=0.5, bg=("BG14", dict(count=12, tally=15)), card=("15 → 12", 1460, 260, 120))],
         sfx=[("lowhit", 4.6)],
         vo=[("NARR", "Then the math breaks. You left fifteen snacks last night. There are twelve.")]),
    dict(id="5.5", tc="5:45", bg="BG14", music="tense", cast=[RH("determined", "up")],
         panels=[dict(at=0.3, cast=[BH("nervous", "panic")])],
         vo=[("RAE", "Three snacks don't just disappear, Bo."), ("BO", "I didn't—"),
             ("NARR", "You didn't take them. But you did take the emergency chocolate. So.")]),

    # ======================================================== B6 DAY 5 LOW POINT (letterbox)
    dict(id="6.1", tc="6:00", bg=("BG10", dict(mats=False)), counter="DAY 5", letterbox=True, music="tense", cam=pan(700, 1100, 1.1),
         cast=[R("walk", "sad", "droop", x=960)], props=[(S.gym_mat(0, 0, 300, 44), 760, 930)],
         vo=[("NARR", "Day five. She moves to the gym. Alone. In the dark.")]),
    dict(id="6.2", tc="6:12", bg="BG09I", letterbox=True, music="keep", cam=push(1.1),
         cast=[B("sit", "sad", "sad", x=960, s=2.4)],
         vo=[("NARR", "You tell yourself it's fine. Your headphones disagree.")]),
    dict(id="6.3", tc="6:22", bg="GFX_BRAIN", letterbox=True, music="keep", cam=push(1.08),
         vo=[("NARR", "Here's the scary part about cold. It doesn't just hurt. Even mild hypothermia slows your brain. People make worse choices, and don't notice.")]),
    dict(id="6.4", tc="6:40", bg=("FIELD", dict(show_figure=True)), letterbox=True, music="none", sfx=[("wind", 0), ("wind", 5)],
         cast=[dict(who="bo", view="back", x=520, s=3.0, y=860)], cam=push(1.25, 1100, 600)),
    dict(id="6.5", tc="6:50", bg=("FIELD", dict(show_figure=False, footprints=True)), letterbox=True, music="none",
         cast=[B("panic", "shocked", "panic", x=420, s=2.4)], sfx=[("lowhit", 0.2), ("wind", 1)],
         vo=[("NARR", "You blink. It's gone. The footprints aren't. They start in the middle of the field. From nowhere.")]),
    dict(id="6.6", tc="7:05", bg=("BG10", dict(mats=True)), letterbox=True, music="none",
         cast=[B("run", "scared", "panic", x=520), R("idle", "sleepy", x=1060, s=1.5, rot=-90, y=870)],
         vo=[("NARR", "You run to tell her. She's stopped shivering. That should be good news. It isn't.")]),
    dict(id="6.7", tc="7:20", bg="GFX_TEMP", letterbox=True, music="none", sfx=[("heartbeat", 0), ("heartbeat", 4), ("heartbeat", 8)],
         vo=[("NARR", "When your body gets cold enough, it can stop shivering. Not because it's warm. Because it's running out.")]),
    dict(id="6.8", tc="7:35", bg="BG09I", letterbox=True, music="heart",
         cast=[R("idle", "sleepy", x=1180, s=1.9, rot=-90, y=820, wrapped=True), B("sit", "determined", "focus", x=640, s=2.2, shirt="#F4F4F4")],
         vo=[("NARR", "You do what you learned on day one. The fort. Body heat. Warm her chest first, not her hands.")]),
    dict(id="6.9", tc="7:55", bg="BG09I", letterbox=True, music="keep", cam=push(1.12, 760, 560),
         cast=[R("idle", "sleepy", x=1180, s=1.9, rot=-90, y=820, wrapped=True), B("sit", "crying", "sad", x=640, s=2.2, shirt="#F4F4F4")]),
    dict(id="6.10", tc="8:10", bg="BG09I", letterbox=True, music="keep", cast=[RH("sleepy", "droop")],
         panels=[dict(at=0.4, cast=[BH("sad", "sad", shirt="#F4F4F4")])],
         vo_at=1.0, vo=[("RAE", "...Your plans are terrible."), ("PAUSE", "1.2"), ("BO", "I know.")]),

    # ======================================================== B7 DAYS 6-7 SELF
    dict(id="7.1", tc="8:30", bg="BG09I", counter="DAY 6", letterbox=True, music="tense",
         cast=[B("think", "thinking", "focus", x=960, s=2.0, shirt="#F4F4F4")],
         props_front=[(S.walkie(False, 1.1), 600, 1000), (S.crank_radio(1.1), 1320, 1000)],
         vo=[("NARR", "Day six. She needs a doctor. Rule three: nobody knows you're here. Unless you tell them.")]),
    dict(id="7.2", tc="8:42", bg="BG09I", letterbox=True, music="none", cast=[BH("determined", "focus", shirt="#F4F4F4")],
         sfx=[("tap", 0.2)], vo_at=1.4,
         panels=[dict(at=0.36, cast=[RH("sleepy", "droop")]), dict(at=0.62, cast=[BH("smug", "focus")])],
         vo=[("BO", "Okay. I have a plan."), ("RAE", "Your plans are terrible."), ("BO", "Yeah. This one's worse.")]),
    dict(id="7.3", tc="8:52", bg="BG09I", letterbox=True, music="swell", cast=[BH("determined", "focus")], sfx=[("tap", 0.5)],
         panels=[dict(at=0.18, cast=[], props_front=[(HEADPHONES, 960, 470), (CABLE_CUT, 960, 470)]),
                 dict(at=0.42, cast=[], props_front=[(S.crank_radio(2.0), 1240, 820), (S.walkie(False, 1.8), 600, 820), (SPLICE, 1000, 760, 1.2)]),
                 dict(at=0.68, cast=[BH("determined", "focus")]),
                 dict(at=0.8, cast=[BH("determined", "off")])]),
    dict(id="7.4", tc="9:27", bg="BG09I", letterbox=True, music="keep", cam=push(1.25, 960, 720),
         cast=[B("idle", "determined", "off", x=620, s=2.0, shirt="#F4F4F4"), R("idle", "determined", x=1300, s=2.0, wrapped=True)],
         props_front=[(S.crank_radio(1.8), 960, 980)], sfx=[("crank", 0), ("crank", 3), ("crank", 6), ("crank", 9), ("crank", 12)],
         panels=[dict(at=0.55, card="+60 MIN")],
         vo=[("NARR", "A minute of cranking buys you about ten minutes of radio. Charging a walkie-talkie? Way less. You crank for an hour.")]),
    dict(id="7.5", tc="9:45", bg="BG09I", letterbox=True, music="none", cam=push(1.6, 960, 600),
         props_front=[(S.walkie(False, 2.4), 960, 1000)],
         panels=[dict(at=0.15, props_front=[(S.walkie(True, 2.4), 960, 1000)])], sfx=[("blip", 2.0), ("static", 9.0)],
         vo_at=3.0, vo=[("BO", "Hello? Anyone? Westbrook High. Two students. One's sick.")]),
    dict(id="7.6", tc="10:00", bg="BG09I", letterbox=True, music="hero", cast=[BH("crying", "off", shirt="#F4F4F4")],
         panels=[dict(at=0.4, cast=[BH("laughing", "off", shirt="#F4F4F4")])], sfx=[("static", 0)],
         vo=[("PLOW", "...County Plow Seven. Say again, kid?"),
             ("NARR", "Your mood light is dead. You don't need it. Everyone can see your face.")]),
    dict(id="7.7", tc="10:15", bg=("BG04D", dict(plow=True, doors_dug=True)), counter="DAY 7", music="keep", cam=push(1.12, 960, 600),
         cast=[dict(who="ff", x=760, s=1.5), dict(who="ff", x=1100, s=1.5, face="happy")],
         panels=[dict(at=0.12, letterbox=False)], letterbox=True,
         vo=[("NARR", "Day seven. The sun comes out. So does a snowplow.")]),
    dict(id="7.8", tc="10:35", bg=("BG04D", dict(plow=True, doors_dug=True)), music="none",
         cast=[dict(who="ff", pose="camera", x=1250, s=2.4), B("idle", "neutral", "off", x=520, s=1.9, shirt="#F4F4F4"),
               R("idle", "neutral", x=780, s=1.9, wrapped=True)],
         panels=[dict(at=0.33, bg="GFX_THERMAL", cast=[]),
                 dict(at=0.66, bg=("BG04D", dict(plow=True, doors_dug=True)),
                      cast=[B("idle", "shocked", "off", x=760, s=2.6, shirt="#F4F4F4"), R("idle", "shocked", x=1180, s=2.6, wrapped=True)])],
         sfx=[("lowhit", 15.0)], vo_at=1.0,
         vo=[("FIREFIGHTER", "We swept the building with thermal. Three heat signatures. Where's the third kid?"),
             ("PAUSE", "6.0"), ("NARR", "...Three.")]),

    # ======================================================== B8 EPILOGUE
    dict(id="8.1", tc="11:00", bg="BG02", card="2 WEEKS LATER", music="comedy",
         cast=[B("idle", "neutral", "calm", x=760, extra=SCRUNCHIE_BAND)], cam=push(1.08),
         vo=[("NARR", "Two weeks later. Everything's normal. Mostly.")]),
    dict(id="8.2", tc="11:10", bg="BG02", music="keep",
         cast=[B("crush_shy", "crush", "crush", x=760, extra=SCRUNCHIE_BAND), R("head_tap", "smirk", x=1240)], sfx=[("blip", 1.2)],
         vo=[("NARR", "Your headphones work again. Sort of. They only seem to have one color now.")]),
    dict(id="8.3", tc="11:20", bg="BG02", music="none", sfx=[("beach", 0.2)],
         cast=[B("idle", "deadpan", "crush", x=760, extra=SCRUNCHIE_BAND), R("walk", "laughing", "up", x=1500, flip=True)]),
    dict(id="8.4", tc="11:28", bg=("BG12", dict(outside="dawn", fill=0.1, night=False)), music="none",
         cam=push(1.3, 1100, 640), sfx=[("wind", 0), ("lowhit", 6)],
         props=[(BIN, 1240, 800, 0.9)], cast=[dict(who="raincoat", x=1130, y=800, s=0.9)],
         panels=[dict(at=0.5, props=[(BIN + WRAPPERS, 1240, 800, 0.9)], cast=[dict(who="raincoat", x=1400, y=790, s=0.85)])]),
    dict(id="8.5", tc="11:40", bg="BG02", music="heart", cast=[BH("thinking", "focus", extra=SCRUNCHIE_BAND)],
         panels=[dict(at=0.45, card="WHO WAS THE 3RD?")], sfx=[("tap", 17.5)],
         vo=[("NARR", "Would you give up the thing that makes you, you, to save someone? And who was the third heat signature? Tell me in the comments.")]),
]
