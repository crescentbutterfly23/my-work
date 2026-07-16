/* ============================================================
   Crescent Butterfly — EDITORIAL theme shared behavior
   year · active nav · ticker · reveals · project data
   ============================================================ */

// current year
document.querySelectorAll("#yr").forEach((el) => (el.textContent = new Date().getFullYear()));

// active nav link
const here = location.pathname.split("/").pop() || "index-editorial.html";
document.querySelectorAll("header.site nav a.link").forEach((a) => {
  if (a.getAttribute("href").split("#")[0] === here) a.classList.add("active");
});

// seamless ticker loop (doubles content so the CSS translate(-50%) is seamless)
document.querySelectorAll("[data-ticker]").forEach((t) => (t.innerHTML += t.innerHTML));

// scroll reveal via IntersectionObserver
const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("in");
        io.unobserve(e.target);
      }
    });
  },
  { threshold: 0.14 }
);
function observeReveals(root = document) {
  root.querySelectorAll(".reveal:not(.in)").forEach((el) => io.observe(el));
}
observeReveals();

// uploaded projects from the API plus built-in case studies
async function loadProjects() {
  const [api, seed] = await Promise.all([
    fetch("/api/projects").then((r) => r.json()).catch(() => []),
    fetch("data/projects.json").then((r) => r.json()).catch(() => []),
  ]);
  return [...(Array.isArray(api) ? api : []), ...(Array.isArray(seed) ? seed : [])];
}

// render an editorial numbered index into a .work-list container
function renderWorkIndex(list, projects) {
  if (!projects.length) {
    list.innerHTML =
      '<div class="work-empty">New work is landing here soon. In the meantime, say hello below.</div>';
    return;
  }
  list.innerHTML = projects
    .map(
      (p, i) => `
      <a class="work-row reveal" href="project-editorial.html?id=${encodeURIComponent(p.id)}">
        <span class="idx">${String(i + 1).padStart(2, "0")}</span>
        <span class="title">${p.title}<span class="cat">${[p.category, p.year]
        .filter(Boolean)
        .join(" · ")}</span></span>
        <span class="go">Read the story &rarr;</span>
        <img class="peek" src="${p.image}" alt="" aria-hidden="true" />
      </a>`
    )
    .join("");
  observeReveals(list);
}
