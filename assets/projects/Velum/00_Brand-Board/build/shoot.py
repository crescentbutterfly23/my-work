# -*- coding: utf-8 -*-
"""Render the brand board SVG to PNG with headless Edge."""
import os, subprocess, shutil, urllib.parse
from PIL import Image

B = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(B + "/..")
TMP = B + "/tmp"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
os.makedirs(TMP, exist_ok=True)

NAME = "velum-brand-board"
W, H = 2000, 2700

shutil.copy(OUT + "/%s.svg" % NAME, TMP + "/%s.svg" % NAME)
html = ('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:#F4F0EE;'
        'width:%dpx;height:%dpx;overflow:hidden}img{display:block;width:%dpx;height:%dpx}</style>'
        '<img src="%s">') % (W, H, W, H, urllib.parse.quote(NAME + ".svg"))
open(TMP + "/v.html", "w", encoding="utf-8").write(html)

out = OUT + "/%s.png" % NAME
if os.path.exists(out):
    os.remove(out)
subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                "--force-device-scale-factor=1", "--window-size=%d,%d" % (W, H),
                "--screenshot=" + out, "file:///" + (TMP + "/v.html").replace("\\", "/")],
               capture_output=True, timeout=240)

im = Image.open(out).convert("RGB")
im.resize((760, 1026)).save(TMP + "/preview.png")
print(out, im.size, os.path.getsize(out) // 1024, "KB")
