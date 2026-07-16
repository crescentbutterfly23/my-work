# Crescent Butterfly

The website for **Crescent Butterfly Graphic Design** — Natalie Cruz Serrat.
Static site, no build step, deployed on GitHub Pages.

## Running locally

The pages fetch `data/projects.json`, so opening the HTML directly with `file://`
won't work. Serve the folder instead:

```bash
python -m http.server 8000
# then open http://localhost:8000
```

## Structure

```
index.html          home  (the "cut paper" zine theme — current default)
work.html           project index + category filters
services.html       services + process
start.html          the guided project brief
project.html        case-study page  (project.html?id=…)
styles.css          the whole design system
shared.js           icon sprite, reveals, sketch animation, project loading
data/projects.json  every project on the site
assets/             logo, illustrations, project images
```

### Theme variants

Two alternate directions live alongside the default while a final look is chosen:

| files | direction |
|---|---|
| `index.html`, `work.html`, `services.html`, `start.html`, `project.html` | **Cut-paper zine** (default) |
| `*-editorial.html` + `css/editorial.css` | Editorial / Fraunces serif |
| `*-corporate.html` + `css/corporate.css` | Corporate / Space Grotesk |

Once a direction is picked, the winner should be promoted to the canonical
filenames and the other two sets deleted.

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

## Notes / gotchas

- **No backend.** GitHub Pages is static only. The "Start a project" brief is
  composed into a `mailto:` and sent from the visitor's own mail client.
- `loadProjects()` still tries `/api/projects` first and falls back to
  `data/projects.json`, so it works with or without a server.
- `admin.html` is **non-functional here** — it needed the old Netlify functions
  and database.
- Motion respects `prefers-reduced-motion`: sketches render fully drawn and
  static rather than animating.

## Credits

Design and code: Natalie Cruz Serrat — [behance.net/crescentbutterfly](https://www.behance.net/crescentbutterfly)
