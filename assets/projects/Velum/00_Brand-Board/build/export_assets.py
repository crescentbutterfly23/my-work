# -*- coding: utf-8 -*-
"""VELUM kit — export logo PNGs (transparent), favicons, and the graphic elements as SVG."""
import os, re, sys, subprocess, urllib.parse, shutil

B = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(B + "/../..")
SRC = os.path.abspath(KIT + "/..")          # Vellum Brand/
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
TMP = B + "/tmp"
os.makedirs(TMP, exist_ok=True)

INK, NAVY, GOLD, CREAM, PEARL, IVORY, BLACK, GREY = (
    "#0B1D34", "#20344D", "#D4AF37", "#E8DCC0", "#DADDE3", "#F7F7F7", "#1A1A1A", "#55585F")

# ---------------------------------------------------------------- source art
def frag(path):
    t = open(path, encoding="utf-8").read()
    m = re.search(r'<g id="Layer_1-2"[^>]*>(.*)</g>\s*</svg>', t, re.S)
    return m.group(1).strip()

FULL = frag(SRC + "/Logos/Full logo - dark.svg")     # cls-1 gold, cls-2 word+sweep, cls-3 V
MONO = frag(SRC + "/Logos/Monogram - dark.svg")      # cls-1 V, cls-2 star, cls-3 sweep

def color(f, mp):
    for k, v in mp.items():
        f = f.replace('class="%s"' % k, 'fill="%s"' % v)
    return f

def svg(vb, f):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s">%s</svg>' % (vb, f)

FVB, MVB = "0 0 141.57 63.16", "0 0 56.34 38.64"
VARIANTS = {
    # name: (viewBox, fragment, mapping)
    "velum-primary-dark-bg":  (FVB, FULL, {"cls-1": GOLD,  "cls-2": IVORY, "cls-3": PEARL}),
    "velum-primary-light-bg": (FVB, FULL, {"cls-1": GOLD,  "cls-2": BLACK, "cls-3": INK}),
    "velum-primary-blanco":   (FVB, FULL, {"cls-1": IVORY, "cls-2": IVORY, "cls-3": IVORY}),
    "velum-primary-azul":     (FVB, FULL, {"cls-1": INK,   "cls-2": INK,   "cls-3": INK}),
    "velum-primary-oro":      (FVB, FULL, {"cls-1": GOLD,  "cls-2": GOLD,  "cls-3": GOLD}),
    "velum-primary-negro":    (FVB, FULL, {"cls-1": BLACK, "cls-2": BLACK, "cls-3": BLACK}),
    "velum-primary-crema":    (FVB, FULL, {"cls-1": CREAM, "cls-2": CREAM, "cls-3": CREAM}),
    "velum-monogram-dark-bg": (MVB, MONO, {"cls-1": PEARL, "cls-2": GOLD,  "cls-3": IVORY}),
    "velum-monogram-light-bg":(MVB, MONO, {"cls-1": INK,   "cls-2": GOLD,  "cls-3": BLACK}),
    "velum-monogram-blanco":  (MVB, MONO, {"cls-1": IVORY, "cls-2": IVORY, "cls-3": IVORY}),
    "velum-monogram-azul":    (MVB, MONO, {"cls-1": INK,   "cls-2": INK,   "cls-3": INK}),
    "velum-monogram-oro":     (MVB, MONO, {"cls-1": GOLD,  "cls-2": GOLD,  "cls-3": GOLD}),
    "velum-monogram-negro":   (MVB, MONO, {"cls-1": BLACK, "cls-2": BLACK, "cls-3": BLACK}),
    "velum-monogram-crema":   (MVB, MONO, {"cls-1": CREAM, "cls-2": CREAM, "cls-3": CREAM}),
}

# ---------------------------------------------------------------- graphic elements
def star(r=100, fill=GOLD):
    k = r * 0.145
    c = r
    d = ("M %.2f %.2f Q %.2f %.2f %.2f %.2f Q %.2f %.2f %.2f %.2f "
         "Q %.2f %.2f %.2f %.2f Q %.2f %.2f %.2f %.2f Z") % (
        c, c - r, c + k, c - k, c + r, c, c + k, c + k, c, c + r,
        c - k, c + k, c - r, c, c - k, c - k, c, c - r)
    return svg("0 0 %d %d" % (2 * r, 2 * r), '<path d="%s" fill="%s"/>' % (d, fill))

def trazo(w=800, rise=224, stroke=IVORY, sw=6):
    d = "M 0 %.1f C %.1f %.1f %.1f %.1f %.1f 0" % (rise, w * 0.30, rise * 0.30, w * 0.62, rise * 0.03, w)
    return svg("0 0 %d %d" % (w, rise + sw), '<path d="%s" fill="none" stroke="%s" stroke-width="%d" '
               'stroke-linecap="round"/>' % (d, stroke, sw))

ICONS = {
    "viajes": "M6 27 L42 17 M6 27 L18 31 L14 41 L20 33 L34 37 M42 17 L34 37",
    "perfumeria": "M19 6 h10 v7 h-10 z M17 13 h14 c3 6 4 9 4 14 v13 a4 4 0 0 1 -4 4 h-14 a4 4 0 0 1 -4 -4 "
                  "v-13 c0 -5 1 -8 4 -14 z M19 26 h10",
    "alimentos": "M6 39 h36 M10 39 a14 15 0 0 1 28 0 M24 10 v-5 M20.5 5 h7",
    "importacion-exportacion": "M24 6 a18 18 0 1 0 0 36 a18 18 0 1 0 0 -36 M6 24 h36 M24 6 c-8 8 -8 28 0 36 "
                               "M24 6 c8 8 8 28 0 36",
    "inmuebles": "M10 42 v-30 h14 v30 M24 42 v-20 h14 v20 M14 18 h6 M14 26 h6 M14 34 h6 M28 28 h6 M28 36 h6 M6 42 h36",
    "vehiculos-electricos": "M9 30 l4 -9 a4 4 0 0 1 3.6 -2.4 h14.8 a4 4 0 0 1 3.6 2.4 l4 9 M7 30 h34 v7 h-34 z "
                            "M13 37 v3.5 M35 37 v3.5 M15.5 33.5 h4 M28.5 33.5 h4",
}

def icon(d, stroke=GOLD):
    return svg("0 0 48 48", '<path d="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round" '
               'stroke-linejoin="round"/>' % (d, stroke))

def pattern_diag(size=320, stroke=PEARL, gap=16):
    o = ['<clipPath id="c"><rect width="%d" height="%d"/></clipPath><g clip-path="url(#c)" opacity="0.45">' % (size, size)]
    n = int(size * 2 / gap) + 2
    for k in range(-n, n):
        x = k * gap
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6"/>'
                 % (x, -size, x + int(size * 1.4), int(size * 1.6), stroke))
    o.append("</g>")
    return svg("0 0 %d %d" % (size, size), "".join(o))

def pattern_grid(size=320, stroke=PEARL, step=40):
    o = ['<g opacity="0.35">']
    for k in range(0, size + 1, step):
        o.append('<line x1="%d" y1="0" x2="%d" y2="%d" stroke="%s" stroke-width="0.8"/>' % (k, k, size, stroke))
        o.append('<line x1="0" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="0.8"/>' % (k, size, k, stroke))
    o.append("</g>")
    return svg("0 0 %d %d" % (size, size), "".join(o))

# ---------------------------------------------------------------- raster export
def render(svg_path, out_png, w, h, transparent=True):
    name = os.path.basename(svg_path)
    if os.path.abspath(svg_path) != os.path.abspath(TMP + "/" + name):
        shutil.copy(svg_path, TMP + "/" + name)
    html = ('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;padding:0;'
            'background:transparent;width:%dpx;height:%dpx;overflow:hidden}img{display:block;width:%dpx;'
            'height:%dpx}</style><img src="%s">') % (w, h, w, h, urllib.parse.quote(name))
    hp = TMP + "/r.html"
    open(hp, "w", encoding="utf-8").write(html)
    if os.path.exists(out_png):
        os.remove(out_png)
    cmd = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
           "--window-size=%d,%d" % (w, h), "--screenshot=" + out_png, "file:///" + hp.replace("\\", "/")]
    if transparent:
        cmd.insert(4, "--default-background-color=00000000")
    subprocess.run(cmd, capture_output=True, timeout=180)

def main():
    LSVG, LPNG, FAV = KIT + "/01_Logo/SVG", KIT + "/01_Logo/PNG", KIT + "/01_Logo/Favicon"
    ESVG = KIT + "/06_Elements/SVG"
    for d in (LSVG, LPNG, FAV, ESVG):
        os.makedirs(d, exist_ok=True)
    for f in os.listdir(LSVG):
        os.remove(LSVG + "/" + f)

    # logo SVGs + PNGs
    for name, (vb, fr, mp) in VARIANTS.items():
        p = LSVG + "/%s.svg" % name
        open(p, "w", encoding="utf-8").write(svg(vb, color(fr, mp)))
        ar = 63.16 / 141.57 if "primary" in name else 38.64 / 56.34
        widths = (600, 1200, 2400) if "primary" in name else (256, 512, 1024)
        for w in widths:
            render(p, LPNG + "/%s@%dw.png" % (name, w), w, max(1, round(w * ar)))
        print("logo", name)

    # favicons — square canvas, monogram centred with padding
    sq = []
    for tone, mp in (("azul", {"cls-1": INK, "cls-2": INK, "cls-3": INK}),
                     ("blanco", {"cls-1": IVORY, "cls-2": IVORY, "cls-3": IVORY}),
                     ("oro", {"cls-1": GOLD, "cls-2": GOLD, "cls-3": GOLD})):
        inner = '<g transform="translate(4.5 13.35)">%s</g>' % color(MONO, mp)
        p = TMP + "/fav-%s.svg" % tone
        open(p, "w", encoding="utf-8").write(svg("0 0 65.34 65.34", inner))
        sq.append((tone, p))
        for s_ in (16, 32, 48, 64, 180, 512):
            render(p, FAV + "/favicon-%s-%dx%d.png" % (tone, s_, s_), s_, s_)
    from PIL import Image
    ims = [Image.open(FAV + "/favicon-azul-%dx%d.png" % (s_, s_)).convert("RGBA") for s_ in (16, 32, 48, 64)]
    ims[-1].save(FAV + "/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("favicons done")

    # graphic elements
    open(ESVG + "/velum-estrella-oro.svg", "w", encoding="utf-8").write(star(100, GOLD))
    open(ESVG + "/velum-estrella-blanco.svg", "w", encoding="utf-8").write(star(100, IVORY))
    open(ESVG + "/velum-trazo-blanco.svg", "w", encoding="utf-8").write(trazo(stroke=IVORY))
    open(ESVG + "/velum-trazo-oro.svg", "w", encoding="utf-8").write(trazo(stroke=GOLD))
    for n, d in ICONS.items():
        open(ESVG + "/velum-icono-%s.svg" % n, "w", encoding="utf-8").write(icon(d))
    open(ESVG + "/velum-trama-diagonal.svg", "w", encoding="utf-8").write(pattern_diag())
    open(ESVG + "/velum-reticula.svg", "w", encoding="utf-8").write(pattern_grid())
    print("elements done")

if __name__ == "__main__":
    main()
