# -*- coding: utf-8 -*-
"""Generates public/data/curriculum.js with module-based lessons for every language."""
import json

# id -> (Display name, exec id, engine, color, icon, blurb)
# engine: "pyodide" (browser python), "js" (browser JS), "ts" (browser TS), "server" (compiler API)
META = {
 "python":     ("Python","python","pyodide","#3776AB","\U0001F40D","Beginner-friendly, powerful, everywhere."),
 "javascript": ("JavaScript","javascript","js","#F7DF1E","\U0001F7E8","The language of the web."),
 "typescript": ("TypeScript","typescript","ts","#3178C6","\U0001F537","JavaScript with types."),
 "java":       ("Java","java","server","#ED8B00","\u2615","Write once, run anywhere."),
 "c":          ("C","c","server","#A8B9CC","\U0001F1E8","Close to the metal."),
 "cpp":        ("C++","c++","server","#00599C","\u2795","Power and performance."),
 "csharp":     ("C#","csharp","server","#239120","\u266F","Modern, versatile, by Microsoft."),
 "go":         ("Go","go","server","#00ADD8","\U0001F439","Simple, fast, concurrent."),
 "rust":       ("Rust","rust","server","#DEA584","\U0001F980","Safe, fast systems programming."),
 "ruby":       ("Ruby","ruby","server","#CC342D","\U0001F48E","A programmer's best friend."),
 "php":        ("PHP","php","server","#777BB4","\U0001F418","Powering the web's backends."),
 "swift":      ("Swift","swift","server","#FA7343","\U0001F985","Apple's modern language."),
 "kotlin":     ("Kotlin","kotlin","server","#7F52FF","\U0001F7E3","Concise JVM language."),
 "bash":       ("Bash","bash","server","#4EAA25","\U0001F4BB","Automate the shell."),
 "lua":        ("Lua","lua","server","#2C2D72","\U0001F319","Lightweight & embeddable."),
 "perl":       ("Perl","perl","server","#39457E","\U0001F42A","The Swiss-army chainsaw."),
 "dart":       ("Dart","dart","server","#0175C2","\U0001F3AF","Behind Flutter apps."),
 "scala":      ("Scala","scala","server","#DC322F","\U0001F53A","Functional meets OOP on the JVM."),
 "haskell":    ("Haskell","haskell","server","#5D4F85","\u03BB","Pure functional programming."),
 "elixir":     ("Elixir","elixir","server","#4B275F","\U0001F4A7","Scalable & fault-tolerant."),
 "r":          ("R","r","server","#276DC3","\U0001F4CA","Statistics & data science."),
 "julia":      ("Julia","julia","server","#9558B2","\U0001F52C","High-performance scientific computing."),
 "clojure":    ("Clojure","clojure","server","#5881D8","\U0001F343","A modern Lisp on the JVM."),
 "sqlite3":    ("SQL","sqlite3","server","#003B57","\U0001F5C4","Query data with SQL."),
}

ORDER = list(META.keys())

# Concept -> (module, title, difficulty, xp)
CONCEPTS = [
 ("hello",   "Getting Started",   "Hello, World",        "Easy",   10),
 ("var",     "Variables & Types", "Store a Value",       "Easy",   12),
 ("math",    "Operators & Math",  "Do the Math",         "Easy",   12),
 ("compare", "Conditionals",      "Compare Two Numbers", "Easy",   16),
 ("cond",    "Conditionals",      "Odd or Even",         "Medium", 18),
 ("str",     "Strings",           "Join Two Words",      "Easy",   14),
 ("loop",    "Loops",             "Count to Three",      "Medium", 20),
 ("while",   "Loops",             "While Countdown",     "Medium", 20),
 ("func",    "Functions",         "Add Function",        "Medium", 22),
]

BRIEF = {
 "hello": "Every journey starts with a greeting. Print exactly `Hello, World!`.",
 "var":   "Create a variable holding `42` and print it. Expected output: `42`.",
 "math":  "Compute and print `7 * 6`. Expected output: `42`.",
 "str":   "Join `Iron` and `yx` into one word and print it. Expected output: `Ironyx`.",
 "cond":  "Given `n = 7`, print `odd` if it's odd, otherwise `even`. Expected output: `odd`.",
 "loop":  "Print the numbers 1, 2, and 3, each on its own line.",
 "compare": "Print `yes` if `5` is greater than `3`, otherwise `no`. Expected output: `yes`.",
 "while":   "Use a **while** loop to print 1, 2, and 3, each on its own line.",
 "func":    "Write a function `add(a, b)` that returns the sum, then print `add(20, 22)`. Expected: `42`.",
}
EXPECT = {"hello":"Hello, World!","var":"42","math":"42","str":"Ironyx","cond":"odd","loop":"1\n2\n3",
          "compare":"yes","while":"1\n2\n3","func":"42"}

# Concept -> "how it works" explanation shown in every lesson.
EXPLAIN = {
 "hello": "**Printing** is how a program shows output to the user. You call the language's print/output function and hand it some text wrapped in quotes (a *string*). The program writes that text to the console, usually followed by a newline.\n\nExample: printing `\"Hello, World!\"` displays exactly `Hello, World!`. This tiny program is the traditional first step in every language because it proves your setup works.",
 "var": "A **variable** is a named box that stores a value so you can reuse it later. You *assign* a value to a name (e.g. `x = 42`), then refer to that name anywhere afterwards — for instance to print it.\n\nExample: set `x = 42`, then print `x` → it shows `42`. Change the value in one place and everywhere that uses the name updates automatically.",
 "math": "Computers calculate with **arithmetic operators**: `+` add, `-` subtract, `*` multiply, `/` divide, and `%` remainder. Expressions follow normal math precedence (multiplication before addition).\n\nExample: `7 * 6` is evaluated to `42` *before* it is printed, so the output is `42`.",
 "compare": "**Comparison operators** (`>`, `<`, `>=`, `<=`, `==`, `!=`) ask a yes/no question and produce a *boolean* (`true`/`false`). You pair them with a conditional to decide what to output.\n\nExample: `5 > 3` is true, so the program prints `yes`. If you changed it to `5 < 3` it would print `no`.",
 "cond": "**Conditionals** (`if` / `else`) run different code depending on whether a test is true. A common trick is the **modulo** operator `% 2`, which gives the remainder after dividing by 2: it's `0` for even numbers and `1` for odd numbers.\n\nExample: `7 % 2` is `1` (not zero) → `7` is odd, so we print `odd`.",
 "str": "**Strings** are sequences of characters (text). *Concatenation* joins two strings end-to-end into one.\n\nExample: joining `\"Iron\"` and `\"yx\"` gives `\"Ironyx\"`. Most languages use `+`; some use `.` (PHP/Perl), `..` (Lua), `<>` (Elixir), `*` (Julia), or `||` (SQL).",
 "loop": "A **`for` loop** repeats a block of code a known number of times by walking a counter through a range of values.\n\nExample: looping from 1 to 3 and printing the counter each pass outputs three lines: `1`, `2`, `3`. Loops save you from copy-pasting the same line over and over.",
 "while": "A **`while` loop** keeps repeating *as long as* its condition stays true. You typically start a counter, do some work (print it), then change the counter each pass. When the condition becomes false, the loop stops.\n\nExample: start `i = 1`, print `i`, add 1, and repeat while `i <= 3` → prints `1`, `2`, `3`. ⚠️ If you forget to update the counter, the condition never turns false and you get an *infinite loop*.",
 "func": "A **function** is a reusable, named block of logic. It accepts inputs (*parameters*), does work, and usually *returns* a result you can use elsewhere. Define it once, call it as many times as you like with different arguments.\n\nExample: `add(a, b)` returns `a + b`, so calling `add(20, 22)` produces `42`. Functions keep code organized and avoid repetition.",
}

# Per-language: concept -> (starter_scaffold, hint_solution)
S = {}
S["python"] = {
 "hello": ("# Print the greeting\n", 'print("Hello, World!")'),
 "var":   ("# Create a variable and print it\nx = \n", 'x = 42\nprint(x)'),
 "math":  ("# Print the product\n", 'print(7 * 6)'),
 "str":   ('a = "Iron"\nb = "yx"\n# Print them joined\n', 'print(a + b)'),
 "cond":  ("n = 7\n# Print 'odd' or 'even'\n", 'print("odd" if n % 2 else "even")'),
 "loop":  ("# Loop and print 1..3\n", 'for i in range(1, 4):\n    print(i)'),
}
S["javascript"] = {
 "hello": ("// Log the greeting\n", 'console.log("Hello, World!");'),
 "var":   ("// Declare a variable and log it\n", 'const x = 42;\nconsole.log(x);'),
 "math":  ("// Log the product\n", 'console.log(7 * 6);'),
 "str":   ('const a = "Iron", b = "yx";\n// Log them joined\n', 'console.log(a + b);'),
 "cond":  ("const n = 7;\n// Log 'odd' or 'even'\n", 'console.log(n % 2 ? "odd" : "even");'),
 "loop":  ("// Loop 1..3\n", 'for (let i = 1; i <= 3; i++) console.log(i);'),
}
S["typescript"] = {
 "hello": ("const msg: string = \"\";\nconsole.log(msg);\n", 'const msg: string = "Hello, World!";\nconsole.log(msg);'),
 "var":   ("const x: number = 0;\nconsole.log(x);\n", 'const x: number = 42;\nconsole.log(x);'),
 "math":  ("// Log the product\n", 'console.log(7 * 6);'),
 "str":   ('const a: string = "Iron";\nconst b: string = "yx";\n', 'console.log(a + b);'),
 "cond":  ("const n: number = 7;\n", 'console.log(n % 2 ? "odd" : "even");'),
 "loop":  ("// Loop 1..3\n", 'for (let i = 1; i <= 3; i++) console.log(i);'),
}
def java(body): return "public class Main {\n  public static void main(String[] args) {\n    "+body+"\n  }\n}\n"
S["java"] = {
 "hello": (java("// print here"), java('System.out.println("Hello, World!");')),
 "var":   (java("int x = 0; // change me\n    System.out.println(x);"), java('int x = 42;\n    System.out.println(x);')),
 "math":  (java("// print the product"), java('System.out.println(7 * 6);')),
 "str":   (java('String a = "Iron", b = "yx";\n    // print joined'), java('String a = "Iron", b = "yx";\n    System.out.println(a + b);')),
 "cond":  (java("int n = 7;\n    // print odd/even"), java('int n = 7;\n    System.out.println(n % 2 != 0 ? "odd" : "even");')),
 "loop":  (java("// loop 1..3"), java('for (int i = 1; i <= 3; i++) System.out.println(i);')),
}
def cwrap(body): return "#include <stdio.h>\nint main() {\n    "+body+"\n    return 0;\n}\n"
S["c"] = {
 "hello": (cwrap("// print here"), cwrap('printf("Hello, World!\\n");')),
 "var":   (cwrap("int x = 0;\n    printf(\"%d\\n\", x);"), cwrap('int x = 42;\n    printf("%d\\n", x);')),
 "math":  (cwrap("// print product with %d"), cwrap('printf("%d\\n", 7 * 6);')),
 "str":   (cwrap("// print Ironyx"), cwrap('printf("%s\\n", "Ironyx");')),
 "cond":  (cwrap("int n = 7;\n    // print odd/even"), cwrap('int n = 7;\n    printf("%s\\n", n % 2 ? "odd" : "even");')),
 "loop":  (cwrap("// loop 1..3"), cwrap('for (int i = 1; i <= 3; i++) printf("%d\\n", i);')),
}
def cpp(body, inc=""): return "#include <iostream>\n"+inc+"using namespace std;\nint main() {\n    "+body+"\n    return 0;\n}\n"
S["cpp"] = {
 "hello": (cpp("// print here"), cpp('cout << "Hello, World!" << endl;')),
 "var":   (cpp("int x = 0;\n    cout << x << endl;"), cpp('int x = 42;\n    cout << x << endl;')),
 "math":  (cpp("// print product"), cpp('cout << 7 * 6 << endl;')),
 "str":   (cpp("// build and print Ironyx", "#include <string>\n"), cpp('string s = string("Iron") + "yx";\n    cout << s << endl;', "#include <string>\n")),
 "cond":  (cpp("int n = 7;\n    // print odd/even"), cpp('int n = 7;\n    cout << (n % 2 ? "odd" : "even") << endl;')),
 "loop":  (cpp("// loop 1..3"), cpp('for (int i = 1; i <= 3; i++) cout << i << endl;')),
}
def cs(body): return "using System;\nclass Program {\n  static void Main() {\n    "+body+"\n  }\n}\n"
S["csharp"] = {
 "hello": (cs("// print here"), cs('Console.WriteLine("Hello, World!");')),
 "var":   (cs("int x = 0;\n    Console.WriteLine(x);"), cs('int x = 42;\n    Console.WriteLine(x);')),
 "math":  (cs("// print product"), cs('Console.WriteLine(7 * 6);')),
 "str":   (cs('// print joined'), cs('Console.WriteLine("Iron" + "yx");')),
 "cond":  (cs("int n = 7;"), cs('int n = 7;\n    Console.WriteLine(n % 2 != 0 ? "odd" : "even");')),
 "loop":  (cs("// loop 1..3"), cs('for (int i = 1; i <= 3; i++) Console.WriteLine(i);')),
}
def go(body): return 'package main\nimport "fmt"\nfunc main() {\n    '+body+'\n}\n'
S["go"] = {
 "hello": (go("// print here"), go('fmt.Println("Hello, World!")')),
 "var":   (go("x := 0\n    fmt.Println(x)"), go('x := 42\n    fmt.Println(x)')),
 "math":  (go("// print product"), go('fmt.Println(7 * 6)')),
 "str":   (go('// print joined'), go('fmt.Println("Iron" + "yx")')),
 "cond":  (go("n := 7\n    // print odd/even"), go('n := 7\n    if n%2 != 0 {\n        fmt.Println("odd")\n    } else {\n        fmt.Println("even")\n    }')),
 "loop":  (go("// loop 1..3"), go('for i := 1; i <= 3; i++ {\n        fmt.Println(i)\n    }')),
}
def rust(body): return "fn main() {\n    "+body+"\n}\n"
S["rust"] = {
 "hello": (rust("// print here"), rust('println!("Hello, World!");')),
 "var":   (rust("let x = 0;\n    println!(\"{}\", x);"), rust('let x = 42;\n    println!("{}", x);')),
 "math":  (rust("// print product"), rust('println!("{}", 7 * 6);')),
 "str":   (rust('// build & print Ironyx'), rust('let s = format!("{}{}", "Iron", "yx");\n    println!("{}", s);')),
 "cond":  (rust("let n = 7;"), rust('let n = 7;\n    println!("{}", if n % 2 != 0 { "odd" } else { "even" });')),
 "loop":  (rust("// loop 1..=3"), rust('for i in 1..=3 {\n        println!("{}", i);\n    }')),
}
S["ruby"] = {
 "hello": ("# print here\n", 'puts "Hello, World!"'),
 "var":   ("x = 0\nputs x\n", 'x = 42\nputs x'),
 "math":  ("# print product\n", 'puts 7 * 6'),
 "str":   ('# print joined\n', 'puts "Iron" + "yx"'),
 "cond":  ("n = 7\n", 'n = 7\nputs(n.odd? ? "odd" : "even")'),
 "loop":  ("# loop 1..3\n", '(1..3).each { |i| puts i }'),
}
S["php"] = {
 "hello": ("<?php\n// echo here\n", '<?php\necho "Hello, World!\\n";'),
 "var":   ("<?php\n$x = 0;\necho $x . \"\\n\";\n", '<?php\n$x = 42;\necho $x . "\\n";'),
 "math":  ("<?php\n// echo product\n", '<?php\necho (7 * 6) . "\\n";'),
 "str":   ('<?php\n// echo joined\n', '<?php\necho "Iron" . "yx" . "\\n";'),
 "cond":  ("<?php\n$n = 7;\n", '<?php\n$n = 7;\necho ($n % 2 ? "odd" : "even") . "\\n";'),
 "loop":  ("<?php\n// loop 1..3\n", '<?php\nfor ($i = 1; $i <= 3; $i++) echo $i . "\\n";'),
}
S["swift"] = {
 "hello": ("// print here\n", 'print("Hello, World!")'),
 "var":   ("let x = 0\nprint(x)\n", 'let x = 42\nprint(x)'),
 "math":  ("// print product\n", 'print(7 * 6)'),
 "str":   ('// print joined\n', 'print("Iron" + "yx")'),
 "cond":  ("let n = 7\n", 'let n = 7\nprint(n % 2 != 0 ? "odd" : "even")'),
 "loop":  ("// loop 1...3\n", 'for i in 1...3 {\n    print(i)\n}'),
}
def kt(body): return "fun main() {\n    "+body+"\n}\n"
S["kotlin"] = {
 "hello": (kt("// print here"), kt('println("Hello, World!")')),
 "var":   (kt("val x = 0\n    println(x)"), kt('val x = 42\n    println(x)')),
 "math":  (kt("// print product"), kt('println(7 * 6)')),
 "str":   (kt('// print joined'), kt('println("Iron" + "yx")')),
 "cond":  (kt("val n = 7"), kt('val n = 7\n    println(if (n % 2 != 0) "odd" else "even")')),
 "loop":  (kt("// loop 1..3"), kt('for (i in 1..3) println(i)')),
}
S["bash"] = {
 "hello": ("# echo here\n", 'echo "Hello, World!"'),
 "var":   ("x=0\necho $x\n", 'x=42\necho $x'),
 "math":  ("# echo product\n", 'echo $((7 * 6))'),
 "str":   ('# echo joined\n', 'echo "Iron""yx"'),
 "cond":  ("n=7\n", 'n=7\nif (( n % 2 )); then echo odd; else echo even; fi'),
 "loop":  ("# loop 1..3\n", 'for i in 1 2 3; do echo $i; done'),
}
S["lua"] = {
 "hello": ("-- print here\n", 'print("Hello, World!")'),
 "var":   ("local x = 0\nprint(x)\n", 'local x = 42\nprint(x)'),
 "math":  ("-- print product\n", 'print(7 * 6)'),
 "str":   ('-- print joined\n', 'print("Iron" .. "yx")'),
 "cond":  ("local n = 7\n", 'local n = 7\nif n % 2 ~= 0 then print("odd") else print("even") end'),
 "loop":  ("-- loop 1..3\n", 'for i = 1, 3 do print(i) end'),
}
S["perl"] = {
 "hello": ("# print here\n", 'print "Hello, World!\\n";'),
 "var":   ("my $x = 0;\nprint \"$x\\n\";\n", 'my $x = 42;\nprint "$x\\n";'),
 "math":  ("# print product\n", 'print 7 * 6, "\\n";'),
 "str":   ('# print joined\n', 'print "Iron" . "yx", "\\n";'),
 "cond":  ("my $n = 7;\n", 'my $n = 7;\nprint(($n % 2 ? "odd" : "even"), "\\n");'),
 "loop":  ("# loop 1..3\n", 'for my $i (1..3) { print "$i\\n"; }'),
}
def dart(body): return "void main() {\n  "+body+"\n}\n"
S["dart"] = {
 "hello": (dart("// print here"), dart("print('Hello, World!');")),
 "var":   (dart("var x = 0;\n  print(x);"), dart("var x = 42;\n  print(x);")),
 "math":  (dart("// print product"), dart("print(7 * 6);")),
 "str":   (dart("// print joined"), dart("print('Iron' + 'yx');")),
 "cond":  (dart("var n = 7;"), dart("var n = 7;\n  print(n % 2 != 0 ? 'odd' : 'even');")),
 "loop":  (dart("// loop 1..3"), dart("for (var i = 1; i <= 3; i++) print(i);")),
}
def scala(body): return "object Main {\n  def main(args: Array[String]): Unit = {\n    "+body+"\n  }\n}\n"
S["scala"] = {
 "hello": (scala("// print here"), scala('println("Hello, World!")')),
 "var":   (scala("val x = 0\n  println(x)"), scala('val x = 42\n  println(x)')),
 "math":  (scala("// print product"), scala('println(7 * 6)')),
 "str":   (scala("// print joined"), scala('println("Iron" + "yx")')),
 "cond":  (scala("val n = 7"), scala('val n = 7\n  println(if (n % 2 != 0) "odd" else "even")')),
 "loop":  (scala("// loop 1..3"), scala('for (i <- 1 to 3) println(i)')),
}
S["haskell"] = {
 "hello": ("main :: IO ()\nmain = putStrLn \"\"\n", 'main :: IO ()\nmain = putStrLn "Hello, World!"'),
 "var":   ("main = print (0 :: Int)\n", 'main = print (42 :: Int)'),
 "math":  ("main = print (0 :: Int)\n", 'main = print (7 * 6 :: Int)'),
 "str":   ('main = putStrLn ("" ++ "")\n', 'main = putStrLn ("Iron" ++ "yx")'),
 "cond":  ("main = putStrLn (if odd (7 :: Int) then \"\" else \"\")\n", 'main = putStrLn (if odd (7 :: Int) then "odd" else "even")'),
 "loop":  ("main = mapM_ print []\n", 'main = mapM_ print [1..3]'),
}
S["elixir"] = {
 "hello": ("# print here\n", 'IO.puts "Hello, World!"'),
 "var":   ("x = 0\nIO.puts x\n", 'x = 42\nIO.puts x'),
 "math":  ("# print product\n", 'IO.puts 7 * 6'),
 "str":   ('# print joined\n', 'IO.puts "Iron" <> "yx"'),
 "cond":  ("n = 7\n", 'n = 7\nIO.puts(if rem(n, 2) != 0, do: "odd", else: "even")'),
 "loop":  ("# loop 1..3\n", 'for i <- 1..3, do: IO.puts(i)'),
}
S["r"] = {
 "hello": ("# print here\n", 'cat("Hello, World!\\n")'),
 "var":   ("x <- 0\ncat(x, \"\\n\", sep=\"\")\n", 'x <- 42\ncat(x, "\\n", sep="")'),
 "math":  ("# print product\n", 'cat(7 * 6, "\\n", sep="")'),
 "str":   ('# print joined\n', 'cat(paste0("Iron", "yx"), "\\n", sep="")'),
 "cond":  ("n <- 7\n", 'n <- 7\ncat(if (n %% 2 != 0) "odd" else "even", "\\n", sep="")'),
 "loop":  ("# loop 1..3\n", 'for (i in 1:3) cat(i, "\\n", sep="")'),
}
S["julia"] = {
 "hello": ("# print here\n", 'println("Hello, World!")'),
 "var":   ("x = 0\nprintln(x)\n", 'x = 42\nprintln(x)'),
 "math":  ("# print product\n", 'println(7 * 6)'),
 "str":   ('# print joined\n', 'println("Iron" * "yx")'),
 "cond":  ("n = 7\n", 'n = 7\nprintln(n % 2 != 0 ? "odd" : "even")'),
 "loop":  ("# loop 1..3\n", 'for i in 1:3\n    println(i)\nend'),
}
S["clojure"] = {
 "hello": (";; print here\n", '(println "Hello, World!")'),
 "var":   ("(def x 0)\n(println x)\n", '(def x 42)\n(println x)'),
 "math":  (";; print product\n", '(println (* 7 6))'),
 "str":   (';; print joined\n', '(println (str "Iron" "yx"))'),
 "cond":  ("(def n 7)\n", '(def n 7)\n(println (if (odd? n) "odd" "even"))'),
 "loop":  (";; loop 1..3\n", '(doseq [i (range 1 4)] (println i))'),
}
S["sqlite3"] = {
 "hello": ("-- write your query\n", "SELECT 'Hello, World!';"),
 "var":   ("-- select 42\n", "SELECT 42;"),
 "math":  ("-- select the product\n", "SELECT 7 * 6;"),
 "str":   ('-- concatenate with ||\n', "SELECT 'Iron' || 'yx';"),
 "cond":  ("-- use CASE WHEN\n", "SELECT CASE WHEN 7 % 2 != 0 THEN 'odd' ELSE 'even' END;"),
 "loop":  ("-- UNION ALL three selects\n", "SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3;"),
}

# ---- New question types added to every language: compare / while / func ----
S["python"].update({
 "compare": ("# Print 'yes' or 'no'\n", 'print("yes" if 5 > 3 else "no")'),
 "while":   ("# Use a while loop to print 1..3\ni = 1\n", 'i = 1\nwhile i <= 3:\n    print(i)\n    i += 1'),
 "func":    ("def add(a, b):\n    return 0\nprint(add(20, 22))\n", 'def add(a, b):\n    return a + b\nprint(add(20, 22))'),
})
S["javascript"].update({
 "compare": ("// Log 'yes' or 'no'\n", 'console.log(5 > 3 ? "yes" : "no");'),
 "while":   ("let i = 1;\n// while loop here\n", 'let i = 1;\nwhile (i <= 3) {\n  console.log(i);\n  i++;\n}'),
 "func":    ("function add(a, b) {\n  return 0;\n}\nconsole.log(add(20, 22));\n", 'function add(a, b) {\n  return a + b;\n}\nconsole.log(add(20, 22));'),
})
S["typescript"].update({
 "compare": ("// Log 'yes' or 'no'\n", 'console.log(5 > 3 ? "yes" : "no");'),
 "while":   ("let i: number = 1;\n", 'let i: number = 1;\nwhile (i <= 3) {\n  console.log(i);\n  i++;\n}'),
 "func":    ("function add(a: number, b: number): number {\n  return 0;\n}\nconsole.log(add(20, 22));\n", 'function add(a: number, b: number): number {\n  return a + b;\n}\nconsole.log(add(20, 22));'),
})
S["java"].update({
 "compare": (java("// print yes/no"), java('System.out.println(5 > 3 ? "yes" : "no");')),
 "while":   (java("int i = 1;\n    // while loop"), java('int i = 1;\n    while (i <= 3) {\n      System.out.println(i);\n      i++;\n    }')),
 "func":    ("public class Main {\n  static int add(int a, int b) {\n    return 0;\n  }\n  public static void main(String[] args) {\n    System.out.println(add(20, 22));\n  }\n}\n",
             "public class Main {\n  static int add(int a, int b) {\n    return a + b;\n  }\n  public static void main(String[] args) {\n    System.out.println(add(20, 22));\n  }\n}\n"),
})
S["c"].update({
 "compare": (cwrap("// print yes/no"), cwrap('printf("%s\\n", 5 > 3 ? "yes" : "no");')),
 "while":   (cwrap("int i = 1;\n    // while loop"), cwrap('int i = 1;\n    while (i <= 3) {\n        printf("%d\\n", i);\n        i++;\n    }')),
 "func":    ("#include <stdio.h>\nint add(int a, int b) {\n    return 0;\n}\nint main() {\n    printf(\"%d\\n\", add(20, 22));\n    return 0;\n}\n",
             "#include <stdio.h>\nint add(int a, int b) {\n    return a + b;\n}\nint main() {\n    printf(\"%d\\n\", add(20, 22));\n    return 0;\n}\n"),
})
S["cpp"].update({
 "compare": (cpp("// print yes/no"), cpp('cout << (5 > 3 ? "yes" : "no") << endl;')),
 "while":   (cpp("int i = 1;\n    // while loop"), cpp('int i = 1;\n    while (i <= 3) {\n        cout << i << endl;\n        i++;\n    }')),
 "func":    ("#include <iostream>\nusing namespace std;\nint add(int a, int b) { return 0; }\nint main() { cout << add(20, 22) << endl; }\n",
             "#include <iostream>\nusing namespace std;\nint add(int a, int b) { return a + b; }\nint main() { cout << add(20, 22) << endl; }\n"),
})
S["csharp"].update({
 "compare": (cs("// print yes/no"), cs('Console.WriteLine(5 > 3 ? "yes" : "no");')),
 "while":   (cs("int i = 1;\n    // while loop"), cs('int i = 1;\n    while (i <= 3) {\n      Console.WriteLine(i);\n      i++;\n    }')),
 "func":    ("using System;\nclass Program {\n  static int Add(int a, int b) { return 0; }\n  static void Main() { Console.WriteLine(Add(20, 22)); }\n}\n",
             "using System;\nclass Program {\n  static int Add(int a, int b) { return a + b; }\n  static void Main() { Console.WriteLine(Add(20, 22)); }\n}\n"),
})
S["go"].update({
 "compare": (go("// print yes/no"), go('if 5 > 3 {\n        fmt.Println("yes")\n    } else {\n        fmt.Println("no")\n    }')),
 "while":   (go("i := 1\n    // Go uses for as a while"), go('i := 1\n    for i <= 3 {\n        fmt.Println(i)\n        i++\n    }')),
 "func":    ("package main\nimport \"fmt\"\nfunc add(a, b int) int { return 0 }\nfunc main() { fmt.Println(add(20, 22)) }\n",
             "package main\nimport \"fmt\"\nfunc add(a, b int) int { return a + b }\nfunc main() { fmt.Println(add(20, 22)) }\n"),
})
S["rust"].update({
 "compare": (rust("// print yes/no"), rust('println!("{}", if 5 > 3 { "yes" } else { "no" });')),
 "while":   (rust("let mut i = 1;\n    // while loop"), rust('let mut i = 1;\n    while i <= 3 {\n        println!("{}", i);\n        i += 1;\n    }')),
 "func":    ("fn add(a: i32, b: i32) -> i32 {\n    0\n}\nfn main() {\n    println!(\"{}\", add(20, 22));\n}\n",
             "fn add(a: i32, b: i32) -> i32 {\n    a + b\n}\nfn main() {\n    println!(\"{}\", add(20, 22));\n}\n"),
})
S["ruby"].update({
 "compare": ("# print yes/no\n", 'puts(5 > 3 ? "yes" : "no")'),
 "while":   ("i = 1\n# while loop\n", 'i = 1\nwhile i <= 3\n  puts i\n  i += 1\nend'),
 "func":    ("def add(a, b)\n  0\nend\nputs add(20, 22)\n", 'def add(a, b)\n  a + b\nend\nputs add(20, 22)'),
})
S["php"].update({
 "compare": ("<?php\n// print yes/no\n", '<?php\necho (5 > 3 ? "yes" : "no") . "\\n";'),
 "while":   ("<?php\n$i = 1;\n", '<?php\n$i = 1;\nwhile ($i <= 3) {\n    echo $i . "\\n";\n    $i++;\n}'),
 "func":    ("<?php\nfunction add($a, $b) {\n    return 0;\n}\necho add(20, 22) . \"\\n\";\n", '<?php\nfunction add($a, $b) {\n    return $a + $b;\n}\necho add(20, 22) . "\\n";'),
})
S["swift"].update({
 "compare": ("// print yes/no\n", 'print(5 > 3 ? "yes" : "no")'),
 "while":   ("var i = 1\n", 'var i = 1\nwhile i <= 3 {\n    print(i)\n    i += 1\n}'),
 "func":    ("func add(_ a: Int, _ b: Int) -> Int {\n    return 0\n}\nprint(add(20, 22))\n", 'func add(_ a: Int, _ b: Int) -> Int {\n    return a + b\n}\nprint(add(20, 22))'),
})
S["kotlin"].update({
 "compare": (kt("// print yes/no"), kt('println(if (5 > 3) "yes" else "no")')),
 "while":   (kt("var i = 1\n    // while loop"), kt('var i = 1\n    while (i <= 3) {\n        println(i)\n        i++\n    }')),
 "func":    ("fun add(a: Int, b: Int): Int = 0\nfun main() {\n    println(add(20, 22))\n}\n", 'fun add(a: Int, b: Int): Int = a + b\nfun main() {\n    println(add(20, 22))\n}'),
})
S["bash"].update({
 "compare": ("# print yes/no\n", 'if [ 5 -gt 3 ]; then echo yes; else echo no; fi'),
 "while":   ("i=1\n# while loop\n", 'i=1\nwhile [ $i -le 3 ]; do\n  echo $i\n  i=$((i+1))\ndone'),
 "func":    ("add() {\n  echo 0\n}\nadd 20 22\n", 'add() {\n  echo $(( $1 + $2 ))\n}\nadd 20 22'),
})
S["lua"].update({
 "compare": ("-- print yes/no\n", 'print(5 > 3 and "yes" or "no")'),
 "while":   ("local i = 1\n", 'local i = 1\nwhile i <= 3 do\n  print(i)\n  i = i + 1\nend'),
 "func":    ("function add(a, b)\n  return 0\nend\nprint(add(20, 22))\n", 'function add(a, b)\n  return a + b\nend\nprint(add(20, 22))'),
})
S["perl"].update({
 "compare": ("# print yes/no\n", 'print((5 > 3 ? "yes" : "no"), "\\n");'),
 "while":   ("my $i = 1;\n", 'my $i = 1;\nwhile ($i <= 3) {\n    print "$i\\n";\n    $i++;\n}'),
 "func":    ("sub add {\n    return 0;\n}\nprint add(20, 22), \"\\n\";\n", 'sub add {\n    return $_[0] + $_[1];\n}\nprint add(20, 22), "\\n";'),
})
S["dart"].update({
 "compare": (dart("// print yes/no"), dart("print(5 > 3 ? 'yes' : 'no');")),
 "while":   (dart("var i = 1;\n  // while loop"), dart("var i = 1;\n  while (i <= 3) {\n    print(i);\n    i++;\n  }")),
 "func":    ("int add(int a, int b) => 0;\nvoid main() {\n  print(add(20, 22));\n}\n", "int add(int a, int b) => a + b;\nvoid main() {\n  print(add(20, 22));\n}"),
})
S["scala"].update({
 "compare": (scala("// print yes/no"), scala('println(if (5 > 3) "yes" else "no")')),
 "while":   (scala("var i = 1\n  // while loop"), scala('var i = 1\n  while (i <= 3) {\n    println(i)\n    i += 1\n  }')),
 "func":    ("object Main {\n  def add(a: Int, b: Int) = 0\n  def main(args: Array[String]): Unit = println(add(20, 22))\n}\n", 'object Main {\n  def add(a: Int, b: Int) = a + b\n  def main(args: Array[String]): Unit = println(add(20, 22))\n}'),
})
S["haskell"].update({
 "compare": ("main = putStrLn (if 5 > 3 then \"\" else \"\")\n", 'main = putStrLn (if 5 > 3 then "yes" else "no")'),
 "func":    ("add :: Int -> Int -> Int\nadd a b = 0\nmain = print (add 20 22)\n", 'add :: Int -> Int -> Int\nadd a b = a + b\nmain = print (add 20 22)'),
})
S["elixir"].update({
 "compare": ("# print yes/no\n", 'IO.puts(if 5 > 3, do: "yes", else: "no")'),
 "func":    ("add = fn a, b -> 0 end\nIO.puts add.(20, 22)\n", 'add = fn a, b -> a + b end\nIO.puts add.(20, 22)'),
})
S["r"].update({
 "compare": ("# print yes/no\n", 'cat(if (5 > 3) "yes" else "no", "\\n", sep="")'),
 "while":   ("i <- 1\n", 'i <- 1\nwhile (i <= 3) {\n  cat(i, "\\n", sep="")\n  i <- i + 1\n}'),
 "func":    ("add <- function(a, b) 0\ncat(add(20, 22), \"\\n\", sep=\"\")\n", 'add <- function(a, b) a + b\ncat(add(20, 22), "\\n", sep="")'),
})
S["julia"].update({
 "compare": ("# print yes/no\n", 'println(5 > 3 ? "yes" : "no")'),
 "while":   ("i = 1\n", 'i = 1\nwhile i <= 3\n    println(i)\n    global i += 1\nend'),
 "func":    ("add(a, b) = 0\nprintln(add(20, 22))\n", 'add(a, b) = a + b\nprintln(add(20, 22))'),
})
S["clojure"].update({
 "compare": (";; print yes/no\n", '(println (if (> 5 3) "yes" "no"))'),
 "func":    ("(defn add [a b] 0)\n(println (add 20 22))\n", '(defn add [a b] (+ a b))\n(println (add 20 22))'),
})
S["sqlite3"].update({
 "compare": ("-- use CASE WHEN with >\n", "SELECT CASE WHEN 5 > 3 THEN 'yes' ELSE 'no' END;"),
})

# ---- Extra advanced lessons for major languages ----
# Each EXTRA item is a dict with its own explanation (the universal Add Function
# lessons now come from the shared CONCEPTS pipeline, so they are not repeated here).
EXTRA = {}
EXTRA["python"] = [
 {"module":"Collections","title":"Sum a List","difficulty":"Medium","xp":22,
  "brief":"Print the sum of `[1, 2, 3, 4]`. Expected: `10`.","hint":"nums = [1, 2, 3, 4]\nprint(sum(nums))",
  "starter":"nums = [1, 2, 3, 4]\n# print the sum\n","expectedOutput":"10",
  "explanation":"A **list** holds many values in order. The built-in `sum()` adds every element together.\n\nExample: `sum([1, 2, 3, 4])` = `1+2+3+4` = `10`. You can also loop and accumulate manually, but `sum()` is the idiomatic shortcut."},
 {"module":"Collections","title":"Dictionary Lookup","difficulty":"Medium","xp":22,
  "brief":"Given `d = {'a': 1, 'b': 2}`, print the value for key `b`. Expected: `2`.","hint":"d = {'a': 1, 'b': 2}\nprint(d['b'])",
  "starter":"d = {'a': 1, 'b': 2}\n# print value for 'b'\n","expectedOutput":"2",
  "explanation":"A **dictionary** maps unique *keys* to *values*. You retrieve a value by its key using square brackets `d[key]`.\n\nExample: for `{'a': 1, 'b': 2}`, `d['b']` returns `2`. Dictionaries give fast lookups by key instead of position."},
 {"module":"Projects","title":"FizzBuzz (1-15)","difficulty":"Hard","xp":35,
  "brief":"Print 1 to 15. For multiples of 3 print `Fizz`, multiples of 5 `Buzz`, both `FizzBuzz`.",
  "hint":'for n in range(1, 16):\n    if n % 15 == 0: print("FizzBuzz")\n    elif n % 3 == 0: print("Fizz")\n    elif n % 5 == 0: print("Buzz")\n    else: print(n)',
  "starter":"for n in range(1, 16):\n    # your logic\n    pass\n",
  "expectedOutput":"1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz",
  "explanation":"The classic interview puzzle. Loop the numbers and use **modulo** to test divisibility. Order matters: check `% 15` (divisible by both 3 *and* 5) **first**, then `% 3`, then `% 5`, otherwise print the number.\n\nExample: 3 → `Fizz`, 5 → `Buzz`, 15 → `FizzBuzz`, 7 → `7`."},
 {"module":"Projects","title":"Sum to 100","difficulty":"Medium","xp":24,
  "brief":"Print the sum of all integers from 1 to 100. Expected: `5050`.","hint":"print(sum(range(1, 101)))",
  "starter":"# print the sum 1..100\n","expectedOutput":"5050",
  "explanation":"Accumulate a running total across a range. Here `sum(range(1, 101))` adds 1 through 100.\n\nExample / math shortcut: the sum 1..n equals `n*(n+1)/2`, so 1..100 = `100*101/2` = `5050`."},
]
EXTRA["javascript"] = [
 {"module":"Collections","title":"Sum an Array","difficulty":"Medium","xp":22,
  "brief":"Print the sum of `[1, 2, 3, 4]`. Expected: `10`.","hint":"const nums = [1, 2, 3, 4];\nconsole.log(nums.reduce((a, b) => a + b, 0));",
  "starter":"const nums = [1, 2, 3, 4];\n// log the sum\n","expectedOutput":"10",
  "explanation":"`reduce` *folds* an array into a single value by repeatedly combining elements with an accumulator.\n\nExample: `[1,2,3,4].reduce((a, b) => a + b, 0)` starts at 0 and adds each element → `10`."},
 {"module":"Strings","title":"Reverse a String","difficulty":"Medium","xp":20,
  "brief":"Reverse `\"code\"` and log it. Expected: `edoc`.","hint":"const s = \"code\";\nconsole.log(s.split('').reverse().join(''));",
  "starter":"const s = \"code\";\n// log reversed\n","expectedOutput":"edoc",
  "explanation":"Strings don't reverse directly, so the trick is: **split** into a character array, **reverse** the array, then **join** it back into a string.\n\nExample: `'code'` → `['c','o','d','e']` → reversed `['e','d','o','c']` → `'edoc'`."},
 {"module":"Projects","title":"FizzBuzz (1-15)","difficulty":"Hard","xp":35,
  "brief":"Print 1 to 15 with Fizz/Buzz/FizzBuzz rules.",
  "hint":'for (let i = 1; i <= 15; i++) {\n  if (i % 15 === 0) console.log("FizzBuzz");\n  else if (i % 3 === 0) console.log("Fizz");\n  else if (i % 5 === 0) console.log("Buzz");\n  else console.log(i);\n}',
  "starter":"for (let i = 1; i <= 15; i++) {\n  // your logic\n}\n",
  "expectedOutput":"1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz",
  "explanation":"Loop the numbers and use **modulo** for divisibility. Check `% 15` first (both 3 and 5), then `% 3`, then `% 5`, else the number itself.\n\nExample: 3 → `Fizz`, 5 → `Buzz`, 15 → `FizzBuzz`."},
]
EXTRA["java"] = [
 {"module":"Projects","title":"Sum to 100","difficulty":"Medium","xp":24,
  "brief":"Print the sum of 1..100. Expected: `5050`.","hint":java('int sum = 0;\n    for (int i = 1; i <= 100; i++) sum += i;\n    System.out.println(sum);'),
  "starter":java("int sum = 0;\n    // loop\n    System.out.println(sum);"),"expectedOutput":"5050",
  "explanation":"Use a loop to build a running total. Start `sum = 0`, then add each `i` from 1 to 100.\n\nExample / shortcut: 1..n = `n*(n+1)/2`, so 1..100 = `5050`."},
]
EXTRA["cpp"] = [
 {"module":"Projects","title":"Sum to 100","difficulty":"Medium","xp":24,
  "brief":"Print the sum of 1..100. Expected: `5050`.","hint":cpp('int sum = 0;\n    for (int i = 1; i <= 100; i++) sum += i;\n    cout << sum << endl;'),
  "starter":cpp("int sum = 0;\n    // loop\n    cout << sum << endl;"),"expectedOutput":"5050",
  "explanation":"Accumulate a total in a loop. Start `sum = 0` and add each `i`.\n\nExample / shortcut: 1..n = `n*(n+1)/2` → 1..100 = `5050`."},
]
EXTRA["go"] = [
 {"module":"Projects","title":"Sum to 100","difficulty":"Medium","xp":24,
  "brief":"Print the sum of 1..100. Expected: `5050`.","hint":go('sum := 0\n    for i := 1; i <= 100; i++ {\n        sum += i\n    }\n    fmt.Println(sum)'),
  "starter":go("sum := 0\n    // loop\n    fmt.Println(sum)"),"expectedOutput":"5050",
  "explanation":"Loop and accumulate into `sum`.\n\nExample / shortcut: 1..n = `n*(n+1)/2`, so 1..100 = `5050`."},
]

# ---- assemble ----
tracks = []
for lid in ORDER:
    name, exec_id, engine, color, icon, blurb = META[lid]
    lessons = []
    n = 1
    for ckey, module, title, diff, xp in CONCEPTS:
        if ckey not in S[lid]:
            continue
        starter, hint = S[lid][ckey]
        lesson = {
            "id": f"{lid}-{n}", "module": module, "title": title,
            "xp": xp, "difficulty": diff, "brief": BRIEF[ckey],
            "explanation": EXPLAIN[ckey], "hint": hint, "starter": starter,
        }
        if lid == "sqlite3":
            lesson["expectedContains"] = EXPECT[ckey].split("\n")[0]
        else:
            lesson["expectedOutput"] = EXPECT[ckey]
        lessons.append(lesson); n += 1
    for item in EXTRA.get(lid, []):
        lesson = {"id": f"{lid}-{n}"}
        lesson.update(item)
        lessons.append(lesson); n += 1
    tracks.append({
        "id": lid, "name": name, "lang": exec_id, "engine": engine,
        "color": color, "icon": icon, "blurb": blurb, "lessons": lessons,
    })

# ---- override the 10 rich languages with the big bank + DSA module ----
import bigbank, dsa
for lid in bigbank.RICH:
    tr = next((t for t in tracks if t["id"] == lid), None)
    if tr:
        tr["lessons"] = bigbank.build_rich(lid) + dsa.build_dsa(lid)

# ---- big structure-graded banks for the remaining traditional languages ----
import morebank
for lid in morebank.ALL:
    tid = "sqlite3" if lid == "sql" else lid
    tr = next((t for t in tracks if t["id"] == tid), None)
    if tr:
        tr["lessons"] = morebank.build(lid)
        tr["engine"] = morebank.ENGINE[lid]

# ---- learning material attached to every module of every language ----
MODULE_GUIDE = {
 "Getting Started": "**Welcome!** Every program communicates by producing *output*. The first skill in any language is printing text to the console. You call a built-in print function and pass it a **string** — text wrapped in quotes. Master this and you can see what your code is doing at every step.\n\n**Key idea:** strings are text in quotes; the print function sends them to the screen.",
 "Variables & Types": "**Variables** are named containers that store values you want to reuse. You *assign* a value to a name, then refer to the name later. Values have **types** — whole numbers (integers), text (strings), decimals, booleans (true/false). Most languages either infer the type automatically or let you declare it.\n\n**Key idea:** assign once, reuse the name everywhere; the type describes what kind of value it holds.",
 "Operators & Math": "**Operators** combine values. Arithmetic: `+` `-` `*` `/` and `%` (remainder). Expressions follow normal math precedence — multiplication and division before addition and subtraction. Integer vs. floating-point division can behave differently, so watch your types.\n\n**Key idea:** an expression is evaluated to a single value before it's used or printed.",
 "Conditionals": "**Conditionals** let a program make decisions. A *comparison* (`>`, `<`, `==`, `!=`) produces a boolean, and `if` / `else` runs different code depending on the result. The `%` (modulo) operator is a workhorse here — `n % 2` tells you if a number is even or odd.\n\n**Key idea:** branch your logic based on true/false tests.",
 "Strings": "**Strings** are sequences of characters. Common operations: *concatenation* (joining with `+`, `.`, `..`, `<>`, `*`, or `||` depending on the language), measuring **length**, indexing characters, and slicing. Text processing is one of the most common real-world programming tasks.\n\n**Key idea:** strings can be combined, measured, and taken apart.",
 "Loops": "**Loops** repeat work. A `for` loop runs a known number of times by walking a counter through a range; a `while` loop runs as long as a condition stays true. Loops often build a *running total* or transform each item. Always make sure the loop can end — or you'll spin forever.\n\n**Key idea:** repeat a block instead of copy-pasting it.",
 "Functions": "**Functions** package reusable logic. They take **parameters** (inputs), do work, and usually **return** a result. Define a function once and call it as many times as you like with different arguments. Functions make code shorter, clearer, and testable.\n\n**Key idea:** name a piece of logic so you can reuse it.",
 "Collections": "**Collections** hold many values together. Arrays / lists keep items in order, accessible by index. You'll constantly sum them, find the max/min, search them, filter them, and loop over them. Mastering collections unlocks almost every real algorithm.\n\n**Key idea:** store many values in one structure, then process them together.",
 "Projects": "**Projects** combine everything — variables, conditionals, loops, and functions — into complete mini-programs like FizzBuzz, factorials, and number patterns. This is where the individual skills click together into real problem-solving.\n\n**Key idea:** compose small skills to solve a bigger problem.",
 "\U0001F9E9 DSA Challenges": "**Data Structures & Algorithms (DSA)** are the classic interview and competitive-programming problems — Two Sum, palindromes, Fibonacci, prime checks, sorting, searching, GCD, and more. Each problem teaches a reusable technique: two-pointer scans, accumulators, divide-by-10 digit tricks, and array traversal.\n\n**Key idea:** recognise the pattern, then apply the right technique. These are the problems that show up in coding interviews.",
 "Output & Printing": "**Output** is how a program shows results. Learn your language's print/output statement and practice printing text (strings, in quotes) and numbers. This is the foundation you'll use to inspect everything else you build.",
 "Comments & Syntax": "**Comments** are notes the compiler ignores — they explain *why* code does something. Every language has its own comment marker (`//`, `#`, `--`, `;`). Good comments make code readable for your future self and teammates.",
}
for tr in tracks:
    mats = {}
    for l in tr["lessons"]:
        m = l["module"]
        if m not in mats:
            mats[m] = {"text": MODULE_GUIDE.get(m, "Learn the core ideas of this module, then practice with the challenges below."), "code": l.get("hint", "")}
    tr["materials"] = mats

# ---- append web / markup / devops tracks ----
import webbank
for wid in webbank.WEB_ORDER:
    tracks.append(webbank.build_web_track(wid))

# ---- override the markup tracks (created above) with the bigger morebank banks ----
for lid in morebank.MARKUP:
    tr = next((t for t in tracks if t["id"] == lid), None)
    if tr:
        tr["lessons"] = morebank.build(lid)
        tr["engine"] = morebank.ENGINE[lid]

# ---- attach a zero-to-advanced learning guide to every track ----
import guides
for tr in tracks:
    tr["guide"] = guides.build_guide(tr)

js = "/* Ironyx curriculum (auto-generated). Edit generate_curriculum.py and re-run. */\n"
js += "window.CURRICULUM = " + json.dumps(tracks, indent=2, ensure_ascii=False) + ";\n"
open("/home/user/work/codequest/public/data/curriculum.js", "w").write(js)
print("languages:", len(tracks))
print("total lessons:", sum(len(t["lessons"]) for t in tracks))
for t in tracks:
    print(f"  {t['icon']} {t['name']:12} {len(t['lessons'])} lessons  [{t['engine']}]")
