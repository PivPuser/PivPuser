#!/usr/bin/env python3
# Generates assets/header.svg : a self-contained SMIL-animated GitHub profile header.
import math, random, os

random.seed(7)

W, H = 720, 560
CX = 360
RCY = 150          # ring/cup center y
R = 92             # ring radius
N = 30             # ring digit count
T = 10.0           # name decode cycle length (s)
GLYPHS = list("@#&*>0/1")

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

out = []
out.append(f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" '
           f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace" role="img" '
           f'aria-label="PivPuser animated profile header">')

# ---- background ----
out.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="20" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>')

# ---- binary ring (rotates as a group) ----
out.append(f'<g>')
out.append(f'<animateTransform attributeName="transform" type="rotate" from="0 {CX} {RCY}" to="360 {CX} {RCY}" dur="26s" repeatCount="indefinite"/>')
for i in range(N):
    th = i * 2 * math.pi / N
    x = CX + R * math.sin(th)
    y = RCY - R * math.cos(th)
    ang = i * 360.0 / N
    d = random.choice("01")
    out.append(f'<text x="{x:.1f}" y="{y:.1f}" transform="rotate({ang:.1f} {x:.1f} {y:.1f})" '
               f'text-anchor="middle" dominant-baseline="central" font-size="16" font-weight="500" '
               f'fill="#ffffff">{d}</text>')
out.append('</g>')

# ---- coffee cup (scaled + centered at CX,RCY) ----
s = 104.0 / 240.0
tx = CX - 240 * s / 2
ty = RCY - 250 * s / 2
out.append(f'<g transform="translate({tx:.1f} {ty:.1f}) scale({s:.4f})">')
out.append('<path d="M198 148 C 236 150, 236 186, 188 188" fill="none" stroke="#ffffff" stroke-width="11" stroke-linecap="round"/>')
out.append('<path d="M38 120 C 44 178, 72 224, 120 224 C 168 224, 196 178, 202 120 Z" fill="#ffffff"/>')
out.append('<ellipse cx="120" cy="120" rx="82" ry="18" fill="#ffffff"/>')
out.append('<ellipse cx="120" cy="120" rx="72" ry="13" fill="#6F4E37"/>')
steam = [
    ("M100 116 C 90 102, 110 94, 98 78 C 88 64, 106 56, 98 42", "0s", "0 6; 0 -14", "0; 0.9; 0", "4.5s"),
    ("M120 116 C 110 102, 130 94, 118 78 C 108 64, 126 56, 118 42", "1.5s", "0 6; 0 -15", "0; 0.95; 0", "4.5s"),
    ("M140 116 C 130 102, 150 94, 138 78 C 128 64, 146 56, 138 42", "3s", "0 6; 0 -14", "0; 0.9; 0", "4.5s"),
]
for d, beg, tr, op, dur in steam:
    out.append('<g opacity="0">')
    out.append(f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round"/>')
    out.append(f'<animateTransform attributeName="transform" type="translate" values="{tr}" dur="{dur}" begin="{beg}" repeatCount="indefinite"/>')
    out.append(f'<animate attributeName="opacity" values="{op}" keyTimes="0; 0.45; 1" dur="{dur}" begin="{beg}" repeatCount="indefinite"/>')
    out.append('</g>')
out.append('</g>')

# ---- prompt line ----
out.append(f'<text x="{CX}" y="300" text-anchor="middle" font-size="15" fill="#ffffff">{esc("PivPuser:~$ Hi, how are you?")}</text>')

# ---- name decode "PivPuser" ----
name = "PivPuser"
cw = 24
nstart = CX - len(name) * cw / 2
ny = 360
for i, ch in enumerate(name):
    x = nstart + cw / 2 + i * cw
    lock = (i + 1) * 0.82
    kt = lock / T
    # scramble gate group (round-robin glyphs), hidden after lock
    out.append('<g>')
    out.append(f'<animate attributeName="opacity" values="1;0" keyTimes="0;{kt:.4f}" '
               f'dur="{T}s" calcMode="discrete" repeatCount="indefinite"/>')
    gl = random.sample(GLYPHS, 4)
    for k, g in enumerate(gl):
        vals = ["0", "0", "0", "0"]
        vals[k] = "1"
        out.append(f'<text x="{x:.1f}" y="{ny}" text-anchor="middle" font-size="40" font-weight="600" '
                   f'fill="#ffffff">{esc(g)}'
                   f'<animate attributeName="opacity" values="{";".join(vals)}" '
                   f'keyTimes="0;0.25;0.5;0.75" dur="0.4s" calcMode="discrete" repeatCount="indefinite"/>'
                   f'</text>')
    out.append('</g>')
    # final letter, appears at lock
    out.append(f'<text x="{x:.1f}" y="{ny}" text-anchor="middle" font-size="40" font-weight="600" '
               f'fill="#ffffff" opacity="0">{esc(ch)}'
               f'<animate attributeName="opacity" values="0;1" keyTimes="0;{kt:.4f}" '
               f'dur="{T}s" calcMode="discrete" repeatCount="indefinite"/>'
               f'</text>')

# ---- "- OK" (blinks during hold window) ----
ok_x = nstart + len(name) * cw + 14
lock_last = len(name) * 0.82
gate = lock_last / T
hp = 0.043
kts = [0.0, gate]
vals = ["0", "1"]
tcur = gate + hp
flip = 0
while tcur < 1.0:
    kts.append(round(tcur, 4))
    vals.append("0" if flip == 0 else "1")
    flip ^= 1
    tcur += hp
kts.append(1.0)
vals.append("0")
out.append(f'<text x="{ok_x:.1f}" y="{ny}" text-anchor="start" font-size="26" font-weight="600" '
           f'fill="#ffffff" opacity="0">- OK'
           f'<animate attributeName="opacity" values="{";".join(vals)}" '
           f'keyTimes="{";".join(str(k) for k in kts)}" dur="{T}s" calcMode="discrete" repeatCount="indefinite"/>'
           f'</text>')

# ---- role (typed once) "[Mid-level] developer & reverse engineer" ----
role = "[Mid-level] developer & reverse engineer"
mid_len = 11
cwr = 10.8
rstart = CX - len(role) * cwr / 2
ry = 408
appear_base = 0.4
appear_step = 0.06
mid_group = []
rest = []
for j, ch in enumerate(role):
    x = rstart + cwr / 2 + j * cwr
    beg = appear_base + j * appear_step
    t = (f'<text x="{x:.1f}" y="{ry}" text-anchor="middle" font-size="18" fill="#ffffff" opacity="0">'
         f'{esc(ch)}'
         f'<animate attributeName="opacity" values="0;1" dur="0.08s" begin="{beg:.2f}s" fill="freeze"/>'
         f'<animate attributeName="fill" values="#0d1117;#ffffff;#0d1117;#ffffff" dur="0.5s" '
         f'begin="{beg:.2f}s" fill="freeze"/>'
         f'</text>')
    (mid_group if j < mid_len else rest).append(t)

typed_done = appear_base + len(role) * appear_step + 0.3
out.append(f'<g>')
out.extend(mid_group)
out.append(f'<animate attributeName="opacity" values="1;0;1" dur="0.4s" begin="{typed_done:.2f}s" '
           f'repeatCount="8" fill="freeze"/>')
out.append('</g>')
out.extend(rest)

# ---- tagline ----
out.append(f'<text x="{CX}" y="448" text-anchor="middle" font-size="14" fill="#8b949e">'
           f'{esc("// running on caffeine, curiosity & raw pointers")}</text>')

out.append('</svg>')

os.makedirs(os.path.join(os.path.dirname(__file__), "assets"), exist_ok=True)
path = os.path.join(os.path.dirname(__file__), "assets", "header.svg")
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("written:", path, "bytes:", os.path.getsize(path))
