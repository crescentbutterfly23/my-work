# Project Design System Template

Every project can carry its own brand style. When you fill these fields in the
Studio (or in `site/data/projects.json` for built-in projects), the project's
story page dresses itself in that brand: background, accent color, text color
and heading font. The Crescent Butterfly header and footer always stay in your
studio brand, so the page reads as "your studio presenting their brand."

## The template

Copy this, fill it in from the client's brand guidelines, then enter the values
in the Studio's "Design system" panel when you create or edit the project:

```json
{
  "theme": {
    "background": "#fdf6f8",
    "surface":    "#ffffff",
    "accent":     "#ba132f",
    "text":       "#7d1128",
    "headingFont": "Poppins",
    "bodyFont":    "Poppins"
  }
}
```

## What each field controls

| Field | What it styles | How to pick it |
|---|---|---|
| `background` | The page background behind the whole story | The brand's lightest field color (paper, cream, mist). Must be light enough for text to pass contrast. |
| `surface` | Cards and the closing call-to-action panel | A tint one step deeper than the background. |
| `accent` | Project title, opening paragraph, links, small rules | The brand's signature color. Used sparingly, exactly like crimson in your own brand. |
| `text` | Body copy | The brand's darkest reading color. Aim for WCAG AA (4.5:1) against `background`. |
| `headingFont` | The project title and headings | A Google Fonts family name, spelled exactly as on fonts.google.com (e.g. `Playfair Display`, `DM Serif Display`, `Archivo`). |
| `bodyFont` | Paragraph text | Usually the brand's workhorse sans. Leave empty to keep Poppins. |

## Rules of thumb

1. **All colors are 6-digit hex** (`#a1b2c3`). Shorthand or rgb() won't apply.
2. **Leave any field empty to inherit** the Crescent Butterfly default, so a
   partial design system is fine.
3. **Fonts load from Google Fonts.** If the client uses a font that isn't
   there, choose the closest Google alternative and note the substitution in
   the project story.
4. **Contrast is on you:** the studio doesn't block low-contrast combinations.
   Check `text` on `background` and white on `accent` before publishing.
5. Screenshots of the client's palette and type specimens make great image
   blocks in the presentation itself. The theme sets the mood; the blocks show
   the receipts.
