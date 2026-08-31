# -*- coding: utf-8 -*-
"""VELUM — single-page brand board, built from the kit's own vectors and gradients."""
import os, re, io, math, base64
from PIL import Image

B = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(B + "/../..")
SRC = os.path.abspath(KIT + "/..")
OUT = os.path.abspath(B + "/..")

W, H = 2000, 2700
M = 70

GROUND, INK, NAVY, GOLD, CREAM, PEARL, IVORY, BLACK, GREY, AMBER = (
    "#F4F0EE", "#0B1D34", "#20344D", "#D4AF37", "#E8DCC0", "#DADDE3", "#F7F7F7",
    "#1A1A1A", "#55585F", "#B8912B")

DIS = "Cinzel, Cormorant Garamond, Georgia, serif"
SER = "Cormorant Garamond, Georgia, serif"
SAN = "Montserrat, Poppins, Arial, sans-serif"

# ---------------------------------------------------------------- assets
def _art(path):
    s = open(path, encoding="utf-8").read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1).split()
    inner = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1).strip()
    return float(vb[2]), float(vb[3]), inner

def place(path, x, y, w):
    aw, ah, inner = _art(path)
    return ('<g transform="translate(%.1f %.1f) scale(%.5f)">%s</g>' % (x, y, w / aw, inner),
            w * ah / aw)

def logo(name, x, y, w):
    return place(KIT + "/01_Logo/SVG/velum-%s.svg" % name, x, y, w)

def elem(name, x, y, w):
    return place(KIT + "/06_Elements/SVG/velum-%s.svg" % name, x, y, w)

_cache = {}
def photo(path, x, y, w, h, px=1000, op=1.0, q=80, crop=None):
    key = (path, px, crop)
    if key not in _cache:
        im = Image.open(path).convert("RGB")
        if crop:
            im = im.crop(crop)
        sc = px / max(im.size)
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, "JPEG", quality=q)
        _cache[key] = base64.b64encode(b.getvalue()).decode()
    a = 'x="%.1f" y="%.1f" width="%.1f" height="%.1f" preserveAspectRatio="xMidYMid slice"' % (x, y, w, h)
    if op != 1.0:
        a += ' opacity="%.2f"' % op
    return '<image %s href="data:image/jpeg;base64,%s"/>' % (a, _cache[key])

# ---------------------------------------------------------------- primitives
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def t(x, y, s, size=16, f=SAN, w=400, fill=INK, ls=0, anchor="start", op=1.0, italic=False):
    a = ['x="%.1f"' % x, 'y="%.1f"' % y, 'font-family="%s"' % f, 'font-size="%.1f"' % size,
         'font-weight="%s"' % w, 'fill="%s"' % fill]
    if ls: a.append('letter-spacing="%.2f"' % ls)
    if anchor != "start": a.append('text-anchor="%s"' % anchor)
    if op != 1.0: a.append('opacity="%.2f"' % op)
    if italic: a.append('font-style="italic"')
    return "<text %s>%s</text>" % (" ".join(a), esc(s))

def label(x, y, s, fill=AMBER, size=12, anchor="start"):
    return t(x, y, s.upper(), size=size, w=600, fill=fill, ls=4.0, anchor=anchor)

def para(x, y, lines, size=17, lh=30, fill=GREY, op=1.0, f=SAN, w=400, anchor="start", italic=False):
    return "".join(t(x, y + i * lh, l, size=size, fill=fill, op=op, f=f, w=w, anchor=anchor, italic=italic)
                   for i, l in enumerate(lines))

def rect(x, y, w, h, fill, op=1.0, rx=0, stroke=None, sw=1):
    a = 'x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"' % (x, y, w, h, fill)
    if rx: a += ' rx="%.1f"' % rx
    if op != 1.0: a += ' opacity="%.2f"' % op
    if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
    return "<rect %s/>" % a

def line(x1, y1, x2, y2, stroke=GOLD, sw=1, op=1.0):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.2f" opacity="%.2f"/>'
            % (x1, y1, x2, y2, stroke, sw, op))

def circ(cx, cy, r, fill="none", stroke=None, sw=1):
    a = 'cx="%.1f" cy="%.1f" r="%.1f" fill="%s"' % (cx, cy, r, fill)
    if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
    return "<circle %s/>" % a

def veil(x, y, w, h, n=9, stroke=GOLD, sw=1.4, op=0.5, spread=1.0):
    o = ['<g fill="none" opacity="%.2f" stroke="%s" stroke-width="%.2f" stroke-linecap="round">' % (op, stroke, sw)]
    for i in range(n):
        f = i / float(max(1, n - 1))
        yy = y + h * f
        amp = h * 0.40 * spread * (0.45 + 0.55 * math.sin(f * math.pi))
        o.append('<path d="M %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f S %.1f %.1f %.1f %.1f"/>' % (
            x, yy, x + w * 0.22, yy - amp, x + w * 0.42, yy + amp * 0.55, x + w * 0.60, yy - amp * 0.12,
            x + w * 0.86, yy - amp * 0.95, x + w, yy - amp * 0.62))
    o.append("</g>")
    return "".join(o)

# ---------------------------------------------------------------- board
def build():
    o = [rect(0, 0, W, H, GROUND)]

    # ---------- header
    hx, hy, hw, hh = M, M, W - 2 * M, 760
    o.append(photo(KIT + "/05_Textures/velum-yeso-hueso.jpg", hx, hy, hw, hh, px=1300))
    o.append(veil(hx, hy + 190, hw, 400, n=16, stroke=INK, sw=1.1, op=0.10, spread=1.2))
    g, gh = logo("primary-light-bg", hx + 90, hy + 210, 720)
    o.append(g)
    o.append(line(hx + 90, hy + 622, hx + 320, hy + 622, stroke=GOLD, sw=1.2))
    o.append(label(hx + 90, hy + 678, "Grupo empresarial  ·  La Habana, Cuba", fill=GREY, size=12))

    o.append(line(hx + 960, hy + 90, hx + 960, hy + hh - 90, stroke=INK, sw=0.8, op=0.25))
    rx = hx + 1030
    o.append(label(rx, hy + 130, "Significado de la marca", fill=GOLD))
    o.append(t(rx, hy + 244, "MÁS ALLÁ", size=46, f=DIS, fill=INK, ls=3))
    o.append(t(rx, hy + 302, "DE LO VISIBLE", size=46, f=DIS, fill=INK, ls=3))
    o.append(para(rx, hy + 368, [
        "Velum significa velo, en latín: lo que separa lo que vemos",
        "de lo que hay detrás. También la vela que atrapa el viento.",
        "Curiosidad y dirección en una sola palabra.",
    ], size=17, lh=31, fill=GREY))
    for i, (k, v) in enumerate([("Descubrir", "Mirar más allá"), ("Conectar", "Unir mundos"),
                                ("Transformar", "Hacerlo tangible")]):
        cx = rx + i * 250
        o.append(line(cx, hy + 566, cx + 210, hy + 566, stroke=GOLD, sw=1))
        o.append(t(cx, hy + 616, k.upper(), size=24, f=DIS, fill=INK, ls=2))
        o.append(t(cx, hy + 646, v, size=12.5, f=SAN, fill=GREY))

    # ---------- row 2 : variaciones | paleta | tipografías
    y2 = 890
    o.append(label(M, y2, "Variaciones del logo", fill=AMBER))
    tiles = [("Fondo hueso", GROUND, "primary-light-bg"), ("Fondo oscuro", INK, "primary-dark-bg"),
             ("Una tinta · oro", INK, "primary-oro"), ("Sello", NAVY, "seal")]
    tw, tg = 232, 22
    for i, (cap, bg, kind) in enumerate(tiles):
        x = M + i * (tw + tg)
        o.append(rect(x, y2 + 34, tw, 232, bg))
        o.append(rect(x, y2 + 34, tw, 232, "none", stroke=INK, sw=0.8, op=0.25))
        if kind == "seal":
            o.append(circ(x + tw / 2, y2 + 150, 84, fill=INK, stroke=GOLD, sw=1))
            g, gh = logo("monogram-dark-bg", x + tw / 2 - 52, y2 + 118, 104)
            o.append(g)
            o.append(t(x + tw / 2, y2 + 104, "VELUM", size=10, f=SAN, fill=GOLD, ls=4, anchor="middle"))
        else:
            g, gh = logo(kind, x + 26, y2 + 122, tw - 52)
            o.append(g)
        o.append(label(x, y2 + 302, cap, fill=GREY, size=9.5))

    px_ = M + 4 * (tw + tg) + 40
    o.append(label(px_, y2, "Paleta", fill=AMBER))
    PAL = [("Blanco Hueso", GROUND), ("Azul Velum", INK), ("Oro Velum", GOLD), ("Crema", CREAM),
           ("Azul Medio", NAVY), ("Gris Perla", PEARL), ("Gris", GREY), ("Negro", BLACK)]
    sw_, sg = 108, 14
    for i, (n, hx_) in enumerate(PAL):
        x = px_ + (i % 4) * (sw_ + sg)
        y = y2 + 34 + (i // 4) * 152
        o.append(rect(x, y, sw_, 98, hx_))
        o.append(rect(x, y, sw_, 98, "none", stroke=INK, sw=0.7, op=0.3))
        o.append(t(x, y + 122, n, size=11.5, fill=INK, op=0.9))
        o.append(t(x, y + 140, hx_.upper(), size=10.5, fill=GREY))

    tx = px_ + 4 * (sw_ + sg) + 40
    o.append(label(tx, y2, "Tipografías", fill=AMBER))
    fams = [("Aa", DIS, "Cinzel Display", "Marca y titulares"),
            ("Aa", SAN, "Montserrat", "Texto y sistema")]
    for i, (aa, f, name, role) in enumerate(fams):
        y = y2 + 120 + i * 150
        o.append(t(tx, y, aa, size=58, f=f, fill=INK))
        o.append(t(tx + 120, y - 20, name, size=18, f=DIS, fill=INK, ls=1.5))
        o.append(t(tx + 120, y + 6, role, size=11.5, fill=AMBER))
        if i < 1:
            o.append(line(tx, y + 52, tx + 300, y + 52, stroke=INK, sw=0.8, op=0.2))

    # ---------- row 3 : divisiones | elementos
    y3 = 1340
    o.append(line(M, y3 - 44, W - M, y3 - 44, stroke=INK, sw=0.8, op=0.2))
    o.append(label(M, y3, "Las seis casas", fill=AMBER))
    DIV = [("viajes", "Velum Travel"), ("perfumeria", "AL — Ana López"), ("alimentos", "Velum Foods"),
           ("importacion-exportacion", "Velum Trade"), ("inmuebles", "Velum Properties"),
           ("vehiculos-electricos", "Velum Mobility")]
    dw = 196
    for i, (k, cap) in enumerate(DIV):
        x = M + i * (dw + 14)
        o.append(rect(x, y3 + 34, dw, 190, CREAM, op=0.45))
        g, gh = elem("icono-" + k, x + dw / 2 - 40, y3 + 78, 80)
        o.append(g)
        o.append(t(x + dw / 2, y3 + 258, cap.upper(), size=13, f=DIS, fill=INK, ls=1.2, anchor="middle"))

    ex = M + 6 * (dw + 14) + 30
    o.append(label(ex, y3, "El velo", fill=AMBER))
    o.append(rect(ex, y3 + 34, W - M - ex, 190, CREAM, op=0.45))
    o.append(veil(ex + 24, y3 + 78, 240, 104, n=9, stroke=INK, sw=1.3, op=0.5))
    g, gh = elem("estrella-oro", ex + 278, y3 + 88, 38)
    o.append(g)
    for i, kind in enumerate(["diag", "grid"]):
        cx, cy, cs = ex + 336 + i * 86, y3 + 106, 74
        o.append(rect(cx, cy, cs, cs, GROUND))
        o.append('<clipPath id="chip%d"><rect x="%.1f" y="%.1f" width="%d" height="%d"/></clipPath>'
                 % (i, cx, cy, cs, cs))
        o.append('<g clip-path="url(#chip%d)" opacity="0.55">' % i)
        if kind == "diag":
            for k in range(-8, 14):
                o.append(line(cx + k * 9, cy - 10, cx + k * 9 + 90, cy + cs + 10, stroke=INK, sw=1.2))
        else:
            for k in range(0, cs + 1, 12):
                o.append(line(cx + k, cy, cx + k, cy + cs, stroke=INK, sw=0.8))
                o.append(line(cx, cy + k, cx + cs, cy + k, stroke=INK, sw=0.8))
        o.append("</g>")
        o.append(rect(cx, cy, cs, cs, "none", stroke=INK, sw=0.7, op=0.35))
    o.append(t(ex + 40, y3 + 258, "Un gesto, seis lecturas", size=15, fill=INK, op=0.9))

    # ---------- row 4 : aplicaciones
    y4 = 1700
    o.append(line(M, y4 - 44, W - M, y4 - 44, stroke=INK, sw=0.8, op=0.2))
    o.append(label(M, y4, "Aplicaciones", fill=AMBER))
    aw = (W - 2 * M - 3 * 20) / 4.0
    o.append(photo(SRC + "/Business_Card_Mockup_3.png", M, y4 + 34, aw, 380, px=1100))
    bx, by, bw, bh = M + (aw + 20), y4 + 34, aw, 380
    o.append(rect(bx, by, bw, bh, GROUND, stroke=INK, sw=0.7))
    o.append(rect(bx, by, bw, 26, CREAM))
    for i, c in enumerate([GOLD, PEARL, GREY]):
        o.append(circ(bx + 16 + i * 14, by + 13, 3.6, fill=c))
    o.append(rect(bx + 62, by + 6, 130, 14, GROUND, rx=7, stroke=INK, sw=0.5))
    o.append(veil(bx, by + 110, bw, 210, n=10, stroke=INK, sw=1, op=0.12))
    g, gh = logo("primary-light-bg", bx + 22, by + 46, 96)
    o.append(g)
    for i, n in enumerate(["Estudio", "Trabajo", "Contacto"]):
        o.append(label(bx + 170 + i * 88, by + 66, n, fill=GREY, size=7))
    o.append(t(bx + 22, by + 242, "MÁS ALLÁ", size=30, f=DIS, fill=INK, ls=2))
    o.append(t(bx + 22, by + 282, "DE LO VISIBLE", size=30, f=DIS, fill=INK, ls=2))
    o.append(rect(bx + 22, by + 308, 120, 30, INK))
    o.append(label(bx + 37, by + 328, "Ver más", fill=GROUND, size=7.5))
    # poster tile
    x3 = M + 2 * (aw + 20)
    o.append(photo(KIT + "/05_Textures/velum-cielo-nocturno.jpg", x3, y4 + 34, aw, 380, px=900))
    g, gh = logo("primary-dark-bg", x3 + aw / 2 - 130, y4 + 160, 260)
    o.append(g)
    # profile tile
    x4 = M + 3 * (aw + 20)
    o.append(rect(x4, y4 + 34, aw, 380, CREAM, op=0.5))
    o.append(circ(x4 + aw / 2, y4 + 190, 96, fill=INK, stroke=GOLD, sw=1))
    g, gh = logo("monogram-dark-bg", x4 + aw / 2 - 60, y4 + 152, 120)
    o.append(g)
    o.append(t(x4 + aw / 2, y4 + 340, "@VELUM", size=22, f=DIS, fill=INK, ls=3, anchor="middle"))
    for i, cap in enumerate(["Tarjeta corporativa", "Sitio web", "Cartel y campaña", "Perfil social"]):
        o.append(label(M + i * (aw + 20), y4 + 448, cap, fill=GREY, size=9.5))

    # ---------- footer
    fy = 2230
    o.append(rect(M, fy, W - 2 * M, 400, INK))
    o.append(veil(M, fy + 70, W - 2 * M, 260, n=14, stroke=GOLD, sw=1.1, op=0.16, spread=1.1))
    o.append(label(M + 70, fy + 100, "El relato", fill=GOLD, size=11))
    o.append(para(M + 70, fy + 160, ["Un viaje puede convertirse en experiencia.",
                                     "Un aroma, en un recuerdo.",
                                     "Un espacio, en un destino.",
                                     "Una idea, en un negocio."],
                  size=19, lh=34, fill=IVORY, f=SER, italic=True))
    g, gh = logo("monogram-dark-bg", M + 900, fy + 150, 150)
    o.append(g)
    o.append(t(W - M - 70, fy + 180, "EL CIELO ES", size=36, f=DIS, fill=IVORY, anchor="end", ls=3))
    o.append(t(W - M - 70, fy + 232, "EL LÍMITE.", size=36, f=DIS, fill=IVORY, anchor="end", ls=3))
    o.append(line(W - M - 190, fy + 266, W - M - 70, fy + 266, stroke=GOLD, sw=1))
    o.append(label(W - M - 70, fy + 316, "Descubrir · Conectar · Transformar", fill=PEARL, size=10, anchor="end"))
    o.append(label(M, H - 26, "VELUM  ·  Brand board  ·  v2.0  ·  2026", fill=GREY, size=9.5))
    o.append(label(W - M, H - 26, "Manual completo en 04_Guidelines", fill=GREY, size=9.5, anchor="end"))

    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>'
            % (W, H, W, H, "".join(o)))

if __name__ == "__main__":
    p = OUT + "/velum-brand-board.svg"
    open(p, "w", encoding="utf-8").write(build())
    print(p, os.path.getsize(p) // 1024, "KB")
