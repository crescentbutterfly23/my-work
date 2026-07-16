/* ============================================================
   Crescent Butterfly — CORPORATE theme shared behavior
   year · active nav · reveals · project data · card grid
   ============================================================ */

document.querySelectorAll("#yr").forEach((el) => (el.textContent = new Date().getFullYear()));

const here = location.pathname.split("/").pop() || "index-corporate.html";
document.querySelectorAll("header.site nav a.link").forEach((a) => {
  if (a.getAttribute("href").split("#")[0] === here) a.classList.add("active");
});

const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    });
  },
  { threshold: 0.14 }
);
function observeReveals(root = document) {
  root.querySelectorAll(".reveal:not(.in)").forEach((el) => io.observe(el));
}
observeReveals();

// Static host (GitHub Pages) has no backend, so the project brief is composed
// into an email the visitor sends from their own client.
function buildBriefMailto(a) {
  const STUDIO_EMAIL = "crescentbutterfly23@gmail.com";
  const body = [
    `Name:      ${a.name}`,
    `Email:     ${a.email}`,
    "",
    `Services:  ${(a.services || []).join(", ") || "—"}`,
    `Stage:     ${a.stage || "—"}`,
    `Timeline:  ${a.timeline || "—"}`,
    `Budget:    ${a.budget || "—"}`,
    "",
    "The story:",
    a.message || "—",
    "",
    "— sent from the Crescent Butterfly site",
  ].join("\n");
  return (
    `mailto:${STUDIO_EMAIL}` +
    `?subject=${encodeURIComponent(`Project brief — ${a.name}`)}` +
    `&body=${encodeURIComponent(body)}`
  );
}

async function loadProjects() {
  const [api, seed] = await Promise.all([
    fetch("/api/projects").then((r) => r.json()).catch(() => []),
    fetch("data/projects.json").then((r) => r.json()).catch(() => []),
  ]);
  return [...(Array.isArray(api) ? api : []), ...(Array.isArray(seed) ? seed : [])];
}

// render clean bordered cards into a .work-grid container
function renderCards(grid, projects) {
  if (!projects.length) {
    grid.innerHTML =
      '<div class="work-empty">New work is landing here soon. In the meantime, get in touch below.</div>';
    return;
  }
  grid.innerHTML = projects
    .map(
      (p) => `
      <a class="wcard reveal" href="project-corporate.html?id=${encodeURIComponent(p.id)}">
        <div class="thumb"><img src="${p.image}" alt="${(p.title || "").replace(/"/g, "&quot;")}" loading="lazy" /></div>
        <div class="meta">
          <span class="cat">${[p.category, p.year].filter(Boolean).join(" · ")}</span>
          <h3>${p.title}</h3>
          <p>${p.description || ""}</p>
        </div>
      </a>`
    )
    .join("");
  observeReveals(grid);
}
