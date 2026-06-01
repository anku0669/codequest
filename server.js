/**
 * CodeQuest server — advanced multi-backend code execution.
 * Backend chain for /api/execute (first that succeeds wins):
 *   1) Piston   — self-hosted engine (docker compose). Supports all 24 langs.
 *   2) Wandbox  — free public API (no key). Covers most compiled languages.
 * (Python, JavaScript and TypeScript run in the browser — never reach this server.)
 * No API keys required. Node 18+ (built-in fetch).
 */
const express = require("express");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
const PISTON_URL = process.env.PISTON_URL || "http://localhost:2000/api/v2";
const WANDBOX_URL = process.env.WANDBOX_URL || "https://wandbox.org/api";
const ENABLE_WANDBOX = (process.env.ENABLE_WANDBOX || "true") !== "false";

app.use(express.json({ limit: "1mb" }));
app.use(express.static(path.join(__dirname, "public")));

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
  const head = matches.find((c) => /(^|-)head$/.test(c.name) || c.name.includes("-head"));
  return (head || matches[0]).name;
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

/* ---------------- routes ---------------- */
app.get("/api/runtimes", async (req, res) => {
  try { res.json(await getRuntimes()); }
  catch (e) { res.status(502).json({ error: e.message }); }
});

app.post("/api/execute", async (req, res) => {
  const { language, version, source, stdin = "" } = req.body || {};
  if (!language || typeof source !== "string")
    return res.status(400).json({ error: "language and source are required" });
  const errors = [];
  try { return res.json(await pistonExecute({ language, version, source, stdin })); }
  catch (e) { errors.push("piston: " + e.message); }
  if (ENABLE_WANDBOX) {
    try { return res.json(await wandboxExecute({ language, source, stdin })); }
    catch (e) { errors.push("wandbox: " + e.message); }
  }
  res.status(502).json({
    error: `No execution backend available for "${language}". ` +
           `Start the bundled engine with "docker compose up", or check your network.`,
    detail: errors,
  });
});

app.get("/api/health", (req, res) => res.json({ ok: true, ts: Date.now() }));
app.get("*", (req, res) => res.sendFile(path.join(__dirname, "public", "index.html")));
app.listen(PORT, () => console.log(`CodeQuest running at http://localhost:${PORT}`));
