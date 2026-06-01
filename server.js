/**
 * Ironyx Code server — advanced multi-backend code execution.
 * Backend chain for /api/execute (first that succeeds wins):
 *   1) Piston   — self-hosted engine (docker compose). Supports all 24 langs.
 *   2) Wandbox  — free public API (no key). Covers most compiled languages.
 * (Python, JavaScript and TypeScript run in the browser — never reach this server.)
 * No API keys required. Node 18+ (built-in fetch).
 *
 * Security & performance:
 *   - gzip compression, long-lived static caching, ETags
 *   - hardened HTTP headers (CSP, nosniff, referrer/permissions policy)
 *   - strict input validation + size caps on /api/execute
 *   - simple in-memory per-IP rate limiting
 *   - generic client errors (details are logged server-side only)
 */
const express = require("express");
const compression = require("compression");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
const PISTON_URL = process.env.PISTON_URL || "http://localhost:2000/api/v2";
const WANDBOX_URL = process.env.WANDBOX_URL || "https://wandbox.org/api";
const ENABLE_WANDBOX = (process.env.ENABLE_WANDBOX || "true") !== "false";
const IS_PROD = process.env.NODE_ENV === "production";

// Limits (overridable via env)
const MAX_SOURCE = parseInt(process.env.MAX_SOURCE_BYTES || "200000", 10); // 200 KB
const MAX_STDIN = parseInt(process.env.MAX_STDIN_BYTES || "100000", 10);    // 100 KB
const RL_WINDOW_MS = parseInt(process.env.RATE_WINDOW_MS || "60000", 10);   // 1 min
const RL_MAX = parseInt(process.env.RATE_MAX || "40", 10);                  // 40 runs/min/IP

app.disable("x-powered-by");
app.set("trust proxy", true);
app.use(compression());
app.use(express.json({ limit: "1mb" }));

/* ---------------- security headers ---------------- */
/* Note: framing is intentionally allowed (no X-Frame-Options / frame-ancestors)
   so the app can be embedded via <iframe> on a WordPress page. */
app.use((req, res, next) => {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
  res.setHeader("Permissions-Policy", "geolocation=(), microphone=(), camera=(), payment=()");
  res.setHeader("Cross-Origin-Resource-Policy", "cross-origin");
  res.setHeader(
    "Content-Security-Policy",
    [
      "default-src 'self'",
      // Pyodide/Monaco/TypeScript load from jsDelivr; Pyodide needs eval + WASM.
      "script-src 'self' 'unsafe-inline' 'unsafe-eval' 'wasm-unsafe-eval' https://cdn.jsdelivr.net blob:",
      "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net",
      "font-src 'self' data: https://fonts.gstatic.com https://cdn.jsdelivr.net",
      "img-src 'self' data: blob:",
      // The browser talks directly to Wandbox; Pyodide/Monaco fetch assets from jsDelivr.
      "connect-src 'self' https://wandbox.org https://cdn.jsdelivr.net",
      "worker-src 'self' blob:",
      "child-frame-src 'self' blob:",
      "frame-src 'self' blob:",
      "object-src 'none'",
      "base-uri 'self'",
    ].join("; ")
  );
  next();
});

/* ---------------- static assets (cached) ---------------- */
app.use(
  express.static(path.join(__dirname, "public"), {
    etag: true,
    lastModified: true,
    maxAge: "7d",
    setHeaders(res, filePath) {
      // index.html must always be revalidated so updates show up immediately.
      if (filePath.endsWith("index.html")) res.setHeader("Cache-Control", "no-cache");
    },
  })
);

const withTimeout = (ms) => {
  const c = new AbortController();
  const id = setTimeout(() => c.abort(), ms);
  return { signal: c.signal, done: () => clearTimeout(id) };
};

/* ---------------- Piston ---------------- */
let runtimeCache = null, runtimeCacheTime = 0;
async function getRuntimes() {
  const now = Date.now();
  if (runtimeCache && now - runtimeCacheTime < 3600000) return runtimeCache;
  const t = withTimeout(6000);
  try {
    const res = await fetch(`${PISTON_URL}/runtimes`, { signal: t.signal });
    if (!res.ok) throw new Error(`runtimes ${res.status}`);
    runtimeCache = await res.json(); runtimeCacheTime = now; return runtimeCache;
  } finally { t.done(); }
}
async function pistonExecute({ language, version, source, stdin }) {
  const find = (rt) => rt.find((r) => r.language === language || (r.aliases || []).includes(language));
  let useVersion = version;
  if (!useVersion) {
    let m = find(await getRuntimes());
    if (!m) { runtimeCacheTime = 0; m = find(await getRuntimes()); }
    if (!m) throw new Error(`piston: language ${language} not installed`);
    useVersion = m.version;
  }
  const t = withTimeout(20000);
  try {
    const r = await fetch(`${PISTON_URL}/execute`, {
      method: "POST", headers: { "Content-Type": "application/json" }, signal: t.signal,
      body: JSON.stringify({ language, version: useVersion, files: [{ content: source }], stdin, compile_timeout: 10000, run_timeout: 8000 }),
    });
    if (!r.ok) throw new Error(`piston execute ${r.status}`);
    const d = await r.json();
    return { backend: "piston", compile: d.compile, run: d.run };
  } finally { t.done(); }
}

/* ---------------- Wandbox ---------------- */
const WANDBOX_LANG = {
  "c": "C", "c++": "C++", "csharp": "C#", "go": "Go", "rust": "Rust",
  "ruby": "Ruby", "php": "PHP", "lua": "Lua", "perl": "Perl",
  "bash": "Bash script", "sqlite3": "SQL", "java": "Java", "scala": "Scala",
  "haskell": "Haskell", "swift": "Swift", "elixir": "Elixir",
  "python": "Python", "javascript": "JavaScript",
};
let wandboxCache = null, wandboxCacheTime = 0;
async function wandboxCompilers() {
  const now = Date.now();
  if (wandboxCache && now - wandboxCacheTime < 6 * 3600000) return wandboxCache;
  const t = withTimeout(8000);
  try {
    const res = await fetch(`${WANDBOX_URL}/list.json`, { signal: t.signal });
    if (!res.ok) throw new Error(`wandbox list ${res.status}`);
    wandboxCache = await res.json(); wandboxCacheTime = now; return wandboxCache;
  } finally { t.done(); }
}
async function pickWandboxCompiler(language) {
  const wl = WANDBOX_LANG[language];
  if (!wl) return null;
  const list = await wandboxCompilers();
  const matches = list.filter((c) => c.language === wl);
  if (!matches.length) return null;
  // Prefer the latest STABLE compiler (Wandbox lists newest first). "-head"
  // nightlies are bleeding-edge and frequently flaky, so use them only as a
  // last resort. This is both more reliable and faster (stable builds are cached).
  const stable = matches.find((c) => !/head/i.test(c.name));
  return (stable || matches[0]).name;
}
async function wandboxExecute({ language, source, stdin }) {
  const compiler = await pickWandboxCompiler(language);
  if (!compiler) throw new Error(`wandbox: unsupported language ${language}`);
  // Wandbox saves Java source as prog.java, so `public class Main` fails.
  let code = source;
  if (language === "java") code = code.replace(/\bpublic\s+(class|interface|enum)\s+/g, "$1 ");
  const t = withTimeout(40000);
  try {
    const r = await fetch(`${WANDBOX_URL}/compile.json`, {
      method: "POST", headers: { "Content-Type": "application/json" }, signal: t.signal,
      body: JSON.stringify({ compiler, code, stdin: stdin || "" }),
    });
    if (!r.ok) throw new Error(`wandbox compile ${r.status}`);
    const d = await r.json();
    const exitCode = typeof d.status === "string" ? parseInt(d.status, 10) || 0 : (d.status || 0);
    return {
      backend: "wandbox",
      compile: { stderr: d.compiler_error || "", stdout: d.compiler_message || "", code: 0 },
      run: { stdout: d.program_output || "", stderr: d.program_error || "", code: exitCode },
    };
  } finally { t.done(); }
}

/* ---------------- rate limiting (in-memory) ---------------- */
const hits = new Map(); // ip -> number[] (timestamps)
function rateLimited(ip) {
  const now = Date.now();
  const arr = (hits.get(ip) || []).filter((t) => now - t < RL_WINDOW_MS);
  arr.push(now);
  hits.set(ip, arr);
  return arr.length > RL_MAX;
}
// Periodically prune stale IPs so the map can't grow unbounded.
setInterval(() => {
  const now = Date.now();
  for (const [ip, arr] of hits) {
    const keep = arr.filter((t) => now - t < RL_WINDOW_MS);
    if (keep.length) hits.set(ip, keep); else hits.delete(ip);
  }
}, RL_WINDOW_MS).unref();

/* ---------------- input validation ---------------- */
const LANG_RE = /^[a-z0-9+#._-]{1,40}$/i;
function validateExec(body) {
  const { language, version, source, stdin = "" } = body || {};
  if (typeof language !== "string" || !LANG_RE.test(language)) return { error: "Invalid or missing language." };
  if (typeof source !== "string" || source.length === 0) return { error: "Source code is required." };
  if (Buffer.byteLength(source, "utf8") > MAX_SOURCE) return { error: `Source too large (max ${MAX_SOURCE} bytes).` };
  if (typeof stdin !== "string" || Buffer.byteLength(stdin, "utf8") > MAX_STDIN) return { error: `Stdin too large (max ${MAX_STDIN} bytes).` };
  if (version != null && (typeof version !== "string" || version.length > 30)) return { error: "Invalid version." };
  return { value: { language, version, source, stdin } };
}

/* ---------------- routes ---------------- */
app.get("/api/runtimes", async (req, res) => {
  try { res.json(await getRuntimes()); }
  catch (e) { res.status(502).json({ error: "Engine unavailable." }); }
});

app.post("/api/execute", async (req, res) => {
  const ip = req.ip || req.socket.remoteAddress || "unknown";
  if (rateLimited(ip)) return res.status(429).json({ error: "Too many runs — slow down and try again shortly." });

  const v = validateExec(req.body);
  if (v.error) return res.status(400).json({ error: v.error });
  const { language, version, source, stdin } = v.value;

  const errors = [];
  try { return res.json(await pistonExecute({ language, version, source, stdin })); }
  catch (e) { errors.push("piston: " + e.message); }
  if (ENABLE_WANDBOX) {
    try { return res.json(await wandboxExecute({ language, source, stdin })); }
    catch (e) { errors.push("wandbox: " + e.message); }
  }
  console.error(`[execute] no backend for "${language}":`, errors.join(" | "));
  res.status(502).json({
    error: `No execution backend available for "${language}". ` +
           `Start the bundled engine with "docker compose up", or check your network.`,
    ...(IS_PROD ? {} : { detail: errors }),
  });
});

app.get("/api/health", (req, res) => res.json({ ok: true, ts: Date.now() }));
app.get("*", (req, res) => res.sendFile(path.join(__dirname, "public", "index.html")));

// JSON body-parse / generic error handler (never leak stack traces to clients).
app.use((err, req, res, next) => {
  if (err && err.type === "entity.too.large") return res.status(413).json({ error: "Request too large." });
  console.error("[error]", err && err.message);
  res.status(500).json({ error: "Internal server error." });
});

app.listen(PORT, () => console.log(`⚡ Ironyx Code running at http://localhost:${PORT}`));
