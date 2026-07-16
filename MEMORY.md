---
schemaVersion: 1
scope: workspace
updatedAt: "2026-07-13T23:01:11.888Z"
workspaceName: "Website"
---

# Project Memory

## Project Overview
- Workspace for the index page visual/web prototype titled “Butterfly Icon Header Animation.”
- Goal: replace a collage-style hero visual with an embossed butterfly logo/icon that zooms in, takes over the page during scroll, then shrinks into the header.

## Current State
- `App.jsx` exists as the original React implementation for the butterfly animation page.
- Root `index.html` now incorporates the same butterfly takeover animation as a standalone HTML implementation.
- The standalone page preserves the original warm editorial style of the existing elements, including header treatment, buttons, spacing, and visual tone.
- The page includes a scroll-driven butterfly transformation and was verified with no runtime or syntactic issues.
- The butterfly’s initial/resting position sits below the hero text/buttons before scrolling and does not overlap the controls.
- `index.html` exposes tweak controls for butterfly hue, zoom scale, emboss depth, and header scale.
- `DESIGN.md` exists and is the authoritative design-system artifact.

## Artifacts
- `index.html` — standalone index page implementation with embossed SVG butterfly, preserved hero/header styling, scroll progress behavior, and tweakable animation values.
- `App.jsx` — React version/source candidate for the animated index page, including embossed SVG butterfly, hero layout, scroll progress behavior, and styling.
- `DESIGN.md` — project design baton/tokens for the butterfly animation page; authoritative design-system artifact.

## Design Direction
- Premium embossed butterfly mark replaces the collage visual.
- Animation path: starts below hero content, zooms into a page takeover moment on scroll, then resolves smaller into the header.
- Visual tone is polished, dimensional, and brand-mark focused rather than collage-heavy.
- Preserve the original style of page elements while swapping in the butterfly animation.
- Typography is local/system-based rather than relying on external font loading.

## User Feedback
- User specifically requested the butterfly icon from the logo with embossed styling.
- User requested it replace the collage, zoom in/take over the page, then become small and turn into the header.
- User emphasized that before scrolling, the butterfly should not be overlapped by text or buttons and should sit below them.
- User asked to incorporate the animation into `index.html`.
- User asked to make sure the original style of the elements is kept.
- User needed clarification on where the implementation changes were located.

## Decisions
- Implemented the butterfly as an inline SVG mark with embossed styling.
- Added tweakable controls for key animation/visual parameters.
- Adjusted initial butterfly placement responsively to avoid hero copy and button overlap.
- Converted the React prototype behavior into standalone root `index.html`.
- Preserved the warm editorial visual style when porting to `index.html`.
- Added/updated `DESIGN.md` as the authoritative design-system artifact.

## Open Questions
- Whether the butterfly should become a persistent header logo on all pages or only this index page.
- Whether final brand assets should replace the inline SVG approximation.
- Exact production scroll timing and header handoff behavior may need review on real content.
- Whether `App.jsx` should remain alongside `index.html` or be deprecated after the HTML version is accepted.

## Next Steps
- Review/preview `index.html` in browser at target viewport sizes.
- Replace the SVG approximation with official logo artwork if available.
- Fine-tune scroll thresholds, zoom scale, and final header size after stakeholder review.
- Decide whether to keep both `App.jsx` and `index.html` or consolidate around one implementation.

## Promotion Candidates For DESIGN.md
- Embossed butterfly logo as the primary brand animation mark.
- Scroll sequence: resting below hero content → zoom takeover → compact header mark.
- Requirement that pre-scroll hero CTAs/text never overlap the butterfly.
- Preserving the original warm editorial element styling during animation changes.
- Local/system typography approach if retained for production.
- Tweakable animation controls: butterfly hue, zoom scale, emboss depth, and header scale.

## Recent History
- 2026-07-13: Created `App.jsx` for the index page butterfly header animation.
- 2026-07-13: Adjusted resting butterfly placement to avoid overlap with hero text/buttons.
- 2026-07-13: Removed external font loading and used local/system typography.
- 2026-07-13: Added minimal `DESIGN.md` and verified the design successfully.
- 2026-07-13: Clarified that the changes were located in `App.jsx` and `DESIGN.md`.
- 2026-07-13: Incorporated the butterfly takeover animation into standalone root `index.html`.
- 2026-07-13: Preserved original element styling while porting the animation to `index.html`.
- 2026-07-13: Verified `index.html` with no syntactic or runtime issues.