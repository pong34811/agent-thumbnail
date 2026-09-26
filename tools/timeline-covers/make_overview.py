import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(r"D:\agent-thumbnail\outputs\aomi-debut-20260731")
items = json.loads((OUT / "delivery-manifest.json").read_text(encoding="utf-8"))
f = ImageFont.truetype(r"D:\agent-thumbnail\outputs\timeline-covers\fonts\Mitr-Bold.ttf", 22)
dest = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT


def sheet(sel, name, cell, cols):
    cw, ch = cell
    rows = (len(sel) + cols - 1) // cols
    out = Image.new("RGB", (cw * cols, (ch + 34) * rows), (20, 20, 26))
    d = ImageDraw.Draw(out)
    for n, it in enumerate(sel):
        x, y = (n % cols) * cw, (n // cols) * (ch + 34)
        with Image.open(it["path"]) as im:
            im = im.convert("RGB")
            im.thumbnail((cw - 8, ch))
        out.paste(im, (x + 4, y + 30))
        d.text((x + 6, y + 3), f"{it['timeline_index']}. {Path(it['path']).stem}"[:60], font=f, fill="white")
    out.save(dest / name, quality=88)


sheet([i for i in items if i["orientation"] == "landscape"], "overview-landscape.jpg", (960, 540), 2)
sheet([i for i in items if i["orientation"] == "portrait"], "overview-portrait.jpg", (480, 853), 4)
