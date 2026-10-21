"""Coop landing illustration: the giant COOP wordmark is the diagram, the egg is the match.

Usage: python hero2.py OUT_DIR
"""
import importlib.util, math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE / 'sketch.py' if (HERE / 'sketch.py').exists() else HERE.parent / 'sketches' / 'sketch.py'
_spec = importlib.util.spec_from_file_location('coop_sketch', ENGINE)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
g = _mod.__dict__
Sheet, Cam, box, ellipse, bez, egg, rrect, dashed = (g[k] for k in ('Sheet', 'Cam', 'box', 'ellipse', 'bez', 'egg', 'rrect', 'dashed'))

W2, H2 = 2000, 900
INK = {'venue': '#3E7396', 'clubs': '#C4572B', 'match': '#7B7A2C', 'regulars': '#B8232F', 'word': '#121212'}
YOLK = '#FFC300'

# wordmark geometry (shared by everything that points at the egg)
K = 3.2
X0, BASE = 500, 600
S = K / 3.0


def wordmark_layout():
    x = X0
    out = []
    for ch in 'CO':
        w, _ = g['PARSED'][ch]
        out.append((ch, x))
        x += w * K + 24 * S
    ex = x + 120 * S
    ey = BASE - 150 * S
    px = ex + 140 * S
    return out, (ex, ey), px


LETTERS, EGG, PX = wordmark_layout()
EGG_R = 1.42 * S            # egg() scale
EGG_TOP = EGG[1] - 95 * EGG_R
EGG_BOT = EGG[1] + 110 * EGG_R


def use(hexc, fill=None):
    f = fill or hexc
    g['PALETTE'] = {'yolk': f, 'dusk': f, 'ink': hexc, 'boost': 0.42 if fill is None else 1.0}
    g['COLOR_INK'] = hexc


def frag(fn, seed, ink, fill=None):
    use(ink, fill)
    sh = Sheet(seed)
    fn(sh)
    use(ink, fill)
    return re.search(r'</defs>(.*)</svg>', sh.svg(color=True), re.S).group(1)


def badge(sh, x, y, n):
    sh.poly(ellipse(x, y, 26, 26, n=22), width=2.4)
    sh.marker(ellipse(x, y, 22, 22, n=14)[:-1], 'yolk', spacing=6, width=6)
    sh.text(str(n), x, y + 13, size=30, anchor='middle', width=2.6)


def label(sh, x, y, n, title, sub):
    badge(sh, x, y, n)
    sh.text(title, x + 42, y + 13, size=34, width=2.6)
    sh.text(sub, x + 44, y + 50, size=19, width=1.8)


# ---------------------------------------------------------------- the giant wordmark
def word(sh):
    for ch, x in LETTERS:
        _, polys = g['PARSED'][ch]
        for pl in polys:
            sh.line([(x + gx * K, BASE - 100 * K + gy * K) for gx, gy in pl], width=9.5, passes=2, wobble=2.4, over=10)
    sh.poly(egg(EGG[0], EGG[1], EGG_R)[:-1], width=9.5)
    _, polys = g['PARSED']['P']
    for pl in polys:
        sh.line([(PX + gx * K, BASE - 100 * K + gy * K) for gx, gy in pl], width=9.5, passes=2, wobble=2.4, over=10)


def yolk(sh):
    for ang in (30, 120):
        sh.marker(ellipse(EGG[0], EGG[1] + 32 * S, 50 * S, 50 * S, n=36)[:-1], 'yolk', angle=ang, opacity=1.0, spacing=4.5, width=4.5, shift=1.5)


# ---------------------------------------------------------------- 1 · the venue: chairs up on the table
def flipped_chair(sh, cam, x, y, top, side):
    """A bistro chair turned upside down on the table: seat down, legs up, backrest hanging over the edge."""
    seat = [cam.P(p) for p in ((x - 20, y - 20, top), (x + 20, y - 20, top), (x + 20, y + 20, top), (x - 20, y + 20, top))]
    sh.poly(seat, width=2.4)
    sh.marker(seat, 'yolk', opacity=0.5)
    for lx, ly in ((x - 18, y - 18), (x + 18, y - 18), (x - 18, y + 18), (x + 18, y + 18)):
        sh.line([cam.P((lx, ly, top)), cam.P((lx + (lx - x) * 0.12, ly + (ly - y) * 0.12, top + 30))], width=2.4, passes=1)
    sh.line([cam.P((x - 20, y - 20, top + 20)), cam.P((x + 20, y - 20, top + 20))], width=1.6, passes=1)
    by = y + 20 if side > 0 else y - 20
    back = [cam.P(p) for p in ((x - 18, by, top), (x + 18, by, top), (x + 18, by, top - 28), (x - 18, by, top - 28))]
    sh.poly(back, width=2.2)
    for k in (-6, 6):
        sh.line([cam.P((x + k, by, top)), cam.P((x + k, by, top - 28))], width=1.5, passes=1)


def venue(sh):
    cam = Cam(-24, 22, 1.7, 220, 420, D=1200)
    sh.color = 'dusk'
    box(sh, cam, -60, -38, 72, 120, 76, 5, shade=0.4, spacing=5)
    sh.color = None
    box(sh, cam, -4, -4, 0, 8, 8, 72, shade=0.3, spacing=4, width=2.2)
    box(sh, cam, -26, -26, 0, 52, 52, 3, shade=0.4, spacing=4, width=2.0)
    flipped_chair(sh, cam, -32, -6, 77, -1)
    flipped_chair(sh, cam, 32, 6, 77, 1)
    sh.line([(40, 416), (390, 404)], width=2.0, passes=1)
    moon = bez((390, 130), (355, 140), (350, 196), (396, 206)) + bez((396, 206), (372, 188), (370, 150), (390, 130))[1:]
    sh.poly(moon, width=2.2)
    sh.marker(moon, 'yolk', opacity=0.5)
    for sx, sy in ((330, 120), (300, 168)):
        sh.line([(sx - 7, sy), (sx + 7, sy)], width=1.8, passes=1, over=1)
        sh.line([(sx, sy - 7), (sx, sy + 7)], width=1.8, passes=1, over=1)
    label(sh, 66, 62, 1, 'THE VENUE', 'EMPTY ON SLOW NIGHTS')


# ---------------------------------------------------------------- 2 · the clubs
def clubs(sh):
    # paint palette + brush
    px, py = 110, 750
    pal = [(px + 52 * math.cos(t) * (1 + 0.08 * math.sin(3 * t)), py + 36 * math.sin(t)) for t in [i * 2 * math.pi / 36 for i in range(36)]]
    sh.poly(pal)
    sh.marker(pal, 'yolk', opacity=0.45)
    sh.poly(ellipse(px + 24, py + 12, 8, 7, n=10), width=1.9, passes=1)
    for dx, dy in ((-26, -10), (-4, -20), (16, -16), (-30, 12)):
        sh.poly(ellipse(px + dx, py + dy, 7, 6, n=10), width=1.7, passes=1)
        sh.marker(ellipse(px + dx, py + dy, 6, 5, n=8)[:-1], 'yolk', spacing=4, width=5, shift=1)
    sh.line([(px + 16, py - 54), (px + 62, py - 92)], width=2.6)
    sh.text('ART', px - 22, py + 84, size=20)
    # scarf on knitting needles
    kx, ky = 225, 680
    sh.line([(kx - 50, ky - 10), (kx + 52, ky + 6)], width=2.6)
    sh.line([(kx - 46, ky + 8), (kx + 56, ky - 14)], width=2.6)
    scarf = [(kx - 30, ky + 2), (kx + 30, ky + 2), (kx + 34, ky + 110), (kx - 26, ky + 112)]
    sh.poly(scarf, width=2.3)
    sh.marker(scarf, 'yolk', opacity=0.55)
    for r in range(6):
        for c in range(4):
            cx, cy = kx - 20 + c * 14 + r * 0.6, ky + 14 + r * 16
            sh.line([(cx - 5, cy - 4), (cx, cy + 4), (cx + 5, cy - 4)], width=1.4, passes=1, over=0.5)
    for fx in (kx - 22, kx - 8, kx + 6, kx + 20):
        sh.line([(fx, ky + 112), (fx - 2, ky + 130)], width=1.6, passes=1)
    sh.text('KNIT', kx - 26, ky + 162, size=20)
    # open book
    bx, by = 345, 752
    left = bez((bx, by + 14), (bx - 30, by - 4), (bx - 62, by - 2), (bx - 76, by + 8)) + [(bx - 76, by + 54)] + bez((bx - 76, by + 54), (bx - 60, by + 46), (bx - 30, by + 48), (bx, by + 62))[1:]
    right = bez((bx, by + 14), (bx + 30, by - 4), (bx + 62, by - 2), (bx + 76, by + 8)) + [(bx + 76, by + 54)] + bez((bx + 76, by + 54), (bx + 60, by + 46), (bx + 30, by + 48), (bx, by + 62))[1:]
    sh.poly(left[:-1], width=2.3)
    sh.poly(right[:-1], width=2.3)
    sh.marker(right[:-1], 'yolk', opacity=0.5)
    sh.line([(bx, by + 14), (bx, by + 62)], width=2.0)
    for k in range(3):
        sh.line([(bx - 62, by + 16 + k * 10), (bx - 14, by + 22 + k * 10)], width=1.3, passes=1)
        sh.line([(bx + 14, by + 22 + k * 10), (bx + 62, by + 16 + k * 10)], width=1.3, passes=1)
    sh.text('BOOK', bx - 30, by + 112, size=20)
    # stopwatch
    wx, wy = 455, 640
    sh.poly(ellipse(wx, wy, 32, 32, n=26), width=2.4)
    sh.marker(ellipse(wx, wy, 28, 28, n=16)[:-1], 'yolk', opacity=0.45)
    sh.poly([(wx - 8, wy - 44), (wx + 8, wy - 44), (wx + 8, wy - 34), (wx - 8, wy - 34)], width=2.0)
    sh.line([(wx + 22, wy - 26), (wx + 30, wy - 34)], width=2.2)
    sh.line([(wx, wy), (wx, wy - 20)], width=2.2)
    sh.line([(wx, wy), (wx + 14, wy + 6)], width=2.2)
    sh.text('RUN', wx - 20, wy + 70, size=20)
    label(sh, 66, 540, 2, 'THE CLUBS', 'NOWHERE TO MEET')


# ---------------------------------------------------------------- 3 · the match (label + checks, sits under the egg)
def match(sh):
    ex = EGG[0]
    badge(sh, ex - 120, BASE + 70, 3)
    sh.text('THE MATCH', ex - 78, BASE + 83, size=30, width=2.5)
    for i, t in enumerate(('AREA', 'SIZE', 'NIGHT')):
        x, y = ex - 140 + i * 102, BASE + 116
        sh.poly([(x, y), (x + 20, y), (x + 20, y + 20), (x, y + 20)], width=2.0)
        sh.line([(x + 3, y + 10), (x + 9, y + 17), (x + 24, y - 5)], width=2.4)
        sh.text(t, x + 28, y + 19, size=17, width=1.7)
    # flows: in from the venue (over the C and O), in from the clubs (under them), out over the P
    a = math.radians(205)
    tip_in1 = (EGG[0] + 96 * EGG_R * math.cos(a) - 48, EGG_TOP + 30 - 44)
    sh.arrow(bez((420, 250), (560, 130), (720, 110), (tip_in1[0], tip_in1[1])), head=16, width=2.8)
    tip_in2 = (EGG[0] - 82 * EGG_R - 40, EGG_BOT - 4)
    sh.arrow(bez((500, 760), (640, 820), (760, 800), (tip_in2[0], tip_in2[1])), head=16, width=2.8)
    start_out = (EGG[0] + 46, EGG_TOP - 44)
    sh.arrow(bez(start_out, (EGG[0] + 160, 100), (1500, 110), (1600, 230)), head=16, width=2.8)


# ---------------------------------------------------------------- 4 · the regulars: a full round table, every week
TX, TY, TR, CR = 1770, 470, 82, 132


def rot(pts, cx, cy, a):
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def regulars(sh):
    sh.poly(ellipse(TX, TY, TR, TR, n=40))
    sh.poly(ellipse(TX, TY, TR - 9, TR - 9, n=40), width=1.5, passes=1)
    for i in range(6):
        t = i * 2 * math.pi / 6 + math.pi / 6
        px, py = TX + (TR - 30) * math.cos(t), TY + (TR - 30) * math.sin(t)
        sh.poly(ellipse(px, py, 12, 12, n=12), width=1.6, passes=1)
        sh.poly(ellipse(px, py, 6, 6, n=8), width=1.2, passes=1)
    tent = rot([(TX - 30, TY - 9), (TX + 30, TY - 9), (TX + 30, TY + 9), (TX - 30, TY + 9)], TX, TY, -0.15)
    sh.poly(tent, width=2.0)
    sh.text('CLUB', TX, TY + 6, size=13, anchor='middle', rot=-0.15, width=1.4)
    for i in range(6):
        t = i * 2 * math.pi / 6 + math.pi / 6
        cx, cy = TX + CR * math.cos(t), TY + CR * math.sin(t)
        q = rot(rrect(cx - 26, cy - 22, 52, 44, 10), cx, cy, t + math.pi / 2)
        sh.poly(q, width=2.3)
        for ang in (25, 115):
            sh.marker(q, 'yolk', angle=ang, opacity=0.95, spacing=5, width=5, shift=1.5)
    # every-week loop
    loop = ellipse(TX, TY, CR + 64, CR + 64, a0=math.radians(200), a1=math.radians(520), n=60)
    sh.arrow(loop, head=16, width=2.4)
    sh.text('EVERY WEEK', TX - 64, TY + CR + 112, size=20)
    label(sh, 1590, 62, 4, 'THE REGULARS', 'EVERY SEAT TAKEN')


def build(out):
    out.mkdir(parents=True, exist_ok=True)
    g['W'], g['H'] = W2, H2
    parts = [
        frag(venue, 2101, INK['venue']),
        frag(clubs, 2102, INK['clubs']),
        frag(regulars, 2104, INK['regulars'], YOLK),
        frag(match, 2103, INK['match']),
        frag(yolk, 2105, INK['word'], YOLK),
        frag(word, 2106, INK['word']),
    ]
    defs = ('<defs><filter id="ink" x="-2%" y="-2%" width="104%" height="104%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="4"/>'
            '<feDisplacementMap in="SourceGraphic" scale="1.6"/></filter></defs>')
    (out / 'coop-hero.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" fill="none">'
                                       + defs + ''.join(parts) + '</svg>', encoding='utf-8')
    print('wrote coop-hero.svg')


if __name__ == '__main__':
    build(Path(sys.argv[1]))
