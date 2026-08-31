# AnaLopez - Typography

Three families. The logotype is a fourth thing: artwork, not a font.

## 1. Logotype - locked artwork, never re-typed

The AnaLopez logotype is a **custom drawing**. It is built from **Italiana Regular**
letterforms with the terminal **z** replaced by the swash **z** of **Bodoni Moda Italic**.
The two are merged and redrawn so the swash resolves into the baseline.

Never reproduce it by typing "AnaLopez" in Italiana - the swash will be missing and the
fit will be wrong. Always place the supplied vector from `01_Logo/SVG/`.

The descriptor locked beneath it is **Poppins ExtraLight**, tracked to **0.30 em**.
It is part of the artwork; it is not re-set.

## 2. Bodoni Moda - display and editorial

Headlines, collection names, pull quotes, campaign lines. It is also the source of the
logotype's swash z, which is why it belongs in the system.

- Variable axes: `opsz` 6-96, `wght` 400-900. Roman and Italic.
- Set large. Below ~18 px the hairlines break up - use Poppins instead.
- Tracking: -2% at display sizes, -1% at 36-48 px, 0 at 24-32 px.

## 3. Poppins - support

Everything functional: labels, navigation, ingredient lists, back-of-pack, body copy,
UI. Weights in use: **200 ExtraLight** (descriptor and labels), **300 Light**,
**400 Regular** (body), **500 Medium** (inline emphasis).

## 4. Italiana - reserved

Reserved for the logotype. May be used for very large numerals or a single collection
title, at 40 px and up. Never for body copy: no bold, no true italic, very small x-height.

## Scale

| Role | Family | Size | Tracking |
|---|---|---|---|
| Campaign line | Bodoni Moda 400 | 48-96 px | -2% |
| Heading 1 | Bodoni Moda 400 | 36-48 px | -1% |
| Heading 2 | Bodoni Moda 500 | 24-32 px | 0 |
| Label / eyebrow | Poppins ExtraLight 200 | 11-13 px | +0.30 em, caps |
| Body | Poppins Regular 400 | 15-17 px / 1.7 | 0 |
| Caption and legal | Poppins Light 300 | 11-12 px / 1.5 | +0.02 em |

## Licensing

Italiana, Bodoni Moda and Poppins are all **SIL Open Font License** - free for print,
web, packaging and embedding. OFL texts are included beside each family in `Fonts/`.

Poppins was not present in `VELUM Enterprise/Font/` and has been added here
(weights 200/300/400/500). Install all three families before opening the guideline
decks or the Figma SVGs, or they will substitute.
