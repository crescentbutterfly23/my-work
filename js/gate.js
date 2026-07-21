/* ============================================================
   Crescent Butterfly — client preview gate
   ------------------------------------------------------------
   Drop this on any preview site you want to share privately before
   it goes live. Two steps:

     1) give <body> the class "cb-locked"
     2) load this script with the passcode hash:

          <body class="cb-locked">
            ...your page...
            <script src="gate.js" data-hash="PASTE_HASH_HERE"></script>
          </body>

   The Studio desk (admin.html) computes the hash for you — set a
   passcode on the project, then hit "Copy gate snippet" and paste the
   whole <script> tag in. The plaintext passcode is never stored in the
   page; you share it with the client separately.

   Same-repo preview (a folder inside my-work)? Point src at this file,
   e.g. src="../js/gate.js". Separate repo? Copy this file in alongside
   your page and use src="gate.js".

   NOTE: this is a casual gate, not real security. Anyone with the link
   and browser dev tools can bypass any client-side check on a static
   site. It keeps a preview out of casual view — not out of determined
   hands. Never put anything genuinely sensitive behind it.
   ============================================================ */
(function () {
  var script = document.currentScript;
  var HASH = (script && script.getAttribute("data-hash") || "").trim().toLowerCase();
  var KEY = "cb-preview-unlocked:" + HASH;

  // No hash configured — fail closed so an unconfigured page never leaks.
  if (!HASH) {
    console.warn("[cb-gate] no data-hash set on the gate script — page stays locked.");
  }

  function reveal() {
    document.body.classList.remove("cb-locked");
    var g = document.getElementById("cb-gate");
    if (g) g.remove();
  }

  // Already unlocked this tab.
  if (HASH && sessionStorage.getItem(KEY) === HASH) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", reveal);
    } else {
      reveal();
    }
    return;
  }

  async function sha256(str) {
    var buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(str));
    return Array.from(new Uint8Array(buf)).map(function (b) {
      return b.toString(16).padStart(2, "0");
    }).join("");
  }

  function buildGate() {
    if (document.getElementById("cb-gate")) return;

    var style = document.createElement("style");
    style.textContent =
      "body.cb-locked{overflow:hidden}" +
      "body.cb-locked>*:not(#cb-gate){display:none!important}" +
      "#cb-gate{position:fixed;inset:0;z-index:2147483647;display:grid;place-items:center;" +
      "padding:6vw;background:#f6dfe0;font-family:'Inter',system-ui,sans-serif}" +
      "#cb-gate .box{background:#fff;border:4px solid #1a1a1a;box-shadow:10px 10px 0 #1a1a1a;" +
      "padding:2rem 1.8rem;max-width:380px;width:100%;transform:rotate(-.6deg)}" +
      "#cb-gate h1{font-size:1.5rem;margin:0 0 .4rem;color:#1a1a1a}" +
      "#cb-gate p{font-size:.8rem;font-weight:600;color:#555;margin:0 0 1.2rem}" +
      "#cb-gate input{width:100%;box-sizing:border-box;font-size:1rem;padding:.65rem .7rem;" +
      "border:3px solid #1a1a1a;background:#fff;color:#3a1020;margin-bottom:.9rem}" +
      "#cb-gate input:focus{outline:3px solid #ff6b5e;outline-offset:1px}" +
      "#cb-gate button{width:100%;font-size:.8rem;font-weight:700;letter-spacing:.1em;" +
      "text-transform:uppercase;cursor:pointer;background:#1a1a1a;color:#fff;border:3px solid #1a1a1a;" +
      "padding:.7rem 1rem;box-shadow:4px 4px 0 #ff6b5e}" +
      "#cb-gate button:hover{background:#c0263f;border-color:#c0263f}" +
      "#cb-gate .err{color:#c0263f;font-size:.75rem;min-height:1.1em;margin-top:.6rem}";
    document.head.appendChild(style);

    var gate = document.createElement("div");
    gate.id = "cb-gate";
    gate.innerHTML =
      '<form class="box">' +
      '<h1>Private preview</h1>' +
      '<p>Enter the passcode to view this page.</p>' +
      '<input type="password" autocomplete="current-password" placeholder="Passcode" autofocus />' +
      '<button type="submit">Unlock</button>' +
      '<div class="err"></div>' +
      '</form>';
    document.body.appendChild(gate);

    var form = gate.querySelector("form");
    var input = gate.querySelector("input");
    var err = gate.querySelector(".err");

    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      if (!HASH) { err.textContent = "This preview isn't configured yet."; return; }
      var h = await sha256(input.value);
      if (h === HASH) {
        sessionStorage.setItem(KEY, HASH);
        reveal();
      } else {
        err.textContent = "Wrong passcode.";
        input.value = "";
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", buildGate);
  } else {
    buildGate();
  }
})();
