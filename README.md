# Crescent Butterfly — Portfolio Website

A branded portfolio site for Netlify with a hidden admin backend for uploading projects.

## Structure

- `site/` — the public site (`index.html`) and the hidden admin page (`admin.html`)
- `netlify/functions/` — serverless backend
  - `projects.mjs` — list (public), add and delete projects (password-protected)
  - `image.mjs` — serves uploaded project images from Netlify Blobs
- Project data and images are stored in **Netlify Blobs** — no database to set up.

## Deploy (one time)

1. Push this `Website` folder to a Git repo (or drag-and-drop won't work here — functions
   need a Git or CLI deploy). Easiest:
   ```
   cd Website
   npm install
   npx netlify login
   npx netlify init      # create the new site
   npx netlify deploy --prod
   ```
2. In the Netlify dashboard → **Site configuration → Environment variables**, add:
   - `ADMIN_PASSWORD` = a strong passphrase only you know
3. Redeploy after setting the variable.

## Using the hidden backend

- Go to `https://YOUR-SITE.netlify.app/admin.html` (not linked anywhere; marked `noindex`).
- Enter your passphrase, then upload a title, category, year, description and image.
- Images are auto-compressed in the browser before upload; delete projects from the same page.
- New projects appear instantly on the homepage "The Work" grid.

## Local preview

```
cd Website
npm install
npx netlify dev
```
`netlify dev` runs the functions and blobs locally; set `ADMIN_PASSWORD` in a `.env` file
or your shell first.
