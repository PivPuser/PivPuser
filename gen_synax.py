#!/usr/bin/env python3
# Generates the "version B" (Synax-style) SVG assets with embedded Shadows Into Light font.
import base64, os

HERE = os.path.dirname(__file__)
A = os.path.join(HERE, "assets")
font_b64 = base64.b64encode(open(os.path.join(A, "ShadowsIntoLight-Regular.ttf"), "rb").read()).decode("ascii")
FONT = ("<defs><style>@font-face{font-family:'SIL';"
        "src:url(data:font/ttf;base64," + font_b64 + ") format('truetype');}"
        "text{font-family:'SIL','Shadows Into Light',cursive;}</style></defs>")

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def write(name, w, h, inner, bg="#0d1117"):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{w}" height="{h}" role="img">{FONT}{rect}{inner}</svg>')
    open(os.path.join(A, name), "w", encoding="utf-8").write(doc)
    print("wrote", name)

def heading(w, text, y=46):
    cx = w / 2
    return (f'<text x="{cx}" y="{y}" text-anchor="middle" font-size="34" fill="#ffffff">{esc(text)}</text>'
            f'<line x1="{w*0.12:.0f}" y1="{y+16}" x2="{w*0.88:.0f}" y2="{y+16}" stroke="#30363d" stroke-width="1.2"/>')

def lines(xs, y0, dy, items, size, fill, anchor="start"):
    out = []
    for i, t in enumerate(items):
        out.append(f'<text x="{xs}" y="{y0 + i*dy}" text-anchor="{anchor}" font-size="{size}" fill="{fill}">{esc(t)}</text>')
    return "".join(out)

# ---- banner: scythe + handwritten nick (white bg) ----
scythe = (
    '<path d="M48 150 C 210 44, 470 30, 606 116 C 480 102, 250 110, 48 150 Z" fill="#111111"/>'
    '<path d="M600 108 L676 244" stroke="#111111" stroke-width="13" stroke-linecap="round"/>'
    '<path d="M600 150 C 560 176, 576 216, 612 196 C 650 216, 664 176, 624 150" fill="none" stroke="#c2c2c2" stroke-width="3"/>'
    '<text x="70" y="234" font-size="66" fill="#111111">PivPuser</text>'
)
write("banner.svg", 760, 250, scythe, bg="#ffffff")

# ---- about ----
bio = [
    "Hey, I'm PivPuser. A mid-level dev and reverse engineer who'd rather",
    "read disassembly than docs. By day I write code; by night I take",
    "other people's code apart to see how it works, until something gives.",
    "Runs on coffee and stubbornness.",
]
about = heading(820, "Know About Me") + lines(70, 100, 30, bio, 21, "#b9c0c7")
write("about.svg", 820, 210, about)

# ---- projects (sits next to the cube gif) ----
proj = [
    "MOD MENU : runtime DLL menu for a UE3 game. easier than asking nicely.",
    "MEM POKE : reads and writes process memory so i don't have to.",
    "DISASM NOTES : my RE notes; mostly arrows at functions i don't get yet.",
]
projects = heading(620, "Top Projects (built to avoid manual labor)", y=40) + lines(30, 92, 32, proj, 19, "#b9c0c7")
write("projects.svg", 620, 200, projects)

# ---- connect heading ----
write("connect.svg", 820, 72, heading(820, "Connect", y=44))

# ---- quotes ----
q = [
    "“code is never finished. it just gets less embarrassing over time.”",
    "“every commit is a tiny apology to whoever debugs this next. usually me.”",
]
quotes = ('<line x1="60" y1="22" x2="60" y2="104" stroke="#30363d" stroke-width="3"/>'
          + lines(78, 56, 42, q, 20, "#8b949e"))
write("quotes.svg", 820, 130, quotes)

# ---- contribution heading ----
write("contrib.svg", 820, 72, heading(820, "Contribution", y=44))

print("done")
