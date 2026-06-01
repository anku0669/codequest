# 🌐 Deploying Ironyx Code to a WordPress website

Ironyx Code's front-end is fully static (HTML + CSS + JS) and uses **hash-based routing**, so it works in any subfolder with **no Node server, no database, and no API key**. Python, JavaScript and TypeScript run directly in the visitor's browser; the other languages run through the free public **Wandbox** engine (called straight from the browser).

Everything you need is in the **`wordpress/`** folder (or the separate `ironyx-code-wordpress.zip`).

---

## Option A — Upload the folder + embed it (recommended)

This keeps Ironyx Code self-contained and avoids theme/CSS conflicts.

### 1. Upload the files
Use your host's **File Manager** (cPanel/Plesk) or **FTP/SFTP**:

1. Unzip `ironyx-code-wordpress.zip` (or open the `wordpress/` folder).
2. Upload the whole `ironyx-code/` folder into your site, e.g. to:
   ```
   wp-content/uploads/ironyx-code/
   ```
   You should end up with:
   ```
   wp-content/uploads/ironyx-code/index.html
   wp-content/uploads/ironyx-code/css/styles.css
   wp-content/uploads/ironyx-code/js/app.js
   wp-content/uploads/ironyx-code/data/curriculum.js
   ```
3. Confirm it loads by visiting:
   ```
   https://YOURSITE.com/wp-content/uploads/ironyx-code/index.html
   ```

### 2. Embed it in a page
In the WordPress editor, create/edit a page, add a **Custom HTML** block, and paste:

```html
<iframe
  src="/wp-content/uploads/ironyx-code/index.html"
  title="Ironyx Code"
  style="width:100%;height:90vh;border:0;border-radius:12px;"
  loading="lazy"
  allow="clipboard-write"></iframe>
```

Publish. That's it — Ironyx Code now lives on your page.

> A ready-made `embed-example.html` is included in the folder so you can preview the iframe before publishing.

---

## Option B — Full-page subdomain / subdirectory

If you'd rather serve it on its own URL (e.g. `https://YOURSITE.com/learn/`), just upload the `ironyx-code/` folder there and link to `index.html`. Because routing is hash-based, no `.htaccess` rewrite rules are needed.

---

## Notes & tips

- **No build step.** The files are ready as-is. Don't rename the `css/`, `js/`, or `data/` folders — paths are relative to `index.html`.
- **Internet required for compiled languages.** Python/JS/TS work offline in the browser; C/C++/Java/Go/Rust/etc. call the free Wandbox API, so visitors need internet (no key, no signup).
- **Progress is saved per browser** via `localStorage` (XP, streaks, badges). It is not shared across devices.
- **HTTPS recommended.** Serve your site over HTTPS so the browser can reach the Wandbox API without mixed-content warnings.
- **Security plugins:** if a plugin (e.g. Wordfence) blocks `.html`/iframes in uploads, allow `wp-content/uploads/ironyx-code/`, or use Option B.
- **Every-language-local option:** if you want all 24 languages without relying on Wandbox, run the bundled Docker stack (`docker compose up --build`) on a server and point an iframe at that host instead.
