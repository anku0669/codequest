# -*- coding: utf-8 -*-
"""Web / markup / devops tracks for CodeQuest.
These languages don't produce stdout, so challenges are graded by checking the
user's code CONTAINS the required pieces (expectedAll tokens). HTML & CSS get a
live preview; the rest are validated structurally."""

# id -> (name, lang(monaco), engine, color, icon, blurb)
WEB_META = {
 "html":       ("HTML", "html", "web", "#E34F26", "🌐", "Structure of every web page."),
 "css":        ("CSS", "css", "web", "#1572B6", "🎨", "Style and lay out the web."),
 "scss":       ("SCSS", "scss", "static", "#CC6699", "💅", "CSS with superpowers."),
 "json":       ("JSON", "json", "static", "#5A5A5A", "🧾", "The data format of the web."),
 "yaml":       ("YAML", "yaml", "static", "#CB171E", "📋", "Config files & pipelines."),
 "markdown":   ("Markdown", "markdown", "static", "#000000", "📝", "Write formatted docs."),
 "xml":        ("XML", "xml", "static", "#F1662A", "🗂️", "Structured markup data."),
 "dockerfile": ("Dockerfile", "dockerfile", "static", "#2496ED", "🐳", "Containerize your apps."),
 "graphql":    ("GraphQL", "graphql", "static", "#E10098", "◈", "Query APIs precisely."),
 "regex":      ("Regex", "plaintext", "static", "#6E4AFF", "🔎", "Match text patterns."),
}
WEB_ORDER = list(WEB_META.keys())

def L(lid, n, module, title, diff, xp, brief, explanation, solution, tokens):
    return {"id": lid + "-" + str(n), "module": module, "title": title, "xp": xp, "difficulty": diff,
            "brief": brief, "explanation": explanation, "hint": solution, "starter": "",
            "expectedAll": tokens}

# ---------------- HTML ----------------
def build_html():
    L_ = []; n = 0
    def add(mod, title, diff, xp, brief, expl, sol, toks):
        nonlocal n; n += 1; L_.append(L("html", n, mod, title, diff, xp, brief, expl, sol, toks))
    TEXTS = ["Hello, World!", "About Us", "Welcome", "My Blog", "Contact", "Latest News", "Our Team", "Pricing", "FAQ", "Get Started"]
    # Structure
    add("Document Structure", "Doctype", "Easy", 10, "Add the HTML5 doctype declaration.", "Every HTML5 page starts with `<!DOCTYPE html>` which tells the browser to use modern standards.", "<!DOCTYPE html>", ["<!doctype html>"])
    add("Document Structure", "html tag", "Easy", 10, "Create the root `<html>` element (opening and closing).", "The `<html>` element wraps the entire page.", "<html>\n</html>", ["<html>", "</html>"])
    add("Document Structure", "head tag", "Easy", 10, "Add a `<head>` section.", "The `<head>` holds metadata like the title and links to styles.", "<head>\n</head>", ["<head>", "</head>"])
    add("Document Structure", "body tag", "Easy", 10, "Add a `<body>` section.", "The `<body>` contains everything visible on the page.", "<body>\n</body>", ["<body>", "</body>"])
    for t in TEXTS:
        add("Document Structure", "Title: " + t, "Easy", 10, "Set the page `<title>` to `%s`." % t, "The `<title>` shows in the browser tab.", "<title>%s</title>" % t, ["<title>", t.lower(), "</title>"])
    # Headings & text
    for i, t in enumerate(TEXTS):
        lvl = (i % 6) + 1
        add("Headings & Text", "h%d: %s" % (lvl, t), "Easy", 12, "Create an `<h%d>` heading that says `%s`." % (lvl, t), "Headings `<h1>`–`<h6>` define titles; `<h1>` is the most important.", "<h%d>%s</h%d>" % (lvl, t, lvl), ["<h%d" % lvl, t.lower(), "</h%d>" % lvl])
    for t in ["This is a paragraph.", "Read more below.", "Welcome to my site."]:
        add("Headings & Text", "Paragraph", "Easy", 12, "Write a paragraph that says `%s`." % t, "`<p>` defines a paragraph of text.", "<p>%s</p>" % t, ["<p>", t.lower(), "</p>"])
    add("Headings & Text", "Bold text", "Easy", 12, "Make the word `important` bold using `<strong>`.", "`<strong>` marks text as important (bold).", "<strong>important</strong>", ["<strong>", "important", "</strong>"])
    add("Headings & Text", "Italic text", "Easy", 12, "Emphasize the word `note` using `<em>`.", "`<em>` emphasizes text (italic).", "<em>note</em>", ["<em>", "note", "</em>"])
    add("Headings & Text", "Line break", "Easy", 10, "Add a line break with `<br>`.", "`<br>` inserts a single line break.", "Line one<br>Line two", ["<br"])
    add("Headings & Text", "Horizontal rule", "Easy", 10, "Add a horizontal divider with `<hr>`.", "`<hr>` draws a thematic divider line.", "<hr>", ["<hr"])
    # Links & images
    URLS = ["https://example.com", "https://gumloop.com", "/about", "/contact", "https://github.com"]
    for u in URLS:
        add("Links & Images", "Link to " + u, "Easy", 14, "Create a link to `%s` with the text `Click here`." % u, "`<a href=\"...\">` creates a hyperlink.", '<a href="%s">Click here</a>' % u, ["<a", "href=", u.lower(), "click here", "</a>"])
    for src in ["cat.jpg", "logo.png", "banner.svg", "photo.webp"]:
        add("Links & Images", "Image " + src, "Easy", 14, "Add an image `%s` with alt text `An image`." % src, "`<img>` embeds an image; always include `alt` text for accessibility.", '<img src="%s" alt="An image">' % src, ["<img", "src=", src.lower(), "alt="])
    # Lists
    add("Lists", "Unordered list", "Easy", 14, "Create an unordered list with items `Apple`, `Banana`, `Cherry`.", "`<ul>` with `<li>` items makes a bulleted list.", "<ul>\n  <li>Apple</li>\n  <li>Banana</li>\n  <li>Cherry</li>\n</ul>", ["<ul>", "<li>", "apple", "banana", "cherry", "</ul>"])
    add("Lists", "Ordered list", "Easy", 14, "Create an ordered list with items `First`, `Second`, `Third`.", "`<ol>` makes a numbered list.", "<ol>\n  <li>First</li>\n  <li>Second</li>\n  <li>Third</li>\n</ol>", ["<ol>", "<li>", "first", "second", "third", "</ol>"])
    for items in [["Home", "About"], ["Red", "Green", "Blue"], ["HTML", "CSS", "JS"], ["One", "Two"], ["A", "B", "C"]]:
        add("Lists", "List: " + ", ".join(items), "Easy", 14, "Make a `<ul>` containing: " + ", ".join("`%s`" % i for i in items) + ".", "Each `<li>` is one list item inside `<ul>`.", "<ul>\n" + "\n".join("  <li>%s</li>" % i for i in items) + "\n</ul>", ["<ul>"] + [i.lower() for i in items] + ["</ul>"])
    # Tables
    add("Tables", "Basic table", "Medium", 18, "Create a `<table>` with one row containing cells `A` and `B`.", "`<table>` holds `<tr>` rows; `<td>` are data cells, `<th>` header cells.", "<table>\n  <tr><td>A</td><td>B</td></tr>\n</table>", ["<table>", "<tr>", "<td>", "</table>"])
    add("Tables", "Header row", "Medium", 18, "Create a table header row with `<th>` cells `Name` and `Age`.", "`<th>` defines a header cell.", "<table>\n  <tr><th>Name</th><th>Age</th></tr>\n</table>", ["<table>", "<th>", "name", "age"])
    for cols in [["Item", "Price"], ["City", "Country"], ["X", "Y"]]:
        add("Tables", "Table: " + "/".join(cols), "Medium", 18, "Make a table header row with `<th>` cells: " + ", ".join("`%s`" % c for c in cols) + ".", "Header cells use `<th>` inside a `<tr>`.", "<table>\n  <tr>" + "".join("<th>%s</th>" % c for c in cols) + "</tr>\n</table>", ["<table>", "<th>"] + [c.lower() for c in cols])
    # Forms
    add("Forms", "Form tag", "Medium", 18, "Create a `<form>` element.", "`<form>` collects user input.", "<form>\n</form>", ["<form>", "</form>"])
    add("Forms", "Text input", "Medium", 18, "Add a text `<input>` with name `username`.", "`<input type=\"text\">` is a single-line text field.", '<input type="text" name="username">', ["<input", "type=", "text", "name=", "username"])
    add("Forms", "Password input", "Medium", 18, "Add a password input named `pass`.", "`type=\"password\"` masks the typed characters.", '<input type="password" name="pass">', ["<input", "password", "name=", "pass"])
    add("Forms", "Submit button", "Medium", 16, "Add a submit `<button>` that says `Send`.", "`<button>` triggers the form action.", "<button>Send</button>", ["<button>", "send", "</button>"])
    add("Forms", "Label", "Medium", 16, "Add a `<label>` with text `Email`.", "`<label>` describes a form control.", "<label>Email</label>", ["<label>", "email", "</label>"])
    add("Forms", "Textarea", "Medium", 16, "Add a `<textarea>` for comments.", "`<textarea>` is a multi-line text box.", "<textarea name=\"comments\"></textarea>", ["<textarea", "</textarea>"])
    add("Forms", "Checkbox", "Medium", 16, "Add a checkbox input.", "`type=\"checkbox\"` is a toggle.", '<input type="checkbox">', ["<input", "checkbox"])
    add("Forms", "Radio button", "Medium", 16, "Add a radio input named `choice`.", "Radio buttons let users pick one option.", '<input type="radio" name="choice">', ["<input", "radio", "name=", "choice"])
    add("Forms", "Dropdown", "Medium", 18, "Create a `<select>` with options `Yes` and `No`.", "`<select>` with `<option>`s makes a dropdown.", "<select>\n  <option>Yes</option>\n  <option>No</option>\n</select>", ["<select>", "<option>", "yes", "no", "</select>"])
    add("Forms", "Email input", "Medium", 16, "Add an email input named `email`.", "`type=\"email\"` validates email format.", '<input type="email" name="email">', ["<input", "email"])
    add("Forms", "Number input", "Medium", 16, "Add a number input named `qty`.", "`type=\"number\"` only accepts numbers.", '<input type="number" name="qty">', ["<input", "number", "qty"])
    # Semantic
    for tag, desc in [("header", "top banner"), ("nav", "navigation"), ("main", "main content"), ("section", "a section"), ("article", "an article"), ("footer", "page footer"), ("aside", "sidebar"), ("figure", "a figure")]:
        add("Semantic HTML", "<%s>" % tag, "Medium", 16, "Add a `<%s>` element (the %s)." % (tag, desc), "Semantic tags describe the meaning of content for accessibility and SEO.", "<%s>\n</%s>" % (tag, tag), ["<%s>" % tag, "</%s>" % tag])
    # Projects
    add("Projects", "Page skeleton", "Hard", 30, "Build a full page skeleton: doctype, html, head with title `My Page`, and body.", "A complete page combines doctype, html, head (with title) and body.", "<!DOCTYPE html>\n<html>\n<head><title>My Page</title></head>\n<body>\n</body>\n</html>", ["<!doctype html>", "<html>", "<head>", "<title>", "my page", "<body>"])
    add("Projects", "Card component", "Hard", 30, "Build a card: an `<h2>` title `Product`, a `<p>` description, and a `<button>` `Buy`.", "Combining headings, paragraphs and buttons builds UI components.", "<div>\n  <h2>Product</h2>\n  <p>A great product.</p>\n  <button>Buy</button>\n</div>", ["<h2>", "product", "<p>", "<button>", "buy"])
    add("Projects", "Nav bar", "Hard", 30, "Build a `<nav>` with a `<ul>` of links `Home`, `About`, `Contact`.", "Navigation bars use a `<nav>` wrapping a list of `<a>` links.", "<nav>\n  <ul>\n    <li><a href=\"/\">Home</a></li>\n    <li><a href=\"/about\">About</a></li>\n    <li><a href=\"/contact\">Contact</a></li>\n  </ul>\n</nav>", ["<nav>", "<ul>", "<a", "home", "about", "contact"])
    add("Projects", "Login form", "Hard", 32, "Build a login `<form>` with email and password inputs and a submit button.", "Forms combine inputs, labels and a submit button.", '<form>\n  <input type="email" name="email">\n  <input type="password" name="pass">\n  <button>Login</button>\n</form>', ["<form>", "email", "password", "<button>"])
    return L_

# ---------------- CSS ----------------
def build_css():
    L_ = []; n = 0
    def add(mod, title, diff, xp, brief, expl, sol, toks):
        nonlocal n; n += 1; L_.append(L("css", n, mod, title, diff, xp, brief, expl, sol, toks))
    COLORS = ["red", "blue", "green", "black", "white", "orange", "purple", "teal", "gray", "navy"]
    # Selectors
    add("Selectors", "Element selector", "Easy", 12, "Write a rule that targets all `<p>` elements (empty body is fine).", "An element selector targets every tag of that type.", "p {\n}", ["p", "{", "}"])
    add("Selectors", "Class selector", "Easy", 12, "Write a rule for the class `.btn`.", "A class selector starts with a dot and targets `class=\"btn\"`.", ".btn {\n}", [".btn", "{", "}"])
    add("Selectors", "ID selector", "Easy", 12, "Write a rule for the id `#header`.", "An id selector starts with `#` and targets a unique element.", "#header {\n}", ["#header", "{", "}"])
    add("Selectors", "Universal selector", "Easy", 12, "Write the universal selector `*` rule.", "`*` targets every element.", "* {\n}", ["*", "{", "}"])
    add("Selectors", "Descendant selector", "Medium", 14, "Target `<a>` inside `<nav>`.", "Space-separated selectors target descendants.", "nav a {\n}", ["nav", "a", "{", "}"])
    add("Selectors", "Hover state", "Medium", 14, "Style the `:hover` state of a `.btn`.", "Pseudo-classes like `:hover` style interaction states.", ".btn:hover {\n}", [".btn", ":hover"])
    # Colors & backgrounds
    for c in COLORS:
        add("Colors & Backgrounds", "Text color: " + c, "Easy", 12, "Set the text `color` to `%s` on the `body`." % c, "`color` sets the text (foreground) color.", "body {\n  color: %s;\n}" % c, ["color:", c])
    for c in COLORS[:6]:
        add("Colors & Backgrounds", "Background: " + c, "Easy", 12, "Set the `background-color` to `%s` on the `body`." % c, "`background-color` fills the element's background.", "body {\n  background-color: %s;\n}" % c, ["background-color:", c])
    for hexv in ["#ff0000", "#00ff00", "#0000ff", "#333333", "#f5f5f5"]:
        add("Colors & Backgrounds", "Hex color " + hexv, "Medium", 14, "Set the text `color` to `%s`." % hexv, "Colors can be written as hex codes like `#rrggbb`.", "body {\n  color: %s;\n}" % hexv, ["color:", hexv])
    add("Colors & Backgrounds", "Opacity", "Medium", 14, "Set `opacity` to `0.5` on `.box`.", "`opacity` controls transparency from 0 to 1.", ".box {\n  opacity: 0.5;\n}", ["opacity:", "0.5"])
    # Text & fonts
    for px in [12, 14, 16, 20, 24, 32, 48]:
        add("Text & Fonts", "Font size " + str(px) + "px", "Easy", 12, "Set `font-size` to `%dpx`." % px, "`font-size` controls text size.", "p {\n  font-size: %dpx;\n}" % px, ["font-size:", "%dpx" % px])
    for w in ["bold", "normal", "300", "600", "900"]:
        add("Text & Fonts", "Font weight " + w, "Easy", 12, "Set `font-weight` to `%s`." % w, "`font-weight` controls boldness.", "p {\n  font-weight: %s;\n}" % w, ["font-weight:", w])
    for a in ["center", "left", "right", "justify"]:
        add("Text & Fonts", "Text align " + a, "Easy", 12, "Set `text-align` to `%s`." % a, "`text-align` positions inline text horizontally.", "p {\n  text-align: %s;\n}" % a, ["text-align:", a])
    add("Text & Fonts", "Font family", "Medium", 14, "Set `font-family` to `Arial`.", "`font-family` picks the typeface.", "body {\n  font-family: Arial;\n}", ["font-family:", "arial"])
    add("Text & Fonts", "Uppercase", "Medium", 14, "Make text uppercase with `text-transform`.", "`text-transform: uppercase` capitalizes all letters.", "h1 {\n  text-transform: uppercase;\n}", ["text-transform:", "uppercase"])
    add("Text & Fonts", "Line height", "Medium", 14, "Set `line-height` to `1.5`.", "`line-height` controls spacing between lines.", "p {\n  line-height: 1.5;\n}", ["line-height:", "1.5"])
    # Box model
    for px in [8, 10, 16, 20, 24, 32]:
        add("Box Model", "Padding " + str(px) + "px", "Easy", 12, "Set `padding` to `%dpx`." % px, "`padding` is space inside the element, around its content.", ".box {\n  padding: %dpx;\n}" % px, ["padding:", "%dpx" % px])
    for px in [8, 16, 24, 40]:
        add("Box Model", "Margin " + str(px) + "px", "Easy", 12, "Set `margin` to `%dpx`." % px, "`margin` is space outside the element.", ".box {\n  margin: %dpx;\n}" % px, ["margin:", "%dpx" % px])
    add("Box Model", "Width", "Easy", 12, "Set `width` to `300px` on `.box`.", "`width` sets the element's content width.", ".box {\n  width: 300px;\n}", ["width:", "300px"])
    add("Box Model", "Height", "Easy", 12, "Set `height` to `200px` on `.box`.", "`height` sets the element's content height.", ".box {\n  height: 200px;\n}", ["height:", "200px"])
    add("Box Model", "Box sizing", "Medium", 14, "Set `box-sizing` to `border-box`.", "`border-box` includes padding/border in the width.", "* {\n  box-sizing: border-box;\n}", ["box-sizing:", "border-box"])
    # Borders & radius
    add("Borders & Radius", "Border", "Easy", 12, "Add a `1px solid black` border to `.box`.", "`border` draws a line around the element.", ".box {\n  border: 1px solid black;\n}", ["border:", "1px", "solid", "black"])
    for r in [4, 8, 12, 50]:
        add("Borders & Radius", "Radius " + str(r) + "px", "Easy", 12, "Set `border-radius` to `%dpx`." % r, "`border-radius` rounds corners.", ".box {\n  border-radius: %dpx;\n}" % r, ["border-radius:", "%dpx" % r])
    add("Borders & Radius", "Circle", "Medium", 14, "Make a `.avatar` a circle with `border-radius: 50%`.", "`border-radius: 50%` turns a square into a circle.", ".avatar {\n  border-radius: 50%;\n}", ["border-radius:", "50%"])
    add("Borders & Radius", "Box shadow", "Medium", 16, "Add a `box-shadow` to `.card`.", "`box-shadow` adds depth under an element.", ".card {\n  box-shadow: 0 2px 8px rgba(0,0,0,0.2);\n}", ["box-shadow:"])
    # Layout
    add("Layout", "Display block", "Medium", 14, "Set `display` to `block`.", "`display` controls how an element is laid out.", "span {\n  display: block;\n}", ["display:", "block"])
    add("Layout", "Display none", "Medium", 14, "Hide `.hidden` with `display: none`.", "`display: none` removes the element from layout.", ".hidden {\n  display: none;\n}", ["display:", "none"])
    add("Layout", "Flexbox", "Medium", 18, "Make `.row` a flex container with `display: flex`.", "Flexbox lays children in a flexible row or column.", ".row {\n  display: flex;\n}", ["display:", "flex"])
    add("Layout", "Justify content", "Medium", 18, "Center flex items with `justify-content: center`.", "`justify-content` aligns items along the main axis.", ".row {\n  display: flex;\n  justify-content: center;\n}", ["justify-content:", "center"])
    add("Layout", "Align items", "Medium", 18, "Vertically center with `align-items: center`.", "`align-items` aligns items along the cross axis.", ".row {\n  display: flex;\n  align-items: center;\n}", ["align-items:", "center"])
    add("Layout", "Gap", "Medium", 16, "Add a `gap` of `16px` between flex items.", "`gap` spaces flex/grid children.", ".row {\n  display: flex;\n  gap: 16px;\n}", ["gap:", "16px"])
    add("Layout", "Grid", "Medium", 18, "Make `.grid` a grid with 3 columns.", "CSS Grid lays out items in rows and columns.", ".grid {\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n}", ["display:", "grid", "grid-template-columns:"])
    # Positioning
    for pos in ["relative", "absolute", "fixed", "sticky"]:
        add("Positioning", "Position " + pos, "Medium", 16, "Set `position` to `%s`." % pos, "`position` controls how an element is placed.", ".el {\n  position: %s;\n}" % pos, ["position:", pos])
    add("Positioning", "Z-index", "Medium", 14, "Set `z-index` to `10`.", "`z-index` controls stacking order.", ".el {\n  position: relative;\n  z-index: 10;\n}", ["z-index:", "10"])
    # Projects
    add("Projects", "Center a box", "Hard", 30, "Center `.box` both ways using flexbox on `.parent`.", "`display:flex` + `justify-content:center` + `align-items:center` centers a child.", ".parent {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}", ["display:", "flex", "justify-content:", "center", "align-items:"])
    add("Projects", "Button style", "Hard", 30, "Style `.btn`: green background, white text, 8px padding, 50px radius.", "Combine background, color, padding and radius for a pill button.", ".btn {\n  background-color: green;\n  color: white;\n  padding: 8px 16px;\n  border-radius: 50px;\n}", ["background-color:", "green", "color:", "white", "padding:", "border-radius:"])
    add("Projects", "Card style", "Hard", 30, "Style `.card`: white background, 12px radius, a box-shadow, 16px padding.", "Cards combine background, radius, shadow and padding.", ".card {\n  background-color: white;\n  border-radius: 12px;\n  box-shadow: 0 1px 3px rgba(0,0,0,0.2);\n  padding: 16px;\n}", ["background-color:", "white", "border-radius:", "12px", "box-shadow:", "padding:"])
    return L_

# ---------------- generic smaller banks ----------------
def build_simple(lid, groups):
    """groups: list of (module, [ (title, brief, expl, solution, tokens) ])"""
    L_ = []; n = 0
    for mod, items in groups:
        for (title, brief, expl, sol, toks) in items:
            n += 1; L_.append(L(lid, n, mod, title, "Easy", 14, brief, expl, sol, toks))
    return L_

def build_json():
    g = [
     ("Basics", [
        ("Empty object", "Write an empty JSON object.", "JSON objects use `{ }`.", "{}", ["{", "}"]),
        ("Empty array", "Write an empty JSON array.", "JSON arrays use `[ ]`.", "[]", ["[", "]"]),
        ("String value", "Create an object with key `name` = `Sam`.", "Keys and string values use double quotes.", '{ "name": "Sam" }', ['"name"', '"sam"']),
        ("Number value", "Create an object with key `age` = `30`.", "Numbers are written without quotes.", '{ "age": 30 }', ['"age"', "30"]),
        ("Boolean value", "Create an object with key `active` = `true`.", "Booleans are `true`/`false`, no quotes.", '{ "active": true }', ['"active"', "true"]),
        ("Null value", "Create an object with key `data` = `null`.", "`null` represents no value.", '{ "data": null }', ['"data"', "null"]),
     ]),
     ("Structures", [
        ("Array of numbers", "Create an array `[1, 2, 3]`.", "Arrays hold ordered values.", "[1, 2, 3]", ["[", "1", "2", "3", "]"]),
        ("Array of strings", "Create an array of `a`, `b`, `c`.", "String items use double quotes.", '["a", "b", "c"]', ['"a"', '"b"', '"c"']),
        ("Nested object", "Object `user` with nested `name` = `Ana`.", "Objects can nest inside objects.", '{ "user": { "name": "Ana" } }', ['"user"', '"name"', '"ana"']),
        ("Array of objects", "Array with one object `{id:1}`.", "Arrays can hold objects.", '[{ "id": 1 }]', ["[", '"id"', "1", "]"]),
        ("Multiple keys", "Object with `x`=1 and `y`=2.", "Separate key/value pairs with commas.", '{ "x": 1, "y": 2 }', ['"x"', "1", '"y"', "2"]),
     ]),
     ("Real-world", [
        ("Person", "Object with `name` `Sam`, `age` 25, `student` true.", "Combine types in one object.", '{ "name": "Sam", "age": 25, "student": true }', ['"name"', '"age"', "25", '"student"', "true"]),
        ("Config", "Object with `port` 3000 and `host` `localhost`.", "Config files are commonly JSON.", '{ "port": 3000, "host": "localhost" }', ['"port"', "3000", '"host"', '"localhost"']),
        ("List of tags", "Object with `tags` = array of `js`, `web`.", "Arrays as values are common.", '{ "tags": ["js", "web"] }', ['"tags"', '"js"', '"web"']),
     ]),
    ]
    return build_simple("json", g)

def build_yaml():
    g = [
     ("Basics", [
        ("Key value", "Write a YAML key `name` with value `Sam`.", "YAML uses `key: value` pairs.", "name: Sam", ["name:", "sam"]),
        ("Number", "Set `age` to `30`.", "Numbers need no quotes.", "age: 30", ["age:", "30"]),
        ("Boolean", "Set `active` to `true`.", "Booleans are `true`/`false`.", "active: true", ["active:", "true"]),
        ("String quote", "Set `city` to `New York`.", "Quotes are optional but help with spaces.", 'city: "New York"', ["city:", "new york"]),
     ]),
     ("Lists", [
        ("Simple list", "Make a list `fruits` with `apple`, `banana`.", "List items start with `- `.", "fruits:\n  - apple\n  - banana", ["fruits:", "- apple", "- banana"]),
        ("Inline list", "Make an inline list `[1, 2, 3]` for `nums`.", "Flow style uses brackets.", "nums: [1, 2, 3]", ["nums:", "1", "2", "3"]),
        ("List of three", "List `colors` with red, green, blue.", "Each item on its own line with `-`.", "colors:\n  - red\n  - green\n  - blue", ["colors:", "- red", "- green", "- blue"]),
     ]),
     ("Nested & Config", [
        ("Nested map", "Nested: `server` with `host: localhost`.", "Indentation creates nesting.", "server:\n  host: localhost", ["server:", "host:", "localhost"]),
        ("Port config", "`server` with `port: 8080`.", "Common in config files.", "server:\n  port: 8080", ["server:", "port:", "8080"]),
        ("CI step", "A `steps` list with one `- run: build`.", "Pipelines use lists of steps.", "steps:\n  - run: build", ["steps:", "- run:", "build"]),
     ]),
    ]
    return build_simple("yaml", g)

def build_markdown():
    g = [
     ("Text", [
        ("H1 heading", "Write an H1 heading `Title`.", "`# ` makes a top-level heading.", "# Title", ["# title"]),
        ("H2 heading", "Write an H2 heading `Section`.", "`## ` makes a second-level heading.", "## Section", ["## section"]),
        ("Bold", "Make `important` bold.", "Wrap text in `**` for bold.", "**important**", ["**important**"]),
        ("Italic", "Make `note` italic.", "Wrap text in `*` for italic.", "*note*", ["*note*"]),
        ("Inline code", "Show `print()` as inline code.", "Wrap code in backticks.", "`print()`", ["`print()`"]),
     ]),
     ("Lists & Links", [
        ("Bullet list", "Make a bullet list of `A`, `B`.", "`- ` starts a bullet.", "- A\n- B", ["- a", "- b"]),
        ("Numbered list", "Make a numbered list `First`, `Second`.", "`1. ` starts a numbered list.", "1. First\n2. Second", ["1. first", "2. second"]),
        ("Link", "Link text `Google` to `https://google.com`.", "`[text](url)` makes a link.", "[Google](https://google.com)", ["[google]", "(https://google.com)"]),
        ("Image", "Embed image `pic.png` with alt `Photo`.", "`![alt](src)` embeds an image.", "![Photo](pic.png)", ["![photo]", "(pic.png)"]),
     ]),
     ("Blocks", [
        ("Blockquote", "Write a blockquote `Hello`.", "`> ` starts a quote.", "> Hello", ["> hello"]),
        ("Code block", "Write a fenced code block.", "Triple backticks fence a code block.", "```\ncode\n```", ["```"]),
        ("Horizontal rule", "Add a horizontal rule.", "`---` draws a divider.", "---", ["---"]),
     ]),
    ]
    return build_simple("markdown", g)

def build_xml():
    g = [
     ("Basics", [
        ("Root element", "Create a `<note>` root element.", "XML wraps data in custom tags.", "<note>\n</note>", ["<note>", "</note>"]),
        ("Child element", "Add a `<to>` child with text `Sam`.", "Elements nest like a tree.", "<note>\n  <to>Sam</to>\n</note>", ["<to>", "sam", "</to>"]),
        ("Attribute", "Add an attribute `id=\"1\"` to `<item>`.", "Attributes add metadata to elements.", '<item id="1"></item>', ["<item", "id=", "1"]),
        ("Declaration", "Add an XML declaration.", "The prolog declares version and encoding.", '<?xml version="1.0" encoding="UTF-8"?>', ["<?xml", "version=", "1.0"]),
     ]),
     ("Structure", [
        ("Two children", "`<user>` with `<name>` and `<age>`.", "Multiple children describe an entity.", "<user>\n  <name>Ana</name>\n  <age>30</age>\n</user>", ["<user>", "<name>", "<age>"]),
        ("List items", "`<list>` with two `<item>` children.", "Repeated tags model lists.", "<list>\n  <item>A</item>\n  <item>B</item>\n</list>", ["<list>", "<item>", "</item>"]),
     ]),
    ]
    return build_simple("xml", g)

def build_dockerfile():
    g = [
     ("Image & Setup", [
        ("FROM", "Start from the `node:20` base image.", "`FROM` sets the base image.", "FROM node:20", ["from ", "node:20"]),
        ("WORKDIR", "Set the working directory to `/app`.", "`WORKDIR` sets the current dir.", "WORKDIR /app", ["workdir ", "/app"]),
        ("COPY", "Copy `package.json` into the image.", "`COPY src dest` adds files.", "COPY package.json .", ["copy ", "package.json"]),
        ("RUN", "Run `npm install`.", "`RUN` executes a build command.", "RUN npm install", ["run ", "npm install"]),
     ]),
     ("Runtime", [
        ("EXPOSE", "Expose port `3000`.", "`EXPOSE` documents the port.", "EXPOSE 3000", ["expose ", "3000"]),
        ("ENV", "Set env `NODE_ENV` to `production`.", "`ENV` sets environment variables.", "ENV NODE_ENV=production", ["env ", "node_env", "production"]),
        ("CMD", "Run `node server.js` on start.", "`CMD` is the default container command.", 'CMD ["node", "server.js"]', ["cmd ", "node", "server.js"]),
        ("Full image", "Combine FROM node:20, WORKDIR /app, CMD.", "A minimal Dockerfile chains these steps.", 'FROM node:20\nWORKDIR /app\nCMD ["node", "server.js"]', ["from ", "workdir ", "cmd "]),
     ]),
    ]
    return build_simple("dockerfile", g)

def build_graphql():
    g = [
     ("Queries", [
        ("Simple query", "Query a `user` field.", "Queries request specific fields.", "query {\n  user\n}", ["query", "user", "{", "}"]),
        ("Nested fields", "Query `user` with `name`.", "Select nested fields inside braces.", "query {\n  user {\n    name\n  }\n}", ["query", "user", "name"]),
        ("Arguments", "Query `user(id: 1)` with `name`.", "Arguments filter the data.", "query {\n  user(id: 1) {\n    name\n  }\n}", ["user(id: 1)", "name"]),
     ]),
     ("Schema", [
        ("Type", "Define a `type User` with `name: String`.", "Types describe your data shape.", "type User {\n  name: String\n}", ["type user", "name:", "string"]),
        ("Field types", "`User` with `id: Int` and `name: String`.", "Each field has a type.", "type User {\n  id: Int\n  name: String\n}", ["type user", "id:", "int", "name:", "string"]),
        ("Mutation", "Define a `Mutation` with `addUser`.", "Mutations change data.", "type Mutation {\n  addUser: User\n}", ["mutation", "adduser"]),
     ]),
    ]
    return build_simple("graphql", g)

def build_regex():
    g = [
     ("Characters", [
        ("Digit", "Match a single digit with `\\d`.", "`\\d` matches any digit 0-9.", "\\d", ["\\d"]),
        ("Word char", "Match a word character with `\\w`.", "`\\w` matches letters, digits, underscore.", "\\w", ["\\w"]),
        ("Whitespace", "Match whitespace with `\\s`.", "`\\s` matches spaces, tabs, newlines.", "\\s", ["\\s"]),
        ("Any char", "Match any character with `.`.", "`.` matches any single character.", ".", ["."]),
     ]),
     ("Quantifiers & Anchors", [
        ("One or more", "Match one or more digits.", "`+` means one or more.", "\\d+", ["\\d+"]),
        ("Zero or more", "Match zero or more word chars.", "`*` means zero or more.", "\\w*", ["\\w*"]),
        ("Start anchor", "Anchor to the start of a line.", "`^` matches the start.", "^abc", ["^"]),
        ("End anchor", "Anchor to the end of a line.", "`$` matches the end.", "abc$", ["$"]),
        ("Exactly n", "Match exactly 3 digits.", "`{3}` means exactly three.", "\\d{3}", ["\\d{3}"]),
     ]),
     ("Patterns", [
        ("Email-ish", "Match text with an `@` between word chars.", "Combine classes to match patterns.", "\\w+@\\w+", ["\\w+", "@", "\\w+"]),
        ("Char set", "Match a vowel using a character set.", "`[...]` matches any listed char.", "[aeiou]", ["[aeiou]"]),
        ("Range", "Match a lowercase letter `a-z`.", "Ranges use a hyphen inside `[]`.", "[a-z]", ["[a-z]"]),
     ]),
    ]
    return build_simple("regex", g)

BUILDERS = {"html": build_html, "css": build_css, "scss": lambda: build_simple("scss", [
     ("Variables", [
        ("Declare variable", "Declare a SCSS variable `$primary` = `blue`.", "SCSS variables start with `$`.", "$primary: blue;", ["$primary:", "blue"]),
        ("Use variable", "Use `$primary` as a text color.", "Reference variables anywhere.", "$primary: blue;\np { color: $primary; }", ["$primary", "color:"]),
        ("Number variable", "Declare `$gap` = `16px`.", "Variables can hold any value.", "$gap: 16px;", ["$gap:", "16px"]),
     ]),
     ("Nesting", [
        ("Nest a rule", "Nest `a` inside `nav`.", "SCSS lets you nest selectors.", "nav {\n  a {\n    color: red;\n  }\n}", ["nav", "a", "{", "color:"]),
        ("Parent selector", "Style `&:hover` inside `.btn`.", "`&` refers to the parent selector.", ".btn {\n  &:hover {\n    color: green;\n  }\n}", ["&:hover", "color:"]),
     ]),
     ("Mixins", [
        ("Define mixin", "Define a mixin `@mixin center`.", "Mixins are reusable rule groups.", "@mixin center {\n  display: flex;\n}", ["@mixin", "center"]),
        ("Include mixin", "Include a mixin with `@include center`.", "`@include` applies a mixin.", ".box { @include center; }", ["@include", "center"]),
     ]),
]), "json": build_json, "yaml": build_yaml, "markdown": build_markdown,
 "xml": build_xml, "dockerfile": build_dockerfile, "graphql": build_graphql, "regex": build_regex}

WEB_MATERIAL = {
 "html": "**HTML** (HyperText Markup Language) is the skeleton of every web page. You describe content with **tags** like `<h1>`, `<p>`, and `<a>`. Tags usually come in pairs — an opening `<p>` and a closing `</p>` — wrapping their content. Attributes (like `href` on a link) add extra info.",
 "css": "**CSS** (Cascading Style Sheets) styles your HTML. A rule has a **selector** (what to style) and a **declaration block** of `property: value;` pairs. Example: `p { color: blue; }` makes all paragraphs blue. CSS controls color, spacing, layout, and more.",
 "scss": "**SCSS** is a superset of CSS that adds **variables** (`$primary`), **nesting**, and **mixins** so stylesheets stay DRY. It compiles down to regular CSS.",
 "json": "**JSON** (JavaScript Object Notation) is the universal data-exchange format. Data is either an **object** `{ \"key\": value }` or an **array** `[ ... ]`. Strings and keys use double quotes; values can be strings, numbers, booleans, null, objects, or arrays.",
 "yaml": "**YAML** is a human-friendly config format used in CI pipelines, Kubernetes, and more. It uses **indentation** for structure, `key: value` pairs, and `- ` for list items.",
 "markdown": "**Markdown** is a lightweight syntax for formatted text. `#` makes headings, `**bold**`, `*italic*`, `- ` bullet lists, and `[text](url)` links. It powers READMEs, docs, and chat.",
 "xml": "**XML** stores data in a tree of custom tags with optional attributes. It's verbose but strict — every tag must close. Used in configs, feeds, and document formats.",
 "dockerfile": "**Dockerfiles** describe how to build a container image. Each instruction (`FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`) becomes a layer. `FROM` picks a base image; `CMD` is what runs when the container starts.",
 "graphql": "**GraphQL** is a query language for APIs. Clients ask for exactly the fields they need. A **schema** defines `type`s and their fields; **queries** read data and **mutations** change it.",
 "regex": "**Regular expressions** match patterns in text. Character classes (`\\d` digit, `\\w` word, `\\s` space), quantifiers (`+` one-or-more, `*` zero-or-more, `{n}` exactly n), and anchors (`^` start, `$` end) combine into powerful matchers.",
}

def build_web_track(lid):
    name, lang, engine, color, icon, blurb = WEB_META[lid]
    lessons = BUILDERS[lid]()
    mats = {}
    for l in lessons:
        if l["module"] not in mats:
            mats[l["module"]] = {"text": WEB_MATERIAL.get(lid, "Practice the core ideas of this module below."), "code": l["hint"]}
    return {"id": lid, "name": name, "lang": lang, "engine": engine, "color": color, "icon": icon, "blurb": blurb, "lessons": lessons, "materials": mats}

if __name__ == "__main__":
    for lid in WEB_ORDER:
        t = build_web_track(lid)
        print(t["icon"], t["name"], len(t["lessons"]), "lessons")
