# VELUM — Prompts de imagen generada

La misma dirección de `FOTOGRAFIA.md`, escrita para un modelo de imagen. Los modelos responden
mejor en inglés, así que el bloque base va en inglés y la explicación en español. Se mantiene el
bloque intacto y **solo se cambia la frase del sujeto**: eso es lo que hace que seis negocios
distintos parezcan una sola marca.

---

## Bloque base

```
Low-angle photograph looking upward, camera positioned below the subject, tilted 30–45° toward
the sky. Strong backlight: the sun sits behind the subject, which reads as a near-silhouette with a
warm gold rim. Two thirds of the frame is empty air. A clear threshold in frame — horizon line,
roof edge, cloud rim. Deep navy shadows (#0B1D34), bone-white highlights (#F4F0EE), one single warm
gold accent (#D4AF37). Shot on a 24–35 mm lens at f/8, low ISO, exposed for the highlights. Fine
film grain, soft contrast curve, no HDR. Editorial, restrained, expensive.
```

**Qué dice, en corto:** cámara baja mirando hacia arriba · luz detrás del sujeto · silueta con
borde dorado · dos tercios de aire · un umbral visible · sombras azules y luces hueso · 24–35 mm a
f/8 · grano fino, sin HDR.

## Prompt negativo

```
planets, rocket, astronaut, galaxy, nebula, outer space illustration, sci-fi, neon, teal and orange
grading, HDR, oversaturated, replaced sky, lens flare overlay, posed people, smiling business team,
handshake, stock photo, watermark, text, logo, letters, collage, cluttered still life, top-down
drone view, flat white studio background, fisheye distortion, heavy vignette
```

---

## Por casa

Cada línea sustituye la **primera frase** del bloque base. Todo lo demás se mantiene.

### Velum Travel
```
Low-angle photograph of a commercial aircraft passing overhead, seen from directly below, wings
cutting across a sky of high scattered cloud.
```
*Avión en contrapicado puro contra cielo de nubes altas. La referencia madre.*

### AL — Ana López
```
Low-angle photograph of a single glass perfume bottle on a stone ledge, seen from just below the
ledge against a sunlit limewash wall, light passing through the amber liquid.
```
*Frasco desde abajo contra muro de cal; la luz atraviesa el líquido y deja el oro.*

### Velum Foods
```
Photograph taken at the level of a stone table, a single raw ingredient in the last third of the
frame, steam or flour dust catching the light from behind.
```
*Cámara al ras de la mesa de piedra; el vapor atrapa el contraluz.*

### Velum Trade
```
Low-angle photograph from the foot of a port crane, steel structure rising and converging against
an open dawn sky, a container edge entering the lower frame.
```
*La grúa como arquitectura, no como logística.*

### Velum Properties
```
Low-angle photograph of the corner of a modern stone building, vertical lines converging against
open sky, an empty doorway or opening visible as a threshold.
```
*La esquina contra el cielo; el vano como umbral literal.*

### Velum Mobility
```
Photograph taken almost at asphalt level, a single vehicle silhouetted against a low dawn sun,
coarse road aggregate sharp in the foreground.
```
*Casi al ras del asfalto; el árido nítido en primer término.*

---

## Texturas y superficies

Para fondos en lugar de escenas — estos alimentan `05_Textures`:

```
Macro photograph of raw concrete / fractured basalt / asphalt aggregate / bone-coloured stone slab,
flat even light, no subject, filling the frame edge to edge, deep navy and bone tones, fine grain,
no pattern repetition, no illustration.
```

---

## Proporciones

| Uso | Proporción |
|---|---|
| Mirada hacia arriba, portada | 4:5 o 2:3 vertical |
| Horizonte, banner web | 16:9 o 2:1 |
| Feed social | 1:1 (recortado desde 4:5, nunca generado cuadrado) |
| Página a sangre del manual | 16:9 |

---

## Método de trabajo

1. Generar **cuatro variantes** del mismo prompt y elegir una. Resistirse a quedarse con tres.
2. Revisar manos, ventanillas, ruedas, reflejos y cualquier texto insinuado por si hay deformación.
3. Ajustar a la paleta: punto negro en `#0B1D34`, punto blanco en `#F4F0EE`, un solo acento cálido.
4. Guardar la imagen en `References/` con su prompt en el nombre o en un `.txt` al lado.
5. Componer la tipografía después, en Cinzel y Montserrat. El modelo nunca escribe palabras.
