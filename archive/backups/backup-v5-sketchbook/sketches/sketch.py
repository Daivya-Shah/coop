"""A tiny pen-sketch engine: 3D-ish objects drawn with doubled, wobbly, overshooting felt-tip lines.

Usage: python sketch.py OUT_DIR
Writes one SVG per sheet (light grey ink on a transparent background).
"""
import math, random, re, sys
from pathlib import Path

INK = '#D3D3D3'
PEN = 1.6  # felt-tip weight multiplier
W, H = 1100, 950


# ---------------------------------------------------------------------------
# geometry helpers
# ---------------------------------------------------------------------------
def resample(pts, step=5.0):
    out = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        for i in range(1, n + 1):
            t = i / n
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    return out


def bez(p0, c1, c2, p3, n=14):
    pts = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        pts.append((a * p0[0] + b * c1[0] + c * c2[0] + d * p3[0], a * p0[1] + b * c1[1] + c * c2[1] + d * p3[1]))
    return pts


def ellipse(cx, cy, rx, ry, rot=0.0, a0=0.0, a1=2 * math.pi, n=48):
    pts, cr, sr = [], math.cos(rot), math.sin(rot)
    for i in range(n + 1):
        t = a0 + (a1 - a0) * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * cr - y * sr, cy + x * sr + y * cr))
    return pts


def clip(poly, n, c, d):
    """Segment of the line {p: p.n = c} inside convex polygon poly, as two points."""
    us = []
    for p, q in zip(poly, poly[1:] + poly[:1]):
        dp = p[0] * n[0] + p[1] * n[1] - c
        dq = q[0] * n[0] + q[1] * n[1] - c
        if dp * dq <= 0 and dp != dq:
            t = dp / (dp - dq)
            x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
            us.append(x * d[0] + y * d[1])
    if len(us) < 2:
        return None
    u0, u1 = min(us), max(us)
    base = (n[0] * c, n[1] * c)
    return ((base[0] + d[0] * u0, base[1] + d[1] * u0), (base[0] + d[0] * u1, base[1] + d[1] * u1))


# ---------------------------------------------------------------------------
# handwriting: single-stroke capitals and digits (100-unit cell)
# ---------------------------------------------------------------------------
GLYPHS = {
    'A': (76, "M5 97 C 16 64, 26 34, 37 5 C 48 36, 60 66, 71 97 M19 63 L57 60"),
    'B': (64, "M11 5 L11 97 M11 6 C 60 0, 64 44, 14 49 M14 49 C 70 46, 72 101, 11 96"),
    'C': (68, "M62 16 C 52 2, 14 0, 8 42 C 4 80, 30 100, 50 94 C 58 92, 62 86, 64 82"),
    'D': (70, "M11 4 L11 97 M11 5 C 76 0, 80 100, 11 96"),
    'E': (62, "M58 6 L12 7 L12 95 L60 93 M12 50 L50 48"),
    'F': (60, "M58 5 L12 7 L12 97 M12 51 L48 48"),
    'G': (70, "M62 16 C 52 2, 14 0, 8 42 C 4 80, 30 100, 50 94 C 60 90, 64 76, 64 60 L40 60"),
    'H': (70, "M10 4 L11 97 M60 3 L61 96 M11 50 L60 48"),
    'I': (26, "M13 4 L14 97"),
    'J': (56, "M48 4 C 48 40, 50 70, 40 88 C 30 100, 12 96, 6 80"),
    'K': (66, "M11 4 L12 97 M60 5 L13 56 M28 42 L63 96"),
    'L': (60, "M11 4 L12 95 L58 93"),
    'M': (86, "M8 97 L10 4 L43 60 L76 4 L78 97"),
    'N': (72, "M10 97 L11 4 L62 96 L63 3"),
    'O': (80, "M42 5 C 14 4, 5 34, 6 56 C 8 84, 26 98, 43 96 C 66 94, 77 68, 75 46 C 73 20, 62 6, 42 5"),
    'P': (64, "M11 97 L11 5 C 64 0, 66 52, 13 54"),
    'Q': (82, "M42 5 C 14 4, 5 34, 6 56 C 8 84, 26 98, 43 96 C 66 94, 77 68, 75 46 C 73 20, 62 6, 42 5 M48 70 L80 100"),
    'R': (70, "M11 97 L11 5 C 64 0, 68 50, 14 52 M30 53 L66 97"),
    'S': (62, "M56 14 C 46 2, 12 2, 10 24 C 8 44, 54 46, 54 70 C 54 94, 18 100, 6 84"),
    'T': (78, "M4 9 L76 5 M40 7 L42 97"),
    'U': (70, "M10 4 C 9 40, 8 70, 18 86 C 28 100, 50 100, 58 84 C 64 70, 62 36, 62 3"),
    'V': (74, "M4 4 L37 97 L70 3"),
    'W': (92, "M4 5 L23 96 L46 30 L66 96 L88 4"),
    'X': (70, "M6 4 L64 96 M64 4 L6 96"),
    'Y': (72, "M4 5 L36 50 L69 4 M36 50 L37 98"),
    'Z': (64, "M6 6 L58 6 L6 94 L60 94"),
    '0': (60, "M30 4 C 4 4, 4 96, 30 96 C 56 96, 56 4, 30 4"),
    '1': (40, "M10 20 L26 4 L26 96"),
    '2': (60, "M8 24 C 10 0, 56 -2, 54 26 C 52 50, 8 70, 6 96 L58 96"),
    '3': (60, "M8 14 C 30 -4, 60 8, 50 34 C 44 48, 28 48, 24 48 C 60 46, 66 92, 30 96 C 18 98, 8 92, 6 86"),
    '4': (62, "M44 96 L44 4 L4 66 L60 66"),
    '5': (60, "M54 4 L14 4 L10 44 C 40 34, 62 50, 58 72 C 54 96, 20 100, 6 86"),
    '6': (60, "M50 8 C 20 0, 4 40, 8 70 C 12 100, 56 100, 54 66 C 52 40, 14 44, 8 66"),
    '7': (60, "M6 6 L58 6 L24 96"),
    '8': (64, "M32 48 C 4 40, 10 4, 32 4 C 54 4, 60 40, 32 48 C 0 56, 6 96, 32 96 C 58 96, 64 56, 32 48"),
    '9': (60, "M52 34 C 50 0, 4 4, 8 32 C 12 56, 50 50, 52 34 C 54 70, 40 96, 12 92"),
    ':': (20, "M10 30 L10 33 M10 80 L10 83"),
    '.': (18, "M9 92 L9 95"),
    '/': (40, "M36 2 L4 98"),
    '-': (40, "M6 54 L34 52"),
    '=': (50, "M6 40 L44 40 M6 64 L44 64"),
    '+': (52, "M26 28 L26 76 M4 52 L48 52"),
    '!': (22, "M11 4 L11 70 M11 92 L11 95"),
    '?': (56, "M8 22 C 10 0, 52 -2, 50 24 C 48 44, 28 46, 28 66 M28 92 L28 95"),
    '$': (62, "M56 18 C 46 6, 12 6, 10 26 C 8 46, 54 46, 54 70 C 54 92, 18 96, 6 82 M31 -4 L31 104"),
    '~': (50, "M4 56 C 14 40, 30 70, 46 50"),
    '%': (60, "M6 94 L54 6 M16 10 C 6 10, 6 30, 16 30 C 26 30, 26 10, 16 10 M44 70 C 34 70, 34 90, 44 90 C 54 90, 54 70, 44 70"),
    "'": (16, "M8 4 L8 24"),
    '"': (30, "M8 4 L8 26 M22 4 L22 26"),
}


def parse(d):
    toks = re.findall(r'[MLC]|-?\d*\.?\d+', d)
    polys, cmd, pen, i = [], None, None, 0
    while i < len(toks):
        t = toks[i]
        if t in ('M', 'L', 'C'):
            cmd = t
            i += 1
            continue
        if cmd == 'M':
            pen = (float(toks[i]), float(toks[i + 1]))
            polys.append([pen])
            i += 2
            cmd = 'L'
        elif cmd == 'L':
            pen = (float(toks[i]), float(toks[i + 1]))
            polys[-1].append(pen)
            i += 2
        elif cmd == 'C':
            c1 = (float(toks[i]), float(toks[i + 1]))
            c2 = (float(toks[i + 2]), float(toks[i + 3]))
            p3 = (float(toks[i + 4]), float(toks[i + 5]))
            polys[-1].extend(bez(pen, c1, c2, p3, 10)[1:])
            pen = p3
            i += 6
    return polys


PARSED = {k: (w, parse(d)) for k, (w, d) in GLYPHS.items()}


# ---------------------------------------------------------------------------
# the sheet / pen
# ---------------------------------------------------------------------------
class Sheet:
    def __init__(self, seed):
        self.r = random.Random(seed)
        self.items = []

    def _emit(self, pts, width, wobble, ox, oy):
        r = self.r
        f1 = 2 * math.pi / r.uniform(110, 240)
        f2 = 2 * math.pi / r.uniform(30, 70)
        p1, p2 = r.uniform(0, 6.3), r.uniform(0, 6.3)
        out, acc = [], 0.0
        for i, (x, y) in enumerate(pts):
            if i:
                acc += math.hypot(x - pts[i - 1][0], y - pts[i - 1][1])
            a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
            tx, ty = b[0] - a[0], b[1] - a[1]
            L = math.hypot(tx, ty) or 1
            off = wobble * (0.65 * math.sin(f1 * acc + p1) + 0.35 * math.sin(f2 * acc + p2))
            out.append((x - ty / L * off + ox, y + tx / L * off + oy))
        d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in out)
        self.items.append(f'<path d="{d}" stroke-width="{width * PEN:.2f}"/>')

    def line(self, pts, width=2.7, passes=2, wobble=1.7, over=9, closed=False, partial=True):
        r = self.r
        pts = list(pts)
        if len(pts) < 2:
            return
        if closed:
            pts = pts + [pts[0]]
        for k in range(passes):
            q = resample(pts, 5)
            if closed:
                q = q + q[1:1 + int(len(q) * r.uniform(0.03, 0.14))]
            else:
                for end in (0, -1):
                    x0, y0 = q[end]
                    x1, y1 = q[min(2, len(q) - 1)] if end == 0 else q[max(-3, -len(q))]
                    L = math.hypot(x1 - x0, y1 - y0) or 1
                    e = r.uniform(0, over)
                    p = (x0 - (x1 - x0) / L * e, y0 - (y1 - y0) / L * e)
                    if end == 0:
                        q.insert(0, p)
                    else:
                        q.append(p)
            if k > 0 and partial and len(q) > 8 and r.random() < 0.55:
                a = int(len(q) * r.uniform(0, 0.35))
                b = int(len(q) * r.uniform(0.6, 1.0))
                q = q[a:max(a + 3, b)]
            mag = r.uniform(0, 0.6) if k == 0 else r.uniform(1.2, 3.0)
            ang = r.uniform(0, 6.3)
            self._emit(q, width * r.uniform(0.8, 1.15), wobble, math.cos(ang) * mag, math.sin(ang) * mag)

    def poly(self, pts, **kw):
        self.line(pts, closed=True, **kw)

    def hatch(self, poly, angle=40, spacing=7.0, width=1.9, zigzag=True, inset=0.35):
        r = self.r
        a = math.radians(angle)
        d = (math.cos(a), math.sin(a))
        n = (-d[1], d[0])
        proj = [p[0] * n[0] + p[1] * n[1] for p in poly]
        c, hi = min(proj) + spacing * r.uniform(0.3, 0.9), max(proj)
        segs = []
        while c < hi:
            s = clip(poly, n, c, d)
            if s:
                (x0, y0), (x1, y1) = s
                L = math.hypot(x1 - x0, y1 - y0)
                if L > 3:
                    i0, i1 = r.uniform(-0.15, inset) * spacing, r.uniform(-0.15, inset) * spacing
                    ux, uy = (x1 - x0) / L, (y1 - y0) / L
                    segs.append(((x0 + ux * i0, y0 + uy * i0), (x1 - ux * i1, y1 - uy * i1)))
            c += spacing * r.uniform(0.75, 1.25)
        if not segs:
            return
        if zigzag:
            path = []
            for i, (p, q) in enumerate(segs):
                path += [p, q] if i % 2 == 0 else [q, p]
            self.line(path, width=width, passes=1, wobble=0.6, over=2)
        else:
            for p, q in segs:
                self.line([p, q], width=width, passes=1, wobble=0.5, over=3)

    def text(self, s, x, y, size=24, rot=0.0, width=2.1, anchor='start'):
        r = self.r
        k = size / 100
        adv = sum(PARSED[ch][0] * k + size * 0.16 if ch in PARSED else size * 0.45 for ch in s)
        if anchor == 'middle':
            x -= adv / 2 * math.cos(rot)
            y -= adv / 2 * math.sin(rot)
        cx = 0.0
        cr, sr = math.cos(rot), math.sin(rot)
        for ch in s:
            if ch not in PARSED:
                cx += size * 0.45
                continue
            w, polys = PARSED[ch]
            jr = r.uniform(-0.06, 0.06)
            jy = r.uniform(-0.05, 0.05) * size
            for pl in polys:
                pts = []
                for gx, gy in pl:
                    gx, gy = gx * k, gy * k - size + jy
                    gx2 = gx * math.cos(jr) - gy * math.sin(jr) + cx
                    gy2 = gx * math.sin(jr) + gy * math.cos(jr)
                    pts.append((x + gx2 * cr - gy2 * sr, y + gx2 * sr + gy2 * cr))
                self.line(pts, width=width, passes=1, wobble=0.45, over=1.5)
            cx += w * k + size * 0.16

    def arrow(self, pts, head=13, width=2.2):
        self.line(pts, width=width, passes=1, wobble=1.0, over=3)
        (x1, y1), (x0, y0) = pts[-1], pts[-2]
        a = math.atan2(y1 - y0, x1 - x0)
        for da in (2.55, -2.55):
            self.line([(x1, y1), (x1 + head * math.cos(a + da), y1 + head * math.sin(a + da))], width=width, passes=1, wobble=0.3, over=2)

    def dim(self, p, q, label, size=20, off=0):
        """Dimension line with end ticks and a label."""
        a = math.atan2(q[1] - p[1], q[0] - p[0])
        nx, ny = -math.sin(a), math.cos(a)
        self.line([p, q], width=1.8, passes=1, wobble=0.5, over=4)
        for (x, y) in (p, q):
            self.line([(x - nx * 9, y - ny * 9), (x + nx * 9, y + ny * 9)], width=1.8, passes=1, wobble=0.2, over=2)
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        self.text(label, mx + nx * (12 + off), my + ny * (12 + off) + size * 0.9 * (1 if ny > 0 else 0), size=size, rot=a, anchor='middle', width=1.9)

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">'
                '<defs><filter id="ink" x="-2%" y="-2%" width="104%" height="104%">'
                '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="4"/>'
                '<feDisplacementMap in="SourceGraphic" scale="1.6"/></filter></defs>'
                f'<g stroke="{INK}" stroke-linecap="round" stroke-linejoin="round" filter="url(#ink)">'
                + ''.join(self.items) + '</g></svg>')


# ---------------------------------------------------------------------------
# 3D camera and primitives
# ---------------------------------------------------------------------------
class Cam:
    def __init__(self, yaw, pitch, scale, ox, oy, D=900):
        self.t, self.f = math.radians(yaw), math.radians(pitch)
        self.s, self.ox, self.oy, self.D = scale, ox, oy, D

    def rot(self, p):
        x, y, z = p
        ct, st = math.cos(self.t), math.sin(self.t)
        return x * ct - y * st, x * st + y * ct, z

    def depth(self, p):
        xr, yr, z = self.rot(p)
        return yr * math.cos(self.f) - z * math.sin(self.f)

    def P(self, p):
        xr, yr, z = self.rot(p)
        cf, sf = math.cos(self.f), math.sin(self.f)
        depth = yr * cf - z * sf
        up = yr * sf + z * cf
        k = self.D / (self.D + depth)
        return self.ox + xr * k * self.s, self.oy - up * k * self.s

    def visible(self, n):
        nx, ny, nz = self.rot(n)
        return ny * math.cos(self.f) - nz * math.sin(self.f) < -1e-6

    def facing_right(self, n):
        return self.rot(n)[0]


FACES = [  # normal, corner indices (dx, dy, dz) packed as dz*4+dy*2+dx
    ((0, 0, 1), (4, 5, 7, 6)), ((0, 0, -1), (0, 2, 3, 1)),
    ((0, -1, 0), (0, 1, 5, 4)), ((0, 1, 0), (2, 6, 7, 3)),
    ((-1, 0, 0), (0, 4, 6, 2)), ((1, 0, 0), (1, 3, 7, 5)),
]


def box(sh, cam, x, y, z, w, d, h, shade=0.35, spacing=7.0, width=2.6, top_shade=False, hatch_angle=None):
    c = [(x + dx * w, y + dy * d, z + dz * h) for dz in (0, 1) for dy in (0, 1) for dx in (0, 1)]
    edges = set()
    for n, idx in FACES:
        if not cam.visible(n):
            continue
        for a, b in zip(idx, idx[1:] + idx[:1]):
            edges.add(tuple(sorted((a, b))))
        fr = cam.facing_right(n)
        poly = [cam.P(c[i]) for i in idx]
        if (fr > shade) or (top_shade and n[2] == 1):
            ang = hatch_angle if hatch_angle is not None else sh.r.choice([35, 50, 62])
            sh.hatch(poly, angle=ang, spacing=spacing)
    for a, b in sorted(edges):
        sh.line([cam.P(c[a]), cam.P(c[b])], width=width)


def circle3d(cam, cx, cy, cz, r, plane='xy', n=40):
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        if plane == 'xy':
            p = (cx + r * math.cos(t), cy + r * math.sin(t), cz)
        elif plane == 'xz':
            p = (cx + r * math.cos(t), cy, cz + r * math.sin(t))
        else:
            p = (cx, cy + r * math.cos(t), cz + r * math.sin(t))
        pts.append(p)
    return pts


def cylinder(sh, cam, cx, cy, z, r, h, width=2.6, shade=True):
    top = circle3d(cam, cx, cy, z + h, r)
    bot = circle3d(cam, cx, cy, z, r)
    sh.poly([cam.P(p) for p in top[:-1]], width=width)
    dc = cam.depth((cx, cy, z))
    front = [cam.P(p) for p in bot if cam.depth(p) <= dc + 1e-6]
    front.sort(key=lambda q: q[0])
    sh.line(front, width=width)
    tp = [cam.P(p) for p in top]
    bp = [cam.P(p) for p in bot]
    i0 = min(range(len(tp)), key=lambda i: tp[i][0])
    i1 = max(range(len(tp)), key=lambda i: tp[i][0])
    sh.line([tp[i0], bp[i0]], width=width)
    sh.line([tp[i1], bp[i1]], width=width)
    if shade:
        mid = [cam.P((cx + r * 0.45, cy - r * 0.2, z + h)), tp[i1], bp[i1], cam.P((cx + r * 0.45, cy - r, z))]
        sh.hatch([cam.P((cx + r * 0.55, cy - r * 0.83, z + h)), tp[i1], bp[i1], cam.P((cx + r * 0.55, cy - r * 0.83, z))], angle=70, spacing=6)


def chair(sh, cam, x, y, back=1, slats=True, seat_z=43, z0=0):
    """Bistro chair: seat centre (x, y); back rest on the +y side (back=1) or -y side (back=-1)."""
    by = y + 16 if back == 1 else y - 19
    seat_z += z0
    box(sh, cam, x - 20, y - 20, seat_z, 40, 40, 4)
    for lx, ly in ((x - 19, y - 19), (x + 16, y - 19), (x - 19, y + 16), (x + 16, y + 16)):
        box(sh, cam, lx, ly, z0, 3, 3, seat_z - z0, shade=2, width=2.2)
    box(sh, cam, x - 19, y - 19, z0 + 14, 38, 2, 2, shade=2, width=1.8)
    for px in (x - 19, x + 16):
        box(sh, cam, px, by, seat_z + 4, 3, 3, 40, shade=2, width=2.2)
    box(sh, cam, x - 19, by, seat_z + 36, 38, 3, 9)
    if slats:
        for sx in (x - 10, x - 1, x + 8):
            box(sh, cam, sx, by + 0.5, seat_z + 6, 2, 2, 30, shade=2, width=1.9)


# ---------------------------------------------------------------------------
# sheets
# ---------------------------------------------------------------------------
def sheet_table():
    sh = Sheet(11)
    cam = Cam(-26, 27, 2.1, 540, 620, D=1100)
    # far chair backs, peeking over the table
    for x in (-150, -70, 10, 90, 170):
        for px in (x - 18, x + 15):
            box(sh, cam, px, 60, 77, 3, 3, 16, shade=2, width=2.1)
        box(sh, cam, x - 18, 60, 88, 36, 3, 8, spacing=5)
    # top + legs
    box(sh, cam, -210, -45, 72, 420, 90, 6, spacing=6)
    for lx, ly in ((-205, -40), (199, -40), (-205, 34), (199, 34)):
        box(sh, cam, lx, ly, 0, 6, 6, 72, shade=0.2, spacing=5, width=2.3)
    # plates and food
    for x in range(-175, 200, 58):
        for y in (-27, 27):
            sh.poly([cam.P(p) for p in circle3d(cam, x, y, 78.5, 12)[:-1]], width=2.3)
            sh.poly([cam.P(p) for p in circle3d(cam, x, y, 78.5, 7.5)[:-1]], width=1.6, passes=1)
    cylinder(sh, cam, -95, 0, 78, 11, 6)
    cylinder(sh, cam, 70, 2, 78, 9, 9)
    box(sh, cam, -20, -7, 78, 34, 14, 9, spacing=5)
    for sx in (-10, 0, 10):
        sh.line([cam.P((sx, -6, 87)), cam.P((sx + 6, 6, 87))], width=1.8, passes=1)
    # the pulled-out chair
    chair(sh, cam, 235, -110, back=-1)
    # notes
    sh.text('TABLE FOR 20', 70, 130, size=40, rot=-0.04, width=2.6)
    sh.arrow(bez((250, 150), (300, 200), (330, 250), (360, 330)))
    a, b = cam.P((-210, -62, 72)), cam.P((210, -62, 72))
    sh.dim(a, b, '4.2 M', size=22, off=6)
    sh.text('+1 EVERY TUE', 520, 880, size=26, rot=-0.03)
    sh.arrow(bez((770, 860), (820, 850), (850, 830), (875, 800)))
    sh.text('SHARED BOWLS', 90, 330, size=20, rot=-0.05, width=1.9)
    sh.arrow(bez((200, 345), (250, 370), (300, 400), (330, 440)), head=10)
    return sh


def sheet_chair():
    sh = Sheet(23)
    big = Cam(-32, 22, 5.2, 400, 760, D=700)
    chair(sh, big, 0, 0)
    front = Cam(0, 0, 2.6, 860, 470, D=10000)
    chair(sh, front, 0, 0, slats=True)
    side = Cam(90, 0, 2.6, 860, 860, D=10000)
    chair(sh, side, 0, 0, slats=False)
    sh.text('BISTRO CHAIR', 80, 110, size=40, width=2.6)
    sh.text('THE ONE WE SAVE FOR YOU', 84, 160, size=20, width=1.8)
    sh.text('FRONT', 815, 210, size=20)
    sh.text('SIDE', 820, 615, size=20)
    sh.text('STACKS X6', 640, 330, size=20, rot=0.08)
    sh.arrow(bez((660, 345), (620, 380), (590, 420), (560, 470)), head=10)
    sh.dim(big.P((-20, -20, 43)), big.P((-20, -20, 0)), '45', size=18, off=4)
    return sh


def sheet_storefront():
    sh = Sheet(37)
    cam = Cam(-28, 10, 1.55, 470, 820, D=2200)
    box(sh, cam, -200, 0, 0, 400, 260, 330, shade=0.5, spacing=8)
    P = lambda x, z, y=0: cam.P((x, y, z))
    # window
    sh.poly([P(-175, 40), P(40, 40), P(40, 235), P(-175, 235)])
    sh.line([P(-68, 40), P(-68, 205)], width=2.2)
    sh.line([P(-175, 205), P(40, 205)], width=2.2)
    box(sh, cam, -185, -10, 30, 235, 10, 10, spacing=5)
    # people inside
    for i, x in enumerate(range(-150, 30, 34)):
        sh.poly([cam.P(p) for p in circle3d(cam, x, 25, 120, 11, plane='xz')[:-1]], width=2.2)
        sh.line([cam.P((x - 16, 25, 92)), cam.P((x - 15, 25, 103)), cam.P((x - 6, 25, 108)), cam.P((x + 6, 25, 108)), cam.P((x + 15, 25, 103)), cam.P((x + 16, 25, 92))], width=2.1, passes=1)
    sh.line([P(-168, 92, 25), P(32, 92, 25)], width=2.3)
    sh.line([P(-68, 205, 25), P(-68, 180, 25)], width=1.8, passes=1)
    sh.line([P(-82, 172, 25), P(-75, 182, 25), P(-61, 182, 25), P(-54, 172, 25)], width=2, passes=1)
    # door
    sh.poly([P(80, 0), P(165, 0), P(165, 255), P(80, 255)])
    sh.poly([P(96, 140), P(150, 140), P(150, 238), P(96, 238)], width=2.1)
    sh.poly(ellipse(*P(152, 110), 4, 4, n=12), width=2, passes=1)
    sh.text('OPEN', *P(103, 175), size=14, rot=-0.06, width=1.6)
    # awning with stripes
    xs = list(range(-190, 191, 38))
    for i, (x0, x1) in enumerate(zip(xs, xs[1:])):
        quad = [P(x0, 280), P(x1, 280), P(x1, 238, -75), P(x0, 238, -75)]
        if i % 2 == 0:
            sh.hatch(quad, angle=78, spacing=5.5)
        sh.line([P(x0, 280), P(x0, 238, -75)], width=1.9, passes=1)
    sh.poly([P(-190, 280), P(190, 280), P(190, 238, -75), P(-190, 238, -75)])
    sc = []
    for x0, x1 in zip(xs, xs[1:]):
        a, b = P(x0, 238, -75), P(x1, 238, -75)
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 16)
        sc += bez(a, (a[0], m[1]), (b[0], m[1]), b, 8)
    sh.line(sc, width=2.3)
    # sign
    sh.poly([P(-120, 290), P(70, 290), P(70, 322), P(-120, 322)])
    a, b = P(-104, 296), P(60, 296)
    sh.text('THE LOCAL', a[0], a[1] - 4, size=26, rot=math.atan2(b[1] - a[1], b[0] - a[0]), width=2.3)
    # pavement + a-board
    sh.line([cam.P((-320, -130, 0)), cam.P((360, -130, 0))], width=2.2)
    sh.line([cam.P((-320, -165, 0)), cam.P((360, -165, 0))], width=1.8, passes=1)
    fb = [cam.P((235, -112, 0)), cam.P((300, -112, 0)), cam.P((293, -95, 105)), cam.P((242, -95, 105))]
    sh.poly(fb)
    sh.line([cam.P((300, -112, 0)), cam.P((300, -78, 0)), cam.P((293, -95, 105))], width=2.2)
    inner = [cam.P((245, -110, 15)), cam.P((290, -110, 15)), cam.P((286, -97, 95)), cam.P((249, -97, 95))]
    sh.hatch(inner, angle=12, spacing=4.5)
    # notes
    sh.text('QUIET TUESDAY?', 690, 120, size=30, rot=0.03)
    sh.text('NOT ANYMORE', 712, 165, size=22, rot=0.03, width=1.9)
    sh.text('BOOK CLUB', 60, 150, size=24, rot=-0.05)
    sh.text('INSIDE', 70, 186, size=20, rot=-0.05)
    sh.arrow(bez((170, 200), (210, 260), (240, 330), (270, 420)))
    sh.text('A-BOARD: TUE 7PM', 690, 915, size=20)
    sh.arrow(bez((830, 885), (835, 860), (835, 835), (828, 805)), head=10)
    return sh


def sheet_calendar():
    sh = Sheet(41)
    cam = Cam(-14, 52, 3.25, 560, 540, D=1000)
    W7, H5, cw, ch = 7, 5, 32, 26
    x0, y0 = -W7 * cw / 2, -H5 * ch / 2
    # pages underneath
    for k, (dx, dy) in enumerate(((7, -6), (3, -3))):
        sh.poly([cam.P((x0 + dx, y0 + dy - 34, -2 - k)), cam.P((-x0 + dx, y0 + dy - 34, -2 - k)), cam.P((-x0 + dx, -y0 + dy + 6, -2 - k)), cam.P((x0 + dx, -y0 + dy + 6, -2 - k))], width=2, passes=1)
    page = [cam.P((x0, y0 - 34, 0)), cam.P((-x0, y0 - 34, 0)), cam.P((-x0, -y0 + 6, 0)), cam.P((x0, -y0 + 6, 0))]
    sh.poly(page)
    # header band (the far side of the page is +y)
    sh.line([cam.P((x0, -y0 - 4 + 10, 0)), cam.P((-x0, -y0 - 4 + 10, 0))], width=2.2)
    a, b = cam.P((x0 + 20, -y0 - 0, 0)), cam.P((-x0 - 20, -y0 - 0, 0))
    hdr = cam.P((0, -y0 + 1, 0))
    for k, (rx) in enumerate(range(-90, 100, 45)):
        sh.poly(ellipse(*cam.P((rx, -y0 + 6, 0)), 8, 11, n=14), width=2, passes=1)
    # grid
    for i in range(W7 + 1):
        sh.line([cam.P((x0 + i * cw, y0, 0)), cam.P((x0 + i * cw, -y0 - 6 + 0, 0))], width=1.9, passes=1)
    for j in range(H5 + 1):
        sh.line([cam.P((x0, y0 + j * ch, 0)), cam.P((-x0, y0 + j * ch, 0))], width=1.9, passes=1)
    # day letters + numbers; rows go from far (+y) to near
    for i, ch_ in enumerate('MTWTFSS'):
        p = cam.P((x0 + i * cw + cw / 2, -y0 - 1, 0))
        sh.text(ch_, p[0] - 8, p[1] + 2, size=20, width=1.6)
    day = 1
    for j in range(H5):
        for i in range(W7):
            if day > 31:
                break
            p = cam.P((x0 + i * cw + 4, -y0 - 6 - j * ch - 3, 0))
            sh.text(str(day), p[0], p[1] + 18, size=15, width=1.3)
            day += 1
    # tuesdays circled
    for j in range(H5):
        c = cam.P((x0 + cw * 1.5, -y0 - 6 - j * ch - ch / 2, 0))
        l, rr = cam.P((x0 + cw, -y0 - 6 - j * ch - ch / 2, 0)), cam.P((x0 + 2 * cw, -y0 - 6 - j * ch - ch / 2, 0))
        t, b = cam.P((x0 + cw * 1.5, -y0 - 6 - j * ch, 0)), cam.P((x0 + cw * 1.5, -y0 - 6 - (j + 1) * ch, 0))
        rx, ry = abs(rr[0] - l[0]) * 0.46, abs(b[1] - t[1]) * 0.47
        sh.poly(ellipse(c[0], c[1], rx * sh.r.uniform(0.93, 1.08), ry * sh.r.uniform(0.9, 1.1), rot=sh.r.uniform(-0.12, 0.12)), width=2.4, passes=1)
    # one tuesday hatched in: today
    j = 2
    cell = [cam.P((x0 + cw, -y0 - 6 - j * ch, 0)), cam.P((x0 + 2 * cw, -y0 - 6 - j * ch, 0)), cam.P((x0 + 2 * cw, -y0 - 6 - (j + 1) * ch, 0)), cam.P((x0 + cw, -y0 - 6 - (j + 1) * ch, 0))]
    sh.hatch(cell, angle=30, spacing=4)
    # loop arrow
    sh.arrow(bez((990, 300), (1080, 380), (1080, 700), (985, 790)))
    sh.text('SAME TIME', 60, 830, size=28, rot=-0.04)
    sh.text('NEXT WEEK', 66, 874, size=28, rot=-0.04)
    sh.text('EVERY TUE', 120, 120, size=30, rot=-0.03)
    sh.arrow(bez((250, 140), (300, 170), (330, 200), (345, 245)), head=11)
    sh.text('4 WEEK PILOT', 800, 110, size=22, rot=0.03)
    return sh


def sheet_card():
    sh = Sheet(53)
    cam = Cam(-24, 24, 4.6, 400, 470, D=600)
    A, B, C, D_ = (-40, -15, 0), (40, -15, 0), (40, 0, 34), (-40, 0, 34)
    E, F = (40, 15, 0), (-40, 15, 0)
    faces = [((0, -34, 15), [A, B, C, D_]), ((0, 34, 15), [D_, C, E, F]), ((1, 0, 0), [B, E, C]), ((-1, 0, 0), [A, D_, F])]
    edges = []
    for n, pts in faces:
        if cam.visible(n):
            pp = [cam.P(p) for p in pts]
            for a, b in zip(pp, pp[1:] + pp[:1]):
                edges.append((a, b))
            if n[0] == 1:
                sh.hatch(pp, angle=60, spacing=6)
    for a, b in edges:
        sh.line([a, b])
    a, b = cam.P((-31, -9, 13)), cam.P((31, -9, 13))
    sh.text('RESERVED', a[0], a[1], size=30, rot=math.atan2(b[1] - a[1], b[0] - a[0]), width=2.4)
    a2 = cam.P((-12, -12, 5))
    sh.text('COOP', a2[0], a2[1], size=13, rot=math.atan2(b[1] - a[1], b[0] - a[0]), width=1.6)
    # unfolded net
    nx, ny, nw, nh = 600, 520, 380, 260
    sh.poly([(nx, ny), (nx + nw, ny), (nx + nw, ny + nh), (nx, ny + nh)])
    for x in range(nx + 6, nx + nw, 22):
        sh.line([(x, ny + nh / 2), (x + 11, ny + nh / 2)], width=1.8, passes=1, over=1)
    sh.text('RESERVED', nx + nw / 2, ny + nh * 0.78, size=30, anchor='middle')
    sh.text('RESERVED', nx + nw / 2, ny + nh * 0.22, size=30, rot=math.pi, anchor='middle')
    sh.dim((nx, ny + nh + 30), (nx + nw, ny + nh + 30), '12 CM', size=18)
    sh.dim((nx + nw + 30, ny), (nx + nw + 30, ny + nh), '8 CM', size=18)
    sh.text('FOLD', nx - 120, ny + nh / 2 + 6, size=22)
    sh.arrow([(nx - 50, ny + nh / 2), (nx - 8, ny + nh / 2)], head=10)
    sh.text('THE ONLY SIGN', 610, 140, size=28, rot=0.03)
    sh.text('WE NEED', 640, 184, size=28, rot=0.03)
    sh.arrow(bez((630, 210), (560, 260), (520, 300), (500, 340)))
    return sh


def sheet_supper():
    sh = Sheet(67)
    # pizza (top view)
    cx, cy, r = 280, 330, 150
    sh.poly(ellipse(cx, cy, r, r, n=60))
    sh.poly(ellipse(cx, cy, r - 18, r - 18, n=60), width=2.1, passes=1)
    for k in range(8):
        a = k * math.pi / 4 + 0.2
        if k == 1:
            continue
        sh.line([(cx, cy), (cx + (r - 18) * math.cos(a), cy + (r - 18) * math.sin(a))], width=2.2)
    for _ in range(14):
        a, d = sh.r.uniform(0, 6.3), sh.r.uniform(25, r - 40)
        px, py = cx + d * math.cos(a), cy + d * math.sin(a)
        sh.poly(ellipse(px, py, 9, 8, n=12), width=1.9, passes=1)
        if sh.r.random() < 0.5:
            sh.hatch(ellipse(px, py, 7, 6, n=10)[:-1], angle=45, spacing=3.5, width=1.5)
    # the missing slice, pulled out
    a0, a1 = 0.2 + math.pi / 4, 0.2 + math.pi / 2
    ox, oy = 60 * math.cos((a0 + a1) / 2), 60 * math.sin((a0 + a1) / 2)
    tip = (cx + ox, cy + oy)
    arc = ellipse(cx + ox, cy + oy, r, r, a0=a0, a1=a1, n=12)
    sh.poly([tip] + arc)
    sh.text('8 SLICES', 70, 110, size=24, rot=-0.04)
    sh.text('ONE GONE', 74, 146, size=20, rot=-0.04, width=1.8)
    # noodle bowl
    cam = Cam(-10, 32, 3.1, 790, 330, D=800)
    rim = [cam.P(p) for p in circle3d(cam, 0, 0, 30, 42)]
    sh.poly(rim[:-1])
    prof_l, prof_r = [], []
    for k in range(9):
        z = 30 - k * 3.6
        rr = 42 * math.sqrt(max(0.0, 1 - (k / 9) ** 1.6)) + 2
        ring = [cam.P(p) for p in circle3d(cam, 0, 0, z, rr)]
        prof_l.append(min(ring, key=lambda q: q[0]))
        prof_r.append(max(ring, key=lambda q: q[0]))
    base = [cam.P(p) for p in circle3d(cam, 0, 0, 0, 16)]
    front = [p for p in base if p[1] >= cam.P((0, 0, 0))[1] - 1]
    sh.line(prof_l + sorted(front, key=lambda q: q[0]) + prof_r[::-1])
    sh.hatch([prof_r[0], prof_r[4], prof_r[8], cam.P((16, -4, 0)), cam.P((30, -20, 26))], angle=75, spacing=6)
    cxr, cyr = cam.P((0, 0, 30))
    for k in range(4):
        y = cyr - 10 + k * 7
        sh.line([(cxr - 70 + x, y + 6 * math.sin(x / 7 + k)) for x in range(0, 140, 4)], width=1.8, passes=1)
    sh.line([(cxr + 20, cyr - 10), (cxr + 160, cyr - 150)], width=2.6)
    sh.line([(cxr + 32, cyr - 4), (cxr + 175, cyr - 136)], width=2.6)
    for k in (-40, 0, 40):
        sh.line([(cxr + k + 6 * math.sin(t / 9), cyr - 70 - t) for t in range(0, 70, 4)], width=1.8, passes=1)
    sh.text('STEAM!!', 640, 110, size=22, rot=0.05)
    # bread
    bx, by = 260, 700
    loaf = bez((bx - 150, by + 60), (bx - 160, by - 70), (bx + 160, by - 70), (bx + 150, by + 60)) + [(bx - 150, by + 60)]
    sh.poly(loaf[:-1])
    for k in range(-2, 3):
        sh.line([(bx + k * 50 - 18, by - 30), (bx + k * 50 + 14, by + 4)], width=2.4)
    sh.hatch([(bx + 40, by + 60), (bx + 150, by + 60), (bx + 140, by + 10), (bx + 90, by + 20)], angle=60, spacing=6)
    sh.line([(bx - 190, by + 64), (bx + 200, by + 64)], width=2.2)
    sh.text('SOURDOUGH', 120, 840, size=22)
    # fork + knife
    fx, fy = 560, 600
    sh.poly([(fx - 9, fy + 70), (fx - 6, fy + 260), (fx + 6, fy + 260), (fx + 9, fy + 70), (fx + 14, fy + 10), (fx - 14, fy + 10)], width=2.3)
    for k in (-10, -3, 4, 11):
        sh.line([(fx + k, fy + 10), (fx + k, fy - 40)], width=2.1)
    kx = 640
    sh.poly([(kx - 8, fy + 260), (kx - 8, fy + 110), (kx - 10, fy - 30), (kx + 8, fy - 40), (kx + 10, fy + 110), (kx + 8, fy + 260)], width=2.3)
    sh.hatch([(kx - 8, fy + 120), (kx + 8, fy + 120), (kx + 8, fy + 255), (kx - 8, fy + 255)], angle=20, spacing=5)
    # plate
    pc = Cam(0, 58, 2.3, 900, 770, D=900)
    for rr, wdt in ((52, 2.6), (40, 2.0)):
        sh.poly([pc.P(p) for p in circle3d(pc, 0, 0, 0, rr)[:-1]], width=wdt)
    sh.text('FAMILY STYLE', 770, 640, size=24, rot=0.04)
    sh.text('$20-30 PP', 830, 905, size=22, rot=-0.03)
    return sh


def sheet_clubkit():
    sh = Sheet(79)
    # sneaker
    s, ox, oy = 1.25, 90, 120
    T = lambda pts: [(ox + x * s, oy + y * s) for x, y in pts]
    upper = bez((10, 140), (0, 60), (30, 40), (70, 40)) + bez((70, 40), (120, 40), (150, 70), (200, 80))[1:] + bez((200, 80), (260, 90), (300, 110), (300, 140))[1:]
    sh.line(T(upper))
    sole = [(4, 140), (304, 140), (300, 162), (10, 162), (4, 140)]
    sh.poly(T(sole[:-1]))
    sh.hatch(T([(10, 150), (300, 150), (298, 161), (12, 161)]), angle=80, spacing=5)
    for k in range(5):
        x = 100 + k * 18
        sh.line(T([(x, 52 + k * 4), (x + 20, 74 + k * 3)]), width=2, passes=1)
    sh.line(T([(30, 128), (290, 128)]), width=1.7, passes=1)
    sh.poly(T(ellipse(55, 78, 22, 14, n=16)[:-1]), width=2.1, passes=1)
    sh.line(T(bez((200, 82), (230, 100), (250, 128), (252, 140))), width=2.0, passes=1)
    sh.line(T([(12, 100), (30, 96), (34, 128)]), width=2.0, passes=1)
    for k in range(5):
        x = 98 + k * 18
        sh.poly(T(ellipse(x, 50 + k * 4, 3, 3, n=8)[:-1]), width=1.5, passes=1)
    sh.text('RUN', 160, 380, size=26)
    # books
    for i, yaw in enumerate((-18, -32, -12)):
        cam = Cam(yaw, 30, 2.5, 790, 330, D=900)
        box(sh, cam, -34, -24, i * 10, 68, 48, 10, shade=0.3, spacing=4.5)
    sh.text('BOOK', 750, 450, size=26)
    # yarn ball + needles
    yx, yy, yr = 240, 640, 78
    sh.line([(yx - 30, yy - 140), (yx + 40, yy + 20)], width=2.6)
    sh.line([(yx + 60, yy - 150), (yx - 10, yy + 10)], width=2.6)
    sh.poly(ellipse(yx - 30, yy - 146, 7, 7, n=10), width=2, passes=1)
    sh.poly(ellipse(yx + 62, yy - 156, 7, 7, n=10), width=2, passes=1)
    sh.poly(ellipse(yx, yy, yr, yr, n=48))
    for k in range(7):
        sh.line(ellipse(yx, yy, yr * 0.95, yr * (0.25 + k * 0.08), rot=0.5 + k * 0.42, a0=0.2, a1=2.9, n=24), width=1.9, passes=1)
    sh.line(bez((yx + yr, yy + 20), (yx + 160, yy + 40), (yx + 120, yy + 140), (yx + 220, yy + 150)), width=2.1, passes=1)
    sh.text('CRAFT', 180, 800, size=26)
    # pawn
    px, py = 560, 720
    prof = [(42, 0), (42, -14), (30, -20), (18, -26), (14, -60), (12, -90), (22, -96), (12, -102)]
    left = [(px - x, py + y) for x, y in prof]
    right = [(px + x, py + y) for x, y in prof]
    sh.line(left[::-1] + right)
    sh.poly(ellipse(px, py - 124, 24, 24, n=24))
    sh.poly(ellipse(px, py, 42, 9, n=24), width=2.1, passes=1)
    sh.hatch([(px + 6, py - 26), (px + 18, py - 26), (px + 14, py - 88), (px + 6, py - 88)], angle=80, spacing=4.5)
    sh.text('CHESS', 510, 800, size=26)
    # notebook + pen
    cam = Cam(-24, 34, 2.3, 860, 640, D=900)
    box(sh, cam, -45, -32, 0, 90, 64, 8, shade=0.3, spacing=4.5)
    sh.line([cam.P((25, -32, 8.2)), cam.P((25, 32, 8.2))], width=2.2)
    sh.line([(760, 720), (980, 560)], width=3.0)
    sh.line([(768, 728), (988, 568)], width=2.0, passes=1)
    sh.line([(760, 720), (748, 738)], width=2.2)
    sh.text('WRITE', 820, 800, size=26)
    sh.text('WHAT EACH CLUB BRINGS', 330, 905, size=24, rot=-0.02, width=1.9)
    return sh


def sheet_plan():
    sh = Sheet(91)
    x0, y0, x1, y1 = 110, 120, 1000, 800
    for o in (0, 12):
        sh.poly([(x0 - o, y0 - o), (x1 + o, y0 - o), (x1 + o, y1 + o), (x0 - o, y1 + o)], width=2.6 if o else 2.8)
    # entrance gap + door swing
    ex = 430
    sh.line([(ex, y1 + 14), (ex, y1 - 70)], width=2.4)
    sh.line(ellipse(ex, y1, 76, 76, a0=-math.pi / 2, a1=0, n=16), width=1.9, passes=1)
    sh.arrow([(ex + 40, y1 + 110), (ex + 40, y1 + 20)])
    sh.text('IN', ex + 60, y1 + 95, size=22)
    # bar + stools
    sh.poly([(140, 190), (210, 190), (210, 560), (140, 560)])
    sh.hatch([(140, 190), (210, 190), (210, 560), (140, 560)], angle=45, spacing=9)
    for y in range(220, 550, 52):
        sh.poly(ellipse(242, y, 14, 14, n=14), width=2.1)
    sh.text('BAR', 150, 172, size=20)
    # cafe tables
    for tx, ty in ((350, 230), (470, 230), (350, 390), (470, 390), (350, 550)):
        sh.poly(ellipse(tx, ty, 28, 28, n=20), width=2.3)
        for dx in (-46, 34):
            sh.poly([(tx + dx, ty - 10), (tx + dx + 12, ty - 10), (tx + dx + 12, ty + 10), (tx + dx, ty + 10)], width=1.9, passes=1)
    # back room
    bx0, by0, bx1, by1 = 620, 120, 1000, 540
    sh.line([(bx0, by0), (bx0, 300)], width=2.8)
    sh.line([(bx0, 400), (bx0, by1), (bx1, by1)], width=2.8)
    sh.hatch([(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)], angle=-35, spacing=26, width=1.4, zigzag=False, inset=0.0)
    tx0, ty0, tx1, ty1 = 690, 290, 950, 370
    sh.poly([(tx0, ty0), (tx1, ty0), (tx1, ty1), (tx0, ty1)], width=2.8)
    n = 9
    for i in range(n):
        x = tx0 + 14 + i * (tx1 - tx0 - 28) / (n - 1)
        for y in (ty0 - 28, ty1 + 8):
            sh.poly([(x - 9, y), (x + 9, y), (x + 9, y + 20), (x - 9, y + 20)], width=1.8, passes=1)
    for x in (tx0 - 30, tx1 + 10):
        sh.poly([(x, 320), (x + 20, 320), (x + 20, 340), (x, 340)], width=1.8, passes=1)
    sh.text('BACK ROOM', 700, 210, size=26)
    sh.text('20 PPL', 760, 455, size=22)
    # kitchen
    sh.poly([(760, 600), (1000, 600), (1000, 800), (760, 800)])
    sh.line([(760, 600), (1000, 800)], width=1.8, passes=1)
    sh.line([(1000, 600), (760, 800)], width=1.8, passes=1)
    sh.text('KITCHEN', 800, 712, size=22)
    # notes
    sh.text('QUIET TUE 6-10', 280, 72, size=28, rot=-0.02)
    sh.arrow(bez((570, 80), (680, 60), (760, 110), (790, 180)))
    sh.dim((110, 870), (330, 870), '4 M', size=18)
    return sh


# ---------------------------------------------------------------------------
# more 2D helpers
# ---------------------------------------------------------------------------
def rrect(x, y, w, h, r, n=5):
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -math.pi / 2), (x + w - r, y + h - r, 0), (x + r, y + h - r, math.pi / 2), (x + r, y + r, math.pi)):
        pts += ellipse(cx, cy, r, r, a0=a0, a1=a0 + math.pi / 2, n=n)
    return pts


def rotate(pts, cx, cy, a):
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def dashed(sh, pts, on=14, off=10, width=2.2):
    q = resample(pts, 2)
    run, acc, drawing = [q[0]], 0.0, True
    for i in range(1, len(q)):
        acc += math.hypot(q[i][0] - q[i - 1][0], q[i][1] - q[i - 1][1])
        if drawing:
            run.append(q[i])
        if acc >= (on if drawing else off):
            if drawing and len(run) > 1:
                sh.line(run, width=width, passes=1, wobble=0.6, over=1.5)
            run, acc, drawing = [q[i]], 0.0, not drawing


def egg(cx, cy, k):
    return (bez((cx, cy - 95 * k), (cx + 62 * k, cy - 95 * k), (cx + 80 * k, cy + 20 * k), (cx + 66 * k, cy + 60 * k))
            + bez((cx + 66 * k, cy + 60 * k), (cx + 40 * k, cy + 110 * k), (cx - 40 * k, cy + 110 * k), (cx - 66 * k, cy + 60 * k))[1:]
            + bez((cx - 66 * k, cy + 60 * k), (cx - 80 * k, cy + 20 * k), (cx - 62 * k, cy - 95 * k), (cx, cy - 95 * k))[1:])


def pawn(sh, px, py, k=1.0, shade=True):
    prof = [(42, 0), (42, -14), (30, -20), (18, -26), (14, -60), (12, -90), (22, -96), (12, -102)]
    left = [(px - x * k, py + y * k) for x, y in prof]
    right = [(px + x * k, py + y * k) for x, y in prof]
    sh.line(left[::-1] + right, width=2.4)
    sh.poly(ellipse(px, py - 124 * k, 24 * k, 24 * k, n=20), width=2.4)
    sh.poly(ellipse(px, py, 42 * k, 9 * k, n=20), width=2.0, passes=1)
    if shade:
        sh.hatch([(px + 6 * k, py - 26 * k), (px + 18 * k, py - 26 * k), (px + 14 * k, py - 88 * k), (px + 6 * k, py - 88 * k)], angle=80, spacing=4.5)


def sheet_lamps():
    sh = Sheet(101)
    for cx in (230, 550, 870):
        sh.line([(cx, 40), (cx + sh.r.uniform(-3, 3), 290)], width=2.2)
    cx = 230
    sh.line(bez((cx - 120, 420), (cx - 118, 290), (cx + 118, 290), (cx + 120, 420)))
    sh.poly(ellipse(cx, 420, 120, 24, n=40))
    sh.hatch([(cx + 30, 318), (cx + 100, 350), (cx + 118, 418), (cx + 40, 432)], angle=70, spacing=6)
    sh.poly(ellipse(cx, 300, 16, 6, n=12), width=2, passes=1)
    sh.line(bez((cx - 22, 430), (cx - 22, 460), (cx + 22, 460), (cx + 22, 430)), width=2.2, passes=1)
    cx = 550
    sh.line([(cx - 22, 300), (cx - 105, 440)])
    sh.line([(cx + 22, 300), (cx + 105, 440)])
    sh.poly(ellipse(cx, 300, 22, 6, n=14), width=2.2)
    sh.poly(ellipse(cx, 440, 105, 22, n=40))
    sh.hatch([(cx + 10, 306), (cx + 22, 302), (cx + 105, 440), (cx + 50, 452)], angle=65, spacing=6)
    cx = 870
    sh.poly(ellipse(cx, 390, 95, 95, n=48))
    for k in range(4):
        sh.line(ellipse(cx, 390, 95, 18 + k * 22, a0=0.05, a1=math.pi - 0.05, n=24), width=1.8, passes=1)
    sh.poly(ellipse(cx, 290, 20, 7, n=12), width=2.2)
    sh.hatch(ellipse(cx + 38, 410, 42, 60, n=16)[:-1], angle=60, spacing=6)
    for cx, y in ((230, 470), (550, 480), (870, 500)):
        for dx in (-60, 0, 60):
            dashed(sh, [(cx + dx * 0.4, y), (cx + dx, y + 160)], on=10, off=10, width=1.8)
    sh.text('OVER THE TABLE', 80, 730, size=34, rot=-0.02)
    sh.text('DOME', 180, 840, size=22)
    sh.text('CONE', 505, 840, size=22)
    sh.text('GLOBE?', 810, 840, size=22)
    sh.text('WARM + LOW', 640, 740, size=22, rot=0.02, width=1.8)
    return sh


def sheet_coffee():
    sh = Sheet(113)
    cam = Cam(-8, 30, 3.4, 330, 560, D=900)
    sh.poly([cam.P(p) for p in circle3d(cam, 0, 0, 0, 62)[:-1]], width=2.4)
    sh.poly([cam.P(p) for p in circle3d(cam, 0, 0, 0, 44)[:-1]], width=1.8, passes=1)
    cylinder(sh, cam, 0, 0, 2, 30, 36)
    sh.poly([cam.P(p) for p in circle3d(cam, 0, 0, 35, 25)[:-1]], width=1.8, passes=1)
    hx, hy = cam.P((31, 0, 22))
    sh.line(bez((hx, hy - 30), (hx + 60, hy - 40), (hx + 60, hy + 30), (hx, hy + 20)))
    tx, ty = cam.P((0, 0, 40))
    for dx in (-30, 0, 30):
        sh.line([(tx + dx + 7 * math.sin(t / 8), ty - 30 - t) for t in range(0, 90, 4)], width=1.9, passes=1)
    cx, cy = 790, 520
    for i, a in enumerate([-1.05, -0.55, 0.0, 0.55, 1.05]):
        r = 26 + (2 - abs(i - 2)) * 18
        x, y = cx + 150 * math.sin(a), cy - 70 * math.cos(a) + 60
        sh.poly(ellipse(x, y, r * 0.8, r, rot=a, n=24), width=2.4)
        if i >= 3:
            sh.hatch(ellipse(x + 6, y + 6, r * 0.55, r * 0.7, rot=a, n=14)[:-1], angle=55, spacing=5)
    sh.poly(ellipse(cx, 610, 230, 40, n=40), width=2.2)
    sh.text('POST-RUN', 120, 130, size=34, rot=-0.03)
    sh.text('COFFEE + CROISSANT', 124, 182, size=24, rot=-0.03, width=1.9)
    sh.text('8:15 AM SAT', 700, 800, size=22, rot=0.03)
    sh.text('$6 EACH?', 690, 205, size=22, rot=0.04)
    sh.arrow(bez((700, 230), (650, 270), (610, 330), (490, 380)))
    return sh


def sheet_chess():
    sh = Sheet(127)
    cam = Cam(-30, 38, 3.0, 520, 560, D=900)
    n, c = 6, 22
    x0 = -n * c / 2
    box(sh, cam, x0 - 6, x0 - 6, -6, n * c + 12, n * c + 12, 6, shade=0.3, spacing=5)
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                q = [cam.P((x0 + i * c, x0 + j * c, 0.1)), cam.P((x0 + (i + 1) * c, x0 + j * c, 0.1)),
                     cam.P((x0 + (i + 1) * c, x0 + (j + 1) * c, 0.1)), cam.P((x0 + i * c, x0 + (j + 1) * c, 0.1))]
                sh.hatch(q, angle=sh.r.choice([30, 40, 55]), spacing=4.2, width=1.6)
    for i in range(n + 1):
        sh.line([cam.P((x0 + i * c, x0, 0.1)), cam.P((x0 + i * c, -x0, 0.1))], width=1.7, passes=1)
        sh.line([cam.P((x0, x0 + i * c, 0.1)), cam.P((-x0, x0 + i * c, 0.1))], width=1.7, passes=1)
    for i, j in ((1, 1), (2, 1), (4, 4), (3, 2), (1, 4)):
        px, py = cam.P((x0 + (i + 0.5) * c, x0 + (j + 0.5) * c, 0))
        pawn(sh, px, py, k=0.42, shade=False)
    sh.text('GAME NIGHT', 90, 130, size=36, rot=-0.03)
    sh.text('BRING THE BOARDS', 94, 180, size=22, rot=-0.03, width=1.8)
    sh.text('6 BOARDS = 12 PPL', 660, 880, size=22, rot=0.02)
    sh.arrow(bez((760, 850), (760, 800), (720, 760), (680, 740)), head=10)
    return sh


def sheet_stack():
    sh = Sheet(139)
    cam = Cam(-34, 20, 4.2, 430, 860, D=700)
    for i in range(4):
        chair(sh, cam, 0, 0, z0=i * 10, slats=(i == 3))
    side = Cam(90, 0, 2.2, 900, 860, D=10000)
    for i in range(6):
        chair(sh, side, 0, 0, z0=i * 10, slats=False)
    sh.text('STACKS X6', 70, 110, size=36, rot=-0.02)
    sh.text('OUT ON TUESDAYS', 74, 160, size=22, rot=-0.02, width=1.8)
    sh.text('SIDE', 860, 330, size=20)
    return sh


def sheet_boards():
    sh = Sheet(151)
    boards = [('MON', 'BOOK CLUB', '7PM'), ('TUE', 'RUN CLUB', '8PM'), ('SUN', 'SUPPER', '7PM')]
    for k, (d, what, t) in enumerate(boards):
        cx = 200 + k * 350
        top, bot = 250, 700
        sh.poly([(cx - 110, top), (cx + 110, top), (cx + 130, bot), (cx - 130, bot)])
        sh.poly([(cx - 92, top + 18), (cx + 92, top + 18), (cx + 108, bot - 90), (cx - 108, bot - 90)], width=2.1)
        sh.line([(cx - 130, bot), (cx - 150, bot + 120)], width=2.6)
        sh.line([(cx + 130, bot), (cx + 150, bot + 120)], width=2.6)
        sh.line([(cx - 140, bot + 50), (cx + 140, bot + 50)], width=2.0, passes=1)
        sh.text(d, cx, top + 100, size=48, anchor='middle', width=2.6)
        sh.text(what, cx, top + 190, size=24, anchor='middle')
        sh.text(t, cx, top + 250, size=24, anchor='middle')
        sh.line([(cx - 60, top + 290), (cx + 60, top + 286)], width=1.8, passes=1)
        sh.hatch([(cx + 112, top + 6), (cx + 128, bot - 4), (cx + 110, bot - 92), (cx + 95, top + 22)], angle=80, spacing=5)
    sh.text('ONE BOARD PER NIGHT', 70, 120, size=34, rot=-0.02)
    return sh


def sheet_route():
    sh = Sheet(163)
    x0, y0, x1, y1 = 150, 170, 980, 860
    sh.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], width=2.0, passes=1)
    for y in range(y0 + 90, y1, 110):
        sh.line([(x0 + 120, y + sh.r.uniform(-6, 6)), (x1, y + sh.r.uniform(-6, 6))], width=1.8, passes=1)
    for x in range(x0 + 220, x1, 140):
        sh.line([(x + sh.r.uniform(-6, 6), y0), (x + sh.r.uniform(-12, 12), y1)], width=1.8, passes=1)
    for k in range(3):
        sh.line([(x0 + 20 + k * 30 + 8 * math.sin(t / 30), t) for t in range(y0, y1, 6)], width=1.6, passes=1)
    sh.text('RIVER', x0 + 92, 600, size=18, rot=-math.pi / 2)
    route = (bez((320, 780), (180, 640), (190, 330), (420, 280)) + bez((420, 280), (650, 230), (900, 280), (860, 500))[1:]
             + bez((860, 500), (820, 700), (620, 760), (700, 640))[1:])
    dashed(sh, route, on=18, off=10, width=2.6)
    sh.poly(ellipse(320, 780, 14, 14, n=12))
    sh.text('START', 240, 835, size=20)
    px, py = 700, 640
    sh.line(bez((px, py), (px - 34, py - 40), (px - 30, py - 80), (px, py - 80)) + bez((px, py - 80), (px + 30, py - 80), (px + 34, py - 40), (px, py))[1:], width=2.6)
    sh.poly(ellipse(px, py - 56, 10, 10, n=10), width=2, passes=1)
    blk = [(620, 500), (740, 500), (740, 560), (620, 560)]
    sh.poly(blk, width=2.2)
    sh.hatch(blk, angle=45, spacing=6)
    sh.text('THE LOCAL', 760, 545, size=20)
    sh.text('RUN CLUB ROUTE', 80, 110, size=36, rot=-0.02)
    sh.text('5K', 900, 140, size=34, rot=0.03)
    sh.text('THEN DINNER', 760, 920, size=22)
    return sh


def sheet_hello():
    sh = Sheet(177)
    cx, cy, r = 550, 500, 150
    sh.poly(ellipse(cx, cy, r, r, n=60))
    sh.poly(ellipse(cx, cy, r - 14, r - 14, n=60), width=1.7, passes=1)
    words = ['HOLA', 'BONJOUR', 'CIAO', 'HALLO', 'OLA', 'HI']
    for k in range(6):
        a = k * math.pi / 3 - math.pi / 2
        sx, sy = cx + (r + 46) * math.cos(a), cy + (r + 46) * math.sin(a)
        sh.poly(rotate(rrect(sx - 32, sy - 24, 64, 48, 10), sx, sy, a + math.pi / 2), width=2.3)
        px, py = cx + (r - 48) * math.cos(a), cy + (r - 48) * math.sin(a)
        sh.poly(ellipse(px, py, 24, 24, n=18), width=2.0)
        sh.poly(ellipse(px, py, 14, 14, n=14), width=1.6, passes=1)
        bx, by = cx + (r + 230) * math.cos(a) * 1.15, cy + (r + 160) * math.sin(a)
        w = 34 + len(words[k]) * 19
        sh.poly(ellipse(bx, by, w / 2 + 14, 34, n=30), width=2.2)
        tx, ty = cx + (r + 90) * math.cos(a), cy + (r + 86) * math.sin(a)
        mx, my = bx + (tx - bx) * 0.42, by + (ty - by) * 0.42
        sh.line([(mx - 8, my - 6), (tx, ty), (mx + 8, my + 6)], width=2.0, passes=1)
        sh.text(words[k], bx, by + 10, size=22, anchor='middle')
    sh.text('LANGUAGE NIGHT', 60, 80, size=32, rot=-0.02)
    return sh


def sheet_logo():
    sh = Sheet(189)
    sh.poly(egg(200, 330, 1.2)[:-1])
    sh.poly(ellipse(200, 370, 44, 44, n=20), width=2.2)
    sh.hatch(ellipse(200, 370, 40, 40, n=16)[:-1], angle=40, spacing=6)
    hx, hy = 560, 360
    sh.poly([(hx - 130, hy + 120), (hx - 130, hy - 30), (hx, hy - 150), (hx + 130, hy - 30), (hx + 130, hy + 120)])
    sh.poly(egg(hx, hy + 30, 0.8)[:-1], width=2.3)
    sh.line([(hx - 150, hy - 20), (hx, hy - 170), (hx + 150, hy - 20)], width=2.0, passes=1)
    ex, ey = 880, 330
    sh.poly(ellipse(ex, ey, 90, 90, n=40))
    sh.text('C', ex - 30, ey + 40, size=80, width=3)
    sh.line([(ex - 110, ey - 110), (ex + 110, ey + 110)], width=2.6)
    sh.line([(ex + 110, ey - 110), (ex - 110, ey + 110)], width=2.6)
    sh.text('COOP', 140, 740, size=110, rot=-0.02, width=3.2)
    sh.text('C O O P', 640, 700, size=48, width=2.2)
    sh.text('COOP.', 650, 800, size=48, width=2.2)
    sh.text('THIS ONE', 470, 120, size=26)
    sh.arrow(bez((540, 140), (560, 170), (565, 190), (562, 205)), head=10)
    sh.text('LOGO?', 70, 110, size=36)
    sh.text('TOO SERIOUS', 810, 480, size=20)
    return sh


def sheet_phone():
    sh = Sheet(201)
    for k, (cx, cy, a) in enumerate(((330, 520, -0.12), (770, 540, 0.1))):
        sh.poly(rotate(rrect(cx - 150, cy - 300, 300, 600, 42), cx, cy, a))
        sh.poly(rotate(rrect(cx - 132, cy - 280, 264, 560, 30), cx, cy, a), width=2.0, passes=1)
        sh.poly(rotate(rrect(cx - 40, cy - 268, 80, 22, 11), cx, cy, a), width=1.8, passes=1)
        sh.hatch(rotate([(cx + 150, cy - 260), (cx + 162, cy - 250), (cx + 162, cy + 290), (cx + 150, cy + 290)], cx, cy, a), angle=80, spacing=4)
        if k == 0:
            sh.poly(rotate(rrect(cx - 110, cy - 200, 210, 90, 18), cx, cy, a), width=2.2)
            for i, t in enumerate(('BOOK CLUB', 'TONIGHT 7PM')):
                p = rotate([(cx - 92, cy - 166 + i * 36)], cx, cy, a)[0]
                sh.text(t, p[0], p[1], size=20, rot=a, width=1.8)
            sh.poly(rotate(rrect(cx - 20, cy - 70, 130, 64, 18), cx, cy, a), width=2.2)
            p = rotate([(cx + 45, cy - 28)], cx, cy, a)[0]
            sh.text("I'M IN!", p[0], p[1], size=22, rot=a, anchor='middle')
        else:
            p = rotate([(cx, cy - 130)], cx, cy, a)[0]
            sh.text('TUE', p[0], p[1], size=70, rot=a, anchor='middle', width=3)
            p = rotate([(cx, cy - 40)], cx, cy, a)[0]
            sh.text('18 GOING', p[0], p[1], size=30, rot=a, anchor='middle')
            for i in range(5):
                c = rotate([(cx - 90 + i * 45, cy + 40)], cx, cy, a)[0]
                sh.poly(ellipse(c[0], c[1], 18, 18, n=14), width=2.0)
            sh.poly(rotate(rrect(cx - 100, cy + 130, 200, 70, 30), cx, cy, a), width=2.4)
            p = rotate([(cx, cy + 178)], cx, cy, a)[0]
            sh.text('RSVP', p[0], p[1], size=26, rot=a, anchor='middle')
    sh.text('NO APP NEEDED', 340, 110, size=30, rot=-0.02)
    sh.text('JUST A TEXT', 380, 152, size=22, rot=-0.02, width=1.8)
    return sh


def sheet_receipt():
    sh = Sheet(213)
    x0, x1, y0, y1 = 330, 770, 150, 860
    n = int((x1 - x0) / 20)
    zz_top = [(x0 + i * 20, y0 + (10 if i % 2 else 0)) for i in range(n + 1)]
    zz_bot = [(x1 - i * 20, y1 - (10 if i % 2 else 0)) for i in range(n + 1)]
    sh.poly(zz_top + zz_bot)
    sh.hatch([(x1, y0 + 20), (x1 + 16, y0 + 36), (x1 + 16, y1 + 10), (x1, y1 - 6)], angle=80, spacing=5)
    sh.text('COOP', 550, 240, size=40, anchor='middle', width=2.6)
    sh.text('EXAMPLE TAB', 550, 290, size=22, anchor='middle', width=1.8)
    y = 380
    for a, b in (('25 X $20', '$500'), ('X 4 TUES', '$2000'), ('FEE 10%', '-$200')):
        sh.text(a, 370, y, size=24)
        sh.text(b, 620, y, size=24)
        y += 70
    dashed(sh, [(370, y - 30), (730, y - 30)], on=10, off=8, width=1.8)
    sh.text('YOURS', 370, y + 30, size=28)
    sh.text('$1800', 610, y + 30, size=28)
    sh.text('NOT A FORECAST', 550, 760, size=20, anchor='middle', width=1.8)
    sh.text('THE MATH', 70, 120, size=36, rot=-0.03)
    sh.text('THANK YOU!', 810, 900, size=22, rot=-0.05)
    return sh


SHEETS = {
    'table-for-twenty': sheet_table,
    'bistro-chair': sheet_chair,
    'storefront': sheet_storefront,
    'tuesday-calendar': sheet_calendar,
    'reserved-card': sheet_card,
    'supper-club': sheet_supper,
    'club-kit': sheet_clubkit,
    'floor-plan': sheet_plan,
    'pendant-lamps': sheet_lamps,
    'post-run-coffee': sheet_coffee,
    'game-night': sheet_chess,
    'chair-stack': sheet_stack,
    'a-boards': sheet_boards,
    'run-route': sheet_route,
    'language-night': sheet_hello,
    'logo-ideas': sheet_logo,
    'no-app-needed': sheet_phone,
    'the-math': sheet_receipt,
}

if __name__ == '__main__':
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    only = sys.argv[2:] or list(SHEETS)
    for name in only:
        (out / f'{name}.svg').write_text(SHEETS[name]().svg(), encoding='utf-8')
        print('wrote', name)
