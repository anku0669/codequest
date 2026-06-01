# -*- coding: utf-8 -*-
"""DSA Challenges: 50+ LeetCode-style problems per rich language.
Algorithms are parameterized (multiple input sets); expected outputs computed in Python."""
import math
from bigbank import RICH, starter, fizz_expected, k_fizz, wrap

def w_php(b): return "<?php\n" + b
def w_java(b): return "public class Main {\n  public static void main(String[] args) {\n" + b + "\n  }\n}\n"
def w_cs(b): return "using System;\nusing System.Linq;\nclass Program {\n  static void Main() {\n" + b + "\n  }\n}\n"
def w_cpp(b, hdr=("iostream", "string", "vector", "algorithm", "numeric")): return "".join("#include <" + h + ">\n" for h in hdr) + "using namespace std;\nint main() {\n" + b + "\nreturn 0;\n}\n"
def w_go(b, imports=("fmt",)):
    imp = 'import "' + imports[0] + '"\n' if len(imports) == 1 else "import (\n" + "".join('  "' + i + '"\n' for i in imports) + ")\n"
    return "package main\n" + imp + "func main() {\n" + b + "\n}\n"
def w_rs(b): return "fn main() {\n" + b + "\n}\n"
def carr(a): return ", ".join(map(str, a))

# ---------- parameterized emitters: each returns {lang: source} ----------
def E_reverse(s):
    return {
        "python": 's = "%s"\nprint(s[::-1])' % s,
        "javascript": 'console.log("%s".split("").reverse().join(""));' % s,
        "typescript": 'console.log("%s".split("").reverse().join(""));' % s,
        "ruby": 'puts "%s".reverse' % s,
        "php": w_php('echo strrev("%s") . "\\n";' % s),
        "java": w_java('System.out.println(new StringBuilder("%s").reverse().toString());' % s),
        "csharp": w_cs('char[] a = "%s".ToCharArray(); Array.Reverse(a); Console.WriteLine(new string(a));' % s),
        "cpp": w_cpp('string s = "%s"; reverse(s.begin(), s.end()); cout << s << endl;' % s),
        "go": w_go('r := []rune("%s")\nfor i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 { r[i], r[j] = r[j], r[i] }\nfmt.Println(string(r))' % s),
        "rust": w_rs('let r: String = "%s".chars().rev().collect(); println!("{}", r);' % s),
    }
def E_palindrome(s):
    return {
        "python": 's = "%s"\nprint("yes" if s == s[::-1] else "no")' % s,
        "javascript": 'const s = "%s"; console.log(s === s.split("").reverse().join("") ? "yes" : "no");' % s,
        "typescript": 'const s = "%s"; console.log(s === s.split("").reverse().join("") ? "yes" : "no");' % s,
        "ruby": 's = "%s"; puts(s == s.reverse ? "yes" : "no")' % s,
        "php": w_php('$s = "%s"; echo ($s === strrev($s) ? "yes" : "no") . "\\n";' % s),
        "java": w_java('String s = "%s"; System.out.println(s.equals(new StringBuilder(s).reverse().toString()) ? "yes" : "no");' % s),
        "csharp": w_cs('string s = "%s"; char[] a = s.ToCharArray(); Array.Reverse(a); Console.WriteLine(s == new string(a) ? "yes" : "no");' % s),
        "cpp": w_cpp('string s = "%s"; string r = s; reverse(r.begin(), r.end()); cout << (s == r ? "yes" : "no") << endl;' % s),
        "go": w_go('s := "%s"\nr := []rune(s)\nfor i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 { r[i], r[j] = r[j], r[i] }\nif string(r) == s { fmt.Println("yes") } else { fmt.Println("no") }' % s),
        "rust": w_rs('let s = "%s"; let r: String = s.chars().rev().collect(); println!("{}", if s == r { "yes" } else { "no" });' % s),
    }
def E_factorial(n):
    return {
        "python": "f = 1\nfor i in range(1, %d): f *= i\nprint(f)" % (n + 1),
        "javascript": "let f = 1; for (let i = 1; i <= %d; i++) f *= i; console.log(f);" % n,
        "typescript": "let f = 1; for (let i = 1; i <= %d; i++) f *= i; console.log(f);" % n,
        "ruby": "f = 1; (1..%d).each { |i| f *= i }; puts f" % n,
        "php": w_php("$f = 1; for ($i = 1; $i <= %d; $i++) $f *= $i; echo $f . \"\\n\";" % n),
        "java": w_java("long f = 1; for (int i = 1; i <= %d; i++) f *= i; System.out.println(f);" % n),
        "csharp": w_cs("long f = 1; for (int i = 1; i <= %d; i++) f *= i; Console.WriteLine(f);" % n),
        "cpp": w_cpp("long long f = 1; for (int i = 1; i <= %d; i++) f *= i; cout << f << endl;" % n),
        "go": w_go("f := 1\nfor i := 1; i <= %d; i++ { f *= i }\nfmt.Println(f)" % n),
        "rust": w_rs("let mut f: i64 = 1; for i in 1..=%d { f *= i as i64; } println!(\"{}\", f);" % n),
    }
def E_fib(n):
    return {
        "python": "a, b = 0, 1\nfor _ in range(%d): a, b = b, a + b\nprint(a)" % n,
        "javascript": "let a = 0, b = 1; for (let i = 0; i < %d; i++) { [a, b] = [b, a + b]; } console.log(a);" % n,
        "typescript": "let a = 0, b = 1; for (let i = 0; i < %d; i++) { [a, b] = [b, a + b]; } console.log(a);" % n,
        "ruby": "a, b = 0, 1; %d.times { a, b = b, a + b }; puts a" % n,
        "php": w_php("$a = 0; $b = 1; for ($i = 0; $i < %d; $i++) { $t = $a + $b; $a = $b; $b = $t; } echo $a . \"\\n\";" % n),
        "java": w_java("long a = 0, b = 1; for (int i = 0; i < %d; i++) { long t = a + b; a = b; b = t; } System.out.println(a);" % n),
        "csharp": w_cs("long a = 0, b = 1; for (int i = 0; i < %d; i++) { long t = a + b; a = b; b = t; } Console.WriteLine(a);" % n),
        "cpp": w_cpp("long long a = 0, b = 1; for (int i = 0; i < %d; i++) { long long t = a + b; a = b; b = t; } cout << a << endl;" % n),
        "go": w_go("a, b := 0, 1\nfor i := 0; i < %d; i++ { a, b = b, a+b }\nfmt.Println(a)" % n),
        "rust": w_rs("let (mut a, mut b): (i64, i64) = (0, 1); for _ in 0..%d { let t = a + b; a = b; b = t; } println!(\"{}\", a);" % n),
    }
def E_prime(n):
    return {
        "python": "n = %d\np = n > 1\nfor i in range(2, int(n**0.5)+1):\n    if n %% i == 0: p = False\nprint(\"yes\" if p else \"no\")" % n,
        "javascript": "const n = %d; let p = n > 1; for (let i = 2; i*i <= n; i++) if (n %% i === 0) p = false; console.log(p ? \"yes\" : \"no\");" % n,
        "typescript": "const n = %d; let p = n > 1; for (let i = 2; i*i <= n; i++) if (n %% i === 0) p = false; console.log(p ? \"yes\" : \"no\");" % n,
        "ruby": "n = %d; p = n > 1; (2..Math.sqrt(n).to_i).each { |i| p = false if n %% i == 0 }; puts(p ? \"yes\" : \"no\")" % n,
        "php": w_php("$n = %d; $p = $n > 1; for ($i = 2; $i*$i <= $n; $i++) if ($n %% $i == 0) $p = false; echo ($p ? \"yes\" : \"no\") . \"\\n\";" % n),
        "java": w_java("int n = %d; boolean p = n > 1; for (int i = 2; (long)i*i <= n; i++) if (n %% i == 0) p = false; System.out.println(p ? \"yes\" : \"no\");" % n),
        "csharp": w_cs("int n = %d; bool p = n > 1; for (int i = 2; (long)i*i <= n; i++) if (n %% i == 0) p = false; Console.WriteLine(p ? \"yes\" : \"no\");" % n),
        "cpp": w_cpp("int n = %d; bool p = n > 1; for (int i = 2; (long)i*i <= n; i++) if (n %% i == 0) p = false; cout << (p ? \"yes\" : \"no\") << endl;" % n),
        "go": w_go("n := %d\np := n > 1\nfor i := 2; i*i <= n; i++ { if n%%i == 0 { p = false } }\nif p { fmt.Println(\"yes\") } else { fmt.Println(\"no\") }" % n),
        "rust": w_rs("let n = %d; let mut p = n > 1; let mut i = 2; while i*i <= n { if n %% i == 0 { p = false; } i += 1; } println!(\"{}\", if p { \"yes\" } else { \"no\" });" % n),
    }
def E_gcd(a, b):
    return {
        "python": "a, b = %d, %d\nwhile b: a, b = b, a %% b\nprint(a)" % (a, b),
        "javascript": "let a = %d, b = %d; while (b) { [a, b] = [b, a %% b]; } console.log(a);" % (a, b),
        "typescript": "let a = %d, b = %d; while (b) { [a, b] = [b, a %% b]; } console.log(a);" % (a, b),
        "ruby": "a, b = %d, %d; while b != 0 do a, b = b, a %% b end; puts a" % (a, b),
        "php": w_php("$a = %d; $b = %d; while ($b != 0) { $t = $a %% $b; $a = $b; $b = $t; } echo $a . \"\\n\";" % (a, b)),
        "java": w_java("int a = %d, b = %d; while (b != 0) { int t = a %% b; a = b; b = t; } System.out.println(a);" % (a, b)),
        "csharp": w_cs("int a = %d, b = %d; while (b != 0) { int t = a %% b; a = b; b = t; } Console.WriteLine(a);" % (a, b)),
        "cpp": w_cpp("int a = %d, b = %d; while (b != 0) { int t = a %% b; a = b; b = t; } cout << a << endl;" % (a, b)),
        "go": w_go("a, b := %d, %d\nfor b != 0 { a, b = b, a%%b }\nfmt.Println(a)" % (a, b)),
        "rust": w_rs("let (mut a, mut b) = (%d, %d); while b != 0 { let t = a %% b; a = b; b = t; } println!(\"{}\", a);" % (a, b)),
    }
def E_sumdigits(n):
    return {
        "python": "n = %d\ns = 0\nwhile n: s += n %% 10; n //= 10\nprint(s)" % n,
        "javascript": "let n = %d, s = 0; while (n > 0) { s += n %% 10; n = Math.floor(n / 10); } console.log(s);" % n,
        "typescript": "let n = %d, s = 0; while (n > 0) { s += n %% 10; n = Math.floor(n / 10); } console.log(s);" % n,
        "ruby": "n = %d; s = 0; while n > 0 do s += n %% 10; n /= 10 end; puts s" % n,
        "php": w_php("$n = %d; $s = 0; while ($n > 0) { $s += $n %% 10; $n = intdiv($n, 10); } echo $s . \"\\n\";" % n),
        "java": w_java("int n = %d, s = 0; while (n > 0) { s += n %% 10; n /= 10; } System.out.println(s);" % n),
        "csharp": w_cs("int n = %d, s = 0; while (n > 0) { s += n %% 10; n /= 10; } Console.WriteLine(s);" % n),
        "cpp": w_cpp("int n = %d, s = 0; while (n > 0) { s += n %% 10; n /= 10; } cout << s << endl;" % n),
        "go": w_go("n := %d\ns := 0\nfor n > 0 { s += n %% 10; n /= 10 }\nfmt.Println(s)" % n),
        "rust": w_rs("let mut n = %d; let mut s = 0; while n > 0 { s += n %% 10; n /= 10; } println!(\"{}\", s);" % n),
    }
def E_vowels(s):
    return {
        "python": 'print(sum(1 for c in "%s" if c in "aeiou"))' % s,
        "javascript": 'console.log(("%s".match(/[aeiou]/g) || []).length);' % s,
        "typescript": 'console.log(("%s".match(/[aeiou]/g) || []).length);' % s,
        "ruby": 'puts "%s".count("aeiou")' % s,
        "php": w_php('$s = "%s"; $c = 0; for ($i = 0; $i < strlen($s); $i++) if (strpos("aeiou", $s[$i]) !== false) $c++; echo $c . "\\n";' % s),
        "java": w_java('String s = "%s"; int c = 0; for (char ch : s.toCharArray()) if ("aeiou".indexOf(ch) >= 0) c++; System.out.println(c);' % s),
        "csharp": w_cs('string s = "%s"; int c = 0; foreach (char ch in s) if ("aeiou".IndexOf(ch) >= 0) c++; Console.WriteLine(c);' % s),
        "cpp": w_cpp('string s = "%s"; int c = 0; for (char ch : s) if (string("aeiou").find(ch) != string::npos) c++; cout << c << endl;' % s),
        "go": w_go('s := "%s"\nc := 0\nfor _, ch := range s { if strings.ContainsRune("aeiou", ch) { c++ } }\nfmt.Println(c)' % s, imports=("fmt", "strings")),
        "rust": w_rs('let c = "%s".chars().filter(|c| "aeiou".contains(*c)).count(); println!("{}", c);' % s),
    }
def E_twosum(arr, t):
    csv = carr(arr)
    return {
        "python": "nums = [%s]\nt = %d\nfor i in range(len(nums)):\n    for j in range(i+1, len(nums)):\n        if nums[i]+nums[j] == t: print(i, j)" % (csv, t),
        "javascript": "const nums = [%s], t = %d; for (let i = 0; i < nums.length; i++) for (let j = i+1; j < nums.length; j++) if (nums[i]+nums[j] === t) console.log(i + \" \" + j);" % (csv, t),
        "typescript": "const nums = [%s], t = %d; for (let i = 0; i < nums.length; i++) for (let j = i+1; j < nums.length; j++) if (nums[i]+nums[j] === t) console.log(i + \" \" + j);" % (csv, t),
        "ruby": "nums = [%s]; t = %d; nums.each_index { |i| (i+1...nums.length).each { |j| puts \"#{i} #{j}\" if nums[i]+nums[j] == t } }" % (csv, t),
        "php": w_php("$nums = [%s]; $t = %d; for ($i=0;$i<count($nums);$i++) for ($j=$i+1;$j<count($nums);$j++) if ($nums[$i]+$nums[$j]==$t) echo \"$i $j\\n\";" % (csv, t)),
        "java": w_java("int[] nums = {%s}; int t = %d; for (int i=0;i<nums.length;i++) for (int j=i+1;j<nums.length;j++) if (nums[i]+nums[j]==t) System.out.println(i+\" \"+j);" % (csv, t)),
        "csharp": w_cs("int[] nums = {%s}; int t = %d; for (int i=0;i<nums.Length;i++) for (int j=i+1;j<nums.Length;j++) if (nums[i]+nums[j]==t) Console.WriteLine(i+\" \"+j);" % (csv, t)),
        "cpp": w_cpp("vector<int> nums = {%s}; int t = %d; for (int i=0;i<(int)nums.size();i++) for (int j=i+1;j<(int)nums.size();j++) if (nums[i]+nums[j]==t) cout << i << \" \" << j << endl;" % (csv, t)),
        "go": w_go("nums := []int{%s}\nt := %d\nfor i := 0; i < len(nums); i++ { for j := i+1; j < len(nums); j++ { if nums[i]+nums[j] == t { fmt.Println(i, j) } } }" % (csv, t)),
        "rust": w_rs("let nums = [%s]; let t = %d; for i in 0..nums.len() { for j in i+1..nums.len() { if nums[i]+nums[j] == t { println!(\"{} {}\", i, j); } } }" % (csv, t)),
    }
def E_arrstat(arr, kind):  # kind: max/min/sum/avg/counteven/product
    csv = carr(arr)
    if kind == "max":
        return {"python": "print(max([%s]))" % csv, "javascript": "console.log(Math.max(...[%s]));" % csv, "typescript": "console.log(Math.max(...[%s]));" % csv,
            "ruby": "puts [%s].max" % csv, "php": w_php("echo max([%s]) . \"\\n\";" % csv),
            "java": w_java("int[] a = {%s}; int m = a[0]; for (int x : a) if (x > m) m = x; System.out.println(m);" % csv),
            "csharp": w_cs("int[] a = {%s}; Console.WriteLine(a.Max());" % csv),
            "go": w_go("a := []int{%s}\nm := a[0]\nfor _, x := range a { if x > m { m = x } }\nfmt.Println(m)" % csv),
            "cpp": w_cpp("vector<int> a = {%s}; cout << *max_element(a.begin(), a.end()) << endl;" % csv),
            "rust": w_rs("let a = [%s]; println!(\"{}\", a.iter().max().unwrap());" % csv)}
    if kind == "min":
        return {"python": "print(min([%s]))" % csv, "javascript": "console.log(Math.min(...[%s]));" % csv, "typescript": "console.log(Math.min(...[%s]));" % csv,
            "ruby": "puts [%s].min" % csv, "php": w_php("echo min([%s]) . \"\\n\";" % csv),
            "java": w_java("int[] a = {%s}; int m = a[0]; for (int x : a) if (x < m) m = x; System.out.println(m);" % csv),
            "csharp": w_cs("int[] a = {%s}; Console.WriteLine(a.Min());" % csv),
            "go": w_go("a := []int{%s}\nm := a[0]\nfor _, x := range a { if x < m { m = x } }\nfmt.Println(m)" % csv),
            "cpp": w_cpp("vector<int> a = {%s}; cout << *min_element(a.begin(), a.end()) << endl;" % csv),
            "rust": w_rs("let a = [%s]; println!(\"{}\", a.iter().min().unwrap());" % csv)}
    if kind == "sum":
        return {"python": "print(sum([%s]))" % csv, "javascript": "console.log([%s].reduce((a,b)=>a+b,0));" % csv, "typescript": "console.log([%s].reduce((a,b)=>a+b,0));" % csv,
            "ruby": "puts [%s].sum" % csv, "php": w_php("echo array_sum([%s]) . \"\\n\";" % csv),
            "java": w_java("int[] a = {%s}; int s = 0; for (int x : a) s += x; System.out.println(s);" % csv),
            "csharp": w_cs("int[] a = {%s}; Console.WriteLine(a.Sum());" % csv),
            "go": w_go("a := []int{%s}\ns := 0\nfor _, x := range a { s += x }\nfmt.Println(s)" % csv),
            "cpp": w_cpp("vector<int> a = {%s}; cout << accumulate(a.begin(), a.end(), 0) << endl;" % csv),
            "rust": w_rs("let a = [%s]; let s: i32 = a.iter().sum(); println!(\"{}\", s);" % csv)}
    if kind == "avg":
        return {"python": "a=[%s]\nprint(sum(a)//len(a))" % csv, "javascript": "const a=[%s]; console.log(Math.floor(a.reduce((x,y)=>x+y,0)/a.length));" % csv, "typescript": "const a=[%s]; console.log(Math.floor(a.reduce((x,y)=>x+y,0)/a.length));" % csv,
            "ruby": "a=[%s]; puts a.sum/a.length" % csv, "php": w_php("$a=[%s]; echo intdiv(array_sum($a),count($a)) . \"\\n\";" % csv),
            "java": w_java("int[] a = {%s}; int s = 0; for (int x : a) s += x; System.out.println(s / a.length);" % csv),
            "csharp": w_cs("int[] a = {%s}; Console.WriteLine(a.Sum() / a.Length);" % csv),
            "go": w_go("a := []int{%s}\ns := 0\nfor _, x := range a { s += x }\nfmt.Println(s / len(a))" % csv),
            "cpp": w_cpp("vector<int> a = {%s}; int s = accumulate(a.begin(), a.end(), 0); cout << s / (int)a.size() << endl;" % csv),
            "rust": w_rs("let a = [%s]; let s: i32 = a.iter().sum(); println!(\"{}\", s / a.len() as i32);" % csv)}
    if kind == "counteven":
        return {"python": "print(sum(1 for x in [%s] if x%%2==0))" % csv, "javascript": "console.log([%s].filter(x=>x%%2===0).length);" % csv, "typescript": "console.log([%s].filter(x=>x%%2===0).length);" % csv,
            "ruby": "puts [%s].count(&:even?)" % csv, "php": w_php("$c=0; foreach ([%s] as $x) if ($x%%2==0) $c++; echo $c . \"\\n\";" % csv),
            "java": w_java("int[] a = {%s}; int c = 0; for (int x : a) if (x %% 2 == 0) c++; System.out.println(c);" % csv),
            "csharp": w_cs("int[] a = {%s}; Console.WriteLine(a.Count(x => x %% 2 == 0));" % csv),
            "go": w_go("a := []int{%s}\nc := 0\nfor _, x := range a { if x%%2 == 0 { c++ } }\nfmt.Println(c)" % csv),
            "cpp": w_cpp("vector<int> a = {%s}; int c = 0; for (int x : a) if (x %% 2 == 0) c++; cout << c << endl;" % csv),
            "rust": w_rs("let a = [%s]; println!(\"{}\", a.iter().filter(|x| *x %% 2 == 0).count());" % csv)}
def E_linsearch(arr, t):
    csv = carr(arr)
    return {
        "python": "nums = [%s]\nt = %d\nfor i, x in enumerate(nums):\n    if x == t: print(i); break" % (csv, t),
        "javascript": "const nums = [%s], t = %d; for (let i = 0; i < nums.length; i++) if (nums[i] === t) { console.log(i); break; }" % (csv, t),
        "typescript": "const nums = [%s], t = %d; for (let i = 0; i < nums.length; i++) if (nums[i] === t) { console.log(i); break; }" % (csv, t),
        "ruby": "puts [%s].index(%d)" % (csv, t),
        "php": w_php("$nums = [%s]; $t = %d; for ($i=0;$i<count($nums);$i++) if ($nums[$i]==$t) { echo $i . \"\\n\"; break; }" % (csv, t)),
        "java": w_java("int[] nums = {%s}; int t = %d; for (int i=0;i<nums.length;i++) if (nums[i]==t) { System.out.println(i); break; }" % (csv, t)),
        "csharp": w_cs("int[] nums = {%s}; int t = %d; for (int i=0;i<nums.Length;i++) if (nums[i]==t) { Console.WriteLine(i); break; }" % (csv, t)),
        "cpp": w_cpp("vector<int> nums = {%s}; int t = %d; for (int i=0;i<(int)nums.size();i++) if (nums[i]==t) { cout << i << endl; break; }" % (csv, t)),
        "go": w_go("nums := []int{%s}\nt := %d\nfor i, x := range nums { if x == t { fmt.Println(i); break } }" % (csv, t)),
        "rust": w_rs("let nums = [%s]; let t = %d; for i in 0..nums.len() { if nums[i] == t { println!(\"{}\", i); break; } }" % (csv, t)),
    }
def E_sortarr(arr):
    csv = carr(arr)
    return {
        "python": "a = [%s]\na.sort()\nprint(' '.join(map(str, a)))" % csv,
        "javascript": "const a = [%s]; a.sort((x,y)=>x-y); console.log(a.join(' '));" % csv,
        "typescript": "const a = [%s]; a.sort((x,y)=>x-y); console.log(a.join(' '));" % csv,
        "ruby": "puts [%s].sort.join(' ')" % csv,
        "php": w_php("$a=[%s]; sort($a); echo implode(' ', $a) . \"\\n\";" % csv),
        "java": w_java("int[] a = {%s}; java.util.Arrays.sort(a); StringBuilder sb = new StringBuilder(); for (int i=0;i<a.length;i++){ if(i>0) sb.append(' '); sb.append(a[i]); } System.out.println(sb.toString());" % csv),
        "csharp": w_cs("int[] a = {%s}; Array.Sort(a); Console.WriteLine(string.Join(\" \", a));" % csv),
        "cpp": w_cpp("vector<int> a = {%s}; sort(a.begin(), a.end()); for (int i=0;i<(int)a.size();i++){ if(i) cout << \" \"; cout << a[i]; } cout << endl;" % csv),
        "go": w_go("a := []int{%s}\nsort.Ints(a)\nfmt.Println(strings.Trim(fmt.Sprint(a), \"[]\"))" % csv, imports=("fmt", "sort", "strings")),
        "rust": w_rs("let mut a = vec![%s]; a.sort(); let s: Vec<String> = a.iter().map(|x| x.to_string()).collect(); println!(\"{}\", s.join(\" \"));" % csv),
    }
def E_secondlargest(arr):
    csv = carr(arr)
    return {
        "python": "print(sorted([%s])[-2])" % csv,
        "javascript": "const a = [%s]; a.sort((x,y)=>x-y); console.log(a[a.length-2]);" % csv,
        "typescript": "const a = [%s]; a.sort((x,y)=>x-y); console.log(a[a.length-2]);" % csv,
        "ruby": "puts [%s].sort[-2]" % csv,
        "php": w_php("$a=[%s]; sort($a); echo $a[count($a)-2] . \"\\n\";" % csv),
        "java": w_java("int[] a = {%s}; java.util.Arrays.sort(a); System.out.println(a[a.length-2]);" % csv),
        "csharp": w_cs("int[] a = {%s}; Array.Sort(a); Console.WriteLine(a[a.Length-2]);" % csv),
        "cpp": w_cpp("vector<int> a = {%s}; sort(a.begin(), a.end()); cout << a[a.size()-2] << endl;" % csv),
        "go": w_go("a := []int{%s}\nsort.Ints(a)\nfmt.Println(a[len(a)-2])" % csv, imports=("fmt", "sort")),
        "rust": w_rs("let mut a = vec![%s]; a.sort(); println!(\"{}\", a[a.len()-2]);" % csv),
    }
def E_power(b, e):
    return {
        "python": "print(%d ** %d)" % (b, e), "javascript": "console.log(Math.pow(%d, %d));" % (b, e), "typescript": "console.log(Math.pow(%d, %d));" % (b, e),
        "ruby": "puts %d ** %d" % (b, e), "php": w_php("echo pow(%d, %d) . \"\\n\";" % (b, e)),
        "java": w_java("long r = 1; for (int i = 0; i < %d; i++) r *= %d; System.out.println(r);" % (e, b)),
        "csharp": w_cs("long r = 1; for (int i = 0; i < %d; i++) r *= %d; Console.WriteLine(r);" % (e, b)),
        "cpp": w_cpp("long long r = 1; for (int i = 0; i < %d; i++) r *= %d; cout << r << endl;" % (e, b)),
        "go": w_go("r := 1\nfor i := 0; i < %d; i++ { r *= %d }\nfmt.Println(r)" % (e, b)),
        "rust": w_rs("let mut r: i64 = 1; for _ in 0..%d { r *= %d; } println!(\"{}\", r);" % (e, b)),
    }
def E_revarr(arr):
    csv = carr(arr)
    return {
        "python": "print(' '.join(map(str, [%s][::-1])))" % csv,
        "javascript": "console.log([%s].reverse().join(' '));" % csv,
        "typescript": "console.log([%s].reverse().join(' '));" % csv,
        "ruby": "puts [%s].reverse.join(' ')" % csv,
        "php": w_php("echo implode(' ', array_reverse([%s])) . \"\\n\";" % csv),
        "java": w_java("int[] a = {%s}; StringBuilder sb = new StringBuilder(); for (int i=a.length-1;i>=0;i--){ if(i<a.length-1) sb.append(' '); sb.append(a[i]); } System.out.println(sb.toString());" % csv),
        "csharp": w_cs("int[] a = {%s}; Array.Reverse(a); Console.WriteLine(string.Join(\" \", a));" % csv),
        "cpp": w_cpp("vector<int> a = {%s}; reverse(a.begin(), a.end()); for (int i=0;i<(int)a.size();i++){ if(i) cout << \" \"; cout << a[i]; } cout << endl;" % csv),
        "go": w_go("a := []int{%s}\nfor i, j := 0, len(a)-1; i < j; i, j = i+1, j-1 { a[i], a[j] = a[j], a[i] }\nfmt.Println(strings.Trim(fmt.Sprint(a), \"[]\"))" % csv, imports=("fmt", "strings")),
        "rust": w_rs("let mut a = vec![%s]; a.reverse(); let s: Vec<String> = a.iter().map(|x| x.to_string()).collect(); println!(\"{}\", s.join(\" \"));" % csv),
    }
def E_fizz(n):
    return {l: wrap(l, k_fizz(l, n)) for l in RICH}

# ---------- expected helpers ----------
def exp_first_pair(arr, t):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i]+arr[j] == t: return f"{i} {j}"
    return ""

# ---------- problem catalogue (parameterized → 50+) ----------
def _b(expected): return "Make your program print exactly: `" + expected.replace("\n", "` then `") + "`"
PROBLEMS = []
def add(title, diff, xp, expl, emit, expected):
    PROBLEMS.append((title, diff, xp, _b(expected), expl, emit, expected))

EX = {
 "reverse": "Reverse a string: split into characters, reverse, re-join. Example: `code` → `edoc`.",
 "palindrome": "A palindrome equals its reverse. Compare the string to its reversed copy.",
 "factorial": "`n! = 1*2*...*n`. Multiply into an accumulator in a loop. Example: `5! = 120`.",
 "fib": "Each Fibonacci number is the sum of the previous two; roll two variables forward n times.",
 "prime": "A prime has no divisors except 1 and itself; test divisors up to √n.",
 "gcd": "Euclid's algorithm: replace (a, b) with (b, a mod b) until b is 0.",
 "sumdigits": "Take the last digit with `% 10`, drop it with `/ 10`, repeat. Example: 123 → 6.",
 "vowels": "Scan each character, count if it's a vowel (a,e,i,o,u).",
 "twosum": "Check every pair (i, j); print the indices whose values add to the target.",
 "arr": "Process an array by scanning it: max/min/sum/average/count with a single pass.",
 "linsearch": "Walk the array; return the first index whose value matches the target.",
 "sort": "Sorting arranges values in order (here ascending).",
 "second": "The second-largest is the element before the last once sorted.",
 "power": "Multiply the base by itself `exp` times. Example: 2^3 = 8.",
 "revarr": "Reverse an array by swapping ends inward, or with a reverse helper.",
 "fizz": "Print Fizz (÷3), Buzz (÷5), FizzBuzz (÷15), else the number. Check ÷15 first.",
}
# reverse (4)
for s in ["algorithm", "hello", "codequest", "kotlin"]:
    add("Reverse '%s'" % s, "Easy", 25, EX["reverse"], E_reverse(s), s[::-1])
# palindrome (4)
for s in ["racecar", "hello", "level", "world"]:
    add("Palindrome? '%s'" % s, "Easy", 25, EX["palindrome"], E_palindrome(s), "yes" if s == s[::-1] else "no")
# factorial (4)
for n in [5, 6, 7, 4]:
    add("Factorial of %d" % n, "Easy", 26, EX["factorial"], E_factorial(n), str(math.factorial(n)))
# fibonacci (4)
def fibv(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return a
for n in [10, 12, 8, 15]:
    add("%dth Fibonacci" % n, "Medium", 30, EX["fib"], E_fib(n), str(fibv(n)))
# prime (4)
def isp(n):
    if n < 2: return False
    i = 2
    while i*i <= n:
        if n % i == 0: return False
        i += 1
    return True
for n in [29, 12, 97, 100]:
    add("Is %d prime?" % n, "Medium", 30, EX["prime"], E_prime(n), "yes" if isp(n) else "no")
# gcd (4)
for a, b in [(48, 36), (100, 75), (54, 24), (81, 27)]:
    add("GCD(%d, %d)" % (a, b), "Medium", 30, EX["gcd"], E_gcd(a, b), str(math.gcd(a, b)))
# sum digits (4)
for n in [12345, 9999, 1001, 54321]:
    add("Sum digits of %d" % n, "Easy", 25, EX["sumdigits"], E_sumdigits(n), str(sum(int(c) for c in str(n))))
# vowels (4)
for s in ["education", "programming", "rhythm", "queue"]:
    add("Count vowels in '%s'" % s, "Easy", 25, EX["vowels"], E_vowels(s), str(sum(1 for c in s if c in "aeiou")))
# two sum (3)
for arr, t in [([2, 7, 11, 15], 9), ([3, 2, 4], 6), ([5, 1, 9, 3], 8)]:
    add("Two Sum %s → %d" % (arr, t), "Medium", 32, EX["twosum"], E_twosum(arr, t), exp_first_pair(arr, t))
# array stats: max/min/sum/avg/counteven (2 each = 10)
for arr in [[3, 9, 4, 9, 1], [12, 5, 30, 8]]:
    add("Max of %s" % arr, "Easy", 22, EX["arr"], E_arrstat(arr, "max"), str(max(arr)))
for arr in [[3, 9, 4, 1, 7], [20, 14, 8, 35]]:
    add("Min of %s" % arr, "Easy", 22, EX["arr"], E_arrstat(arr, "min"), str(min(arr)))
for arr in [[5, 10, 15, 20], [1, 2, 3, 4, 5, 6]]:
    add("Sum of %s" % arr, "Easy", 22, EX["arr"], E_arrstat(arr, "sum"), str(sum(arr)))
for arr in [[10, 20, 30, 40], [4, 8, 12, 16]]:
    add("Average of %s" % arr, "Medium", 26, EX["arr"], E_arrstat(arr, "avg"), str(sum(arr) // len(arr)))
for arr in [[1, 2, 3, 4, 5, 6], [10, 7, 4, 3, 2]]:
    add("Count evens in %s" % arr, "Easy", 24, EX["arr"], E_arrstat(arr, "counteven"), str(sum(1 for x in arr if x % 2 == 0)))
# linear search (2)
for arr, t in [([4, 8, 15, 16, 23], 16), ([9, 3, 7, 1, 5], 7)]:
    add("Find %d in %s" % (t, arr), "Medium", 28, EX["linsearch"], E_linsearch(arr, t), str(arr.index(t)))
# sort (2)
for arr in [[5, 2, 9, 1, 7], [8, 3, 6, 2, 9, 1]]:
    add("Sort %s" % arr, "Medium", 30, EX["sort"], E_sortarr(arr), " ".join(map(str, sorted(arr))))
# second largest (2)
for arr in [[10, 5, 8, 20, 15], [3, 7, 1, 9, 4]]:
    add("2nd largest of %s" % arr, "Medium", 30, EX["second"], E_secondlargest(arr), str(sorted(arr)[-2]))
# power (2)
for b, e in [(2, 10), (3, 5)]:
    add("%d to the power %d" % (b, e), "Medium", 28, EX["power"], E_power(b, e), str(b ** e))
# reverse array (2)
for arr in [[1, 2, 3, 4, 5], [9, 8, 7, 6]]:
    add("Reverse %s" % arr, "Easy", 24, EX["revarr"], E_revarr(arr), " ".join(map(str, arr[::-1])))
# fizzbuzz (2)
for n in [15, 20]:
    add("FizzBuzz to %d" % n, "Hard", 35, EX["fizz"], E_fizz(n), fizz_expected(n))

def build_dsa(lid):
    out = []
    for i, (title, diff, xp, brief, expl, emit, expected) in enumerate(PROBLEMS, 1):
        if lid not in emit:
            continue
        out.append({"id": lid + "-dsa-" + str(i), "module": "🧩 DSA Challenges", "title": title, "xp": xp,
            "difficulty": diff, "brief": brief, "explanation": expl, "hint": emit[lid], "starter": starter(lid), "expectedOutput": expected})
    return out

if __name__ == "__main__":
    print("DSA problems per language:", len(PROBLEMS))
