# -*- coding: utf-8 -*-
"""VELUM manual — pages 01-18."""
from core import *
from parts import head, divider, icon, yes_no, foot

S1 = "01 — %s"
S2 = "02 — %s"

# ---------------------------------------------------------------- 01 cover
def p01(L):
    o = [rect(0, 0, W, H, GROUND)]
    o.append(veil(0, 120, W, 840, n=14, stroke=INK, sw=1.1, op=0.10, spread=1.25))
    o.append(rect(56, 56, W - 112, H - 112, "none", stroke=INK, sw=0.8, op=0.16))
    o.append(label(W / 2, 300, L["cover_eyebrow"], fill=AMBER, size=12, anchor="middle"))
    o.append(full_logo(680, 360, 560, "light"))
    o.append(line(W / 2 - 46, 706, W / 2 + 46, 706, stroke=GOLD, sw=1.2))
    o.append(t(W / 2, 776, L["cover_tag"], size=26, f=DIS, fill=TXT, op=0.78, anchor="middle", ls=6))
    o.append(t(W / 2, 838, L["cover_sub"], size=15, fill=GREY, anchor="middle", ls=1))
    o.append(label(130, 1000, L["descriptor"], fill=GREY, size=10, w=500))
    o.append(label(W - 130, 1000, "01 / %d" % L["total"], fill=GREY, size=10, anchor="end", w=500))
    return page("".join(o), bg=GROUND)

# ---------------------------------------------------------------- 02 contents
def p02(L):
    o = [chrome(L["contents"], 2, L["total"], sub=L["manual"])]
    o.append(t(M, 300, L["contents"].upper(), size=92, f=DIS, w=400, fill=TXT, ls=4))
    o.append(line(M, 352, M + 120, 352, stroke=GOLD, sw=1.4))
    o.append(para(M, 424, L["contents_intro"], size=17, lh=30, fill=GREY))
    o.append(mono_logo(M - 10, 640, 240, "light"))
    x, y = 830, 210
    for i, (n, ttl, sub) in enumerate(L["sections"]):
        yy = y + i * 122
        o.append(line(x, yy - 44, W - M, yy - 44, stroke=INK, sw=0.7, op=0.16))
        o.append(t(x, yy, n, size=13, w=600, fill=AMBER, ls=2))
        o.append(t(x + 92, yy + 8, ttl.upper(), size=34, f=DIS, w=400, fill=TXT, ls=2))
        o.append(t(x + 92, yy + 42, sub, size=15, fill=GREY))
    o.append(line(x, y + 6 * 122 - 44, W - M, y + 6 * 122 - 44, stroke=INK, sw=0.7, op=0.16))
    return page("".join(o))

# ---------------------------------------------------------------- 03 divider
def p03(L):
    s = L["sections"][0]
    return divider(L, 3, s[0], s[1], s[2])

# ---------------------------------------------------------------- 04 origin
def p04(L):
    o = [chrome(S1 % L["sections"][0][1], 4, L["total"], sub=L["manual"])]
    o.append(img("grad1.b64", 1180, 130, W - 1180 - 130, H - 260))
    o.append(veil(1180, 380, W - 1180 - 130, 320, n=8, stroke=GOLD, sw=1.2, op=0.45))
    o.append(label(M, 210, L["origin_eyebrow"], fill=AMBER))
    o.append(t(M, 318, L["origin_h1"], size=88, f=DIS, w=400, fill=TXT, ls=3))
    o.append(t(M, 410, L["origin_h2"], size=88, f=DIS, w=400, fill=TXT, ls=3))
    o.append(line(M, 470, M + 90, 470, stroke=GOLD, sw=1.4))
    o.append(para(M, 534, L["origin_lead"], size=22, lh=36, fill=TXT, op=0.9))
    for i, (h, lines) in enumerate(L["origin_cols"]):
        x = M + i * 480
        o.append(line(x, 648, x + 400, 648, stroke=INK, sw=0.8, op=0.25))
        o.append(t(x, 700, h.upper(), size=26, f=DIS, fill=TXT, ls=2.5))
        o.append(para(x, 746, lines, size=16, lh=28, fill=GREY))
    o.append(para(M, 880, L["origin_body"][3:], size=16, lh=29, fill=GREY))
    return page("".join(o))

# ---------------------------------------------------------------- 05 purpose
def p05(L):
    o = head(L, S1 % L["sections"][0][1], 5, L["pvm_eyebrow"], L["pvm_title"])
    o.append(line(M, 400, W - M, 400, stroke=INK, sw=0.7, op=0.18))
    for i, (n, h, lines) in enumerate(L["pvm"]):
        y = 470 + i * 190
        o.append(t(M, y, n, size=13, w=600, fill=AMBER, ls=2))
        o.append(t(M + 92, y + 4, h.upper(), size=34, f=DIS, fill=TXT, ls=2.5))
        o.append(para(M + 92, y + 48, lines, size=18, lh=30, fill=GREY))
        o.append(line(M, y + 128, W - M, y + 128, stroke=INK, sw=0.7, op=0.12))
    o.append(veil(M, 1010, W - 2 * M, 40, n=5, stroke=GOLD, sw=1.1, op=0.5, spread=0.5))
    return page("".join(o))

# ---------------------------------------------------------------- 06 values
def p06(L):
    o = head(L, S1 % L["sections"][0][1], 6, L["values_eyebrow"], L["values_title"])
    o.append(line(M, 400, W - M, 400, stroke=INK, sw=0.7, op=0.18))
    cw = (W - 2 * M) / 3.0
    for i, (h, sub) in enumerate(L["values"]):
        x = M + (i % 3) * cw
        y = 500 + (i // 3) * 260
        o.append(t(x, y, "0%d" % (i + 1), size=13, w=600, fill=AMBER, ls=2))
        o.append(t(x, y + 54, h.upper(), size=32, f=DIS, fill=TXT, ls=2))
        o.append(para(x, y + 100, [sub], size=16, lh=28, fill=GREY))
        o.append(line(x, y + 160, x + cw - 60, y + 160, stroke=INK, sw=0.7, op=0.12))
    return page("".join(o))

# ---------------------------------------------------------------- 07 positioning
def p07(L):
    o = head(L, S1 % L["sections"][0][1], 7, L["pos_eyebrow"], L["pos_title"], L["pos_lead"])
    o.append(line(M, 450, W - M, 450, stroke=INK, sw=0.7, op=0.18))
    o += yes_no(M, M + 900, 520, L["pos_yes_h"], L["pos_no_h"], L["pos_yes"], L["pos_no"], lh=68, size=22)
    return page("".join(o))

# ---------------------------------------------------------------- 08 personality
def p08(L):
    o = head(L, S1 % L["sections"][0][1], 8, L["per_eyebrow"], L["per_title"])
    o.append(line(M, 400, W - M, 400, stroke=INK, sw=0.7, op=0.18))
    o += yes_no(M, M + 760, 460, L["per_yes_h"], L["per_no_h"], L["per_yes"], L["per_no"],
                lh=62, size=21)
    o.append(para(W - M, 520, L["per_note"], size=16, lh=30, fill=GREY, anchor="end"))
    return page("".join(o))

# ---------------------------------------------------------------- 09 territory
def p09(L):
    o = head(L, S1 % L["sections"][0][1], 9, L["ter_eyebrow"], L["ter_title"])
    o.append(line(M, 400, W - M, 400, stroke=INK, sw=0.7, op=0.18))
    grads = ["grad3.b64", "grad1.b64", "grad4.b64", "grad5.b64", "grad7.b64"]
    cw = (W - 2 * M - 4 * 20) / 5.0
    for i, (h, sub) in enumerate(L["ter"]):
        x = M + i * (cw + 20)
        o.append(img(grads[i], x, 450, cw, 300))
        o.append(rect(x, 450, cw, 300, "none", stroke=INK, sw=0.7, op=0.2))
        o.append(t(x, 802, h.upper(), size=24, f=DIS, fill=TXT, ls=2))
        o.append(para(x, 844, [sub], size=14, lh=24, fill=GREY))
    o.append(foot(["01 — 05"], y=980))
    return page("".join(o))

# ---------------------------------------------------------------- 10 manifesto
def p10(L):
    o = [chrome(S1 % L["sections"][0][1], 10, L["total"], fill=IVORY, sub=L["manual"])]
    o = [rect(0, 0, W, H, INK)] + o
    o.append(veil(0, 260, W, 560, n=16, stroke=GOLD, sw=1.1, op=0.13, spread=1.2))
    o.append(label(M, 210, L["man_eyebrow"], fill=GOLD))
    y = 330
    for i, ln in enumerate(L["man_lines"]):
        if ln:
            o.append(t(M, y, ln, size=34, f=SER, fill=IVORY, op=0.94, italic=True))
        y += 46 if ln else 26
    o.append(line(M, y + 30, M + 120, y + 30, stroke=GOLD, sw=1.2))
    o.append(t(M, y + 96, L["man_sign"], size=30, f=DIS, fill=GOLD, ls=3))
    o.append(mono_logo(W - M - 260, 380, 220, "dark"))
    return page("".join(o), bg=INK)

# ---------------------------------------------------------------- 11 houses
def p11(L):
    o = head(L, S1 % L["sections"][0][1], 11, L["houses_eyebrow"], L["houses_title"], L["houses_lead"])
    o.append(line(M, 440, W - M, 440, stroke=INK, sw=0.7, op=0.18))
    cw = (W - 2 * M) / 3.0
    for i, (h, sub, cross, ic) in enumerate(L["houses"]):
        x = M + (i % 3) * cw
        y = 486 + (i // 3) * 248
        o.append(icon(ic, x, y, 1.5))
        o.append(t(x, y + 136, h.upper(), size=24, f=DIS, w=400, fill=TXT, ls=2))
        o.append(t(x, y + 170, sub, size=15, fill=GREY))
        o.append(t(x, y + 200, "%s · %s" % (L["crosses"], cross), size=13, fill=AMBER))
        o.append(line(x, y + 228, x + cw - 60, y + 228, stroke=INK, sw=0.7, op=0.14))
    o.append(foot(L["houses_foot"]))
    return page("".join(o))

# ---------------------------------------------------------------- 12 architecture
def p12(L):
    o = head(L, S1 % L["sections"][0][1], 12, L["arch_eyebrow"], L["arch_title"])
    o.append(rect(M, 390, W - 2 * M, 300, PAPER, op=0.4))
    o.append(full_logo(M + 110, 456, 300, "light"))
    o.append(t(M + 110, 630, L["arch_parent"], size=16, fill=GREY))
    o.append(line(M + 560, 430, M + 560, 650, stroke=INK, sw=0.8, op=0.3))
    o.append(t(M + 640, 506, L["arch_child_name"], size=32, f=DIS, fill=TXT, ls=2.5))
    o.append(t(M + 640, 550, L["arch_child_desc"], size=18, fill=GREY))
    o.append(t(M + 640, 630, L["arch_child_world"], size=16, fill=GREY))
    o.append(veil(M + 1180, 450, 490, 190, n=8, stroke=GOLD, sw=1.3, op=0.55))
    o += yes_no(M, M + 760, 750, L["arch_yes_h"], L["arch_no_h"], L["arch_yes"], L["arch_no"],
                lh=52, size=17)
    o.append(para(W - M, 806, L["arch_note"], size=16, lh=28, fill=GREY, anchor="end"))
    return page("".join(o))

# ---------------------------------------------------------------- 13 voice
def p13(L):
    o = head(L, S1 % L["sections"][0][1], 13, L["voice_eyebrow"], L["voice_title"], L["voice_lead"])
    o.append(line(M, 450, W - M, 450, stroke=INK, sw=0.7, op=0.18))
    for i, (yh, ys, nh, ns) in enumerate(L["voice_pairs"]):
        y = 520 + i * 150
        o.append(label(M, y, yh, fill=AMBER, size=10))
        o.append(t(M, y + 46, ys, size=25, f=SER, fill=TXT, italic=True))
        o.append(label(M + 900, y, nh, fill=CLAY, size=10))
        o.append(t(M + 900, y + 46, ns, size=21, fill=GREY, op=0.85))
        o.append(line(M, y + 86, W - M, y + 86, stroke=INK, sw=0.7, op=0.12))
    o.append(label(M, 1000 - 60, L["voice_rules_h"], fill=AMBER, size=11))
    for i, r in enumerate(L["voice_rules"]):
        o.append(t(M + 200 + (i % 2) * 800, 940 + (i // 2) * 34, "— " + r, size=15, fill=GREY))
    return page("".join(o))

# ---------------------------------------------------------------- 14 divider
def p14(L):
    s = L["sections"][1]
    return divider(L, 14, s[0], s[1], s[2])

# ---------------------------------------------------------------- 15 anatomy
def p15(L):
    o = head(L, S2 % L["sections"][1][1], 15, L["id_anatomy_eyebrow"], L["id_anatomy_title"])
    o.append(rect(560, 390, W - M - 560, 420, PAPER, op=0.4))
    lx, ly, lw = 640, 430, 760
    sc = lw / 141.57
    o.append(full_logo(lx, ly, lw, "light"))
    for (ax, ay, r) in ((22, 38, 96), (60, 26, 80), (118, 6.5, 52)):
        o.append(circ(lx + ax * sc, ly + ay * sc, r, stroke=AMBER, sw=1, op=0.75, dash="5 6"))
    for i, (n, h, lines) in enumerate(L["id_anatomy"]):
        y = 420 + i * 170
        o.append(t(M, y, n, size=13, w=600, fill=AMBER, ls=2))
        o.append(t(M, y + 44, h.upper(), size=26, f=DIS, fill=TXT, ls=2))
        o.append(para(M, y + 80, lines, size=15, lh=25, fill=GREY))
    o.append(line(M, 900, W - M, 900, stroke=INK, sw=0.7, op=0.16))
    o.append(foot(L["id_anatomy_foot"], y=944))
    return page("".join(o))

# ---------------------------------------------------------------- 16 construction
def p16(L):
    o = head(L, S2 % L["sections"][1][1], 16, L["id_geom_eyebrow"], L["id_geom_title"])
    gx, gy, gw = 620, 400, 620
    gh = gw * 38.64 / 56.34
    o.append(rect(gx - 60, gy - 60, gw + 120, gh + 120, PAPER, op=0.4))
    o.append(grid(gx - 60, gy - 60, gw + 120, gh + 120, op=0.2))
    o.append(rect(gx - 60, gy - 60, gw + 120, gh + 120, "none", stroke=INK, sw=0.7, op=0.25))
    cx, cy = gx + gw * 0.30, gy + gh * 0.52
    o.append(circ(cx, cy, gh * 0.62, stroke=AMBER, sw=0.8, op=0.5, dash="5 6"))
    o.append(circ(cx, cy, gh * 0.40, stroke=AMBER, sw=0.8, op=0.35, dash="5 6"))
    o.append(line(gx - 60, cy, gx + gw + 60, cy, stroke=INK, sw=0.7, op=0.28, dash="5 6"))
    o.append(line(cx, gy - 60, cx, gy + gh + 60, stroke=INK, sw=0.7, op=0.28, dash="5 6"))
    o.append(mono_logo(gx, gy, gw, "light"))
    o.append(label(M, 430, "56 : 39", fill=AMBER, size=11))
    o.append(para(M, 480, ["1x = " + ("altura de la estrella" if L["lang"] == "ES" else "height of the star")],
                  size=16, lh=27, fill=GREY))
    o.append(line(M, 940, W - M, 940, stroke=INK, sw=0.7, op=0.16))
    o.append(foot(L["id_geom_foot"], y=984))
    return page("".join(o))

# ---------------------------------------------------------------- 17 lockups
def p17(L):
    o = head(L, S2 % L["sections"][1][1], 17, L["id_lock_eyebrow"], L["id_lock_title"])
    cw, ch = (W - 2 * M - 3 * 26) / 4.0, 260
    for i, (name, lines) in enumerate(L["id_locks"]):
        x = M + i * (cw + 26)
        o.append(rect(x, 400, cw, ch, PAPER, op=0.4))
        o.append(rect(x, 400, cw, ch, "none", stroke=INK, sw=0.7, op=0.2))
        if i == 0:
            o.append(full_logo(x + 30, 490, cw - 60, "light"))
        elif i == 1:
            o.append(mono_logo(x + cw / 2 - 70, 470, 140, "light"))
        elif i == 2:
            o.append(circ(x + cw / 2, 530, 86, fill=INK))
            o.append(mono_logo(x + cw / 2 - 52, 504, 104, "dark"))
            o.append(t(x + cw / 2, 494, "VELUM", size=10, fill=GOLD, ls=4, anchor="middle"))
        else:
            o.append(full_logo(x + 30, 470, cw - 60, "light"))
            o.append(line(x + 30, 566, x + cw - 30, 566, stroke=INK, sw=0.7, op=0.3))
            o.append(t(x + cw / 2, 596, "TRAVEL", size=16, f=DIS, fill=TXT, ls=4, anchor="middle"))
        o.append(t(x, ch + 452, name.upper(), size=20, f=DIS, fill=TXT, ls=2))
        o.append(para(x, ch + 492, lines, size=14, lh=24, fill=GREY))
    return page("".join(o))

# ---------------------------------------------------------------- 18 clear space
def p18(L):
    o = head(L, S2 % L["sections"][1][1], 18, L["id_clear_eyebrow"], L["id_clear_title"])
    lw, lh = 640, 640 * 63.16 / 141.57
    lx, ly = 430, 470
    pad = 84
    o.append(rect(lx - pad * 2, ly - pad * 2, lw + pad * 4, lh + pad * 4, PAPER, op=0.5))
    o.append(full_logo(lx, ly, lw, "light"))
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s" '
             'stroke-width="1" stroke-dasharray="6 7" opacity="0.75"/>'
             % (lx - pad, ly - pad, lw + pad * 2, lh + pad * 2, AMBER))
    o.append(line(lx + lw / 2, ly - pad * 2, lx + lw / 2, ly - pad, stroke=AMBER, sw=0.8))
    o.append(line(lx - pad * 2, ly + lh / 2, lx - pad, ly + lh / 2, stroke=AMBER, sw=0.8))
    o.append(t(lx + lw / 2 + 14, ly - pad * 1.4, "x", size=17, f=SER, fill=AMBER, italic=True))
    o.append(t(lx - pad * 1.5, ly + lh / 2 - 12, "x", size=17, f=SER, fill=AMBER, italic=True))
    o.append(label(M, 620, L["id_clear_h"], fill=AMBER, size=11))
    o.append(para(M, 668, L["id_clear_body"], size=16, lh=27, fill=GREY))
    o.append(label(M, 800, L["id_min_h"], fill=AMBER, size=11))
    o.append(para(M, 848, L["id_min_body"], size=16, lh=27, fill=GREY))
    o.append(line(W - M - 300, 620, W - M, 620, stroke=INK, sw=0.7, op=0.2))
    o.append(para(W - M, 668, L["id_clear_note"], size=16, lh=27, fill=GREY, anchor="end"))
    return page("".join(o))
