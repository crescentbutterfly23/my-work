# -*- coding: utf-8 -*-
"""VELUM — stone, concrete and mineral textures.

Hard, unmovable, expansive: the ground under the brand. Outer space read as geology,
not as illustration — basalt fracture, regolith, aggregate, mineral veins in the rock.
Never planets, rockets or galaxies.
"""
import os, math
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

B = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(B + "/../..")
OUT = KIT + "/05_Textures"
os.makedirs(OUT, exist_ok=True)

W, H = 2400, 1350
GROUND = np.array((244, 240, 238), dtype=np.float32)
INK    = np.array((11, 29, 52), dtype=np.float32)
NAVY   = np.array((32, 52, 77), dtype=np.float32)
GOLD   = np.array((212, 175, 55), dtype=np.float32)
PEARL  = np.array((218, 221, 227), dtype=np.float32)

rng = np.random.default_rng(19)

def save(arr, name, q=88):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    p = OUT + "/" + name
    im.save(p, quality=q)
    print(name, im.size, os.path.getsize(p) // 1024, "KB")

def up(a, w=W, h=H):
    return np.array(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC),
                    dtype=np.float32) / 255.0

def fnoise(w, h, scale, octaves=5, seed=None):
    r = rng if seed is None else np.random.default_rng(seed)
    out = np.zeros((h, w), dtype=np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        s = max(2, int(scale / (2 ** o)))
        small = r.random((max(2, h // s), max(2, w // s))).astype(np.float32)
        out += up(small, w, h) * amp
        tot += amp
        amp *= 0.52
    return out / tot

def speckle(w, h, density=0.04, blur=0.6, seed=None):
    r = rng if seed is None else np.random.default_rng(seed)
    m = (r.random((h, w)) < density).astype(np.float32)
    return np.array(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur)),
                    dtype=np.float32) / 255.0

def voronoi(n=180, seed=1, ws=600, hs=338, jitter=1.0):
    """Return (edge, cell) at low res: edge is F2-F1 (0 on a crack), cell is F1."""
    r = np.random.default_rng(seed)
    pts = np.stack([r.random(n) * ws, r.random(n) * hs], axis=1).astype(np.float32)
    pts += r.normal(0, 6 * jitter, pts.shape).astype(np.float32)
    ys, xs = np.mgrid[0:hs, 0:ws].astype(np.float32)
    f1 = np.full((hs, ws), 1e9, dtype=np.float32)
    f2 = np.full((hs, ws), 1e9, dtype=np.float32)
    step = 40
    for i in range(0, n, step):
        chunk = pts[i:i + step]
        d = np.sqrt((xs[..., None] - chunk[:, 0]) ** 2 + (ys[..., None] - chunk[:, 1]) ** 2)
        d.sort(axis=2)
        a = d[:, :, 0]
        b = d[:, :, 1] if d.shape[2] > 1 else d[:, :, 0]
        both = np.stack([f1, f2, a, b], axis=2)
        both.sort(axis=2)
        f1, f2 = both[:, :, 0], both[:, :, 1]
    edge = f2 - f1
    scale = max(1e-6, np.percentile(edge, 98))
    return np.clip(edge / scale, 0, 1), f1 / max(1e-6, f1.max())

def cracks(n=200, seed=1, width=0.055, jitter=1.0):
    """1 on the fracture lines, 0 elsewhere."""
    edge, _ = voronoi(n=n, seed=seed, jitter=jitter)
    c = np.clip(1.0 - edge / width, 0, 1) ** 1.2
    return up(c)

def mix(c1, c2, t):
    return c1[None, None, :] * (1 - t[..., None]) + c2[None, None, :] * t[..., None]

# ---------------------------------------------------------------- concrete
def hormigon(name, base, dark, grit=1.0, seed=3, seams=True):
    body = fnoise(W, H, 460, 5, seed)
    blotch = fnoise(W, H, 150, 4, seed + 1)
    fine = fnoise(W, H, 34, 3, seed + 2)
    t = np.clip(0.48 * body + 0.34 * blotch + 0.18 * fine, 0, 1)
    arr = mix(base, dark, t * 0.72)
    arr -= speckle(W, H, 0.030, 0.5, seed + 3)[..., None] * 26 * grit
    arr += speckle(W, H, 0.010, 0.8, seed + 4)[..., None] * 14
    if seams:
        y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
        seam = np.exp(-((np.sin(y * math.pi * 3.0)) ** 2) * 300.0)
        arr -= np.repeat(seam, W, axis=1)[..., None] * 8
    arr += rng.normal(0, 1, (H, W, 1)) * 3.6 * grit
    save(arr, name)

# ---------------------------------------------------------------- asphalt / aggregate
def asfalto(name, base, chip, seed=11):
    """Aggregate: real stone chips drawn as ellipses, like the asphalt under the card."""
    body = fnoise(W, H, 300, 5, seed)
    arr = mix(base * 0.80, base * 1.20, body * 0.7)
    r = np.random.default_rng(seed)
    layer = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(layer)
    tones = Image.new("L", (W, H), 128)
    dt = ImageDraw.Draw(tones)
    for count, rmin, rmax in ((9000, 2, 5), (3800, 4, 9), (900, 8, 15), (180, 14, 22)):
        for _ in range(count):
            cx, cy = int(r.integers(0, W)), int(r.integers(0, H))
            rad = float(r.integers(rmin, rmax))
            k = int(r.integers(5, 8))
            ang = r.random() * 6.283
            poly = []
            for j in range(k):
                a = ang + j * 6.283 / k
                rr = rad * (0.62 + r.random() * 0.55)
                poly.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.85))
            d.polygon(poly, fill=255)
            dt.polygon(poly, fill=int(96 + r.random() * 74))
    layer = layer.filter(ImageFilter.GaussianBlur(0.7))
    tones = tones.filter(ImageFilter.GaussianBlur(0.7))
    m = np.array(layer, dtype=np.float32) / 255.0
    tn = (np.array(tones, dtype=np.float32) / 255.0 - 0.5) * 2.0
    light = np.clip(tn, 0, 1)[..., None] * (chip - base)[None, None, :] * 0.62
    dark = np.clip(-tn, 0, 1)[..., None] * (base * 0.55 - base)[None, None, :] * 0.62
    arr += m[..., None] * (light + dark)
    arr -= speckle(W, H, 0.05, 0.4, seed + 7)[..., None] * 12
    arr += rng.normal(0, 1, (H, W, 1)) * 4.0
    save(arr, name)

# ---------------------------------------------------------------- basalt, fractured
def basalto(name, base, dark, crack_col, seed=23):
    body = fnoise(W, H, 320, 5, seed)
    arr = mix(base, dark, body * 0.8)
    c = cracks(n=260, seed=seed + 4, width=0.05)
    c2 = cracks(n=900, seed=seed + 9, width=0.03) * 0.45
    c = np.clip(c + c2, 0, 1)
    arr = arr * (1 - c[..., None] * 0.9) + crack_col[None, None, :] * c[..., None] * 0.9
    # shallow relief so the plates read as solid
    rel = np.array(Image.fromarray((c * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6.0)),
                   dtype=np.float32) / 255.0
    arr += (0.5 - rel)[..., None] * 9
    arr -= speckle(W, H, 0.03, 0.5, seed + 12)[..., None] * 14
    arr += rng.normal(0, 1, (H, W, 1)) * 3.2
    save(arr, name)

# ---------------------------------------------------------------- mineral veins in gold
def mineral(name, base, dark, vein, seed=41):
    body = fnoise(W, H, 400, 5, seed)
    arr = mix(base, dark, body * 0.82)
    c = cracks(n=40, seed=seed + 3, width=0.075)
    brk = (fnoise(W, H, 90, 4, seed + 21) > 0.46).astype(np.float32)
    c = c * brk
    mask = (fnoise(W, H, 500, 3, seed + 6) > 0.52).astype(np.float32)
    mask = np.array(Image.fromarray((mask * 255).astype(np.uint8))
                    .filter(ImageFilter.GaussianBlur(30.0)), dtype=np.float32) / 255.0
    v = c * mask
    v = np.array(Image.fromarray((v * 255).astype(np.uint8))
                 .filter(ImageFilter.GaussianBlur(1.1)), dtype=np.float32) / 255.0
    arr = arr * (1 - v[..., None] * 0.62) + vein[None, None, :] * v[..., None] * 0.62
    glow = np.array(Image.fromarray((v * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10.0)),
                    dtype=np.float32) / 255.0
    arr += glow[..., None] * vein[None, None, :] * 0.10
    arr -= speckle(W, H, 0.025, 0.5, seed + 11)[..., None] * 12
    arr += rng.normal(0, 1, (H, W, 1)) * 2.8
    save(arr, name)

# ---------------------------------------------------------------- regolith / crater field
def regolito(name, base, dark, n_craters=42, seed=57, light=(-0.7, -0.7)):
    r = np.random.default_rng(seed)
    body = fnoise(W, H, 560, 5, seed)
    dust = fnoise(W, H, 26, 3, seed + 2)
    arr = mix(base, dark, np.clip(0.72 * body + 0.28 * dust, 0, 1) * 0.5)
    hs, ws = H // 3, W // 3
    ys, xs = np.mgrid[0:hs, 0:ws].astype(np.float32)
    hgt = (fnoise(ws, hs, 90, 5, seed + 31) - 0.5) * 1.6
    hgt += (fnoise(ws, hs, 22, 4, seed + 32) - 0.5) * 0.7
    for _ in range(n_craters):
        cx, cy = r.random() * ws, r.random() * hs
        rad = (26 + r.random() ** 2.2 * 150)
        d = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2) / rad
        hgt -= np.clip(1 - d, 0, 1) ** 2.4 * 0.30
        hgt += np.exp(-((d - 1.0) ** 2) * 12.0) * 0.16
    hgt = np.array(Image.fromarray(((hgt - hgt.min()) / max(1e-6, np.ptp(hgt)) * 255).astype(np.uint8))
                   .filter(ImageFilter.GaussianBlur(1.2)), dtype=np.float32) / 255.0
    gy, gx = np.gradient(hgt)
    shade = np.clip(0.5 + (gx * light[0] + gy * light[1]) * 5.0, 0, 1)
    shade = up(shade)
    arr += (shade - 0.5)[..., None] * 30
    arr += speckle(W, H, 0.018, 0.4, seed + 8)[..., None] * 10
    arr += rng.normal(0, 1, (H, W, 1)) * 3.0
    save(arr, name)

# ---------------------------------------------------------------- stone slab, bone
def piedra(name, seed=71):
    body = fnoise(W, H, 640, 5, seed)
    grain = fnoise(W, H, 70, 4, seed + 1)
    arr = mix(GROUND, np.array((203, 197, 191), dtype=np.float32),
              np.clip(0.72 * body + 0.28 * grain, 0, 1) * 0.8)
    c = cracks(n=70, seed=seed + 6, width=0.02)
    arr -= c[..., None] * 13
    arr += speckle(W, H, 0.012, 0.4, seed + 11)[..., None] * 10
    arr += rng.normal(0, 1, (H, W, 1)) * 2.4
    save(arr, name)

if __name__ == "__main__":
    hormigon("velum-hormigon-hueso.jpg", GROUND, np.array((196, 190, 185), dtype=np.float32))
    hormigon("velum-hormigon-azul.jpg", NAVY, INK * 0.66, grit=1.15, seed=8)
    asfalto("velum-asfalto-azul.jpg", INK * 1.5, np.array((150, 152, 156), dtype=np.float32))
    basalto("velum-basalto.jpg", NAVY * 0.92, INK * 0.66, INK * 0.42)
    mineral("velum-mineral-oro.jpg", NAVY * 0.8, INK * 0.62, GOLD)
    regolito("velum-regolito-hueso.jpg", GROUND, np.array((188, 182, 176), dtype=np.float32), n_craters=18)
    regolito("velum-regolito-azul.jpg", NAVY, INK * 0.66, n_craters=22, seed=91)
    piedra("velum-piedra-hueso.jpg")
