# Mockup Library — web edition

A travelling copy of the studio mockup index: 1,000 free, commercially-usable mockups with
preview thumbnails, filterable by category, source, style, business type, setting and
customization level.

Open it at `mockups/index.html` — or from the **🖼 Mockup library** button on the Studio Desk.

## How this differs from the copy on the studio drive

- **No Have / Need status.** No badges, no status filter, no on-disk detection. This copy is
  a browsing index, not an inventory — inventory only means something next to the actual files.
- **Every row links out to its download page.** Nothing points at a local file path, including
  the two mockups already filed on the drive.
- **Thumbnails are downscaled** to 520 px wide (~24 MB total instead of 106 MB) so the repo
  stays reasonable. Cards display at ~258 px, so they still look sharp on a retina screen.

## Sources

| Source | License | Catch |
|---|---|---|
| Mr.Mockup | Free, personal + commercial | Download button on each page |
| MockupTree | Free, personal + commercial | Free cart/checkout, email may be needed |
| Magnific (Freepik) | Free **only with attribution** | Free account required; most of their mockups are Premium |

**Magnific attribution is mandatory.** Their free license allows commercial use only if
"Designed by Magnific" plus a link to www.magnific.com appears visibly on the finished piece.
The library footer carries that credit; it has to travel onto any client work too. Only
free-license items are indexed — their Premium mockups need a paid subscription.

## Downloads

Neither source allows a direct-file link — Mr.Mockup puts a download button on each product
page, MockupTree routes through a free cart/checkout. So **“Go to download” lands on the page
holding the PSD**, one click from the file.

## Finishes

A **finishes** filter covers print treatments — Spot UV, emboss, deboss, letterpress,
foil stamp, die cut, varnish, engraving, kraft/uncoated, textured stock.

Two things feed it, and the hand-curated one is the important half:

1. **Keyword guess.** If a title literally says "Embossed Business Card", it gets tagged.
   Restricted to print categories, so "Matte Lipstick" and "Metallic Food Pouch" are not
   mistaken for print finishes. This only catches **11 of 1,009** — source titles almost
   never mention finishes, and nothing in the catalog says spot UV, letterpress or die cut.
2. **`FINISHES` in `mockup-data.js`.** A map of `url -> finish`, hand-edited, which always
   wins over the guess. This is where the filter actually becomes useful: when you open a
   PSD and see what it supports, record it and it stays filterable.

The map is not limited to print categories — tag an apparel mockup "Screen print" or
"Embroidery" and it works, and the label becomes a filter option automatically.

Unfinished entries are not given a made-up default; they show `—` and group under
**Not specified** in the filter.

## Updating

The catalog lives in `mockup-data.js` as rows of
`[title, url, category, subcategory, sourceIndex, optionalPreview]`. Thumbnails are looked up
at `thumbs/<mm|mt>-<slugified-url>.jpg`; a 6th element overrides that path.

To regenerate from the studio-drive copy, re-derive it from
`Mockups/_Guide/mockup-data.js`: drop the `ON_DISK` block and the “Local library” source, and
repoint any local-path rows at their source page.
