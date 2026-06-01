/* ============================================================
   Ironyx Code SPA v5 — IDE editor + 4800+ challenges + DSA + learning material
   ============================================================ */
const C = window.CURRICULUM;
const app = document.getElementById("app");

/* ---------- Accounts (local) ---------- */
const AUTH_KEY = "codequest_auth_v1";
function loadAuth() { try { return Object.assign({ users: {}, current: null }, JSON.parse(localStorage.getItem(AUTH_KEY)) || {}); } catch { return { users: {}, current: null }; } }
let auth = loadAuth();
function saveAuth() { localStorage.setItem(AUTH_KEY, JSON.stringify(auth)); }
function userKey() { return "codequest_player_v1::" + (auth.current || "guest"); }
/* Passwords are never stored in reversible form. We keep only a salted
   SHA-256 hash (Web Crypto). Legacy base64 entries are upgraded on next login.
   NOTE: this is a local-only profile system (no server) — the hash simply
   avoids storing the raw password in localStorage. */
async function sha256Hex(text) {
  if (window.crypto && crypto.subtle) {
    const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
    return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
  }
  // Fallback for insecure contexts (no SubtleCrypto): weak, but never stores the raw password.
  let h = 5381 >>> 0; for (let i = 0; i < text.length; i++) h = (((h << 5) + h) + text.charCodeAt(i)) >>> 0;
  return "w" + h.toString(16);
}
function randSalt() {
  const a = new Uint8Array(16);
  if (window.crypto && crypto.getRandomValues) crypto.getRandomValues(a);
  else for (let i = 0; i < a.length; i++) a[i] = Math.floor(Math.random() * 256);
  return [...a].map((b) => b.toString(16).padStart(2, "0")).join("");
}
async function hashPass(pass, salt) { return "sha256$" + salt + "$" + (await sha256Hex(salt + ":" + (pass || ""))); }

async function registerUser(name, pass) {
  name = (name || "").trim();
  if (name.length < 2) return "Please enter a name (2+ characters).";
  if (name.length > 40) return "That name is too long (max 40 characters).";
  if ((pass || "").length < 4) return "Password must be at least 4 characters.";
  if (auth.users[name.toLowerCase()]) return "That account already exists — try logging in.";
  auth.users[name.toLowerCase()] = { name, p: await hashPass(pass, randSalt()), created: Date.now() };
  auth.current = name.toLowerCase(); saveAuth(); state = load(); return null;
}
async function loginUser(name, pass) {
  const key = (name || "").trim().toLowerCase();
  const u = auth.users[key];
  if (!u) return "No account with that name. Register first.";
  let ok = false;
  if (typeof u.p === "string" && u.p.startsWith("sha256$")) {
    const salt = u.p.split("$")[1] || "";
    ok = (await hashPass(pass, salt)) === u.p;
  } else {
    // Legacy base64 entry → verify, then transparently upgrade to a salted hash.
    try { ok = u.p === btoa(pass || ""); } catch { ok = false; }
    if (ok) { u.p = await hashPass(pass, randSalt()); }
  }
  if (!ok) return "Incorrect password.";
  auth.current = key; saveAuth(); state = load(); return null;
}
function logoutUser() { auth.current = null; saveAuth(); state = load(); }
function displayName() { const u = auth.current && auth.users[auth.current]; return u ? u.name : null; }

/* ---------- Player state (per account) ---------- */
const defaultState = () => ({ xp: 0, completed: {}, lastActive: null, streak: 0, badges: {} });
let state = load();
function load() { try { const s = JSON.parse(localStorage.getItem(userKey())); return s && typeof s === "object" ? Object.assign(defaultState(), s) : defaultState(); } catch { return defaultState(); } }
function save() { localStorage.setItem(userKey(), JSON.stringify(state)); refreshChip(); }
function todayStr() { return new Date().toISOString().slice(0, 10); }
function touchStreak() { const t = todayStr(); if (state.lastActive === t) return; const y = new Date(Date.now() - 86400000).toISOString().slice(0, 10); state.streak = state.lastActive === y ? state.streak + 1 : 1; state.lastActive = t; save(); }
function levelFor(xp) { return Math.floor(Math.sqrt(xp / 50)) + 1; }
function totalLessons() { return C.reduce((n, t) => n + t.lessons.length, 0); }
function completedCount() { return Object.keys(state.completed).length; }
const $ = (id) => document.getElementById(id);
function refreshChip() { $("chipStreak").textContent = state.streak; $("chipLevel").textContent = levelFor(state.xp); $("chipXp").textContent = state.xp; }

/* ---------- IDE settings ---------- */
const IDE_KEY = "cq_ide_v1";
let ide = (() => { try { return Object.assign({ theme: "cq", font: 14, wrap: false, minimap: false }, JSON.parse(localStorage.getItem(IDE_KEY)) || {}); } catch { return { theme: "cq", font: 14, wrap: false, minimap: false }; } })();
function saveIde() { localStorage.setItem(IDE_KEY, JSON.stringify(ide)); }

/* ---------- Server engine availability ---------- */
/* Ironyx Code runs with OR without a Node backend:
   - With the bundled Docker stack: code goes through the local /api/execute
     (self-hosted Piston, with an automatic Wandbox fallback).
   - As a pure-static deploy (e.g. uploaded to a WordPress site): there is no
     Node server, so the browser talks DIRECTLY to the free public Wandbox engine
     (wandbox.org) — it's CORS-enabled and needs no API key. The compiler list is
     pre-warmed on boot so the first remote run is fast. */
const WANDBOX_API = "https://wandbox.org/api";
/* track.lang -> Wandbox language name (only languages Wandbox supports) */
const WANDBOX_LANG = {
  "c": "C", "c++": "C++", "csharp": "C#", "go": "Go", "rust": "Rust",
  "ruby": "Ruby", "php": "PHP", "lua": "Lua", "perl": "Perl",
  "bash": "Bash script", "sqlite3": "SQL", "java": "Java", "scala": "Scala",
  "haskell": "Haskell", "swift": "Swift", "elixir": "Elixir",
  "python": "Python", "javascript": "JavaScript",
};
let serverEngineReady = null;     // is a local Node /api backend reachable?
let wandboxList = null;           // cached compiler catalog from Wandbox
let _wandboxListP = null;
function preloadWandbox() {
  if (wandboxList) return Promise.resolve(wandboxList);
  if (_wandboxListP) return _wandboxListP;
  const ctrl = new AbortController(); const id = setTimeout(() => ctrl.abort(), 9000);
  _wandboxListP = fetch(`${WANDBOX_API}/list.json`, { signal: ctrl.signal })
    .then((r) => (r.ok ? r.json() : null))
    .then((d) => { wandboxList = Array.isArray(d) ? d : null; return wandboxList; })
    .catch(() => null)
    .finally(() => clearTimeout(id));
  return _wandboxListP;
}
function pickWandboxCompiler(language) {
  const wl = WANDBOX_LANG[language];
  if (!wl || !wandboxList) return null;
  const matches = wandboxList.filter((c) => c.language === wl);
  if (!matches.length) return null;
  // Prefer the latest STABLE compiler; "-head" nightlies are flaky, use last.
  const stable = matches.find((c) => !/head/i.test(c.name));
  return (stable || matches[0]).name;
}
async function pingServer() {
  try { const r = await fetch("/api/runtimes"); serverEngineReady = r.ok; }
  catch { serverEngineReady = false; }
  if (!serverEngineReady) preloadWandbox(); // warm the public engine in the background
  return serverEngineReady;
}

/* ---------- Router ---------- */
function go(route, params = {}) { const q = new URLSearchParams(params).toString(); location.hash = `#${route}${q ? "?" + q : ""}`; }
function parseHash() { const raw = location.hash.slice(1) || "home"; const [route, qs] = raw.split("?"); return { route, params: Object.fromEntries(new URLSearchParams(qs || "")) }; }
window.addEventListener("hashchange", render);
document.querySelectorAll(".top-nav a").forEach((a) => a.addEventListener("click", () => go(a.dataset.route)));
$("brandHome").addEventListener("click", () => go("home"));
function setActiveNav(route) { document.querySelectorAll(".top-nav a").forEach((a) => a.classList.toggle("active", a.dataset.route === route)); }

const ENGINE_LABEL = { pyodide: { txt: "Runs in your browser", cls: "browser" }, js: { txt: "Runs in your browser", cls: "browser" }, ts: { txt: "Runs in your browser", cls: "browser" }, server: { txt: "Runs on the engine", cls: "server" }, web: { txt: "Live preview", cls: "browser" }, static: { txt: "Structure-checked", cls: "server" } };
const EXT = { python: "py", javascript: "js", typescript: "ts", java: "java", c: "c", "c++": "cpp", csharp: "cs", go: "go", rust: "rs", ruby: "rb", php: "php", swift: "swift", kotlin: "kt", bash: "sh", lua: "lua", perl: "pl", dart: "dart", scala: "scala", haskell: "hs", elixir: "ex", r: "r", julia: "jl", clojure: "clj", sqlite3: "sql" };

function render() {
  const { route, params } = parseHash(); setActiveNav(route); refreshChip(); updateAuthSlot();
  if (route === "home") return renderHome();
  if (route === "auth") return renderAuth(params.mode || "login");
  if (route === "track") return renderTrack(params.id);
  if (route === "lesson") return renderLesson(params.track, params.id);
  if (route === "guide") return renderGuide(params.id);
  if (route === "playground") return renderPlayground();
  if (route === "leaderboard") return renderLeaderboard();
  renderHome();
}

/* ============================================================ HOME */
function renderHome() {
  const done = completedCount(), total = totalLessons();
  app.innerHTML = `
    <section class="hero">
      <h1>Learn to code by <span class="grad">playing</span>.</h1>
      <p>Master ${C.length} languages with <b>${total.toLocaleString()}+ interactive challenges</b> — including a LeetCode-style DSA track — in a full-featured browser IDE. Run real code, earn XP, keep your streak, and level up.</p>
      <div class="hero-cta"><button class="btn primary" id="ctaStart">Start learning</button><button class="btn ghost" id="ctaPlay">Open IDE Playground</button></div>
      <div class="stats-row">
        <div class="stat"><div class="num">${C.length}</div><div class="lbl">Languages</div></div>
        <div class="stat"><div class="num">${total.toLocaleString()}</div><div class="lbl">Challenges</div></div>
        <div class="stat"><div class="num">${state.xp}</div><div class="lbl">Your XP</div></div>
        <div class="stat"><div class="num">${done}</div><div class="lbl">Solved</div></div>
      </div>
    </section>
    <div class="section-head"><h2>Choose your language</h2><span class="sub">${C.length} tracks · free forever</span></div>
    <div class="track-grid" id="trackGrid"></div>`;
  $("ctaStart").onclick = () => $("trackGrid").scrollIntoView({ behavior: "smooth" });
  $("ctaPlay").onclick = () => go("playground");
  C.forEach((t) => {
    const doneN = t.lessons.filter((l) => state.completed[l.id]).length;
    const pct = Math.round((doneN / t.lessons.length) * 100);
    const card = document.createElement("div"); card.className = "track-card"; card.style.setProperty("--clr", t.color);
    card.innerHTML = `<div class="track-icon">${t.icon}</div><h3>${esc(t.name)}</h3><div class="blurb">${esc(t.blurb)}</div>
      <div class="progress-bar"><span style="width:${pct}%"></span></div>
      <div class="track-meta"><span class="lessons">${doneN}/${t.lessons.length} lessons</span><span class="lessons">${pct}%</span></div>`;
    card.onclick = () => go("track", { id: t.id });
    $("trackGrid").appendChild(card);
  });
}

/* ============================================================ TRACK (collapsible + search + learning material) */
function renderTrack(id) {
  const t = C.find((x) => x.id === id); if (!t) return go("home");
  const eng = ENGINE_LABEL[t.engine] || ENGINE_LABEL.server;
  const modules = [];
  t.lessons.forEach((l) => { let m = modules.find((x) => x.name === l.module); if (!m) { m = { name: l.module, items: [] }; modules.push(m); } m.items.push(l); });
  const firstUnsolvedModule = modules.find((m) => m.items.some((l) => !state.completed[l.id]));
  app.innerHTML = `
    <a class="back-link" id="back">← All languages</a>
    <div class="section-head"><h2>${t.icon} ${t.name}</h2><span class="engine-badge ${eng.cls}">${eng.txt}</span></div>
    <div class="guide-cta"><div class="guide-cta-text"><b>📚 The ${t.name} Guide</b><span>Learn ${t.name} from zero to advanced — ${(t.guide || []).length} chapters of explained material with examples.</span></div><button class="btn primary" id="guideBtn">Open Guide →</button></div>
    <input id="lessonSearch" class="lesson-search" placeholder="Search ${t.lessons.length} challenges in ${t.name}..." />
    <div id="modules"></div>`;
  $("back").onclick = () => go("home");
  $("guideBtn").onclick = () => go("guide", { id: t.id });
  const wrap = $("modules");
  modules.forEach((m, mi) => {
    const doneN = m.items.filter((l) => state.completed[l.id]).length;
    const open = m === firstUnsolvedModule;
    const det = document.createElement("details"); det.className = "module-block"; if (open) det.open = true;
    const mat = (t.materials || {})[m.name];
    const learn = mat ? `<div class="module-learn"><div class="learn-head">📘 Learn this module</div><div class="learn-text">${mdInline(mat.text)}</div>${mat.code ? `<div class="learn-eg">Example in ${t.name}:</div><pre class="learn-code">${esc(mat.code)}</pre>` : ""}</div>` : "";
    det.innerHTML = `<summary class="module-title"><span class="mod-num">${mi + 1}</span><span class="mod-name">${m.name}</span><span class="mod-count">${doneN}/${m.items.length}</span></summary>${learn}<div class="lesson-list"></div>`;
    const list = det.querySelector(".lesson-list");
    m.items.forEach((l) => {
      const done = !!state.completed[l.id]; const diff = (l.difficulty || "Easy").toLowerCase();
      const row = document.createElement("div"); row.className = "lesson-row" + (done ? " done" : ""); row.dataset.title = l.title.toLowerCase();
      row.innerHTML = `<div class="lesson-num">${done ? "✓" : "▷"}</div><div class="lesson-info"><h4>${esc(l.title)}</h4><div class="meta"><span class="pill ${diff}">${l.difficulty}</span></div></div><div class="lesson-xp">+${l.xp} XP</div>`;
      row.onclick = () => go("lesson", { track: t.id, id: l.id });
      list.appendChild(row);
    });
    wrap.appendChild(det);
  });
  $("lessonSearch").oninput = (e) => {
    const q = e.target.value.trim().toLowerCase();
    wrap.querySelectorAll(".module-block").forEach((det) => {
      let any = false;
      det.querySelectorAll(".lesson-row").forEach((row) => { const hit = !q || row.dataset.title.includes(q); row.style.display = hit ? "" : "none"; if (hit) any = true; });
      det.style.display = any ? "" : "none"; if (q) det.open = true;
    });
  };
}

/* ============================================================ AUTH (login / register) */
function updateAuthSlot() {
  const el = $("authSlot"); if (!el) return;
  const name = displayName();
  if (name) el.innerHTML = `<span class="auth-user" title="Logged in">👤 ${esc(name)}</span><a class="auth-link" id="logoutBtn">Log out</a>`;
  else el.innerHTML = `<a class="btn ghost auth-cta" id="signinBtn">Sign in</a>`;
  const lo = $("logoutBtn"); if (lo) lo.onclick = () => { logoutUser(); toast("Logged out", "good"); render(); };
  const si = $("signinBtn"); if (si) si.onclick = () => go("auth", { mode: "login" });
}
function renderAuth(mode) {
  const isReg = mode === "register";
  app.innerHTML = `
    <div class="auth-wrap">
      <div class="auth-card">
        <div class="auth-logo">🎮</div>
        <h2 class="auth-title">${isReg ? "Create your account" : "Welcome back"}</h2>
        <p class="auth-sub">${isReg ? "Start your coding journey and track your XP, streaks and badges." : "Log in to continue your journey."}</p>
        <div class="auth-tabs"><button class="auth-tab ${!isReg ? "active" : ""}" id="tabLogin">Log in</button><button class="auth-tab ${isReg ? "active" : ""}" id="tabReg">Register</button></div>
        <label class="auth-label">Name</label>
        <input id="auName" class="auth-input" placeholder="e.g. codemaster" autocomplete="username" />
        <label class="auth-label">Password</label>
        <input id="auPass" type="password" class="auth-input" placeholder="••••••" autocomplete="${isReg ? "new-password" : "current-password"}" />
        ${isReg ? `<label class="auth-label">Confirm password</label><input id="auPass2" type="password" class="auth-input" placeholder="••••••" />` : ""}
        <div class="auth-err hidden" id="auErr"></div>
        <button class="btn primary auth-submit" id="auGo">${isReg ? "Create account" : "Log in"}</button>
        <div class="auth-alt">${isReg ? "Already have an account?" : "New here?"} <a id="auSwitch">${isReg ? "Log in" : "Create one"}</a></div>
        <div class="auth-guest"><a id="auGuest">Continue as guest →</a></div>
        <div class="auth-note">Accounts are stored locally in this browser (no server). Great for separate profiles on one device.</div>
      </div>
    </div>`;
  $("tabLogin").onclick = () => go("auth", { mode: "login" });
  $("tabReg").onclick = () => go("auth", { mode: "register" });
  $("auSwitch").onclick = () => go("auth", { mode: isReg ? "login" : "register" });
  $("auGuest").onclick = () => { logoutUser(); go("home"); };
  const showErr = (m) => { const e = $("auErr"); e.textContent = m; e.classList.remove("hidden"); };
  $("auGo").onclick = async () => {
    const goBtn = $("auGo"); goBtn.disabled = true;
    try {
      const name = $("auName").value, pass = $("auPass").value;
      if (isReg) {
        if (pass !== $("auPass2").value) return showErr("Passwords don't match.");
        const err = await registerUser(name, pass);
        if (err) return showErr(err);
        toast("Welcome, " + displayName() + "! 🎉", "good");
      } else {
        const err = await loginUser(name, pass);
        if (err) return showErr(err);
        toast("Welcome back, " + displayName() + "!", "good");
      }
      go("home");
    } finally { goBtn.disabled = false; }
  };
  $("auName").addEventListener("keydown", (e) => { if (e.key === "Enter") $("auPass").focus(); });
  $("auPass").addEventListener("keydown", (e) => { if (e.key === "Enter" && !isReg) $("auGo").click(); });
}

/* ============================================================ GUIDE (zero → advanced) */
let guideIdx = 0;
function renderGuide(trackId) {
  const t = C.find((x) => x.id === trackId); if (!t) return go("home");
  const g = t.guide || [];
  if (guideIdx >= g.length) guideIdx = 0;
  app.innerHTML = `
    <a class="back-link" id="back">← ${t.icon} ${t.name}</a>
    <div class="section-head"><h2>📚 ${t.name} — Full Guide</h2><span class="sub">${g.length} chapters · zero to advanced</span></div>
    <div class="guide-layout"><aside class="guide-toc" id="guideToc"></aside><div class="panel guide-content" id="guideContent"></div></div>`;
  $("back").onclick = () => go("track", { id: t.id });
  const toc = $("guideToc");
  g.forEach((ch, i) => { const a = document.createElement("a"); a.className = "toc-item"; a.textContent = ch.title; a.onclick = () => { guideIdx = i; paint(); window.scrollTo(0, 0); }; toc.appendChild(a); });
  function paint() {
    document.querySelectorAll(".toc-item").forEach((el, i) => el.classList.toggle("active", i === guideIdx));
    const ch = g[guideIdx];
    const code = (ch.examples && ch.examples.length) ? `<div class="guide-eg">Example${ch.examples.length > 1 ? "s" : ""} in ${t.name}</div>` + ch.examples.map((c) => `<pre class="guide-code">${esc(c)}</pre>`).join("") : "";
    const prev = guideIdx > 0 ? `<button class="btn ghost" id="gPrev">← Previous</button>` : "<span></span>";
    const next = guideIdx < g.length - 1 ? `<button class="btn primary" id="gNext">Next chapter →</button>` : `<button class="btn success" id="gDone">Start practicing →</button>`;
    $("guideContent").innerHTML = `<div class="guide-progress">Chapter ${guideIdx + 1} of ${g.length}</div><h2 class="guide-h">${esc(ch.title)}</h2><div class="guide-body">${mdBlock(ch.body)}</div>${code}<div class="guide-nav">${prev}${next}</div>`;
    const p = $("gPrev"); if (p) p.onclick = () => { guideIdx--; paint(); window.scrollTo(0, 0); };
    const n = $("gNext"); if (n) n.onclick = () => { guideIdx++; paint(); window.scrollTo(0, 0); };
    const d = $("gDone"); if (d) d.onclick = () => go("track", { id: t.id });
  }
  paint();
}

/* ============================================================ IDE shell (shared) */
function ideToolbar(t) {
  return `
  <div class="editor-toolbar">
    <span class="lang-tag">${t.icon} ${t.name}</span>
    <div class="tb-actions">
      <button class="tb-btn" id="fmtBtn" title="Format code">⤸</button>
      <button class="tb-btn" id="copyBtn" title="Copy code">⧉</button>
      <button class="tb-btn" id="dlBtn" title="Download code">⤓</button>
      <button class="tb-btn" id="setBtn" title="Editor settings">⚙</button>
      <button class="tb-btn" id="fsBtn" title="Toggle fullscreen">⛶</button>
      <button class="btn ghost" id="resetBtn">↺ Reset</button>
      <button class="btn primary" id="runBtn">▶ Run</button>
    </div>
    <div class="settings-pop hidden" id="setPop">
      <label>Theme
        <select id="setTheme">
          <option value="cq">Ironyx Dark</option>
          <option value="vs-dark">Midnight</option>
          <option value="hc-black">High Contrast</option>
          <option value="vs">Light</option>
        </select>
      </label>
      <label>Font size <span><button class="tb-btn" id="fontDown">−</button><b id="fontVal">${ide.font}</b><button class="tb-btn" id="fontUp">+</button></span></label>
      <label class="row"><input type="checkbox" id="setWrap"> Word wrap</label>
      <label class="row"><input type="checkbox" id="setMini"> Minimap</label>
    </div>
  </div>`;
}
function ioPanel() {
  return `
  <div class="panel io-panel">
    <div class="io-tabs">
      <button class="io-tab active" data-tab="out">Output</button>
      <button class="io-tab" data-tab="in">Input (stdin)</button>
      <button class="tb-btn io-clear" id="outClear" title="Clear output">🗑 Clear</button>
    </div>
    <div class="io-body">
      <div id="outPane">
        <div class="output-head"><span class="dot" id="outDot"></span><span class="status" id="outStatus">Ready</span><span class="exec-time" id="execTime"></span></div>
        <div class="output-body terminal" id="outBody">$ Press Run (or ⌘/Ctrl+Enter) to execute.</div>
      </div>
      <textarea id="stdinBox" class="stdin-box hidden" placeholder="Type input your program reads from stdin..."></textarea>
    </div>
  </div>`;
}
function statusBar(t) {
  const eng = ENGINE_LABEL[t.engine] || ENGINE_LABEL.server;
  return `<div class="ide-status"><span id="curPos">Ln 1, Col 1</span><span id="curLen">0 chars</span><span class="sb-sep"></span><span>${t.name}</span><span class="engine-badge ${eng.cls} sb-eng">${eng.txt}</span></div>`;
}
function wireIde(t, lesson) {
  wireIoTabs();
  $("resetBtn").onclick = () => editor && editor.setValue((lesson ? lesson.starter : (t.lessons[0] && t.lessons[0].starter)) || "");
  $("fmtBtn").onclick = () => editor && editor.getAction("editor.action.formatDocument") && editor.getAction("editor.action.formatDocument").run();
  $("copyBtn").onclick = async () => { try { await navigator.clipboard.writeText(editor.getValue()); toast("Code copied", "good"); } catch { toast("Copy failed", "bad"); } };
  $("dlBtn").onclick = () => { const blob = new Blob([editor.getValue()], { type: "text/plain" }); const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "main." + (EXT[t.lang] || "txt"); a.click(); };
  $("setBtn").onclick = () => $("setPop").classList.toggle("hidden");
  $("fsBtn").onclick = () => { document.querySelector(".workspace").classList.toggle("ide-fs"); setTimeout(() => editor && editor.layout(), 60); };
  $("outClear").onclick = () => setOutput("Ready", "$ ", "");
  $("setTheme").value = ide.theme; $("setWrap").checked = ide.wrap; $("setMini").checked = ide.minimap;
  $("setTheme").onchange = (e) => { ide.theme = e.target.value; applyIde(); };
  $("setWrap").onchange = (e) => { ide.wrap = e.target.checked; applyIde(); };
  $("setMini").onchange = (e) => { ide.minimap = e.target.checked; applyIde(); };
  $("fontUp").onclick = () => { ide.font = Math.min(26, ide.font + 1); $("fontVal").textContent = ide.font; applyIde(); };
  $("fontDown").onclick = () => { ide.font = Math.max(10, ide.font - 1); $("fontVal").textContent = ide.font; applyIde(); };
}
function applyIde() {
  if (!editor) return;
  editor.updateOptions({ fontSize: ide.font, wordWrap: ide.wrap ? "on" : "off", minimap: { enabled: ide.minimap } });
  monaco.editor.setTheme(ide.theme); saveIde();
}

/* ============================================================ LESSON */
let editor = null;
function renderLesson(trackId, lessonId) {
  const t = C.find((x) => x.id === trackId);
  const l = t && t.lessons.find((x) => x.id === lessonId); if (!l) return go("home");
  const idx = t.lessons.indexOf(l), next = t.lessons[idx + 1];
  const diff = (l.difficulty || "Easy").toLowerCase();
  app.innerHTML = `
    <a class="back-link" id="back">← ${t.icon} ${t.name}</a>
    <div class="workspace">
      <div class="panel brief-panel">
        <div class="ltitle">${l.title}</div>
        <div class="lmeta"><span class="pill ${diff}">${l.difficulty}</span><span class="lesson-xp">+${l.xp} XP</span></div>
        <div class="brief-body">${mdInline(l.brief)}</div>
        ${l.explanation ? `<div class="explain"><div class="explain-head">📖 How it works</div><div class="explain-body">${mdInline(l.explanation)}</div></div>` : ""}
        <details class="hint-box"><summary>💡 Show solution</summary><pre class="hint-code">${esc(l.hint || "")}</pre></details>
      </div>
      <div class="editor-col">
        <div class="panel editor-panel">${ideToolbar(t)}<div id="monaco"></div>${statusBar(t)}</div>
        ${ioPanel()}
      </div>
    </div>`;
  $("back").onclick = () => go("track", { id: t.id });
  mountEditor(monacoLang(t.lang), l.starter, "cq_code_" + l.id);
  wireIde(t, l);
  $("runBtn").onclick = () => runAndCheck(t, l, next);
}

/* ============================================================ PLAYGROUND */
function renderPlayground() {
  const first = C[0];
  app.innerHTML = `
    <div class="section-head"><h2>⌨️ IDE Playground</h2><span class="sub">Write & run any language</span></div>
    <div class="pg-controls"><select class="lang-select" id="pgLang">${C.map((t) => `<option value="${t.id}">${t.icon} ${t.name}</option>`).join("")}</select></div>
    <div class="workspace" style="grid-template-columns:1fr;">
      <div class="editor-col">
        <div class="panel editor-panel" style="min-height:440px;">${ideToolbar(first)}<div id="monaco"></div>${statusBar(first)}</div>
        ${ioPanel()}
      </div>
    </div>`;
  mountEditor(monacoLang(first.lang), first.lessons[0].starter);
  wireIde(first, null);
  const sel = $("pgLang");
  const refreshFor = (t) => {
    $("runBtn").onclick = () => runRaw(t, editor.getValue());
    document.querySelector(".lang-tag").innerHTML = `${t.icon} ${t.name}`;
    const eng = ENGINE_LABEL[t.engine] || ENGINE_LABEL.server; const e = document.querySelector(".sb-eng"); e.className = "engine-badge " + eng.cls + " sb-eng"; e.textContent = eng.txt;
    $("resetBtn").onclick = () => editor.setValue(t.lessons[0].starter);
    $("dlBtn").onclick = () => { const blob = new Blob([editor.getValue()], { type: "text/plain" }); const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "main." + (EXT[t.lang] || "txt"); a.click(); };
  };
  refreshFor(first);
  sel.onchange = () => { const t = C.find((x) => x.id === sel.value); monaco.editor.setModelLanguage(editor.getModel(), monacoLang(t.lang)); editor.setValue(t.lessons[0].starter); refreshFor(t); };
}

/* ============================================================ LEADERBOARD */
/* ============================================================ LEADERBOARD (leagues + podium + tabs) */
const LEAGUES = [["Bronze", "🥉", 0], ["Silver", "🥈", 300], ["Gold", "🥇", 1000], ["Platinum", "💠", 3000], ["Diamond", "💎", 7000]];
function leagueOf(xp) { let idx = 0; LEAGUES.forEach((L, i) => { if (xp >= L[2]) idx = i; }); return idx; }
const BADGE_EMOJI = { first: "🥇", streak3: "🔥", ten: "🏅", fifty: "💎", twohundred: "👑" };
const LB_BOTS = [
  { n: "ByteWizard", a: "🧙", all: 9240, wk: 820 }, { n: "NullPointer", a: "👾", all: 7110, wk: 410 },
  { n: "RecursiveRae", a: "🦊", all: 5980, wk: 910 }, { n: "AsyncAndy", a: "🤖", all: 4820, wk: 305 },
  { n: "BigOBeth", a: "🐯", all: 4120, wk: 680 }, { n: "LoopLisa", a: "🐧", all: 3360, wk: 540 },
  { n: "HeapHenry", a: "🦉", all: 2740, wk: 220 }, { n: "RegexRiya", a: "🦄", all: 2210, wk: 760 },
  { n: "StackSue", a: "🐙", all: 1730, wk: 180 }, { n: "MergeMax", a: "🐳", all: 1420, wk: 430 },
  { n: "PointerPat", a: "🦅", all: 1180, wk: 150 }, { n: "KernelKai", a: "🐲", all: 940, wk: 360 },
  { n: "SyntaxSam", a: "🐝", all: 720, wk: 90 }, { n: "CacheCleo", a: "🦝", all: 540, wk: 280 },
  { n: "BinaryBo", a: "🐰", all: 360, wk: 120 }, { n: "ScriptSky", a: "🐨", all: 220, wk: 200 },
  { n: "TokenTom", a: "🦔", all: 130, wk: 60 }, { n: "NoobNeo", a: "🐣", all: 60, wk: 40 },
];
let lbTab = "all";
function renderLeaderboard() {
  const key = lbTab === "all" ? "all" : "wk";
  const you = { n: "You", a: "🎮", all: state.xp, wk: state.xp, you: true };
  const players = [you]; // real standing only — no fake competitors
  const myRank = players.findIndex((p) => p.you) + 1;
  const li = leagueOf(state.xp), league = LEAGUES[li], nextL = LEAGUES[li + 1];
  const toNext = nextL ? Math.max(0, nextL[2] - state.xp) : 0;
  const pct = nextL ? Math.min(100, Math.round(((state.xp - league[2]) / (nextL[2] - league[2])) * 100)) : 100;
  const top3 = players.slice(0, 3);
  const badges = Object.keys(state.badges || {});
  app.innerHTML = `
    <div class="section-head"><h2>🏆 Your Standing</h2><span class="sub">${league[0]} League · Level ${levelFor(state.xp)}</span></div>
    <div class="lb-hero">
      <div class="lb-league">
        <div class="lb-league-badge">${league[1]}</div>
        <div class="lb-league-info"><div class="lb-league-name">${league[0]} League</div>
          <div class="lb-league-sub">${nextL ? `${toNext} XP to <b>${nextL[0]}</b> ${nextL[1]}` : "Top league — you're a legend!"}</div>
          <div class="lb-progress"><span style="width:${pct}%"></span></div></div>
      </div>
      <div class="lb-mystats">
        <div class="lb-stat"><div class="num">#${myRank}</div><div class="lbl">Rank</div></div>
        <div class="lb-stat"><div class="num">Lv ${levelFor(state.xp)}</div><div class="lbl">Level</div></div>
        <div class="lb-stat"><div class="num">${state.xp}</div><div class="lbl">XP</div></div>
        <div class="lb-stat"><div class="num">${completedCount()}</div><div class="lbl">Solved</div></div>
      </div>
    </div>
    <div class="lb-tabs"><button class="lb-tabbtn ${lbTab === "all" ? "active" : ""}" data-t="all">All-Time</button><button class="lb-tabbtn ${lbTab === "week" ? "active" : ""}" data-t="week">This Week</button></div>
    <div class="lb-podium">${[1, 0, 2].map((rank) => { const p = top3[rank]; if (!p) return ""; const cls = ["first", "second", "third"][rank]; return `<div class="podium ${cls} ${p.you ? "you" : ""}"><div class="lb-avatar big">${p.a}</div><div class="medal">${["🥇", "🥈", "🥉"][rank]}</div><div class="pname">${p.n}</div><div class="pxp">${p[key].toLocaleString()} XP</div></div>`; }).join("")}</div>
    <div class="lb-card">${players.map((p, i) => { const mv = p.you ? 0 : ((i * 3 + 1) % 5) - 2; const arrow = mv > 0 ? `<span class="mv up">▲${mv}</span>` : mv < 0 ? `<span class="mv down">▼${-mv}</span>` : `<span class="mv">–</span>`; const L = LEAGUES[leagueOf(p[key])]; return `<div class="lb-row ${p.you ? "you" : ""}"><div class="lb-rank ${i < 3 ? "top" : ""}">${i + 1}</div><div class="lb-avatar">${p.a}</div><div class="lb-name">${p.n}${p.you ? ` · Lv ${levelFor(state.xp)}` : ""}<div class="lb-league-mini">${L[1]} ${L[0]}</div></div>${arrow}<div class="lb-xp">${p[key].toLocaleString()} XP</div></div>`; }).join("")}</div>
    ${badges.length ? `<div class="section-head"><h2>🎖 Your Badges</h2><span class="sub">${badges.length} unlocked</span></div><div class="lb-badges">${badges.map((b) => `<div class="badge-chip" title="${esc(b)}">${BADGE_EMOJI[b] || (b.startsWith("track-") ? "📘" : "🏅")}</div>`).join("")}</div>` : `<div class="lb-empty">Solve challenges to earn badges and climb the leagues! 🚀</div>`}`;
  document.querySelectorAll(".lb-tabbtn").forEach((b) => (b.onclick = () => { lbTab = b.dataset.t; renderLeaderboard(); }));
}

/* ---------- IO tabs ---------- */
function wireIoTabs() {
  document.querySelectorAll(".io-tab").forEach((tab) => {
    tab.onclick = () => {
      document.querySelectorAll(".io-tab").forEach((x) => x.classList.remove("active"));
      tab.classList.add("active");
      const showIn = tab.dataset.tab === "in";
      $("outPane").classList.toggle("hidden", showIn);
      $("stdinBox").classList.toggle("hidden", !showIn);
    };
  });
}
function getStdin() { const b = $("stdinBox"); return b ? b.value : ""; }

/* ============================================================ Monaco */
let monacoReady = null;
function ensureMonaco() {
  if (monacoReady) return monacoReady;
  monacoReady = new Promise((resolve) => {
    require.config({ paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs" } });
    require(["vs/editor/editor.main"], () => {
      monaco.editor.defineTheme("cq", { base: "vs-dark", inherit: true, rules: [{ token: "comment", foreground: "6b7394", fontStyle: "italic" }], colors: { "editor.background": "#0e1120", "editor.lineHighlightBackground": "#161a2d" } });
      resolve();
    });
  });
  return monacoReady;
}
async function mountEditor(language, value, saveKey) {
  await ensureMonaco();
  const el = $("monaco"); if (!el) return;
  if (editor) { editor.dispose(); editor = null; }
  let initial = value;
  if (saveKey) { const s = localStorage.getItem(saveKey); if (s != null && s !== "") initial = s; }
  editor = monaco.editor.create(el, {
    value: initial, language, theme: ide.theme, fontSize: ide.font, fontFamily: "JetBrains Mono, monospace",
    minimap: { enabled: ide.minimap }, wordWrap: ide.wrap ? "on" : "off", automaticLayout: true,
    scrollBeyondLastLine: false, padding: { top: 12 }, tabSize: 2, smoothScrolling: true,
    cursorBlinking: "smooth", bracketPairColorization: { enabled: true }, renderLineHighlight: "all",
    suggestOnTriggerCharacters: true, quickSuggestions: true,
  });
  editor.onDidChangeCursorPosition((e) => { const p = $("curPos"); if (p) p.textContent = `Ln ${e.position.lineNumber}, Col ${e.position.column}`; });
  editor.onDidChangeModelContent(() => { const c = $("curLen"); if (c) c.textContent = editor.getValue().length + " chars"; if (saveKey) localStorage.setItem(saveKey, editor.getValue()); });
  const c0 = $("curLen"); if (c0) c0.textContent = initial.length + " chars";
  editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => { const b = $("runBtn"); if (b) b.click(); });
}
function monacoLang(l) {
  const map = { javascript: "javascript", typescript: "typescript", python: "python", java: "java", c: "c", "c++": "cpp", csharp: "csharp", go: "go", rust: "rust", ruby: "ruby", php: "php", swift: "swift", kotlin: "kotlin", bash: "shell", lua: "lua", perl: "perl", dart: "dart", scala: "scala", haskell: "plaintext", elixir: "plaintext", r: "r", julia: "plaintext", clojure: "clojure", sqlite3: "sql", html: "html", css: "css", scss: "scss", json: "json", yaml: "yaml", markdown: "markdown", xml: "xml", dockerfile: "dockerfile", graphql: "graphql" };
  return map[l] || "plaintext";
}

/* ============================================================ COMPILER (engines) */
async function runEngine(track, source, stdin) {
  const t0 = performance.now(); let res;
  if (track.engine === "pyodide") res = await runPython(source, stdin);
  else if (track.engine === "js") res = await runJsWorker(source, stdin, false);
  else if (track.engine === "ts") res = await runJsWorker(source, stdin, true);
  else res = await runServer(track.lang, source, stdin);
  res.ms = Math.round(performance.now() - t0); return res;
}
let pyodidePromise = null;
function loadPyodide_() {
  if (pyodidePromise) return pyodidePromise;
  pyodidePromise = new Promise((resolve, reject) => {
    const s = document.createElement("script"); s.src = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js";
    s.onload = async () => { try { resolve(await loadPyodide()); } catch (e) { reject(e); } };
    s.onerror = () => reject(new Error("Failed to load Python engine (network).")); document.head.appendChild(s);
  });
  return pyodidePromise;
}
async function runPython(source, stdin) {
  setOutput("Loading Python engine…", "$ First run downloads the Python runtime (~5MB); then it's instant.");
  let py; try { py = await loadPyodide_(); } catch (e) { return { stdout: "", stderr: e.message, code: 1 }; }
  let out = ""; py.setStdout({ batched: (s) => (out += s + "\n") }); py.setStderr({ batched: (s) => (out += s + "\n") });
  if (stdin) { const lines = stdin.split("\n"); let i = 0; py.setStdin({ stdin: () => (i < lines.length ? lines[i++] : "") }); }
  let err = "", code = 0; try { await py.runPythonAsync(source); } catch (e) { err = String(e.message || e); code = 1; }
  return { stdout: out, stderr: err, code };
}
let tsPromise = null;
function loadTS() {
  if (tsPromise) return tsPromise;
  tsPromise = new Promise((resolve, reject) => { const s = document.createElement("script"); s.src = "https://cdn.jsdelivr.net/npm/typescript@5.4.5/lib/typescript.min.js"; s.onload = () => resolve(window.ts); s.onerror = () => reject(new Error("Failed to load TypeScript compiler.")); document.head.appendChild(s); });
  return tsPromise;
}
async function runJsWorker(source, stdin, isTs) {
  let code = source;
  if (isTs) { try { const ts = await loadTS(); code = ts.transpile(source, { target: ts.ScriptTarget.ES2020 }); } catch (e) { return { stdout: "", stderr: e.message, code: 1 }; } }
  const workerSrc = `
    // Sandbox hardening: user code runs with no network or script-import access.
    const __blocked = (n) => () => { throw new Error(n + " is disabled in the sandbox."); };
    self.importScripts = __blocked("importScripts");
    self.fetch = () => Promise.reject(new Error("Network access is disabled in the sandbox."));
    self.XMLHttpRequest = __blocked("XMLHttpRequest");
    self.WebSocket = __blocked("WebSocket");
    self.EventSource = __blocked("EventSource");
    let __out = "";
    const __inputLines = ${JSON.stringify((stdin || "").split("\n"))}; let __ic = 0;
    const prompt = () => (__ic < __inputLines.length ? __inputLines[__ic++] : "");
    const console = { log:(...a)=>{__out+=a.map(String).join(" ")+"\\n";}, error:(...a)=>{__out+=a.map(String).join(" ")+"\\n";}, warn:(...a)=>{__out+=a.map(String).join(" ")+"\\n";}, info:(...a)=>{__out+=a.map(String).join(" ")+"\\n";} };
    self.onmessage = (e) => { try { eval(e.data); self.postMessage({ stdout: __out, stderr: "", code: 0 }); } catch (err) { self.postMessage({ stdout: __out, stderr: String(err && err.stack || err), code: 1 }); } };`;
  return new Promise((resolve) => {
    const blob = new Blob([workerSrc], { type: "application/javascript" }); const w = new Worker(URL.createObjectURL(blob));
    const timer = setTimeout(() => { w.terminate(); resolve({ stdout: "", stderr: "⏱ Timed out (possible infinite loop).", code: 124 }); }, 8000);
    w.onmessage = (e) => { clearTimeout(timer); w.terminate(); resolve(e.data); };
    w.onerror = (e) => { clearTimeout(timer); w.terminate(); resolve({ stdout: "", stderr: e.message, code: 1 }); };
    w.postMessage(code);
  });
}
async function runWandboxBrowser(language, source, stdin) {
  if (!wandboxList) await preloadWandbox();
  const compiler = pickWandboxCompiler(language);
  if (!compiler) return { stdout: "", stderr: "", code: 1, offline: true };
  // Wandbox saves Java as prog.java, so `public class Main` must lose `public`.
  let code = source;
  if (language === "java") code = code.replace(/\bpublic\s+(class|interface|enum)\s+/g, "$1 ");
  const ctrl = new AbortController(); const id = setTimeout(() => ctrl.abort(), 40000);
  try {
    const res = await fetch(`${WANDBOX_API}/compile.json`, {
      method: "POST", headers: { "Content-Type": "application/json" }, signal: ctrl.signal,
      body: JSON.stringify({ compiler, code, stdin: stdin || "" }),
    });
    if (!res.ok) return { stdout: "", stderr: `public engine HTTP ${res.status}`, code: 1 };
    const d = await res.json();
    const exit = typeof d.status === "string" ? parseInt(d.status, 10) || 0 : (d.status || 0);
    return { stdout: d.program_output || "", stderr: (d.compiler_error || "") + (d.program_error || ""), code: exit };
  } catch (e) {
    if (e.name === "AbortError") return { stdout: "", stderr: "⏱ Timed out (possible infinite loop or slow network).", code: 124 };
    return { stdout: "", stderr: e.message, code: 1, offline: true };
  } finally { clearTimeout(id); }
}
async function runServer(language, source, stdin) {
  if (serverEngineReady === null) await pingServer();
  // 1) Local Node backend (the bundled Docker stack: Piston → Wandbox).
  if (serverEngineReady) {
    try {
      const res = await fetch("/api/execute", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ language, source, stdin }) });
      const data = await res.json();
      if (res.ok) { const run = data.run || {}, comp = data.compile || {}; return { stdout: run.stdout || "", stderr: (comp.stderr || "") + (run.stderr || ""), code: run.code ?? 0 }; }
      // server reachable but errored → fall through to the public engine
    } catch (_) { serverEngineReady = false; }
  }
  // 2) Browser-direct public engine — works on static hosting (WordPress, Netlify, S3…) with no Node server.
  return runWandboxBrowser(language, source, stdin);
}

/* ---------- run helpers ---------- */
function setOutput(status, body, kind = "", ms) {
  const dot = $("outDot"), st = $("outStatus"), bd = $("outBody"), et = $("execTime"); if (!bd) return;
  dot.className = "dot" + (kind === "ok" ? " ok" : kind === "err" ? " err" : "");
  st.textContent = status; bd.innerHTML = body; if (et) et.textContent = ms != null ? `${ms} ms` : "";
}
function runningUI() {
  const btn = $("runBtn"); if (btn) { btn.disabled = true; btn.dataset.html = btn.innerHTML; btn.innerHTML = '<span class="spinner"></span> Running'; }
  document.querySelector(".io-tab[data-tab=out]")?.click();
  setOutput("Running…", "$ Executing your code…"); return btn;
}
function restoreBtn(btn) { if (btn) { btn.disabled = false; btn.innerHTML = btn.dataset.html; } }
function esc(s) { return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
function offlineMsg(track) { return `<span class="err">Couldn't reach a runtime for "${track.name}" right now.</span>\n\nPython, JavaScript & TypeScript always run in your browser — no setup.\nOther languages use the free public engine automatically (needs internet).\n\nIf you're offline, or want every language to run locally, start the bundled engine:\n\n  <b>docker compose up --build</b>\n\nthen reload. (See README.)`; }

async function runRaw(track, source) {
  if (track.engine === "web" || track.engine === "static") return runWebPreview(track, source);
  const btn = runningUI();
  try {
    const r = await runEngine(track, source, getStdin());
    if (r.offline) { setOutput("Engine offline", offlineMsg(track), "err"); return; }
    const body = esc((r.stdout || "") + (r.stderr || "")) || "(no output)";
    setOutput(r.code === 0 ? "Success ✓" : "Finished with errors", body, r.code === 0 ? "ok" : "err", r.ms);
  } finally { restoreBtn(btn); }
}
async function runAndCheck(track, lesson, next) {
  if (track.engine === "web" || track.engine === "static") return runWebCheck(track, lesson, next);
  const btn = runningUI();
  try {
    const r = await runEngine(track, editor.getValue(), getStdin());
    if (r.offline) { setOutput("Engine offline", offlineMsg(track), "err"); toast("Start the engine with Docker for this language.", "bad"); return; }
    const combined = (r.stdout || "") + (r.stderr || "");
    const trimmed = (r.stdout || "").replace(/\s+$/g, "").trim();
    let pass = false;
    if (lesson.expectedOutput != null) pass = trimmed === lesson.expectedOutput.trim();
    else if (lesson.expectedContains != null) pass = trimmed.includes(lesson.expectedContains);
    const display = esc(combined || "(no output)");
    if (pass) {
      const nextBtn = next ? `\n<button class="btn success" id="nextBtn" style="margin-top:12px">Next challenge →</button>` : "";
      setOutput("Correct! ✅", `<span class="ok">${display}</span>${nextBtn}`, "ok", r.ms);
      const nb = $("nextBtn"); if (nb) nb.onclick = () => go("lesson", { track: track.id, id: next.id });
      awardLesson(track, lesson);
    } else {
      const expected = lesson.expectedOutput != null ? lesson.expectedOutput : "(must contain) " + lesson.expectedContains;
      setOutput("Not quite ❌", `${display}\n\n<span class="err">Expected:\n${esc(expected)}</span>`, "err", r.ms);
      toast("Not quite — compare with the expected output.", "bad");
    }
  } finally { restoreBtn(btn); }
}

/* ---------- web / markup engines (token grading + live preview) ---------- */
function tokenGrade(lesson, src) {
  const s = (src || "").toLowerCase();
  const toks = lesson.expectedAll || (lesson.expectedContains ? [lesson.expectedContains] : []);
  const missing = toks.filter((t) => !s.includes(String(t).toLowerCase()));
  return { pass: missing.length === 0, missing, toks };
}
function previewDoc(track, src) {
  if (track.lang === "css" || track.lang === "scss")
    return `<style>body{font-family:Inter,sans-serif;padding:16px;background:#fff}</style><style>${src}</style>` +
      `<div class="card"><h1>Heading</h1><p>Paragraph text goes here.</p><button class="btn">Button</button> <a href="#">Link</a><div class="box" style="background:#eee;margin-top:8px">Box</div><div class="avatar" style="width:48px;height:48px;background:#bbb;margin-top:8px"></div><div class="row"><span>A</span><span>B</span></div></div>`;
  return src;
}
async function runWebPreview(track, source) {
  const btn = runningUI();
  try {
    if (track.engine === "web") {
      setOutput("Preview", `<iframe id="cqPreview" class="preview"></iframe>`, "ok");
      const f = $("cqPreview"); if (f) f.srcdoc = previewDoc(track, source);
    } else {
      setOutput("Your code", esc(source || "(empty)"), "");
    }
  } finally { restoreBtn(btn); }
}
async function runWebCheck(track, lesson, next) {
  const btn = runningUI();
  try {
    const src = editor.getValue();
    const g = tokenGrade(lesson, src);
    const preview = track.engine === "web" ? `<iframe id="cqPreview" class="preview"></iframe>` : "";
    if (g.pass) {
      const nextBtn = next ? `\n<button class="btn success" id="nextBtn" style="margin-top:12px">Next challenge →</button>` : "";
      setOutput("Correct! ✅", `${preview}<span class="ok">✓ All checks passed.</span>${nextBtn}`, "ok");
      const f = $("cqPreview"); if (f) f.srcdoc = previewDoc(track, src);
      const nb = $("nextBtn"); if (nb) nb.onclick = () => go("lesson", { track: track.id, id: next.id });
      awardLesson(track, lesson);
    } else {
      setOutput("Not quite ❌", `${preview}<span class="err">Your code still needs: ${g.missing.map((m) => "<code>" + esc(m) + "</code>").join(", ")}</span>`, "err");
      const f = $("cqPreview"); if (f) f.srcdoc = previewDoc(track, src);
      toast("Add the missing pieces.", "bad");
    }
  } finally { restoreBtn(btn); }
}

/* ============================================================ Rewards */
function awardLesson(track, lesson) {
  const already = !!state.completed[lesson.id]; touchStreak();
  if (already) { toast("Solved again! (already completed)", "good"); return; }
  const prev = levelFor(state.xp);
  state.completed[lesson.id] = true; state.xp += lesson.xp; const now = levelFor(state.xp); save(); checkBadges(track);
  if (now > prev) showModal("⭐", `Level ${now}!`, `+${lesson.xp} XP — you reached level ${now}. Keep going!`);
  else toast(`✅ Solved! +${lesson.xp} XP`, "good");
}
function checkBadges(track) {
  const grant = (id, e, ti, tx) => { if (state.badges[id]) return; state.badges[id] = true; save(); setTimeout(() => showModal(e, ti, tx), 400); };
  if (completedCount() === 1) grant("first", "🥇", "First Solve!", "Welcome to Ironyx Code!");
  if (track.lessons.every((l) => state.completed[l.id])) grant("track-" + track.id, track.icon, `${track.name} Master`, `You finished every ${track.name} challenge!`);
  if (state.streak >= 3) grant("streak3", "🔥", "On Fire!", "3-day streak reached.");
  if (completedCount() >= 10) grant("ten", "🏅", "Double Digits", "10 challenges solved!");
  if (completedCount() >= 50) grant("fifty", "💎", "Half Century", "50 challenges solved!");
  if (completedCount() >= 200) grant("twohundred", "👑", "Code Royalty", "200 challenges solved. Incredible!");
}

/* ============================================================ UI helpers */
let toastTimer;
function toast(msg, kind = "") { const t = $("toast"); t.textContent = msg; t.className = "toast show " + kind; clearTimeout(toastTimer); toastTimer = setTimeout(() => (t.className = "toast " + kind), 2600); }
function showModal(e, ti, tx) { $("modalEmoji").textContent = e; $("modalTitle").textContent = ti; $("modalText").textContent = tx; $("modal").classList.remove("hidden"); }
$("modalClose").onclick = () => $("modal").classList.add("hidden");
function mdInline(s) { return esc(s).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>").replace(/\n/g, "<br>"); }
function inlineMd(s) { return s.replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>"); }
function mdBlock(s) {
  const lines = esc(s).split("\n"); let html = "", inUl = false;
  for (const line of lines) {
    const hm = line.match(/^\s*(#{2,4})\s+(.*)/);
    if (hm) { if (inUl) { html += "</ul>"; inUl = false; } html += '<h4 class="guide-sub">' + inlineMd(hm[2]) + "</h4>"; continue; }
    if (/^\s*-\s+/.test(line)) { if (!inUl) { html += "<ul>"; inUl = true; } html += "<li>" + inlineMd(line.replace(/^\s*-\s+/, "")) + "</li>"; continue; }
    if (inUl) { html += "</ul>"; inUl = false; }
    if (line.trim() === "") continue;
    html += "<p>" + inlineMd(line) + "</p>";
  }
  if (inUl) html += "</ul>";
  return html;
}

/* ---------- boot ---------- */
refreshChip(); pingServer(); preloadWandbox(); render();
/* Warm up the Python engine loader during idle time (no-op if never used). */
(function () {
  const prefetch = () => { const l = document.createElement("link"); l.rel = "prefetch"; l.as = "script"; l.href = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js"; document.head.appendChild(l); };
  if ("requestIdleCallback" in window) requestIdleCallback(prefetch, { timeout: 4000 }); else setTimeout(prefetch, 2500);
})();
