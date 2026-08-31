# -*- coding: utf-8 -*-
"""Build velum-brand-kit-web.html — the whole kit as one self-contained bilingual page."""
import os, re, io, base64, glob
from PIL import Image

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)          # 04_Guidelines
KIT = os.path.dirname(ROOT)            # VELUM-Brand Kit
OUT = ROOT + "/velum-brand-kit-web.html"

GROUND, INK, NAVY, GOLD, CREAM, AMBER, PEARL, GREY, BLACK = (
    "#F4F0EE", "#0B1D34", "#20344D", "#D4AF37", "#E8DCC0", "#B8912B", "#DADDE3", "#55585F", "#1A1A1A")

# ---------------------------------------------------------------- assets
def logo_svg(name, fill_map=None, cls=""):
    s = open(KIT + "/01_Logo/SVG/%s.svg" % name, encoding="utf-8").read()
    s = s.replace("<svg ", '<svg class="%s" ' % cls, 1) if cls else s
    return s.replace("\n", "")

def jpg(path, w=760, q=74, crop=None):
    im = Image.open(path).convert("RGB")
    if crop:
        im = im.crop(crop)
    sc = w / im.width
    im = im.resize((w, max(1, int(im.height * sc))), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=q)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def tex(name, w=560):
    return jpg(KIT + "/05_Textures/" + name, w=w, q=72)

def raw_b64(path):
    import base64 as _b
    return _b.b64encode(open(path, "rb").read()).decode()

def page_png(code, num, w=900):
    f = glob.glob(KIT + "/04_Guidelines/PNG_%s/velum-%s-%02d-*.png" % (code, code.lower(), num))
    return jpg(f[0], w=w, q=78)

# ---------------------------------------------------------------- copy
def T(es, en):
    """Bilingual text node."""
    return '<span data-es="%s" data-en="%s">%s</span>' % (es, en, es)

def TA(tag, es, en, attrs=""):
    return '<%s %s data-es="%s" data-en="%s">%s</%s>' % (tag, attrs, es, en, es, tag.split(" ")[0])

PAL = [("Blanco Hueso", "Bone White", GROUND, "Fondo principal", "Main ground"),
       ("Azul Velum", "Velum Blue", INK, "Tinta y paneles", "Ink and panels"),
       ("Oro Velum", "Velum Gold", GOLD, "Acento gráfico", "Graphic accent"),
       ("Crema", "Cream", CREAM, "Superficie cálida", "Warm surface"),
       ("Azul Medio", "Mid Blue", NAVY, "Bloques y sellos", "Blocks and seals"),
       ("Oro Oscuro", "Deep Gold", AMBER, "Oro como texto", "Gold as text"),
       ("Gris Perla", "Pearl Grey", PEARL, "La V sobre oscuro", "The V on dark"),
       ("Gris", "Grey", GREY, "Texto secundario", "Secondary text"),
       ("Negro", "Black", BLACK, "Una tinta, grabado", "One ink, engraving")]

HOUSES = [("Velum Travel", "Viajes y experiencias", "Travel and experiences",
           "M6 27 L42 17 M6 27 L18 31 L14 41 L20 33 L34 37 M42 17 L34 37"),
          ("AL — Ana López", "Aromas que transportan", "Scents that carry you",
           "M19 6 h10 v7 h-10 z M17 13 h14 c3 6 4 9 4 14 v13 a4 4 0 0 1 -4 4 h-14 a4 4 0 0 1 -4 -4 "
           "v-13 c0 -5 1 -8 4 -14 z M19 26 h10"),
          ("Velum Foods", "Alimentos y gastronomía", "Food and gastronomy",
           "M6 39 h36 M10 39 a14 15 0 0 1 28 0 M24 10 v-5 M20.5 5 h7"),
          ("Velum Trade", "Importación y exportación", "Import and export",
           "M24 6 a18 18 0 1 0 0 36 a18 18 0 1 0 0 -36 M6 24 h36 M24 6 c-8 8 -8 28 0 36 M24 6 c8 8 8 28 0 36"),
          ("Velum Properties", "Inmuebles y turismo", "Property and tourism",
           "M10 42 v-30 h14 v30 M24 42 v-20 h14 v20 M14 18 h6 M14 26 h6 M14 34 h6 M28 28 h6 M28 36 h6 M6 42 h36"),
          ("Velum Mobility", "Movilidad eléctrica", "Electric mobility",
           "M9 30 l4 -9 a4 4 0 0 1 3.6 -2.4 h14.8 a4 4 0 0 1 3.6 2.4 l4 9 M7 30 h34 v7 h-34 z "
           "M13 37 v3.5 M35 37 v3.5 M15.5 33.5 h4 M28.5 33.5 h4")]

TEXTURES = [("velum-hormigon-hueso.jpg", "Hormigón", "Concrete"),
            ("velum-hormigon-azul.jpg", "Hormigón azul", "Blue concrete"),
            ("velum-asfalto-azul.jpg", "Árido", "Aggregate"),
            ("velum-basalto.jpg", "Basalto", "Basalt"),
            ("velum-mineral-oro.jpg", "Veta mineral", "Mineral vein"),
            ("velum-piedra-hueso.jpg", "Piedra hueso", "Bone stone"),
            ("velum-regolito-azul.jpg", "Regolito", "Regolith"),
            ("velum-cielo-nocturno.jpg", "Cielo nocturno", "Night sky"),
            ("velum-horizonte-azul.jpg", "Horizonte", "Horizon"),
            ("velum-marmol-hueso.jpg", "Mármol", "Marble")]

SECS = [("marca", "La marca", "The brand"), ("casas", "Las casas", "The houses"),
        ("logotipo", "Logotipo", "Logotype"), ("color", "Color", "Colour"),
        ("tipografia", "Tipografía", "Typography"), ("velo", "El velo", "The veil"),
        ("fotografia", "Fotografía", "Photography"),
        ("aplicaciones", "Aplicaciones", "Applications"), ("descargas", "Descargas", "Downloads")]

PRINCIPLES = [
    ("01", "Contrapicado", "Low angle",
     "La cámara por debajo del sujeto, inclinada 30–45° hacia el cielo.",
     "The camera below the subject, tilted 30–45° toward the sky."),
    ("02", "Contraluz", "Backlight",
     "La luz detrás. El sujeto cae a silueta con un borde cálido.",
     "Light behind. The subject falls to silhouette with a warm rim."),
    ("03", "Aire", "Air",
     "60–70% del encuadre vacío. El aire no es fondo: es el tema.",
     "60–70% of the frame empty. Air is not background: it is the subject."),
    ("04", "Un solo sujeto", "One subject",
     "Un objeto, un gesto. Nunca un bodegón de tres productos.",
     "One object, one gesture. Never a three-product still life."),
    ("05", "El umbral", "The threshold",
     "Un límite que se cruza: horizonte, borde de azotea, vano, orilla.",
     "A limit being crossed: horizon, roof edge, doorway, shoreline."),
    ("06", "Materia dura", "Hard matter",
     "Si hay suelo o muro, es piedra, hormigón, asfalto o metal.",
     "Where there is ground or wall, it is stone, concrete, asphalt or metal."),
    ("07", "Color", "Colour",
     "Sombra azul, luz hueso y un solo acento cálido por imagen.",
     "Blue shadow, bone light and one warm accent per image."),
]

SUBJECTS = [("Velum Travel", "Avión, ala, estela, torre", "Aircraft, wing, contrail, tower"),
            ("AL — Ana López", "Frasco, vidrio, jazmín", "Bottle, glass, jasmine"),
            ("Velum Foods", "Materia prima, manos, mesa", "Raw ingredient, hands, table"),
            ("Velum Trade", "Grúa, contenedor, muelle", "Crane, container, dock"),
            ("Velum Properties", "Esquina, escalera, vano", "Corner, stair, doorway"),
            ("Velum Mobility", "Coche, carga, carretera", "Vehicle, charge, road")]

PH_YES = [("Siluetas limpias contra luz abierta", "Clean silhouettes against open light"),
          ("Cielo con estructura: capas, estelas", "Skies with structure: layers, contrails"),
          ("Superficies duras con textura real", "Hard surfaces with real texture"),
          ("Escala: lo pequeño revela lo enorme", "Scale: the small reveals the enormous"),
          ("Un solo destello cálido", "A single warm flare")]

PH_NO = [("Planetas, cohetes, astronautas, galaxias", "Planets, rockets, astronauts, galaxies"),
         ("Personas posando, equipos de oficina", "People posing, office teams"),
         ("Saturación alta, teal-orange, neón, HDR", "High saturation, teal-orange, neon, HDR"),
         ("Collages de producto y bodegones", "Product collages and still lifes"),
         ("Drones cenitales: mirar hacia abajo", "Top-down drones: looking down")]

REFS = [("velum-foto-13-umbral-arco-figura.jpg", "Umbral", "Threshold"),
        ("velum-foto-07-properties-esquina-hormigon.jpg", "Contrapicado", "Low angle"),
        ("velum-foto-05-mobility-camioneta-horizonte.jpg", "Contraluz", "Backlight"),
        ("velum-foto-14-aire-figura-llanura.jpg", "Aire", "Air"),
        ("velum-foto-12-materia-cornisa-cielo.jpg", "Materia dura", "Hard matter"),
        ("velum-foto-02-al-frasco-muro-cal.jpg", "AL — Ana López", "AL — Ana López"),
        ("velum-foto-04-trade-muelle-contrapicado.jpg", "Velum Trade", "Velum Trade"),
        ("velum-foto-06-foods-pan-piedra.jpg", "Velum Foods", "Velum Foods"),
        ("velum-foto-03-materia-hormigon-apice.jpg", "Velum Properties", "Velum Properties"),
        ("velum-foto-09-umbral-pino-muro.jpg", "Contraluz", "Backlight"),
        ("velum-foto-10-umbral-losa-llanura.jpg", "Umbral", "Threshold"),
        ("velum-foto-11-umbral-niebla-figura.jpg", "Aire", "Air")]

PH_SPEC = [("24–35 mm", "Contrapicado y cielo", "Low angle and sky"),
           ("85–135 mm", "Detalle y horizonte", "Detail and horizon"),
           ("f/8 – f/11", "Planos de cielo", "Sky frames"),
           ("Hora dorada", "±40 min, y hora azul", "±40 min, and blue hour"),
           ("4:5 · 2:3", "Mirada hacia arriba", "The upward gaze"),
           ("16:9 · 2:1", "Horizontes", "Horizons")]

def veil_svg(stroke, op=0.5, n=9, w=600, h=180):
    import math
    o = ['<svg class="veil" viewBox="0 0 %d %d" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">' % (w, h),
         '<g fill="none" stroke="currentColor" stroke-width="1.6" opacity="%.2f" stroke-linecap="round">' % op]
    for i in range(n):
        f = i / float(n - 1)
        yy = h * (0.12 + 0.76 * f)
        amp = h * 0.30 * (0.45 + 0.55 * math.sin(f * math.pi))
        o.append('<path d="M 0 %.1f C %.1f %.1f %.1f %.1f %.1f %.1f S %.1f %.1f %.1f %.1f"/>' % (
            yy, w * 0.22, yy - amp, w * 0.42, yy + amp * 0.55, w * 0.60, yy - amp * 0.12,
            w * 0.86, yy - amp * 0.95, w, yy - amp * 0.62))
    o.append("</g></svg>")
    return "".join(o)

def build():
    hero_bg = tex("velum-hormigon-azul.jpg", w=1400)
    ico = raw_b64(KIT + "/01_Logo/Favicon/favicon.ico")
    touch = raw_b64(KIT + "/01_Logo/Favicon/favicon-app-180x180.png")
    A = []
    A.append("""<title>VELUM — Brand Kit</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" type="image/x-icon" href="data:image/x-icon;base64,__ICO__">
<link rel="apple-touch-icon" sizes="180x180" href="data:image/png;base64,__TOUCH__">
<meta name="theme-color" content="#0B1D34">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&family=Montserrat:wght@300;400;500;600&display=swap">
<style>
:root{
  --ground:#F4F0EE; --surface:#EAE5E1; --surface-2:#E8DCC0;
  --ink:#0B1D34; --ink-2:#55585F; --ink-3:#8A8F97;
  --line:rgba(11,29,52,.16); --line-2:rgba(11,29,52,.30);
  --gold:#D4AF37; --amber:#B8912B; --navy:#20344D; --pearl:#DADDE3;
  --shadow:0 1px 2px rgba(11,29,52,.05), 0 10px 30px rgba(11,29,52,.07);
  --display:"Cinzel",Georgia,"Times New Roman",serif;
  --sans:"Montserrat",-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;
  --maxw:1180px;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#0B1D34; --surface:#132840; --surface-2:#16304C;
    --ink:#F4F0EE; --ink-2:#B9C2CD; --ink-3:#8A97A6;
    --line:rgba(218,221,227,.16); --line-2:rgba(218,221,227,.30);
    --shadow:0 1px 2px rgba(0,0,0,.3), 0 10px 30px rgba(0,0,0,.35);
  }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:76px}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);
  font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 28px}
h1,h2,h3{font-family:var(--display);font-weight:400;letter-spacing:.06em;margin:0}
h2{font-size:clamp(1.5rem,1.1rem+1.4vw,2.1rem);text-transform:uppercase}
h3{font-size:1.05rem;text-transform:uppercase;letter-spacing:.1em}
p{margin:0 0 1rem}
a{color:inherit}
.eyebrow{font-size:.68rem;letter-spacing:.34em;text-transform:uppercase;color:var(--amber);
  font-weight:600;margin-bottom:.9rem}
.lead{font-size:1.06rem;color:var(--ink-2);max-width:62ch}
.small{font-size:.82rem;color:var(--ink-2)}
/* bar */
.bar{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--ground) 88%,transparent);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar-in{display:flex;align-items:center;gap:20px;height:64px}
.bar-mark{display:flex;align-items:center;gap:10px;font-size:.68rem;letter-spacing:.3em;
  text-transform:uppercase;color:var(--ink-2);white-space:nowrap}
.bar-mark svg{height:26px;width:auto}
.secs{display:flex;gap:18px;overflow-x:auto;flex:1;scrollbar-width:none}
.secs::-webkit-scrollbar{display:none}
.secs a{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;text-decoration:none;
  color:var(--ink-2);white-space:nowrap;padding:6px 0;border-bottom:1px solid transparent}
.secs a:hover{color:var(--ink);border-color:var(--gold)}
.lang{display:flex;border:1px solid var(--line-2);border-radius:2px;overflow:hidden}
.lang button{border:0;background:transparent;color:var(--ink-2);font-family:var(--sans);
  font-size:.68rem;letter-spacing:.16em;padding:6px 10px;cursor:pointer}
.lang button[aria-pressed="true"]{background:var(--ink);color:var(--ground)}
/* hero */
.hero{position:relative;min-height:74vh;display:flex;align-items:center;overflow:hidden;
  background:var(--ink)}
.hero-bg{position:absolute;inset:0;background-size:cover;background-position:center;opacity:.9}
.hero-veil{position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(11,29,52,.72),rgba(11,29,52,.55) 45%,rgba(11,29,52,.86))}
.hero-in{position:relative;padding:96px 28px;color:#F7F7F7}
.hero .lock{width:min(460px,72vw);height:auto;display:block;margin-bottom:28px}
.hero h1{font-size:clamp(1.3rem,.9rem+1.6vw,2rem);letter-spacing:.34em;color:#F7F7F7}
.hero .sub{margin-top:14px;color:var(--pearl);letter-spacing:.06em}
.hero .rule{width:76px;height:1px;background:var(--gold);margin:26px 0}
/* sections */
section{padding:84px 0;border-top:1px solid var(--line)}
section:first-of-type{border-top:0}
.grid{display:grid;gap:22px}
.g2{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.g4{grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
.card{background:var(--surface);padding:24px;border:1px solid var(--line);box-shadow:var(--shadow)}
.card h3{margin-bottom:8px}
.card p{margin:0;color:var(--ink-2);font-size:.92rem}
.pill{display:inline-block;font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;
  color:var(--amber);border:1px solid var(--line-2);padding:3px 10px;margin-top:12px}
/* houses */
.house svg{width:44px;height:44px;stroke:var(--amber);fill:none;stroke-width:1.6;
  stroke-linecap:round;stroke-linejoin:round;margin-bottom:14px}
/* swatches */
.sw{border:1px solid var(--line);cursor:pointer;background:none;padding:0;text-align:left;
  font-family:var(--sans);color:inherit;width:100%}
.sw .chip{height:112px;display:block}
.sw .meta{display:block;padding:12px 14px;background:var(--surface)}
.sw .hex{font-size:.78rem;color:var(--ink-2);letter-spacing:.08em}

.sw .nm{display:inline-block;margin-bottom:2px;font-family:var(--display);letter-spacing:.08em;text-transform:uppercase;font-size:.92rem}
.bar-prop{display:flex;height:44px;margin:26px 0 8px;border:1px solid var(--line)}
.bar-prop i{display:block;border-right:1px solid var(--line-2)}
.bar-prop i:last-child{border-right:0}
.copied{position:fixed;left:50%;bottom:28px;transform:translateX(-50%);background:var(--ink);
  color:var(--ground);padding:8px 16px;font-size:.76rem;letter-spacing:.14em;text-transform:uppercase;
  opacity:0;pointer-events:none;transition:opacity .25s}
.copied.on{opacity:1}
/* type */
.spec{background:var(--surface);border:1px solid var(--line);padding:28px}
.spec .aa{font-size:5.4rem;line-height:1;margin-bottom:10px}
.spec .set{color:var(--ink-2);font-size:.88rem;word-break:break-word}
table{width:100%;border-collapse:collapse;margin-top:18px;font-size:.86rem}
th,td{text-align:left;padding:10px 8px;border-bottom:1px solid var(--line);color:var(--ink-2)}
th{font-size:.66rem;letter-spacing:.22em;text-transform:uppercase;color:var(--amber);font-weight:600}
td:first-child{color:var(--ink);font-family:var(--display);letter-spacing:.06em;text-transform:uppercase}
/* media */
figure{margin:0}
figure img{width:100%;height:auto;display:block;border:1px solid var(--line)}
figcaption{font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--ink-2);
  margin-top:10px}
.logo-tile{display:flex;align-items:center;justify-content:center;height:150px;border:1px solid var(--line)}
.logo-tile svg{width:74%;height:auto}
.veil{width:100%;height:150px;display:block;color:var(--ink)}
.pages{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
.hero-shot{position:relative;border:1px solid var(--line);overflow:hidden}
.hero-shot img{width:100%;height:520px;object-fit:cover;object-position:center 38%;display:block}
.hero-shot .tag{position:absolute;left:0;bottom:0;right:0;padding:18px 22px;
  background:linear-gradient(180deg,rgba(11,29,52,0),rgba(11,29,52,.85));color:#F7F7F7}
.hero-shot .tag .k{font-family:var(--display);letter-spacing:.14em;text-transform:uppercase;font-size:1rem}
.hero-shot .tag .v{font-size:.78rem;color:var(--pearl)}
.pnum{font-size:.7rem;letter-spacing:.2em;color:var(--amber);font-weight:600}
.subj{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:0;
  border-top:1px solid var(--line)}
.subj div{padding:16px 0;border-bottom:1px solid var(--line)}
.subj .h{font-family:var(--display);text-transform:uppercase;letter-spacing:.1em;font-size:.9rem}
.subj .s{font-size:.82rem;color:var(--ink-2)}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:26px;margin-top:26px}
.two ul{list-style:none;margin:12px 0 0;padding:0}
.two li{font-size:.92rem;padding:7px 0;border-bottom:1px solid var(--line);color:var(--ink-2)}
.rule-line{font-family:var(--display);letter-spacing:.12em;text-transform:uppercase;
  font-size:.92rem;color:var(--ink);margin-top:26px}
/* downloads */
.dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.dl a{display:block;padding:18px 20px;border:1px solid var(--line-2);text-decoration:none;
  background:var(--surface);transition:border-color .2s,transform .2s}
.dl a:hover{border-color:var(--gold);transform:translateY(-2px)}
.dl .k{font-family:var(--display);letter-spacing:.08em;text-transform:uppercase;font-size:.94rem}
.dl .v{font-size:.78rem;color:var(--ink-2)}
footer{padding:56px 0 72px;border-top:1px solid var(--line);color:var(--ink-2);font-size:.8rem;
  letter-spacing:.06em}
.rule-g{width:76px;height:1px;background:var(--gold);margin:22px 0}
@media (max-width:900px){.secs{display:none}}
@media (max-width:720px){.hero{min-height:60vh}}
</style>""")

    # ---------------- bar
    A.append('<div class="bar"><div class="wrap bar-in">')
    A.append('<div class="bar-mark">%s<span>VELUM</span></div>' % logo_svg("velum-monogram-azul"))
    A.append('<nav class="secs">')
    for sid, es, en in SECS:
        A.append('<a href="#%s" data-es="%s" data-en="%s">%s</a>' % (sid, es, en, es))
    A.append('</nav>')
    A.append('<div class="lang" role="group" aria-label="Language">'
             '<button type="button" data-lang="es" aria-pressed="true">ES</button>'
             '<button type="button" data-lang="en" aria-pressed="false">EN</button></div>')
    A.append('</div></div>')

    # ---------------- hero
    A.append('<header class="hero"><div class="hero-bg" style="background-image:url(%s)"></div>'
             '<div class="hero-veil"></div><div class="wrap hero-in">' % hero_bg)
    A.append(logo_svg("velum-primary-dark-bg", cls="lock"))
    A.append('<h1 data-es="EL CIELO ES EL LÍMITE" data-en="THE SKY IS THE LIMIT">EL CIELO ES EL LÍMITE</h1>')
    A.append('<div class="rule"></div>')
    A.append('<p class="sub" data-es="Grupo empresarial · La Habana, Cuba · Manual de marca 1.0"'
             ' data-en="Business group · Havana, Cuba · Brand guidelines 1.0">'
             'Grupo empresarial · La Habana, Cuba · Manual de marca 1.0</p>')
    A.append('</div></header>')

    A.append('<main class="wrap">')

    # ---------------- 1 marca
    A.append('<section id="marca">')
    A.append('<div class="eyebrow" data-es="La marca" data-en="The brand">La marca</div>')
    A.append('<h2 data-es="Más allá de lo visible" data-en="Beyond the visible">Más allá de lo visible</h2>')
    A.append('<div class="rule-g"></div>')
    A.append('<p class="lead" data-es="Velum significa velo en latín: lo que separa lo que vemos de lo que '
             'hay detrás. También es la vela que atrapa el viento y busca destino. Curiosidad y dirección '
             'en una sola palabra." data-en="Velum is Latin for veil: what separates what we see from what '
             'lies behind it. It is also the sail that catches the wind and finds a destination. Curiosity '
             'and direction in one word.">Velum significa velo en latín: lo que separa lo que vemos de lo '
             'que hay detrás. También es la vela que atrapa el viento y busca destino. Curiosidad y '
             'dirección en una sola palabra.</p>')
    A.append('<div class="grid g3" style="margin-top:34px">')
    for es, en, des, den in [("Descubrir", "Discover", "Mirar más allá de lo que ya existe.",
                              "Look beyond what already exists."),
                             ("Conectar", "Connect", "Unir personas, mercados, ideas y experiencias.",
                              "Bring people, markets, ideas and experiences together."),
                             ("Transformar", "Transform", "Convertir posibilidades en algo tangible.",
                              "Turn possibilities into something tangible.")]:
        A.append('<div class="card"><h3 data-es="%s" data-en="%s">%s</h3>'
                 '<p data-es="%s" data-en="%s">%s</p></div>' % (es, en, es, des, den, des))
    A.append('</div>')
    A.append('<div class="card" style="margin-top:22px;background:var(--surface-2)">'
             '<p style="font-family:var(--display);letter-spacing:.06em;line-height:2;color:var(--ink)" '
             'data-es="Hay un mundo detrás de cada horizonte. Un viaje puede convertirse en una experiencia. '
             'Un aroma, en un recuerdo. Un espacio, en un destino. Una idea, en un negocio." '
             'data-en="There is a world behind every horizon. A journey can become an experience. '
             'A scent, a memory. A space, a destination. An idea, a business.">'
             'Hay un mundo detrás de cada horizonte. Un viaje puede convertirse en una experiencia. '
             'Un aroma, en un recuerdo. Un espacio, en un destino. Una idea, en un negocio.</p></div>')
    A.append('</section>')

    # ---------------- 2 casas
    A.append('<section id="casas">')
    A.append('<div class="eyebrow" data-es="Arquitectura" data-en="Architecture">Arquitectura</div>')
    A.append('<h2 data-es="Una marca madre, seis casas" data-en="One parent brand, six houses">'
             'Una marca madre, seis casas</h2>')
    A.append('<div class="rule-g"></div>')
    A.append('<div class="grid g3">')
    for name, es, en, path in HOUSES:
        A.append('<div class="card house"><svg viewBox="0 0 48 48"><path d="%s"/></svg>'
                 '<h3>%s</h3><p data-es="%s" data-en="%s">%s</p></div>' % (path, name, es, en, es))
    A.append('</div>')
    A.append('<p class="small" style="margin-top:20px" data-es="Cada casa firma con el logotipo Velum y su '
             'nombre. Nunca se crea un logotipo nuevo por sector." data-en="Every house signs with the Velum '
             'logotype and its own name. No new logo is ever created per sector.">'
             'Cada casa firma con el logotipo Velum y su nombre. Nunca se crea un logotipo nuevo por sector.</p>')
    A.append('</section>')

    # ---------------- 3 logotipo
    A.append('<section id="logotipo">')
    A.append('<div class="eyebrow" data-es="Identidad" data-en="Identity">Identidad</div>')
    A.append('<h2 data-es="El logotipo" data-en="The logotype">El logotipo</h2>')
    A.append('<div class="rule-g"></div>')
    A.append('<div class="grid g4">')
    for bg, variant, es, en in [(GROUND, "velum-primary-light-bg", "Fondo hueso", "Bone ground"),
                                (INK, "velum-primary-dark-bg", "Fondo oscuro", "Dark ground"),
                                (CREAM, "velum-primary-azul", "Una tinta · azul", "One ink · blue"),
                                (INK, "velum-primary-oro", "Una tinta · oro", "One ink · gold")]:
        A.append('<figure><div class="logo-tile" style="background:%s">%s</div>'
                 '<figcaption data-es="%s" data-en="%s">%s</figcaption></figure>'
                 % (bg, logo_svg(variant), es, en, es))
    A.append('</div>')
    A.append('<div class="grid g2" style="margin-top:22px">')
    A.append('<div class="card"><h3 data-es="Área de respeto" data-en="Clear space">Área de respeto</h3>'
             '<p data-es="Ningún elemento invade el margen «x», igual a la altura de la estrella." '
             'data-en="No element enters the margin «x», equal to the height of the star.">'
             'Ningún elemento invade el margen «x», igual a la altura de la estrella.</p>'
             '<span class="pill">x = ★</span></div>')
    A.append('<div class="card"><h3 data-es="Tamaño mínimo" data-en="Minimum size">Tamaño mínimo</h3>'
             '<p>Principal · 180 px / 40 mm<br>Monograma · 32 px / 10 mm</p></div>')
    A.append('<div class="card"><h3 data-es="Nunca" data-en="Never">Nunca</h3>'
             '<p data-es="Deformar, rotar, recolorear, añadir sombra, separar los elementos o usarlo sobre '
             'fondos sin contraste." data-en="Distort, rotate, recolour, add shadow, separate the elements '
             'or place it on low-contrast grounds.">Deformar, rotar, recolorear, añadir sombra, separar los '
             'elementos o usarlo sobre fondos sin contraste.</p></div>')
    A.append('<div class="card"><h3 data-es="Es un dibujo" data-en="It is artwork">Es un dibujo</h3>'
             '<p data-es="El trazo no existe en ninguna tipografía. Se coloca siempre el vector maestro, '
             'nunca se re-escribe." data-en="The stroke exists in no typeface. Always place the master '
             'vector; never re-type it.">El trazo no existe en ninguna tipografía. Se coloca siempre el '
             'vector maestro, nunca se re-escribe.</p></div>')
    A.append('</div></section>')

    # ---------------- 4 color
    A.append('<section id="color">')
    A.append('<div class="eyebrow" data-es="Color" data-en="Colour">Color</div>')
    A.append('<h2 data-es="Hueso, azul y oro" data-en="Bone, blue and gold">Hueso, azul y oro</h2>')
    A.append('<div class="rule-g"></div>')
    A.append('<p class="lead" data-es="Nueve tokens. Toca un color para copiar su HEX." '
             'data-en="Nine tokens. Tap a colour to copy its HEX.">Nueve tokens. Toca un color para copiar '
             'su HEX.</p>')
    A.append('<div class="grid g4" style="margin-top:26px">')
    for es, en, hx, ues, uen in PAL:
        A.append('<button class="sw" data-hex="%s"><span class="chip" style="background:%s"></span>'
                 '<span class="meta"><span class="nm" data-es="%s" data-en="%s">%s</span><br>'
                 '<span class="hex">%s</span><br><span class="hex" data-es="%s" data-en="%s">%s</span>'
                 '</span></button>' % (hx, hx, es, en, es, hx, ues, uen, ues))
    A.append('</div>')
    A.append('<h3 style="margin-top:40px" data-es="Proporción" data-en="Proportion">Proporción</h3>')
    A.append('<div class="bar-prop">')
    for pc, hx in ((60, GROUND), (22, INK), (10, CREAM), (5, GOLD), (3, NAVY)):
        A.append('<i style="background:%s;width:%d%%"></i>' % (hx, pc))
    A.append('</div>')
    A.append('<p class="small" data-es="60% hueso · 22% azul · 10% crema · 5% oro · 3% azul medio. '
             'El oro aparece una sola vez por pieza." data-en="60% bone · 22% blue · 10% cream · 5% gold · '
             '3% mid blue. Gold appears once per piece.">60% hueso · 22% azul · 10% crema · 5% oro · '
             '3% azul medio. El oro aparece una sola vez por pieza.</p>')
    A.append('<p class="small" style="color:var(--amber)" data-es="El Oro Velum no pasa AA como texto sobre '
             'hueso (2.0:1). Para texto sobre fondo claro se usa Oro Oscuro #B8912B." '
             'data-en="Velum Gold fails AA as text on bone (2.0:1). For text on a light ground use '
             'Deep Gold #B8912B.">El Oro Velum no pasa AA como texto sobre hueso (2.0:1). Para texto sobre '
             'fondo claro se usa Oro Oscuro #B8912B.</p>')
    A.append('</section>')

    # ---------------- 5 tipografía
    A.append('<section id="tipografia">')
    A.append('<div class="eyebrow" data-es="Tipografía" data-en="Typography">Tipografía</div>')
    A.append('<h2 data-es="Permanencia y claridad" data-en="Permanence and clarity">Permanencia y claridad</h2>')
    A.append('<div class="rule-g"></div>')
    A.append('<div class="grid g2">')
    A.append('<div class="spec"><div class="aa" style="font-family:var(--display)">Aa</div>'
             '<h3>Cinzel Display</h3><p class="small" data-es="Marca y titulares. Solo versales, '
             'tracking +2 a +4. Nunca texto corrido." data-en="Brand and headlines. Capitals only, '
             'tracking +2 to +4. Never body text.">Marca y titulares. Solo versales, tracking +2 a +4. '
             'Nunca texto corrido.</p><div class="set" style="font-family:var(--display)">'
             'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ 0123456789</div></div>')
    A.append('<div class="spec"><div class="aa" style="font-family:var(--sans);font-weight:300">Aa</div>'
             '<h3>Montserrat</h3><p class="small" data-es="Cuerpo, etiquetas, interfaz y datos. '
             'Light · Regular · Medium · SemiBold." data-en="Body, labels, interface and data. '
             'Light · Regular · Medium · SemiBold.">Cuerpo, etiquetas, interfaz y datos. '
             'Light · Regular · Medium · SemiBold.</p><div class="set">'
             'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ abcdefghijklmnñopqrstuvwxyz 0123456789</div></div>')
    A.append('</div>')
    A.append('<table><thead><tr>'
             '<th data-es="Función" data-en="Role">Función</th>'
             '<th data-es="Familia" data-en="Family">Familia</th>'
             '<th data-es="Tamaño" data-en="Size">Tamaño</th>'
             '<th>Tracking</th></tr></thead><tbody>')
    for r in [("Display", "Cinzel Display 400", "92 / 104", "+4"),
              ("Titular 1", "Cinzel Display 400", "52 / 60", "+2.5"),
              ("Titular 2", "Cinzel Display 400", "30 / 38", "+2"),
              ("Etiqueta", "Montserrat SemiBold", "11 / 16", "+3.4"),
              ("Cuerpo", "Montserrat Regular", "17 / 30", "0"),
              ("Pie", "Montserrat Light", "12 / 18", "+0.2")]:
        A.append("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>")
    A.append('</tbody></table></section>')

    # ---------------- 6 velo + texturas
    A.append('<section id="velo">')
    A.append('<div class="eyebrow" data-es="Elemento gráfico" data-en="Graphic device">Elemento gráfico</div>')
    A.append('<h2 data-es="Un solo gesto, seis lecturas" data-en="One gesture, six readings">'
             'Un solo gesto, seis lecturas</h2>')
    A.append('<div class="rule-g"></div>')
    A.append('<div class="card" style="padding:0;border:1px solid var(--line);background:var(--surface)">%s</div>'
             % veil_svg(INK, 0.6, 11))
    A.append('<p class="small" style="margin-top:14px" data-es="Rutas de vuelo, difusión del aroma, rutas '
             'globales, trayectorias de movimiento: mismo ADN, distinta lectura." data-en="Flight paths, '
             'scent diffusion, global routes, movement trajectories: same DNA, different reading.">'
             'Rutas de vuelo, difusión del aroma, rutas globales, trayectorias de movimiento: mismo ADN, '
             'distinta lectura.</p>')
    A.append('<h3 style="margin-top:44px" data-es="Texturas" data-en="Textures">Texturas</h3>')
    A.append('<p class="lead" data-es="Lo pétreo sostiene la marca: superficie dura, inamovible, y una '
             'mirada amplia. El espacio exterior se lee como geología, nunca como ilustración." '
             'data-en="Stone holds the brand up: a hard, unmovable surface and a wide view. Outer space is '
             'read as geology, never as illustration.">Lo pétreo sostiene la marca: superficie dura, '
             'inamovible, y una mirada amplia. El espacio exterior se lee como geología, nunca como '
             'ilustración.</p>')
    A.append('<div class="grid g4" style="margin-top:22px">')
    for fn, es, en in TEXTURES:
        A.append('<figure><img src="%s" alt=""><figcaption data-es="%s" data-en="%s">%s</figcaption></figure>'
                 % (tex(fn), es, en, es))
    A.append('</div></section>')

    # ---------------- 6b fotografía
    A.append('<section id="fotografia">')
    A.append('<div class="eyebrow" data-es="Dirección de fotografía" data-en="Photography direction">'
             'Dirección de fotografía</div>')
    A.append('<h2 data-es="La mirada hacia arriba" data-en="The upward gaze">La mirada hacia arriba</h2>')
    A.append('<div class="rule-g"></div>')
    A.append('<p class="lead" data-es="Velum no es una compañía de viajes: es la casa madre de seis '
             'negocios distintos. Por eso la fotografía no es un catálogo de temas, sino una misma forma '
             'de mirar aplicada a todos ellos." data-en="Velum is not a travel company: it is the parent '
             'house of six different businesses. So the photography is not a catalogue of subjects but one '
             'way of looking, applied to all of them.">Velum no es una compañía de viajes: es la casa madre '
             'de seis negocios distintos. Por eso la fotografía no es un catálogo de temas, sino una misma '
             'forma de mirar aplicada a todos ellos.</p>')
    A.append('<div class="hero-shot" style="margin-top:26px"><img src="%s" alt="">'
             '<div class="tag"><span class="k" data-es="Referencia madre" data-en="Parent reference">'
             'Referencia madre</span><br><span class="v" data-es="Si una foto se puede describir sin decir '
             'el sector, está bien hecha." data-en="If a frame can be described without naming the sector, '
             'it works.">Si una foto se puede describir sin decir el sector, está bien hecha.</span>'
             '</div></div>'
             % jpg(KIT + "/07_Photography/References/velum-foto-01-travel-avion-contrapicado.png", w=1200, q=78))

    A.append('<h3 style="margin-top:44px" data-es="Los siete principios" data-en="The seven principles">'
             'Los siete principios</h3>')
    A.append('<div class="grid g4" style="margin-top:20px">')
    for num, es, en, des, den in PRINCIPLES:
        A.append('<div class="card"><div class="pnum">%s</div>'
                 '<h3 style="margin:6px 0 8px" data-es="%s" data-en="%s">%s</h3>'
                 '<p data-es="%s" data-en="%s">%s</p></div>' % (num, es, en, es, des, den, des))
    A.append('</div>')

    A.append('<h3 style="margin-top:44px" data-es="Qué fotografía cada casa" '
             'data-en="What each house photographs">Qué fotografía cada casa</h3>')
    A.append('<p class="small" data-es="La gramática no cambia; cambia el sujeto." '
             'data-en="The grammar does not change; the subject does.">'
             'La gramática no cambia; cambia el sujeto.</p>')
    A.append('<div class="subj">')
    for name, es, en in SUBJECTS:
        A.append('<div><span class="h">%s</span><br><span class="s" data-es="%s" data-en="%s">%s</span></div>'
                 % (name, es, en, es))
    A.append('</div>')
    A.append('<p class="rule-line" data-es="Tres tomas por casa en cada sesión: mirada · materia · umbral" '
             'data-en="Three frames per house on every shoot: gaze · matter · threshold">'
             'Tres tomas por casa en cada sesión: mirada · materia · umbral</p>')

    A.append('<div class="two">')
    A.append('<div><div class="eyebrow" data-es="Buscamos" data-en="We look for">Buscamos</div><ul>')
    for es, en in PH_YES:
        A.append('<li data-es="%s" data-en="%s">%s</li>' % (es, en, es))
    A.append('</ul></div>')
    A.append('<div><div class="eyebrow" style="color:#8C5A3C" data-es="Evitamos" data-en="We avoid">'
             'Evitamos</div><ul>')
    for es, en in PH_NO:
        A.append('<li data-es="%s" data-en="%s">%s</li>' % (es, en, es))
    A.append('</ul></div>')
    A.append('<div><div class="eyebrow" data-es="Ficha técnica" data-en="Technical spec">Ficha técnica</div>'
             '<table style="margin-top:6px"><tbody>')
    for k, es, en in PH_SPEC:
        A.append('<tr><td>%s</td><td data-es="%s" data-en="%s">%s</td></tr>' % (k, es, en, es))
    A.append('</tbody></table></div>')
    A.append('</div>')

    A.append('<h3 style="margin-top:44px" data-es="Referencias aprobadas" data-en="Approved references">'
             'Referencias aprobadas</h3>')
    A.append('<p class="small" data-es="Catálogo completo con su principio y su casa en '
             '07_Photography/References/INDEX.md." data-en="Full catalogue with principle and house in '
             '07_Photography/References/INDEX.md.">Catálogo completo con su principio y su casa en '
             '07_Photography/References/INDEX.md.</p>')
    A.append('<div class="grid g4" style="margin-top:18px">')
    for fn, es, en in REFS:
        A.append('<figure><img src="%s" alt="" style="height:190px;object-fit:cover">'
                 '<figcaption data-es="%s" data-en="%s">%s</figcaption></figure>'
                 % (jpg(KIT + "/07_Photography/References/" + fn, w=520, q=74), es, en, es))
    A.append('</div>')
    A.append('<div class="card" style="margin-top:30px;background:var(--surface-2)">'
             '<h3 data-es="El logotipo sobre foto" data-en="The logotype over photography">'
             'El logotipo sobre foto</h3>'
             '<p data-es="Zona más limpia y oscura del encuadre, nunca sobre el sujeto. Una sola tinta: '
             'blanco sobre imagen oscura, azul sobre clara. Sin caja de fondo — se cambia el encuadre o se '
             'usa un degradado del propio azul al 40–60%. Área «x» completa. Una imagen lleva logotipo o '
             'texto, no ambos." data-en="The cleanest, darkest area of the frame, never over the subject. '
             'One ink: white on a dark image, blue on a light one. No background box — change the frame or '
             'use a gradient of the blue itself at 40–60%. Full «x» clear space. An image carries a '
             'logotype or a line of text, not both.">Zona más limpia y oscura del encuadre, nunca sobre el '
             'sujeto. Una sola tinta: blanco sobre imagen oscura, azul sobre clara. Sin caja de fondo — se '
             'cambia el encuadre o se usa un degradado del propio azul al 40–60%. Área «x» completa. Una '
             'imagen lleva logotipo o texto, no ambos.</p></div>')

    A.append('<div class="dl" style="margin-top:26px">')
    for href, es, en, meta in [
            ("../07_Photography/FOTOGRAFIA.md", "Guía completa (ES)", "Full guide (ES)", "Markdown"),
            ("../07_Photography/PHOTOGRAPHY-EN.md", "Guía completa (EN)", "Full guide (EN)", "Markdown"),
            ("../07_Photography/velum-photography-board.png", "Tablero de dirección", "Direction board",
             "PNG · 2000×2700"),
            ("../07_Photography/Prompts/", "Prompts de imagen generada", "Generated-image prompts",
             "ES · EN")]:
        A.append('<a href="%s"><span class="k" data-es="%s" data-en="%s">%s</span><br>'
                 '<span class="v">%s</span></a>' % (href, es, en, es, meta))
    A.append('</div></section>')

    # ---------------- 7 aplicaciones
    A.append('<section id="aplicaciones">')
    A.append('<div class="eyebrow" data-es="Aplicaciones" data-en="Applications">Aplicaciones</div>')
    A.append('<h2 data-es="La marca en el mundo" data-en="The brand out in the world">La marca en el mundo</h2>')
    A.append('<div class="rule-g"></div>')
    A.append('<div class="pages">')
    for num, es, en in [(34, "Papelería", "Stationery"), (35, "Digital", "Digital"),
                        (31, "Texturas", "Textures"), (11, "Las seis casas", "The six houses")]:
        A.append('<figure><img src="%s" alt=""><figcaption data-es="%s" data-en="%s">%s</figcaption></figure>'
                 % (page_png("ES", num), es, en, es))
    A.append('</div></section>')

    # ---------------- 8 descargas
    A.append('<section id="descargas">')
    A.append('<div class="eyebrow" data-es="Descargas" data-en="Downloads">Descargas</div>')
    A.append('<h2 data-es="El kit completo" data-en="The complete kit">El kit completo</h2>')
    A.append('<div class="rule-g"></div>')
    A.append('<div class="dl">')
    dl = [("VELUM_Manual_de_Marca_ES.pdf", "Manual de marca (ES)", "Brand guidelines (ES)", "PDF · 36 pp"),
          ("VELUM_Brand_Guidelines_EN.pdf", "Manual de marca (EN)", "Brand guidelines (EN)", "PDF · 36 pp"),
          ("VELUM_Manual_de_Marca_ES.pptx", "Presentación (ES)", "Deck (ES)", "PPTX · 16:9"),
          ("VELUM_Brand_Guidelines_EN.pptx", "Presentación (EN)", "Deck (EN)", "PPTX · 16:9"),
          ("SVG_ES/", "Páginas en SVG (ES)", "Page SVGs (ES)", "Figma-ready"),
          ("SVG_EN/", "Páginas en SVG (EN)", "Page SVGs (EN)", "Figma-ready"),
          ("../01_Logo/", "Logotipos", "Logotypes", "SVG · PNG · Favicon"),
          ("../02_Color/", "Color", "Colour", "MD · CSS · SCSS · JSON"),
          ("../03_Type/", "Tipografía", "Typography", "MD · Fonts"),
          ("../05_Textures/", "Texturas", "Textures", "JPG · SVG"),
          ("../07_Photography/", "Fotografía", "Photography", "Guía · Prompts · Board"),
          ("../06_Elements/", "Elementos", "Elements", "SVG"),
          ("../00_Brand-Board/velum-brand-board.svg", "Brand board", "Brand board", "SVG · 2000×2700")]
    for href, es, en, meta in dl:
        A.append('<a href="%s"><span class="k" data-es="%s" data-en="%s">%s</span><br>'
                 '<span class="v">%s</span></a>' % (href, es, en, es, meta))
    A.append('</div></section>')

    A.append('</main>')
    A.append('<footer><div class="wrap">'
             '<span data-es="VELUM Enterprise · Manual de marca 1.0 · 2026" '
             'data-en="VELUM Enterprise · Brand guidelines 1.0 · 2026">'
             'VELUM Enterprise · Manual de marca 1.0 · 2026</span></div></footer>')
    A.append('<div class="copied" id="copied">Copiado</div>')

    A.append("""<script>
(function(){
  var lang = localStorage.getItem('velum-lang') || 'es';
  function apply(l){
    lang = l;
    document.documentElement.lang = l;
    document.querySelectorAll('[data-es]').forEach(function(el){
      var v = el.getAttribute('data-' + l);
      if (v !== null) el.textContent = v;
    });
    document.querySelectorAll('.lang button').forEach(function(b){
      b.setAttribute('aria-pressed', b.dataset.lang === l ? 'true' : 'false');
    });
    try { localStorage.setItem('velum-lang', l); } catch(e){}
  }
  document.querySelectorAll('.lang button').forEach(function(b){
    b.addEventListener('click', function(){ apply(b.dataset.lang); });
  });
  apply(lang);

  var note = document.getElementById('copied');
  document.querySelectorAll('.sw').forEach(function(sw){
    sw.addEventListener('click', function(){
      var hex = sw.dataset.hex;
      var done = function(){
        note.textContent = (lang === 'es' ? 'Copiado ' : 'Copied ') + hex;
        note.classList.add('on');
        setTimeout(function(){ note.classList.remove('on'); }, 1400);
      };
      if (navigator.clipboard) { navigator.clipboard.writeText(hex).then(done, done); }
      else { done(); }
    });
  });
})();
</script>""")

    html = "\n".join(A)
    open(OUT, "w", encoding="utf-8").write(html)
    print(OUT, os.path.getsize(OUT) // 1024, "KB")

if __name__ == "__main__":
    build()
