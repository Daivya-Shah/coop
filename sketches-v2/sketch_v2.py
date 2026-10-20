"""Coop sketches, volume 2: people, chickens, and goofier moments.

Builds on the pen engine in sketch.py (same folder).
Usage: python sketch_v2.py OUT_DIR [name ...]
"""
import math, sys
from pathlib import Path
from runpy import run_path

HERE = Path(__file__).resolve().parent
ENGINE = HERE / 'sketch.py' if (HERE / 'sketch.py').exists() else HERE.parent / 'sketches' / 'sketch.py'
g = run_path(str(ENGINE))
Sheet, bez, ellipse, egg, rrect, rotate, dashed, Cam, box, pawn = (
    g[k] for k in ('Sheet', 'bez', 'ellipse', 'egg', 'rrect', 'rotate', 'dashed', 'Cam', 'box', 'pawn'))

# a few more letters for the handwriting
for ch, (w, d) in {
    ',': (18, "M9 90 L5 104"),
    '(': (30, "M24 0 C 4 30, 4 70, 24 100"),
    ')': (30, "M6 0 C 26 30, 26 70, 6 100"),
    '#': (60, "M20 10 L14 92 M44 10 L38 92 M6 36 L56 36 M4 66 L54 66"),
}.items():
    g['PARSED'][ch] = (w, g['parse'](d))

PI = math.pi


# ---------------------------------------------------------------------------
# small drawing helpers
# ---------------------------------------------------------------------------
def dirv(a):
    r = math.radians(a)
    return math.sin(r), math.cos(r)


def dot(sh, x, y, r=2.4):
    sh.poly(ellipse(x, y, r, r * 1.1, n=8), width=2.6, passes=1)


def limb(sh, p, a1, l1, a2, l2, width=3.0, hand=True, hr=6.0):
    d1, d2 = dirv(a1), dirv(a2)
    e = (p[0] + l1 * d1[0], p[1] + l1 * d1[1])
    h = (e[0] + l2 * d2[0], e[1] + l2 * d2[1])
    sh.line([p, e, h], width=width)
    if hand:
        sh.poly(ellipse(h[0], h[1], hr, hr, n=10), width=2.2, passes=1)
    return h


def heart(sh, cx, cy, s, shade=True):
    pts = bez((cx, cy + 40 * s), (cx - 70 * s, cy - 10 * s), (cx - 40 * s, cy - 60 * s), (cx, cy - 25 * s)) + \
          bez((cx, cy - 25 * s), (cx + 40 * s, cy - 60 * s), (cx + 70 * s, cy - 10 * s), (cx, cy + 40 * s))[1:]
    sh.poly(pts[:-1])
    if shade:
        sh.hatch([(cx + 8 * s, cy - 20 * s), (cx + 40 * s, cy - 38 * s), (cx + 55 * s, cy - 8 * s), (cx + 8 * s, cy + 30 * s)], angle=60, spacing=5)


def sparkle(sh, x, y, s=1.0):
    for a in (0, 45, 90, 135):
        dx, dy = 12 * s * math.cos(math.radians(a)), 12 * s * math.sin(math.radians(a))
        k = 1 if a % 90 == 0 else 0.55
        sh.line([(x - dx * k, y - dy * k), (x + dx * k, y + dy * k)], width=1.9, passes=1, over=1)


def bubble(sh, cx, cy, rx, ry, tail, lines, size=24):
    tx, ty = tail
    a = math.atan2(ty - cy, tx - cx)
    b1 = (cx + rx * 0.85 * math.cos(a - 0.18), cy + ry * 0.85 * math.sin(a - 0.18))
    b2 = (cx + rx * 0.85 * math.cos(a + 0.18), cy + ry * 0.85 * math.sin(a + 0.18))
    sh.poly(ellipse(cx, cy, rx, ry, n=40))
    sh.line([b1, (tx, ty), b2], width=2.4)
    n = len(lines)
    for i, t in enumerate(lines):
        sh.text(t, cx, cy + size * 0.42 + (i - (n - 1) / 2) * size * 1.25, size=size, anchor='middle')


def sweat(sh, x, y, s=1.0):
    sh.poly(bez((x, y - 10 * s), (x - 7 * s, y), (x - 6 * s, y + 8 * s), (x, y + 8 * s)) + bez((x, y + 8 * s), (x + 6 * s, y + 8 * s), (x + 7 * s, y), (x, y - 10 * s))[1:], width=2.0, passes=1)


def motion(sh, x, y, n=3, length=40, gap=14, angle=0.0):
    for i in range(n):
        yy = y + (i - (n - 1) / 2) * gap
        sh.line([(x, yy), (x - length * math.cos(angle), yy - length * math.sin(angle))], width=2.0, passes=1, over=2)


# ---------------------------------------------------------------------------
# people
# ---------------------------------------------------------------------------
def face(sh, hx, hy, s, kind='smile', look=0, brows=None):
    ex = look * 3 * s
    if kind == 'sleepy':
        for dx in (-8, 8):
            sh.line(ellipse(hx + dx * s + ex, hy - 3 * s, 4.5 * s, 3 * s, a0=0.2, a1=PI - 0.2, n=6), width=2.2, passes=1)
    elif kind == 'wide':
        for dx in (-9, 9):
            sh.poly(ellipse(hx + dx * s + ex, hy - 3 * s, 5 * s, 6 * s, n=10), width=2.0, passes=1)
            dot(sh, hx + dx * s + ex * 1.4, hy - 2 * s, 1.6 * s)
    else:
        for dx in (-8, 8):
            dot(sh, hx + dx * s + ex, hy - 2 * s, 2.2 * s)
    m = hy + 9 * s
    if kind in ('smile', 'sleepy'):
        sh.line(ellipse(hx + ex, m - 2 * s, 8 * s, 5 * s, a0=0.3, a1=PI - 0.3, n=10), width=2.3, passes=1)
    elif kind == 'grin':
        sh.poly([(hx - 10 * s + ex, m - 2 * s)] + ellipse(hx + ex, m - 2 * s, 10 * s, 9 * s, a0=0, a1=PI, n=10), width=2.3, passes=1)
    elif kind in ('o', 'wide'):
        sh.poly(ellipse(hx + ex, m + 2 * s, 4 * s, 5 * s, n=10), width=2.2, passes=1)
    elif kind == 'flat':
        sh.line([(hx - 6 * s + ex, m + 1 * s), (hx + 6 * s + ex, m + 1 * s)], width=2.2, passes=1)
    elif kind == 'wavy':
        sh.line([(hx - 9 * s + ex + i * 3 * s, m + (2 if i % 2 else -1) * s) for i in range(7)], width=2.0, passes=1)
    if brows:
        for side in (-1, 1):
            bx = hx + side * 8 * s + ex
            if brows == 'angry':
                p, q = (bx - side * 6 * s, hy - 15 * s), (bx + side * 6 * s, hy - 10 * s)
                p, q = (bx - 6 * s, hy - (10 if side < 0 else 15) * s - 2 * s), (bx + 6 * s, hy - (15 if side < 0 else 10) * s - 2 * s)
                sh.line([p, q], width=3.4, passes=1)
            elif brows == 'up':
                sh.line(ellipse(bx, hy - 12 * s, 6 * s, 3 * s, a0=PI + 0.3, a1=2 * PI - 0.3, n=6), width=2.4, passes=1)
            elif brows == 'worried':
                p, q = (bx - 6 * s, hy - (15 if side < 0 else 11) * s), (bx + 6 * s, hy - (11 if side < 0 else 15) * s)
                sh.line([p, q], width=2.4, passes=1)


def hair(sh, hx, hy, r, s, style, facing=1):
    cap = ellipse(hx, hy, r * 1.04, r * 1.04, a0=PI + 0.12, a1=2 * PI - 0.12, n=16) + [(hx + r * 0.75, hy - r * 0.18), (hx, hy - r * 0.42), (hx - r * 0.75, hy - r * 0.18)]
    if style in ('scribble', 'bun', 'long'):
        sh.hatch(cap, angle=78, spacing=3.6 * s + 1.2, width=1.9)
    if style == 'bun':
        sh.poly(ellipse(hx + 4 * s, hy - r - 9 * s, 11 * s, 10 * s, n=12), width=2.2)
        sh.hatch(ellipse(hx + 4 * s, hy - r - 9 * s, 9 * s, 8 * s, n=10)[:-1], angle=40, spacing=3.5)
    if style == 'long':
        for side in (-1, 1):
            sh.line(bez((hx + side * r * 0.95, hy - r * 0.3), (hx + side * r * 1.25, hy + r * 0.6), (hx + side * r * 1.15, hy + r * 1.2), (hx + side * r * 1.3, hy + r * 1.7)), width=2.4)
    if style == 'curly':
        for a in range(195, 350, 22):
            sh.poly(ellipse(hx + r * math.cos(math.radians(a)), hy + r * math.sin(math.radians(a)), 7.5 * s, 7.5 * s, n=10), width=2.1, passes=1)
    if style == 'cap':
        sh.hatch(cap, angle=20, spacing=4.5, width=1.8)
        sh.poly(cap, width=2.3)
        sh.line([(hx + facing * r * 0.9, hy - r * 0.22), (hx + facing * (r + 26 * s), hy - r * 0.1)], width=3.2)
    if style == 'beanie':
        sh.poly(cap, width=2.3)
        sh.hatch(cap, angle=88, spacing=5, width=1.7)
        sh.poly(ellipse(hx, hy - r - 8 * s, 8 * s, 8 * s, n=10), width=2.2)
    if style == 'headband':
        sh.line(ellipse(hx, hy, r * 1.02, r * 0.5, a0=PI + 0.25, a1=2 * PI - 0.25, n=12), width=2.0, passes=1)
        sh.line(ellipse(hx, hy - 4 * s, r * 1.02, r * 0.62, a0=PI + 0.25, a1=2 * PI - 0.25, n=12), width=2.0, passes=1)
        for i in range(-3, 4):
            sh.line([(hx + i * 6 * s, hy - r * 0.95), (hx + i * 7 * s + 2 * s, hy - r * 1.25)], width=2.0, passes=1)
    if style == 'spiky':
        sh.line([(hx - r + i * r / 4, hy - r * (0.75 if i % 2 == 0 else 1.25)) for i in range(9)], width=2.4)
    if style == 'bald':
        sh.line(ellipse(hx - 6 * s, hy - 10 * s, r * 0.55, r * 0.6, a0=PI + 0.6, a1=PI + 1.4, n=6), width=1.8, passes=1)


def person(sh, x, y, s=1.0, arms=((-15, -8), (15, 8)), legs=((-6, -4), (6, 4)), face_kind='smile',
           hair_style='scribble', extras=(), lean=0.0, look=0, brows=None, facing=1, bib=None, stripes=False):
    """A sketchy bean-person standing on (x, y). Angles: 0 = straight down, +90 = to the right, 180 = up."""
    hip_y, neck_y = y - 95 * s, y - 168 * s
    hx, hy, r = x + lean * s, y - 198 * s, 25 * s
    if legs:
        for side, (a1, a2) in zip((-1, 1), legs):
            f = limb(sh, (x + side * 10 * s, hip_y), a1, 50 * s, a2, 46 * s, width=3.2, hand=False)
            sh.poly(ellipse(f[0] + facing * 7 * s, f[1] + 2 * s, 13 * s, 6 * s, n=12), width=2.4)
    tl, tr = (x - 23 * s + lean * 0.5 * s, neck_y + 4 * s), (x + 23 * s + lean * 0.5 * s, neck_y + 4 * s)
    bl, br = (x - 21 * s, hip_y + 4 * s), (x + 21 * s, hip_y + 4 * s)
    torso = bez(bl, (bl[0] - 4 * s, bl[1] - 30 * s), (tl[0] - 8 * s, tl[1] + 20 * s), tl) + [tr] + \
        bez(tr, (tr[0] + 8 * s, tr[1] + 20 * s), (br[0] + 4 * s, br[1] - 30 * s), br)[1:]
    sh.poly(torso)
    if stripes:
        for k in range(1, 5):
            yy = neck_y + 4 * s + k * (hip_y - neck_y) / 5
            sh.line([(x - 21 * s, yy), (x + 21 * s, yy + 2 * s)], width=1.8, passes=1)
    if 'apron' in extras:
        ap = [(x - 18 * s, neck_y + 34 * s), (x + 18 * s, neck_y + 34 * s), (x + 22 * s, hip_y + 34 * s), (x - 22 * s, hip_y + 34 * s)]
        sh.poly(ap, width=2.3)
        sh.line([(x - 18 * s, neck_y + 34 * s), (x - 8 * s, neck_y + 6 * s)], width=1.8, passes=1)
        sh.line([(x + 18 * s, neck_y + 34 * s), (x + 8 * s, neck_y + 6 * s)], width=1.8, passes=1)
        sh.poly(rrect(x - 9 * s, neck_y + 52 * s, 18 * s, 14 * s, 3 * s), width=1.8, passes=1)
    if 'tie' in extras:
        sh.poly([(x, neck_y + 8 * s), (x - 5 * s, neck_y + 16 * s), (x, neck_y + 50 * s), (x + 5 * s, neck_y + 16 * s)], width=2.0)
    if 'bowtie' in extras:
        by = neck_y + 10 * s
        sh.poly([(x, by), (x - 14 * s, by - 8 * s), (x - 14 * s, by + 8 * s)], width=2.2)
        sh.poly([(x, by), (x + 14 * s, by - 8 * s), (x + 14 * s, by + 8 * s)], width=2.2)
    if bib:
        sh.poly(rrect(x - 15 * s, neck_y + 22 * s, 30 * s, 26 * s, 3 * s), width=2.0)
        sh.text(bib, x, neck_y + 43 * s, size=17 * s, anchor='middle', width=1.8)
    if 'tote' in extras:
        sx = x - facing * 21 * s
        sh.poly(rrect(sx - 18 * s, hip_y - 26 * s, 36 * s, 42 * s, 4 * s), width=2.3)
        sh.line([(sx - 12 * s, hip_y - 26 * s), (x - facing * 14 * s, neck_y + 6 * s), (sx + 12 * s, hip_y - 26 * s)], width=2.0, passes=1)
    sh.line([(hx - 6 * s, hy + r - 2 * s), (x - 6 * s + lean * 0.5 * s, neck_y + 4 * s)], width=2.2, passes=1)
    sh.line([(hx + 6 * s, hy + r - 2 * s), (x + 6 * s + lean * 0.5 * s, neck_y + 4 * s)], width=2.2, passes=1)
    sh.poly(ellipse(hx, hy, r * 0.95, r, n=28))
    face(sh, hx, hy, s, face_kind, look=look, brows=brows)
    hair(sh, hx, hy, r, s, hair_style, facing=facing)
    if 'glasses' in extras:
        for dx in (-9, 9):
            sh.poly(ellipse(hx + dx * s + look * 3 * s, hy - 2 * s, 7 * s, 6 * s, n=12), width=1.9, passes=1)
        sh.line([(hx - 2 * s, hy - 3 * s), (hx + 2 * s, hy - 3 * s)], width=1.8, passes=1)
    if 'mustache' in extras:
        my = hy + 5 * s
        sh.line(bez((hx, my), (hx - 6 * s, my - 4 * s), (hx - 16 * s, my + 2 * s), (hx - 18 * s, my - 6 * s)), width=2.6, passes=1)
        sh.line(bez((hx, my), (hx + 6 * s, my - 4 * s), (hx + 16 * s, my + 2 * s), (hx + 18 * s, my - 6 * s)), width=2.6, passes=1)
    if 'sweat' in extras:
        sweat(sh, hx + facing * (r + 8 * s), hy - 12 * s, s)
        sweat(sh, hx - facing * (r + 6 * s), hy - 2 * s, s * 0.8)
    hands = []
    for side, (a1, a2) in zip((-1, 1), arms):
        sp = (x + side * 21 * s + lean * 0.5 * s, neck_y + 14 * s)
        hands.append(limb(sh, sp, a1, 36 * s, a2, 34 * s, width=3.0, hr=6 * s))
    return {'hands': hands, 'head': (hx, hy, r)}


def bust(sh, x, y, s=1.0, **kw):
    """Head and shoulders only (for crowds and tables). (x, y) = bottom centre of the shoulders."""
    hx, hy, r = x, y - 62 * s, 25 * s
    sh.line(bez((x - 34 * s, y), (x - 34 * s, y - 30 * s), (x - 20 * s, y - 34 * s), (x - 8 * s, y - 36 * s)) +
            [(x + 8 * s, y - 36 * s)] + bez((x + 8 * s, y - 36 * s), (x + 20 * s, y - 34 * s), (x + 34 * s, y - 30 * s), (x + 34 * s, y))[1:], width=2.6)
    sh.poly(ellipse(hx, hy, r * 0.95, r, n=24))
    face(sh, hx, hy, s, kw.get('face_kind', 'smile'), look=kw.get('look', 0), brows=kw.get('brows'))
    hair(sh, hx, hy, r, s, kw.get('hair_style', 'scribble'), facing=kw.get('facing', 1))
    return (hx, hy, r)


# ---------------------------------------------------------------------------
# chickens and eggs
# ---------------------------------------------------------------------------
def chicken(sh, cx, cy, k=1.0, f=-1, hat=False, bowtie=False, monocle=False, legs=True, eye='dot'):
    """f = -1 faces left, +1 faces right. (cx, cy) = body centre."""
    sh.poly(ellipse(cx, cy, 120 * k, 92 * k, rot=-0.22 * f, n=40))
    for i in range(3):
        bx, by = cx - f * 100 * k, cy - 40 * k + i * 22 * k
        sh.line(bez((bx, by), (bx - f * 60 * k, by - 50 * k), (bx - f * 90 * k, by - 20 * k), (bx - f * 40 * k, by + 10 * k)), width=2.4)
    for i in range(4):
        wx = cx - f * (10 - i * 20) * k
        sh.line(ellipse(wx, cy + 10 * k, 22 * k, 30 * k, a0=0.1, a1=PI - 0.1, n=8), width=2.0, passes=1)
    sh.hatch([(cx - 50 * k, cy + 40 * k), (cx + 50 * k, cy + 40 * k), (cx + 40 * k, cy + 80 * k), (cx - 40 * k, cy + 80 * k)], angle=70, spacing=6)
    hx, hy = cx + f * 80 * k, cy - 115 * k
    sh.line([(hx - f * 34 * k, hy + 34 * k), (cx + f * 10 * k, cy - 70 * k)], width=2.4)
    sh.poly(ellipse(hx, hy, 44 * k, 48 * k, n=28))
    for i, dx in enumerate((-22, 0, 22)):
        sh.poly(ellipse(hx + dx * k - f * 6 * k, hy - 52 * k - (6 if i == 1 else 0) * k, 14 * k, 16 * k, n=12), width=2.2)
    sh.poly([(hx + f * 38 * k, hy - 4 * k), (hx + f * 76 * k, hy + 8 * k), (hx + f * 38 * k, hy + 20 * k)], width=2.4)
    sh.poly(ellipse(hx + f * 40 * k, hy + 38 * k, 8 * k, 14 * k, n=12), width=2.0)
    ex, ey = hx + f * 14 * k, hy - 10 * k
    if eye == 'dot':
        dot(sh, ex, ey, 3.4 * k)
    else:
        sh.poly(ellipse(ex, ey, 7 * k, 8 * k, n=10), width=2.0, passes=1)
        dot(sh, ex + f * 2 * k, ey, 2.4 * k)
    if monocle:
        sh.poly(ellipse(ex, ey, 14 * k, 14 * k, n=16), width=2.3)
        sh.line(bez((ex, ey + 14 * k), (ex - f * 10 * k, ey + 50 * k), (ex - f * 30 * k, ey + 60 * k), (ex - f * 34 * k, ey + 90 * k)), width=1.6, passes=1)
    if bowtie:
        bx, by = hx - f * 4 * k, hy + 50 * k
        sh.poly([(bx, by), (bx - 22 * k, by - 12 * k), (bx - 22 * k, by + 12 * k)], width=2.3)
        sh.poly([(bx, by), (bx + 22 * k, by - 12 * k), (bx + 22 * k, by + 12 * k)], width=2.3)
        sh.hatch([(bx - 20 * k, by - 9 * k), (bx - 4 * k, by - 2 * k), (bx - 4 * k, by + 2 * k), (bx - 20 * k, by + 9 * k)], angle=80, spacing=4)
    if hat:
        tip = (hx - f * 8 * k, hy - 130 * k)
        sh.poly([(hx - 30 * k, hy - 52 * k), tip, (hx + 22 * k, hy - 56 * k)], width=2.4)
        sh.poly(ellipse(tip[0], tip[1] - 8 * k, 9 * k, 9 * k, n=10), width=2.0)
        sh.line([(hx - 18 * k, hy - 80 * k), (hx + 8 * k, hy - 90 * k)], width=1.8, passes=1)
        sh.line([(hx - 10 * k, hy - 104 * k), (hx + 2 * k, hy - 110 * k)], width=1.8, passes=1)
    if legs:
        for dx in (-22, 22):
            lx, ly = cx + dx * k, cy + 88 * k
            sh.line([(lx, ly), (lx, ly + 70 * k)], width=2.6)
            for a in (-35, 0, 35):
                d = dirv(180 - a + 90 * f * 0)  # toes point down-forward
                sh.line([(lx, ly + 70 * k), (lx + f * 24 * k * math.cos(math.radians(a)), ly + 70 * k + 8 * k * math.sin(math.radians(a)) + 4 * k)], width=2.2, passes=1)
    return (hx, hy)


def eggbert(sh, cx, cy, k=1.0, face_kind='smile', arms=((-60, -30), (60, 30)), legs=((-10, -10), (10, 10)), extras=()):
    """The egg mascot. (cx, cy) = egg centre."""
    sh.poly(egg(cx, cy, k)[:-1])
    face(sh, cx, cy - 20 * k, k * 1.6, face_kind)
    hands = []
    for side, (a1, a2) in zip((-1, 1), arms):
        hands.append(limb(sh, (cx + side * 70 * k, cy + 10 * k), a1, 34 * k, a2, 30 * k, width=2.8, hr=7 * k))
    for side, (a1, a2) in zip((-1, 1), legs):
        f = limb(sh, (cx + side * 28 * k, cy + 102 * k), a1, 30 * k, a2, 26 * k, width=3.0, hand=False)
        sh.poly(ellipse(f[0] + side * 8 * k, f[1] + 2 * k, 14 * k, 6 * k, n=10), width=2.3)
    if 'headband' in extras:
        sh.line(ellipse(cx, cy - 40 * k, 62 * k, 14 * k, a0=PI + 0.15, a1=2 * PI - 0.15, n=12), width=2.2, passes=1)
        sh.line(ellipse(cx, cy - 52 * k, 58 * k, 14 * k, a0=PI + 0.15, a1=2 * PI - 0.15, n=12), width=2.2, passes=1)
    if 'crack' in extras:
        sh.line([(cx - 40 * k, cy - 70 * k), (cx - 26 * k, cy - 58 * k), (cx - 30 * k, cy - 48 * k), (cx - 16 * k, cy - 40 * k)], width=2.0, passes=1)
    return hands


# ---------------------------------------------------------------------------
# the sheets
# ---------------------------------------------------------------------------
def s_matched():
    sh = Sheet(301)
    a = person(sh, 380, 840, s=2.0, arms=((-12, -6), (62, 95)), legs=((-4, -2), (4, 2)), face_kind='grin',
               hair_style='bald', extras=('apron', 'mustache'), facing=1, look=1)
    b = person(sh, 720, 840, s=2.0, arms=((-62, -95), (14, 150)), legs=((-4, -2), (4, 2)), face_kind='grin',
               hair_style='bun', extras=('tote', 'glasses'), facing=-1, look=-1)
    hx, hy = b['hands'][1]
    sh.poly(rotate(rrect(hx - 30, hy - 70, 60, 80, 5), hx, hy, 0.2), width=2.4)
    for i in range(3):
        sh.line(rotate([(hx - 18, hy - 50 + i * 16), (hx + 18, hy - 50 + i * 16)], hx, hy, 0.2), width=1.8, passes=1)
    heart(sh, 550, 300, 1.6)
    for x, y in ((450, 250), (660, 230), (620, 380), (470, 380)):
        sparkle(sh, x, y, 1.1)
    motion(sh, 520, 520, n=2, length=26, gap=16, angle=-1.2)
    motion(sh, 600, 520, n=2, length=26, gap=16, angle=-1.9)
    sh.text('MATCHED!', 550, 140, size=52, anchor='middle', width=3.0)
    sh.text('THE VENUE', 300, 920, size=22)
    sh.text('THE CLUB', 650, 920, size=22)
    sh.text('(TUE OK?)', 120, 470, size=20, rot=-0.06)
    sh.text('(TUE OK!)', 860, 470, size=20, rot=0.06)
    return sh


def s_host():
    sh = Sheet(313)
    sh.poly([(150, 560), (290, 560), (300, 880), (140, 880)])
    sh.text('HOST', 220, 640, size=26, anchor='middle')
    sh.hatch([(290, 562), (300, 880), (282, 880), (276, 570)], angle=80, spacing=5)
    chicken(sh, 430, 600, k=1.25, f=1, bowtie=True, monocle=True, eye='big')
    sh.poly(rotate(rrect(470, 560, 90, 120, 6), 515, 620, -0.25))
    sh.text('MENU', 492, 618, size=18, rot=-0.25, width=1.8)
    bubble(sh, 760, 210, 240, 85, (620, 380), ['TABLE FOR 20?', 'RIGHT THIS WAY'], size=28)
    person(sh, 790, 880, s=1.0, arms=((-15, -8), (40, 140)), face_kind='o', hair_style='curly', facing=-1, look=-1)
    person(sh, 900, 880, s=1.05, arms=((-20, -10), (20, 10)), face_kind='smile', hair_style='long', facing=-1, look=-1, extras=('glasses',))
    person(sh, 1000, 880, s=0.95, arms=((-10, -5), (150, 175)), face_kind='grin', hair_style='cap', facing=-1, look=-1)
    sh.line([(100, 882), (1060, 882)], width=2.2)
    sh.text('THE HOST', 60, 110, size=36, rot=-0.02)
    return sh


def s_conga():
    sh = Sheet(327)
    sh.poly([(890, 360), (1050, 360), (1050, 870), (890, 870)])
    sh.poly([(906, 380), (1034, 380), (1034, 870), (906, 870)], width=2.0)
    sh.hatch([(906, 380), (1034, 380), (1034, 870), (906, 870)], angle=60, spacing=7)
    sh.poly(rrect(860, 280, 220, 54, 6))
    sh.text('THE LOCAL', 970, 318, size=26, anchor='middle')
    sh.line([(40, 872), (1070, 872)], width=2.2)
    crew = [
        (140, 'headband', 'grin', 'run'),
        (290, 'long', 'smile', 'book'),
        (440, 'beanie', 'grin', 'yarn'),
        (590, 'curly', 'o', 'chess'),
        (740, 'spiky', 'grin', 'pen'),
    ]
    for i, (x, h, fk, prop) in enumerate(crew):
        stride = 1 if i % 2 == 0 else -1
        legs = ((-28 * stride, -10 * stride), (28 * stride, 12 * stride))
        p = person(sh, x, 860, s=1.4, arms=((-30, -60), (80, 86)), legs=legs, face_kind=fk, hair_style=h,
                   facing=1, look=1, lean=6, bib='12' if prop == 'run' else None)
        lx, ly = p['hands'][0]
        if prop == 'book':
            sh.poly(rotate(rrect(lx - 24, ly - 6, 48, 34, 3), lx, ly, -0.3), width=2.3)
            sh.line(rotate([(lx, ly - 6), (lx, ly + 28)], lx, ly, -0.3), width=1.8, passes=1)
        elif prop == 'yarn':
            sh.poly(ellipse(lx - 10, ly + 20, 18, 18, n=14), width=2.3)
            sh.line(bez((lx - 10, ly + 38), (lx - 60, ly + 80), (lx - 120, ly + 40), (lx - 170, ly + 90)), width=1.8, passes=1)
        elif prop == 'chess':
            sh.poly(rotate([(lx - 34, ly), (lx + 20, ly), (lx + 20, ly + 10), (lx - 34, ly + 10)], lx, ly, -0.4), width=2.3)
        elif prop == 'pen':
            sh.line([(lx - 6, ly + 20), (lx + 20, ly - 30)], width=3.0)
        motion(sh, x - 70, 760, n=3, length=30, gap=16)
    sh.text('EVERY TUESDAY', 260, 180, size=44, rot=-0.03, width=2.8)
    sh.arrow(bez((640, 170), (760, 160), (840, 200), (880, 260)))
    sh.text('CONGA IS OPTIONAL', 300, 240, size=20, rot=-0.03, width=1.8)
    return sh


def s_before_after():
    sh = Sheet(339)
    for x0, label in ((60, 'BEFORE'), (570, 'AFTER')):
        sh.poly([(x0, 160), (x0 + 470, 160), (x0 + 470, 860), (x0, 860)], width=2.4)
        sh.text(label, x0 + (100 if label == 'BEFORE' else 18), 210, size=30)
        sh.poly([(x0 + 20, 640), (x0 + 450, 640), (x0 + 450, 680), (x0 + 20, 680)], width=2.4)
        sh.line([(x0 + 30, 680), (x0 + 30, 860)], width=2.0, passes=1)
        sh.line([(x0 + 440, 680), (x0 + 440, 860)], width=2.0, passes=1)
    # before: lonely bartender, tumbleweed, cobweb, clock
    bt = person(sh, 300, 780, s=1.5, arms=((-40, 60), (40, -60)), legs=None, face_kind='flat', hair_style='bald',
                extras=('apron', 'mustache'), brows='worried')
    gx = (bt['hands'][0][0] + bt['hands'][1][0]) / 2
    gy = (bt['hands'][0][1] + bt['hands'][1][1]) / 2
    sh.poly(ellipse(gx, gy - 6, 14, 22, n=14), width=2.0)
    for k in range(3):
        sh.poly(ellipse(150, 820, 30 - k * 8, 26 - k * 7, rot=k, n=16), width=1.8, passes=1)
    sh.line([(150, 846), (130, 850)], width=1.6, passes=1)
    motion(sh, 110, 820, n=3, length=30, gap=12)
    for k in range(4):
        sh.line([(60, 160), (60 + 70 * math.cos(k * 0.45), 160 + 70 * math.sin(k * 0.45))], width=1.4, passes=1)
    for rr in (22, 44, 66):
        sh.line([(60 + rr * math.cos(t * 0.45), 160 + rr * math.sin(t * 0.45)) for t in range(4)], width=1.4, passes=1)
    sh.poly(ellipse(460, 280, 36, 36, n=24), width=2.2)
    sh.line([(460, 280), (460, 254), (460, 280), (480, 288)], width=2.0, passes=1)
    sh.text('TUE 7PM', 380, 350, size=18)
    sh.text('CHIRP', 200, 440, size=18, rot=-0.2, width=1.6)
    sh.text('CHIRP', 400, 500, size=16, rot=0.15, width=1.6)
    # after: a crowd at the bar
    person(sh, 810, 780, s=1.5, arms=((-150, -175), (150, 175)), legs=None, face_kind='grin', hair_style='bald',
           extras=('apron', 'mustache', 'sweat'))
    heads = [(620, 'curly', 'grin'), (680, 'bun', 'smile'), (740, 'cap', 'o'), (880, 'long', 'grin'), (940, 'headband', 'smile'), (1000, 'spiky', 'grin')]
    for i, (x, hs, fk) in enumerate(heads):
        bust(sh, x, 760 + (i % 2) * 40, s=1.05, hair_style=hs, face_kind=fk, look=1 if x < 810 else -1)
    for x in (660, 760, 900):
        sh.poly(ellipse(x, 636, 26, 6, n=14), width=2.0, passes=1)
    for x, y in ((640, 330), (990, 360)):
        sh.line([(x, y), (x, y - 40), (x + 22, y - 48), (x + 22, y - 10)], width=2.2, passes=1)
        sh.poly(ellipse(x - 6, y, 7, 5, n=8), width=2.2, passes=1)
        sh.poly(ellipse(x + 16, y - 10, 7, 5, n=8), width=2.2, passes=1)
    bubble(sh, 660, 470, 72, 34, (650, 640), ['HOLA!'], size=22)
    sh.text('SAME BAR. SAME TUESDAY.', 300, 110, size=28, rot=-0.01)
    return sh


def s_living_room():
    sh = Sheet(353)
    sh.poly(rrect(200, 480, 700, 260, 40))
    sh.poly(rrect(160, 560, 80, 230, 30))
    sh.poly(rrect(860, 560, 80, 230, 30))
    sh.line([(240, 640), (860, 640)], width=2.2)
    sh.line([(230, 790), (220, 840)], width=2.6)
    sh.line([(870, 790), (880, 840)], width=2.6)
    sh.hatch([(240, 660), (860, 660), (860, 740), (240, 740)], angle=20, spacing=10, width=1.4)
    crowd = [(270, 'curly', 'o'), (340, 'long', 'flat'), (410, 'bun', 'wavy'), (480, 'cap', 'o'), (550, 'spiky', 'flat'),
             (620, 'headband', 'wavy'), (690, 'scribble', 'o'), (760, 'long', 'flat'), (830, 'beanie', 'wavy')]
    for i, (x, hs, fk) in enumerate(crowd):
        bust(sh, x, 640 - (i % 2) * 14, s=1.1, hair_style=hs, face_kind=fk, brows='worried' if i % 3 == 0 else None)
    bust(sh, 200, 560, s=1.0, hair_style='spiky', face_kind='o')
    bust(sh, 560, 860, s=1.0, hair_style='scribble', face_kind='flat')
    # cat on a head
    cx, cy = 480, 520
    sh.poly(ellipse(cx, cy, 34, 20, n=20), width=2.3)
    sh.poly(ellipse(cx + 30, cy - 14, 16, 15, n=14), width=2.3)
    sh.line([(cx + 20, cy - 26), (cx + 24, cy - 42), (cx + 32, cy - 28), (cx + 38, cy - 42), (cx + 42, cy - 24)], width=2.0, passes=1)
    sh.line(bez((cx - 34, cy), (cx - 60, cy - 10), (cx - 60, cy - 40), (cx - 44, cy - 50)), width=2.0, passes=1)
    sh.line([(cx + 25, cy - 16), (cx + 29, cy - 14)], width=2.0, passes=1)
    # books on laps
    for x in (340, 620, 760):
        sh.poly([(x - 22, 650), (x + 22, 650), (x + 22, 668), (x - 22, 668)], width=2.0, passes=1)
    sh.poly(ellipse(980, 400, 40, 40, n=24), width=2.2)
    sh.line([(980, 400), (980, 374), (980, 400), (998, 412)], width=2.0, passes=1)
    bubble(sh, 830, 230, 140, 54, (760, 520), ['MY KNEES'], size=26)
    sh.text('BOOK CLUB. LIVING ROOM.', 70, 110, size=32, rot=-0.02)
    sh.text('AGAIN.', 74, 160, size=32, rot=-0.02)
    sh.text('WE CAN FIX THIS', 140, 920, size=24, rot=-0.02)
    return sh


def s_run_club():
    sh = Sheet(367)
    sh.poly([(40, 300), (180, 300), (180, 880), (40, 880)], width=2.4)
    sh.line([(180, 300), (240, 330), (240, 860), (180, 880)], width=2.2)
    sh.line([(40, 882), (1060, 882)], width=2.2)
    runners = [(320, 'headband', '7', 'grin'), (470, 'bun', '12', 'grin'), (620, 'spiky', '31', 'wide')]
    for i, (x, hs, num, fk) in enumerate(runners):
        stride = 1 if i % 2 == 0 else -1
        person(sh, x, 870, s=1.55, arms=((-60 * stride, -100 * stride), (60 * stride, 120 * stride)),
               legs=((-40 * stride, -10 * stride), (40 * stride, 30 * stride)), face_kind=fk, hair_style=hs,
               lean=26, facing=1, look=1, bib=num, extras=('sweat',))
        motion(sh, x - 90, 600, n=4, length=50, gap=24)
    # the waiter, terrified, tray of pasta held high
    p = person(sh, 930, 870, s=1.6, arms=((-150, -172), (40, 20)), face_kind='wide', hair_style='scribble',
               extras=('bowtie',), facing=-1, look=-1, brows='up')
    tx, ty = p['hands'][0]
    sh.poly(ellipse(tx, ty - 6, 90, 14, n=28), width=2.4)
    for dx in (-50, 0, 50):
        sh.line(bez((tx + dx - 26, ty - 10), (tx + dx - 20, ty - 46), (tx + dx + 20, ty - 46), (tx + dx + 26, ty - 10)), width=2.2)
        sh.line([(tx + dx - 12 + 4 * math.sin(t / 3), ty - 30 - t) for t in range(0, 30, 3)], width=1.6, passes=1)
    bubble(sh, 470, 210, 210, 74, (480, 500), ['5K DONE.', 'FEED US.'], size=30)
    sh.text('RUN CLUB ARRIVES', 60, 90, size=30, rot=-0.02)
    sh.text('!!', 860, 520, size=36)
    return sh


def s_brain():
    sh = Sheet(379)
    # left: side profile, top open, chaos inside
    prof = (bez((360, 860), (360, 760), (380, 700), (330, 650)) + bez((330, 650), (300, 620), (300, 600), (320, 590))[1:]
            + [(300, 560), (330, 540), (320, 470)] + bez((320, 470), (320, 380), (400, 330), (480, 340))[1:]
            + bez((480, 340), (570, 350), (600, 430), (590, 520))[1:] + bez((590, 520), (580, 600), (540, 650), (520, 720))[1:]
            + [(530, 860)])
    sh.line(prof, width=2.8)
    dot(sh, 360, 450, 3)
    sh.line(ellipse(360, 430, 14, 6, a0=PI + 0.4, a1=2 * PI - 0.4, n=6), width=2.4, passes=1)
    sh.line([(330, 520), (345, 528)], width=2.4, passes=1)
    # chaos cloud
    chaos = ['DM?', '??', 'WHERE?', 'TUE?', '15 BARS']
    for i, t in enumerate(chaos):
        a = -PI / 2 + (i - 2) * 0.62
        sh.text(t, 450 + 220 * math.cos(a) - 30, 270 + 140 * math.sin(a), size=22, rot=(i - 2) * 0.15)
    sh.line([(400 + 60 * math.cos(t / 3) + t * 1.5, 300 + 40 * math.sin(t / 2.2)) for t in range(0, 80)], width=1.6, passes=1)
    for x, y in ((300, 230), (610, 240), (540, 140)):
        sh.poly(rrect(x - 16, y - 26, 32, 52, 6), width=2.0, passes=1)
        sh.line([(x - 6, y + 18), (x + 6, y + 18)], width=1.6, passes=1)
    sh.text('BEFORE', 360, 920, size=24)
    sh.arrow(bez((620, 600), (680, 560), (720, 560), (760, 600)))
    # right: calm face, one checked box
    bust(sh, 880, 760, s=2.4, face_kind='sleepy', hair_style='bun')
    sh.poly([(820, 360), (860, 360), (860, 400), (820, 400)], width=2.4)
    sh.line([(826, 380), (838, 394), (868, 352)], width=3.0)
    sh.text('TUE 7PM', 880, 395, size=28)
    sh.text('AFTER', 840, 920, size=24)
    sh.text("THE ORGANIZER'S BRAIN", 60, 90, size=28, rot=-0.02)
    return sh


def s_flock():
    sh = Sheet(391)
    sh.poly([(80, 660), (1020, 660), (1020, 690), (80, 690)])
    sh.line([(120, 690), (110, 880)], width=2.6)
    sh.line([(980, 690), (990, 880)], width=2.6)
    for i, x in enumerate((200, 420, 680, 900)):
        chicken(sh, x, 580, k=0.58, f=1 if i < 2 else -1, hat=True, legs=False, eye='big' if i % 2 else 'dot')
    for x in (310, 550, 790):
        sh.poly(ellipse(x, 652, 50, 9, n=20), width=2.2)
        for k in range(5):
            sh.poly(ellipse(x - 24 + k * 12, 644, 5, 4, n=6), width=1.6, passes=1)
    sh.poly(rotate(rrect(470, 610, 50, 36, 3), 495, 628, 0.2), width=2.1)
    sh.poly(rrect(290, 120, 520, 70, 8))
    sh.text('EVERY FLOCK NEEDS ONE', 550, 168, size=26, anchor='middle')
    sh.line([(340, 190), (320, 250)], width=1.8, passes=1)
    sh.line([(760, 190), (780, 250)], width=1.8, passes=1)
    for x, y in ((150, 200), (950, 230), (300, 330), (820, 330)):
        sparkle(sh, x, y, 1.0)
    sh.text('THE FLOCK', 60, 90, size=32, rot=-0.02)
    sh.text('CORN, FAMILY STYLE', 640, 920, size=20)
    return sh


def s_eggbert():
    sh = Sheet(403)
    poses = [
        (190, 330, 'WAVING', dict(face_kind='grin', arms=((-60, -30), (150, 175)))),
        (550, 330, 'RUN CLUB', dict(face_kind='grin', arms=((-110, -150), (110, 60)), legs=((-40, -10), (40, 10)), extras=('headband',))),
        (910, 330, 'BOOK CLUB', dict(face_kind='smile', arms=((-40, 60), (40, -60)))),
        (190, 720, 'QUIET TUESDAY', dict(face_kind='sleepy', arms=((-20, -10), (20, 10)), extras=('crack',))),
        (550, 720, 'GAME NIGHT', dict(face_kind='o', arms=((-80, -120), (80, 120)))),
        (910, 720, 'SUPPER CLUB', dict(face_kind='grin', arms=((-150, -170), (40, 60)))),
    ]
    for cx, cy, label, kw in poses:
        hands = eggbert(sh, cx, cy - 20, k=0.85, **kw)
        sh.text(label, cx, cy + 150, size=20, anchor='middle')
        if label == 'BOOK CLUB':
            sh.poly([(cx - 40, cy + 20), (cx, cy + 30), (cx + 40, cy + 20), (cx + 40, cy + 60), (cx, cy + 70), (cx - 40, cy + 60)], width=2.3)
            sh.line([(cx, cy + 30), (cx, cy + 70)], width=1.8, passes=1)
        if label == 'QUIET TUESDAY':
            sh.text('Z', cx + 70, cy - 110, size=26)
            sh.text('Z', cx + 96, cy - 140, size=20)
            sh.text('Z', cx + 116, cy - 162, size=14)
        if label == 'GAME NIGHT':
            pawn(sh, cx + 90, cy + 110, k=0.5, shade=False)
        if label == 'SUPPER CLUB':
            hx, hy = hands[0]
            sh.poly(ellipse(hx, hy - 8, 46, 9, n=18), width=2.2)
            sh.line(bez((hx - 30, hy - 12), (hx - 20, hy - 46), (hx + 20, hy - 46), (hx + 30, hy - 12)), width=2.2)
        if label == 'RUN CLUB':
            motion(sh, cx - 110, cy - 10, n=3, length=40, gap=18)
    sh.text('MEET EGGBERT?', 60, 90, size=32, rot=-0.02)
    sh.text('(NAME PENDING)', 410, 94, size=20, rot=-0.02, width=1.8)
    return sh


def s_tangled():
    sh = Sheet(419)
    seats = [(250, 520, 1), (850, 520, -1), (400, 860, 1), (700, 860, -1)]
    hands = []
    for i, (x, y, f) in enumerate(seats):
        if y < 700:
            p = person(sh, x, y + 210, s=1.25, arms=((-50 * f, -90 * f), (60 * f, 100 * f)), legs=None,
                       face_kind=['o', 'grin', 'wavy', 'smile'][i], hair_style=['bun', 'beanie', 'curly', 'long'][i], facing=f, look=f)
            hands += p['hands']
        else:
            hx, hy, r = bust(sh, x, y, s=1.25, hair_style=['bun', 'beanie', 'curly', 'long'][i], face_kind=['o', 'grin', 'wavy', 'grin'][i], look=f)
            hands += [(x - 30, y - 20), (x + 30, y - 20)]
    cx, cy = 550, 560
    for k in range(10):
        sh.poly(ellipse(cx + 6 * math.sin(k), cy + 5 * math.cos(k * 1.3), 70 - k * 5, 52 - k * 3, rot=k * 0.6, n=24), width=1.7, passes=1)
    for (hx, hy) in hands:
        mid = ((hx + cx) / 2 + 40 * math.sin(hx), (hy + cy) / 2 - 60)
        sh.line(bez((hx, hy), mid, (cx + 30 * math.cos(hy), cy - 30), (cx, cy)), width=1.7, passes=1)
    for (hx, hy) in hands[:4]:
        sh.line([(hx - 20, hy - 30), (hx + 18, hy + 20)], width=2.6)
    sh.line(bez((120, 760), (300, 600), (180, 380), (380, 300)), width=1.7, passes=1)
    sh.text('CRAFT NIGHT', 60, 100, size=34, rot=-0.02)
    sh.text('GOING GREAT', 64, 150, size=24, rot=-0.02, width=1.9)
    sh.text('HELP', 780, 330, size=22, rot=0.1)
    return sh


def s_chart():
    sh = Sheet(431)
    x0, y0 = 160, 820
    sh.arrow([(x0, y0), (x0, 170)])
    sh.arrow([(x0, y0), (1000, y0)])
    bars = [('MON', 90), ('TUE', 470), ('WED', 120), ('THU', 160), ('FRI', 300)]
    for i, (d, h) in enumerate(bars):
        bx = x0 + 60 + i * 160
        sh.poly([(bx, y0), (bx + 90, y0), (bx + 90, y0 - h), (bx, y0 - h)], width=2.6)
        if d != 'TUE':
            sh.hatch([(bx, y0), (bx + 90, y0), (bx + 90, y0 - h), (bx, y0 - h)], angle=60, spacing=8)
        sh.text(d, bx + 45, y0 + 40, size=22, anchor='middle')
    bx = x0 + 60 + 160
    # ladder + climber + flag
    sh.line([(bx - 60, y0), (bx - 10, y0 - 300)], width=2.4)
    sh.line([(bx - 30, y0), (bx + 20, y0 - 300)], width=2.4)
    for k in range(1, 8):
        t = k / 8
        sh.line([(bx - 60 + 50 * t, y0 - 300 * t), (bx - 30 + 50 * t, y0 - 300 * t)], width=2.0, passes=1)
    person(sh, bx + 45, y0 - 470, s=0.95, arms=((-150, -175), (60, 20)), face_kind='grin', hair_style='bald', extras=('apron', 'mustache'))
    sh.line([(bx + 70, y0 - 470), (bx + 74, y0 - 640)], width=2.4)
    sh.poly([(bx + 74, y0 - 640), (bx + 160, y0 - 620), (bx + 72, y0 - 596)], width=2.2)
    sh.text('COOP', bx + 82, y0 - 612, size=16, width=1.6)
    sh.text('TUESDAYS, BEFORE AND AFTER', 260, 100, size=26, rot=-0.01)
    sh.text('ILLUSTRATIVE, NOT A FORECAST', 520, 900, size=18, width=1.6)
    return sh


def s_chess_faceoff():
    sh = Sheet(443)
    sh.poly([(330, 620), (770, 620), (770, 650), (330, 650)])
    sh.line([(380, 650), (370, 880)], width=2.6)
    sh.line([(720, 650), (730, 880)], width=2.6)
    cam = Cam(0, 60, 1.6, 550, 600, D=900)
    box(sh, cam, -50, -50, 0, 100, 100, 6, shade=0.3, spacing=5)
    for i, j in ((0, 0), (2, 0), (1, 1), (3, 1), (0, 2), (2, 2), (1, 3), (3, 3)):
        q = [cam.P((-50 + i * 25, -50 + j * 25, 6.1)), cam.P((-25 + i * 25, -50 + j * 25, 6.1)), cam.P((-25 + i * 25, -25 + j * 25, 6.1)), cam.P((-50 + i * 25, -25 + j * 25, 6.1))]
        sh.hatch(q, angle=45, spacing=4, width=1.5)
    pawn(sh, 520, 560, k=0.35, shade=False)
    pawn(sh, 590, 548, k=0.35, shade=False)
    person(sh, 250, 880, s=1.7, arms=((-20, -10), (40, 100)), legs=((10, 0), (30, 0)), face_kind='flat', hair_style='spiky',
           brows='angry', facing=1, look=1, extras=('sweat',))
    person(sh, 850, 880, s=1.7, arms=((-40, -100), (20, 10)), legs=((-30, 0), (-10, 0)), face_kind='flat', hair_style='long',
           brows='angry', facing=-1, look=-1, extras=('glasses', 'sweat'))
    sh.line([(330, 520), (380, 490), (360, 510), (420, 470), (400, 492), (720, 470), (700, 492), (770, 520)], width=2.2, passes=1)
    for x in (230, 270, 830, 870):
        sh.line([(x + 6 * math.sin(t / 6), 470 - t) for t in range(0, 60, 4)], width=1.6, passes=1)
    # spectator with popcorn
    p = bust(sh, 1010, 700, s=1.0, hair_style='cap', face_kind='o', look=-1)
    sh.poly([(950, 730), (990, 730), (984, 780), (956, 780)], width=2.2)
    for k in range(5):
        sh.poly(ellipse(955 + k * 8, 724 - (k % 2) * 6, 6, 5, n=8), width=1.6, passes=1)
    sh.text('GAME NIGHT', 60, 100, size=34, rot=-0.02)
    sh.text('GETS SERIOUS', 64, 150, size=24, rot=-0.02, width=1.9)
    return sh


SHEETS = {
    'matched': s_matched,
    'the-host': s_host,
    'conga-line': s_conga,
    'before-after': s_before_after,
    'living-room': s_living_room,
    'run-club-arrives': s_run_club,
    'organizer-brain': s_brain,
    'the-flock': s_flock,
    'meet-eggbert': s_eggbert,
    'craft-night-tangle': s_tangled,
    'tuesday-chart': s_chart,
    'chess-faceoff': s_chess_faceoff,
}

if __name__ == '__main__':
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name in (sys.argv[2:] or list(SHEETS)):
        (out / f'{name}.svg').write_text(SHEETS[name]().svg(), encoding='utf-8')
        print('wrote', name)
