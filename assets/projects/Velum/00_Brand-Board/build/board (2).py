# -*- coding: utf-8 -*-
"""AnaLopez - single-page brand board, built from the kit's own vectors and photography."""
import os, re, io, base64
from PIL import Image

B = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(B + "/../..")
AL = os.path.abspath(KIT + "/..")
OUT = os.path.abspath(B + "/..")

W, H = 2000, 2700
M = 70

NEGRO  = "#0D0D0C"
VERDE  = "#1C2417"
OLIVA  = "#585C41"
CACAO  = "#492B17"
AMBAR  = "#B8762A"
ARENA  = "#D6BD9A"
JAZMIN = "#EDE5DA"
CAL    = "#F5F0EA"

DIS = "Bodoni Moda, Didot, Georgia, serif"
SAN = "Poppins, Montserrat, Arial, sans-serif"
ITA = "Italiana, Cormorant Garamond, Georgia, serif"

# ---------------------------------------------------------------- asset loading
def _inner(path):
    s = open(path, encoding="utf-8").read()
    m = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1).split()
    return float(vb[2]), float(vb[3]), m.group(1).strip()

def art(path, x, y, w, fill=None):
    aw, ah, frag = _inner(path)
    if fill:
        frag = frag.replace('fill="#0D0D0C"', 'fill="%s"' % fill)
    return '<g transform="translate(%.1f %.1f) scale(%.5f)">%s</g>' % (x, y, w / aw, frag), w * ah / aw

def logo(kind, color, x, y, w):
    return art(KIT + "/01_Logo/SVG/analopez-%s-negro.svg" % kind, x, y, w, color)

def jasmine(kind, color, x, y, w):
    return art(KIT + "/06_Illustrations/SVG/analopez-jasmine-%s-negro.svg" % kind, x, y, w, color)

_imgcache = {}
def photo(path, x, y, w, h, px=900, op=1.0, quality=80):
    key = (path, px)
    if key not in _imgcache:
        im = Image.open(path).convert("RGB")
        sc = px / max(im.size)
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, "JPEG", quality=quality)
        _imgcache[key] = base64.b64encode(b.getvalue()).decode()
    a = 'x="%.1f" y="%.1f" width="%.1f" height="%.1f" preserveAspectRatio="xMidYMid slice"' % (x, y, w, h)
    if op != 1.0:
        a += ' opacity="%.2f"' % op
    return '<image %s href="data:image/jpeg;base64,%s"/>' % (a, _imgcache[key])

# ---------------------------------------------------------------- primitives
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def t(x, y, s, size=16, f=SAN, w=400, fill=NEGRO, ls=0, anchor="start", op=1.0, italic=False):
    a = ['x="%.1f"' % x, 'y="%.1f"' % y, 'font-family="%s"' % f, 'font-size="%.1f"' % size,
         'font-weight="%s"' % w, 'fill="%s"' % fill]
    if ls: a.append('letter-spacing="%.2f"' % ls)
    if anchor != "start": a.append('text-anchor="%s"' % anchor)
    if op != 1.0: a.append('opacity="%.2f"' % op)
    if italic: a.append('font-style="italic"')
    return "<text %s>%s</text>" % (" ".join(a), esc(s))

def label(x, y, s, fill=OLIVA, size=13, anchor="start"):
    return t(x, y, s.upper(), size=size, w=400, fill=fill, ls=4.2, anchor=anchor, f=SAN)

def para(x, y, lines, size=17, lh=30, fill=NEGRO, op=0.8, f=SAN, w=400, anchor="start", italic=False):
    return "".join(t(x, y + i * lh, l, size=size, fill=fill, op=op, f=f, w=w, anchor=anchor, italic=italic)
                   for i, l in enumerate(lines))

def rect(x, y, w, h, fill, op=1.0, rx=0, stroke=None, sw=1):
    a = 'x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"' % (x, y, w, h, fill)
    if rx: a += ' rx="%.1f"' % rx
    if op != 1.0: a += ' opacity="%.2f"' % op
    if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
    return "<rect %s/>" % a

def line(x1, y1, x2, y2, stroke=OLIVA, sw=1, op=1.0):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.2f" opacity="%.2f"/>' % (
        x1, y1, x2, y2, stroke, sw, op)

def circ(cx, cy, r, fill="none", stroke=None, sw=1):
    a = 'cx="%.1f" cy="%.1f" r="%.1f" fill="%s"' % (cx, cy, r, fill)
    if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
    return "<circle %s/>" % a

# ---------------------------------------------------------------- board
def build():
    o = [rect(0, 0, W, H, CAL)]

    # ---------- header
    hx, hy, hw, hh = M, M, W - 2 * M, 750
    o.append(rect(hx, hy, hw, hh, JAZMIN))
    o.append(photo(KIT + "/05_Textures/texture-limewash-cal.jpg", hx, hy, hw, hh, px=1100, op=0.55))
    o.append(rect(hx, hy, hw, hh, JAZMIN, op=0.42))
    g, gh = logo("primary", NEGRO, hx + 90, hy + 250, 780)
    o.append(g)
    o.append(line(hx + 90, hy + 520, hx + 330, hy + 520, stroke=AMBAR, sw=1.2, op=0.9))
    o.append(label(hx + 90, hy + 578, "Casa de perfumería y belleza  ·  La Habana, Cuba", fill=OLIVA, size=13))
    o.append(t(hx + 90, hy + 646, "Memoria, cultura y ciencia. Nacida en Cuba.", size=27, f=DIS, fill=NEGRO, op=0.7, italic=True))

    o.append(line(hx + 980, hy + 90, hx + 980, hy + hh - 90, stroke=OLIVA, sw=0.8, op=0.35))
    rx = hx + 1050
    o.append(label(rx, hy + 130, "Significado de la marca", fill=AMBAR))
    o.append(t(rx, hy + 232, "«Cada mañana", size=46, f=DIS, fill=NEGRO, italic=True))
    o.append(t(rx, hy + 288, "olía a jazmín.»", size=46, f=DIS, fill=NEGRO, italic=True))
    o.append(para(rx, hy + 366, [
        "En La Habana, junto al cuarto donde dormía su fundador",
        "de niño, crecía una planta de jazmín. Había pertenecido a",
        "su abuela, Ana. La planta desapareció; el aroma quedó en",
        "la memoria. Esa memoria es el origen de la casa.",
    ], size=17, lh=31, fill=NEGRO, op=0.78))
    for i, (k, v) in enumerate([("Memoria", "Materia prima"), ("Herencia", "Lo que se transmite"),
                                ("Cuba", "Origen, no decoración"), ("Ciencia", "Base real")]):
        cx = rx + i * 185
        o.append(line(cx, hy + 560, cx + 150, hy + 560, stroke=OLIVA, sw=0.8, op=0.4))
        o.append(t(cx, hy + 604, k, size=22, f=DIS, fill=NEGRO))
        o.append(t(cx, hy + 632, v, size=12, f=SAN, fill=OLIVA, op=0.9))

    # ---------- row 2 : variaciones | paleta | tipografías
    y2 = 880
    o.append(label(M, y2, "Variaciones del logo", fill=OLIVA))
    tiles = [("Principal", CAL, "primary", NEGRO),
             ("Reverso", VERDE, "primary", JAZMIN),
             ("Apilado", ARENA, "stacked", NEGRO),
             ("Sello", VERDE, "seal", JAZMIN)]
    tw, tg = 232, 22
    for i, (cap, bg, kind, ink) in enumerate(tiles):
        x = M + i * (tw + tg)
        o.append(rect(x, y2 + 34, tw, 232, bg))
        if bg == CAL:
            o.append(rect(x, y2 + 34, tw, 232, "none", stroke=OLIVA, sw=0.8))
        if kind == "seal":
            o.append(circ(x + tw / 2, y2 + 150, 86, stroke=JAZMIN, sw=1))
            g, gh = logo("monogram", ink, x + tw / 2 - 34, y2 + 108, 68)
            o.append(g)
            o.append(t(x + tw / 2, y2 + 92, "ANALOPEZ", size=9, f=SAN, fill=JAZMIN, ls=3, anchor="middle"))
            o.append(t(x + tw / 2, y2 + 222, "CASA DE ESENCIAS", size=8, f=SAN, fill=JAZMIN, ls=2.4, anchor="middle"))
        elif kind == "stacked":
            g, gh = logo("stacked", ink, x + tw / 2 - 62, y2 + 96, 124)
            o.append(g)
        else:
            g, gh = logo("primary", ink, x + 26, y2 + 128, tw - 52)
            o.append(g)
        o.append(label(x, y2 + 300, cap, fill=OLIVA, size=10))

    px_ = M + 4 * (tw + tg) + 40
    o.append(label(px_, y2, "Paleta", fill=OLIVA))
    PAL = [("Negro", NEGRO), ("Verde Profundo", VERDE), ("Oliva", OLIVA), ("Cacao", CACAO),
           ("Ámbar", AMBAR), ("Arena", ARENA), ("Jazmín", JAZMIN), ("Blanco Cal", CAL)]
    sw_, sg = 108, 14
    for i, (n, hx_) in enumerate(PAL):
        x = px_ + (i % 4) * (sw_ + sg)
        y = y2 + 34 + (i // 4) * 152
        o.append(rect(x, y, sw_, 98, hx_))
        if hx_ in (JAZMIN, CAL):
            o.append(rect(x, y, sw_, 98, "none", stroke=OLIVA, sw=0.8))
        o.append(t(x, y + 122, n, size=11.5, f=SAN, fill=NEGRO, op=0.85))
        o.append(t(x, y + 140, hx_.upper(), size=10.5, f=SAN, fill=OLIVA))

    tx = px_ + 4 * (sw_ + sg) + 40
    o.append(label(tx, y2, "Tipografías", fill=OLIVA))
    fams = [("Aa", ITA, "Italiana", "Reservada · logotipo"),
            ("Aa", DIS, "Bodoni Moda", "Display y editorial"),
            ("Aa", SAN, "Poppins", "Texto y etiquetas")]
    for i, (aa, f, name, role) in enumerate(fams):
        y = y2 + 96 + i * 108
        o.append(t(tx, y, aa, size=54, f=f, fill=NEGRO))
        o.append(t(tx + 96, y - 18, name, size=19, f=DIS, fill=NEGRO))
        o.append(t(tx + 96, y + 4, role, size=12, f=SAN, fill=OLIVA))
        if i < 2:
            o.append(line(tx, y + 42, tx + 300, y + 42, stroke=OLIVA, sw=0.8, op=0.3))

    # ---------- row 3 : ilustraciones | texturas
    y3 = 1330
    o.append(line(M, y3 - 44, W - M, y3 - 44, stroke=OLIVA, sw=0.8, op=0.3))
    o.append(label(M, y3, "El jazmín · símbolo secundario", fill=OLIVA))
    kinds = [("bloom", "Flor"), ("branch-wide", "Rama ancha"), ("branch-diagonal", "Rama diagonal"),
             ("single", "Flor sola"), ("spray", "Ramillete"), ("stem", "Tallo")]
    iw = 178
    for i, (k, cap) in enumerate(kinds):
        x = M + i * (iw + 16)
        o.append(rect(x, y3 + 34, iw, 200, JAZMIN))
        g, gh = jasmine(k, CACAO, x + 22, y3 + 60, iw - 44)
        o.append(g)
        o.append(label(x, y3 + 268, cap, fill=OLIVA, size=9.5))

    txx = M + 6 * (iw + 16) + 30
    o.append(label(txx, y3, "Texturas", fill=OLIVA))
    texs = [("texture-limewash-cal.jpg", "Cal"), ("texture-plaster-arena.jpg", "Yeso Arena"),
            ("texture-matte-board-verde.jpg", "Cartulina Verde"), ("texture-kraft.jpg", "Kraft")]
    cw2 = (W - M - txx - 3 * 14) / 4.0
    for i, (fn, cap) in enumerate(texs):
        x = txx + i * (cw2 + 14)
        o.append(photo(KIT + "/05_Textures/" + fn, x, y3 + 34, cw2, 200, px=500))
        o.append(label(x, y3 + 268, cap, fill=OLIVA, size=9.5))

    # ---------- row 4 : aplicaciones
    y4 = 1700
    o.append(line(M, y4 - 44, W - M, y4 - 44, stroke=OLIVA, sw=0.8, op=0.3))
    o.append(label(M, y4, "Aplicaciones", fill=OLIVA))
    apps = [(AL + "/Free Perfume Bottle with Box Mockup.png", "Eau de Parfum"),
            (AL + "/Paper Shopping Bags Mockup.png", "Bolsas"),
            (AL + "/Soap_Bar_v01.png", "Jabón"),
            (AL + "/Gemini_Generated_Image_7gv6cr7gv6cr7gv6.jpg", "Dirección de imagen")]
    aw = (W - 2 * M - 3 * 20) / 4.0
    for i, (fn, cap) in enumerate(apps):
        x = M + i * (aw + 20)
        o.append(photo(fn, x, y4 + 34, aw, 380, px=1000))
        o.append(label(x, y4 + 448, cap, fill=OLIVA, size=9.5))

    # ---------- footer
    fy = 2230
    o.append(rect(M, fy, W - 2 * M, 400, VERDE))
    o.append(photo(KIT + "/05_Textures/texture-matte-board-verde.jpg", M, fy, W - 2 * M, 400, px=900, op=0.5))
    o.append(rect(M, fy, W - 2 * M, 400, VERDE, op=0.55))
    o.append(label(M + 70, fy + 90, "Manifiesto", fill=ARENA, size=11))
    o.append(para(M + 70, fy + 148, ["Las cosas cambian. Las casas cambian.",
                                     "Los jardines desaparecen.",
                                     "Pero algunos recuerdos permanecen.",
                                     "Y nosotros decidimos convertirlo en perfume."],
                  size=18, lh=32, fill=JAZMIN, op=0.85, f=DIS))
    g, gh = logo("stacked", JAZMIN, M + 830, fy + 130, 200)
    o.append(g)
    o.append(t(W - M - 70, fy + 160, "The scent of", size=40, f=DIS, fill=JAZMIN, anchor="end", italic=True))
    o.append(t(W - M - 70, fy + 212, "what remains.", size=40, f=DIS, fill=JAZMIN, anchor="end", italic=True))
    o.append(line(W - M - 190, fy + 256, W - M - 70, fy + 256, stroke=AMBAR, sw=1))
    o.append(label(W - M - 70, fy + 306, "Una casa Velum", fill=ARENA, size=10, anchor="end"))
    o.append(label(M, H - 26, "AnaLopez  ·  Brand board  ·  v1.0  ·  2026", fill=OLIVA, size=9.5))
    o.append(label(W - M, H - 26, "Casa de esencias nacida en Cuba", fill=OLIVA, size=9.5, anchor="end"))

    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>'
            % (W, H, W, H, "".join(o)))

if __name__ == "__main__":
    svg = build()
    p = OUT + "/analopez-brand-board.svg"
    open(p, "w", encoding="utf-8").write(svg)
    print(p, os.path.getsize(p) // 1024, "KB")
