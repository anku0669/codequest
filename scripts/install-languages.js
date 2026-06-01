/**
 * Installs the language runtimes Ironyx Code needs into a self-hosted Piston instance.
 * Runs once on `docker compose up` (the `piston-init` service) and is safe to re-run.
 * Env: PISTON_URL (default http://piston:2000/api/v2)
 */
const PISTON = process.env.PISTON_URL || "http://piston:2000/api/v2";
const WANTED = [
  "python", "node", "typescript", "java", "gcc", "mono", "dotnet",
  "go", "rust", "ruby", "php", "swift", "kotlin", "bash", "lua",
  "perl", "dart", "scala", "haskell", "elixir", "r", "rscript",
  "julia", "clojure", "sqlite3",
];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function getJSON(url, opts) {
  const res = await fetch(url, opts);
  const txt = await res.text();
  let data; try { data = JSON.parse(txt); } catch { data = txt; }
  return { ok: res.ok, status: res.status, data };
}
async function waitForPiston() {
  process.stdout.write("⏳ Waiting for Piston");
  for (let i = 0; i < 60; i++) {
    try { const r = await getJSON(`${PISTON}/runtimes`); if (r.ok) { console.log(" ✓"); return; } } catch (_) {}
    process.stdout.write("."); await sleep(2000);
  }
  console.log("\n❌ Piston not ready in time."); process.exit(1);
}
function latestVersion(versions) {
  return versions.slice().sort((a, b) => a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" })).pop();
}
async function main() {
  await waitForPiston();
  const cat = await getJSON(`${PISTON}/packages`);
  if (!cat.ok || !Array.isArray(cat.data)) { console.log("❌ Could not read package catalog:", cat.status); process.exit(1); }
  const byLang = {};
  for (const p of cat.data) (byLang[p.language] = byLang[p.language] || []).push(p.language_version);
  const targets = WANTED.filter((w) => byLang[w]);
  console.log(`📦 Installing ${targets.length} language packages...\n`);
  const installed = [], failed = [];
  for (const lang of targets) {
    const version = latestVersion(byLang[lang]);
    process.stdout.write(`   → ${lang}@${version} ... `);
    try {
      const r = await getJSON(`${PISTON}/packages`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ language: lang, version }) });
      if (r.ok || (r.data && /already installed/i.test(JSON.stringify(r.data)))) { console.log("ok"); installed.push(`${lang}@${version}`); }
      else { console.log("FAILED", r.status); failed.push(lang); }
    } catch (e) { console.log("ERROR", e.message); failed.push(lang); }
    await sleep(500);
  }
  console.log(`\n✅ Installed: ${installed.length}`);
  if (failed.length) console.log(`⚠️  Not installed: ${failed.join(", ")}`);
  console.log("⚡ Ironyx Code runtimes are ready.");
}
main().catch((e) => { console.error(e); process.exit(1); });
