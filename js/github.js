/* ============================================================
   Crescent Butterfly — Studio ⇄ GitHub sync
   ------------------------------------------------------------
   The site is static (GitHub Pages, no backend), so on its own the
   Studio can't write anything. This module lets the admin pages commit
   straight to the repo through the GitHub Contents API, using a
   personal access token YOU paste in once.

   Set up (one time):
     1. github.com → Settings → Developer settings →
        Fine-grained personal access tokens → Generate new token
     2. Repository access → Only select repositories → my-work
     3. Permissions → Repository permissions → Contents → Read and write
     4. Generate, copy it, paste it into the Studio's "Connect GitHub" box.

   The token is kept in this browser only (localStorage) and is never
   written into any file the site publishes. Anyone with the token can
   push to the repo, so treat it like a password — don't paste it
   anywhere public, and hit "Disconnect" on a shared machine.
   ============================================================ */
const GH = { owner: "crescentbutterfly23", repo: "my-work", branch: "main" };
const GH_TOKEN_KEY = "cb-gh-token";

const ghToken = () => localStorage.getItem(GH_TOKEN_KEY) || "";
const ghSetToken = (t) => localStorage.setItem(GH_TOKEN_KEY, t.trim());
const ghClearToken = () => localStorage.removeItem(GH_TOKEN_KEY);
const ghConnected = () => !!ghToken();

function ghHeaders() {
  return {
    Authorization: `Bearer ${ghToken()}`,
    Accept: "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
  };
}

// Encode each path segment but keep the slashes.
const ghUrl = (path) =>
  `https://api.github.com/repos/${GH.owner}/${GH.repo}/contents/` +
  path.split("/").map(encodeURIComponent).join("/");

/** Validate the token + confirm it can push. Returns {ok, reason?}. */
async function ghCheck() {
  if (!ghConnected()) return { ok: false, reason: "No token set." };
  try {
    const r = await fetch(`https://api.github.com/repos/${GH.owner}/${GH.repo}`, { headers: ghHeaders() });
    if (r.status === 401) return { ok: false, reason: "Token rejected (401) — wrong or expired." };
    if (r.status === 404) return { ok: false, reason: "Repo not visible to this token — check its repository access." };
    if (!r.ok) return { ok: false, reason: `GitHub error ${r.status}.` };
    const data = await r.json();
    if (!data.permissions || !data.permissions.push) {
      return { ok: false, reason: "Token can read but not write — give it Contents: Read and write." };
    }
    return { ok: true };
  } catch (e) {
    return { ok: false, reason: "Network error reaching GitHub." };
  }
}

/** Current blob SHA for a path, or null if the file doesn't exist yet. */
async function ghGetSha(path) {
  const r = await fetch(`${ghUrl(path)}?ref=${GH.branch}`, { headers: ghHeaders() });
  if (r.status === 404) return null;
  if (!r.ok) throw new Error(`Couldn't read ${path} (${r.status}).`);
  const data = await r.json();
  return data.sha || null;
}

const blobToBase64 = (blob) =>
  new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.onload = () => resolve(String(fr.result).split(",")[1]); // strip the data: prefix
    fr.onerror = () => reject(new Error("Couldn't read the file."));
    fr.readAsDataURL(blob);
  });

/** Create or overwrite a file. `content` is a Blob or a string. */
async function ghPutFile(path, content, message) {
  if (!ghConnected()) throw new Error("Connect GitHub first.");
  const blob = content instanceof Blob ? content : new Blob([content], { type: "text/plain" });
  const base64 = await blobToBase64(blob);
  const sha = await ghGetSha(path); // omitted → create; present → update
  const body = { message, content: base64, branch: GH.branch };
  if (sha) body.sha = sha;
  const r = await fetch(ghUrl(path), { method: "PUT", headers: ghHeaders(), body: JSON.stringify(body) });
  if (!r.ok) {
    let detail = "";
    try { detail = (await r.json()).message || ""; } catch {}
    throw new Error(`Save failed (${r.status})${detail ? ": " + detail : ""}.`);
  }
  return path;
}

/** Commit the whole projects array to data/projects.json. */
async function ghSaveProjects(projects) {
  const text = JSON.stringify(projects, null, 2) + "\n";
  return ghPutFile("data/projects.json", text, "Update projects.json via Studio");
}

/** Commit an uploaded image under assets/projects/<id>/ and return its repo path. */
async function ghUploadImage(file, projectId, hint) {
  const ext = (file.type.split("/")[1] || "png").replace("jpeg", "jpg").toLowerCase();
  const slug = (projectId || "project").replace(/[^a-z0-9-]+/gi, "-").toLowerCase();
  const stamp = Date.now().toString(36);
  const name = `${hint ? hint + "-" : ""}${stamp}.${ext}`;
  const path = `assets/projects/${slug}/${name}`;
  await ghPutFile(path, file, `Add image ${path} via Studio`);
  return path;
}

/* ---------- the little Connect/Save widget both pages mount ---------- */
/* Injects a connect panel into #gh-mount and returns a `save` fn the page
   wires to its Save button. `onSaved` runs after a successful projects save. */
function ghMountConnect(mountId) {
  const mount = document.getElementById(mountId);
  if (!mount) return;

  function paint() {
    if (ghConnected()) {
      mount.innerHTML =
        `<span class="gh-ok">✓ Connected — ${GH.owner}/${GH.repo}</span>` +
        `<button type="button" class="gh-btn" data-gh="disconnect">Disconnect</button>`;
    } else {
      mount.innerHTML =
        `<span class="gh-off">Not connected — Save is offline.</span>` +
        `<input type="password" class="gh-input" data-gh="token" placeholder="Paste GitHub token" autocomplete="off" />` +
        `<button type="button" class="gh-btn" data-gh="connect">Connect</button>` +
        `<a class="gh-help" href="https://github.com/settings/tokens?type=beta" target="_blank" rel="noopener">get a token ↗</a>`;
    }
  }

  mount.addEventListener("click", async (e) => {
    const act = e.target.dataset.gh;
    if (act === "disconnect") { ghClearToken(); paint(); document.dispatchEvent(new Event("gh-change")); }
    if (act === "connect") {
      const input = mount.querySelector('[data-gh="token"]');
      const val = (input.value || "").trim();
      if (!val) return;
      const btn = e.target;
      btn.textContent = "Checking…"; btn.disabled = true;
      ghSetToken(val);
      const res = await ghCheck();
      if (res.ok) { paint(); document.dispatchEvent(new Event("gh-change")); }
      else { ghClearToken(); btn.disabled = false; btn.textContent = "Connect"; alert("Couldn't connect: " + res.reason); }
    }
  });

  paint();
}
