# -*- coding: utf-8 -*-
"""Shared page furniture for the VELUM manual."""
from core import *

def head(L, sec, num, eyebrow, title, sub=None):
    """Standard page top: chrome + eyebrow + Cinzel title (+ optional lead)."""
    o = [chrome(sec, num, L["total"], sub=L["manual"])]
    o.append(label(M, 210, eyebrow, fill=AMBER))
    o.append(t(M, 300, title, size=52, f=DIS, w=400, fill=TXT, ls=2.5))
    if sub:
        o.append(para(M, 356, sub, size=16, lh=27, fill=GREY))
    return o

def divider(L, num, no, title, sub):
    """Full-bleed section divider on Azul Velum."""
    o = [rect(0, 0, W, H, INK)]
    o.append(veil(0, 300, W, 520, n=14, stroke=GOLD, sw=1.1, op=0.14, spread=1.2))
    o.append(rect(56, 56, W - 112, H - 112, "none", stroke=PEARL, sw=0.8, op=0.22))
    o.append(t(M + 40, 470, no, size=150, f=DIS, w=400, fill=GOLD, op=0.9, ls=4))
    o.append(t(M + 40, 610, title.upper(), size=76, f=DIS, w=400, fill=IVORY, ls=4))
    o.append(line(M + 40, 668, M + 240, 668, stroke=GOLD, sw=1.2))
    o.append(t(M + 40, 726, sub, size=18, fill=PEARL, op=0.85))
    o.append(mono_logo(W - M - 220, 380, 180, "dark"))
    o.append(label(M + 40, H - 100, L["brand"], fill=PEARL, size=10))
    o.append(t(W - M - 40, H - 98, "%02d" % num, size=15, w=600, fill=PEARL, ls=1, anchor="end"))
    o.append(t(W - M - 76, H - 98, "/ %02d" % L["total"], size=15, w=400, fill=PEARL,
               ls=1, anchor="end", op=0.5))
    return page("".join(o), bg=INK)

ICON_PATHS = {
    "plane": "M6 27 L42 17 M6 27 L18 31 L14 41 L20 33 L34 37 M42 17 L34 37",
    "bottle": "M19 6 h10 v7 h-10 z M17 13 h14 c3 6 4 9 4 14 v13 a4 4 0 0 1 -4 4 h-14 a4 4 0 0 1 -4 -4 "
              "v-13 c0 -5 1 -8 4 -14 z M19 26 h10",
    "cloche": "M6 39 h36 M10 39 a14 15 0 0 1 28 0 M24 10 v-5 M20.5 5 h7",
    "globe": "M24 6 a18 18 0 1 0 0 36 a18 18 0 1 0 0 -36 M6 24 h36 M24 6 c-8 8 -8 28 0 36 M24 6 c8 8 8 28 0 36",
    "building": "M10 42 v-30 h14 v30 M24 42 v-20 h14 v20 M14 18 h6 M14 26 h6 M14 34 h6 M28 28 h6 M28 36 h6 M6 42 h36",
    "car": "M9 30 l4 -9 a4 4 0 0 1 3.6 -2.4 h14.8 a4 4 0 0 1 3.6 2.4 l4 9 M7 30 h34 v7 h-34 z "
           "M13 37 v3.5 M35 37 v3.5 M15.5 33.5 h4 M28.5 33.5 h4",
}

def icon(kind, x, y, s=1.0, stroke=None, sw=1.6):
    c = stroke or AMBER
    return ('<g transform="translate(%.1f %.1f) scale(%.3f)" fill="none" stroke="%s" '
            'stroke-width="%.2f" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="%s"/></g>') % (x, y, s, c, sw, ICON_PATHS[kind])

def yes_no(x_yes, x_no, y, yes_h, no_h, yes, no, lh=54, size=20):
    """Two facing lists: what it is / what it is not."""
    o = [label(x_yes, y, yes_h, fill=AMBER, size=11), label(x_no, y, no_h, fill=CLAY, size=11)]
    for i, v in enumerate(yes):
        yy = y + 56 + i * lh
        o.append(t(x_yes, yy, v, size=size, fill=TXT, op=0.92))
        o.append(line(x_yes, yy + 20, x_yes + 560, yy + 20, stroke=INK, sw=0.7, op=0.12))
    for i, v in enumerate(no):
        yy = y + 56 + i * lh
        o.append(t(x_no, yy, v, size=size, fill=GREY))
        o.append(line(x_no, yy + 20, x_no + 560, yy + 20, stroke=INK, sw=0.7, op=0.12))
    return o

def foot(lines, y=1000, size=14):
    return para(M, y, lines, size=size, lh=24, fill=GREY)
