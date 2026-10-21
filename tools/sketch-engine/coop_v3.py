"""Sketches for the v3 site: every drawing has one job and appears once.

    python coop_v3.py ../../public/img/sketches

How it works (match green):  intro-cards, who-gets-along, weekly-calendar
For clubs (club orange):     group-chat, reserved-card
First flock (regulars red):  pilot-map
Venues keep corner-booth and floor-plan (venue blue); the join panel keeps name-tags.
"""
import math
import sys
from pathlib import Path

import sketch as S
from sketch import Sheet, rrect, rotate, ellipse, bez, dashed

VENUE, CLUB, MATCH, REGULARS = '#3E7396', '#C4572B', '#7B7A2C', '#B8232F'


def tick(sh, x, y, k=1.0):
    sh.line([(x, y), (x + 12 * k, y + 14 * k), (x + 34 * k, y - 18 * k)], width=2.8, passes=1)


def card(sh, cx, cy, w, h, a, lines, title, fill='yolk'):
    """A handwritten index card, slightly turned, with tape on top."""
    body = rotate(rrect(cx - w / 2, cy - h / 2, w, h, 10), cx, cy, a)
    sh.poly(body)
    sh.marker(rotate([(cx - w / 2 + 6, cy - h / 2 + 6), (cx + w / 2 - 6, cy - h / 2 + 6),
                      (cx + w / 2 - 6, cy - h / 2 + 58), (cx - w / 2 + 6, cy - h / 2 + 58)], cx, cy, a), fill, opacity=0.7)
    tape = rotate(rrect(cx + w / 2 - 110, cy - h / 2 - 24, 90, 38, 4), cx, cy, a + 0.12)
    sh.poly(tape, width=1.8, passes=1)
    sh.hatch(tape, angle=70, spacing=9, width=1.4)
    p = rotate([(cx - w / 2 + 26, cy - h / 2 + 44)], cx, cy, a)[0]
    sh.text(title, p[0], p[1], size=23, rot=a, width=2.2)
    for i, t in enumerate(lines):
        y = cy - h / 2 + 112 + i * 56
        sh.line(rotate([(cx - w / 2 + 24, y + 12), (cx + w / 2 - 24, y + 12)], cx, cy, a), width=1.2, passes=1, wobble=0.8)
        p = rotate([(cx - w / 2 + 28, y)], cx, cy, a)[0]
        sh.text(t, p[0], p[1], size=24, rot=a, width=1.9)


def sheet_intro_cards():
    """01 Tell us a little about yourself: a club and a venue each fill in a card."""
    sh = Sheet(901)
    card(sh, 330, 560, 470, 330, -0.07, ['14 OF US, USUALLY', 'WEDNESDAYS', 'A QUIET CORNER'], 'CHELSEA KNITTERS')
    card(sh, 790, 470, 450, 330, 0.06, ['BACK ROOM FOR 20', 'SLOW ON MON + WED', 'LONG TABLE'], 'THE CORNER CAFE')
    pen = rotate(rrect(880, 700, 40, 250, 16), 900, 825, 0.7)
    sh.poly(pen)
    sh.marker(pen, 'yolk', opacity=0.6)
    sh.hatch(rotate([(884, 706), (916, 706), (916, 770), (884, 770)], 900, 825, 0.7), angle=10, spacing=5)
    sh.text('TELL US A LITTLE', 70, 110, size=38, rot=-0.02)
    sh.text('BOTH SIDES, TWO MINUTES', 74, 160, size=22, rot=-0.02, width=1.9)
    return sh


def sheet_who_gets_along():
    """02 We'll see who might get along: where the club and the venue overlap."""
    sh = Sheet(917)
    lx, rx, cy, r = 430, 680, 520, 235
    sh.poly(ellipse(lx, cy, r, r, n=70))
    sh.poly(ellipse(rx, cy, r, r, n=70))
    lens = [p for p in ellipse(lx, cy, r - 8, r - 8, n=90) if math.hypot(p[0] - rx, p[1] - cy) < r - 8]
    lens += [p for p in ellipse(rx, cy, r - 8, r - 8, n=90)[::-1] if math.hypot(p[0] - lx, p[1] - cy) < r - 8][::-1]
    sh.marker(lens, 'yolk', opacity=0.75, spacing=9)
    sh.text('THE CLUB', lx - 150, cy - 120, size=23, width=2.1)
    for i, t in enumerate(('KNITTING', '14 PEOPLE', 'LIKES QUIET')):
        sh.text(t, lx - 165, cy - 40 + i * 48, size=20, width=1.7)
    sh.text('THE VENUE', rx + 22, cy - 120, size=23, width=2.1)
    for i, t in enumerate(('BACK ROOM', 'FITS 20', 'SLOW WEDS')):
        sh.text(t, rx + 50, cy - 40 + i * 48, size=20, width=1.7)
    sh.text('WEDS', 555, cy - 14, size=30, anchor='middle', width=2.6)
    sh.text('NEARBY', 555, cy + 32, size=20, anchor='middle', width=1.8)
    # both say yes, underneath
    for i, (x, who) in enumerate(((300, 'CLUB'), (640, 'VENUE'))):
        box = rrect(x, 810, 46, 46, 6)
        sh.poly(box, width=2.2, passes=1)
        tick(sh, x + 6, 830, 1.0)
        sh.text(who + ' SAYS YES', x + 70, 846, size=24, width=2.0)
    sh.text('WHO MIGHT GET ALONG', 70, 110, size=38, rot=-0.02)
    sh.text('NOTHING BOOKED TILL BOTH SAY YES', 74, 160, size=22, rot=-0.02, width=1.9)
    return sh


def sheet_group_chat():
    """For clubs, the problem: the weekly 'where are we meeting?' thread."""
    sh = Sheet(931)
    cx, cy, a = 560, 540, -0.05
    R = lambda pts: rotate(pts, cx, cy, a)
    sh.poly(R(rrect(cx - 190, cy - 360, 380, 720, 48)))
    sh.poly(R(rrect(cx - 170, cy - 338, 340, 676, 34)), width=2.0, passes=1)
    sh.poly(R(rrect(cx - 46, cy - 326, 92, 22, 11)), width=1.8, passes=1)
    sh.hatch(R([(cx + 190, cy - 320), (cx + 204, cy - 308), (cx + 204, cy + 350), (cx + 190, cy + 350)]), angle=80, spacing=4)
    sh.text('KNIT CLUB (14)', *R([(cx - 140, cy - 262)])[0], size=22, rot=a, width=2.0)
    sh.line(R([(cx - 160, cy - 244), (cx + 160, cy - 244)]), width=1.6, passes=1)
    msgs = [  # (text, right side?, y)
        ('SO WHERE ARE WE', False, -190), ('MEETING THIS WEEK?', False, -158),
        ('THE CAFE IS FULL', True, -84),
        ('ANYONE? :(', False, -10),
        ('BAR ON 9TH?', True, 64), ('TOO LOUD', True, 96),
        ('SAME QUESTION', False, 170), ('EVERY WEEK...', False, 202),
    ]
    groups = [(0, 2), (2, 3), (3, 4), (4, 6), (6, 8)]
    for g0, g1 in groups:
        right = msgs[g0][1]
        y0, y1 = cy + msgs[g0][2] - 30, cy + msgs[g1 - 1][2] + 16
        w = max(len(m[0]) for m in msgs[g0:g1]) * 14 + 40
        x0 = cx + 150 - w if right else cx - 150
        bubble = R(rrect(x0, y0, w, y1 - y0, 18))
        sh.poly(bubble, width=2.0, passes=1)
        if not right:
            sh.marker(bubble, 'yolk', opacity=0.45, spacing=12)
        for t, _, dy in msgs[g0:g1]:
            sh.text(t, *R([(x0 + 18, cy + dy)])[0], size=19, rot=a, width=1.6)
    sh.text('THE GROUP CHAT', 70, 110, size=38, rot=-0.02)
    sh.text('EVERY. SINGLE. WEEK.', 74, 160, size=22, rot=-0.02, width=1.9)
    return sh


SHEETS = {
    'intro-cards': (sheet_intro_cards, MATCH),
    'who-gets-along': (sheet_who_gets_along, MATCH),
    'group-chat': (sheet_group_chat, CLUB),
    # existing drawings, recoloured for their new place
    'weekly-calendar': (S.sheet_calendar, MATCH),
    'reserved-card': (S.sheet_card, CLUB),
    'pilot-map': (S.sheet_map, REGULARS),
}

# words inside the reused drawings, adjusted for their new job
REWRITES = {
    'weekly-calendar': {'EVERY TUE': 'THEIR NIGHT', '4 WEEK PILOT': 'EVERY WEEK'},
    'reserved-card': {'THE ONLY SIGN': 'A TABLE THAT', 'WE NEED': 'KNOWS YOUR NAME', 'COOP': 'KNIT CLUB'},
}


def render(out, names):
    out.mkdir(parents=True, exist_ok=True)
    for name in names:
        fn, ink = SHEETS[name]
        S.PALETTE = {'yolk': ink, 'dusk': ink, 'ink': ink, 'boost': 0.42}
        S.COLOR_INK = ink
        S.CURRENT_SHEET = name
        S.REWRITES = {name: dict(REWRITES.get(name, {}))}
        (out / f'{name}.svg').write_text(fn().svg(color=True), encoding='utf-8')
        print('wrote', name)


if __name__ == '__main__':
    render(Path(sys.argv[1]), sys.argv[2:] or list(SHEETS))
