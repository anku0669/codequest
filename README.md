<div align="center">

# 🎮 CodeQuest

### Learn to code by *playing*.

A free, gamified, browser-based coding platform — solve interactive challenges in **34 languages**, write code in a real **in-browser IDE**, earn **XP**, build **streaks**, climb **leagues**, and learn from a deep **per-language guide**.

[![Live Demo](https://img.shields.io/badge/▶_Live_Demo-006241?style=for-the-badge)](https://anku0669.github.io/codequest/)
&nbsp;
![Languages](https://img.shields.io/badge/Languages-34-00754A?style=for-the-badge)
![Challenges](https://img.shields.io/badge/Challenges-4800%2B-cba258?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-1E3932?style=for-the-badge)

**🔗 Live site: https://anku0669.github.io/codequest/**

</div>

---

## ✨ Features

- **34 language tracks** — Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Bash, Lua, Perl, Dart, Scala, Haskell, Elixir, R, Julia, Clojure, SQL + **HTML, CSS, SCSS, JSON, YAML, Markdown, XML, Dockerfile, GraphQL, Regex**.
- **4,800+ interactive challenges** organized into modules (Output → Variables → Operators → Strings → Conditionals → Loops → Functions → Collections → Projects).
- **🧩 DSA Challenges** — 57 LeetCode-style problems per core language (Two Sum, palindrome, Fibonacci, prime, GCD, sorting, search, FizzBuzz, and more).
- **📚 Per-language Learning Guide** — a huge **22-chapter, zero-to-advanced** guide for every language, each chapter with rich explanations and real code examples.
- **⌨️ Full in-browser IDE** — Monaco (the editor behind VS Code): themes, font size, word-wrap, minimap, format, copy, download, fullscreen, live status bar, **stdin**, **per-lesson auto-save**, and **⌘/Ctrl + Enter** to run.
- **👤 Accounts** — local Register / Login with per-profile progress (XP, streaks, badges) and a guest mode.
- **🏆 Leagues & badges** — Bronze → Diamond leagues with progress, your standing, and achievement badges.
- **Real code execution**
  - **Python** runs in the browser via **Pyodide** (WASM).
  - **JavaScript / TypeScript** run in a sandboxed **Web Worker**.
  - **Compiled languages** run via the free public **Wandbox** API (or a bundled **Piston** engine when self-hosted with Docker).
  - **Markup/structure tracks** are graded by checking your code contains the right constructs, with a **live preview** for HTML & CSS.
- **Top-notch UI** — a warm, clean, Starbucks-inspired design (cream canvas, four-tier green, gold accents, pill buttons, no gradients).

---

## 🚀 Live Demo

👉 **https://anku0669.github.io/codequest/**

> The live site is fully static. Python/JS/TS and all structure-graded tracks run entirely in your browser; compiled languages run via the public Wandbox API. For guaranteed local execution of **all** languages, run it with Docker (below).

---

## 🖥️ Run locally

### Option A — Node (recommended for full features)
```bash
npm install
npm start
# open http://localhost:3000
```

### Option B — Docker (bundled multi-language engine, all 34 languages execute)
```bash
docker compose up --build
# open http://localhost:3000
```

### Option C — Just the static site
```bash
cd public && python3 -m http.server 8000
# open http://localhost:8000
```

---

## 🧩 How it works

```
Browser (Monaco IDE + UI)
│
├─ Python  ─────────────▶ Pyodide (WASM, in-browser)
├─ JS / TS ─────────────▶ sandboxed Web Worker
├─ Markup/structure ────▶ graded by structure (HTML/CSS get a live preview)
└─ Compiled languages ──▶ /api/execute → Piston (Docker)  ·  or Wandbox (public API)
```

Progress, accounts, streaks and badges are stored in the browser (`localStorage`).

---

## 📁 Project structure

```
codequest/
├── public/                 # the web app (this is what GitHub Pages serves)
│   ├── index.html
│   ├── css/styles.css
│   ├── js/app.js           # SPA: routing, IDE, engines, auth, gamification
│   └── data/curriculum.js  # all languages, challenges & guides (generated)
├── server.js               # Express server + execution proxy (Piston → Wandbox)
├── generate_curriculum.py  # builds the curriculum
├── bigbank.py / dsa.py / morebank.py / webbank.py / guides.py
├── scripts/install-languages.js
├── Dockerfile · docker-compose.yml
└── README.md
```

Regenerate the curriculum with `python3 generate_curriculum.py`.

---

## 🤝 Contributing

Issues and PRs welcome! Add challenges in the generator files, then re-run `generate_curriculum.py`.

## 📝 License

[MIT](LICENSE) — free to use, learn from, and build on.

<div align="center">

Built with ❤️ for learners everywhere. **[Try it live →](https://anku0669.github.io/codequest/)**

</div>
