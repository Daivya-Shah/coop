"""Landing concepts in Coop's existing style: white page, coloured pen sketches, one colour per step.

Every sketch is drawn big and airy on its own canvas. Usage: python landing_v2.py OUT_DIR
"""
import importlib.util, math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('coop_sketch', HERE / 'sketch.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
g = mod.__dict__
Sheet, Cam, box, stool, chair, cylinder, circle3d, pawn, egg, ellipse, bez, rrect, rotate, dashed = (
    g[k] for k in ('Sheet', 'Cam', 'box', 'stool', 'chair', 'cylinder', 'circle3d', 'pawn', 'egg', 'ellipse', 'bez', 'rrect', 'rotate', 'dashed'))
g['CLEAN'] = True

TEAL, RUST, OLIVE, CRIMSON, PINK, YOLK = '#3E7396', '#C4572B', '#7B7A2C', '#B8232F', '#D776A8', '#FFC300'
DEFS = ('<defs><filter id="ink" x="-2%" y="-2%" width="104%" height="104%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="4"/>'
        '<feDisplacementMap in="SourceGraphic" scale="1.6"/></filter></defs>')


def ink(hexc, fill=None):
    if fill:
        g['PALETTE'] = {'yolk': fill, 'dusk': fill, 'ink': hexc, 'boost': 1.0}
    else:
        g['PALETTE'] = {'yolk': hexc, 'dusk': hexc, 'ink': hexc, 'boost': 0.42}
    g['COLOR_INK'] = hexc


def compose(w, h, parts, seed=1):
    """parts: list of (draw_fn, ink_hex, fill_hex_or_None). Each is drawn on its own layer and stacked."""
    g['W'], g['H'] = w, h
    layers = []
    for i, (fn, c, f) in enumerate(parts):
        ink(c, f)
        sh = Sheet(seed * 100 + i)
        fn(sh)
        ink(c, f)
        layers.append(re.search(r'</defs>(.*)</svg>', sh.svg(color=True), re.S).group(1))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">{DEFS}{"".join(layers)}</svg>'


def badge(sh, x, y, n, label=None, sub=None, size=44):
    sh.poly(ellipse(x, y, 28, 28, n=22), width=2.4)
    sh.marker(ellipse(x, y, 24, 24, n=14)[:-1], 'yolk', spacing=6, width=6)
    sh.text(str(n), x, y + 14, size=32, anchor='middle', width=2.6)
    if label:
        sh.text(label, x + 48, y + 16, size=size, width=2.7)
    if sub:
        sh.text(sub, x + 50, y + 54, size=22, width=1.9)


# ---------------------------------------------------------------- objects
def yarn(sh, x, y, s=1.0):
    r = 34 * s
    sh.poly(ellipse(x, y, r, r, n=28))
    sh.marker(ellipse(x, y, r - 3, r - 3, n=18)[:-1], 'yolk')
    for k in range(4):
        sh.line(ellipse(x, y, r * .92, r * (.3 + k * .17), rot=.5 + k * .5, a0=.2, a1=2.9, n=14), width=1.6, passes=1)
    sh.line([(x - 18 * s, y - 62 * s), (x + 16 * s, y + 6 * s)], width=2.3)
    sh.line([(x + 26 * s, y - 66 * s), (x - 4 * s, y + 4 * s)], width=2.3)


def books(sh, x, y, s=1.0):
    for i, (dx, rot) in enumerate(((0, -.05), (5, .04), (-4, -.02))):
        q = [(dx - 46, -i * 15), (dx + 46, -i * 15), (dx + 46, -i * 15 - 13), (dx - 46, -i * 15 - 13)]
        q = [(x + (u * math.cos(rot) - v * math.sin(rot)) * s, y + (u * math.sin(rot) + v * math.cos(rot)) * s) for u, v in q]
        sh.poly(q, width=2.2)
        if i != 1:
            sh.marker(q, 'yolk', spacing=6, width=7)


def sneaker(sh, x, y, s=1.0):
    k = .34 * s
    T = lambda pts: [(x + (u - 150) * k, y + (v - 100) * k) for u, v in pts]
    up = bez((10, 140), (0, 60), (30, 40), (70, 40)) + bez((70, 40), (120, 40), (150, 70), (200, 80))[1:] + bez((200, 80), (260, 90), (300, 110), (300, 140))[1:]
    sh.line(T(up))
    sh.poly(T([(4, 140), (304, 140), (300, 160), (10, 160)]))
    sh.marker(T(up + [(300, 140), (10, 140)]), 'yolk')
    for i in range(4):
        u = 100 + i * 18
        sh.line(T([(u, 52 + i * 4), (u + 20, 74 + i * 3)]), width=1.6, passes=1)


def palette(sh, x, y, s=1.0):
    pal = [(x + 54 * s * math.cos(t) * (1 + .08 * math.sin(3 * t)), y + 38 * s * math.sin(t)) for t in [i * 2 * math.pi / 36 for i in range(36)]]
    sh.poly(pal)
    sh.marker(pal, 'yolk', opacity=.6)
    sh.poly(ellipse(x + 24 * s, y + 12 * s, 8 * s, 7 * s, n=10), width=1.6, passes=1)
    for dx, dy in ((-26, -10), (-4, -21), (16, -17), (-30, 12)):
        sh.poly(ellipse(x + dx * s, y + dy * s, 7 * s, 6 * s, n=10), width=1.5, passes=1)
    sh.line([(x + 16 * s, y - 58 * s), (x + 66 * s, y - 100 * s)], width=2.3)


def hola(sh, x, y, s=1.0):
    sh.poly(ellipse(x, y, 60 * s, 28 * s, n=26), width=2.1)
    sh.line([(x - 22 * s, y + 24 * s), (x - 38 * s, y + 50 * s), (x - 4 * s, y + 27 * s)], width=2.0)
    sh.text('HOLA!', x, y + 9 * s, size=22 * s, anchor='middle', width=1.9)


def pendant(sh, x, top, y, s=1.0, lit=False):
    sh.line([(x, top), (x, y - 26 * s)], width=1.8)
    dome = bez((x - 34 * s, y), (x - 32 * s, y - 34 * s), (x + 32 * s, y - 34 * s), (x + 34 * s, y))
    sh.line(dome)
    sh.poly(ellipse(x, y, 34 * s, 6 * s, n=20), width=1.8)
    sh.marker(dome, 'yolk')
    if lit:
        for dx in (-26, -9, 9, 26):
            sh.line([(x + dx * .4 * s, y + 12 * s), (x + dx * 1.5 * s, y + 70 * s)], width=1.4, passes=1)


def clock(sh, x, y, r=30):
    sh.poly(ellipse(x, y, r, r, n=24))
    sh.line([(x, y), (x, y - r * .7)], width=2.0)
    sh.line([(x, y), (x + r * .55, y + r * .3)], width=2.0)


# ---------------------------------------------------------------- the venue (empty or full), one consistent room
def venue_room(sh, ox, oy, s=1.0, full=False):
    cam = Cam(-30, 17, 1.25 * s, ox, oy, D=1500)
    sh.color = 'dusk'
    box(sh, cam, -240, -10, 0, 230, 45, 96, shade=0.4, spacing=7)
    box(sh, cam, -246, -16, 96, 242, 58, 6, shade=0.4, spacing=4)
    sh.color = None
    box(sh, cam, -225, 0, 102, 54, 30, 34, shade=0.4, spacing=5)
    for x in (-215, -160, -105, -50):
        stool(sh, cam, x, -55)
    sh.color = 'yolk' if full else None
    box(sh, cam, 120, -120, 72, 100, 76, 5, shade=0.4, spacing=5)
    sh.color = None
    box(sh, cam, 166, -86, 0, 8, 8, 72, shade=0.3, spacing=4, width=2.2)
    box(sh, cam, 146, -106, 0, 48, 48, 3, shade=0.4, spacing=4, width=2.0)
    if full:
        for x, y in ((140, -100), (196, -70)):
            cylinder(sh, cam, x, y, 77, 7, 9, shade=False)
        for x in (-190, -125, -70):
            cylinder(sh, cam, x, 6, 102, 6, 8, shade=False)
        chair(sh, cam, 120, -150, back=-1)
        chair(sh, cam, 200, -150, back=-1)
    lx0 = ox - 230 * s
    for k, lx in enumerate((lx0, lx0 + 130 * s, lx0 + 330 * s)):
        pendant(sh, lx, oy - 400 * s, oy - 330 * s, s=s * .85, lit=full)


def scene_venue(sh):
    venue_room(sh, 500, 790, s=1.5)
    clock(sh, 790, 250)
    badge(sh, 90, 90, 1, 'THE VENUE', 'EMPTY ON SLOW NIGHTS')


def scene_venue_full(sh):
    venue_room(sh, 500, 790, s=1.5, full=True)
    badge(sh, 90, 90, 4, 'THE REGULARS', 'SAME TABLE, EVERY WEEK')


# ---------------------------------------------------------------- the clubs, spread out
def scene_clubs(sh):
    items = [(yarn, 170, 360, 'KNIT'), (books, 430, 380, 'BOOK'), (palette, 690, 360, 'ART'),
             (sneaker, 190, 640, 'RUN'), (lambda sh, x, y, s: pawn(sh, x, y + 50, k=.7, shade=True), 450, 610, 'CHESS'), (hola, 700, 600, 'TALK')]
    for fn, x, y, lab in items:
        fn(sh, x, y, 1.25)
        sh.text(lab, x, y + 110, size=24, anchor='middle', width=2.0)
    badge(sh, 90, 90, 2, 'THE CLUBS', 'NOWHERE REGULAR TO MEET')


# ---------------------------------------------------------------- the match
def scene_match(sh):
    hx, hy = 450, 450
    house = [(hx - 170, hy + 170), (hx - 170, hy - 30), (hx, hy - 190), (hx + 170, hy - 30), (hx + 170, hy + 170)]
    sh.poly(house, width=2.8)
    sh.marker(house, 'yolk', opacity=.4)
    sh.line([(hx - 200, hy - 16), (hx, hy - 222), (hx + 200, hy - 16)], width=2.0, passes=1)
    sh.poly(egg(hx, hy + 52, 1.0)[:-1], width=2.8)
    for i, t in enumerate(('RIGHT AREA', 'RIGHT SIZE', 'RIGHT NIGHT')):
        x, y = 290, 700 + i * 46
        sh.poly([(x, y), (x + 26, y), (x + 26, y + 26), (x, y + 26)], width=2.2)
        sh.line([(x + 4, y + 13), (x + 11, y + 22), (x + 32, y - 8)], width=2.8)
        sh.text(t, x + 44, y + 25, size=24, width=2.0)
    badge(sh, 90, 90, 3, 'THE MATCH', 'BOTH SAY YES FIRST')


def yolk_for(cx, cy, r):
    def fn(sh):
        for ang in (30, 120):
            sh.marker(ellipse(cx, cy, r, r, n=30)[:-1], 'yolk', angle=ang, opacity=1.0, spacing=4.5, width=4.5, shift=1)
    return fn


# ---------------------------------------------------------------- the regulars: the long table
def scene_regulars(sh):
    cam = Cam(-26, 27, 1.55, 470, 560, D=1100)
    for x in (-150, -70, 10, 90, 170):
        for px in (x - 18, x + 15):
            box(sh, cam, px, 60, 77, 3, 3, 16, shade=2, width=2.1)
        box(sh, cam, x - 18, 60, 88, 36, 3, 8, spacing=5)
    sh.color = 'dusk'
    box(sh, cam, -210, -45, 72, 420, 90, 6, spacing=6)
    sh.color = None
    for lx, ly in ((-205, -40), (199, -40), (-205, 34), (199, 34)):
        box(sh, cam, lx, ly, 0, 6, 6, 72, shade=0.2, spacing=5, width=2.3)
    for x, y in ((-140, 10), (-40, 0), (60, 14), (150, -6)):
        cylinder(sh, cam, x, y, 78, 7, 9, shade=False)
    for x in (-180, -90, 20, 110, 190):
        sh.poly([cam.P(p) for p in circle3d(cam, x, -28, 78.5, 10)[:-1]], width=1.8, passes=1)
    chair(sh, cam, 235, -110, back=-1)
    for lx in (250, 470, 690):
        pendant(sh, lx, 160, 270, s=1.0, lit=True)
    sh.text('ONE SAVED FOR YOU', 520, 860, size=24, width=2.0)
    badge(sh, 90, 90, 4, 'THE REGULARS', 'SAME TABLE, EVERY WEEK')


# ---------------------------------------------------------------- noticeboard in the step colours
def card(sh, cx, cy, w, h, rot, lines, size=22, fill=False):
    q = rotate(rrect(cx - w / 2, cy - h / 2, w, h, 6), cx, cy, rot)
    if fill:
        sh.marker(q, 'yolk', opacity=.35, spacing=12)
    sh.poly(q, width=2.1)
    n = len(lines)
    for i, t in enumerate(lines):
        p = rotate([(cx, cy - (n - 1) * size * .7 + i * size * 1.4 + size * .35)], cx, cy, rot)[0]
        sh.text(t, p[0], p[1], size=size if i == 0 else size * .82, rot=rot, anchor='middle', width=2.0 if i == 0 else 1.6)
    p = rotate([(cx, cy - h / 2 + 14)], cx, cy, rot)[0]
    sh.poly(ellipse(p[0], p[1], 9, 9, n=12), width=1.8)


CLUB_CARDS = [((260, 200), -.05, ['BOOK CLUB', '14 OF US', 'NEED A TABLE']),
              ((250, 620), .04, ['RUN CLUB', '5K...', 'THEN WHERE?']),
              ((1190, 400), .05, ['KNITTERS', 'SEEKING A', 'COZY CORNER'])]
VENUE_CARDS = [((720, 170), .03, ['BACK ROOM FREE', 'MONDAYS', 'WINE BAR, LES']),
               ((1180, 740), -.04, ['QUIET WEDNESDAYS', 'ROOM FOR 20', 'CAFE, CHELSEA']),
               ((700, 740), .02, ['6 CHESS TABLES', 'EMPTY TUESDAYS', 'BAR, EAST VILLAGE'])]
HUB = (720, 450)


def board_frame(sh):
    sh.poly([(40, 40), (1420, 40), (1420, 880), (40, 880)], width=2.4)
    sh.poly([(62, 62), (1398, 62), (1398, 858), (62, 858)], width=1.5, passes=1)
    for (c, _, _) in CLUB_CARDS + VENUE_CARDS:
        mid = ((c[0] + HUB[0]) / 2, (c[1] + HUB[1]) / 2 + 40)
        dashed(sh, bez((c[0], c[1] - 50), mid, mid, (HUB[0], HUB[1] - 100)), on=9, off=8, width=1.4)


def board_clubs(sh):
    for c, rot, lines in CLUB_CARDS:
        card(sh, c[0], c[1], 260, 160, rot, lines, fill=True)


def board_venues(sh):
    for c, rot, lines in VENUE_CARDS:
        card(sh, c[0], c[1], 290, 160, rot, lines, size=20, fill=True)


def board_hub(sh):
    card(sh, HUB[0], HUB[1], 320, 260, -.015, [], fill=True)
    sh.poly(egg(HUB[0], HUB[1] - 46, .38)[:-1], width=2.2)
    sh.text('COOP', HUB[0], HUB[1] + 44, size=40, anchor='middle', width=2.6)
    sh.text("WE'LL INTRODUCE YOU", HUB[0], HUB[1] + 90, size=19, anchor='middle', width=1.7)


def build(out):
    out.mkdir(parents=True, exist_ok=True)
    files = {
        'step1.svg': compose(900, 900, [(scene_venue, TEAL, None)], 1),
        'step2.svg': compose(900, 900, [(scene_clubs, RUST, None)], 2),
        'step3.svg': compose(900, 900, [(scene_match, OLIVE, None), (yolk_for(450, 450 + 52 + 16, 34), OLIVE, YOLK)], 3),
        'step4.svg': compose(900, 900, [(scene_regulars, CRIMSON, None)], 4),
        'empty.svg': compose(900, 900, [(scene_venue, TEAL, None)], 5),
        'full.svg': compose(900, 900, [(scene_venue_full, CRIMSON, None)], 6),
        'board.svg': compose(1460, 920, [(board_frame, '#8a7f72', None), (board_clubs, RUST, None),
                                          (board_venues, TEAL, None), (board_hub, OLIVE, None),
                                          (yolk_for(HUB[0], HUB[1] - 40, 14), OLIVE, YOLK)], 7),
    }
    for name, svg in files.items():
        (out / name).write_text(svg, encoding='utf-8')
        print('wrote', name)


if __name__ == '__main__':
    build(Path(sys.argv[1]))
