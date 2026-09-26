"""Mechanical checks for the delivered covers; prints one line per file and a summary."""
import json
import sys
from pathlib import Path

from PIL import Image

OUT = Path(r"D:\agent-thumbnail\outputs\aomi-debut-20260731")
ROOT = Path(__file__).parent
audit = json.loads((ROOT / "timeline-audit.json").read_text(encoding="utf-8"))
names = [t["name"] for t in audit["timelines"]]
items = json.loads((OUT / "delivery-manifest.json").read_text(encoding="utf-8"))
MARGIN = 40
problems = []
expected = {f"{n}.jpg" for n in names} | {f"{n}-short.jpg" for n in names}
on_disk = {p.name for p in (OUT / "jpg").glob("*.jpg")}
if on_disk != expected:
    problems.append(f"file set mismatch: missing={sorted(expected - on_disk)} extra={sorted(on_disk - expected)}")
small = ROOT / "small"
small.mkdir(exist_ok=True)
for it in items:
    p = Path(it["path"])
    w, h = it["size"]
    with Image.open(p) as im:
        im.load()
        fmt, size, mode = im.format, im.size, im.mode
        thumb = im.convert("RGB")
        thumb.thumbnail((320, 180) if w > h else (180, 320), Image.Resampling.LANCZOS)
        thumb.save(small / p.name, quality=90)
    msgs = []
    if fmt != "JPEG" or size != (w, h) or mode != "RGB":
        msgs.append(f"format {fmt} {size} {mode}")
    for key in ("hook_ink", "secondary_ink"):
        x0, y0, x1, y1 = it[key]
        if x0 < MARGIN or y0 < MARGIN or x1 > w - MARGIN or y1 > h - MARGIN:
            msgs.append(f"{key} outside {MARGIN}px margin: {it[key]}")
    mx0, my0, mx1, my1 = it["model_box"]
    for key in ("hook_ink", "secondary_ink"):
        x0, y0, x1, y1 = it[key]
        if x0 < mx1 and x1 > mx0 and y0 < my1 and y1 > my0:
            msgs.append(f"{key} overlaps model bbox {it['model_box']}")
    if it["orientation"] == "portrait":
        cx = (mx0 + mx1) / 2
        if abs(cx - w / 2) > 3 or mx0 < 0 or mx1 > w:
            msgs.append(f"model not centred/inside: centre {cx}")
        if my0 < h / 2:
            msgs.append(f"model top {my0} above the lower half")
        for key in ("hook_ink", "secondary_ink"):
            c = (it[key][0] + it[key][2]) / 2
            if abs(c - w / 2) > 6:
                msgs.append(f"{key} not horizontally centred: {c}")
    if it["hook_font"] <= it["secondary_font"]:
        msgs.append("hook not larger than secondary")
    stem = p.stem[:-6] if p.stem.endswith("-short") else p.stem
    if stem not in names:
        msgs.append("file name is not a timeline name")
    status = "OK " if not msgs else "BAD"
    print(status, p.name, size, f"{p.stat().st_size // 1024}KB", "; ".join(msgs))
    problems += [f"{p.name}: {m}" for m in msgs]
print("SUMMARY:", "PASS" if not problems else f"{len(problems)} problem(s)")
for m in problems:
    print("  -", m)
sys.exit(1 if problems else 0)
