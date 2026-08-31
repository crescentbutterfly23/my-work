# -*- coding: utf-8 -*-
"""VELUM manual — pages 19-36."""
from core import *
from parts import head, divider, icon, yes_no, foot

S2 = "02 — %s"
S3 = "03 — %s"
S4 = "04 — %s"
S5 = "05 — %s"
S6 = "06 — %s"

def _rgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

def _cmyk(h):
    r, g, b = [v / 255.0 for v in _rgb(h)]
    k = 1 - max(r, g, b)
    if k >= 0.999:
        return (0, 0, 0, 100)
    return tuple(int(round(v * 100)) for v in ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k),
                                               (1 - b - k) / (1 - k), k))

def _lum(h):
    def f(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = _rgb(h)
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def _ratio(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

PAL = [("Blanco Hueso", "Bone White", GROUND), ("Azul Velum", "Velum Blue", INK),
       ("Oro Velum", "Velum Gold", GOLD), ("Crema", "Cream", PAPER),
       ("Azul Medio", "Mid Blue", NAVY), ("Oro Oscuro", "Deep Gold", AMBER),
       ("Gris Perla", "Pearl Grey", PEARL), ("Gris", "Grey", GREY), ("Negro", "Black", BLACK)]

def _pname(p, L):
    return p[0] if L["lang"] == "ES" else p[1]

# ---------------------------------------------------------------- 19 colour versions
def p19(L):
    o = head(L, S2 % L["sections"][1][1], 19, L["id_col_eyebrow"], L["id_col_title"])
    tiles = [(GROUND, "light"), (PAPER, "light"), (PEARL, "light"),
             (INK, "dark"), (NAVY, "gold"), (BLACK, "dark"), (GOLD, "navy")]
    cw, ch = (W - 2 * M - 6 * 18) / 7.0, 300
    for i, (bg, mode) in enumerate(tiles):
        x = M + i * (cw + 18)
        o.append(rect(x, 420, cw, ch, bg))
        o.append(rect(x, 420, cw, ch, "none", stroke=INK, sw=0.7, op=0.22))
        o.append(mono_logo(x + cw / 2 - 52, 520, 104, mode))
        nm = {"light": ("Azul / Negro", "Blue / Black"), "dark": ("Blanco / Perla", "White / Pearl"),
              "gold": ("Oro", "Gold"), "navy": ("Azul", "Blue")}[mode]
        o.append(label(x, 762, nm[0] if L["lang"] == "ES" else nm[1], fill=GREY, size=9))
    o.append(line(M, 830, W - M, 830, stroke=INK, sw=0.7, op=0.16))
    o.append(full_logo(M, 880, 320, "light"))
    o.append(rect(M + 400, 866, 380, 120, INK))
    o.append(full_logo(M + 430, 890, 320, "dark"))
    o.append(rect(M + 820, 866, 380, 120, PAPER))
    o.append(full_logo(M + 850, 890, 320, "light"))
    o.append(foot(L["id_col_foot"], y=1024))
    return page("".join(o))

# ---------------------------------------------------------------- 20 misuse
def p20(L):
    o = head(L, S2 % L["sections"][1][1], 20, L["id_mis_eyebrow"], L["id_mis_title"])
    cw, ch = (W - 2 * M - 2 * 30) / 3.0, 238

    def base(x, y, w=330):
        return full_logo(x + cw / 2 - w / 2, y + ch / 2 - w * 0.223, w, "light")

    for i in range(6):
        x = M + (i % 3) * (cw + 30)
        y = 400 + (i // 3) * (ch + 80)
        bg = PAPER if i != 5 else NAVY
        o.append(rect(x, y, cw, ch, bg, op=(0.5 if i != 5 else 1)))
        o.append(rect(x, y, cw, ch, "none", stroke=INK, sw=0.7, op=0.2))
        cxm, cym = x + cw / 2, y + ch / 2
        if i == 0:
            o.append('<g transform="translate(%.1f %.1f) scale(1.25 0.62) translate(%.1f %.1f)">%s</g>'
                     % (cxm, cym, -cxm, -cym, base(x, y)))
        elif i == 1:
            o.append('<g transform="rotate(-11 %.1f %.1f)">%s</g>' % (cxm, cym, base(x, y)))
        elif i == 2:
            o.append(base(x, y).replace(GOLD, "#7CFF3C").replace(BLACK, "#C42BB5").replace(INK, "#7CFF3C"))
        elif i == 3:
            sh = base(x, y).replace(GOLD, "#9A9A9A").replace(BLACK, "#9A9A9A").replace(INK, "#9A9A9A")
            o.append('<g opacity="0.55" transform="translate(9 10)">%s</g>' % sh)
            o.append(base(x, y))
        elif i == 4:
            o.append(mono_logo(x + 44, y + 58, 150, "light"))
            o.append(star(x + cw - 74, y + 66, 16))
            o.append(sweep(x + cw - 250, y + 178, 200, stroke=INK, sw=2.4, rise=44))
        else:
            o.append(base(x, y))
        o.append(circ(x + cw - 34, y + 34, 15, fill=CLAY))
        o.append(t(x + cw - 34, y + 40, "✕", size=15, fill=GROUND, anchor="middle", w=600))
        o.append(label(x, y + ch + 32, L["id_mis"][i], fill=GREY, size=10, w=500))
    return page("".join(o))

# ---------------------------------------------------------------- 21 monogram
def p21(L):
    o = head(L, S2 % L["sections"][1][1], 21, L["id_mono_eyebrow"], L["id_mono_title"], L["id_mono_body"])
    o.append(rect(M, 460, 760, 400, PAPER, op=0.4))
    o.append(mono_logo(M + 200, 540, 360, "light"))
    o.append(label(M + 900, 500, L["id_mono_fav"], fill=AMBER, size=11))
    sizes = [180, 128, 96, 72, 56, 40]
    labels_px = ["512", "180", "64", "48", "32", "16"]
    x = M + 900
    for i, s in enumerate(sizes):
        o.append(circ(x + s / 2, 640, s / 2, fill=INK))
        o.append(mono_logo(x + s / 2 - s * 0.30, 640 - s * 0.21, s * 0.60, "dark"))
        o.append(t(x + s / 2, 640 + s / 2 + 28, labels_px[i], size=12, fill=GREY, anchor="middle"))
        x += s + 34
    o.append(line(M, 920, W - M, 920, stroke=INK, sw=0.7, op=0.16))
    o.append(foot(L["id_mono_foot"], y=964))
    return page("".join(o))

# ---------------------------------------------------------------- 22 divider
def p22(L):
    s = L["sections"][2]
    return divider(L, 22, s[0], s[1], s[2])

# ---------------------------------------------------------------- 23 palette
def p23(L):
    o = head(L, S3 % L["sections"][2][1], 23, L["col_eyebrow"], L["col_title"], L["col_lead"])
    cw = (W - 2 * M - 4 * 22) / 5.0
    for i, p in enumerate(PAL[:5]):
        x = M + i * (cw + 22)
        o.append(rect(x, 430, cw, 250, p[2]))
        o.append(rect(x, 430, cw, 250, "none", stroke=INK, sw=0.8, op=0.3))
        o.append(t(x, 726, _pname(p, L).upper(), size=19, f=DIS, fill=TXT, ls=1.5))
        r, g, b = _rgb(p[2]); c, m, y_, k = _cmyk(p[2])
        o.append(para(x, 762, [p[2].upper(), "RGB %d %d %d" % (r, g, b),
                               "CMYK %d %d %d %d" % (c, m, y_, k)], size=12.5, lh=21, fill=GREY))
    o.append(line(M, 860, W - M, 860, stroke=INK, sw=0.7, op=0.16))
    for i, p in enumerate(PAL[5:]):
        x = M + i * 420
        o.append(rect(x, 900, 40, 40, p[2], rx=20, stroke=INK, sw=0.7))
        o.append(t(x + 56, 918, _pname(p, L), size=16, fill=TXT, op=0.9))
        o.append(t(x + 56, 940, p[2].upper(), size=12, fill=GREY))
    return page("".join(o))

# ---------------------------------------------------------------- 24 proportion
def p24(L):
    o = head(L, S3 % L["sections"][2][1], 24, L["col_prop_eyebrow"], L["col_prop_title"], L["col_prop_lead"])
    cols = [GROUND, INK, PAPER, GOLD, NAVY]
    bx, bw = M, W - 2 * M
    props = [0.60, 0.22, 0.10, 0.05, 0.03]
    cx = bx
    for i, p in enumerate(props):
        o.append(rect(cx, 440, bw * p - 5, 90, cols[i], stroke=INK, sw=0.6))
        cx += bw * p
    for i, (pc, nm, use) in enumerate(L["col_prop"]):
        y = 600 + i * 76
        o.append(t(M, y, pc, size=26, f=DIS, fill=AMBER, ls=1.5))
        o.append(t(M + 130, y, nm.upper(), size=20, f=DIS, fill=TXT, ls=1.5))
        o.append(t(M + 520, y, use, size=16, fill=GREY))
        o.append(line(M, y + 24, W - M, y + 24, stroke=INK, sw=0.7, op=0.12))
    o.append(label(M, 990, L["col_comb_h"], fill=AMBER, size=11))
    combos = [(GROUND, INK), (INK, PAPER), (PAPER, INK), (NAVY, GOLD), (GROUND, AMBER)]
    for i, (bg, fg) in enumerate(combos):
        x = M + 300 + i * 240
        o.append(rect(x, 954, 210, 56, bg, stroke=INK, sw=0.6))
        o.append(t(x + 105, 990, "Aa", size=26, f=DIS, fill=fg, anchor="middle", ls=2))
    return page("".join(o))

# ---------------------------------------------------------------- 25 contrast
def p25(L):
    o = head(L, S3 % L["sections"][2][1], 25, L["col_acc_eyebrow"], L["col_acc_title"], L["col_acc_lead"])
    keys = [PAL[0], PAL[1], PAL[2], PAL[3], PAL[4], PAL[5], PAL[7]]
    n = len(keys)
    x0, y0, cell = M + 250, 500, 92
    for j, kb in enumerate(keys):
        o.append(t(x0 + j * cell + cell / 2, y0 - 26, _pname(kb, L).split()[0], size=11,
                   fill=GREY, anchor="middle"))
    for i, ka in enumerate(keys):
        y = y0 + i * 58
        o.append(t(x0 - 24, y + 22, _pname(ka, L), size=12, fill=TXT, anchor="end"))
        for j, kb in enumerate(keys):
            x = x0 + j * cell
            v = _ratio(ka[2], kb[2])
            ok = v >= 4.5
            mid = 3.0 <= v < 4.5
            o.append(rect(x, y, cell - 6, 44, kb[2], stroke=INK, sw=0.5))
            o.append(t(x + (cell - 6) / 2, y + 28, "%.1f" % v, size=13, fill=ka[2], anchor="middle"))
            if not ok:
                o.append(line(x, y + 44, x + cell - 6, y + 44, stroke=(AMBER if mid else CLAY), sw=2.4))
    o.append(rect(M, 950, 26, 6, CLAY))
    o.append(t(M + 40, 958, L["col_acc_no"], size=13, fill=GREY))
    o.append(rect(M + 300, 950, 26, 6, AMBER))
    o.append(t(M + 340, 958, "AA-lg (3.0 — 4.5)", size=13, fill=GREY))
    o.append(foot(L["col_acc_warn"], y=1000))
    return page("".join(o))

# ---------------------------------------------------------------- 26 divider
def p26(L):
    s = L["sections"][3]
    return divider(L, 26, s[0], s[1], s[2])

# ---------------------------------------------------------------- 27 families
def p27(L):
    o = head(L, S4 % L["sections"][3][1], 27, L["typ_eyebrow"], L["typ_title"])
    o.append(line(W / 2, 400, W / 2, 900, stroke=INK, sw=0.7, op=0.16))
    o.append(t(M, 620, "Aa", size=230, f=DIS, w=400, fill=TXT))
    o.append(t(M + 340, 500, "CINZEL", size=30, f=DIS, w=400, fill=AMBER, ls=4))
    o.append(t(M + 340, 540, "DISPLAY", size=30, f=DIS, w=400, fill=AMBER, ls=4))
    o.append(t(M + 340, 590, L["typ_cinzel_role"], size=16, fill=TXT, op=0.85))
    o.append(para(M + 340, 630, L["typ_cinzel_body"], size=14.5, lh=25, fill=GREY))
    o.append(t(M, 700, "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", size=23, f=DIS, fill=TXT, op=0.85))
    o.append(t(M, 742, "0123456789  ·  &  ·  +2 / +4", size=20, f=DIS, fill=GREY))
    o.append(t(M, 820, "EL CIELO ES EL LÍMITE" if L["lang"] == "ES" else "THE SKY IS THE LIMIT",
               size=34, f=DIS, fill=TXT, ls=3))
    x2 = W / 2 + 70
    o.append(t(x2, 620, "Aa", size=200, f=SAN, w=300, fill=TXT))
    o.append(t(x2 + 300, 500, "Montserrat", size=30, f=SAN, w=700, fill=AMBER, ls=-0.5))
    o.append(t(x2 + 300, 546, L["typ_mont_role"], size=16, fill=TXT, op=0.85))
    o.append(para(x2 + 300, 586, L["typ_mont_body"], size=14.5, lh=25, fill=GREY))
    o.append(t(x2, 700, "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", size=19, f=SAN, fill=TXT, op=0.85))
    o.append(t(x2, 742, "abcdefghijklmnñopqrstuvwxyz 0123456789", size=19, f=SAN, fill=GREY))
    o.append(para(x2, 812, ["Light 300  ·  Regular 400", "Medium 500  ·  SemiBold 600"],
                  size=20, lh=32, fill=TXT, op=0.85))
    return page("".join(o))

# ---------------------------------------------------------------- 28 scale
def p28(L):
    o = head(L, S4 % L["sections"][3][1], 28, L["typ_scale_eyebrow"], L["typ_scale_title"])
    o.append(line(M, 400, W - M, 400, stroke=INK, sw=0.7, op=0.18))
    sizes = [(38, DIS, 4), (30, DIS, 2.5), (22, DIS, 2), (13, SAN, 3.4), (17, SAN, 0), (13, SAN, 0.5)]
    for i, (nm, spec, sample) in enumerate(L["typ_scale_rows"]):
        y = 470 + i * 88
        sz, f, ls = sizes[i]
        o.append(t(M, y, nm, size=13, fill=AMBER, w=600, ls=1.5))
        o.append(t(M + 190, y, spec, size=13, fill=GREY))
        o.append(t(M + 720, y + 6, sample, size=sz, f=f, fill=TXT, ls=ls,
                   w=(600 if nm in ("Etiqueta", "Label") else 400)))
        o.append(line(M, y + 30, W - M, y + 30, stroke=INK, sw=0.7, op=0.1))
    o.append(foot(L["typ_scale_foot"], y=1010))
    return page("".join(o))

# ---------------------------------------------------------------- 29 divider
def p29(L):
    s = L["sections"][4]
    return divider(L, 29, s[0], s[1], s[2])

# ---------------------------------------------------------------- 30 the veil
def p30(L):
    o = head(L, S5 % L["sections"][4][1], 30, L["veil_eyebrow"], L["veil_title"])
    o.append(rect(M, 390, W - 2 * M, 300, PAPER, op=0.45))
    o.append(veil(M + 60, 448, W - 2 * M - 120, 190, n=11, stroke=INK, sw=1.5, op=0.55, spread=1.1))
    o.append(star(W - M - 120, 470, 15))
    o.append(label(M + 60, 658, L["veil_caption"], fill=GREY, size=10))
    cw = (W - 2 * M) / 4.0
    for i, (h, read) in enumerate(L["veil_reads"]):
        x = M + i * cw
        o.append(rect(x, 730, cw - 24, 150, GROUND, stroke=INK, sw=0.7))
        o.append(veil(x + 20, 764, cw - 64, 82, n=6, stroke=GOLD, sw=1.2, op=0.8, spread=0.9))
        o.append(t(x, 916, h.upper(), size=17, f=DIS, fill=TXT, ls=1.5))
        o.append(t(x, 944, read, size=14, fill=GREY))
    o.append(foot(L["veil_foot"], y=1006))
    return page("".join(o))

# ---------------------------------------------------------------- 31 textures
def p31(L):
    o = head(L, S5 % L["sections"][4][1], 31, L["tex_eyebrow"], L["tex_title"])
    files = ["hormigon", "hormigon_azul", "arido", "basalto", "mineral", "piedra"]
    cw = (W - 2 * M - 5 * 18) / 6.0
    for i, (h, sub) in enumerate(L["tex"]):
        x = M + i * (cw + 18)
        o.append(img("tex_%s.b64" % files[i], x, 420, cw, 260))
        o.append(rect(x, 420, cw, 260, "none", stroke=INK, sw=0.7, op=0.2))
        o.append(t(x, 726, h.upper(), size=17, f=DIS, fill=TXT, ls=1.5))
        o.append(para(x, 762, [sub], size=13.5, lh=22, fill=GREY))
    o.append(line(M, 880, W - M, 880, stroke=INK, sw=0.7, op=0.16))
    o.append(foot(L["tex_foot"], y=926))
    return page("".join(o))

# ---------------------------------------------------------------- 32 image direction
def p32(L):
    o = head(L, S5 % L["sections"][4][1], 32, L["img_eyebrow"], L["img_title"], L["img_lead"])
    o.append(img("ref_plane.b64", M, 440, 700, 470))
    o.append(rect(M, 440, 700, 470, "none", stroke=INK, sw=0.7, op=0.2))
    o.append(label(M, 944, L["img_caps"][0], fill=GREY, size=10))
    iw, ih = 232, 206
    for i, g in enumerate(["ref_umbral.b64", "ref_materia.b64", "ref_aire.b64", "ref_contraluz.b64"]):
        x = M + 730 + (i % 2) * (iw + 20)
        y = 440 + (i // 2) * (ih + 48)
        o.append(img(g, x, y, iw, ih))
        o.append(rect(x, y, iw, ih, "none", stroke=INK, sw=0.7, op=0.2))
        o.append(label(x, y + ih + 26, L["img_caps"][i + 1], fill=GREY, size=9))
    px = M + 730 + 2 * (iw + 20) + 30
    for i, (h, sub) in enumerate(L["img_princ"]):
        y = 470 + i * 92
        o.append(t(px, y, "0%d" % (i + 1), size=11, w=600, fill=AMBER, ls=2))
        o.append(t(px + 46, y, h.upper(), size=19, f=DIS, fill=TXT, ls=1.5))
        o.append(t(px + 46, y + 28, sub, size=13.5, fill=GREY))
    o.append(para(px, 856, L["img_note"], size=13.5, lh=22, fill=GREY))
    o.append(line(M, 946, W - M, 946, stroke=INK, sw=0.7, op=0.16))
    o.append(label(M, 984, L["img_no_h"], fill=CLAY, size=11))
    o.append(t(M + 150, 988, L["img_no"][0].rstrip(".") + "  ·  " + L["img_no"][1].rstrip("."),
               size=14, fill=GREY))
    return page("".join(o))

# ---------------------------------------------------------------- 33 divider
def p33(L):
    s = L["sections"][5]
    return divider(L, 33, s[0], s[1], s[2])

# ---------------------------------------------------------------- 34 stationery
def p34(L):
    o = head(L, S6 % L["sections"][5][1], 34, L["sta_eyebrow"], L["sta_title"])
    cw, ch = 500, 290
    x, y = M, 400
    o.append(rect(x + 8, y + 10, cw, ch, INK, op=0.14, rx=6))
    o.append(rect(x, y, cw, ch, INK, rx=6))
    o.append(full_logo(x + 90, y + 92, 320, "dark"))
    x2 = x + cw + 60
    o.append(rect(x2 + 8, y + 10, cw, ch, INK, op=0.14, rx=6))
    o.append(rect(x2, y, cw, ch, GROUND, rx=6, stroke=INK, sw=0.7))
    o.append(mono_logo(x2 + 48, y + 96, 120, "light"))
    o.append(line(x2 + 200, y + 92, x2 + 200, y + 200, stroke=INK, sw=0.8, op=0.35))
    o.append(t(x2 + 230, y + 126, "NOMBRE APELLIDO" if L["lang"] == "ES" else "NAME SURNAME",
               size=18, f=DIS, w=400, fill=TXT, ls=2))
    o.append(label(x2 + 230, y + 152, "Cargo" if L["lang"] == "ES" else "Role", fill=AMBER, size=9))
    o.append(para(x2 + 230, y + 190, ["+53 000 000 000", "nombre@velum.com"], size=13, lh=22, fill=GREY))
    o.append(label(x, y + ch + 44, L["sta_caps"][0], fill=GREY, size=10, w=500))
    lx, ly, lw, lh = M + 1130, 400, 250, 354
    o.append(rect(lx + 6, ly + 8, lw, lh, INK, op=0.12))
    o.append(rect(lx, ly, lw, lh, "#FFFFFF", stroke=INK, sw=0.6))
    o.append(full_logo(lx + 26, ly + 26, 110, "light"))
    for i in range(9):
        o.append(rect(lx + 26, ly + 120 + i * 17, (lw - 52) * (1 if i % 4 else 0.62), 4, INK, op=0.16))
    o.append(rect(lx, ly + lh - 16, lw, 16, INK))
    o.append(label(lx, ly + lh + 44, L["sta_caps"][1], fill=GREY, size=10, w=500))
    ex, ey, ew, eh = lx + lw + 40, 400, 260, 180
    o.append(rect(ex + 6, ey + 8, ew, eh, INK, op=0.12))
    o.append(rect(ex, ey, ew, eh, INK))
    o.append('<path d="M %d %d L %d %d L %d %d" fill="none" stroke="%s" stroke-width="0.8" opacity="0.35"/>'
             % (ex, ey, ex + ew / 2, ey + eh * 0.55, ex + ew, ey, PEARL))
    o.append(mono_logo(ex + 22, ey + eh - 62, 78, "dark"))
    o.append(label(ex, ey + eh + 44, L["sta_caps"][2], fill=GREY, size=10, w=500))
    o.append(rect(ex, 640, ew, 114, PAPER))
    o.append(veil(ex, 656, ew, 84, n=6, stroke=INK, sw=1, op=0.28))
    o.append(full_logo(ex + 66, 674, 128, "navy"))
    o.append(label(ex, 798, L["sta_caps"][3], fill=GREY, size=10, w=500))
    o.append(line(M, 850, W - M, 850, stroke=INK, sw=0.7, op=0.16))
    o.append(foot(L["sta_foot"], y=900, size=16))
    return page("".join(o))

# ---------------------------------------------------------------- 35 digital
def p35(L):
    o = head(L, S6 % L["sections"][5][1], 35, L["dig_eyebrow"], L["dig_title"])
    bx, by, bw, bh = M, 400, 1100, 540
    o.append(rect(bx, by, bw, bh, GROUND, rx=8, stroke=INK, sw=0.7))
    o.append(rect(bx, by, bw, 40, PAPER, rx=8))
    o.append(rect(bx, by + 26, bw, 14, PAPER))
    for i, c in enumerate([CLAY, GOLD, PEARL]):
        o.append(circ(bx + 24 + i * 20, by + 20, 5, fill=c))
    o.append(rect(bx + 110, by + 10, 320, 20, GROUND, rx=10, stroke=INK, sw=0.5))
    o.append(t(bx + 128, by + 25, "velum.com", size=11, fill=GREY))
    o.append(veil(bx, by + 120, bw, 360, n=12, stroke=INK, sw=1.1, op=0.12, spread=1.2))
    o.append(full_logo(bx + 40, by + 74, 150, "light"))
    for i, n in enumerate(L["dig_nav"]):
        o.append(label(bx + 560 + i * 130, by + 106, n, fill=GREY, size=10))
    o.append(t(bx + 60, by + 290, L["origin_h1"], size=56, f=DIS, fill=TXT, ls=3))
    o.append(t(bx + 60, by + 352, L["origin_h2"], size=56, f=DIS, fill=TXT, ls=3))
    o.append(rect(bx + 60, by + 396, 210, 46, INK))
    o.append(label(bx + 88, by + 425, L["dig_cta"], fill=GROUND, size=10))
    o.append(label(bx, by + bh + 44, L["dig_caps"][0], fill=GREY, size=10, w=500))
    sx = bx + bw + 60
    o.append(circ(sx + 60, 460, 60, fill=INK, stroke=GOLD, sw=1))
    o.append(mono_logo(sx + 16, 432, 88, "dark"))
    o.append(t(sx + 150, 448, "@velum", size=26, f=DIS, fill=TXT, ls=2))
    o.append(para(sx + 150, 482, L["dig_bio"], size=14, lh=22, fill=GREY))
    tw = 160
    for i in range(3):
        for j in range(2):
            x = sx + i * (tw + 12); y = 560 + j * (tw + 12)
            k = (i + j) % 3
            if k == 0:
                o.append(img("grad4.b64", x, y, tw, tw))
                o.append(rect(x, y, tw, tw, INK, op=0.35))
                o.append(mono_logo(x + tw / 2 - 34, y + tw / 2 - 24, 68, "dark"))
            elif k == 1:
                o.append(rect(x, y, tw, tw, GROUND, stroke=INK, sw=0.7))
                words = L["close_tag"].rstrip(".").split()
                o.append(t(x + 18, y + 70, " ".join(words[:2]), size=17, f=DIS, fill=TXT, ls=1.5))
                o.append(t(x + 18, y + 96, " ".join(words[2:]) + ".", size=17, f=DIS, fill=TXT, ls=1.5))
                o.append(star(x + tw - 30, y + 30, 10))
            else:
                o.append(rect(x, y, tw, tw, PAPER))
                o.append(veil(x, y + 40, tw, 80, n=7, stroke=INK, sw=1, op=0.35))
    o.append(label(sx, 920, L["dig_caps"][1], fill=GREY, size=10, w=500))
    return page("".join(o))

# ---------------------------------------------------------------- 36 close
def p36(L):
    o = [rect(0, 0, W, H, GROUND)]
    o.append(veil(0, 260, W, 620, n=16, stroke=INK, sw=1.1, op=0.10, spread=1.3))
    o.append(rect(56, 56, W - 112, H - 112, "none", stroke=INK, sw=0.8, op=0.16))
    o.append(mono_logo(W / 2 - 120, 300, 240, "light"))
    o.append(t(W / 2, 646, L["close_tag"], size=64, f=DIS, fill=TXT, anchor="middle", ls=4))
    o.append(line(W / 2 - 46, 706, W / 2 + 46, 706, stroke=GOLD, sw=1.2))
    o.append(t(W / 2, 774, L["close_pillars"], size=17, fill=GREY, anchor="middle", ls=2))
    o.append(label(130, 1000, L["close_foot"], fill=GREY, size=10, w=500))
    o.append(label(W - 130, 1000, "%d / %d" % (L["total"], L["total"]), fill=GREY,
                   size=10, anchor="end", w=500))
    return page("".join(o), bg=GROUND)
