// shared behavior: reveals, marquee, nav state, project data
document.querySelectorAll("#yr").forEach((el) => (el.textContent = new Date().getFullYear()));

// active nav link
const here = location.pathname.split("/").pop() || "index.html";
document.querySelectorAll("header.site nav a").forEach((a) => {
  if (a.getAttribute("href").split("#")[0] === here) a.classList.add("active");
});

// seamless marquee loop
const track = document.getElementById("marqueeTrack");
if (track) track.innerHTML += track.innerHTML;

// scroll reveal via IntersectionObserver (no scroll listeners)
// Mercury-style: elements rise + blur-clear; siblings entering together cascade.
const io = new IntersectionObserver(
  (entries) => {
    // group entries firing in the same frame so siblings stagger in order
    const showing = entries.filter((e) => e.isIntersecting);
    showing.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    showing.forEach((e, i) => {
      const el = e.target;
      if (!el.style.getPropertyValue("--d") && showing.length > 1) {
        el.style.setProperty("--d", `${Math.min(i, 6) * 0.08}s`);
      }
      el.classList.add("in");
      el.addEventListener("transitionend", () => (el.style.willChange = "auto"), { once: true });
      io.unobserve(el);
    });
  },
  { threshold: 0.15 }
);
function observeReveals(root = document) {
  root.querySelectorAll(".reveal:not(.in)").forEach((el) => io.observe(el));
}
observeReveals();

// ambient background: drifting butterflies that parallax with the pointer
const MOTION_OK = matchMedia("(prefers-reduced-motion: no-preference)").matches;
if (MOTION_OK) {
  const layer = document.createElement("div");
  layer.className = "ambient";
  layer.setAttribute("aria-hidden", "true");
  const flies = [];
  const rnd = (a, b) => a + Math.random() * (b - a);
  const ART = ["assets/illus/petals.png", "assets/illus/sparkle.png", "assets/illus/moon.png"];
  for (let i = 0; i < 7; i++) {
    const depth = rnd(0.25, 1); // deeper = bigger + moves more
    const el = document.createElement("div");
    el.className = "fly";
    el.style.width = `${Math.round(46 + depth * 110)}px`;
    el.style.left = `${rnd(2, 90)}%`;
    el.style.top = `${rnd(4, 90)}%`;
    el.style.opacity = (0.07 + depth * 0.1).toFixed(3);
    el.innerHTML = `<img src="${ART[i % ART.length]}" alt="" style="transform:rotate(${rnd(-25, 25)}deg)">`;
    layer.appendChild(el);
    flies.push({ el, depth, phase: rnd(0, Math.PI * 2), speed: rnd(0.15, 0.4) });
  }
  document.body.appendChild(layer);

  let mx = 0, my = 0; // pointer offset from center, -1..1
  addEventListener("pointermove", (e) => {
    mx = (e.clientX / innerWidth) * 2 - 1;
    my = (e.clientY / innerHeight) * 2 - 1;
  }, { passive: true });

  let t = 0;
  (function drift(now) {
    t = now / 1000;
    for (const f of flies) {
      const sway = Math.sin(t * f.speed + f.phase) * 18;
      const bob = Math.cos(t * f.speed * 0.8 + f.phase) * 14;
      const px = -mx * 34 * f.depth;
      const py = -my * 26 * f.depth;
      f.el.style.transform = `translate(${(sway + px).toFixed(1)}px, ${(bob + py).toFixed(1)}px)`;
    }
    requestAnimationFrame(drift);
  })(0);
}

// gentle 3D tilt on work cards, following the pointer
function attachTilt(card) {
  if (!MOTION_OK) return;
  const thumb = card.querySelector(".thumb");
  if (!thumb) return;
  card.addEventListener("pointermove", (e) => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    thumb.style.transform = `perspective(700px) rotateY(${(x * 5).toFixed(2)}deg) rotateX(${(-y * 5).toFixed(2)}deg)`;
  });
  card.addEventListener("pointerleave", () => {
    thumb.style.transform = "";
  });
}

// uploaded projects from the API plus built-in case studies
async function loadProjects() {
  const [api, seed] = await Promise.all([
    fetch("/api/projects").then((r) => r.json()).catch(() => []),
    fetch("data/projects.json").then((r) => r.json()).catch(() => []),
  ]);
  return [...(Array.isArray(api) ? api : []), ...(Array.isArray(seed) ? seed : [])];
}

function renderCards(grid, projects) {
  grid.innerHTML = "";
  if (!projects.length) {
    grid.innerHTML =
      '<div class="empty reveal in"><img src="assets/illus/petals.png" alt="">New work is landing here soon. In the meantime, say hello below.</div>';
    return;
  }
  projects.forEach((p, i) => {
    const card = document.createElement("a");
    card.className = "card reveal";
    card.href = `project.html?id=${encodeURIComponent(p.id)}`;
    card.style.setProperty("--d", `${(i % 3) * 0.08}s`);
    card.innerHTML = `
      <div class="thumb"><img ${i === 0 ? 'fetchpriority="high"' : 'loading="lazy"'} alt=""></div>
      <div class="meta">
        <span class="cat"></span>
        <h3></h3>
        <p></p>
        <span class="read">Read the story</span>
      </div>`;
    card.querySelector("img").src = p.image;
    card.querySelector("img").alt = p.title;
    card.querySelector(".cat").textContent = [p.category, p.year].filter(Boolean).join(" · ");
    card.querySelector("h3").textContent = p.title;
    card.querySelector(".meta p").textContent = p.description || "";
    attachTilt(card);
    grid.appendChild(card);
  });
  observeReveals(grid);
}
