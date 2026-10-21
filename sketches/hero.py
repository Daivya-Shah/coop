"""Coop hero: the whole business in one sketch, plus the hand-lettered wordmark.

Usage: python hero.py OUT_DIR
"""
import importlib.util, math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE / 'sketch.py' if (HERE / 'sketch.py').exists() else HERE.parent / 'sketches' / 'sketch.py'
_spec = importlib.util.spec_from_file_location('coop_sketch', ENGINE)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
g = _mod.__dict__   # live module namespace, so palette/size changes take effect
Sheet, Cam, box, chair, cylinder, stool, pawn, egg, ellipse, bez, dashed, circle3d = (
    g[k] for k in ('Sheet', 'Cam', 'box', 'chair', 'cylinder', 'stool', 'pawn', 'egg', 'ellipse', 'bez', 'dashed', 'circle3d'))

HW, HH = 2000, 1060
INKS = {'venue': '#3E7396', 'clubs': '#C4572B', 'match': '#7B7A2C', 'regulars': '#B8232F'}


def use_ink(hexc):
    g['PALETTE'] = {'yolk': hexc, 'dusk': hexc, 'ink': hexc, 'boost': 0.42}
    g['COLOR_INK'] = hexc


def badge(sh, x, y, n):
    sh.poly(ellipse(x, y, 30, 30, n=24), width=2.6)
    sh.marker(ellipse(x, y, 26, 26, n=16)[:-1], 'yolk', spacing=7, width=7)
    sh.text(str(n), x, y + 15, size=34, anchor='middle', width=2.8)


# ---------------------------------------------------------------- 1 · the venue, empty
def venue():
    sh = Sheet(901)
    cam = Cam(-30, 17, 1.25, 330, 560, D=1500)
    sh.color = 'dusk'
    box(sh, cam, -240, -10, 0, 230, 45, 96, shade=0.4, spacing=7)
    box(sh, cam, -246, -16, 96, 242, 58, 6, shade=0.4, spacing=4)
    sh.color = None
    box(sh, cam, -225, 0, 102, 54, 30, 34, shade=0.4, spacing=5)
    for x in (-215, -160, -105, -50):
        stool(sh, cam, x, -55)
    sh.color = 'yolk'
    box(sh, cam, 120, -120, 72, 100, 76, 5, shade=0.4, spacing=5)
    sh.color = None
    box(sh, cam, 166, -86, 0, 8, 8, 72, shade=0.3, spacing=4, width=2.2)
    box(sh, cam, 146, -106, 0, 48, 48, 3, shade=0.4, spacing=4, width=2.0)
    for lx in (110, 230, 420):
        sh.line([(lx, 190), (lx, 236)], width=1.9)
        sh.line(bez((lx - 30, 262), (lx - 28, 230), (lx + 28, 230), (lx + 30, 262)))
        sh.poly(ellipse(lx, 262, 30, 6, n=18), width=2.0)
        sh.marker(bez((lx - 30, 262), (lx - 28, 230), (lx + 28, 230), (lx + 30, 262)), 'dusk')
    sh.poly(ellipse(570, 190, 34, 34, n=24))
    sh.line([(570, 190), (570, 166)], width=2.2)
    sh.line([(570, 190), (588, 200)], width=2.2)
    badge(sh, 70, 105, 1)
    sh.text('THE VENUE', 118, 120, size=38, width=2.6)
    sh.text('EMPTY ON SLOW NIGHTS', 122, 162, size=20, width=1.9)
    return sh


# ---------------------------------------------------------------- 2 · the clubs, homeless
def clubs():
    sh = Sheet(913)
    # yarn + needles
    yx, yy = 130, 880
    sh.poly(ellipse(yx, yy, 50, 50, n=32))
    sh.marker(ellipse(yx, yy, 46, 46, n=20)[:-1], 'yolk')
    for k in range(5):
        sh.line(ellipse(yx, yy, 46, 14 + k * 7, rot=0.5 + k * 0.45, a0=0.2, a1=2.9, n=16), width=1.7, passes=1)
    sh.line([(yx - 26, yy - 90), (yx + 24, yy + 6)], width=2.5)
    sh.line([(yx + 38, yy - 96), (yx - 4, yy + 4)], width=2.5)
    sh.text('KNIT', yx - 30, yy + 90, size=22)
    # books
    cam = Cam(-22, 30, 1.5, 300, 905, D=900)
    for i in range(3):
        sh.color = 'yolk' if i != 1 else None
        box(sh, cam, -34, -24, i * 10, 68, 48, 10, shade=0.3, spacing=4.5)
        sh.color = None
    sh.text('BOOK', 262, 970, size=22)
    # paint palette + brush
    px, py = 470, 880
    pal = [(px + 62 * math.cos(t) * (1 + 0.08 * math.sin(3 * t)), py + 44 * math.sin(t)) for t in [i * 2 * math.pi / 40 for i in range(40)]]
    sh.poly(pal)
    sh.marker(pal, 'yolk', opacity=0.5)
    sh.poly(ellipse(px + 30, py + 14, 10, 8, n=10), width=2.0, passes=1)
    for dx, dy in ((-30, -12), (-6, -24), (18, -20), (-34, 14)):
        sh.poly(ellipse(px + dx, py + dy, 8, 7, n=10), width=1.8, passes=1)
        sh.marker(ellipse(px + dx, py + dy, 7, 6, n=8)[:-1], 'yolk', spacing=5, width=6, shift=1)
    sh.line([(px + 20, py - 70), (px + 80, py - 120)], width=2.8)
    sh.text('ART', px - 20, py + 90, size=22)
    # pawn
    pawn(sh, 610, 930, k=0.5, shade=True)
    sh.text('CHESS', 575, 970, size=22)
    # speech bubble + sneaker
    sh.poly(ellipse(715, 860, 58, 28, n=26), width=2.3)
    sh.line([(690, 884), (668, 908), (712, 888)], width=2.2)
    sh.text('HOLA!', 715, 870, size=22, anchor='middle')
    sx, sy, s = 520, 720, 0.42
    T = lambda pts: [(sx + x * s, sy + y * s) for x, y in pts]
    upper = bez((10, 140), (0, 60), (30, 40), (70, 40)) + bez((70, 40), (120, 40), (150, 70), (200, 80))[1:] + bez((200, 80), (260, 90), (300, 110), (300, 140))[1:]
    sh.line(T(upper))
    sh.poly(T([(4, 140), (304, 140), (300, 162), (10, 162)]))
    sh.marker(T(upper + [(300, 140), (10, 140)]), 'yolk')
    sh.text('RUN', 560, 820, size=22)
    badge(sh, 70, 680, 2)
    sh.text('THE CLUBS', 118, 695, size=38, width=2.6)
    sh.text('NOWHERE REGULAR TO MEET', 122, 737, size=20, width=1.9)
    return sh


# ---------------------------------------------------------------- 3 · coop, the match
def match():
    sh = Sheet(927)
    hx, hy = 960, 560
    house = [(hx - 120, hy + 110), (hx - 120, hy - 25), (hx, hy - 135), (hx + 120, hy - 25), (hx + 120, hy + 110)]
    sh.poly(house)
    sh.marker(house, 'yolk', opacity=0.45)
    sh.line([(hx - 142, hy - 14), (hx, hy - 160), (hx + 142, hy - 14)], width=2.0, passes=1)
    sh.poly(egg(hx, hy + 30, 0.72)[:-1], width=2.6)
    sh.marker(ellipse(hx, hy + 46, 26, 26, n=16)[:-1], 'yolk', opacity=0.95, spacing=7, width=8)
    # flows in and out
    sh.arrow(bez((560, 420), (690, 395), (760, 410), (795, 462)), width=2.6)
    sh.arrow(bez((660, 790), (740, 785), (785, 715), (800, 650)), width=2.6)
    sh.arrow(bez((1112, 560), (1160, 545), (1210, 545), (1262, 560)), head=15, width=2.6)
    badge(sh, 870, 790, 3)
    sh.text('COOP', 918, 805, size=38, width=2.6)
    sh.text('MATCHES THEM', 880, 850, size=24)
    for i, t in enumerate(('AREA', 'SIZE', 'NIGHT')):
        x, y = 860, 890 + i * 40
        sh.poly([(x, y), (x + 22, y), (x + 22, y + 22), (x, y + 22)], width=2.1)
        sh.line([(x + 3, y + 11), (x + 9, y + 19), (x + 26, y - 6)], width=2.6)
        sh.text(t, x + 36, y + 21, size=20)
    sh.text('BOTH SAY YES', 1100, 515, size=20, rot=-0.02)
    return sh


# ---------------------------------------------------------------- 4 · the regulars
def regulars():
    sh = Sheet(941)
    cam = Cam(-26, 27, 1.42, 1610, 690, D=1100)
    for x in (-150, -70, 10, 90, 170):
        for px in (x - 18, x + 15):
            box(sh, cam, px, 60, 77, 3, 3, 16, shade=2, width=2.1)
        box(sh, cam, x - 18, 60, 88, 36, 3, 8, spacing=5)
    sh.color = 'dusk'
    box(sh, cam, -210, -45, 72, 420, 90, 6, spacing=6)
    sh.color = None
    for lx, ly in ((-205, -40), (199, -40), (-205, 34), (199, 34)):
        box(sh, cam, lx, ly, 0, 6, 6, 72, shade=0.2, spacing=5, width=2.3)
    # club stuff all over the table
    A, B, C, D_ = (-60, -20, 78), (0, -20, 78), (0, -8, 104), (-60, -8, 104)
    sh.poly([cam.P(p) for p in (A, B, C, D_)])
    sh.marker([cam.P(p) for p in (A, B, C, D_)], 'yolk')
    sh.line([cam.P(B), cam.P((0, 4, 78)), cam.P(C)], width=2.2)
    a, b = cam.P((-54, -16, 88)), cam.P((-6, -16, 88))
    sh.text('RESERVED', a[0] + 2, a[1], size=11, rot=math.atan2(b[1] - a[1], b[0] - a[0]), width=1.5)
    yx, yy = cam.P((-150, 0, 86))
    sh.poly(ellipse(yx, yy, 18, 18, n=16), width=2.2)
    sh.marker(ellipse(yx, yy, 16, 16, n=12)[:-1], 'yolk')
    for i in range(2):
        sh.color = 'yolk'
        box(sh, cam, 40, -24, 78 + i * 6, 40, 28, 6, shade=0.3, spacing=4)
        sh.color = None
    for x, y in ((-100, 20), (120, 18), (160, -20), (-180, -25)):
        cylinder(sh, cam, x, y, 78, 7, 9, shade=False)
    for x in (-130, 90, 190):
        sh.poly([cam.P(p) for p in circle3d(cam, x, -30, 78.5, 10)[:-1]], width=1.9, passes=1)
    chair(sh, cam, 235, -110, back=-1)
    # lamps over the table, lit
    for lx in (1390, 1610, 1830):
        sh.line([(lx, 195), (lx, 300)], width=1.9)
        sh.line(bez((lx - 38, 330), (lx - 36, 290), (lx + 36, 290), (lx + 38, 330)))
        sh.poly(ellipse(lx, 330, 38, 7, n=20), width=2.0)
        sh.marker(bez((lx - 38, 330), (lx - 36, 290), (lx + 36, 290), (lx + 38, 330)), 'yolk')
        for dx in (-26, 0, 26):
            sh.line([(lx + dx * 0.4, 344), (lx + dx, 400)], width=1.6, passes=1)
    badge(sh, 1300, 105, 4)
    sh.text('THE REGULARS', 1348, 120, size=38, width=2.6)
    sh.text('SAME TABLE, SAME CLUB, EVERY WEEK', 1352, 162, size=20, width=1.9)
    sh.text('ONE SAVED FOR YOU', 1560, 990, size=20)
    sh.arrow(bez((1790, 972), (1830, 965), (1855, 950), (1868, 930)), head=9)
    return sh


# ---------------------------------------------------------------- the wordmark
def wordmark():
    sh = Sheet(959)
    k, y0 = 3.0, 300
    g['PARSED']['C'] = g['PARSED']['C']
    x = 40
    for ch in 'CO':
        w, polys = g['PARSED'][ch]
        for pl in polys:
            sh.line([(x + gx * k, y0 - 100 * k + gy * k) for gx, gy in pl], width=9, passes=2, wobble=2.2, over=10)
        x += w * k + 24
    # the second O is an egg with a yolk
    ex, ey = x + 120, y0 - 150
    sh.poly(egg(ex, ey, 1.42)[:-1], width=9)
    for ang in (30, 120):
        sh.marker(ellipse(ex, ey + 30, 46, 46, n=36)[:-1], 'yolk', angle=ang, opacity=1.0, spacing=4.5, width=4.5, shift=1.5)
    x = ex + 140
    w, polys = g['PARSED']['P']
    for pl in polys:
        sh.line([(x + gx * k, y0 - 100 * k + gy * k) for gx, gy in pl], width=9, passes=2, wobble=2.2, over=10)
    return sh


def svg_of(sh, ink, w, h):
    use_ink(ink)
    inner = re.search(r'</defs>(.*)</svg>', sh.svg(color=True), re.S).group(1)
    return inner


def build(out):
    out.mkdir(parents=True, exist_ok=True)
    g['CLEAN'] = True
    g['W'], g['H'] = HW, HH
    parts = []
    for fn, key in ((venue, 'venue'), (clubs, 'clubs'), (match, 'match'), (regulars, 'regulars')):
        use_ink(INKS[key])
        sh = fn()
        parts.append(svg_of(sh, INKS[key], HW, HH))
    defs = ('<defs><filter id="ink" x="-2%" y="-2%" width="104%" height="104%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="4"/>'
            '<feDisplacementMap in="SourceGraphic" scale="1.6"/></filter></defs>')
    (out / 'hero.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{HW}" height="{HH}" viewBox="0 0 {HW} {HH}" fill="none">'
                                  + defs + ''.join(parts) + '</svg>', encoding='utf-8')
    # wordmark: dark ink with a yolk egg
    g['W'], g['H'] = 990, 340
    g['PALETTE'] = {'yolk': '#FFC300', 'dusk': '#FFC300', 'ink': '#121212'}
    g['COLOR_INK'] = '#121212'
    wm = wordmark().svg(color=True)
    (out / 'wordmark.svg').write_text(wm, encoding='utf-8')
    print('wrote hero.svg and wordmark.svg')


if __name__ == '__main__':
    build(Path(sys.argv[1]))
