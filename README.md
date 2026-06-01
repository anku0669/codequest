# ⚡ Ironyx Code

A **free, gamified, browser-based coding platform**. Pick from **34 tracks** (24 programming languages + HTML, CSS, SCSS, JSON, YAML, Markdown, XML, Dockerfile, GraphQL, Regex), solve **4,800+ interactive challenges**, learn from built-in study material, write code in a **full browser IDE** (Monaco, the VS Code editor), run it for real, earn **XP**, build **daily streaks**, **level up**, and unlock **badges**.

![node](https://img.shields.io/badge/Node-20-green) ![editor](https://img.shields.io/badge/Editor-Monaco-blue) ![langs](https://img.shields.io/badge/Tracks-34-orange) ![license](https://img.shields.io/badge/License-MIT-purple)

> **Runs two ways:** as a self-contained **Docker** stack (every language locally), **or** as a pure **static site** you can upload to a **WordPress** website — no Node server required.

---

## ⚙️ How code runs (the compiler)

Ironyx Code uses a layered execution strategy so it works **with or without a server**:

| Layer | Languages | Where it runs | Needs a server? |
|-------|-----------|---------------|-----------------|
| **Browser (Pyodide WASM)** | Python | In the user's browser | ❌ none |
| **Browser (sandboxed Web Worker)** | JavaScript, TypeScript | In the user's browser | ❌ none |
| **Browser → Wandbox** | C, C++, C#, Go, Rust, Ruby, PHP, Lua, Perl, Bash, SQL, Java, Scala, Haskell, Swift, Elixir | Free public API (CORS, **no key**) | ❌ none |
| **Server → Piston** | All 24 languages | Self-hosted engine (Docker) | ✅ `docker compose up` |

**Result:**
- **Static / WordPress (no Node):** Python/JS/TS run in-browser and ~16 more languages run via the free Wandbox API directly from the browser — **most languages work instantly, no setup.**
- **Docker stack:** the bundled Piston engine runs **all 24** languages locally, with Wandbox as an automatic backup.

No API keys anywhere. The compiler list is pre-warmed on load so the first remote run is fast.

---

## 🚀 Quick start (Docker — test it locally)

Run the full self-hosted stack (web app + Piston engine + auto language install):

```bash
docker compose up --build
```

Then open **http://localhost:3000**.

> First boot downloads the language runtimes into a cached volume (a few minutes). Later boots are fast.

### Or run just the web app (no Docker)

```bash
npm install
npm start
# open http://localhost:3000
```

Without Docker, Python/JS/TS run in-browser and the other languages use the free public Wandbox engine automatically.

---

## 🌐 Deploy to a WordPress website

Ironyx Code's front-end is 100% static (HTML/CSS/JS), uses hash-based routing, and needs **no Node server** — perfect for WordPress.

The upload-ready files are in the **`wordpress/`** folder. See **[WORDPRESS.md](WORDPRESS.md)** for step-by-step instructions (upload + embed via iframe). Short version:

1. Upload the contents of `wordpress/` to your site (e.g. `wp-content/uploads/ironyx-code/`).
2. Add a page with an iframe pointing at `…/ironyx-code/index.html`.
3. Done — Python/JS/TS run in the visitor's browser; other languages run via the free Wandbox engine.

---

## 🧱 Project structure

```
ironyx-code/
├─ public/                 # the app (also the static site)
│  ├─ index.html
│  ├─ css/styles.css
│  ├─ js/app.js            # SPA: IDE, challenges, XP, multi-engine compiler
│  └─ data/curriculum.js   # generated: 34 tracks, 4,800+ lessons
├─ wordpress/              # upload-ready static copy for WordPress
├─ server.js               # Node API: Piston → Wandbox execution proxy
├─ scripts/install-languages.js
├─ Dockerfile
├─ docker-compose.yml
├─ generate_curriculum.py  # rebuild curriculum.js (edit + `npm run generate`)
└─ *.py                    # challenge/content banks used by the generator
```

## 🔁 Rebuilding the curriculum

```bash
npm run generate   # runs generate_curriculum.py → public/data/curriculum.js
```

## 🔒 Security & performance

**Security**
- **Hardened HTTP headers** — Content-Security-Policy, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`; `X-Powered-By` removed. Framing is intentionally allowed so the app can be embedded in a WordPress iframe.
- **Sandboxed JS/TS execution** — user code runs in a Web Worker with `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource` and `importScripts` disabled (no network / no exfiltration).
- **Strict input validation** — `/api/execute` validates the language, caps source (200 KB) and stdin (100 KB), and rejects malformed requests.
- **Rate limiting** — in-memory per-IP limiter (default 40 runs/min) to prevent abuse.
- **No secrets / generic errors** — no API keys anywhere; internal error details are logged server-side, not returned to clients (in production).
- **Salted password hashing** — local profiles store a salted **SHA-256** hash via Web Crypto (never the raw password); legacy entries upgrade automatically on login.
- **Non-root container** — the Docker image runs as the unprivileged `node` user with `tini` as PID 1.

**Performance**
- **gzip compression** — the 3 MB curriculum is served at **~300 KB** (≈90% smaller).
- **Long-lived caching + ETags** for static assets; `index.html` stays revalidated.
- **Engine pre-warming** — the remote compiler list loads on boot and the Python engine is prefetched during idle time, so first runs are fast.
- **In-browser engines** — Python/JS/TS never hit the network for execution.

## 📝 License

MIT.
