/* ============================================================
   Crescent Butterfly — shared behavior
   icon sprite · year · active nav · reveals · project data
   ============================================================ */

/* ---- brand icons, hand-drawn for the cut-paper theme ----
   Flat fills + thick ink strokes. Use: <svg class="ic"><use href="#ic-moon"/></svg>
   Fills read CSS vars, so icons re-colour with the theme.            */
const ICON_SPRITE = `
<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true" focusable="false">
  <!-- moon + sparkle are SKETCHED: open outlines, overdrawn a second time, hatched -->
  <symbol id="ic-moon" viewBox="0 0 64 64">
    <path d="M41 4C21 6 6 21 6 39c0 13 10 21 24 21 9 0 17-4 22-11-18 5-33-6-33-23 0-10 8-19 22-22z"
          fill="none" stroke="var(--ink)" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>
    <path d="M38 9C22 12 10 24 11 39c1 11 9 17 19 17" fill="none" stroke="var(--ink)"
          stroke-width="1.5" stroke-linecap="round" opacity=".55"/>
    <path d="M15 27l10-7M14 35l13-9M17 43l12-8M23 49l9-6" stroke="var(--ink)" stroke-width="1.4"
          stroke-linecap="round" opacity=".45" fill="none"/>
    <circle cx="28" cy="16" r="2.1" fill="var(--ink)"/>
    <circle cx="20" cy="31" r="1.7" fill="var(--ink)"/>
  </symbol>

  <symbol id="ic-sparkle" viewBox="0 0 64 64">
    <path d="M32 3c2.5 15 13.5 26 29 29-15.5 3-26.5 14-29 29-2.5-15-13.5-26-29-29 15.5-3 26.5-14 29-29z"
          fill="none" stroke="var(--ink)" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M32 13c2 10 9 17 19 19-10 2-17 9-19 19-2-10-9-17-19-19 10-2 17-9 19-19z"
          fill="none" stroke="var(--crimson)" stroke-width="1.5" stroke-linejoin="round" opacity=".75"/>
  </symbol>

  <!-- single petal: solid, used for the fanning button -->
  <symbol id="ic-petal" viewBox="0 0 48 48">
    <path d="M24 3C36 14 39 31 30 43c-3 4-9 4-12 0C9 31 12 14 24 3z"
          fill="var(--blush)" stroke="var(--ink)" stroke-width="3" stroke-linejoin="round"/>
  </symbol>

  <symbol id="ic-butterfly" viewBox="0 0 64 64">
    <!-- upper wings: crescent petals splaying up-and-out -->
    <path d="M32 32C21 28 7 21 6 12 5 3 16 2 24 11c5 6 7 13 8 21z"
          fill="var(--coral)" stroke="var(--ink)" stroke-width="3" stroke-linejoin="round"/>
    <path d="M32 32c11-4 25-11 26-20 1-9-10-10-18-1-5 6-7 13-8 21z"
          fill="var(--coral)" stroke="var(--ink)" stroke-width="3" stroke-linejoin="round"/>
    <!-- lower wings: shorter, fuller crescents -->
    <path d="M32 34c-10 1-20 8-20 18 0 9 11 9 16-1 3-6 4-12 4-17z"
          fill="var(--blush)" stroke="var(--ink)" stroke-width="3" stroke-linejoin="round"/>
    <path d="M32 34c10 1 20 8 20 18 0 9-11 9-16-1-3-6-4-12-4-17z"
          fill="var(--blush)" stroke="var(--ink)" stroke-width="3" stroke-linejoin="round"/>
    <!-- the dotted wing detail from the mark -->
    <circle cx="13" cy="11" r="1.8" fill="var(--ink)"/><circle cx="20" cy="15" r="1.8" fill="var(--ink)"/>
    <circle cx="51" cy="11" r="1.8" fill="var(--ink)"/><circle cx="44" cy="15" r="1.8" fill="var(--ink)"/>
  </symbol>

  <symbol id="ic-bloom" viewBox="0 0 64 64">
    <g stroke="var(--ink)" stroke-width="3.5" stroke-linejoin="round">
      <ellipse cx="32" cy="13" rx="9.5" ry="12" fill="var(--blush)"/>
      <ellipse cx="32" cy="51" rx="9.5" ry="12" fill="var(--blush)"/>
      <ellipse cx="13" cy="32" rx="12" ry="9.5" fill="var(--rose)"/>
      <ellipse cx="51" cy="32" rx="12" ry="9.5" fill="var(--rose)"/>
      <circle cx="32" cy="32" r="8.5" fill="var(--coral)"/>
    </g>
  </symbol>

  <symbol id="ic-petals" viewBox="0 0 64 64">
    <path d="M30 59C10 48 6 24 22 6c13 13 17 35 8 53z" fill="var(--rose)" stroke="var(--ink)" stroke-width="3.5" stroke-linejoin="round"/>
    <path d="M36 59c20-11 24-35 8-53-13 13-17 35-8 53z" fill="var(--blush)" stroke="var(--ink)" stroke-width="3.5" stroke-linejoin="round"/>
  </symbol>
</svg>`;
document.body.insertAdjacentHTML("afterbegin", ICON_SPRITE);
const icon = (name) => `<svg class="ic" aria-hidden="true"><use href="#ic-${name}"/></svg>`;

// current year
document.querySelectorAll("#yr").forEach((el) => (el.textContent = new Date().getFullYear()));

// active nav link
const here = location.pathname.split("/").pop() || "index.html";
document.querySelectorAll("header.site nav a").forEach((a) => {
  if (a.getAttribute("href")?.split("#")[0] === here) a.classList.add("active");
});

// scroll reveal
const io =
  "IntersectionObserver" in window
    ? new IntersectionObserver(
        (entries) => {
          const showing = entries.filter((e) => e.isIntersecting);
          showing.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
          showing.forEach((e, i) => {
            const el = e.target;
            if (!el.style.getPropertyValue("--d") && showing.length > 1) {
              el.style.setProperty("--d", `${Math.min(i, 5) * 0.06}s`);
            }
            el.classList.add("in");
            io.unobserve(el);
          });
        },
        { threshold: 0.14 }
      )
    : null;

const MOTION_OK = matchMedia("(prefers-reduced-motion: no-preference)").matches;

/* Self-drawing sketches.
   Hide each stroke behind a dash gap, then let CSS animate the offset to 0
   once it scrolls into view — so the line looks drawn at the moment you see it.
   stroke-dasharray is an INHERITED svg property, so setting it on the outer
   <svg> also reaches the paths inside a <use>'s shadow tree. */
function primeSketches(root = document) {
  if (!MOTION_OK) return; // reduced motion: leave the strokes fully drawn
  root.querySelectorAll(".draw").forEach((el) => {
    const svg = el.querySelector("svg");
    if (!svg) return;
    const len = el.dataset.len || 240;
    svg.style.strokeDasharray = len;
    svg.style.strokeDashoffset = len;
  });
}

function observeReveals(root = document) {
  root.querySelectorAll(".reveal:not(.in), .draw:not(.in)").forEach((el) => {
    if (io) io.observe(el);
    else el.classList.add("in");
  });
}
primeSketches();
observeReveals();

// Every project lives in data/projects.json — edit it via admin.html.
// (Relative path on purpose: the site is served from /my-work/ on GitHub Pages.)
async function loadProjects() {
  const seed = await fetch("data/projects.json").then((r) => r.json()).catch(() => []);
  return Array.isArray(seed) ? seed : [];
}

// pinned-up paper cards
function renderCards(grid, projects) {
  grid.innerHTML = "";
  if (!projects.length) {
    grid.innerHTML =
      `<div class="empty reveal in"><span class="icon">${icon("petals")}</span>New work lands here soon — say hello below.</div>`;
    return;
  }
  projects.forEach((p, i) => {
    const card = document.createElement("a");
    card.className = "card reveal";
    // projects with a `url` live on Behance — send people there;
    // everything else opens the internal case-study page
    const external = Boolean(p.url);
    card.href = external ? p.url : `project.html?id=${encodeURIComponent(p.id)}`;
    if (external) {
      card.target = "_blank";
      card.rel = "noopener";
    }
    card.style.setProperty("--d", `${(i % 3) * 0.06}s`);
    card.innerHTML = `
      <div class="thumb"><img ${i === 0 ? 'fetchpriority="high"' : 'loading="lazy"'} alt=""></div>
      <div class="meta">
        <span class="cat"></span>
        <h3></h3>
        <p></p>
        <span class="read">${external ? "View on Behance ↗" : "Read the story →"}</span>
      </div>`;
    const img = card.querySelector("img");
    img.src = p.image;
    img.alt = p.title;
    card.querySelector(".cat").textContent = [p.category, p.year].filter(Boolean).join(" · ");
    card.querySelector("h3").textContent = p.title;
    card.querySelector(".meta p").textContent = p.description || "";
    grid.appendChild(card);
  });
  observeReveals(grid);
}
