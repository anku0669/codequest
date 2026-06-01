# -*- coding: utf-8 -*-
"""Large structure-graded banks for languages we can't execute-verify in this env.
Lessons are graded by checking the learner's code CONTAINS the right constructs
(expectedAll tokens, case-insensitive) — the same safe model used for markup.
~130 lessons per language across modules."""

MORE = ["c", "swift", "kotlin", "bash", "perl", "scala", "haskell", "elixir", "julia", "clojure", "sql"]

PHRASES = ["Hello World", "Welcome", "I love coding", "Keep going", "Practice daily", "Stay curious",
 "Code wins", "Learn fast", "Build things", "Never quit", "Hello again", "Good morning", "Ship it",
 "Think clearly", "Debug calmly", "Read the docs", "Test first", "Small steps", "You can do it",
 "Onward", "Focus", "Iterate", "Refactor", "Commit often", "Less is more", "Be kind", "Stay sharp",
 "Dream big", "Start now", "Finish strong", "Hello coder", "Greetings", "Level up", "Game on",
 "Nice work", "Well done", "Keep learning", "Push forward", "Stay humble", "Explore", "Create",
 "Imagine", "Persist", "Achieve", "Inspire", "Begin", "Hello there", "Code daily", "Have fun", "Go far"]
NUMS = [0, 1, 2, 3, 5, 7, 8, 9, 10, 13, 21, 42, 64, 99, 100, 128, 256, 512, 1000, 2024]
VARS = [("x", 5), ("count", 10), ("age", 30), ("score", 99), ("year", 2024), ("n", 7), ("total", 100),
 ("size", 42), ("level", 3), ("speed", 60), ("price", 25), ("qty", 12), ("hp", 100), ("gold", 500),
 ("lives", 3), ("rank", 1), ("streak", 7), ("coins", 250), ("xp", 1000), ("temp", 72)]
MATHS = [(7, "+", 6), (13, "+", 8), (20, "-", 5), (9, "*", 9), (100, "-", 58), (8, "*", 7), (15, "+", 15),
 (6, "*", 6), (50, "-", 8), (3, "*", 14), (40, "+", 2), (12, "*", 12), (25, "+", 25), (60, "-", 18), (21, "+", 21)]
IFNS = [7, 10, 0, 42, 99, 5, 8, 100, 3, 21]
LOOPNS = [3, 4, 5, 6, 7, 8, 9, 10]
FUNCS = [(20, 22), (1, 1), (50, 50), (7, 8), (3, 4), (9, 9), (40, 2), (11, 89)]

# Per-language emitters. Each returns (solution, [tokens]). Tokens are lowercased substrings
# that MUST appear in a correct solution.
def low(*xs): return [str(x).lower() for x in xs]

E = {}
E["c"] = {
 "say": lambda s: ('#include <stdio.h>\nint main() {\n    printf("%s\\n");\n    return 0;\n}\n' % s, low("printf(", s)),
 "num": lambda n: ('#include <stdio.h>\nint main() {\n    printf("%%d\\n", %d);\n    return 0;\n}\n' % n, low("printf(", n)),
 "var": lambda nm, v: ('#include <stdio.h>\nint main() {\n    int %s = %d;\n    printf("%%d\\n", %s);\n    return 0;\n}\n' % (nm, v, nm), low("int " + nm, v, "printf(")),
 "math": lambda a, op, b: ('#include <stdio.h>\nint main() {\n    printf("%%d\\n", %d %s %d);\n    return 0;\n}\n' % (a, op, b), low("printf(", "%d %s %d" % (a, op, b))),
 "if": lambda n: ('#include <stdio.h>\nint main() {\n    int n = %d;\n    if (n > 0) printf("positive\\n"); else printf("not positive\\n");\n    return 0;\n}\n' % n, low("if (", "n > 0", "printf(")),
 "loop": lambda n: ('#include <stdio.h>\nint main() {\n    for (int i = 1; i <= %d; i++) printf("%%d\\n", i);\n    return 0;\n}\n' % n, low("for (", "i <= %d" % n, "printf(")),
 "func": lambda a, b: ('#include <stdio.h>\nint add(int a, int b) { return a + b; }\nint main() {\n    printf("%%d\\n", add(%d, %d));\n    return 0;\n}\n' % (a, b), low("int add(", "return a + b", "add(%d, %d)" % (a, b))),
 "comment": lambda: ("// this is a comment\nint main() { return 0; }\n", low("//")),
}
E["swift"] = {
 "say": lambda s: ('print("%s")' % s, low("print(", s)),
 "num": lambda n: ('print(%d)' % n, low("print(", n)),
 "var": lambda nm, v: ('let %s = %d\nprint(%s)' % (nm, v, nm), low("let " + nm, v, "print(")),
 "math": lambda a, op, b: ('print(%d %s %d)' % (a, op, b), low("print(", "%d %s %d" % (a, op, b))),
 "if": lambda n: ('let n = %d\nif n > 0 { print("positive") } else { print("not positive") }' % n, low("if n > 0", "print(")),
 "loop": lambda n: ('for i in 1...%d {\n    print(i)\n}' % n, low("for i in 1...%d" % n, "print(i)")),
 "func": lambda a, b: ('func add(_ a: Int, _ b: Int) -> Int { return a + b }\nprint(add(%d, %d))' % (a, b), low("func add(", "return a + b", "add(%d, %d)" % (a, b))),
 "comment": lambda: ("// this is a comment\nprint(\"hi\")", low("//")),
}
E["kotlin"] = {
 "say": lambda s: ('fun main() {\n    println("%s")\n}' % s, low("println(", s)),
 "num": lambda n: ('fun main() {\n    println(%d)\n}' % n, low("println(", n)),
 "var": lambda nm, v: ('fun main() {\n    val %s = %d\n    println(%s)\n}' % (nm, v, nm), low("val " + nm, v, "println(")),
 "math": lambda a, op, b: ('fun main() {\n    println(%d %s %d)\n}' % (a, op, b), low("println(", "%d %s %d" % (a, op, b))),
 "if": lambda n: ('fun main() {\n    val n = %d\n    if (n > 0) println("positive") else println("not positive")\n}' % n, low("if (n > 0)", "println(")),
 "loop": lambda n: ('fun main() {\n    for (i in 1..%d) println(i)\n}' % n, low("for (i in 1..%d)" % n, "println(i)")),
 "func": lambda a, b: ('fun add(a: Int, b: Int) = a + b\nfun main() {\n    println(add(%d, %d))\n}' % (a, b), low("fun add(", "a + b", "add(%d, %d)" % (a, b))),
 "comment": lambda: ("// this is a comment\nfun main() {}", low("//")),
}
E["scala"] = {
 "say": lambda s: ('@main def run() = println("%s")' % s, low("println(", s)),
 "num": lambda n: ('@main def run() = println(%d)' % n, low("println(", n)),
 "var": lambda nm, v: ('@main def run() = {\n  val %s = %d\n  println(%s)\n}' % (nm, v, nm), low("val " + nm, v, "println(")),
 "math": lambda a, op, b: ('@main def run() = println(%d %s %d)' % (a, op, b), low("println(", "%d %s %d" % (a, op, b))),
 "if": lambda n: ('@main def run() = {\n  val n = %d\n  if (n > 0) println("positive") else println("not positive")\n}' % n, low("if (n > 0)", "println(")),
 "loop": lambda n: ('@main def run() = for (i <- 1 to %d) println(i)' % n, low("for (i <- 1 to %d)" % n, "println(i)")),
 "func": lambda a, b: ('def add(a: Int, b: Int) = a + b\n@main def run() = println(add(%d, %d))' % (a, b), low("def add(", "a + b", "add(%d, %d)" % (a, b))),
 "comment": lambda: ("// this is a comment\n@main def run() = ()", low("//")),
}
E["haskell"] = {
 "say": lambda s: ('main :: IO ()\nmain = putStrLn "%s"' % s, low("putstrln", s)),
 "num": lambda n: ('main = print (%d :: Int)' % n, low("print", n)),
 "var": lambda nm, v: ('main = do\n  let %s = %d\n  print %s' % (nm, v, nm), low("let " + nm, v, "print")),
 "math": lambda a, op, b: ('main = print (%d %s %d)' % (a, op, b), low("print", "%d %s %d" % (a, op, b))),
 "if": lambda n: ('main = putStrLn (if (%d :: Int) > 0 then "positive" else "not positive")' % n, low("if", "> 0", "putstrln")),
 "loop": lambda n: ('main = mapM_ print [1..%d]' % n, low("mapm_", "[1..%d]" % n)),
 "func": lambda a, b: ('add :: Int -> Int -> Int\nadd a b = a + b\nmain = print (add %d %d)' % (a, b), low("add a b = a + b", "add %d %d" % (a, b))),
 "comment": lambda: ("-- this is a comment\nmain = return ()", low("--")),
}
E["elixir"] = {
 "say": lambda s: ('IO.puts "%s"' % s, low("io.puts", s)),
 "num": lambda n: ('IO.puts %d' % n, low("io.puts", n)),
 "var": lambda nm, v: ('%s = %d\nIO.puts %s' % (nm, v, nm), low(nm + " = " + str(v), "io.puts")),
 "math": lambda a, op, b: ('IO.puts(%d %s %d)' % (a, op, b), low("io.puts", "%d %s %d" % (a, op, b))),
 "if": lambda n: ('n = %d\nIO.puts(if n > 0, do: "positive", else: "not positive")' % n, low("if n > 0", "io.puts")),
 "loop": lambda n: ('for i <- 1..%d, do: IO.puts(i)' % n, low("for i <- 1..%d" % n, "io.puts")),
 "func": lambda a, b: ('add = fn a, b -> a + b end\nIO.puts add.(%d, %d)' % (a, b), low("fn a, b -> a + b", "add.(%d, %d)" % (a, b))),
 "comment": lambda: ("# this is a comment\nIO.puts \"hi\"", low("#")),
}
E["julia"] = {
 "say": lambda s: ('println("%s")' % s, low("println(", s)),
 "num": lambda n: ('println(%d)' % n, low("println(", n)),
 "var": lambda nm, v: ('%s = %d\nprintln(%s)' % (nm, v, nm), low(nm + " = " + str(v), "println(")),
 "math": lambda a, op, b: ('println(%d %s %d)' % (a, op, b), low("println(", "%d %s %d" % (a, op, b))),
 "if": lambda n: ('n = %d\nprintln(n > 0 ? "positive" : "not positive")' % n, low("n > 0", "println(")),
 "loop": lambda n: ('for i in 1:%d\n    println(i)\nend' % n, low("for i in 1:%d" % n, "println(i)")),
 "func": lambda a, b: ('add(a, b) = a + b\nprintln(add(%d, %d))' % (a, b), low("add(a, b) = a + b", "add(%d, %d)" % (a, b))),
 "comment": lambda: ("# this is a comment\nprintln(\"hi\")", low("#")),
}
E["clojure"] = {
 "say": lambda s: ('(println "%s")' % s, low("(println", s)),
 "num": lambda n: ('(println %d)' % n, low("(println", n)),
 "var": lambda nm, v: ('(def %s %d)\n(println %s)' % (nm, v, nm), low("(def " + nm, v, "(println")),
 "math": lambda a, op, b: ('(println (%s %d %d))' % (op, a, b), low("(println", "(%s %d %d)" % (op, a, b))),
 "if": lambda n: ('(def n %d)\n(println (if (> n 0) "positive" "not positive"))' % n, low("(if (> n 0)", "(println")),
 "loop": lambda n: ('(doseq [i (range 1 %d)] (println i))' % (n + 1), low("doseq", "(range 1 %d)" % (n + 1), "(println i)")),
 "func": lambda a, b: ('(defn add [a b] (+ a b))\n(println (add %d %d))' % (a, b), low("(defn add", "(+ a b)", "(add %d %d)" % (a, b))),
 "comment": lambda: ("; this is a comment\n(println \"hi\")", low(";")),
}
E["bash"] = {
 "say": lambda s: ('echo "%s"' % s, low("echo", s)),
 "num": lambda n: ('echo %d' % n, low("echo", n)),
 "var": lambda nm, v: ('%s=%d\necho $%s' % (nm, v, nm), low(nm + "=" + str(v), "echo $" + nm)),
 "math": lambda a, op, b: ('echo $(( %d %s %d ))' % (a, op, b), low("echo $((", "%d %s %d" % (a, op, b))),
 "if": lambda n: ('n=%d\nif [ $n -gt 0 ]; then echo positive; else echo "not positive"; fi' % n, low("if [", "-gt 0", "echo")),
 "loop": lambda n: ('for i in $(seq 1 %d); do echo $i; done' % n, low("for i in", "seq 1 %d" % n, "echo $i")),
 "func": lambda a, b: ('add() { echo $(( $1 + $2 )); }\nadd %d %d' % (a, b), low("add()", "$1 + $2", "add %d %d" % (a, b))),
 "comment": lambda: ("# this is a comment\necho hi", low("#")),
}
E["perl"] = {
 "say": lambda s: ('print "%s\\n";' % s, low("print", s)),
 "num": lambda n: ('print %d, "\\n";' % n, low("print", n)),
 "var": lambda nm, v: ('my $%s = %d;\nprint "$%s\\n";' % (nm, v, nm), low("my $" + nm + " = " + str(v), "print")),
 "math": lambda a, op, b: ('print %d %s %d, "\\n";' % (a, op, b), low("print", "%d %s %d" % (a, op, b))),
 "if": lambda n: ('my $n = %d;\nif ($n > 0) { print "positive\\n"; } else { print "not positive\\n"; }' % n, low("if ($n > 0)", "print")),
 "loop": lambda n: ('for my $i (1..%d) { print "$i\\n"; }' % n, low("for my $i (1..%d)" % n, "print")),
 "func": lambda a, b: ('sub add { return $_[0] + $_[1]; }\nprint add(%d, %d), "\\n";' % (a, b), low("sub add", "$_[0] + $_[1]", "add(%d, %d)" % (a, b))),
 "comment": lambda: ("# this is a comment\nprint \"hi\\n\";", low("#")),
}

EXPL = {
 "say": "Use your language's output statement to print a line of text (a **string** in quotes).",
 "num": "Print a **number** directly — no quotes needed for numeric literals.",
 "var": "Declare a **variable**, give it a value, then print the variable. Reusing the name reuses the value.",
 "math": "Use **arithmetic operators** (`+ - * /`). The expression is evaluated before it's printed.",
 "if": "Use an **if / else** statement with a comparison (`> 0`) to choose what to output.",
 "loop": "Use a **loop** to repeat output for a range of values.",
 "func": "Define a **function** that returns a value, then call it. Define once, reuse anywhere.",
 "comment": "Write a **comment** — notes ignored by the compiler that explain your code.",
}

def _mk(lid, n, module, title, diff, xp, brief, expl, sol, tokens):
    return {"id": lid + "-" + str(n), "module": module, "title": title, "xp": xp, "difficulty": diff,
            "brief": brief, "explanation": expl, "hint": sol, "starter": "", "expectedAll": tokens}

def build_more(lid):
    e = E[lid]; out = []; n = 0
    def add(mod, title, diff, xp, key, *args):
        nonlocal n; n += 1
        sol, toks = e[key](*args)
        if key == "say": brief = "Print the text `%s`." % args[0]
        elif key == "num": brief = "Print the number `%s`." % args[0]
        elif key == "var": brief = "Create a variable `%s` set to `%s` and print it." % (args[0], args[1])
        elif key == "math": brief = "Compute and print `%d %s %d`." % args
        elif key == "if": brief = "Given `n = %s`, print `positive` if it's greater than 0, else `not positive`." % args[0]
        elif key == "loop": brief = "Use a loop to print the numbers 1 through %s, one per line." % args[0]
        elif key == "func": brief = "Write an `add` function and print `add(%s, %s)`." % (args[0], args[1])
        else: brief = "Write a single-line comment in this language."
        out.append(_mk(lid, n, mod, title, diff, xp, brief, EXPL[key], sol, toks))
    for s in PHRASES: add("Output & Printing", "Print: " + s, "Easy", 10, "say", s)
    for v in NUMS: add("Output & Printing", "Print number " + str(v), "Easy", 10, "num", v)
    for nm, v in VARS: add("Variables", "Variable: " + nm, "Easy", 12, "var", nm, v)
    for a, op, b in MATHS: add("Operators & Math", "%d %s %d" % (a, op, b), "Easy", 12, "math", a, op, b)
    for v in IFNS: add("Conditionals", "Positive check: " + str(v), "Medium", 16, "if", v)
    for v in LOOPNS: add("Loops", "Count to " + str(v), "Medium", 18, "loop", v)
    for a, b in FUNCS: add("Functions", "add(%d, %d)" % (a, b), "Medium", 22, "func", a, b)
    for i in range(4): add("Comments & Syntax", "Write a comment #" + str(i + 1), "Easy", 8, "comment")
    return out

# ---------------- SQL (its own task set) ----------------
def build_sql():
    out = []; n = 0
    def add(mod, title, diff, xp, brief, expl, sol, toks):
        nonlocal n; n += 1
        out.append(_mk("sql", n, mod, title, diff, xp, brief, expl, sol, toks))
    for s in PHRASES:
        add("SELECT Basics", "Select text: " + s, "Easy", 10, "Select the literal text `%s`." % s, "`SELECT` returns a value or row set.", "SELECT '%s';" % s, low("select", s))
    for v in NUMS:
        add("SELECT Basics", "Select number " + str(v), "Easy", 10, "Select the number `%d`." % v, "You can select literal numbers.", "SELECT %d;" % v, low("select", v))
    for a, op, b in MATHS:
        add("Math in SQL", "%d %s %d" % (a, op, b), "Easy", 12, "Select the result of `%d %s %d`." % (a, op, b), "SQL evaluates arithmetic in SELECT.", "SELECT %d %s %d;" % (a, op, b), low("select", "%d %s %d" % (a, op, b)))
    for nm, v in VARS:
        add("Aliases", "Alias " + nm, "Easy", 12, "Select `%d` with the column alias `%s`." % (v, nm), "`AS` names a result column.", "SELECT %d AS %s;" % (v, nm), low("select", v, "as " + nm))
    qs = [("users", "name"), ("products", "price"), ("orders", "id"), ("books", "title"), ("cities", "population"),
          ("songs", "title"), ("teams", "wins"), ("movies", "year"), ("students", "grade"), ("cars", "model")]
    for tbl, col in qs:
        add("Querying Tables", "Select %s from %s" % (col, tbl), "Medium", 16, "Select the `%s` column from the `%s` table." % (col, tbl), "`SELECT col FROM table` reads a column.", "SELECT %s FROM %s;" % (col, tbl), low("select", col, "from " + tbl))
        add("Filtering (WHERE)", "Filter %s" % tbl, "Medium", 18, "Select all from `%s` where `%s` is greater than 10." % (tbl, col), "`WHERE` filters rows.", "SELECT * FROM %s WHERE %s > 10;" % (tbl, col), low("select", "from " + tbl, "where", col, "> 10"))
        add("Sorting (ORDER BY)", "Order %s" % tbl, "Medium", 18, "Select all from `%s` ordered by `%s`." % (tbl, col), "`ORDER BY` sorts the result.", "SELECT * FROM %s ORDER BY %s;" % (tbl, col), low("select", "from " + tbl, "order by", col))
        add("Aggregates", "Count %s" % tbl, "Medium", 18, "Count the rows in `%s`." % tbl, "`COUNT(*)` counts rows.", "SELECT COUNT(*) FROM %s;" % tbl, low("select", "count(", "from " + tbl))
        add("Aggregates", "Max %s" % col, "Medium", 18, "Find the maximum `%s` in `%s`." % (col, tbl), "`MAX()` returns the largest value.", "SELECT MAX(%s) FROM %s;" % (col, tbl), low("select", "max(", col, "from " + tbl))
    add("Joins & More", "Limit rows", "Medium", 16, "Select the first 5 rows from `users`.", "`LIMIT` caps the number of rows.", "SELECT * FROM users LIMIT 5;", low("select", "from users", "limit", "5"))
    add("Joins & More", "Distinct", "Medium", 16, "Select distinct `city` from `users`.", "`DISTINCT` removes duplicates.", "SELECT DISTINCT city FROM users;", low("select", "distinct", "city", "from users"))
    add("Joins & More", "Group by", "Hard", 24, "Count users grouped by `city`.", "`GROUP BY` buckets rows for aggregation.", "SELECT city, COUNT(*) FROM users GROUP BY city;", low("select", "count(", "group by", "city"))
    return out

ENGINE = {l: "server" for l in MORE}
ENGINE["sql"] = "static"  # graded structurally (no runtime needed)
# all MORE langs are graded structurally; keep server engine so users can still run via Docker/Wandbox
for l in MORE:
    ENGINE[l] = "static"

def build(lid):
    return build_sql() if lid == "sql" else build_more(lid)

# ===================== Dart + markup expansion =====================
E["dart"] = {
 "say": lambda s: ('void main() {\n  print("%s");\n}' % s, low("print(", s)),
 "num": lambda n: ('void main() {\n  print(%d);\n}' % n, low("print(", n)),
 "var": lambda nm, v: ('void main() {\n  var %s = %d;\n  print(%s);\n}' % (nm, v, nm), low("var " + nm, v, "print(")),
 "math": lambda a, op, b: ('void main() {\n  print(%d %s %d);\n}' % (a, op, b), low("print(", "%d %s %d" % (a, op, b))),
 "if": lambda n: ('void main() {\n  var n = %d;\n  print(n > 0 ? "positive" : "not positive");\n}' % n, low("n > 0", "print(")),
 "loop": lambda n: ('void main() {\n  for (var i = 1; i <= %d; i++) print(i);\n}' % n, low("for (var i = 1; i <= %d" % n, "print(i)")),
 "func": lambda a, b: ('int add(int a, int b) => a + b;\nvoid main() {\n  print(add(%d, %d));\n}' % (a, b), low("int add(", "a + b", "add(%d, %d)" % (a, b))),
 "comment": lambda: ("// this is a comment\nvoid main() {}", low("//")),
}

KVS = [("name", "Sam", 0), ("title", "Hello", 0), ("city", "Paris", 0), ("status", "active", 0),
 ("role", "admin", 0), ("color", "blue", 0), ("brand", "Acme", 0), ("lang", "English", 0),
 ("country", "France", 0), ("team", "Red", 0), ("env", "prod", 0), ("region", "west", 0),
 ("age", 30, 1), ("year", 2024, 1), ("count", 10, 1), ("price", 99, 1), ("score", 88, 1),
 ("port", 8080, 1), ("qty", 5, 1), ("level", 3, 1), ("size", 42, 1), ("max", 100, 1), ("min", 1, 1), ("timeout", 30, 1)]
URLS = ["https://example.com", "https://gumloop.com", "/about", "/docs", "https://github.com", "/contact"]

def _mkmarkup(lid):
    out = []; n = 0
    def add(mod, title, brief, expl, sol, toks):
        nonlocal n; n += 1
        out.append(_mk(lid, n, mod, title, "Easy", 12, brief, expl, sol, toks))
    if lid == "json":
        for k, v, num in KVS:
            val = str(v) if num else '"%s"' % v
            add("Key/Value", "Object: " + k, "Create a JSON object with key `%s` set to `%s`." % (k, v), "JSON objects use `{ \"key\": value }`; strings need double quotes.", '{ "%s": %s }' % (k, val), low('"%s"' % k, val))
        for k, v, num in KVS[:12]:
            val = str(v) if num else '"%s"' % v
            add("Arrays", "Array for " + k, "Create an object where `%s` is an array containing `%s`." % (k, v), "Arrays use square brackets `[ ]`.", '{ "%s": [%s] }' % (k, val), low('"%s"' % k, "[" + val))
        for k, v, num in KVS[:10]:
            add("Nested", "Nested " + k, "Create a nested object: `data` containing `%s`." % k, "Objects can nest inside objects.", '{ "data": { "%s": %s } }' % (k, str(v) if num else '"%s"' % v), low('"data"', '"%s"' % k))
        add("Types", "Boolean", "Create an object with `active` = `true`.", "Booleans are `true`/`false`.", '{ "active": true }', low('"active"', "true"))
        add("Types", "Null", "Create an object with `data` = `null`.", "`null` means no value.", '{ "data": null }', low('"data"', "null"))
    elif lid == "yaml":
        for k, v, num in KVS:
            add("Key/Value", "Set " + k, "Set `%s` to `%s`." % (k, v), "YAML uses `key: value`.", "%s: %s" % (k, v), low(k + ":", v))
        for k, v, num in KVS[:12]:
            add("Lists", "List for " + k, "Make `%s` a list containing `%s`." % (k, v), "List items start with `- `.", "%s:\n  - %s" % (k, v), low(k + ":", "- " + str(v)))
        for k, v, num in KVS[:10]:
            add("Nested", "Nested " + k, "Nest `%s` under `config`." % k, "Indentation creates nesting.", "config:\n  %s: %s" % (k, v), low("config:", k + ":"))
    elif lid == "xml":
        for k, v, num in KVS:
            add("Elements", "Element " + k, "Create an element `<%s>` with text `%s`." % (k, v), "XML wraps data in custom tags.", "<%s>%s</%s>" % (k, v, k), low("<%s>" % k, str(v), "</%s>" % k))
        for k, v, num in KVS[:12]:
            add("Attributes", "Attribute " + k, "Create `<item %s=\"%s\">`." % (k, v), "Attributes add metadata.", '<item %s="%s"></item>' % (k, v), low("<item", k + "=", str(v)))
        for k, v, num in KVS[:10]:
            add("Nesting", "Nested " + k, "Nest `<%s>` inside `<root>`." % k, "Elements nest like a tree.", "<root>\n  <%s>%s</%s>\n</root>" % (k, v, k), low("<root>", "<%s>" % k))
    elif lid == "scss":
        for k, v, num in KVS:
            val = str(v) if num else v
            add("Variables", "Variable $" + k, "Declare a SCSS variable `$%s` = `%s`." % (k, v), "SCSS variables start with `$`.", "$%s: %s;" % (k, val), low("$%s:" % k, val))
        props = [("color", "red"), ("background", "blue"), ("font-size", "16px"), ("margin", "8px"), ("padding", "12px"), ("border", "1px solid"), ("width", "100px"), ("height", "50px"), ("display", "flex"), ("opacity", "0.5")]
        for p, v in props:
            add("Properties", "Set " + p, "In a `.box` rule, set `%s` to `%s`." % (p, v), "SCSS uses the same properties as CSS.", ".box {\n  %s: %s;\n}" % (p, v), low(".box", p + ":", v))
        add("Nesting", "Nest a rule", "Nest `a` inside `nav` and set its color to red.", "SCSS lets you nest selectors.", "nav {\n  a { color: red; }\n}", low("nav", "a", "color:"))
        add("Nesting", "Parent &", "Style `&:hover` inside `.btn`.", "`&` is the parent selector.", ".btn {\n  &:hover { color: green; }\n}", low("&:hover", "color:"))
        add("Mixins", "Define mixin", "Define a mixin `@mixin center`.", "Mixins are reusable rule groups.", "@mixin center {\n  display: flex;\n}", low("@mixin", "center"))
        add("Mixins", "Use mixin", "Include `@include center` in `.box`.", "`@include` applies a mixin.", ".box { @include center; }", low("@include", "center"))
    elif lid == "markdown":
        for i, s in enumerate(PHRASES[:30]):
            lvl = (i % 3) + 1
            add("Headings", "H%d: %s" % (lvl, s), "Write an H%d heading that says `%s`." % (lvl, s), "`#`×level makes a heading.", ("#" * lvl) + " " + s, low(("#" * lvl) + " " + s.lower()))
        for s in ["bold", "important", "note", "warning", "tip", "key", "core", "main"]:
            add("Emphasis", "Bold " + s, "Make the word `%s` bold." % s, "Wrap text in `**` for bold.", "**%s**" % s, low("**%s**" % s))
        for s in ["italic", "subtle", "aside", "hint", "soft"]:
            add("Emphasis", "Italic " + s, "Make the word `%s` italic." % s, "Wrap text in `*` for italic.", "*%s*" % s, low("*%s*" % s))
        for u in URLS:
            add("Links", "Link to " + u, "Create a link with text `Click` to `%s`." % u, "`[text](url)` makes a link.", "[Click](%s)" % u, low("[click]", "(%s)" % u))
        add("Lists", "Bullet list", "Make a bullet list of `A`, `B`, `C`.", "`- ` starts bullets.", "- A\n- B\n- C", low("- a", "- b", "- c"))
        add("Lists", "Numbered list", "Make a numbered list `One`, `Two`.", "`1. ` starts numbers.", "1. One\n2. Two", low("1. one", "2. two"))
        add("Iron", "Inline code", "Show `print()` as inline code.", "Backticks make inline code.", "`print()`", low("`print()`"))
        add("Iron", "Code block", "Write a fenced code block.", "Triple backticks fence code.", "```\ncode\n```", low("```"))
    elif lid == "dockerfile":
        imgs = ["node:20", "python:3.12", "alpine:3.19", "ubuntu:22.04", "golang:1.22", "nginx:latest", "redis:7", "openjdk:21"]
        for im in imgs:
            add("Base Image", "FROM " + im, "Start from the `%s` base image." % im, "`FROM` sets the base image.", "FROM %s" % im, low("from ", im))
        cmds = ["npm install", "pip install -r requirements.txt", "apt-get update", "go build", "make", "yarn", "npm run build", "go mod download"]
        for c in cmds:
            add("Build Steps", "RUN " + c.split()[0], "Run `%s` during the build." % c, "`RUN` executes a build command.", "RUN %s" % c, low("run ", c.split()[0]))
        for k, v, num in KVS[:10]:
            add("Environment", "ENV " + k, "Set env var `%s` to `%s`." % (k.upper(), v), "`ENV` sets environment variables.", "ENV %s=%s" % (k.upper(), v), low("env ", k.lower() + "=", str(v).lower()))
        for p in [3000, 8080, 80, 443, 5000, 5432, 6379, 27017]:
            add("Networking", "EXPOSE " + str(p), "Expose port `%d`." % p, "`EXPOSE` documents the port.", "EXPOSE %d" % p, low("expose ", p))
        add("Workdir & Copy", "WORKDIR", "Set the working directory to `/app`.", "`WORKDIR` sets the current dir.", "WORKDIR /app", low("workdir ", "/app"))
        add("Workdir & Copy", "COPY", "Copy `package.json` into the image.", "`COPY src dest` adds files.", "COPY package.json .", low("copy ", "package.json"))
        add("Startup", "CMD", "Run `node server.js` on start.", "`CMD` is the default command.", 'CMD ["node", "server.js"]', low("cmd ", "node", "server.js"))
        add("Startup", "ENTRYPOINT", "Set the entrypoint to `python`.", "`ENTRYPOINT` is the fixed executable.", 'ENTRYPOINT ["python"]', low("entrypoint", "python"))
    elif lid == "graphql":
        fields = ["user", "product", "order", "post", "comment", "book", "movie", "team", "city", "song"]
        for f in fields:
            add("Queries", "Query " + f, "Write a query for a `%s` field." % f, "Queries request fields.", "query {\n  %s\n}" % f, low("query", f))
            add("Nested Fields", "Fields of " + f, "Query `%s` with `id` and `name`." % f, "Select nested fields in braces.", "query {\n  %s {\n    id\n    name\n  }\n}" % f, low("query", f, "id", "name"))
            add("Arguments", "Arg on " + f, "Query `%s(id: 1)` with `name`." % f, "Arguments filter data.", "query {\n  %s(id: 1) {\n    name\n  }\n}" % f, low("%s(id: 1)" % f, "name"))
        for f in fields[:6]:
            add("Schema", "Type " + f.capitalize(), "Define `type %s` with `name: String`." % f.capitalize(), "Types describe data shape.", "type %s {\n  name: String\n}" % f.capitalize(), low("type %s" % f.lower(), "name:", "string"))
        add("Mutations", "addUser", "Define a `Mutation` with `addUser: User`.", "Mutations change data.", "type Mutation {\n  addUser: User\n}", low("mutation", "adduser"))
    elif lid == "regex":
        items = [("Digit", "Match a single digit.", "\\d", ["\\d"]), ("Word char", "Match a word character.", "\\w", ["\\w"]),
         ("Whitespace", "Match whitespace.", "\\s", ["\\s"]), ("Any char", "Match any character.", ".", ["."]),
         ("One or more digits", "Match one or more digits.", "\\d+", ["\\d+"]), ("Zero or more words", "Match zero or more word chars.", "\\w*", ["\\w*"]),
         ("Optional", "Make the previous char optional.", "a?", ["a?"]), ("Start anchor", "Anchor to start of line.", "^abc", ["^"]),
         ("End anchor", "Anchor to end of line.", "abc$", ["$"]), ("Exactly 3", "Match exactly 3 digits.", "\\d{3}", ["\\d{3}"]),
         ("Range 2-4", "Match 2 to 4 letters.", "[a-z]{2,4}", ["{2,4}"]), ("Char set vowels", "Match any vowel.", "[aeiou]", ["[aeiou]"]),
         ("Lowercase range", "Match a lowercase letter.", "[a-z]", ["[a-z]"]), ("Uppercase range", "Match an uppercase letter.", "[A-Z]", ["[a-z]"]),
         ("Digit range", "Match a digit 0-9.", "[0-9]", ["[0-9]"]), ("Negated set", "Match any non-digit.", "[^0-9]", ["[^0-9]"]),
         ("Alternation", "Match cat or dog.", "cat|dog", ["cat", "dog", "|"]), ("Group", "Group `ab` and repeat.", "(ab)+", ["(ab)"]),
         ("Word boundary", "Match a word boundary.", "\\bword\\b", ["\\b"]), ("Email-ish", "Match word@word.", "\\w+@\\w+", ["@"]),
         ("Phone-ish", "Match 3 digits dash 4 digits.", "\\d{3}-\\d{4}", ["\\d{3}", "\\d{4}"]), ("Hex", "Match a hex color.", "#[0-9a-f]{6}", ["#", "{6}"]),
         ("Escaped dot", "Match a literal dot.", "\\.", ["\\."]), ("Tab", "Match a tab character.", "\\t", ["\\t"])]
        for title, brief, sol, toks in items:
            add("Patterns", title, brief + " (write the regex)", "Regex matches text patterns with metacharacters.", sol, [t.lower() for t in toks])
    return out

MARKUP = ["scss", "json", "yaml", "markdown", "xml", "dockerfile", "graphql", "regex"]
MORE = MORE + ["dart"]
ALL = MORE + MARKUP
for _l in MARKUP: ENGINE[_l] = "static"
ENGINE["dart"] = "static"

def build(lid):
    if lid == "sql": return build_sql()
    if lid in MARKUP: return _mkmarkup(lid)
    return build_more(lid)

if __name__ == "__main__":
    bad = 0; tot = 0
    for lid in MORE:
        ls = build(lid)
        for l in ls:
            tot += 1
            s = l["hint"].lower()
            for t in l["expectedAll"]:
                if str(t).lower() not in s:
                    bad += 1; print("MISMATCH", lid, l["title"], "tok:", t); break
        print(lid, len(ls), "lessons")
    print("TOTAL", tot, "token-mismatches:", bad)
