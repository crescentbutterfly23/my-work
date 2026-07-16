---
version: alpha
name: Butterfly Icon Header Animation
---

## Overview

Warm editorial index-page motion system where an embossed butterfly logo replaces the collage visual, rests below the hero copy before scroll, expands into a page takeover, and resolves into the fixed header identity. `index.html` is the standalone page version; `App.jsx` remains the React prototype reference.

## colors

- `paper`: oklch(0.94 0.025 82) — warm page base.
- `cream`: oklch(0.89 0.045 82) — ambient gradient tone.
- `ink`: oklch(0.18 0.03 60) — primary text and dark actions.
- `muted`: oklch(0.45 0.04 63) — supporting copy.
- `line`: oklch(0.63 0.06 70 / .34) — soft dividers and button borders.
- `cocoa`: oklch(0.25 0.045 48) — header action surface.
- `butterflyHue`: oklch(0.62 0.13 55) — tweakable embossed wing color.

## typography

- UI: Avenir Next, Trebuchet MS, Segoe UI, sans-serif.
- Display: Georgia, Charter, serif.
- Hero headline: clamp(3.45rem, 9.8vw, 9.4rem), tight line-height, negative tracking.
- Body: 1.03rem–1.32rem with generous editorial line-height.

## rounded

- Pills: 999px for buttons and logo slot.
- Large panels: clamp(1.6rem, 3vw, 3rem).

## spacing

- Page gutters: clamp(1.2rem, 5vw, 5rem).
- Header padding: clamp(1rem, 2vw, 1.6rem) vertical.
- Hero gap: clamp(2rem, 7vw, 7rem).
- Content panel padding: clamp(1.4rem, 4vw, 4rem).

## components

- `ButterflyMark`: inline SVG logo with embossed filter, wing gradients, and accessible label.
- `site-header`: fixed translucent navigation with brand slot and pill actions.
- `hero`: sticky opening section; copy fades while the butterfly zooms.
- `content.panel`: frosted card explaining the three animation states.

## motion

- Resting: butterfly is positioned below and to the side of hero copy, not over buttons.
- Takeover: scale rises toward the tweakable zoom scale.
- Header settle: mark contracts toward the brand area using the tweakable header scale.

## tweak defaults

- `embossDepth`: 1.15
- `zoomScale`: 6.2
- `butterflyHue`: oklch(0.62 0.13 55)
- `headerScale`: 0.36
