# -*- coding: utf-8 -*-
"""Move the loose reference photographs into 07_Photography/References with speaking names."""
import os, shutil

B = os.path.dirname(os.path.abspath(__file__))
SEC = os.path.dirname(B)
KIT = os.path.dirname(SEC)
SRC = os.path.dirname(KIT)                 # Vellum Brand/
REF = SEC + "/References"
os.makedirs(REF, exist_ok=True)

# source stem -> (new name, principle, house, ES caption, EN caption)
MAP = [
    ("adwtkd", "velum-foto-01-travel-avion-contrapicado", "Contrapicado", "Velum Travel",
     "Avión desde abajo contra cielo abierto. La referencia madre.",
     "Aircraft from below against open sky. The parent reference."),
    ("trbggj", "velum-foto-02-properties-esquina-hormigon", "Contrapicado", "Velum Properties",
     "Esquina de hormigón, líneas convergiendo hacia el cielo.",
     "Concrete corner, lines converging towards the sky."),
    ("333y1t", "velum-foto-03-properties-monolito-cielo", "Contrapicado", "Velum Properties",
     "Monolito de piedra visto desde su base.",
     "Stone monolith seen from its base."),
    ("mbe6g1", "velum-foto-04-trade-muelle-contrapicado", "Contrapicado", "Velum Trade",
     "Estructura de muelle desde el agua, a contraluz.",
     "Pier structure from the water, backlit."),
    ("u8ydos", "velum-foto-05-mobility-camioneta-horizonte", "Contraluz", "Velum Mobility",
     "Vehículo recortado contra el sol bajo, árido en primer término.",
     "Vehicle cut against the low sun, aggregate in the foreground."),
    ("fung8v", "velum-foto-06-foods-pan-piedra", "Contraluz", "Velum Foods",
     "Materia prima sobre mesa de piedra, luz de ventana detrás.",
     "Raw ingredient on a stone table, window light behind."),
    ("fn3lhk", "velum-foto-07-umbral-arco-figura", "Umbral", "—",
     "Vano de piedra: el umbral literal, con la figura mirando afuera.",
     "Stone doorway: the literal threshold, figure looking out."),
    ("6mrn8f", "velum-foto-08-umbral-borde-figura", "Umbral", "—",
     "El borde de la losa contra el horizonte.",
     "The edge of the slab against the horizon."),
    ("9q5syf", "velum-foto-09-umbral-pino-muro", "Contraluz", "—",
     "El sol justo detrás del muro; la rama entra en el aire.",
     "The sun just behind the wall; the branch enters the air."),
    ("ilkxxo", "velum-foto-10-umbral-losa-llanura", "Umbral", "—",
     "Losa vertical sobre llanura de piedra al atardecer.",
     "Vertical slab on a stone plain at dusk."),
    ("litxdz", "velum-foto-11-umbral-niebla-figura", "Aire", "—",
     "Niebla entre dos planos oscuros: el umbral sin objeto.",
     "Fog between two dark planes: the threshold with no object."),
    ("pxb5ae", "velum-foto-12-aire-figura-llanura", "Aire", "—",
     "Dos tercios de cielo, la figura en el último tercio.",
     "Two thirds of sky, the figure in the last third."),
    ("bpw34i", "velum-foto-13-horizonte-acantilado", "Aire", "—",
     "Capas de horizonte: lo que se ve y lo que todavía no.",
     "Layers of horizon: what can be seen and what cannot yet."),
    ("th3iwe", "velum-foto-14-materia-cornisa-cielo", "Materia dura", "—",
     "Cornisa de piedra desde abajo: materia contra aire.",
     "Stone cornice from below: matter against air."),
]

def find(stem):
    for d in (SRC, REF):
        for f in os.listdir(d):
            if stem in f and f.lower().endswith((".jpg", ".jpeg", ".png")):
                return d + "/" + f
    return None

if __name__ == "__main__":
    moved, rows = 0, []
    for stem, new, prin, house, es, en in MAP:
        src = find(stem)
        if not src:
            print("  missing:", stem)
            continue
        ext = os.path.splitext(src)[1].lower()
        dst = REF + "/" + new + ext
        if os.path.abspath(src) != os.path.abspath(dst):
            shutil.move(src, dst)
            moved += 1
        rows.append((os.path.basename(dst), prin, house, es, en))
    # drop the old first-reference name if it is still around
    old = REF + "/velum-referencia-01-contrapicado.png"
    if os.path.exists(old) and os.path.exists(REF + "/velum-foto-01-travel-avion-contrapicado.png"):
        os.remove(old)

    L = ["# VELUM — Referencias fotográficas", "",
         "Imágenes aprobadas. Cada una demuestra al menos un principio de `FOTOGRAFIA.md`.",
         "Al añadir una nueva se guarda su prompt en `../Prompts/` o en un `.txt` al lado.", "",
         "| Archivo | Principio | Casa | Qué demuestra |", "|---|---|---|---|"]
    for f, prin, house, es, en in rows:
        L.append("| `%s` | %s | %s | %s |" % (f, prin, house, es))
    L += ["", "---", "", "# VELUM — Photographic references", "",
          "Approved images. Each one demonstrates at least one principle from `PHOTOGRAPHY-EN.md`.", "",
          "| File | Principle | House | What it shows |", "|---|---|---|---|"]
    EN_P = {"Contrapicado": "Low angle", "Contraluz": "Backlight", "Umbral": "Threshold",
            "Aire": "Air", "Materia dura": "Hard matter"}
    for f, prin, house, es, en in rows:
        L.append("| `%s` | %s | %s | %s |" % (f, EN_P.get(prin, prin), house, en))
    L.append("")
    open(REF + "/INDEX.md", "w", encoding="utf-8").write("\n".join(L))
    print("moved %d files · %d cataloged" % (moved, len(rows)))
