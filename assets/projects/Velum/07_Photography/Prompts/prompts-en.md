# VELUM — Image generation prompts

The same direction as `PHOTOGRAPHY-EN.md`, written for an image model. Keep the base block intact
and swap only the subject line: that is what keeps six different businesses looking like one brand.

---

## Base block

```
Low-angle photograph looking upward, camera positioned below the subject, tilted 30–45° toward
the sky. Strong backlight: the sun sits behind the subject, which reads as a near-silhouette with a
warm gold rim. Two thirds of the frame is empty air. A clear threshold in frame — horizon line,
roof edge, cloud rim. Deep navy shadows (#0B1D34), bone-white highlights (#F4F0EE), one single warm
gold accent (#D4AF37). Shot on a 24–35 mm lens at f/8, low ISO, exposed for the highlights. Fine
film grain, soft contrast curve, no HDR. Editorial, restrained, expensive.
```

## Negative prompt

```
planets, rocket, astronaut, galaxy, nebula, outer space illustration, sci-fi, neon, teal and orange
grading, HDR, oversaturated, replaced sky, lens flare overlay, posed people, smiling business team,
handshake, stock photo, watermark, text, logo, letters, collage, cluttered still life, top-down
drone view, flat white studio background, fisheye distortion, heavy vignette
```

---

## Per house

Each line replaces the first sentence of the base block. Keep everything after it.

### Velum Travel
```
Low-angle photograph of a commercial aircraft passing overhead, seen from directly below, wings
cutting across a sky of high scattered cloud.
```

### AL — Ana López
```
Low-angle photograph of a single glass perfume bottle on a stone ledge, seen from just below the
ledge against a sunlit limewash wall, light passing through the amber liquid.
```

### Velum Foods
```
Photograph taken at the level of a stone table, a single raw ingredient in the last third of the
frame, steam or flour dust catching the light from behind.
```

### Velum Trade
```
Low-angle photograph from the foot of a port crane, steel structure rising and converging against
an open dawn sky, a container edge entering the lower frame.
```

### Velum Properties
```
Low-angle photograph of the corner of a modern stone building, vertical lines converging against
open sky, an empty doorway or opening visible as a threshold.
```

### Velum Mobility
```
Photograph taken almost at asphalt level, a single vehicle silhouetted against a low dawn sun,
coarse road aggregate sharp in the foreground.
```

---

## Textures and grounds

For backgrounds rather than scenes — these feed `05_Textures`:

```
Macro photograph of raw concrete / fractured basalt / asphalt aggregate / bone-coloured stone slab,
flat even light, no subject, filling the frame edge to edge, deep navy and bone tones, fine grain,
no pattern repetition, no illustration.
```

---

## Aspect ratios

| Use | Ratio |
|---|---|
| Upward gaze, hero | 4:5 or 2:3 vertical |
| Horizon, web banner | 16:9 or 2:1 |
| Social feed | 1:1 (crop from 4:5, never generate square first) |
| Deck full-bleed page | 16:9 |

---

## Working method

1. Generate **four variants** of the same prompt; choose one. Resist the urge to keep three.
2. Check hands, windows, wheels, reflections and any implied text for deformation.
3. Grade to the palette: black point at `#0B1D34`, white point at `#F4F0EE`, one warm accent.
4. Save the image to `References/` with its prompt in the filename or a sidecar `.txt`.
5. Set all type afterwards, in Cinzel and Montserrat. Never let the model write words.
