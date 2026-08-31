# -*- coding: utf-8 -*-
"""VELUM — photography direction board (2000 x 2700)."""
import os, io, re, math, base64, sys
from PIL import Image

B = os.path.dirname(os.path.abspath(__file__))
SEC = os.path.dirname(B)               # 07_Photography
KIT = os.path.dirname(SEC)
OUT = SEC

W, H = 2000, 2700
M = 70

GROUND, INK, NAVY, GOLD, CREAM, AMBER, PEARL, GREY, BLACK, CLAY = (
    "#F4F0EE", "#0B1D34", "#20344D", "#D4AF37", "#E8DCC0", "#B8912B",
    "#DADDE3", "#55585F", "#1A1A1A", "#8C5A3C")

DIS = "Cinzel, Cormorant Garamond, Georgia, serif"
SAN = "Montserrat, Poppins, Arial, sans-serif"

LANG = sys.argv[1] if len(sys.argv) > 1 else "ES"
ES = LANG == "ES"

def tr(es, en):
    return es if ES else en

# ---------------------------------------------------------------- helpers
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def t(x, y, s, size=16, f=SAN, w=400, fill=INK, ls=0, anchor="start", op=1.0, italic=False):
    a = ['x="%.1f"' % x, 'y="%.1f"' % y, 'font-family="%s"' % f, 'font-size="%.1f"' % size,
         'font-weight="%s"' % w, 'fill="%s"' % fill]
    if ls: a.append('letter-spacing="%.2f"' % ls)
    if anchor != "start": a.append('text-anchor="%s"' % anchor)
    if op != 1.0: a.append('opacity="%.2f"' % op)
    if italic: a.append('font-style="italic"')
    return "<text %s>%s</text>" % (" ".join(a), esc(s))

def label(x, y, s, fill=AMBER, size=11, anchor="start"):
    return t(x, y, s.upper(), size=size, w=600, fill=fill, ls=3.6, anchor=anchor)

def para(x, y, lines, size=15, lh=25, fill=GREY, anchor="start", f=SAN, italic=False):
    return "".join(t(x, y + i * lh, l, size=size, fill=fill, anchor=anchor, f=f, italic=italic)
                   for i, l in enumerate(lines))

def rect(x, y, w, h, fill, op=1.0, rx=0, stroke=None, sw=1):
    a = 'x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"' % (x, y, w, h, fill)
    if rx: a += ' rx="%.1f"' % rx
    if op != 1.0: a += ' opacity="%.2f"' % op
    if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
    return "<rect %s/>" % a

def line(x1, y1, x2, y2, stroke=INK, sw=1, op=1.0, dash=None):
    a = 'x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.2f" opacity="%.2f"' % (
        x1, y1, x2, y2, stroke, sw, op)
    if dash: a += ' stroke-dasharray="%s"' % dash
    return "<line %s/>" % a

def circ(cx, cy, r, fill="none", stroke=None, sw=1, op=1.0, dash=None):
    a = 'cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f"' % (cx, cy, r, fill, op)
    if stroke: a += ' stroke="%s" stroke-width="%.2f"' % (stroke, sw)
    if dash: a += ' stroke-dasharray="%s"' % dash
    return "<circle %s/>" % a

def path(d, fill="none", stroke=None, sw=1.4, op=1.0, dash=None):
    a = 'd="%s" fill="%s" opacity="%.2f"' % (d, fill, op)
    if stroke: a += ' stroke="%s" stroke-width="%.2f" stroke-linecap="round" stroke-linejoin="round"' % (stroke, sw)
    if dash: a += ' stroke-dasharray="%s"' % dash
    return "<path %s/>" % a

_cache = {}
def photo(p, x, y, w, h, px=1100, op=1.0, q=80):
    key = (p, px)
    if key not in _cache:
        im = Image.open(p).convert("RGB")
        sc = px / max(im.size)
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, "JPEG", quality=q)
        _cache[key] = base64.b64encode(b.getvalue()).decode()
    a = 'x="%.1f" y="%.1f" width="%.1f" height="%.1f" preserveAspectRatio="xMidYMid slice"' % (x, y, w, h)
    if op != 1.0:
        a += ' opacity="%.2f"' % op
    return '<image %s href="data:image/jpeg;base64,%s"/>' % (a, _cache[key])

def logo(name, x, y, w):
    s = open(KIT + "/01_Logo/SVG/velum-%s.svg" % name, encoding="utf-8").read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1).split()
    inner = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1).strip()
    sc = w / float(vb[2])
    return '<g transform="translate(%.1f %.1f) scale(%.5f)">%s</g>' % (x, y, sc, inner)

def icon(kind, x, y, s=1.0, stroke=AMBER, sw=1.6):
    P = {"plane": "M6 27 L42 17 M6 27 L18 31 L14 41 L20 33 L34 37 M42 17 L34 37",
         "bottle": "M19 6 h10 v7 h-10 z M17 13 h14 c3 6 4 9 4 14 v13 a4 4 0 0 1 -4 4 h-14 a4 4 0 0 1 -4 -4 "
                   "v-13 c0 -5 1 -8 4 -14 z M19 26 h10",
         "cloche": "M6 39 h36 M10 39 a14 15 0 0 1 28 0 M24 10 v-5 M20.5 5 h7",
         "globe": "M24 6 a18 18 0 1 0 0 36 a18 18 0 1 0 0 -36 M6 24 h36 M24 6 c-8 8 -8 28 0 36 M24 6 c8 8 8 28 0 36",
         "building": "M10 42 v-30 h14 v30 M24 42 v-20 h14 v20 M14 18 h6 M14 26 h6 M14 34 h6 M28 28 h6 M28 36 h6 M6 42 h36",
         "car": "M9 30 l4 -9 a4 4 0 0 1 3.6 -2.4 h14.8 a4 4 0 0 1 3.6 2.4 l4 9 M7 30 h34 v7 h-34 z "
                "M13 37 v3.5 M35 37 v3.5 M15.5 33.5 h4 M28.5 33.5 h4"}[kind]
    return ('<g transform="translate(%.1f %.1f) scale(%.3f)" fill="none" stroke="%s" stroke-width="%.2f" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="%s"/></g>') % (x, y, s, stroke, sw, P)

# ---------------------------------------------------------------- diagrams (140 x 120 box)
def dia(kind, x, y, w=150, h=118):
    o = []
    if kind == "angle":                      # camera below, looking up
        o.append(line(x + 8, y + h - 14, x + w - 8, y + h - 14, INK, 1, .3))
        o.append(rect(x + 16, y + h - 30, 26, 16, INK))
        o.append(path("M %.1f %.1f l 12 -6 v 12 z" % (x + 42, y + h - 28), fill=INK))
        o.append(line(x + 30, y + h - 30, x + w - 26, y + 18, AMBER, 1.4, 1, dash="5 5"))
        o.append(circ(x + w - 22, y + 16, 9, fill=INK))
        o.append(path("M %.1f %.1f a 44 44 0 0 1 34 -20" % (x + 30, y + h - 30),
                      stroke=AMBER, sw=1, op=.7))
        o.append(t(x + 62, y + h - 40, "35°", size=11, fill=AMBER))
    elif kind == "backlight":                # sun behind subject
        o.append(circ(x + w - 34, y + 40, 20, fill=GOLD, op=.95))
        for a in range(8):
            an = a * math.pi / 4
            o.append(line(x + w - 34 + math.cos(an) * 26, y + 40 + math.sin(an) * 26,
                          x + w - 34 + math.cos(an) * 34, y + 40 + math.sin(an) * 34, GOLD, 1.2, .8))
        o.append(rect(x + w - 76, y + 26, 26, 46, INK))
        o.append(rect(x + 16, y + h - 40, 26, 16, INK))
        o.append(path("M %.1f %.1f l 12 -6 v 12 z" % (x + 42, y + h - 38), fill=INK))
        o.append(line(x + 56, y + h - 32, x + w - 78, y + 52, INK, 1.2, .5, dash="5 5"))
    elif kind == "air":                      # rule of air
        o.append(rect(x + 12, y + 10, w - 24, h - 26, PEARL, op=.5, stroke=INK, sw=.8))
        o.append(line(x + 12, y + 10 + (h - 26) / 3, x + w - 12, y + 10 + (h - 26) / 3, INK, .8, .3, dash="4 5"))
        o.append(line(x + 12, y + 10 + 2 * (h - 26) / 3, x + w - 12, y + 10 + 2 * (h - 26) / 3, INK, .8, .3, dash="4 5"))
        o.append(circ(x + w - 44, y + h - 44, 13, fill=INK))
        o.append(t(x + 26, y + 42, tr("aire", "air"), size=12, fill=GREY))
        o.append(t(x + 26, y + h - 22, "⅔ / ⅓", size=12, fill=AMBER))
    elif kind == "one":                      # one subject
        o.append(circ(x + 44, y + 52, 17, fill=INK))
        for i in range(2):
            cx = x + 96 + i * 34
            o.append(circ(cx, y + 52, 13, fill="none", stroke=CLAY, sw=1.2, op=.8))
            o.append(line(cx - 9, y + 43, cx + 9, y + 61, CLAY, 1.2, .8))
        o.append(t(x + 30, y + h - 16, tr("uno", "one"), size=12, fill=GREY))
    elif kind == "threshold":                # subject crossing a line
        o.append(rect(x + 12, y + 10, w - 24, h - 26, PEARL, op=.35))
        o.append(line(x + 12, y + 62, x + w - 12, y + 62, AMBER, 1.6))
        o.append(circ(x + w / 2 - 4, y + 48, 15, fill=INK))
        o.append(t(x + 22, y + h - 18, tr("umbral", "threshold"), size=12, fill=GREY))
    elif kind == "matter":
        o.append(photo(KIT + "/05_Textures/velum-basalto.jpg", x + 12, y + 10, w - 24, h - 26, px=420))
        o.append(rect(x + 12, y + 10, w - 24, h - 26, "none", stroke=INK, sw=.8))
    elif kind == "colour":
        for i, c in enumerate([INK, GROUND, GOLD]):
            o.append(rect(x + 14 + i * 42, y + 24, 36, 58, c, stroke=INK, sw=.7))
        o.append(t(x + 14, y + h - 16, "#0B1D34 · #F4F0EE · #D4AF37", size=10.5, fill=GREY))
    return "".join(o)

PRINCIPLES = [
    ("angle", "01", tr("Contrapicado", "Low angle"),
     tr(["La cámara por debajo", "del sujeto, 30–45°."], ["Camera below the", "subject, 30–45°."])),
    ("backlight", "02", tr("Contraluz", "Backlight"),
     tr(["La luz detrás. Silueta", "con borde cálido."], ["Light behind. Silhouette", "with a warm rim."])),
    ("air", "03", tr("Aire", "Air"),
     tr(["60–70% del encuadre", "vacío. El aire es el tema."], ["60–70% of the frame", "empty. Air is the subject."])),
    ("one", "04", tr("Un sujeto", "One subject"),
     tr(["Un objeto, un gesto.", "Nunca un bodegón."], ["One object, one gesture.", "Never a still life."])),
    ("threshold", "05", tr("El umbral", "The threshold"),
     tr(["Un límite que se cruza:", "horizonte, borde, vano."], ["A limit being crossed:", "horizon, edge, doorway."])),
    ("matter", "06", tr("Materia dura", "Hard matter"),
     tr(["Piedra, hormigón,", "asfalto, metal."], ["Stone, concrete,", "asphalt, metal."])),
    ("colour", "07", tr("Color", "Colour"),
     tr(["Sombra azul, luz hueso,", "un solo acento de oro."], ["Blue shadow, bone light,", "one gold accent."])),
]

HOUSES = [("plane", "Velum Travel", tr("Avión, ala, estela", "Aircraft, wing, contrail")),
          ("bottle", "AL — Ana López", tr("Frasco, vidrio, jazmín", "Bottle, glass, jasmine")),
          ("cloche", "Velum Foods", tr("Materia prima, mesa", "Raw ingredient, table")),
          ("globe", "Velum Trade", tr("Grúa, contenedor, muelle", "Crane, container, dock")),
          ("building", "Velum Properties", tr("Esquina, escalera, vano", "Corner, stair, doorway")),
          ("car", "Velum Mobility", tr("Coche, carga, carretera", "Vehicle, charge, road"))]

YES = tr(["Siluetas limpias contra luz abierta",
          "Cielo con estructura: capas, estelas",
          "Superficies duras con textura real",
          "Escala: lo pequeño revela lo enorme",
          "Un solo destello cálido"],
         ["Clean silhouettes against open light",
          "Skies with structure: layers, contrails",
          "Hard surfaces with real texture",
          "Scale: the small reveals the enormous",
          "A single warm flare"])

NO = tr(["Planetas, cohetes, astronautas, galaxias",
         "Personas posando, equipos de oficina",
         "Saturación alta, teal-orange, neón, HDR",
         "Collages de producto y bodegones",
         "Drones cenitales: mirar hacia abajo"],
        ["Planets, rockets, astronauts, galaxies",
         "People posing, office teams",
         "High saturation, teal-orange, neon, HDR",
         "Product collages and still lifes",
         "Top-down drones: looking down"])

SPEC = [("24–35 mm", tr("Contrapicado y cielo", "Low angle and sky")),
        ("85–135 mm", tr("Detalle y horizonte", "Detail and horizon")),
        ("f/8 – f/11", tr("Planos de cielo", "Sky frames")),
        (tr("Hora dorada", "Golden hour"), tr("±40 min, y hora azul", "±40 min, and blue hour")),
        ("4:5 · 2:3", tr("Mirada hacia arriba", "The upward gaze")),
        ("16:9 · 2:1", tr("Horizontes", "Horizons"))]

def build():
    o = [rect(0, 0, W, H, GROUND)]

    # ---------- header: the north star
    hx, hy, hw, hh = M, M, W - 2 * M, 700
    o.append(photo(SEC + "/References/velum-foto-01-travel-avion-contrapicado.png", hx, hy, hw, hh, px=1500))
    o.append(rect(hx, hy, hw, hh, INK, op=0.30))
    o.append(rect(hx, hy + hh - 300, hw, 300, INK, op=0.42))
    o.append(logo("primary-dark-bg", hx + 60, hy + 54, 240))
    o.append(label(hx + 60, hy + hh - 210, tr("Dirección de fotografía", "Photography direction"),
                   fill=GOLD, size=12))
    o.append(t(hx + 60, hy + hh - 132, tr("LA MIRADA HACIA ARRIBA", "THE UPWARD GAZE"),
               size=54, f=DIS, fill="#F7F7F7", ls=4))
    o.append(t(hx + 60, hy + hh - 74,
               tr("Una sola forma de mirar para seis negocios distintos.",
                  "One way of looking, for six different businesses."),
               size=19, fill=PEARL))
    o.append(label(hx + hw - 60, hy + hh - 74, tr("Referencia madre", "Parent reference"),
                   fill=PEARL, size=9, anchor="end"))

    # ---------- principles
    y0 = 830
    o.append(label(M, y0, tr("Los siete principios", "The seven principles"), fill=AMBER))
    o.append(t(M, y0 + 62, tr("SI SE PUEDE DESCRIBIR SIN DECIR EL SECTOR, ESTÁ BIEN HECHA",
                              "IF IT CAN BE DESCRIBED WITHOUT NAMING THE SECTOR, IT WORKS"),
               size=27, f=DIS, fill=INK, ls=2))
    o.append(line(M, y0 + 96, W - M, y0 + 96, INK, .8, .18))

    cw = (W - 2 * M) / 4.0
    for i, (kind, num, name, lines) in enumerate(PRINCIPLES):
        x = M + (i % 4) * cw
        y = y0 + 130 + (i // 4) * 280
        o.append(rect(x, y, cw - 24, 130, CREAM, op=.42))
        o.append(dia(kind, x, y + 6, cw - 24, 124))
        o.append(t(x, y + 172, num, size=12, w=600, fill=AMBER, ls=2))
        o.append(t(x, y + 206, name.upper(), size=21, f=DIS, fill=INK, ls=2))
        o.append(para(x, y + 240, lines, size=14, lh=23))

    # ---------- houses
    y1 = 1700
    o.append(line(M, y1 - 46, W - M, y1 - 46, INK, .8, .18))
    o.append(label(M, y1, tr("Qué fotografía cada casa", "What each house photographs"), fill=AMBER))
    o.append(t(M, y1 + 54, tr("LA GRAMÁTICA NO CAMBIA; CAMBIA EL SUJETO",
                              "THE GRAMMAR DOES NOT CHANGE; THE SUBJECT DOES"),
               size=24, f=DIS, fill=INK, ls=2))
    hw2 = (W - 2 * M) / 6.0
    for i, (ic, name, subj) in enumerate(HOUSES):
        x = M + i * hw2
        o.append(icon(ic, x, y1 + 96, 1.15))
        o.append(t(x, y1 + 190, name.upper(), size=13, f=DIS, fill=INK, ls=1.2))
        o.append(para(x, y1 + 218, [subj], size=12.5, lh=20))
    o.append(t(M, y1 + 286, tr("Tres tomas por casa en cada sesión:  mirada  ·  materia  ·  umbral",
                               "Three frames per house on every shoot:  gaze  ·  matter  ·  threshold"),
               size=15, fill=INK, op=.9))

    # ---------- spec + do/don't
    y2 = 2070
    o.append(line(M, y2 - 40, W - M, y2 - 40, INK, .8, .18))
    o.append(label(M, y2, tr("Ficha técnica", "Technical spec"), fill=AMBER))
    for i, (k, v) in enumerate(SPEC):
        yy = y2 + 52 + i * 58
        o.append(t(M, yy, k, size=19, f=DIS, fill=INK, ls=1.2))
        o.append(t(M + 210, yy, v, size=14, fill=GREY))
        o.append(line(M, yy + 20, M + 480, yy + 20, INK, .7, .12))

    xg = M + 580
    o.append(label(xg, y2, tr("Buscamos", "We look for"), fill=AMBER))
    for i, v in enumerate(YES):
        o.append(t(xg, y2 + 52 + i * 44, "— " + v, size=15, fill=INK, op=.88))
    xn = M + 1180
    o.append(label(xn, y2, tr("Evitamos", "We avoid"), fill=CLAY))
    for i, v in enumerate(NO):
        o.append(t(xn, y2 + 52 + i * 44, "✕  " + v, size=15, fill=GREY))

    # ---------- logo over photo
    y3 = 2430
    o.append(rect(M, y3, W - 2 * M, 190, INK))
    o.append(photo(KIT + "/05_Textures/velum-cielo-nocturno.jpg", M, y3, W - 2 * M, 190, px=1100, op=.55))
    o.append(label(M + 50, y3 + 54, tr("El logotipo sobre foto", "The logotype over photography"),
                   fill=GOLD, size=10))
    o.append(para(M + 50, y3 + 96, tr(
        ["Zona más limpia y oscura, nunca sobre el sujeto. Una sola tinta: blanco sobre imagen",
         "oscura, azul sobre clara. Sin caja de fondo. Área «x» completa. Logotipo o texto, no ambos."],
        ["The cleanest, darkest area, never over the subject. One ink: white on a dark image,",
         "blue on a light one. No background box. Full «x» clear space. Logotype or text, not both."]),
        size=15, lh=27, fill=PEARL))
    o.append(logo("primary-blanco", W - M - 290, y3 + 66, 230))

    o.append(label(M, H - 40, "VELUM  ·  " + tr("Dirección de fotografía 1.0  ·  2026",
                                                "Photography direction 1.0  ·  2026"), fill=GREY, size=9.5))
    o.append(label(W - M, H - 40, tr("07_Photography", "07_Photography"), fill=GREY, size=9.5, anchor="end"))

    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>'
            % (W, H, W, H, "".join(o)))

if __name__ == "__main__":
    name = "velum-photography-board" + ("" if ES else "-en")
    p = OUT + "/%s.svg" % name
    open(p, "w", encoding="utf-8").write(build())
    print(p, os.path.getsize(p) // 1024, "KB")
