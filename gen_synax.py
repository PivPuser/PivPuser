#!/usr/bin/env python3
# Generates the "version B" (Synax-style) SVG assets with embedded Shadows Into Light font.
import base64, os, math, random

random.seed(5)
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

# coffee cup inner (white cup, brown coffee, 3 animated steam wisps)
CUP_INNER = ('<path d="M198 148 C 236 150, 236 186, 188 188" fill="none" stroke="#ffffff" stroke-width="11" stroke-linecap="round"/>'
       '<path d="M38 120 C 44 178, 72 224, 120 224 C 168 224, 196 178, 202 120 Z" fill="#ffffff"/>'
       '<ellipse cx="120" cy="120" rx="82" ry="18" fill="#ffffff"/>'
       '<ellipse cx="120" cy="120" rx="72" ry="13" fill="#6F4E37"/>'
       '<g opacity="0"><path d="M100 116 C 90 102, 110 94, 98 78 C 88 64, 106 56, 98 42" fill="none" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round"/>'
       '<animateTransform attributeName="transform" type="translate" values="0 6; 0 -14" dur="4.5s" begin="0s" repeatCount="indefinite"/>'
       '<animate attributeName="opacity" values="0; 0.9; 0" keyTimes="0; 0.45; 1" dur="4.5s" begin="0s" repeatCount="indefinite"/></g>'
       '<g opacity="0"><path d="M120 116 C 110 102, 130 94, 118 78 C 108 64, 126 56, 118 42" fill="none" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round"/>'
       '<animateTransform attributeName="transform" type="translate" values="0 6; 0 -15" dur="4.5s" begin="1.5s" repeatCount="indefinite"/>'
       '<animate attributeName="opacity" values="0; 0.95; 0" keyTimes="0; 0.45; 1" dur="4.5s" begin="1.5s" repeatCount="indefinite"/></g>'
       '<g opacity="0"><path d="M140 116 C 130 102, 150 94, 138 78 C 128 64, 146 56, 138 42" fill="none" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round"/>'
       '<animateTransform attributeName="transform" type="translate" values="0 6; 0 -14" dur="4.5s" begin="3s" repeatCount="indefinite"/>'
       '<animate attributeName="opacity" values="0; 0.9; 0" keyTimes="0; 0.45; 1" dur="4.5s" begin="3s" repeatCount="indefinite"/></g>')

def about_art():
    cx, cy = 715, 113
    saucer = f'<ellipse cx="{cx}" cy="158" rx="40" ry="7" fill="#ffffff"/>'
    cup = '<g transform="translate(660 52) scale(0.46)">' + CUP_INNER + '</g>'
    ring = ['<g><animateTransform attributeName="transform" type="rotate" '
            f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="2.4s" repeatCount="indefinite"/>']
    N, R = 14, 55
    for i in range(N):
        th = i * 2 * math.pi / N
        x = cx + R * math.sin(th)
        y = cy - R * math.cos(th)
        ang = i * 360.0 / N
        ring.append(f'<text x="{x:.1f}" y="{y:.1f}" transform="rotate({ang:.1f} {x:.1f} {y:.1f})" '
                    f'text-anchor="middle" dominant-baseline="central" font-size="13" fill="#ffffff" '
                    f'style="font-family:monospace">{random.choice("01")}</text>')
    ring.append('</g>')
    return saucer + cup + "".join(ring)

# ---- about ----
bio = [
    "Hey, I'm PivPuser. A mid-level dev and reverse engineer who'd rather",
    "read disassembly than docs. By day I write code; by night I take",
    "other people's code apart to see how it works, until something gives.",
    "Runs on coffee and stubbornness.",
]
about = heading(820, "Know About Me") + lines(70, 102, 30, bio, 21, "#b9c0c7") + about_art()
write("about.svg", 820, 215, about)

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
