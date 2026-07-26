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

## Downloads

Neither source allows a direct-file link — Mr.Mockup puts a download button on each product
page, MockupTree routes through a free cart/checkout. So **“Go to download” lands on the page
holding the PSD**, one click from the file.

## Updating

The catalog lives in `mockup-data.js` as rows of
`[title, url, category, subcategory, sourceIndex, optionalPreview]`. Thumbnails are looked up
at `thumbs/<mm|mt>-<slugified-url>.jpg`; a 6th element overrides that path.

To regenerate from the studio-drive copy, re-derive it from
`Mockups/_Guide/mockup-data.js`: drop the `ON_DISK` block and the “Local library” source, and
repoint any local-path rows at their source page.
