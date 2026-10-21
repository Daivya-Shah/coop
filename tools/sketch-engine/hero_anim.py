"""Coop animated hero: club things float into the Coop egg, then fill a venue's empty table.

Usage: python hero_anim.py OUT_DIR
Writes hero-anim.svg (SMIL animation, works inside <img>) and wordmark-light.svg.
"""
import importlib.util, math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE / 'sketch.py' if (HERE / 'sketch.py').exists() else HERE.parent / 'sketches' / 'sketch.py'
_spec = importlib.util.spec_from_file_location('coop_sketch', ENGINE)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
g = _mod.__dict__
Sheet, ellipse, bez, egg, pawn, rrect = (g[k] for k in ('Sheet', 'ellipse', 'bez', 'egg', 'pawn', 'rrect'))

AW, AH = 1200, 760
INK = {'olive': '#7B7A2C', 'teal': '#3E7396', 'rust': '#C4572B', 'crimson': '#B8232F', 'pink': '#D776A8'}
YOLK = '#FFC300'
CYCLE = 7.0   # seconds per loop


def use(hexc, fill=None):
    f = fill or hexc
    g['PALETTE'] = {'yolk': f, 'dusk': f, 'ink': hexc, 'boost': 0.42 if fill is None else 1.0}
    g['COLOR_INK'] = hexc


def frag(sh, ink, fill=None):
    use(ink, fill)
    return re.search(r'</defs>(.*)</svg>', sh.svg(color=True), re.S).group(1)


def draw(fn, seed, ink, fill=None):
    use(ink, fill)
    sh = Sheet(seed)
    fn(sh)
    return frag(sh, ink, fill)


# ---------------------------------------------------------------- club things, drawn around (0, 0)
def yarn(sh):
    sh.poly(ellipse(0, 0, 34, 34, n=28))
    sh.marker(ellipse(0, 0, 31, 31, n=18)[:-1], 'yolk')
    for k in range(4):
        sh.line(ellipse(0, 0, 31, 10 + k * 6, rot=0.5 + k * 0.5, a0=0.2, a1=2.9, n=14), width=1.7, passes=1)
    sh.line([(-18, -62), (16, 6)], width=2.4)
    sh.line([(26, -66), (-4, 4)], width=2.4)


def books(sh):
    for i, (dx, rot) in enumerate(((0, -0.06), (4, 0.05), (-3, -0.02))):
        q = [(dx - 46, -i * 16), (dx + 46, -i * 16), (dx + 46, -i * 16 - 14), (dx - 46, -i * 16 - 14)]
        q = [(x * math.cos(rot) - y * math.sin(rot), x * math.sin(rot) + y * math.cos(rot)) for x, y in q]
        sh.poly(q, width=2.4)
        if i != 1:
            sh.marker(q, 'yolk', spacing=6, width=7)
        sh.line([q[0], q[3]], width=1.6, passes=1)


def sneaker(sh):
    s = 0.36
    T = lambda pts: [(x * s - 54, y * s - 40) for x, y in pts]
    up = bez((10, 140), (0, 60), (30, 40), (70, 40)) + bez((70, 40), (120, 40), (150, 70), (200, 80))[1:] + bez((200, 80), (260, 90), (300, 110), (300, 140))[1:]
    sh.line(T(up))
    sh.poly(T([(4, 140), (304, 140), (300, 162), (10, 162)]))
    sh.marker(T(up + [(300, 140), (10, 140)]), 'yolk')
    for k in range(4):
        x = 100 + k * 18
        sh.line(T([(x, 52 + k * 4), (x + 20, 74 + k * 3)]), width=1.8, passes=1)


def palette(sh):
    pal = [(54 * math.cos(t) * (1 + 0.08 * math.sin(3 * t)), 38 * math.sin(t)) for t in [i * 2 * math.pi / 36 for i in range(36)]]
    sh.poly(pal)
    sh.marker(pal, 'yolk', opacity=0.45)
    sh.poly(ellipse(24, 12, 9, 7, n=10), width=1.9, passes=1)
    for dx, dy in ((-26, -10), (-4, -21), (16, -17), (-30, 12)):
        sh.poly(ellipse(dx, dy, 7, 6, n=10), width=1.7, passes=1)
        sh.marker(ellipse(dx, dy, 6, 5, n=8)[:-1], 'yolk', spacing=4, width=5, shift=1)
    sh.line([(16, -58), (66, -100)], width=2.6)


def chesspiece(sh):
    pawn(sh, 0, 44, k=0.55, shade=True)


def hola(sh):
    sh.poly(ellipse(0, 0, 58, 28, n=26), width=2.3)
    sh.line([(-22, 24), (-38, 48), (-4, 27)], width=2.2)
    sh.text('HOLA!', 0, 10, size=22, anchor='middle')


ITEMS = [  # drawing, ink, start point, control points into the egg
    (yarn, 'rust', (110, 230)),
    (books, 'teal', (270, 190)),
    (sneaker, 'pink', (120, 420)),
    (palette, 'crimson', (270, 340)),
    (chesspiece, 'olive', (110, 620)),
    (hola, 'teal', (270, 580)),
]
EGG = (560, 400)


def item_group(i, fn, ink, start):
    art = draw(fn, 1001 + i, INK[ink])
    sx, sy = start
    ex, ey = EGG
    c1 = (sx + 160, sy + (ey - sy) * 0.1 - 40)
    c2 = (ex - 140, ey - (ey - sy) * 0.15)
    path = f'M{sx} {sy} C {c1[0]:.0f} {c1[1]:.0f}, {c2[0]:.0f} {c2[1]:.0f}, {ex} {ey}'
    begin = f'{-i * CYCLE / len(ITEMS):.2f}s'
    bob = f'<animateTransform attributeName="transform" type="translate" values="0 0; 0 -6; 0 0" dur="{2.2 + i * 0.3:.1f}s" repeatCount="indefinite" additive="sum"/>'
    return (f'<g>'
            f'<animateMotion dur="{CYCLE}s" begin="{begin}" repeatCount="indefinite" calcMode="linear" '
            f'keyPoints="0;0;1;1" keyTimes="0;0.35;0.8;1" path="{path}"/>'
            f'<animate attributeName="opacity" dur="{CYCLE}s" begin="{begin}" repeatCount="indefinite" '
            f'values="1;1;1;0;0;1" keyTimes="0;0.35;0.74;0.82;0.92;1"/>'
            f'<g>{bob}<g><animateTransform attributeName="transform" type="scale" dur="{CYCLE}s" begin="{begin}" repeatCount="indefinite" '
            f'values="1;1;0.45;0.45;1" keyTimes="0;0.35;0.8;0.92;1"/>{art}</g></g></g>'), path


# ---------------------------------------------------------------- coop egg
def coop_egg(sh):
    ex, ey = EGG
    sh.poly(egg(ex, ey, 1.05)[:-1], width=3.2)
    for t in range(200, 350, 30):
        r = math.radians(t)
        sh.line([(ex + 112 * math.cos(r), ey + 10 + 124 * math.sin(r)), (ex + 130 * math.cos(r), ey + 10 + 142 * math.sin(r))], width=1.8, passes=1, over=1)
    sh.text('COOP', ex, ey + 168, size=34, anchor='middle', width=2.6)
    sh.text('MATCHES THEM', ex, ey + 204, size=20, anchor='middle', width=1.9)


def yolk_art(sh):
    for ang in (30, 120):
        sh.marker(ellipse(0, 0, 36, 36, n=30)[:-1], 'yolk', angle=ang, opacity=1.0, spacing=4.5, width=4.5, shift=1)


# ---------------------------------------------------------------- the venue table, from above
TX, TY, TR, CR = 985, 400, 88, 142
N_CHAIRS = 8


def table_art(sh):
    sh.poly(ellipse(TX, TY, TR, TR, n=40))
    sh.poly(ellipse(TX, TY, TR - 10, TR - 10, n=40), width=1.6, passes=1)
    sh.marker(ellipse(TX, TY, TR - 6, TR - 6, n=24)[:-1], 'dusk', opacity=0.35, spacing=14)
    for a in range(N_CHAIRS):
        t = a * 2 * math.pi / N_CHAIRS
        cx, cy = TX + CR * math.cos(t), TY + CR * math.sin(t)
        sh.poly(rotate_pts(rrect(cx - 26, cy - 22, 52, 44, 10), cx, cy, t + math.pi / 2), width=2.3)
    # plates appear as the table fills (drawn static, faint)
    for a in range(N_CHAIRS):
        t = a * 2 * math.pi / N_CHAIRS
        px, py = TX + (TR - 30) * math.cos(t), TY + (TR - 30) * math.sin(t)
        sh.poly(ellipse(px, py, 11, 11, n=12), width=1.5, passes=1)


def rotate_pts(pts, cx, cy, a):
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def seat_fill(i):
    t = i * 2 * math.pi / N_CHAIRS

    def fn(sh):
        cx, cy = TX + CR * math.cos(t), TY + CR * math.sin(t)
        q = rotate_pts(rrect(cx - 24, cy - 20, 48, 40, 9), cx, cy, t + math.pi / 2)
        for ang in (25, 115):
            sh.marker(q, 'yolk', angle=ang, opacity=0.95, spacing=5, width=5, shift=1.5)
    return fn


def venue_labels(sh):
    sh.text('A SLOW NIGHT', TX, 150, size=30, anchor='middle', width=2.4)
    sh.text('EMPTY SEATS...', TX, 186, size=20, anchor='middle', width=1.9)
    sh.text('...NOW REGULARS', TX, 700, size=22, anchor='middle', width=2.0)


def club_labels(sh):
    sh.text('THE CLUBS', 60, 60, size=30, width=2.4)
    sh.text('KNIT, READ, RUN, PAINT, PLAY, TALK', 62, 94, size=17, width=1.7)


def build(out):
    out.mkdir(parents=True, exist_ok=True)
    g['W'], g['H'] = AW, AH
    parts = []
    parts.append(draw(club_labels, 1101, INK['rust']))
    parts.append(draw(venue_labels, 1102, INK['crimson']))
    # path from egg to table: moving dashes
    parts.append(f'<path d="M668 400 C 720 380, 750 380, 790 396" stroke="{INK["olive"]}" stroke-width="4" '
                 f'stroke-linecap="round" stroke-dasharray="4 14" fill="none">'
                 f'<animate attributeName="stroke-dashoffset" values="36;0" dur="0.9s" repeatCount="indefinite"/></path>'
                 f'<path d="M779 384 L795 397 L778 410" stroke="{INK["olive"]}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')
    parts.append(draw(table_art, 1103, INK['teal']))
    # seats fill one by one, hold, then reset
    for i in range(N_CHAIRS):
        on = 0.12 + i * 0.085
        art = draw(seat_fill(i), 1200 + i, INK['crimson'], YOLK)
        parts.append(f'<g opacity="0"><animate attributeName="opacity" dur="{CYCLE * 1.6:.1f}s" repeatCount="indefinite" '
                     f'values="0;0;1;1;0" keyTimes="0;{on:.3f};{on + 0.03:.3f};0.93;1"/>{art}</g>')
    # FULL! sticker
    full = draw(lambda sh: (sh.poly(rrect(TX - 65, TY + 166, 130, 50, 14), width=2.6),
                            sh.marker(rrect(TX - 65, TY + 166, 130, 50, 14), 'yolk', opacity=1.0, spacing=5, width=6),
                            sh.text('FULL!', TX, TY + 202, size=28, anchor='middle', width=2.6)), 1300, INK['crimson'], YOLK)
    parts.append(f'<g opacity="0"><animate attributeName="opacity" dur="{CYCLE * 1.6:.1f}s" repeatCount="indefinite" '
                 f'values="0;0;1;1;0" keyTimes="0;0.8;0.83;0.93;1"/>{full}</g>')
    # the egg + pulsing yolk
    parts.append(draw(coop_egg, 1104, INK['olive']))
    yolk = draw(yolk_art, 1105, INK['olive'], YOLK)
    parts.append(f'<g transform="translate({EGG[0]} {EGG[1] + 18})"><g>'
                 f'<animateTransform attributeName="transform" type="scale" values="1;1.12;1" dur="1.4s" repeatCount="indefinite"/>'
                 f'{yolk}</g></g>')
    # club things travelling in (drawn last so they pass over the egg)
    for i, (fn, ink, start) in enumerate(ITEMS):
        grp, _ = item_group(i, fn, ink, start)
        parts.append(grp)
    defs = ('<defs><filter id="ink" x="-2%" y="-2%" width="104%" height="104%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="4"/>'
            '<feDisplacementMap in="SourceGraphic" scale="1.6"/></filter></defs>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{AW}" height="{AH}" viewBox="0 0 {AW} {AH}" fill="none">'
           + defs + ''.join(parts) + '</svg>')
    (out / 'hero-anim.svg').write_text(svg, encoding='utf-8')

    # light wordmark for the dark footer
    src = (out / 'wordmark.svg')
    if src.exists():
        (out / 'wordmark-light.svg').write_text(src.read_text(encoding='utf-8').replace('#121212', '#f5f5f5'), encoding='utf-8')
    print('wrote hero-anim.svg and wordmark-light.svg')


if __name__ == '__main__':
    build(Path(sys.argv[1]))
