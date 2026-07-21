# Crescent Butterfly

**→ [crescentbutterfly23.github.io/my-work](https://crescentbutterfly23.github.io/my-work/)**

The website for **Crescent Butterfly Graphic Design** — Natalie Cruz Serrat.
Static site, no build step, deployed on GitHub Pages.

[![Behance](https://img.shields.io/badge/Behance-crescentbutterfly-1769ff?logo=behance&logoColor=white)](https://www.behance.net/crescentbutterfly)
[![Email](https://img.shields.io/badge/Email-crescentbutterfly23%40gmail.com-ba132f)](mailto:crescentbutterfly23@gmail.com)

## Deploying

Pushing to `main` publishes the site. GitHub Pages is configured under
**Settings → Pages → Deploy from a branch → `main` / (root)**.

The site is served from the `/my-work/` subpath, so **every path must stay
relative** (`assets/…`, not `/assets/…`) or it will 404 once deployed.

## Running locally

The pages fetch `data/projects.json`, so opening the HTML directly with `file://`
won't work. Serve the folder instead:

```bash
python -m http.server 8000
# then open http://localhost:8000
```

## Structure

```
index.html          home
work.html           project index + category filters
services.html       services + process
start.html          the guided project brief
project.html        case-study page  (project.html?id=…)

admin.html          the studio desk — every project, star, reorder
project-edit.html   focused editor for one project's page blocks
js/desk.js          shared draft store for those two

styles.css          the whole design system
shared.js           icon sprite, reveals, sketch animation, project loading
data/projects.json  every project on the site
assets/             logo + project images
```

The look is the **cut-paper zine** theme. Two alternate directions (editorial /
corporate) were explored and live in the working folder outside this repo —
they're deliberately not deployed.

## Projects

`data/projects.json` drives every project grid. Two shapes are supported:

- **External** — has a `url`, so the card links out to Behance.
- **Internal** — has `story` + `gallery`, so the card opens `project.html?id=…`.

```json
{
  "id": "my-project",
  "title": "My Project",
  "category": "Brand Identity",
  "year": "2025",
  "description": "One or two lines shown on the card.",
  "image": "assets/projects/behance/my-project.png",
  "url": "https://www.behance.net/gallery/…"
}
```

## Editing projects — `admin.html`

Run the site locally and open **`/admin.html`**. It lists every project, and lets you:

- **★ star** a project — starred ones show on the home page, the rest stay on `work.html`
- edit the title, category, year, description, image path and Behance link
- reorder, add and delete

It has no backend, so nothing saves by itself. When you're done hit
**Download projects.json**, drop it into `site/data/`, then commit and push —
that's what publishes the change.

### Client previews (unlisted + passcode)

Each project row has a **Client preview** panel for sharing a site with a client
before it's public:

- **Hide from the public site** — sets `unlisted`, so the project drops off the
  home and Work grids but stays in the Studio and reachable by direct link.
- **Live / preview link** — the site's URL (`previewUrl`). If set, `project.html`
  shows a "Visit the live site" button.
- **Passcode** — typing one stores its SHA-256 as `passcodeHash` (the plaintext is
  never saved). **Clear** removes it.

To lock the preview site itself, host it (a separate repo →
`https://crescentbutterfly23.github.io/<repo>/`, or a folder in this one →
`…/my-work/<folder>/`) and drop [`js/gate.js`](js/gate.js) beside its page:

```html
<body class="cb-locked">
  …your page…
  <script src="gate.js" data-hash="…"></script>
</body>
```

Hit **Copy gate snippet** in the Studio to get that `<script>` tag with the hash
filled in, then give the client the passcode separately.

**This is a casual gate, not real security** — GitHub Pages is always public, and
any client-side check can be bypassed with browser dev tools. It keeps a preview
out of casual view; never put anything genuinely sensitive behind it.

## Notes / gotchas

- **No backend.** GitHub Pages is static only. The "Start a project" brief is
  composed into a `mailto:` and sent from the visitor's own mail client.
- Motion respects `prefers-reduced-motion`: sketches render fully drawn and
  static rather than animating.
- Behance cover images are stored in `assets/projects/behance/` rather than
  hotlinked, so the site doesn't depend on Behance staying reachable.

## Credits

Design and code: Natalie Cruz Serrat — [behance.net/crescentbutterfly](https://www.behance.net/crescentbutterfly)
