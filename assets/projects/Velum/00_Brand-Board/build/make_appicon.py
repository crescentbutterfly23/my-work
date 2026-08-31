# -*- coding: utf-8 -*-
"""VELUM — app icon: the monogram on a solid Azul Velum tile, so it survives any browser theme."""
import os, re, subprocess, urllib.parse
from PIL import Image

B = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(B + "/../..")
SRC = os.path.abspath(KIT + "/..")
FAV = KIT + "/01_Logo/Favicon"
TMP = B + "/tmp"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
os.makedirs(FAV, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

INK, GOLD, IVORY, PEARL = "#0B1D34", "#D4AF37", "#F7F7F7", "#DADDE3"

def frag(path):
    t = open(path, encoding="utf-8").read()
    m = re.search(r'<g id="Layer_1-2"[^>]*>(.*)</g>\s*</svg>', t, re.S)
    return m.group(1).strip()

MONO = frag(SRC + "/Logos/Monogram - dark.svg")   # cls-1 V, cls-2 star, cls-3 sweep

def colour(f, mp):
    for k, v in mp.items():
        f = f.replace('class="%s"' % k, 'fill="%s"' % v)
    return f

def icon_svg(radius=0.18):
    """512-unit tile, monogram centred at 62% width."""
    S = 512
    g = colour(MONO, {"cls-1": PEARL, "cls-2": GOLD, "cls-3": IVORY})
    w = S * 0.62
    sc = w / 56.34
    h = 38.64 * sc
    x = (S - w) / 2.0
    y = (S - h) / 2.0
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
            '<rect width="%d" height="%d" rx="%.1f" fill="%s"/>'
            '<g transform="translate(%.2f %.2f) scale(%.5f)">%s</g></svg>'
            % (S, S, S, S, S, S, S * radius, INK, x, y, sc, g))

def render(svg_path, out_png, size):
    name = os.path.basename(svg_path)
    html = ('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;padding:0;'
            'background:transparent;width:%dpx;height:%dpx;overflow:hidden}'
            'img{display:block;width:%dpx;height:%dpx}</style><img src="%s">'
            % (size, size, size, size, urllib.parse.quote(name)))
    h = TMP + "/i.html"
    open(h, "w", encoding="utf-8").write(html)
    if os.path.exists(out_png):
        os.remove(out_png)
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--default-background-color=00000000", "--force-device-scale-factor=1",
                    "--window-size=%d,%d" % (size, size), "--screenshot=" + out_png,
                    "file:///" + h.replace("\\", "/")], capture_output=True, timeout=120)

if __name__ == "__main__":
    p = TMP + "/velum-app-icon.svg"
    open(p, "w", encoding="utf-8").write(icon_svg())
    open(FAV + "/velum-app-icon.svg", "w", encoding="utf-8").write(icon_svg())
    for s in (512, 192, 180, 64, 48, 32, 16):
        render(p, FAV + "/favicon-app-%dx%d.png" % (s, s), s)
        print("favicon-app-%dx%d.png" % (s, s))
    ims = [Image.open(FAV + "/favicon-app-%dx%d.png" % (s, s)).convert("RGBA") for s in (16, 32, 48, 64)]
    ims[-1].save(FAV + "/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("favicon.ico rebuilt from the app icon")
