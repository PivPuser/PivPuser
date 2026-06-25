#!/usr/bin/env python3
# Generates assets/cube.gif : a small tumbling wireframe cube with 0/1 on its faces.
import math, random, os
from PIL import Image, ImageDraw, ImageFont

random.seed(11)
SIZE = 160
CENTER = SIZE / 2
SCALE = 60
D = 4.2          # camera distance
F = 2.3          # focal
FRAMES = 36
LINE = (255, 255, 255, 255)

font = ImageFont.load_default(size=13)

# 8 cube vertices
verts = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
# 12 edges: pairs differing in exactly one coordinate
edges = []
for i in range(8):
    for j in range(i + 1, 8):
        if sum(a != b for a, b in zip(verts[i], verts[j])) == 1:
            edges.append((i, j))

# a few fixed 0/1 markers sitting on the 6 faces
markers = []
for axis in range(3):
    for sign in (-1, 1):
        for _ in range(2):
            p = [0, 0, 0]
            p[axis] = sign
            o1, o2 = [k for k in range(3) if k != axis]
            p[o1] = random.choice([-0.55, 0.0, 0.55])
            p[o2] = random.choice([-0.55, 0.0, 0.55])
            markers.append((tuple(p), random.choice("01")))

def rot(p, ax, ay, az):
    x, y, z = p
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    x, y = x * math.cos(az) - y * math.sin(az), x * math.sin(az) + y * math.cos(az)
    return (x, y, z)

def proj(p):
    x, y, z = p
    s = F / (D - z)
    return (CENTER + x * s * SCALE, CENTER + y * s * SCALE)

def to_p(im):
    alpha = im.split()[3]
    p = im.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
    mask = alpha.point(lambda a: 255 if a <= 128 else 0)
    p.paste(255, mask)
    return p

frames = []
for fr in range(FRAMES):
    t = fr / FRAMES
    ax = 2 * math.pi * 1 * t
    ay = 2 * math.pi * 2 * t
    az = 2 * math.pi * 3 * t
    rv = [rot(v, ax, ay, az) for v in verts]
    pv = [proj(v) for v in rv]
    im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    for a, b in edges:
        dr.line([pv[a], pv[b]], fill=LINE, width=2)
    for mp, ch in markers:
        x, y = proj(rot(mp, ax, ay, az))
        dr.text((x - 4, y - 7), ch, font=font, fill=LINE)
    frames.append(to_p(im))

path = os.path.join(os.path.dirname(__file__), "assets", "cube.gif")
frames[0].save(path, save_all=True, append_images=frames[1:], duration=70,
               loop=0, transparency=255, disposal=2, optimize=False)
print("written:", path, os.path.getsize(path), "bytes,", FRAMES, "frames,", SIZE, "px")
