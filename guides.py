# -*- coding: utf-8 -*-
"""Generates a HUGE 'zero to advanced' learning GUIDE for every track.
~18-22 chapters, each with rich multi-paragraph explanations plus several real
code examples pulled from that language's own lessons."""

# Each programming chapter: (example_match_keys_or_None, title, body_markdown)
PROG = [
 (None, "1. Introduction & Mindset",
  "Welcome to the complete **{name}** guide — a path from absolute beginner to confident developer.\n\n{blurb}\n\n## How to use this guide\nRead a chapter, then immediately try the example in the editor and tweak it. Programming is a *skill*, not a fact — you learn it by doing, breaking things, and fixing them. Aim for a little every day rather than a marathon once a month.\n\n## The learning loop\n- **Read** the concept and the example.\n- **Run** it, then change one thing and predict the result.\n- **Practice** with the challenges in each module.\n- **Build** something small that uses the idea.\n\n## A note on frustration\nEveryone gets stuck. Being stuck is not failure — it's the exact moment learning happens. Read the error message slowly, isolate the smallest broken piece, and search for the exact words of the error. You've got this."),
 (None, "2. Setting Up & Running Code",
  "Before writing serious programs you need a way to run **{name}**.\n\n## Right here\nThis platform runs your code in the browser or a bundled engine — just press **Run** (or ⌘/Ctrl+Enter). No setup needed to start learning.\n\n## On your own machine\nWhen you're ready to build real projects:\n- Install the official {name} toolchain (compiler/interpreter/runtime).\n- Use a good editor — **VS Code** is free and excellent, with {name} extensions for autocomplete and error highlighting.\n- Keep a terminal open to run your programs.\n\n## The edit → run → read loop\nWrite code, run it, read the output or error, adjust, repeat. The faster you can do this loop, the faster you learn. Most professional developers run their code dozens of times an hour."),
 (["Hello, World", "Print:", "-1", "say", "Select text"], "3. Output: Talking to the User",
  "Every program produces **output** — that's how it tells you what happened.\n\n## Printing\nYou call your language's print/output function and pass it a **string** (text in quotes). The program writes that text to the console, usually followed by a newline.\n\n## Why it matters\nPrinting is also your #1 debugging tool: when something behaves unexpectedly, print the values along the way to *see* what your program is actually doing.\n\n## Common mistakes\n- Forgetting the quotes around text.\n- Mismatched quotes (`\"` vs `'`) — pick one and close it.\n- Forgetting the parentheses or semicolon your language requires.\n\nTry the examples below, then change the message and run again."),
 (["comment", "Write a comment"], "4. Comments: Notes for Humans",
  "**Comments** are text the compiler ignores. They exist purely to explain your code to humans — including *future you*.\n\n## When to comment\n- Explain **why**, not **what**. Good code already shows *what* it does; comments explain the reasoning, trade-offs, or gotchas.\n- Leave a `TODO:` where work remains.\n- Avoid obvious comments like `// add 1 to x` — they just add noise.\n\n## Every language has its own marker\n`//`, `#`, `--`, or `;` depending on the language. Block comments span multiple lines.\n\nClean, well-commented code is a sign of a thoughtful engineer."),
 (["Store ", "var", "Variable", "Set "], "5. Variables: Storing Values",
  "A **variable** is a named box that stores a value so you can reuse it.\n\n## How it works\nYou *assign* a value to a name, then refer to that name later. Reading a variable doesn't change it; assigning again replaces the value.\n\n## Naming well\n- Use clear, descriptive names: `totalPrice`, not `tp`.\n- Be consistent with style (camelCase, snake_case) — follow your language's convention.\n- Names can't start with a number and usually can't contain spaces.\n\n## Mutability\nSome languages distinguish **constants** (never change) from **variables** (can change). Prefer constants when a value shouldn't change — it prevents bugs.\n\n## Common mistakes\n- Using a variable before assigning it.\n- Typos in names (the computer treats `score` and `scor` as different)."),
 (["Store ", "num", "Print number", "Select number"], "6. Data Types",
  "Values have **types** that decide what they are and what you can do with them.\n\n## The core types\n- **Integers** — whole numbers: `42`, `-7`.\n- **Floats / doubles** — decimals: `3.14`.\n- **Strings** — text: `\"hello\"`.\n- **Booleans** — `true` / `false`.\n- **Null / nil / None** — the absence of a value.\n- **Collections** — lists/arrays and key–value maps (covered later).\n\n## Static vs dynamic typing\nSome languages check types at compile time (catching mistakes early); others figure them out at runtime (more flexible, fewer guarantees). Neither is 'better' — they're different trade-offs.\n\n## Type errors\nMixing types incorrectly — like adding a number to text — is one of the most common beginner bugs. The error message usually tells you exactly which line."),
 (["math", "Do the Math", " + ", " * "], "7. Operators & Math",
  "**Operators** combine values into new ones.\n\n## Arithmetic\n`+` add, `-` subtract, `*` multiply, `/` divide, `%` remainder (modulo). Expressions follow normal math **precedence**: multiplication and division happen before addition and subtraction. Use parentheses to be explicit.\n\n## Integer vs float division\nIn many languages `7 / 2` gives `3` (integer division) while `7.0 / 2` gives `3.5`. Know which your language does.\n\n## The modulo trick\n`n % 2` is `0` for even numbers and `1` for odd — you'll use this constantly (e.g. FizzBuzz).\n\n## Assignment shortcuts\n`x += 1` means `x = x + 1`. Most languages have `+=`, `-=`, `*=`, `/=`."),
 (["Join ", "concat", "Length of", "Reverse"], "8. Strings In Depth",
  "**Strings** are sequences of characters, and text processing is everywhere.\n\n## Core operations\n- **Concatenation** — join strings end to end (`+`, `.`, `..`, `<>`, `||` depending on language).\n- **Length** — how many characters.\n- **Indexing & slicing** — grab a character or a substring.\n- **Search & replace** — find text and swap it.\n- **Case** — upper/lower transforms.\n\n## Escape sequences\n`\\n` is a newline, `\\t` a tab, `\\\\` a literal backslash, and `\\\"` a quote inside a string.\n\n## Immutability\nIn many languages strings are **immutable** — operations return a *new* string rather than changing the original. Capture the result in a variable."),
 (["compare", "Is ", "Compare"], "9. Booleans & Comparisons",
  "A **boolean** is a value that's either `true` or `false`, and it's the foundation of every decision a program makes.\n\n## Comparison operators\n`>` greater, `<` less, `>=`, `<=`, `==` equal, `!=` not equal. Each yields a boolean.\n\n## Combining conditions\n- **AND** — true only if both sides are true.\n- **OR** — true if either side is true.\n- **NOT** — flips true/false.\n\n## Watch out\n- `=` (assignment) vs `==` (comparison) is a classic bug.\n- Comparing floating-point numbers for exact equality is unreliable — compare with a small tolerance instead."),
 (["Odd or even", "Positive check", "if"], "10. Conditionals: Making Decisions",
  "**Conditionals** let your program choose between paths.\n\n## if / else\nRun one block when a test is true, another when it's false. Chain with `else if` (or `elif`) for multiple cases.\n\n## The modulo pattern\n`if n % 2 == 0` → even; otherwise odd. This single idea powers a huge number of beginner exercises.\n\n## switch / match\nMany languages offer a cleaner way to branch on many values of one variable.\n\n## Style tips\n- Keep conditions readable; extract complex tests into well-named variables.\n- Deeply nested `if`s are a smell — consider early returns or combining conditions."),
 (["Count to", "loop", "Sum 1.."], "11. Loops: Repetition (for)",
  "**Loops** repeat work so you don't copy-paste.\n\n## The for loop\nWalk a counter through a range, running the body each step. Perfect when you know how many times to repeat.\n\n## Accumulators\nA classic pattern: start a `total = 0`, then add to it each pass. That's how you sum a range or a list.\n\n## Iterating collections\nMost languages let you loop directly over the items of a list/array (`for item in items`).\n\n## Common mistakes\n- **Off-by-one errors** — double-check whether your range is inclusive or exclusive of the end.\n- Modifying a collection while looping over it can cause surprises."),
 (["While"], "12. Loops: Repetition (while)",
  "A **while loop** repeats *as long as* a condition stays true.\n\n## When to use it\nWhen you don't know in advance how many iterations you need — e.g. 'keep reading input until the user types quit'.\n\n## The shape\nInitialise a value, test the condition, do work, update the value so the loop can eventually end.\n\n## ⚠️ Infinite loops\nThe #1 while-loop bug: forgetting to update the variable in the condition, so it never becomes false. If your program hangs, this is the first thing to check.\n\n## break & continue\n`break` exits a loop early; `continue` skips to the next iteration. Use them to keep logic clean."),
 (["add(", "Add Function", "mul(", "func"], "13. Functions: Reusable Logic",
  "A **function** packages logic you can reuse.\n\n## Anatomy\n- **Name** — what it does (`calculateTotal`).\n- **Parameters** — the inputs it accepts.\n- **Body** — the work it performs.\n- **Return value** — the result it hands back.\n\n## Why functions matter\nThey let you write logic once and call it everywhere, give names to ideas, and make code testable. They're the single most important tool for managing complexity.\n\n## Best practices\n- One function = one job. If it does five things, split it.\n- Keep parameter lists short.\n- Return early to avoid deep nesting.\n- Pure functions (same input → same output, no side effects) are easiest to reason about."),
 (["Sum of", "Largest", "list"], "14. Collections: Lists & Arrays",
  "**Collections** hold many values together — the backbone of real programs.\n\n## Arrays / lists\nOrdered sequences accessed by **index** (usually starting at 0). You can add, remove, and read items by position.\n\n## Everyday operations\n- **Sum / max / min / average** of the elements.\n- **Search** for a value.\n- **Filter** to a subset, **map** to transform each item.\n- **Sort** into order.\n\n## Looping\nYou'll almost always pair collections with loops to process each element.\n\n## Common mistakes\n- **Index out of range** — accessing position 5 in a 3-item list.\n- Off-by-one when iterating to `length` vs `length - 1`."),
 (["Dictionary", "Sum of"], "15. Maps, Dictionaries & Key–Value Data",
  "Beyond ordered lists, you'll need **key–value** structures (called maps, dictionaries, hashes, or objects).\n\n## The idea\nInstead of accessing by numeric position, you look up a value by a **key** — like a real dictionary maps a word to its definition.\n\n## Why they're powerful\nLookups are fast and the code reads naturally: `user[\"email\"]` is clearer than `user[3]`.\n\n## Typical uses\n- Counting occurrences (word → count).\n- Grouping data.\n- Representing records/objects with named fields.\n\n## Tips\n- Keys are usually unique; assigning an existing key overwrites it.\n- Check whether a key exists before reading it to avoid errors."),
 (["Factorial", "FizzBuzz"], "16. Recursion",
  "**Recursion** is when a function calls itself to solve a smaller version of the same problem.\n\n## Two essential parts\n1. **Base case** — the simplest input, where the function returns directly (stops the recursion).\n2. **Recursive case** — the function calls itself on a smaller input and combines the result.\n\n## Classic examples\nFactorial (`n! = n × (n-1)!`), Fibonacci, and traversing trees/nested data.\n\n## ⚠️ Watch out\nForgetting or never reaching the base case causes infinite recursion and a **stack overflow**. Every recursion must shrink toward the base case.\n\n## Recursion vs loops\nAnything recursive can be written with a loop and vice-versa — choose whichever expresses the problem most clearly."),
 (None, "17. Errors & Debugging",
  "Bugs are a normal, daily part of programming. Great developers are great *debuggers*.\n\n## Two kinds of errors\n- **Syntax errors** — the code won't even run (a typo, missing bracket). The compiler points to the line and column.\n- **Runtime / logic errors** — it runs but crashes or gives the wrong answer.\n\n## A debugging method\n1. **Read the error message** — slowly, all of it. It usually names the file, line, and problem.\n2. **Reproduce** it reliably.\n3. **Isolate** — comment out code or add prints until you find the smallest broken piece.\n4. **Fix one thing**, then re-run.\n\n## try / catch\nMost languages let you *handle* errors gracefully (`try`/`catch`, `rescue`, `except`) instead of crashing — essential for real programs that touch files, networks, or user input."),
 (["FizzBuzz", "Two Sum", "Sort", "Reverse", "Factorial"], "18. Algorithms & Problem Solving",
  "An **algorithm** is a step-by-step recipe to solve a problem. Learning to think algorithmically is what separates someone who knows syntax from someone who can *build*.\n\n## A problem-solving framework\n1. **Understand** the problem — what are the inputs and expected outputs?\n2. **Examples** — work a small case by hand.\n3. **Plan** — write the steps in plain language first.\n4. **Code** it.\n5. **Test** edge cases (empty input, one item, negatives, duplicates).\n\n## Patterns you'll reuse\n- **Accumulator** (running total).\n- **Two pointers** (scan from both ends).\n- **Search** (linear, then binary).\n- **Sorting** and using sorted order.\n\n## Big-O (complexity)\nAs inputs grow, how does the work grow? `O(n)` scales linearly, `O(n²)` much worse. You'll care about this for large data and interviews. Practice the **DSA Challenges** module to build this muscle."),
 (None, "19. Clean Code & Best Practices",
  "Working code is the start; *good* code is the goal.\n\n## Principles\n- **Readability first** — code is read far more than it's written.\n- **DRY** (Don't Repeat Yourself) — extract repetition into functions.\n- **Small pieces** — short functions, single responsibilities.\n- **Meaningful names** — the best comment is a good name.\n- **Consistent style** — follow your language's conventions; use a formatter.\n\n## Quality habits\n- Write **tests** so you can change code without fear.\n- Use **version control (Git)** to track history and collaborate.\n- Review your own diffs before sharing.\n\nGood habits compound — they're what make a senior engineer fast *and* reliable."),
 (None, "20. Tools, Ecosystem & Going Pro",
  "Real development is more than syntax.\n\n## The toolbox\n- **Package manager** — install and share libraries so you don't reinvent the wheel.\n- **Formatter & linter** — keep code clean and catch mistakes automatically.\n- **Testing framework** — prove your code works and keep it working.\n- **Debugger** — step through code line by line and inspect values.\n- **Version control (Git)** + a host like GitHub — essential for any real project.\n\n## The standard library\nEvery language ships with a rich set of built-in functions — learn to reach for them before writing your own.\n\n## Community\nDocs, forums, and open-source code are your best teachers. Reading great code is one of the fastest ways to improve."),
 (None, "21. Your 30-Day Practice Plan",
  "Consistency beats intensity. Here's a simple plan:\n\n## Week 1 — Foundations\nOutput, variables, types, operators. Do every challenge in those modules. Build: a tip calculator.\n\n## Week 2 — Logic & Loops\nConditionals, for/while loops. Build: a number-guessing game and a multiplication table.\n\n## Week 3 — Functions & Collections\nWrite small functions; work with arrays and maps. Build: a to-do list in memory; compute stats over a list.\n\n## Week 4 — Problem Solving\nTackle the **DSA Challenges**. Re-solve a few from scratch without looking. Build: one small project end-to-end and share it.\n\n## Daily rhythm\n20–40 focused minutes. Keep your streak alive on this platform — the XP and badges are there to make the habit stick."),
 (None, "22. Glossary & Where to Go Next",
  "## Mini glossary\n- **Variable** — a named value.\n- **Function** — reusable block of logic with inputs and an output.\n- **Argument / parameter** — a value passed into a function.\n- **Loop** — repeated execution.\n- **Array / list** — ordered collection.\n- **Map / dictionary** — key–value collection.\n- **Boolean** — true/false.\n- **Compile** — translate code before running.\n- **Runtime** — while the program is executing.\n- **Bug** — a defect; **debugging** is finding and fixing it.\n\n## Where to go next\n1. Finish every module in this track — fluency comes from reps.\n2. Clear the **DSA Challenges**.\n3. Build a real project that excites you.\n4. Read other people's code and the official docs.\n5. Teach someone else — it's the ultimate test of understanding.\n\nKeep going. The difference between a beginner and a pro is mostly time and reps. 🚀"),
]

def _find_all(track, keys, limit=3):
    if not keys: return []
    seen, out = set(), []
    for l in track["lessons"]:
        t = l.get("title", "")
        if any(k in t or k in l.get("id", "") for k in keys):
            h = l.get("hint") or l.get("starter") or ""
            if h and h not in seen:
                seen.add(h); out.append(h)
                if len(out) >= limit: break
    return out

def build_guide(track):
    name = track["name"]
    if track.get("engine") in ("web", "static"):
        chapters = [{
            "title": "1. Introduction",
            "body": "Welcome to the complete **{n}** guide. {b}\n\n## How to use this guide\nRead each topic, study the examples, then practice with the challenges in that module. Come back here whenever you need a refresher.".format(n=name, b=track.get("blurb", "")),
            "examples": [],
        }]
        i = 2
        mats = track.get("materials", {})
        seen = []
        for l in track["lessons"]:
            m = l["module"]
            if m in seen: continue
            seen.append(m)
            mat = mats.get(m, {})
            body = mat.get("text", "Practice this topic with the challenges in this module. Study each example carefully and try changing it.")
            egs = _find_all(track, [], 0)
            # gather up to 4 example solutions from this module
            ex = []
            for ll in track["lessons"]:
                if ll["module"] == m and (ll.get("hint") or ""):
                    ex.append(ll["hint"])
                    if len(ex) >= 4: break
            chapters.append({"title": "%d. %s" % (i, m), "body": body, "examples": ex})
            i += 1
        return chapters
    out = []
    for keys, title, body in PROG:
        out.append({"title": title, "body": body.format(name=name, blurb=track.get("blurb", "")), "examples": _find_all(track, keys, 3) if keys else []})
    return out

if __name__ == "__main__":
    demo = {"name": "Python", "blurb": "Powerful.", "engine": "pyodide", "lessons": [
        {"id": "python-1", "title": "Print: Hello, World!", "hint": 'print("Hello, World!")'},
        {"id": "python-2", "title": "Store 42", "hint": "x = 42\nprint(x)"}]}
    g = build_guide(demo)
    print("chapters:", len(g), "| ch3 examples:", len(g[2]["examples"]))
