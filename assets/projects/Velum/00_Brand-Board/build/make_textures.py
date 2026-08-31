# -*- coding: utf-8 -*-
"""VELUM — generate the brand's texture backgrounds.

Celestial by suggestion, never by decoration: sky, horizon, trajectory, veil, grain.
No planets, no rockets, no galaxies.
"""
import os, math
import numpy as np
from PIL import Image, ImageFilter

B = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(B + "/../..")
OUT = KIT + "/05_Textures"
os.makedirs(OUT, exist_ok=True)

W, H = 2400, 1350
GROUND = (244, 240, 238)   # #F4F0EE
INK    = (11, 29, 52)      # #0B1D34
NAVY   = (32, 52, 77)      # #20344D
GOLD   = (212, 175, 55)    # #D4AF37
CREAM  = (232, 220, 192)   # #E8DCC0
PEARL  = (218, 221, 227)   # #DADDE3

rng = np.random.default_rng(7)

def _save(arr, name, q=90):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    p = OUT + "/" + name
    if name.endswith(".png"):
        im.save(p)
    else:
        im.save(p, quality=q)
    print(name, im.size, os.path.getsize(p) // 1024, "KB")

def _smooth_noise(w, h, scale, octaves=4):
    """Fractal value noise in [0,1]."""
    out = np.zeros((h, w), dtype=np.float32)
    amp, total = 1.0, 0.0
    for o in range(octaves):
        s = max(2, int(scale / (2 ** o)))
        small = rng.random((max(2, h // s), max(2, w // s))).astype(np.float32)
        up = np.array(Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC),
                      dtype=np.float32) / 255.0
        out += up * amp
        total += amp
        amp *= 0.5
    return out / total

def _mix(c1, c2, t):
    """t is an (h,w) array in [0,1]."""
    c1 = np.array(c1, dtype=np.float32)
    c2 = np.array(c2, dtype=np.float32)
    return c1[None, None, :] * (1 - t[..., None]) + c2[None, None, :] * t[..., None]

# ---------------------------------------------------------------- 1. paper grain
def grain_hueso():
    n = rng.normal(0, 1, (H, W)).astype(np.float32)
    n = np.array(Image.fromarray(((n - n.min()) / np.ptp(n) * 255).astype(np.uint8))
                 .filter(ImageFilter.GaussianBlur(0.6)), dtype=np.float32) / 255.0
    fib = _smooth_noise(W, H, 220, 3)
    t = 0.55 * n + 0.45 * fib
    base = np.array(GROUND, dtype=np.float32)[None, None, :]
    arr = base + (t[..., None] - 0.5) * 15.0
    _save(arr, "velum-grano-hueso.jpg")

# ---------------------------------------------------------------- 2. limewash / plaster
def yeso_hueso():
    n = _smooth_noise(W, H, 380, 5)
    n2 = _smooth_noise(W, H, 90, 3)
    t = np.clip(0.7 * n + 0.3 * n2, 0, 1)
    arr = _mix(GROUND, (228, 222, 216), t ** 1.4)
    arr += (rng.normal(0, 1, (H, W, 1)) * 2.2)
    _save(arr, "velum-yeso-hueso.jpg")

# ---------------------------------------------------------------- 3. marble veining
def marmol_hueso():
    x = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    warp = _smooth_noise(W, H, 300, 4)
    v = np.sin((x * 2.6 + y * 1.1 + warp * 1.5) * math.pi)
    vein = np.exp(-((v) ** 2) * 14.0)
    fine = np.exp(-((np.sin((x * 7.0 + y * 0.6 + warp * 2.2) * math.pi)) ** 2) * 42.0) * 0.30
    t = np.clip(vein + fine, 0, 1)
    arr = _mix(GROUND, (222, 216, 210), t * 0.62)
    arr = arr + (_smooth_noise(W, H, 700, 3)[..., None] - 0.5) * 6
    _save(arr, "velum-marmol-hueso.jpg")

# ---------------------------------------------------------------- 4. night sky, very restrained
def cielo_nocturno():
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    x = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    grad = np.clip(0.15 + 0.85 * (1 - y) ** 1.6 + 0.10 * np.sin(x * math.pi), 0, 1)
    arr = _mix(INK, NAVY, grad * 0.55)
    cloud = _smooth_noise(W, H, 520, 4)
    arr = arr + ((cloud - 0.5)[..., None] * np.array([10, 14, 20], dtype=np.float32)[None, None, :])
    # sparse stars, small and dim
    stars = np.zeros((H, W), dtype=np.float32)
    n = 1500
    xs = rng.integers(0, W, n); ys = rng.integers(0, H, n)
    mag = rng.random(n) ** 2.0
    for i in range(n):
        stars[ys[i], xs[i]] = mag[i]
    stars = np.array(Image.fromarray((stars * 255).astype(np.uint8))
                     .filter(ImageFilter.GaussianBlur(0.8)), dtype=np.float32) / 255.0
    glow = np.zeros((H, W), dtype=np.float32)
    for i in range(0, n, 40):
        glow[ys[i], xs[i]] = 1.0
    glow = np.array(Image.fromarray((glow * 255).astype(np.uint8))
                    .filter(ImageFilter.GaussianBlur(4.0)), dtype=np.float32) / 255.0
    arr = arr + stars[..., None] * np.array(PEARL, dtype=np.float32)[None, None, :] * 2.6
    arr = arr + glow[..., None] * np.array(GOLD, dtype=np.float32)[None, None, :] * 0.9
    # one gold star, the brand's own
    _save(arr, "velum-cielo-nocturno.jpg")

# ---------------------------------------------------------------- 5. horizon bands
def horizonte(name, top, bottom, accent=None, pos=0.62):
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    t = np.clip((y - 0.05) / 0.9, 0, 1) ** 1.25
    t = np.repeat(t, W, axis=1)
    arr = _mix(top, bottom, t)
    if accent:
        band = np.exp(-((y - pos) ** 2) / (2 * 0.012 ** 2))
        band = np.repeat(band, W, axis=1)
        arr = arr + band[..., None] * (np.array(accent, dtype=np.float32)[None, None, :] * 0.55)
    arr = arr + (_smooth_noise(W, H, 600, 3)[..., None] - 0.5) * 5
    _save(arr, name)

# ---------------------------------------------------------------- 6. veil lines (vector)
def veil_svg(name, w=2400, h=1350, bg=None, stroke="#0B1D34", op=0.16, n=26, sw=1.6, spread=1.0):
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (w, h, w, h)]
    if bg:
        o.append('<rect width="%d" height="%d" fill="%s"/>' % (w, h, bg))
    o.append('<g fill="none" stroke="%s" stroke-width="%.2f" opacity="%.2f" stroke-linecap="round">'
             % (stroke, sw, op))
    for i in range(n):
        f = i / float(n - 1)
        yy = h * (0.10 + 0.80 * f)
        amp = h * 0.16 * spread * (0.5 + 0.5 * math.sin(f * math.pi))
        o.append('<path d="M 0 %.1f C %.1f %.1f %.1f %.1f %.1f %.1f S %.1f %.1f %.1f %.1f"/>' % (
            yy,
            w * 0.22, yy - amp,
            w * 0.42, yy + amp * 0.55,
            w * 0.60, yy - amp * 0.12,
            w * 0.86, yy - amp * 0.95,
            w, yy - amp * 0.62))
    o.append("</g></svg>")
    p = OUT + "/" + name
    open(p, "w", encoding="utf-8").write("".join(o))
    print(name, os.path.getsize(p) // 1024, "KB")

# ---------------------------------------------------------------- 7. orbits (vector)
def orbits_svg(name, w=2400, h=1350, bg=None, stroke="#0B1D34", op=0.18):
    cx, cy = w * 0.28, h * 1.02
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (w, h, w, h)]
    if bg:
        o.append('<rect width="%d" height="%d" fill="%s"/>' % (w, h, bg))
    o.append('<g fill="none" stroke="%s" stroke-width="1.4" opacity="%.2f">' % (stroke, op))
    for i in range(14):
        r = h * (0.22 + i * 0.115)
        o.append('<circle cx="%.1f" cy="%.1f" r="%.1f"/>' % (cx, cy, r))
    o.append("</g>")
    o.append('<g fill="none" stroke="%s" stroke-width="1.1" opacity="%.2f" stroke-dasharray="7 11">'
             % (stroke, op * 0.8))
    for i in range(5):
        rr = h * (0.55 + i * 0.28)
        o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(-16 %.1f %.1f)"/>'
                 % (cx, cy, rr, rr * 0.42, cx, cy))
    o.append("</g></svg>")
    p = OUT + "/" + name
    open(p, "w", encoding="utf-8").write("".join(o))
    print(name, os.path.getsize(p) // 1024, "KB")

# ---------------------------------------------------------------- 8. halftone fade
def halftone(name, bg, dot, gap=16, r_max=5.2):
    w, h = 2400, 1350
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (w, h, w, h),
         '<rect width="%d" height="%d" fill="%s"/>' % (w, h, bg), '<g fill="%s">' % dot]
    for j in range(int(h / gap) + 1):
        for i in range(int(w / gap) + 1):
            x, y = i * gap, j * gap
            f = 1.0 - (y / float(h)) * 0.92 - (x / float(w)) * 0.10
            f = max(0.0, min(1.0, f))
            r = r_max * (f ** 2.1)
            if r > 0.25:
                o.append('<circle cx="%d" cy="%d" r="%.2f"/>' % (x, y, r))
    o.append("</g></svg>")
    p = OUT + "/" + name
    open(p, "w", encoding="utf-8").write("".join(o))
    print(name, os.path.getsize(p) // 1024, "KB")

if __name__ == "__main__":
    grain_hueso()
    yeso_hueso()
    marmol_hueso()
    cielo_nocturno()
    horizonte("velum-horizonte-azul.jpg", INK, NAVY, GOLD, 0.66)
    horizonte("velum-horizonte-hueso.jpg", GROUND, CREAM, GOLD, 0.72)
    horizonte("velum-degradado-hueso-azul.jpg", GROUND, INK, None)
    veil_svg("velum-velo-hueso.svg", bg="#F4F0EE", stroke="#0B1D34", op=0.14)
    veil_svg("velum-velo-azul.svg", bg="#0B1D34", stroke="#D4AF37", op=0.30, n=22, spread=1.1)
    veil_svg("velum-velo-oro.svg", bg=None, stroke="#D4AF37", op=0.55, n=14, sw=1.9)
    orbits_svg("velum-orbitas-hueso.svg", bg="#F4F0EE", stroke="#0B1D34", op=0.16)
    orbits_svg("velum-orbitas-azul.svg", bg="#0B1D34", stroke="#D4AF37", op=0.22)
    halftone("velum-halftone-hueso.svg", "#F4F0EE", "#0B1D34")
    halftone("velum-halftone-azul.svg", "#0B1D34", "#DADDE3")
