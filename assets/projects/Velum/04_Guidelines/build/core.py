# -*- coding: utf-8 -*-
import re, os
B = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080
M = 130

# Palette from the VELUM master plan board (Aug 2026)
GROUND = "#F4F0EE"   # Blanco Hueso - main background
INK    = "#0B1D34"   # Azul Velum   - ink and dark panels
NAVY   = "#20344D"   # Azul Medio
NAVY2  = "#16283A"
SKY    = "#20344D"
SKY_L  = "#DADDE3"   # Gris Perla
GOLD   = "#D4AF37"   # Oro Velum    - graphic accent
AMBER  = "#B8912B"   # Oro oscuro   - gold that reads as text on light
IVORY  = "#F7F7F7"   # Blanco       - text on dark panels
TXT    = "#0B1D34"   # text on light ground
BLACK  = "#1A1A1A"
PAPER  = "#E8DCC0"   # Crema
PEARL  = "#DADDE3"
GREY   = "#55585F"
MUTED  = "#55585F"
CLAY   = "#8C5A3C"

DIS = "Cinzel, Cormorant Garamond, Georgia, serif"    # display / titles (caps)
SER = "Cormorant Garamond, Georgia, serif"            # editorial fallback
SAN = "Montserrat, Poppins, Arial, sans-serif"        # everything functional

_full = open(B + "/full.frag", encoding="utf-8").read()
_mono = open(B + "/mono.frag", encoding="utf-8").read()

def _color(frag, mapping):
    out = frag
    for k, v in mapping.items():
        out = out.replace('class="%s"' % k, 'fill="%s"' % v)
    return out

def full_logo(x, y, w, mode="dark"):
    sc = w / 141.57
    mp = {"dark":  {"cls-1": GOLD,  "cls-2": IVORY, "cls-3": SKY_L},
          "light": {"cls-1": GOLD,  "cls-2": BLACK, "cls-3": NAVY},
          "ivory": {"cls-1": IVORY, "cls-2": IVORY, "cls-3": IVORY},
          "navy":  {"cls-1": NAVY,  "cls-2": NAVY,  "cls-3": NAVY},
          "gold":  {"cls-1": GOLD,  "cls-2": GOLD,  "cls-3": GOLD}}[mode]
    return '<g transform="translate(%.2f %.2f) scale(%.5f)">%s</g>' % (x, y, sc, _color(_full, mp))

def mono_logo(x, y, w, mode="dark"):
    sc = w / 56.34
    mp = {"dark":  {"cls-1": SKY_L, "cls-2": GOLD,  "cls-3": IVORY},
          "light": {"cls-1": NAVY,  "cls-2": GOLD,  "cls-3": BLACK},
          "ivory": {"cls-1": IVORY, "cls-2": IVORY, "cls-3": IVORY},
          "navy":  {"cls-1": NAVY,  "cls-2": NAVY,  "cls-3": NAVY},
          "gold":  {"cls-1": GOLD,  "cls-2": GOLD,  "cls-3": GOLD}}[mode]
    return '<g transform="translate(%.2f %.2f) scale(%.5f)">%s</g>' % (x, y, sc, _color(_mono, mp))

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def t(x, y, s, size=16, f=SAN, w=400, fill=TXT, ls=0, anchor="start", op=1.0, italic=False):
    a = ['x="%.1f"' % x, 'y="%.1f"' % y, 'font-family="%s"' % f,
         'font-size="%.1f"' % size, 'font-weight="%s"' % w, 'fill="%s"' % fill]
    if ls: a.append('letter-spacing="%.2f"' % ls)
    if anchor != "start": a.append('text-anchor="%s"' % anchor)
    if op != 1.0: a.append('opacity="%.2f"' % op)
    if italic: a.append('font-style="italic"')
    return "<text %s>%s</text>" % (" ".join(a), esc(s))

def label(x, y, s, fill=AMBER, size=12, anchor="start", w=600):
    return t(x, y, s.upper(), size=size, w=w, fill=fill, ls=3.4, anchor=anchor)

def para(x, y, lines, size=18, lh=32, fill=TXT, op=0.78, f=SAN, w=400, anchor="start", italic=False):
    return "".join(t(x, y + i * lh, l, size=size, fill=fill, op=op, f=f, w=w, anchor=anchor, italic=italic)
                   for i, l in enumerate(lines))

def rect(x, y, w, h, fill, op=1.0, rx=0, stroke=None, sw=1):
    a = 'x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"' % (x, y, w, h, fill)
    if rx: a += ' rx="%.1f"' % rx
    if op != 1.0: a += ' opacity="%.2f"' % op
    if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
    return "<rect %s/>" % a

def line(x1, y1, x2, y2, stroke=GOLD, sw=1, op=1.0, dash=None):
    a = 'x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.2f"' % (x1, y1, x2, y2, stroke, sw)
    if op != 1.0: a += ' opacity="%.2f"' % op
    if dash: a += ' stroke-dasharray="%s"' % dash
    return "<line %s/>" % a

def circ(cx, cy, r, fill="none", stroke=None, sw=1, op=1.0, dash=None):
    a = 'cx="%.1f" cy="%.1f" r="%.1f" fill="%s"' % (cx, cy, r, fill)
    if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
    if op != 1.0: a += ' opacity="%.2f"' % op
    if dash: a += ' stroke-dasharray="%s"' % dash
    return "<circle %s/>" % a

def star(cx, cy, r, fill=GOLD, op=1.0):
    k = r * 0.145
    d = ("M %.2f %.2f Q %.2f %.2f %.2f %.2f Q %.2f %.2f %.2f %.2f "
         "Q %.2f %.2f %.2f %.2f Q %.2f %.2f %.2f %.2f Z") % (
        cx, cy - r, cx + k, cy - k, cx + r, cy,
        cx + k, cy + k, cx, cy + r,
        cx - k, cy + k, cx - r, cy,
        cx - k, cy - k, cx, cy - r)
    return '<path d="%s" fill="%s"%s/>' % (d, fill, "" if op == 1 else ' opacity="%.2f"' % op)

def sweep(x, y, w, stroke=INK, sw=3, op=1.0, rise=None):
    h = w * 0.28 if rise is None else rise
    d = "M %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f" % (
        x, y + h, x + w * 0.30, y + h * 0.30, x + w * 0.62, y + h * 0.03, x + w, y)
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round"%s/>' % (
        d, stroke, sw, "" if op == 1 else ' opacity="%.2f"' % op)

def veil(x, y, w, h, n=9, stroke=None, sw=1.4, op=0.55, spread=1.0, phase=0.0):
    """The veil: parallel flowing curves. One device, many readings."""
    c = stroke or GOLD
    o = ['<g opacity="%.2f">' % op]
    for i in range(n):
        f = i / float(max(1, n - 1))
        yy = y + h * f
        amp = h * 0.42 * spread * (0.45 + 0.55 * (1 - abs(f - 0.5) * 2))
        d = ("M %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f S %.1f %.1f %.1f %.1f") % (
            x, yy,
            x + w * 0.22, yy - amp * (1 + phase * 0.1),
            x + w * 0.40, yy + amp * 0.55,
            x + w * 0.58, yy - amp * 0.10,
            x + w * 0.86, yy - amp * 0.85,
            x + w, yy - amp * 0.55)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round"/>'
                 % (d, c, sw))
    o.append("</g>")
    return "".join(o)

def img(name, x, y, w, h, op=1.0, clip=None):
    d = open(B + "/" + name, encoding="utf-8").read()
    a = 'x="%.1f" y="%.1f" width="%.1f" height="%.1f" preserveAspectRatio="xMidYMid slice"' % (x, y, w, h)
    if op != 1.0: a += ' opacity="%.2f"' % op
    if clip: a += ' clip-path="url(#%s)"' % clip
    return '<image %s href="data:image/jpeg;base64,%s"/>' % (a, d)

_cid = [0]
def _clip(x, y, w, h):
    _cid[0] += 1
    i = "c%d" % _cid[0]
    return i, '<clipPath id="%s"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath>' % (i, x, y, w, h)

def diag(x, y, w, h, stroke=INK, sw=1.6, gap=16, op=0.30):
    """35-degree screen drawn as real lines (Figma-safe)."""
    i, cp = _clip(x, y, w, h)
    o = [cp, '<g clip-path="url(#%s)" opacity="%.2f">' % (i, op)]
    span = int((w + h * 2) / gap) + 2
    for k in range(-span, span):
        x0 = x + k * gap
        o.append(line(x0, y - h, x0 + h * 1.4 + w, y + h * 1.6, stroke=stroke, sw=sw))
    o.append("</g>")
    return "".join(o)

def grid(x, y, w, h, stroke=INK, sw=0.6, step=40, op=0.16):
    """Construction grid drawn as real lines (Figma-safe)."""
    o = ['<g opacity="%.2f">' % op]
    k = 0
    while x + k * step <= x + w:
        o.append(line(x + k * step, y, x + k * step, y + h, stroke=stroke, sw=sw)); k += 1
    k = 0
    while y + k * step <= y + h:
        o.append(line(x, y + k * step, x + w, y + k * step, stroke=stroke, sw=sw)); k += 1
    o.append("</g>")
    return "".join(o)

DEFS = """
<defs>
  <linearGradient id="gGround" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#F4F0EE"/><stop offset="0.55" stop-color="#EFEAE6"/><stop offset="1" stop-color="#F4F0EE"/>
  </linearGradient>
  <linearGradient id="gDark" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0B1D34"/><stop offset="0.55" stop-color="#162943"/><stop offset="1" stop-color="#0B1D34"/>
  </linearGradient>
  <linearGradient id="gGold" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#8A6522"/><stop offset="0.5" stop-color="#D4AF37"/><stop offset="1" stop-color="#E8DCC0"/>
  </linearGradient>
  <linearGradient id="gSky" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#0B1D34"/><stop offset="0.5" stop-color="#20344D"/><stop offset="1" stop-color="#DADDE3"/>
  </linearGradient>
  <linearGradient id="gScrim" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0B1D34" stop-opacity="0.86"/><stop offset="0.5" stop-color="#0B1D34" stop-opacity="0.46"/><stop offset="1" stop-color="#0B1D34" stop-opacity="0.92"/>
  </linearGradient>
  <linearGradient id="gFadeL" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#F4F0EE" stop-opacity="1"/><stop offset="1" stop-color="#F4F0EE" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="gStrip" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#F4F0EE"/><stop offset="0.35" stop-color="#D4AF37"/><stop offset="1" stop-color="#0B1D34"/>
  </linearGradient>
</defs>
"""

def chrome(sec, num, total=16, fill=TXT, sub="MANUAL DE MARCA"):
    o = []
    o.append(line(M, 78, W - M, 78, stroke=fill, sw=0.8, op=0.28))
    o.append(label(M, 68, sec, fill=(AMBER if fill == TXT else fill), size=11))
    o.append(label(W - M, 68, sub, fill=fill, size=11, anchor="end", w=500))
    o.append(line(M, H - 74, W - M, H - 74, stroke=fill, sw=0.8, op=0.18))
    o.append(label(M, H - 48, "VELUM ENTERPRISE", fill=fill, size=10, w=500))
    o.append(t(W - M, H - 46, "%02d" % num, size=15, w=600, fill=fill, ls=1, anchor="end"))
    o.append(t(W - M - 36, H - 46, "/ %02d" % total, size=15, w=400, fill=fill, ls=1, anchor="end", op=0.4))
    return "".join(o)

def page(body, bg="url(#gGround)"):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
            '%s<rect width="%d" height="%d" fill="%s"/>%s</svg>') % (W, H, W, H, DEFS, W, H, bg, body)

def write(n, name, svg):
    p = os.path.dirname(B) + "/SVG_ES/velum-%02d-%s.svg" % (n, name)
    open(p, "w", encoding="utf-8").write(svg)
    return p
