# -*- coding: utf-8 -*-
"""One-shot: convert board.py to the light system (#F4F0EE) and the new narrative."""
import io

p = 'board.py'
s = open(p, encoding='utf-8').read()

R = []

R.append(('''INK, NAVY, GOLD, CREAM, PEARL, IVORY, BLACK, GREY = (
    "#0B1D34", "#20344D", "#D4AF37", "#E8DCC0", "#DADDE3", "#F7F7F7", "#1A1A1A", "#55585F")

SER = "Cormorant Garamond, Georgia, serif"
SAN = "Montserrat, Poppins, Arial, sans-serif"''',
'''GROUND, INK, NAVY, GOLD, CREAM, PEARL, IVORY, BLACK, GREY, AMBER = (
    "#F4F0EE", "#0B1D34", "#20344D", "#D4AF37", "#E8DCC0", "#DADDE3", "#F7F7F7",
    "#1A1A1A", "#55585F", "#B8912B")

DIS = "Cinzel, Cormorant Garamond, Georgia, serif"
SER = "Cormorant Garamond, Georgia, serif"
SAN = "Montserrat, Poppins, Arial, sans-serif"'''))

R.append(('def t(x, y, s, size=16, f=SAN, w=400, fill=IVORY,', 'def t(x, y, s, size=16, f=SAN, w=400, fill=INK,'))
R.append(('def label(x, y, s, fill=GOLD, size=12, anchor="start"):', 'def label(x, y, s, fill=AMBER, size=12, anchor="start"):'))
R.append(('def para(x, y, lines, size=17, lh=30, fill=IVORY, op=0.8,', 'def para(x, y, lines, size=17, lh=30, fill=GREY, op=1.0,'))

R.append(('# ---------------------------------------------------------------- board',
'''def veil(x, y, w, h, n=9, stroke=GOLD, sw=1.4, op=0.5, spread=1.0):
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

# ---------------------------------------------------------------- board'''))

R.append(('import os, re, io, base64', 'import os, re, io, math, base64'))

# ---------------- header
R.append(('    o = [rect(0, 0, W, H, INK)]', '    o = [rect(0, 0, W, H, GROUND)]'))
R.append(('''    o.append(photo(KIT + "/05_Textures/velum-gradiente-04-aurora.jpg", hx, hy, hw, hh, px=1400, op=0.95))
    o.append(rect(hx, hy, hw, hh, INK, op=0.62))
    g, gh = logo("primary-dark-bg", hx + 90, hy + 210, 720)''',
'''    o.append(photo(KIT + "/05_Textures/velum-yeso-hueso.jpg", hx, hy, hw, hh, px=1300))
    o.append(veil(hx, hy + 190, hw, 400, n=16, stroke=INK, sw=1.1, op=0.10, spread=1.2))
    g, gh = logo("primary-light-bg", hx + 90, hy + 210, 720)'''))
R.append(('o.append(label(hx + 90, hy + 678, "Grupo empresarial  ·  La Habana, Cuba", fill=PEARL, size=12))',
          'o.append(label(hx + 90, hy + 678, "Grupo empresarial  ·  La Habana, Cuba", fill=GREY, size=12))'))
R.append(('o.append(line(hx + 960, hy + 90, hx + 960, hy + hh - 90, stroke=PEARL, sw=0.8, op=0.3))',
          'o.append(line(hx + 960, hy + 90, hx + 960, hy + hh - 90, stroke=INK, sw=0.8, op=0.25))'))
R.append(('''    o.append(t(rx, hy + 238, "Velum significa", size=44, f=SER, fill=IVORY))
    o.append(t(rx, hy + 292, "velo, en latín.", size=44, f=SER, fill=IVORY, italic=True))''',
'''    o.append(t(rx, hy + 244, "MÁS ALLÁ", size=46, f=DIS, fill=INK, ls=3))
    o.append(t(rx, hy + 302, "DE LO VISIBLE", size=46, f=DIS, fill=INK, ls=3))'''))
R.append(('''        "El vínculo entre lo visible y lo desconocido: la exploración",
        "de nuevos horizontes y la conexión de mundos distintos para",
        "crear experiencias, productos y servicios que transforman.",
    ], size=17, lh=31, fill=IVORY, op=0.8))''',
'''        "Velum significa velo, en latín: lo que separa lo que vemos",
        "de lo que hay detrás. También la vela que atrapa el viento.",
        "Curiosidad y dirección en una sola palabra.",
    ], size=17, lh=31, fill=GREY))'''))
R.append(('''    for i, (k, v) in enumerate([("Velo", "Conexión"), ("Estrella", "Visión"), ("Mundos", "Diversidad"),
                                ("Horizonte", "Expansión"), ("Trayectoria", "Crecimiento")]):
        cx = rx + i * 152
        o.append(line(cx, hy + 566, cx + 120, hy + 566, stroke=PEARL, sw=0.8, op=0.35))
        o.append(t(cx, hy + 610, k, size=21, f=SER, fill=IVORY))
        o.append(t(cx, hy + 638, v, size=11.5, f=SAN, fill=GOLD, op=0.9))''',
'''    for i, (k, v) in enumerate([("Descubrir", "Mirar más allá"), ("Conectar", "Unir mundos"),
                                ("Transformar", "Hacerlo tangible")]):
        cx = rx + i * 250
        o.append(line(cx, hy + 566, cx + 210, hy + 566, stroke=GOLD, sw=1))
        o.append(t(cx, hy + 616, k.upper(), size=24, f=DIS, fill=INK, ls=2))
        o.append(t(cx, hy + 646, v, size=12.5, f=SAN, fill=GREY))'''))

# ---------------- row 2
R.append(('o.append(label(M, y2, "Variaciones del logo", fill=PEARL))', 'o.append(label(M, y2, "Variaciones del logo", fill=AMBER))'))
R.append(('''    tiles = [("Fondo oscuro", INK, "primary-dark-bg"), ("Fondo claro", CREAM, "primary-light-bg"),
             ("Una tinta · oro", NAVY, "primary-oro"), ("Sello", NAVY, "seal")]''',
'''    tiles = [("Fondo hueso", GROUND, "primary-light-bg"), ("Fondo oscuro", INK, "primary-dark-bg"),
             ("Una tinta · oro", INK, "primary-oro"), ("Sello", NAVY, "seal")]'''))
R.append(('o.append(rect(x, y2 + 34, tw, 232, "none", stroke=PEARL, sw=0.8, op=0.25))',
          'o.append(rect(x, y2 + 34, tw, 232, "none", stroke=INK, sw=0.8, op=0.25))'))
R.append(('o.append(label(x, y2 + 302, cap, fill=PEARL, size=9.5))', 'o.append(label(x, y2 + 302, cap, fill=GREY, size=9.5))'))
R.append(('o.append(label(px_, y2, "Paleta", fill=PEARL))', 'o.append(label(px_, y2, "Paleta", fill=AMBER))'))
R.append(('''    PAL = [("Azul Velum", INK), ("Azul Medio", NAVY), ("Oro Velum", GOLD), ("Crema", CREAM),
           ("Gris Perla", PEARL), ("Blanco", IVORY), ("Gris", GREY), ("Negro", BLACK)]''',
'''    PAL = [("Blanco Hueso", GROUND), ("Azul Velum", INK), ("Oro Velum", GOLD), ("Crema", CREAM),
           ("Azul Medio", NAVY), ("Gris Perla", PEARL), ("Gris", GREY), ("Negro", BLACK)]'''))
R.append(('o.append(rect(x, y, sw_, 98, "none", stroke=PEARL, sw=0.7, op=0.3))', 'o.append(rect(x, y, sw_, 98, "none", stroke=INK, sw=0.7, op=0.3))'))
R.append(('o.append(t(x, y + 122, n, size=11.5, fill=IVORY, op=0.9))', 'o.append(t(x, y + 122, n, size=11.5, fill=INK, op=0.9))'))
R.append(('o.append(t(x, y + 140, hx_.upper(), size=10.5, fill=PEARL, op=0.6))', 'o.append(t(x, y + 140, hx_.upper(), size=10.5, fill=GREY))'))
R.append(('o.append(label(tx, y2, "Tipografías", fill=PEARL))', 'o.append(label(tx, y2, "Tipografías", fill=AMBER))'))
R.append(('''    fams = [("Aa", SER, "Cormorant Garamond", "Display y editorial"),
            ("Aa", SAN, "Montserrat", "Texto y sistema"),
            ("Aa", "Cinzel, " + SER, "Cinzel Display", "Titulación ceremonial")]''',
'''    fams = [("Aa", DIS, "Cinzel Display", "Marca y titulares"),
            ("Aa", SAN, "Montserrat", "Texto y sistema")]'''))
R.append(('''        y = y2 + 96 + i * 108
        o.append(t(tx, y, aa, size=52, f=f, fill=IVORY))''',
'''        y = y2 + 120 + i * 150
        o.append(t(tx, y, aa, size=58, f=f, fill=INK))'''))
R.append(('o.append(t(tx + 96, y - 18, name, size=18, f=SER, fill=IVORY))', 'o.append(t(tx + 120, y - 20, name, size=18, f=DIS, fill=INK, ls=1.5))'))
R.append(('o.append(t(tx + 96, y + 4, role, size=11.5, fill=GOLD, op=0.9))', 'o.append(t(tx + 120, y + 6, role, size=11.5, fill=AMBER))'))
R.append(('''        if i < 2:
            o.append(line(tx, y + 42, tx + 300, y + 42, stroke=PEARL, sw=0.8, op=0.22))''',
'''        if i < 1:
            o.append(line(tx, y + 52, tx + 300, y + 52, stroke=INK, sw=0.8, op=0.2))'''))

# ---------------- row 3
R.append(('o.append(line(M, y3 - 44, W - M, y3 - 44, stroke=PEARL, sw=0.8, op=0.22))', 'o.append(line(M, y3 - 44, W - M, y3 - 44, stroke=INK, sw=0.8, op=0.2))'))
R.append(('o.append(label(M, y3, "Divisiones", fill=PEARL))', 'o.append(label(M, y3, "Las seis casas", fill=AMBER))'))
R.append(('''    DIV = [("viajes", "Viajes"), ("perfumeria", "Perfumería"), ("alimentos", "Alimentos"),
           ("importacion-exportacion", "Import. y export."), ("inmuebles", "Inmuebles"),
           ("vehiculos-electricos", "Vehículos eléctricos")]''',
'''    DIV = [("viajes", "Velum Travel"), ("perfumeria", "AL — Ana López"), ("alimentos", "Velum Foods"),
           ("importacion-exportacion", "Velum Trade"), ("inmuebles", "Velum Properties"),
           ("vehiculos-electricos", "Velum Mobility")]'''))
R.append(('o.append(rect(x, y3 + 34, dw, 190, NAVY, op=0.55))', 'o.append(rect(x, y3 + 34, dw, 190, CREAM, op=0.45))'))
R.append(('o.append(t(x + dw / 2, y3 + 258, cap, size=15, fill=IVORY, op=0.9, anchor="middle"))',
          'o.append(t(x + dw / 2, y3 + 258, cap.upper(), size=13, f=DIS, fill=INK, ls=1.2, anchor="middle"))'))
R.append(('o.append(label(ex, y3, "Elementos", fill=PEARL))', 'o.append(label(ex, y3, "El velo", fill=AMBER))'))
R.append(('o.append(rect(ex, y3 + 34, W - M - ex, 190, NAVY, op=0.55))', 'o.append(rect(ex, y3 + 34, W - M - ex, 190, CREAM, op=0.45))'))
R.append(('''    g, gh = elem("trazo-blanco", ex + 40, y3 + 74, 340)
    o.append(g)
    g, gh = elem("estrella-oro", ex + 392, y3 + 66, 46)
    o.append(g)''',
'''    o.append(veil(ex + 34, y3 + 78, 300, 104, n=9, stroke=INK, sw=1.3, op=0.5))
    g, gh = elem("estrella-oro", ex + 372, y3 + 84, 42)
    o.append(g)'''))
R.append(('o.append(t(ex + 40, y3 + 258, "El trazo, la estrella y las tramas", size=15, fill=IVORY, op=0.9))',
          'o.append(t(ex + 40, y3 + 258, "Un gesto, seis lecturas", size=15, fill=INK, op=0.9))'))
R.append(('o.append(rect(cx, cy, cs, cs, INK))', 'o.append(rect(cx, cy, cs, cs, GROUND))'))
R.append(('o.append(line(cx + k * 9, cy - 10, cx + k * 9 + 90, cy + cs + 10, stroke=PEARL, sw=1.4))',
          'o.append(line(cx + k * 9, cy - 10, cx + k * 9 + 90, cy + cs + 10, stroke=INK, sw=1.2))'))
R.append(('o.append(line(cx + k, cy, cx + k, cy + cs, stroke=PEARL, sw=0.9))', 'o.append(line(cx + k, cy, cx + k, cy + cs, stroke=INK, sw=0.8))'))
R.append(('o.append(line(cx, cy + k, cx + cs, cy + k, stroke=PEARL, sw=0.9))', 'o.append(line(cx, cy + k, cx + cs, cy + k, stroke=INK, sw=0.8))'))
R.append(('o.append(rect(cx, cy, cs, cs, "none", stroke=PEARL, sw=0.7, op=0.35))', 'o.append(rect(cx, cy, cs, cs, "none", stroke=INK, sw=0.7, op=0.35))'))

# ---------------- row 4
R.append(('o.append(line(M, y4 - 44, W - M, y4 - 44, stroke=PEARL, sw=0.8, op=0.22))', 'o.append(line(M, y4 - 44, W - M, y4 - 44, stroke=INK, sw=0.8, op=0.2))'))
R.append(('o.append(label(M, y4, "Aplicaciones", fill=PEARL))', 'o.append(label(M, y4, "Aplicaciones", fill=AMBER))'))
R.append(('''    o.append(rect(bx, by, bw, bh, "#0D2136"))
    o.append(rect(bx, by, bw, 26, NAVY))''',
'''    o.append(rect(bx, by, bw, bh, GROUND, stroke=INK, sw=0.7))
    o.append(rect(bx, by, bw, 26, CREAM))'''))
R.append(('o.append(rect(bx + 62, by + 6, 130, 14, INK, rx=7))', 'o.append(rect(bx + 62, by + 6, 130, 14, GROUND, rx=7, stroke=INK, sw=0.5))'))
R.append(('''    o.append(photo(KIT + "/05_Textures/velum-gradiente-03-altura.jpg", bx, by + 26, bw, bh - 26, px=800))
    o.append(rect(bx, by + 26, bw, bh - 26, INK, op=0.55))
    g, gh = logo("primary-dark-bg", bx + 22, by + 46, 96)''',
'''    o.append(veil(bx, by + 110, bw, 210, n=10, stroke=INK, sw=1, op=0.12))
    g, gh = logo("primary-light-bg", bx + 22, by + 46, 96)'''))
R.append(('        o.append(label(bx + 170 + i * 88, by + 66, n, fill=IVORY, size=7))', '        o.append(label(bx + 170 + i * 88, by + 66, n, fill=GREY, size=7))'))
R.append(('''    o.append(t(bx + 22, by + 236, "El cielo no", size=34, f=SER, fill=IVORY))
    o.append(t(bx + 22, by + 274, "tiene límites.", size=34, f=SER, fill=IVORY, italic=True))
    o.append(rect(bx + 22, by + 300, 108, 28, "none", stroke=GOLD, sw=1))
    o.append(label(bx + 36, by + 318, "Ver más", fill=GOLD, size=7.5))''',
'''    o.append(t(bx + 22, by + 242, "MÁS ALLÁ", size=30, f=DIS, fill=INK, ls=2))
    o.append(t(bx + 22, by + 282, "DE LO VISIBLE", size=30, f=DIS, fill=INK, ls=2))
    o.append(rect(bx + 22, by + 308, 120, 30, INK))
    o.append(label(bx + 37, by + 328, "Ver más", fill=GROUND, size=7.5))'''))
R.append(('''    o.append(photo(KIT + "/05_Textures/velum-gradiente-01-horizonte.jpg", x3, y4 + 34, aw, 380, px=900))
    o.append(rect(x3, y4 + 34, aw, 380, INK, op=0.5))''',
'''    o.append(photo(KIT + "/05_Textures/velum-cielo-nocturno.jpg", x3, y4 + 34, aw, 380, px=900))'''))
R.append(('    o.append(rect(x4, y4 + 34, aw, 380, NAVY))', '    o.append(rect(x4, y4 + 34, aw, 380, CREAM, op=0.5))'))
R.append(('o.append(t(x4 + aw / 2, y4 + 340, "@velum", size=24, f=SER, fill=IVORY, anchor="middle"))',
          'o.append(t(x4 + aw / 2, y4 + 340, "@VELUM", size=22, f=DIS, fill=INK, ls=3, anchor="middle"))'))
R.append(('        o.append(label(M + i * (aw + 20), y4 + 448, cap, fill=PEARL, size=9.5))', '        o.append(label(M + i * (aw + 20), y4 + 448, cap, fill=GREY, size=9.5))'))

# ---------------- footer
R.append(('''    o.append(photo(KIT + "/05_Textures/velum-gradiente-05-bruma.jpg", M, fy, W - 2 * M, 400, px=1200, op=0.9))
    o.append(rect(M, fy, W - 2 * M, 400, INK, op=0.72))
    o.append(label(M + 70, fy + 90, "Esencia", fill=GOLD, size=11))
    o.append(para(M + 70, fy + 150, ["Conexión que impulsa.", "Experiencias que transforman.",
                                     "Horizontes que inspiran.", "Posibilidades que no tienen límites."],
                  size=19, lh=34, fill=IVORY, op=0.9, f=SER))''',
'''    o.append(rect(M, fy, W - 2 * M, 400, INK))
    o.append(veil(M, fy + 70, W - 2 * M, 260, n=14, stroke=GOLD, sw=1.1, op=0.16, spread=1.1))
    o.append(label(M + 70, fy + 100, "El relato", fill=GOLD, size=11))
    o.append(para(M + 70, fy + 160, ["Un viaje puede convertirse en experiencia.",
                                     "Un aroma, en un recuerdo.",
                                     "Un espacio, en un destino.",
                                     "Una idea, en un negocio."],
                  size=19, lh=34, fill=IVORY, f=SER, italic=True))'''))
R.append(('    g, gh = logo("monogram-dark-bg", M + 860, fy + 150, 160)', '    g, gh = logo("monogram-dark-bg", M + 900, fy + 150, 150)'))
R.append(('''    o.append(t(W - M - 70, fy + 170, "El cielo no", size=40, f=SER, fill=IVORY, anchor="end"))
    o.append(t(W - M - 70, fy + 222, "tiene límites.", size=40, f=SER, fill=IVORY, anchor="end", italic=True))''',
'''    o.append(t(W - M - 70, fy + 180, "EL CIELO ES", size=36, f=DIS, fill=IVORY, anchor="end", ls=3))
    o.append(t(W - M - 70, fy + 232, "EL LÍMITE.", size=36, f=DIS, fill=IVORY, anchor="end", ls=3))'''))
R.append(('o.append(label(W - M - 70, fy + 316, "Velum Enterprise", fill=PEARL, size=10, anchor="end"))',
          'o.append(label(W - M - 70, fy + 316, "Descubrir · Conectar · Transformar", fill=PEARL, size=10, anchor="end"))'))
R.append(('o.append(label(M, H - 26, "VELUM  ·  Brand board  ·  v1.0  ·  2026", fill=GREY, size=9.5))',
          'o.append(label(M, H - 26, "VELUM  ·  Brand board  ·  v2.0  ·  2026", fill=GREY, size=9.5))'))

missing = []
for a, b in R:
    if a not in s:
        missing.append(a.splitlines()[0][:70])
    s = s.replace(a, b)

open(p, 'w', encoding='utf-8').write(s)
print("replacements:", len(R), "| not found:", len(missing))
for m in missing:
    print("  MISS:", m)
