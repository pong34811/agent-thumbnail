"""Evidence-based KATY404 cover renderer; no source media or Resolve mutations.

Run from any directory with a Pillow/RAQM-enabled Python:
  python render_covers.py --selection selection.json [--only 1,12,30] [--format portrait]
  python render_covers.py --check-environment
"""
from __future__ import annotations

import argparse
import io
import json
import math
import os
import re
import sys
from pathlib import Path

# Pillow's Windows RAQM build dynamically loads FriBiDi. Keep its search handle
# alive for the entire render and load task-local DLLs before importing Pillow.
RUNTIME = Path(__file__).resolve().parent / "runtime"
DLL_DIRECTORY = os.add_dll_directory(str(RUNTIME)) if os.name == "nt" and RUNTIME.is_dir() else None
if DLL_DIRECTORY:
    import ctypes
    for dll_name in ("fribidi.dll", "libfribidi-0.dll"):
        if (RUNTIME / dll_name).is_file():
            ctypes.WinDLL(str(RUNTIME / dll_name))

import numpy as np
from PIL import Image, ImageChops, ImageCms, ImageDraw, ImageFilter, features

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from src.engine.text_thai import get_font, line_masks, resolve_font_path, text_box
from src.engine.graphics import create_backdrop_gradient, draw_hand_drawn_circle
from src.engine.shorts_titles import (
    canonical_title_from_timeline,
    fit_single_line_size,
    validate_title_parts,
)

OUT = Path(__file__).resolve().parent
RED = (236, 28, 36)
MAX_BYTES = 2 * 1024 * 1024


def environment():
    font = resolve_font_path()
    if not font:
        raise RuntimeError("Mitr Bold is missing; set THUMBNAIL_FONT_PATH to Mitr-Bold.ttf")
    if not features.check("raqm"):
        raise RuntimeError("Pillow requires real RAQM support; fallback Thai rendering is forbidden")
    f = get_font(100, str(font))
    if f.layout_engine != ImageFontLayoutRAQM():
        raise RuntimeError("Font did not load using RAQM")
    family, style = f.getname()
    if "Mitr" not in family or "Bold" not in style:
        raise RuntimeError(f"Expected Mitr Bold; received {family} {style}")
    return str(font)


def ImageFontLayoutRAQM():
    from PIL import ImageFont
    return ImageFont.Layout.RAQM


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def filename(name):
    # Preserve the actual timeline spelling; only Windows-invalid characters change.
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).rstrip(" .") + ".jpg"


def validate(row):
    required = ("index", "hook_lines", "secondary_lines", "source_path",
                "source_time_seconds", "frame_path", "avatar_file", "rationale", "caveats",
                "portrait_clip_title", "portrait_title_red", "portrait_title_white")
    missing = [k for k in required if k not in row]
    if missing:
        raise ValueError(f"Selection missing fields {missing}")
    if type(row["index"]) is not int or not 1 <= row["index"] <= 30:
        raise ValueError("Selection index must be integer 1–30")
    for key in ("hook_lines", "secondary_lines"):
        if not isinstance(row[key], list) or any(not isinstance(x, str) or not x.strip() for x in row[key]):
            raise ValueError(f"{key} must contain nonempty strings")
        if len(row[key]) > 2 or (key == "hook_lines" and not row[key]):
            raise ValueError(f"{key} allows at most two lines (hook is required)")
    validate_title_parts(row["portrait_clip_title"], row["portrait_title_red"], row["portrait_title_white"])
    if not isinstance(row["source_time_seconds"], (float, int)) or not math.isfinite(row["source_time_seconds"]) or row["source_time_seconds"] < 0:
        raise ValueError("Invalid source time")
    for key in ("source_path", "frame_path", "avatar_file"):
        p = Path(row[key])
        if not p.is_absolute() or not p.is_file():
            raise FileNotFoundError(f"{key} must be an existing absolute file: {p}")
    if "gameplay_crop" in row:
        c = row["gameplay_crop"]
        if len(c) != 4 or not all(0 <= x <= 1 for x in c) or c[0] >= c[2] or c[1] >= c[3]:
            raise ValueError("gameplay_crop must be normalized [left,top,right,bottom]")
    if "focus_point" in row and (len(row["focus_point"]) != 2 or not all(0 <= x <= 1 for x in row["focus_point"])):
        raise ValueError("focus_point must be normalized [x,y]")


def source_crop(frame, row, size):
    """Crop source aspect-preservingly, returning original-source crop coordinates."""
    fw, fh = frame.size
    c = row.get("gameplay_crop", [0, 0, 1, 1])
    l, t, r, b = c[0] * fw, c[1] * fh, c[2] * fw, c[3] * fh
    cw, ch = r - l, b - t
    aspect = size[0] / size[1]
    if cw / ch > aspect:
        cw = ch * aspect
    else:
        ch = cw / aspect
    fx, fy = row.get("focus_point", [(l + r) / (2 * fw), (t + b) / (2 * fh)])
    l = max(l, min(fx * fw - cw / 2, r - cw))
    t = max(t, min(fy * fh - ch / 2, b - ch))
    box = (round(l), round(t), round(l + cw), round(t + ch))
    return frame.crop(box).resize(size, Image.Resampling.LANCZOS), box


def one_line(text, size, color, font_path):
    """Use Thai collision clearing on a small local layer, then crop actual ink."""
    font = get_font(size, font_path)
    stroke = max(3, round(size * .08))
    box = text_box(text, font, stroke)
    pad = size // 2 + stroke + 4
    dims = (box[2] - box[0] + 2 * pad, box[3] - box[1] + 2 * pad)
    sm, fm = line_masks(dims, (pad - box[0], pad - box[1]), text, font, "ls", stroke)
    s = Image.fromarray(np.clip(sm, 0, 255).astype(np.uint8))
    f = Image.fromarray(np.clip(fm, 0, 255).astype(np.uint8))
    layer = Image.new("RGBA", dims, (0, 0, 0, 255))
    layer.putalpha(s)
    fill = Image.new("RGBA", dims, (*color, 255))
    fill.putalpha(f)
    layer.alpha_composite(fill)
    ink = layer.getchannel("A").getbbox()
    if not ink:
        raise ValueError(f"Text has no visible ink: {text}")
    return layer.crop(ink)


def text_block(lines, max_width, max_height, start_size, color, font_path):
    if not lines:
        return None, None
    # Fitting checks standard RAQM bounds before expensive collision-clearing masks.
    for size in range(start_size, 39, -2):
        font = get_font(size, font_path)
        stroke = max(3, round(size * .08))
        boxes = [text_box(s, font, stroke) for s in lines]
        gap = round(size * .12)
        if max(b[2] - b[0] for b in boxes) > max_width or sum(b[3] - b[1] for b in boxes) + gap * (len(lines) - 1) > max_height:
            continue
        layers = [one_line(s, size, color, font_path) for s in lines]
        w = max(x.width for x in layers)
        h = sum(x.height for x in layers) + gap * (len(layers) - 1)
        if w > max_width or h > max_height:
            continue
        block = Image.new("RGBA", (w, h))
        y = 0
        for layer in layers:
            block.alpha_composite(layer, ((w - layer.width) // 2, y))
            y += layer.height + gap
        return block, size
    raise ValueError(f"Text cannot fit safely and readably: {lines}")


def fit_title_line(text, max_width, preferred_size, minimum_size, color, font_path):
    if not text:
        return None, None

    def measure(value, size):
        stroke = max(3, round(size * .08))
        box = text_box(value, get_font(size, font_path), stroke)
        return box[2] - box[0]

    size = fit_single_line_size(text, max_width, preferred_size, minimum_size, measure)
    if size is None:
        raise ValueError(f"Title line cannot fit in {minimum_size}–{preferred_size}px: {text!r}")
    return one_line(text, size, color, font_path), size


def fit_title_pair(red_text, white_text, font_path, max_width=756, max_height=315):
    red_sizes = (100,)  # uniform red title size across all Shorts covers
    white_sizes = range(90, 59, -2) if white_text else (None,)
    red_metrics = {}
    for size in red_sizes:
        stroke = max(3, round(size * .08))
        box = text_box(red_text, get_font(size, font_path), stroke)
        red_metrics[size] = (box[2] - box[0], box[3] - box[1])
    white_metrics = {}
    for size in white_sizes:
        if size:
            stroke = max(3, round(size * .08))
            box = text_box(white_text, get_font(size, font_path), stroke)
            white_metrics[size] = (box[2] - box[0], box[3] - box[1])
    candidates = []
    for red_size in red_sizes:
        red_width, red_height = red_metrics[red_size]
        if red_width > max_width * 1.02:
            continue
        for white_size in white_sizes:
            if white_size:
                white_width, white_height = white_metrics[white_size]
                if white_width > max_width * 1.02:
                    continue
            else:
                white_height = 0
            block_height = red_height + (22 + white_height if white_size else 0)
            if block_height > max_height:
                continue
            score = ((red_size - 100) / 50) + (((white_size - 60) / 30) if white_size else 0)
            candidates.append((score, red_size, white_size or 0))
    if not candidates:
        raise ValueError("Title lines cannot fit the portrait text zone within approved font ranges")
    _, red_size, white_size = max(candidates, key=lambda c: (c[0], c[1], c[2]))
    red_layer = one_line(red_text, red_size, RED, font_path)
    if red_layer.width > max_width:
        red_layer = red_layer.resize((max_width, red_layer.height), Image.Resampling.LANCZOS)
    white_layer = one_line(white_text, white_size, (255, 255, 255), font_path) if white_size else None
    if white_layer and white_layer.width > max_width:
        white_layer = white_layer.resize((max_width, white_layer.height), Image.Resampling.LANCZOS)
    return red_layer, red_size, white_layer, white_size or None


def avatar_layer(path, max_size):
    with Image.open(path) as im:
        av = im.convert("RGBA")
    bounds = av.getchannel("A").getbbox()
    if not bounds or av.getchannel("A").getextrema()[0] == 255:
        raise ValueError("Avatar must have real transparent alpha and visible content")
    av = av.crop(bounds)
    scale = min(max_size[0] / av.width, max_size[1] / av.height)
    av = av.resize((max(1, round(av.width * scale)), max(1, round(av.height * scale))), Image.Resampling.LANCZOS)
    pad = 44
    result = Image.new("RGBA", (av.width + 2 * pad, av.height + 2 * pad))
    alpha = Image.new("L", result.size)
    alpha.paste(av.getchannel("A"), (pad, pad))
    # Keep a clean VTuber rim without making the model read like a floating sticker.
    accent = alpha.filter(ImageFilter.MaxFilter(7))
    white = alpha.filter(ImageFilter.MaxFilter(5))
    shadow_mask = accent.filter(ImageFilter.GaussianBlur(13)).point(lambda x: round(x * .75))
    shadow = Image.new("RGBA", result.size, (0, 0, 0, 255))
    shadow.putalpha(shadow_mask)
    result.alpha_composite(shadow, (8, 10))
    for mask, color in ((accent, (32, 65, 82)), (white, (255, 255, 255))):
        rim = Image.new("RGBA", result.size, (*color, 255))
        rim.putalpha(mask)
        result.alpha_composite(rim)
    result.alpha_composite(av, (pad, pad))
    # Content bounds deliberately exclude decorative shadow, but include ears/hands.
    return result, (pad, pad, pad + av.width, pad + av.height), list(bounds)


def place(canvas, layer, center_x, top):
    if layer is None:
        return None
    x = round(center_x - layer.width / 2)
    canvas.alpha_composite(layer, (x, top))
    return [x, top, x + layer.width, top + layer.height]


def add_contact_shadow(canvas, avatar_bbox, portrait):
    """Anchor the cutout to a soft, scene-colored contact point at its lower edge."""
    left, top, right, bottom = avatar_bbox
    width = right - left
    cx = round((left + right) / 2)
    broad = Image.new("L", canvas.size)
    draw = ImageDraw.Draw(broad)
    broad_h = 30 if portrait else 26
    draw.ellipse((left + width * .06, bottom - 10, right - width * .06, bottom + broad_h), fill=165)
    broad = broad.filter(ImageFilter.GaussianBlur(12 if portrait else 10))
    contact = Image.new("L", canvas.size)
    draw = ImageDraw.Draw(contact)
    contact_h = 9 if portrait else 7
    draw.ellipse((left + width * .10, bottom - 3, right - width * .10, bottom + contact_h), fill=185)
    contact = contact.filter(ImageFilter.GaussianBlur(3))
    mask = ImageChops.lighter(broad, contact)
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 255))
    shadow.putalpha(mask)
    canvas.alpha_composite(shadow)


def intersects(a, b):
    return bool(a and b and max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3]))


def render(row, portrait, font_path):
    size = (1080, 1920) if portrait else (1920, 1080)
    with Image.open(row["frame_path"]) as im:
        frame = im.convert("RGB")
    bg, crop = source_crop(frame, row, size)
    canvas = bg.convert("RGBA")
    if portrait:
        # Original footage is independently cropped; sharp evidence window preserves context.
        canvas.alpha_composite(Image.new("RGBA", size, (4, 8, 20, 100)))
        evidence, evidence_crop = source_crop(frame, row, (860, 250))
        canvas.paste(evidence, (45, 45))
        validate_title_parts(
            row["portrait_clip_title"], row["portrait_title_red"], row["portrait_title_white"]
        )
        hook, hs, secondary, ss = fit_title_pair(
            row["portrait_title_red"], row["portrait_title_white"], font_path
        )
        hb = place(canvas, hook, 540, 585)
        sb = place(canvas, secondary, 540, hb[3] + 22) if secondary else None
        if sb and sb[3] > 970:
            raise ValueError("Portrait title lines extend below y970")
        portrait_avatar_file = row.get("portrait_avatar_file", row["avatar_file"])
        # Use the current high-resolution character art, enlarged and centered.
        # Crop the torso below the frame edge to remove the floating sticker baseline.
        avatar, inner, alpha_crop = avatar_layer(portrait_avatar_file, (920, 900))
        x, y = round(540 - avatar.width / 2), 2130 - inner[3]
        # Keep the lower control region visually quiet without blurring game pixels.
        bottom_mask = Image.new("L", size)
        bd = ImageDraw.Draw(bottom_mask)
        for scan_y in range(1380, size[1]):
            bd.line((0, scan_y, size[0], scan_y), fill=round(205 * min(1, (scan_y - 1380) / 300)))
        bottom = Image.new("RGBA", size, (4, 8, 20, 255))
        bottom.putalpha(bottom_mask)
        canvas.alpha_composite(bottom)
    else:
        evidence_crop = None
        canvas.alpha_composite(create_backdrop_gradient(size, 40, 1090, .66))
        hook, hs = text_block(row["hook_lines"], 940, 270, 188, RED, font_path)
        secondary, ss = text_block(row["secondary_lines"], 940, 165, 100, (255, 255, 255), font_path)
        total = hook.height + (secondary.height + 24 if secondary else 0)
        top = max(330, round(490 - total / 2))
        hb = place(canvas, hook, 510, top)
        sb = place(canvas, secondary, 510, hb[3] + 24)
        # Let the lower torso run past the frame edge. This removes the floating
        # cutout baseline while keeping the face away from YouTube's duration badge.
        avatar, inner, alpha_crop = avatar_layer(row["avatar_file"], (740, 815))
        x, y = 1725 - inner[2], 1096 - inner[3]
    ab = [x + inner[0], y + inner[1], x + inner[2], y + inner[3]]
    if not portrait:
        add_contact_shadow(canvas, ab, portrait)
    canvas.alpha_composite(avatar, (x, y))
    boxes = {"hook": hb, "secondary": sb, "avatar": ab}
    violations = []
    for key, b in boxes.items():
        if b is None:
            continue
        max_right = (980 if key == "avatar" else 918) if portrait else (1760 if key == "avatar" else 1880)
        max_bottom = (2140 if key == "avatar" else 1700) if portrait else (1120 if key == "avatar" else 960)
        if b[0] < 40 or b[1] < 40 or b[2] > max_right or b[3] > max_bottom:
            violations.append(f"{key} outside declared safe zone")
    if intersects(hb, ab) or intersects(sb, ab):
        violations.append("text/avatar bounds collide")
    if intersects(hb, sb):
        violations.append("hook/secondary bounds collide")
    if violations:
        raise ValueError(f"Selection {row['index']}: {violations}")
    # Circle is opt-in and appears only if it avoids all principal content bounds.
    circle = None
    if not portrait and row.get("focus_radius") and row.get("focus_point"):
        fx, fy = row["focus_point"]
        cx = round((fx * frame.width - crop[0]) / (crop[2] - crop[0]) * size[0])
        cy = round((fy * frame.height - crop[1]) / (crop[3] - crop[1]) * size[1])
        radius = round(float(row["focus_radius"]) * size[0])
        circle_bounds = [cx - radius - 20, cy - radius - 20, cx + radius + 20, cy + radius + 20]
        if radius > 0 and circle_bounds[0] >= 20 and circle_bounds[1] >= 20 and circle_bounds[2] < size[0]-20 and circle_bounds[3] < 950 and not any(intersects(circle_bounds, b) for b in boxes.values()):
            draw_hand_drawn_circle(canvas, (cx, cy), radius, stroke_width=9)
            circle = circle_bounds
    return canvas.convert("RGB"), {
        "safe_text_bbox": {"hook": hb, "secondary": sb}, "safe_avatar_bbox": ab,
        "text_font_sizes": {"hook": hs, "secondary": ss}, "text_stroke_ratio": .08,
        "gameplay_source_crop_pixels": list(crop), "evidence_window_source_crop_pixels": list(evidence_crop) if evidence_crop else None,
        "avatar_source_alpha_crop_pixels": alpha_crop, "circle_bbox": circle,
        "avatar_contact_shadow": not portrait, "avatar_rim": "slim white rim with muted teal outer edge",
        "avatar_anchor": "frame-bottom crop" if not portrait else "centered enlarged bottom-edge crop",
        "avatar_crop_bottom_px": max(0, ab[3] - size[1]),
        "geometry_pass": True, "violations": violations,
        "avatar_width_fraction": round((ab[2] - ab[0]) / size[0], 3),
    }


def save_jpeg(image, path, icc):
    for quality in (95, 93, 91, 89, 87, 85, 82, 78):
        buf = io.BytesIO()
        image.save(buf, "JPEG", quality=quality, optimize=True, subsampling=0, icc_profile=icc)
        if buf.tell() <= MAX_BYTES:
            Path(path).write_bytes(buf.getvalue())
            return quality, buf.tell()
    raise ValueError(f"Cannot export JPEG below 2MB: {path}")


def previews_and_sheets(manifest, font_path):
    directory = OUT / "previews"
    directory.mkdir(exist_ok=True)
    for portrait in (False, True):
        entries = [m for m in manifest if (m["height"] > m["width"]) == portrait]
        tile = (180, 320) if portrait else (320, 180)
        cols, per_page = (5, 10) if portrait else (3, 12)
        for start in range(0, len(entries), per_page):
            page_entries = entries[start:start + per_page]
            sheet = Image.new("RGB", (cols * (tile[0] + 20) + 20, math.ceil(len(page_entries) / cols) * (tile[1] + 44) + 20), (22, 25, 31))
            draw = ImageDraw.Draw(sheet)
            for offset, entry in enumerate(page_entries):
                with Image.open(OUT / "jpg" / entry["filename"]) as im:
                    thumb = im.resize(tile, Image.Resampling.LANCZOS)
                ident = f"{entry['timeline_index']:02d}"
                thumb.save(directory / f"{ident}-{entry['format']}.jpg", quality=93)
                thumb.convert("L").save(directory / f"{ident}-{entry['format']}-gray.jpg", quality=93)
                x, y = 20 + offset % cols * (tile[0] + 20), 20 + offset // cols * (tile[1] + 44)
                sheet.paste(thumb, (x, y))
                label = f"#{ident} {entry['selection_index']:02d} / {'Shorts' if portrait else 'Landscape'}"
                draw.text((x, y + tile[1] + 5), label, font=get_font(16, font_path), fill="white")
            sheet.save(directory / f"contact-{'portrait' if portrait else 'landscape'}-{start // per_page + 1:02d}.jpg", quality=95)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, default=OUT / "selection.json")
    parser.add_argument("--only", help="Comma-separated paired selection indices")
    parser.add_argument("--format", choices=("both", "portrait", "landscape"), default="both",
                        help="Which timeline format to render; portrait-only preserves landscape files")
    parser.add_argument("--check-environment", action="store_true")
    args = parser.parse_args()
    font_path = environment()
    if args.check_environment:
        print(json.dumps({"font": font_path, "raqm": True, "python": sys.executable}))
        return
    rows = load_json(args.selection)
    if not isinstance(rows, list):
        raise ValueError("selection.json must be a list")
    by_index = {}
    for row in rows:
        validate(row)
        if row["index"] in by_index:
            raise ValueError("Duplicate selection index")
        by_index[row["index"]] = row
    if set(by_index) != set(range(1, 31)):
        raise ValueError("Selection must cover exactly all 30 landscape indices")
    timelines = load_json(OUT / "audit" / "live-timeline-audit.json")["result"]["timelines"]
    if len(timelines) != 60:
        raise ValueError("Expected exactly 60 live timelines")
    by_name = {t["name"]: t for t in timelines}
    landscapes = {t["index"]: t for t in timelines if (int(t["width"]), int(t["height"])) == (1920, 1080)}
    if set(landscapes) != set(by_index):
        raise ValueError("Live landscape indices differ from selection")
    paired = {}
    for index, timeline in landscapes.items():
        twin = by_name.get(timeline["name"] + "_9x16")
        if not twin or (int(twin["width"]), int(twin["height"])) != (1080, 1920):
            raise ValueError(f"Missing exact portrait pair for {timeline['name']}")
        paired[index] = twin
        if by_index[index]["portrait_clip_title"] != canonical_title_from_timeline(twin["name"]):
            raise ValueError(f"Selection {index}: title differs from paired timeline {twin['name']}")
        expected_sources = {os.path.normcase(str(Path(c["source"]))) for track in timeline["tracks"]
                            if track["kind"] == "video" and track["number"] == 1
                            for c in track["clips"] if c.get("source")}
        if os.path.normcase(str(Path(by_index[index]["source_path"]))) not in expected_sources:
            raise ValueError(f"Selection {index} source differs from live primary video track")
    requested = set(map(int, args.only.split(","))) if args.only else set(by_index)
    if not requested or not requested <= set(by_index):
        raise ValueError("--only indices must be 1–30")
    selected_formats = [False, True] if args.format == "both" else [args.format == "portrait"]
    manifest_path = OUT / "delivery-manifest.json"
    partial_render = args.only is not None or args.format != "both"
    if partial_render and not manifest_path.exists():
        raise ValueError("Partial rendering requires an existing complete delivery manifest")
    existing = load_json(manifest_path) if partial_render else []
    replaced_formats = {"landscape", "portrait"} if args.format == "both" else {args.format}
    manifest = [
        x for x in existing
        if not (x["selection_index"] in requested and x["format"] in replaced_formats)
    ]
    (OUT / "jpg").mkdir(exist_ok=True)
    icc = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    for index in sorted(requested):
        row = by_index[index]
        timeline_pairs = ((False, landscapes[index]), (True, paired[index]))
        for portrait, timeline in (pair for pair in timeline_pairs if pair[0] in selected_formats):
            image, geometry = render(row, portrait, font_path)
            name = filename(timeline["name"])
            quality, byte_count = save_jpeg(image, OUT / "jpg" / name, icc)
            hook_lines = [row["portrait_title_red"]] if portrait else row["hook_lines"]
            secondary_lines = ([row["portrait_title_white"]] if portrait and row["portrait_title_white"] else
                               ([] if portrait else row["secondary_lines"]))
            entry = {
                "filename": name, "timeline_name": timeline["name"], "timeline_index": timeline["index"],
                "selection_index": index, "index": timeline["index"],
                "format": "portrait" if portrait else "landscape", "width": image.width, "height": image.height,
                "dimensions": list(image.size), "hook": hook_lines, "secondary": secondary_lines,
                "timeline_fps": timeline["fps"],
                "source": row["source_path"], "source_path": row["source_path"], "source_time_seconds": row["source_time_seconds"],
                "avatar": row.get("portrait_avatar_file", row["avatar_file"]) if portrait else row["avatar_file"], "source_evidence": {"frame_path": row["frame_path"], "rationale": row["rationale"], "caveats": row["caveats"]},
                "font": font_path, "raqm": True, "color_profile": "sRGB", "jpeg_quality": quality, "bytes": byte_count,
                **geometry,
            }
            if portrait:
                entry.update({
                    "clip_title": row["portrait_clip_title"],
                    "title_lines": {"red": row["portrait_title_red"], "white": row["portrait_title_white"]},
                })
            manifest.append(entry)
            print(f"Rendered {timeline['index']:02d}: {name}", flush=True)
    manifest.sort(key=lambda x: x["timeline_index"])
    if {m["timeline_name"] for m in manifest} != set(by_name) or len(manifest) != 60:
        raise ValueError("Output scope differs from live inventory")
    if len({m["filename"] for m in manifest}) != len(manifest):
        raise ValueError("Sanitized filenames collide")
    write_json(manifest_path, manifest)
    write_json(OUT / "geometry-report.json", {"pass": all(m["geometry_pass"] for m in manifest), "count": len(manifest), "covers": [{k: v for k, v in m.items() if k in ("timeline_index", "timeline_name", "safe_text_bbox", "safe_avatar_bbox", "geometry_pass", "violations", "avatar_width_fraction")} for m in manifest]})
    previews_and_sheets(manifest, font_path)
    print(f"Manifest: {manifest_path} ({len(manifest)} covers)")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)








