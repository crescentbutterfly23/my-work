/* ============================================================
   Studio desk — shared working draft
   ------------------------------------------------------------
   admin.html and project-edit.html are two pages, so edits have to
   survive the jump between them. They share one draft in localStorage,
   seeded from data/projects.json.

   Nothing here writes to the repo — the draft is a scratchpad. The only
   thing that publishes is downloading projects.json and committing it.
   ============================================================ */
const DRAFT_KEY = "cb-desk-draft";

const withBlocks = (p) => ({ ...p, blocks: Array.isArray(p.blocks) ? p.blocks : [] });

/** Draft if one exists, otherwise the committed file. */
async function deskLoad() {
  const raw = localStorage.getItem(DRAFT_KEY);
  if (raw) {
    try {
      const d = JSON.parse(raw);
      if (Array.isArray(d)) return d.map(withBlocks);
    } catch {
      localStorage.removeItem(DRAFT_KEY); // corrupt draft — fall through to the file
    }
  }
  const d = await fetch("data/projects.json", { cache: "no-store" }).then((r) => r.json());
  return d.map(withBlocks);
}

function deskSave(projects) {
  try {
    localStorage.setItem(DRAFT_KEY, JSON.stringify(projects));
    return true;
  } catch {
    // localStorage is ~5MB. Embedded data: URLs are what blow it.
    alert(
      "Couldn't save the draft — browser storage is full.\n\n" +
      "This usually means an image was embedded rather than linked. " +
      "Download projects.json now so you don't lose the work."
    );
    return false;
  }
}

const deskHasDraft = () => !!localStorage.getItem(DRAFT_KEY);
const deskDiscard = () => localStorage.removeItem(DRAFT_KEY);

function deskDownload(projects) {
  const blob = new Blob([JSON.stringify(projects, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "projects.json";
  a.click();
  URL.revokeObjectURL(a.href);
}

/* ---------- the block vocabulary (shared by the editor and project.html) ---------- */
const TEXT_STYLES = [
  ["heading", "Heading"],
  ["lead", "Lead"],
  ["body", "Body"],
];
// how much of the block's width the image takes
const IMG_WIDTHS = [
  ["third", "1 / 3"],
  ["half", "1 / 2"],
  ["full", "Full width"],
];
const SPLIT_SIDES = [
  ["left", "Image left, text right"],
  ["right", "Text left, image right"],
];

const newBlock = (type) => {
  if (type === "text") return { type: "text", style: "body", text: "" };
  if (type === "image") return { type: "image", width: "full", image: "", caption: "" };
  if (type === "split") return { type: "split", width: "half", side: "left", image: "", text: "", caption: "" };
  if (type === "grid") return { type: "grid", images: [] };
  return null;
};
