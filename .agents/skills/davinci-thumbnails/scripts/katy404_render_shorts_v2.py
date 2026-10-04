"""KATY404 Shorts v2: crisp gameplay window, hook on top, face above the feed UI.

  python render_shorts_v2.py [--only 1,14,30] [--data <delivery folder>]
Reads selection.json + audit/ from the delivery folder (render_covers.py lives there too)
and writes ./jpg-shorts-v2 inside it; the original jpg/ folder is left untouched.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_DATA = Path(__file__).resolve().parents[4] / "outputs" / "2026-10-04" / "Katy404-2026-09-29"
_pre = argparse.ArgumentParser(add_help=False)
_pre.add_argument("--data", default=str(DEFAULT_DATA))
DATA = Path(_pre.parse_known_args()[0].data)
sys.path.insert(0, str(DATA))
sys.path.insert(0, str(DATA.parents[2]))  # repo root that holds src/engine/shorts_titles.py

import render_covers as rc  # noqa: E402  (loads task-local fribidi runtime)
from PIL import Image, ImageCms, ImageDraw, ImageFilter  # noqa: E402
from src.engine.text_thai import text_box  # noqa: E402

W, H = 1080, 1920
TEXT_W = 960
TITLE_TOP = 290
WIN = (30, 650, 1050, 1150)          # crisp gameplay window (1020x500)
AVATAR_W = 900
AVATAR_TOP = 975                    # head overlaps window edge; torso bleeds off the bottom
OUT = DATA / "jpg-shorts-v2"


def uniform_red_size(rows, font_path):
    for size in range(150, 99, -2):
        stroke = max(3, round(size * .08))
        widest = max(
            (lambda b: b[2] - b[0])(text_box(r["portrait_title_red"], rc.get_font(size, font_path), stroke))
            for r in rows
        )
        if widest <= TEXT_W:
            return size
    raise ValueError("red lines cannot share one size >= 100")


def white_layer(text, font_path):
    for size in range(96, 59, -2):
        stroke = max(3, round(size * .08))
        b = text_box(text, rc.get_font(size, font_path), stroke)
        if b[2] - b[0] <= TEXT_W:
            return rc.one_line(text, size, (255, 255, 255), font_path), size
    raise ValueError(f"white line too wide at 60px: {text}")


def render(row, red_size, font_path):
    with Image.open(row["frame_path"]) as im:
        frame = im.convert("RGB")
    # decorative fill only: darkened + soft; the gameplay itself stays unblurred below
    bg = frame.crop((0, 0, round(frame.width * .74), frame.height)).resize((W, H), Image.Resampling.BILINEAR)
    bg = bg.filter(ImageFilter.GaussianBlur(28))
    canvas = Image.blend(bg, Image.new("RGB", (W, H), (6, 9, 22)), .68).convert("RGBA")

    win_size = (WIN[2] - WIN[0], WIN[3] - WIN[1])
    crop, src_box = rc.source_crop(frame, row, win_size)
    card = Image.new("RGBA", (win_size[0] + 12, win_size[1] + 12), (255, 255, 255, 255))
    card.paste(crop, (6, 6))
    shadow = Image.new("RGBA", (card.width + 80, card.height + 80), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle((40, 48, 40 + card.width, 48 + card.height), fill=(0, 0, 0, 190))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.alpha_composite(shadow, (WIN[0] - 46, WIN[1] - 46))
    canvas.alpha_composite(card, (WIN[0] - 6, WIN[1] - 6))

    # hook (red) + rest of the clip title (white), one visual line per colour
    rc.validate_title_parts(row["portrait_clip_title"], row["portrait_title_red"], row["portrait_title_white"])
    red = rc.one_line(row["portrait_title_red"], red_size, rc.RED, font_path)
    white_text = row["portrait_title_white"].strip()
    wl, ws = white_layer(white_text, font_path) if white_text else (None, None)
    block = red.height + (20 + wl.height if wl else 0)
    top = max(285, round(285 + (WIN[1] - 20 - 285 - block) / 2))  # centre inside the 4:5-safe text zone
    hb = rc.place(canvas, red, 540, top)
    sb = rc.place(canvas, wl, 540, hb[3] + 20) if wl else None
    limit = WIN[1] - 20
    if (sb or hb)[3] > limit:
        raise ValueError(f"#{row['index']} title block reaches y{(sb or hb)[3]} > {limit}")

    # model: half-body, centred, head overlapping the window edge, torso bleeds off the bottom
    av, inner, _ = rc.avatar_layer(row.get("portrait_avatar_file", row["avatar_file"]), (AVATAR_W, 2000))
    ax = round(540 - av.width / 2)
    ay = AVATAR_TOP - inner[1]
    scrim = Image.new("L", (W, H))
    d = ImageDraw.Draw(scrim)
    for y in range(1500, H):
        d.line((0, y, W, y), fill=round(170 * min(1, (y - 1500) / 300)))
    bottom = Image.new("RGBA", (W, H), (4, 8, 20, 255))
    bottom.putalpha(scrim)
    canvas.alpha_composite(av, (ax, ay))
    canvas.alpha_composite(bottom)
    ab = [ax + inner[0], ay + inner[1], ax + inner[2], ay + inner[3]]
    geo = {
        "hook_bbox": hb, "secondary_bbox": sb, "window": list(WIN), "avatar_bbox": ab,
        "font_sizes": {"red": red_size, "white": ws}, "gameplay_source_crop": list(src_box),
        "gameplay_scale": round(win_size[0] / (src_box[2] - src_box[0]), 3),
    }
    return canvas.convert("RGB"), geo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--data", default=str(DEFAULT_DATA))
    args = ap.parse_args()
    font_path = rc.environment()
    rows = rc.load_json(DATA / "selection.json")
    audit = rc.load_json(DATA / "audit" / "live-timeline-audit.json")["result"]["timelines"]
    names = {t["index"]: t["name"] for t in audit if (int(t["width"]), int(t["height"])) == (1920, 1080)}
    only = {int(x) for x in args.only.split(",") if x}
    red_size = uniform_red_size(rows, font_path)
    icc = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    OUT.mkdir(exist_ok=True)
    manifest = []
    for row in rows:
        if only and row["index"] not in only:
            continue
        img, geo = render(row, red_size, font_path)
        name = rc.filename(names[row["index"]] + "_9x16")
        q, nbytes = rc.save_jpeg(img, OUT / name, icc)
        manifest.append({"index": row["index"], "file": name, "bytes": nbytes, "quality": q,
                         "title": row["portrait_clip_title"], "source_frame": row["frame_path"], **geo})
        print(row["index"], name, nbytes, geo["font_sizes"], geo["gameplay_scale"])
    (OUT / "shorts-v2-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf8")


if __name__ == "__main__":
    main()
