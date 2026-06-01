# -*- coding: utf-8 -*-
"""Big question bank: ~20 questions per module for each rich language (~200/module).
Every expected output is computed in Python so grading is exact."""
import math, json

RICH = ["python", "javascript", "typescript", "java", "cpp", "csharp", "go", "rust", "ruby", "php", "lua", "r"]

def slit(lang, s): return '"' + s + '"'
def pr(lang, e):
    return {
        "python": "print(" + e + ")", "ruby": "puts " + e,
        "javascript": "console.log(" + e + ");", "typescript": "console.log(" + e + ");",
        "java": "System.out.println(" + e + ");", "csharp": "Console.WriteLine(" + e + ");",
        "go": "fmt.Println(" + e + ")", "rust": 'println!("{}", ' + e + ");",
        "cpp": "cout << " + e + " << endl;", "php": "echo (" + e + ') . "\\n";',
        "lua": "print(" + e + ")", "r": "cat(" + e + ', "\\n", sep="")',
    }[lang]
def cat(lang, a, b):
    if lang == "cpp": return "string(" + a + ") + " + b
    if lang == "rust": return 'format!("{}{}", ' + a + ", " + b + ")"
    if lang == "php": return a + " . " + b
    if lang == "lua": return a + " .. " + b
    if lang == "r": return "paste0(" + a + ", " + b + ")"
    return a + " + " + b
def lenof(lang, e):
    return {"python": "len(" + e + ")", "javascript": e + ".length", "typescript": e + ".length",
        "java": e + ".length()", "csharp": e + ".Length", "go": "len(" + e + ")",
        "cpp": "string(" + e + ").size()", "rust": e + ".len()", "ruby": e + ".length", "php": "strlen(" + e + ")",
        "lua": "#" + e, "r": "nchar(" + e + ")"}[lang]
def wrap(lang, body):
    if lang in ("python", "ruby", "javascript", "typescript", "lua", "r"): return body
    if lang == "php": return "<?php\n" + body
    if lang == "java": return "public class Main {\n  public static void main(String[] args) {\n" + body + "\n  }\n}\n"
    if lang == "cpp": return ("#include <iostream>\n#include <string>\n#include <vector>\n#include <algorithm>\n#include <numeric>\nusing namespace std;\nint main() {\n" + body + "\nreturn 0;\n}\n")
    if lang == "csharp": return "using System;\nusing System.Linq;\nclass Program {\n  static void Main() {\n" + body + "\n  }\n}\n"
    if lang == "go": return 'package main\nimport "fmt"\nfunc main() {\n' + body + "\n}\n"
    if lang == "rust": return "fn main() {\n" + body + "\n}\n"
    return body
COMMENT = {}
for _l in RICH:
    COMMENT[_l] = "-- Write your code here" if _l == "lua" else ("# Write your code here" if _l in ("python", "ruby", "r", "php") else "// Write your code here")
def starter(lang): return wrap(lang, COMMENT[lang])
N = str

def k_vint(lang, n):
    if lang == "python": return "x = " + N(n) + "\nprint(x)"
    if lang == "ruby": return "x = " + N(n) + "\nputs x"
    if lang in ("javascript", "typescript"): return "let x = " + N(n) + ";\nconsole.log(x);"
    if lang == "java": return "int x = " + N(n) + ";\nSystem.out.println(x);"
    if lang == "csharp": return "int x = " + N(n) + ";\nConsole.WriteLine(x);"
    if lang == "go": return "x := " + N(n) + "\nfmt.Println(x)"
    if lang == "rust": return "let x = " + N(n) + ";\nprintln!(\"{}\", x);"
    if lang == "cpp": return "int x = " + N(n) + ";\ncout << x << endl;"
    if lang == "php": return "$x = " + N(n) + ";\necho $x . \"\\n\";"
    if lang == "lua": return "local x = " + N(n) + "\nprint(x)"
    if lang == "r": return "x <- " + N(n) + '\ncat(x, "\\n", sep="")'
def k_vstr(lang, s):
    q = '"' + s + '"'
    if lang == "python": return "x = " + q + "\nprint(x)"
    if lang == "ruby": return "x = " + q + "\nputs x"
    if lang in ("javascript", "typescript"): return "let x = " + q + ";\nconsole.log(x);"
    if lang == "java": return "String x = " + q + ";\nSystem.out.println(x);"
    if lang == "csharp": return "string x = " + q + ";\nConsole.WriteLine(x);"
    if lang == "go": return "x := " + q + "\nfmt.Println(x)"
    if lang == "rust": return "let x = " + q + ";\nprintln!(\"{}\", x);"
    if lang == "cpp": return "string x = " + q + ";\ncout << x << endl;"
    if lang == "php": return "$x = " + q + ";\necho $x . \"\\n\";"
    if lang == "lua": return "local x = " + q + "\nprint(x)"
    if lang == "r": return "x <- " + q + '\ncat(x, "\\n", sep="")'
def k_cmp(lang, a, op, b):
    cond = N(a) + " " + op + " " + N(b)
    if lang == "python": return 'print("yes" if ' + cond + ' else "no")'
    if lang == "ruby": return 'puts(' + cond + ' ? "yes" : "no")'
    if lang in ("javascript", "typescript"): return 'console.log(' + cond + ' ? "yes" : "no");'
    if lang == "java": return 'System.out.println(' + cond + ' ? "yes" : "no");'
    if lang == "csharp": return 'Console.WriteLine(' + cond + ' ? "yes" : "no");'
    if lang == "go": return 'if ' + cond + ' { fmt.Println("yes") } else { fmt.Println("no") }'
    if lang == "rust": return 'println!("{}", if ' + cond + ' { "yes" } else { "no" });'
    if lang == "cpp": return 'cout << (' + cond + ' ? "yes" : "no") << endl;'
    if lang == "php": return 'echo (' + cond + ' ? "yes" : "no") . "\\n";'
    if lang == "lua": return 'if ' + N(a) + " " + op.replace("!=", "~=") + " " + N(b) + ' then print("yes") else print("no") end'
    if lang == "r": return 'cat(if (' + cond + ') "yes" else "no", "\\n", sep="")'
def k_oddeven(lang, n):
    if lang == "python": return "n = " + N(n) + '\nprint("odd" if n % 2 else "even")'
    if lang == "ruby": return "n = " + N(n) + '\nputs(n.odd? ? "odd" : "even")'
    if lang in ("javascript", "typescript"): return "const n = " + N(n) + ';\nconsole.log(n % 2 ? "odd" : "even");'
    if lang == "java": return "int n = " + N(n) + ';\nSystem.out.println(n % 2 != 0 ? "odd" : "even");'
    if lang == "csharp": return "int n = " + N(n) + ';\nConsole.WriteLine(n % 2 != 0 ? "odd" : "even");'
    if lang == "go": return "n := " + N(n) + '\nif n%2 != 0 { fmt.Println("odd") } else { fmt.Println("even") }'
    if lang == "rust": return "let n = " + N(n) + ';\nprintln!("{}", if n % 2 != 0 { "odd" } else { "even" });'
    if lang == "cpp": return "int n = " + N(n) + ';\ncout << (n % 2 != 0 ? "odd" : "even") << endl;'
    if lang == "php": return "$n = " + N(n) + ';\necho ($n % 2 != 0 ? "odd" : "even") . "\\n";'
    if lang == "lua": return "local n = " + N(n) + '\nif n % 2 ~= 0 then print("odd") else print("even") end'
    if lang == "r": return "n <- " + N(n) + '\ncat(if (n %% 2 != 0) "odd" else "even", "\\n", sep="")'
def k_count(lang, n):
    if lang == "python": return "for i in range(1, " + N(n + 1) + "):\n    print(i)"
    if lang == "ruby": return "(1.." + N(n) + ").each { |i| puts i }"
    if lang in ("javascript", "typescript"): return "for (let i = 1; i <= " + N(n) + "; i++) console.log(i);"
    if lang == "java": return "for (int i = 1; i <= " + N(n) + "; i++) System.out.println(i);"
    if lang == "csharp": return "for (int i = 1; i <= " + N(n) + "; i++) Console.WriteLine(i);"
    if lang == "go": return "for i := 1; i <= " + N(n) + "; i++ { fmt.Println(i) }"
    if lang == "rust": return "for i in 1..=" + N(n) + ' { println!("{}", i); }'
    if lang == "cpp": return "for (int i = 1; i <= " + N(n) + "; i++) cout << i << endl;"
    if lang == "php": return "for ($i = 1; $i <= " + N(n) + '; $i++) echo $i . "\\n";'
    if lang == "lua": return "for i = 1, " + N(n) + " do print(i) end"
    if lang == "r": return "for (i in 1:" + N(n) + ') cat(i, "\\n", sep="")'
def k_sumto(lang, n):
    if lang == "python": return "total = 0\nfor i in range(1, " + N(n + 1) + "):\n    total += i\nprint(total)"
    if lang == "ruby": return "total = 0\n(1.." + N(n) + ").each { |i| total += i }\nputs total"
    if lang in ("javascript", "typescript"): return "let total = 0;\nfor (let i = 1; i <= " + N(n) + "; i++) total += i;\nconsole.log(total);"
    if lang == "java": return "long total = 0;\nfor (int i = 1; i <= " + N(n) + "; i++) total += i;\nSystem.out.println(total);"
    if lang == "csharp": return "long total = 0;\nfor (int i = 1; i <= " + N(n) + "; i++) total += i;\nConsole.WriteLine(total);"
    if lang == "go": return "total := 0\nfor i := 1; i <= " + N(n) + "; i++ { total += i }\nfmt.Println(total)"
    if lang == "rust": return "let mut total: i64 = 0;\nfor i in 1..=" + N(n) + ' { total += i as i64; }\nprintln!("{}", total);'
    if lang == "cpp": return "long long total = 0;\nfor (int i = 1; i <= " + N(n) + "; i++) total += i;\ncout << total << endl;"
    if lang == "php": return "$total = 0;\nfor ($i = 1; $i <= " + N(n) + '; $i++) $total += $i;\necho $total . "\\n";'
    if lang == "lua": return "local total = 0\nfor i = 1, " + N(n) + " do total = total + i end\nprint(total)"
    if lang == "r": return "total <- 0\nfor (i in 1:" + N(n) + ") total <- total + i\n" + 'cat(total, "\\n", sep="")'
def k_fact(lang, n):
    if lang == "lua": return "local f = 1\nfor i = 1, " + N(n) + " do f = f * i end\nprint(f)"
    if lang == "r": return "f <- 1\nfor (i in 1:" + N(n) + ") f <- f * i\n" + 'cat(f, "\\n", sep="")'
    if lang == "python": return "f = 1\nfor i in range(1, " + N(n + 1) + "):\n    f *= i\nprint(f)"
    if lang == "ruby": return "f = 1\n(1.." + N(n) + ").each { |i| f *= i }\nputs f"
    if lang in ("javascript", "typescript"): return "let f = 1;\nfor (let i = 1; i <= " + N(n) + "; i++) f *= i;\nconsole.log(f);"
    if lang == "java": return "long f = 1;\nfor (int i = 1; i <= " + N(n) + "; i++) f *= i;\nSystem.out.println(f);"
    if lang == "csharp": return "long f = 1;\nfor (int i = 1; i <= " + N(n) + "; i++) f *= i;\nConsole.WriteLine(f);"
    if lang == "go": return "f := 1\nfor i := 1; i <= " + N(n) + "; i++ { f *= i }\nfmt.Println(f)"
    if lang == "rust": return "let mut f: i64 = 1;\nfor i in 1..=" + N(n) + ' { f *= i as i64; }\nprintln!("{}", f);'
    if lang == "cpp": return "long long f = 1;\nfor (int i = 1; i <= " + N(n) + "; i++) f *= i;\ncout << f << endl;"
    if lang == "php": return "$f = 1;\nfor ($i = 1; $i <= " + N(n) + '; $i++) $f *= $i;\necho $f . "\\n";'
def k_fizz(lang, n):
    if lang == "lua":
        return ("for i = 1, " + N(n) + " do\n  if i % 15 == 0 then print(\"FizzBuzz\")\n  elseif i % 3 == 0 then print(\"Fizz\")\n  elseif i % 5 == 0 then print(\"Buzz\")\n  else print(i) end\nend")
    if lang == "r":
        return ("for (i in 1:" + N(n) + ") {\n  if (i %% 15 == 0) cat(\"FizzBuzz\\n\")\n  else if (i %% 3 == 0) cat(\"Fizz\\n\")\n  else if (i %% 5 == 0) cat(\"Buzz\\n\")\n  else cat(i, \"\\n\", sep=\"\")\n}")
    if lang == "python":
        return ("for i in range(1, " + N(n + 1) + "):\n    if i % 15 == 0:\n        print(\"FizzBuzz\")\n    elif i % 3 == 0:\n        print(\"Fizz\")\n    elif i % 5 == 0:\n        print(\"Buzz\")\n    else:\n        print(i)")
    if lang == "ruby":
        return ("(1.." + N(n) + ").each do |i|\n  if i % 15 == 0 then puts \"FizzBuzz\"\n  elsif i % 3 == 0 then puts \"Fizz\"\n  elsif i % 5 == 0 then puts \"Buzz\"\n  else puts i end\nend")
    if lang in ("javascript", "typescript"):
        return ("for (let i = 1; i <= " + N(n) + "; i++) {\n  if (i % 15 === 0) console.log(\"FizzBuzz\");\n  else if (i % 3 === 0) console.log(\"Fizz\");\n  else if (i % 5 === 0) console.log(\"Buzz\");\n  else console.log(i);\n}")
    if lang == "java":
        return ("for (int i = 1; i <= " + N(n) + "; i++) {\n  if (i % 15 == 0) System.out.println(\"FizzBuzz\");\n  else if (i % 3 == 0) System.out.println(\"Fizz\");\n  else if (i % 5 == 0) System.out.println(\"Buzz\");\n  else System.out.println(i);\n}")
    if lang == "csharp":
        return ("for (int i = 1; i <= " + N(n) + "; i++) {\n  if (i % 15 == 0) Console.WriteLine(\"FizzBuzz\");\n  else if (i % 3 == 0) Console.WriteLine(\"Fizz\");\n  else if (i % 5 == 0) Console.WriteLine(\"Buzz\");\n  else Console.WriteLine(i);\n}")
    if lang == "go":
        return ("for i := 1; i <= " + N(n) + "; i++ {\n  if i%15 == 0 { fmt.Println(\"FizzBuzz\") } else if i%3 == 0 { fmt.Println(\"Fizz\") } else if i%5 == 0 { fmt.Println(\"Buzz\") } else { fmt.Println(i) }\n}")
    if lang == "rust":
        return ("for i in 1..=" + N(n) + " {\n  if i % 15 == 0 { println!(\"FizzBuzz\"); } else if i % 3 == 0 { println!(\"Fizz\"); } else if i % 5 == 0 { println!(\"Buzz\"); } else { println!(\"{}\", i); }\n}")
    if lang == "cpp":
        return ("for (int i = 1; i <= " + N(n) + "; i++) {\n  if (i % 15 == 0) cout << \"FizzBuzz\" << endl;\n  else if (i % 3 == 0) cout << \"Fizz\" << endl;\n  else if (i % 5 == 0) cout << \"Buzz\" << endl;\n  else cout << i << endl;\n}")
    if lang == "php":
        return ("for ($i = 1; $i <= " + N(n) + "; $i++) {\n  if ($i % 15 == 0) echo \"FizzBuzz\\n\";\n  else if ($i % 3 == 0) echo \"Fizz\\n\";\n  else if ($i % 5 == 0) echo \"Buzz\\n\";\n  else echo $i . \"\\n\";\n}")
def k_listsum(lang, nums):
    csv = ", ".join(map(str, nums))
    if lang == "lua": return "local a = {" + csv + "}\nlocal s = 0\nfor _, x in ipairs(a) do s = s + x end\nprint(s)"
    if lang == "r": return 'cat(sum(c(' + csv + ')), "\\n", sep="")'
    if lang == "python": return "nums = [" + csv + "]\nprint(sum(nums))"
    if lang == "ruby": return "nums = [" + csv + "]\nputs nums.sum"
    if lang in ("javascript", "typescript"): return "const nums = [" + csv + "];\nconsole.log(nums.reduce((a, b) => a + b, 0));"
    if lang == "java": return "int[] nums = {" + csv + "};\nint s = 0;\nfor (int x : nums) s += x;\nSystem.out.println(s);"
    if lang == "csharp": return "int[] nums = {" + csv + "};\nConsole.WriteLine(nums.Sum());"
    if lang == "go": return "nums := []int{" + csv + "}\ns := 0\nfor _, x := range nums { s += x }\nfmt.Println(s)"
    if lang == "rust": return "let nums = [" + csv + "];\nlet s: i32 = nums.iter().sum();\nprintln!(\"{}\", s);"
    if lang == "cpp": return "vector<int> nums = {" + csv + "};\nint s = accumulate(nums.begin(), nums.end(), 0);\ncout << s << endl;"
    if lang == "php": return "$nums = [" + csv + "];\necho array_sum($nums) . \"\\n\";"
def k_listmax(lang, nums):
    csv = ", ".join(map(str, nums))
    if lang == "lua": return "local a = {" + csv + "}\nlocal m = a[1]\nfor _, x in ipairs(a) do if x > m then m = x end end\nprint(m)"
    if lang == "r": return 'cat(max(c(' + csv + ')), "\\n", sep="")'
    if lang == "python": return "nums = [" + csv + "]\nprint(max(nums))"
    if lang == "ruby": return "nums = [" + csv + "]\nputs nums.max"
    if lang in ("javascript", "typescript"): return "const nums = [" + csv + "];\nconsole.log(Math.max(...nums));"
    if lang == "java": return "int[] nums = {" + csv + "};\nint m = nums[0];\nfor (int x : nums) if (x > m) m = x;\nSystem.out.println(m);"
    if lang == "csharp": return "int[] nums = {" + csv + "};\nConsole.WriteLine(nums.Max());"
    if lang == "go": return "nums := []int{" + csv + "}\nm := nums[0]\nfor _, x := range nums { if x > m { m = x } }\nfmt.Println(m)"
    if lang == "rust": return "let nums = [" + csv + "];\nprintln!(\"{}\", nums.iter().max().unwrap());"
    if lang == "cpp": return "vector<int> nums = {" + csv + "};\ncout << *max_element(nums.begin(), nums.end()) << endl;"
    if lang == "php": return "$nums = [" + csv + "];\necho max($nums) . \"\\n\";"
def k_func(lang, name, op, a, b):
    A, B = N(a), N(b)
    if lang == "lua": return "function " + name + "(a, b) return a " + op + " b end\nprint(" + name + "(" + A + ", " + B + "))"
    if lang == "r": return name + " <- function(a, b) a " + op + " b\n" + 'cat(' + name + "(" + A + ", " + B + '), "\\n", sep="")'
    if lang == "python": return "def " + name + "(a, b):\n    return a " + op + " b\nprint(" + name + "(" + A + ", " + B + "))"
    if lang == "ruby": return "def " + name + "(a, b)\n  a " + op + " b\nend\nputs " + name + "(" + A + ", " + B + ")"
    if lang in ("javascript", "typescript"): return "function " + name + "(a, b) { return a " + op + " b; }\nconsole.log(" + name + "(" + A + ", " + B + "));"
    if lang == "java": return ("public class Main {\n  static int " + name + "(int a, int b) { return a " + op + " b; }\n  public static void main(String[] x) { System.out.println(" + name + "(" + A + ", " + B + ")); }\n}\n")
    if lang == "csharp": return ("using System;\nclass Program {\n  static int " + name + "(int a, int b) { return a " + op + " b; }\n  static void Main() { Console.WriteLine(" + name + "(" + A + ", " + B + ")); }\n}\n")
    if lang == "go": return ('package main\nimport "fmt"\nfunc ' + name + "(a, b int) int { return a " + op + " b }\nfunc main() { fmt.Println(" + name + "(" + A + ", " + B + ")) }\n")
    if lang == "rust": return ("fn " + name + "(a: i32, b: i32) -> i32 { a " + op + " b }\nfn main() { println!(\"{}\", " + name + "(" + A + ", " + B + ")); }\n")
    if lang == "cpp": return ("#include <iostream>\nusing namespace std;\nint " + name + "(int a, int b) { return a " + op + " b; }\nint main() { cout << " + name + "(" + A + ", " + B + ") << endl; }\n")
    if lang == "php": return ("<?php\nfunction " + name + "($a, $b) { return $a " + op + " $b; }\necho " + name + "(" + A + ", " + B + ") . \"\\n\";")

EX = {
 "say": "Use your language's print/output function to display text. Wrap the text in quotes (a **string**).\n\nExample: printing `\"Hi there\"` outputs exactly `Hi there`.",
 "vint": "Store a number in a **variable**, then print it. The name lets you reuse the value.\n\nExample: `x = 7` then print `x` → `7`.",
 "vstr": "Store text in a **variable**, then print it.\n\nExample: `name = \"Sam\"` then print `name` → `Sam`.",
 "arith": "**Arithmetic operators**: `+` add, `-` subtract, `*` multiply. The expression is evaluated *before* it's printed.\n\nExample: `6 * 4` → `24`.",
 "cmp": "A **comparison** like `a > b` yields true/false. A conditional then picks the output.\n\nExample: `8 > 2` is true → print `yes`.",
 "oddeven": "`n % 2` is the remainder after dividing by 2: `0` even, `1` odd.\n\nExample: `9 % 2 = 1` → `odd`.",
 "concat": "**Concatenation** joins two strings end-to-end.\n\nExample: `\"foo\" + \"bar\"` → `foobar`.",
 "strlen": "The **length** of a string is how many characters it has.\n\nExample: length of `\"hello\"` is `5`.",
 "count": "A **for-loop** walks a counter through a range.\n\nExample: counting 1..4 prints `1`, `2`, `3`, `4`.",
 "sumto": "Keep a **running total** inside a loop.\n\nExample: `1 + 2 + 3 = 6`. Shortcut: `n*(n+1)/2`.",
 "func": "A **function** takes inputs and returns a result you can reuse.\n\nExample: `add(a, b)` returns `a + b`, so `add(2, 3) = 5`.",
 "listsum": "A **list/array** holds many values. Summing adds them all.\n\nExample: sum of `[1, 2, 3]` = `6`.",
 "listmax": "Finding the **maximum** scans the values, keeping the largest.\n\nExample: max of `[3, 9, 4]` = `9`.",
 "factorial": "**Factorial** `n!` multiplies `1*2*...*n`.\n\nExample: `4! = 24`.",
 "fizzbuzz": "Print `Fizz` for ÷3, `Buzz` for ÷5, `FizzBuzz` for ÷15, else the number. Check `% 15` first.",
}
PHRASES = ["Hello, World!", "I love coding", "Ironyx rocks", "Practice makes perfect", "Keep learning", "Code every day", "Stay curious", "Debugging is fun", "Hello again", "Ship it", "Think in code", "Learn by doing", "Never give up", "One step at a time", "Build cool things", "Quality over speed", "Read the docs", "Test your code", "Small wins count", "You got this"]
VINTS = [42, 7, 100, 256, 1, 99, 2024, 13, 500, 77]
VSTRS = ["Sam", "coder", "Ironyx", "Pluto", "banana", "ninja", "sunrise", "rocket", "hello", "Mars"]
ARITHS = [(7,'*',6),(13,'+',8),(20,'-',5),(9,'*',9),(100,'-',58),(12,'+',30),(8,'*',7),(15,'+',15),(45,'-',3),(11,'*',11),(6,'+',6),(50,'-',8),(3,'*',14),(40,'+',2),(99,'-',9),(12,'*',12),(25,'+',25),(7,'*',8),(60,'-',18),(21,'+',21)]
CMPS = [(5,'>',3),(2,'<',9),(7,'>=',7),(4,'<=',3),(10,'==',10),(8,'!=',8),(15,'>',20),(1,'<',1),(6,'>=',2),(9,'<=',9),(3,'==',4),(5,'!=',6),(100,'>',99),(0,'<',5)]
ODDEVENS = [7, 10, 21, 100, 15, 8]
CONCATS = [("Iron","yx"),("foo","bar"),("Hello","World"),("data","base"),("up","load"),("note","book"),("key","board"),("sun","flower"),("rain","bow"),("home","work"),("fire","fly"),("water","fall")]
STRLENS = ["hello", "Ironyx", "a", "banana", "programming", "sun", "keyboard", "x"]
COUNTS = [3, 4, 5, 6, 7, 8, 9, 10, 2, 12]
SUMTOS = [5, 10, 3, 7, 100, 4, 6, 8, 9, 50]
ADDS = [(20,22),(1,1),(50,50),(7,8),(100,23),(3,4),(15,27),(9,9),(40,2),(11,89)]
MULS = [(6,7),(9,9),(12,12),(3,5),(8,8),(10,10),(7,6),(4,25),(2,21),(11,11)]
LSUMS = [[1,2,3,4],[10,20,30],[5,5,5,5,5],[2,4,6,8,10],[1,1,1],[7,3,9],[100,1],[3,6,9,12],[8,8,8,8],[1,2,3,4,5,6]]
LMAXS = [[3,9,4],[1,2,3],[10,5,8,2],[7,7,7],[100,99,98],[4,15,9],[2,8,6,4],[33,11,22],[5,50,500],[9,1,8,2,7]]
FACTS = [4, 5, 6, 3, 7, 8, 10]
FIZZES = [15, 16, 20, 5, 10, 30, 12]
BIGSUMS = [100, 50, 200, 1000, 25, 500]

def fizz_expected(n):
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0: out.append("FizzBuzz")
        elif i % 3 == 0: out.append("Fizz")
        elif i % 5 == 0: out.append("Buzz")
        else: out.append(str(i))
    return "\n".join(out)

def build_rich(lid):
    lessons = []; n = 0
    def add(module, title, diff, xp, kind, solution, expected):
        nonlocal n; n += 1
        lessons.append({"id": lid + "-" + str(n), "module": module, "title": title, "xp": xp, "difficulty": diff,
            "brief": "Make your program print exactly: `" + expected.replace("\n", "` then `") + "`",
            "explanation": EX[kind], "hint": solution, "starter": starter(lid), "expectedOutput": expected})
    for p in PHRASES: add("Getting Started", "Print: " + p, "Easy", 10, "say", wrap(lid, pr(lid, slit(lid, p))), p)
    for v in VINTS: add("Variables & Types", "Store " + str(v), "Easy", 12, "vint", wrap(lid, k_vint(lid, v)), str(v))
    for s in VSTRS: add("Variables & Types", "Store '" + s + "'", "Easy", 12, "vstr", wrap(lid, k_vstr(lid, s)), s)
    for a, op, b in ARITHS:
        add("Operators & Math", str(a) + " " + op + " " + str(b), "Easy", 12, "arith", wrap(lid, pr(lid, str(a) + " " + op + " " + str(b))), str(eval(str(a) + op + str(b))))
    import operator as _o
    OPS = {">": _o.gt, "<": _o.lt, ">=": _o.ge, "<=": _o.le, "==": _o.eq, "!=": _o.ne}
    for a, op, b in CMPS: add("Conditionals", "Is " + str(a) + " " + op + " " + str(b) + "?", "Medium", 16, "cmp", wrap(lid, k_cmp(lid, a, op, b)), "yes" if OPS[op](a, b) else "no")
    for v in ODDEVENS: add("Conditionals", "Odd or even: " + str(v), "Medium", 16, "oddeven", wrap(lid, k_oddeven(lid, v)), "odd" if v % 2 else "even")
    for x, y in CONCATS: add("Strings", "Join " + x + " + " + y, "Easy", 14, "concat", wrap(lid, pr(lid, cat(lid, slit(lid, x), slit(lid, y)))), x + y)
    for s in STRLENS: add("Strings", "Length of '" + s + "'", "Medium", 16, "strlen", wrap(lid, pr(lid, lenof(lid, slit(lid, s)))), str(len(s)))
    for c in COUNTS: add("Loops", "Count to " + str(c), "Medium", 18, "count", wrap(lid, k_count(lid, c)), "\n".join(str(i) for i in range(1, c + 1)))
    for s in SUMTOS: add("Loops", "Sum 1.." + str(s), "Medium", 20, "sumto", wrap(lid, k_sumto(lid, s)), str(s * (s + 1) // 2))
    for a, b in ADDS: add("Functions", "add(" + str(a) + ", " + str(b) + ")", "Medium", 22, "func", k_func(lid, "add", "+", a, b), str(a + b))
    for a, b in MULS: add("Functions", "mul(" + str(a) + ", " + str(b) + ")", "Medium", 22, "func", k_func(lid, "mul", "*", a, b), str(a * b))
    for nums in LSUMS: add("Collections", "Sum of " + str(nums), "Medium", 22, "listsum", wrap(lid, k_listsum(lid, nums)), str(sum(nums)))
    for nums in LMAXS: add("Collections", "Largest in " + str(nums), "Medium", 22, "listmax", wrap(lid, k_listmax(lid, nums)), str(max(nums)))
    for v in FACTS: add("Projects", "Factorial of " + str(v), "Hard", 30, "factorial", wrap(lid, k_fact(lid, v)), str(math.factorial(v)))
    for v in FIZZES: add("Projects", "FizzBuzz to " + str(v), "Hard", 35, "fizzbuzz", wrap(lid, k_fizz(lid, v)), fizz_expected(v))
    for v in BIGSUMS: add("Projects", "Sum 1.." + str(v) + " (big)", "Hard", 30, "sumto", wrap(lid, k_sumto(lid, v)), str(v * (v + 1) // 2))
    return lessons

if __name__ == "__main__":
    print("per lang:", len(build_rich("python")), "total:", sum(len(build_rich(l)) for l in RICH))
