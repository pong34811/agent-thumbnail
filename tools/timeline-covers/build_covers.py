"""Build KATY404-style covers for the 8 timelines of 【DEBUT STREAM】AOMI-MAMA.

One 1920x1080 cover per timeline plus a 1080x1920 Shorts cover ("-short").
Hook = red Mitr Bold with black outline, secondary = white Mitr Bold with black
outline. Text is taken from each timeline's own subtitles / Text+ captions.
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).parent
OUT = Path(r"D:\agent-thumbnail\outputs\aomi-debut-20260731")
JPG = OUT / "jpg"
FONT = r"D:\agent-thumbnail\outputs\timeline-covers\fonts\Mitr-Bold.ttf"
MODELS = ROOT / "models"
RED = (236, 28, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Per timeline: hook/secondary lines per orientation, model file, background
# source + crop (x0, y0, x1, y1 in that source) for each orientation.
# Evidence = the timeline cues the wording comes from.
TL = {
    1: dict(model="vts_2026-07-02_20-33-46.png", mood="หัวเราะขณะเล่าว่าตกใจจนปิดไลฟ์หนี",
            evidence="มีคนเข้ามาในไลฟ์หนู | วันนั้นคนแรก | เข้ามา | หนูตกใจมาก | แล้วก็ปิดไลฟ์หนี",
            land=dict(sec=["คนแรกเข้ามาในไลฟ์"], hook=["ปิดไลฟ์หนี"]),
            short=dict(sec=["คนแรกเข้ามาในไลฟ์"], hook=["ปิดไลฟ์หนี"]),
            # Cat Goes Fishing = the game on stream when the first viewer came in
            # (the still is placed on V2 of this timeline at that cue).
            bg="stills/Cat Goes Fishing.jpg", land_crop=(0, 0, 460, 215), short_crop=(150, 0, 271, 215)),
    2: dict(model="IMG_7135.PNG", mood="ยิ้มถือมีด (มุกจ้วงแทงข้างหลัง)",
            evidence="แล้วก็มันจวงแทง | คนจากข้างหลัง | ง่ายด้วย | ตัวเล็กมีประโยชน์นะ",
            land=dict(sec=["ตัวเล็กมีประโยชน์นะ"], hook=["จ้วงแทงคน", "จากข้างหลัง"]),
            short=dict(sec=["ตัวเล็กมีประโยชน์นะ"], hook=["จ้วงแทงคน", "จากข้างหลัง"]),
            bg="bg/tl2.png", land_crop=(700, 0, 1920, 686), short_crop=(700, 0, 1308, 1080)),
    3: dict(model="IMG_7132.PNG", mood="หงุดหงิด/บ่น",
            evidence="อ่านให้ฟังเลยน่าจะง่ายกว่า | ใครมันเขียน Text เนี้ย | ลิ้นไปหมดละ",
            land=dict(sec=["อ่านสตอรี่จนลิ้นไปหมด"], hook=["ใครมันเขียน", "Text เนี่ย"]),
            short=dict(sec=["อ่านสตอรี่จนลิ้นไปหมด"], hook=["ใครมันเขียน", "Text เนี่ย"]),
            bg="bg/tl3.png", land_crop=(700, 0, 1920, 686), short_crop=(760, 0, 1368, 1080)),
    4: dict(model="IMG_7137.PNG", mood="พนมมือ ขอร้อง/ขอบคุณตอนจบไลฟ์",
            evidence="ตอนเล่น LOL อย่าว่าผม | ผมไม่ค่อยเล่น | ไม่ค่อยเก่ง 55 | ขอบคุณสำหรับเวลา ... ฝันดีนะ (ชื่อ Timeline: จบไลฟ์เดบิวต์ เล่น LoL ไม่เก่งอย่าว่าหนูนะ)",
            land=dict(sec=["จบไลฟ์เดบิวต์", "เล่น LoL ไม่ค่อยเก่ง"], hook=["อย่าว่าหนูนะ"]),
            short=dict(sec=["จบไลฟ์เดบิวต์", "เล่น LoL ไม่ค่อยเก่ง"], hook=["อย่าว่าหนูนะ"]),
            bg="bg/tl4.png", land_crop=(560, 0, 1920, 765), short_crop=(900, 0, 1508, 1080)),
    5: dict(model="vts_2026-07-02_20-45-41.png", mood="หน้าเรียบ ๆ ไม่อิน", bust=1750,  # head sits low: longer crop shows the shirt
            evidence="เคยเล่นหรือเล่นอยู่มั้ยฮะ | ROV ไม่ | เคยเล่นอยุ่นะแต่ว่า | ไม่ได้ชอบอะ | มันเร็วไปสำหรับฉัน | เร็วเกิน | ไปหน่อย | ไม่ไหว",
            land=dict(sec=["ROV เคยเล่นอยู่นะ", "แต่ไม่ได้ชอบ"], hook=["เร็วเกิน", "ไปหน่อย"]),
            short=dict(sec=["ROV เคยเล่นอยู่นะ", "แต่ไม่ได้ชอบ"], hook=["เร็วเกิน", "ไปหน่อย"]),
            bg="bg/tl5.png", land_crop=(0, 60, 1250, 763), short_crop=(360, 0, 968, 1080)),
    6: dict(model="vts_2026-07-04_09-09-45.png", mood="ยิ้มอ่อน จริงใจ", short_bust=1250,  # wide hair: shorter crop keeps the face large
            evidence="หนูไม่เสียใจ | เลยนะตอนนี้ | ... | เพราะว่าหนูได้กลับมา | ทำสิ่งที่ | หนูชอบ | จริงจังอีกครั้งนึง",
            land=dict(sec=["ได้กลับมาทำ", "สิ่งที่ชอบอีกครั้ง"], hook=["หนูไม่เสียใจ"]),
            short=dict(sec=["ได้กลับมาทำสิ่งที่ชอบ", "อีกครั้ง"], hook=["หนูไม่เสียใจ"]),
            bg="bg/tl6.png", land_crop=(700, 0, 1920, 686), short_crop=(1150, 0, 1758, 1080)),
    7: dict(model="IMG_7136.PNG", mood="กำหมัด ฮึกเหิม",
            evidence="เป้าหมายของเรานะ | ก็เป็นเป้าหมายตั้งต้นนะ | คือ ผู้ติดตาม 1000 คน",
            land=dict(sec=["เป้าหมายตั้งต้นของเรา"], hook=["ผู้ติดตาม", "1,000 คน"]),
            short=dict(sec=["เป้าหมายตั้งต้นของเรา"], hook=["ผู้ติดตาม", "1,000 คน"]),
            bg="bg/tl7.png", land_crop=(700, 0, 1920, 686), short_crop=(1250, 0, 1858, 1080)),
    8: dict(model="IMG_7138.PNG", mood="ร้องไห้ กลัวแมลง",
            evidence="ตก | ลงไปใน | บึงแมลง | ... | หนูจำฝังใจ | จนถึงทุกวันเนี้ย",
            land=dict(sec=["จำฝังใจจนถึงทุกวันนี้"], hook=["ตกบึงแมลง"]),
            short=dict(sec=["จำฝังใจจนถึงทุกวันนี้"], hook=["ตกบึงแมลง"]),
            bg="bg/tl8.png", land_crop=(700, 0, 1920, 686), short_crop=(1312, 0, 1920, 1080)),
}

# --- Thai text rendering -----------------------------------------------------
# Mitr Bold sets some upper marks right against the ascender of ป ฝ ฟ (e.g. ั on
# ฝ, ์ on ฟ); a thick outline then fuses them. For every mark cluster on those
# consonants we find the mark at its real shaped position, and only if its fill
# is closer than MIN_GAP to the rest of the line we nudge it left until it
# clears. The build fails if a mark cannot be cleared.
TALL = {"ป": "บ", "ฝ": "ผ", "ฟ": "พ"}  # same advance, no ascender
UPPER = set("ัิีึื็่้๊๋์ํ")
MIN_GAP = 0.05  # em, fill gap kept between a mark and the ascender
PLACEMENTS = []  # (line, cluster, size, shaped offset vs twin, extra left shift) for the build log


def font(size):
    return ImageFont.truetype(FONT, size, layout_engine=ImageFont.Layout.RAQM)


def text_box(text, f, stroke):
    return ImageDraw.Draw(Image.new("L", (8, 8))).textbbox((0, 0), text, font=f, anchor="ls", stroke_width=stroke)


def fit(lines, max_w, start, minimum, stroke_ratio):
    size = start
    while size > minimum:
        f, stroke = font(size), max(4, round(size * stroke_ratio))
        if all(text_box(ln, f, stroke)[2] - text_box(ln, f, stroke)[0] <= max_w for ln in lines):
            return f, stroke
        size -= 2
    return font(minimum), max(4, round(minimum * stroke_ratio))


def _mask(size, xy, text, f, anchor, stroke=0):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).text(xy, text, font=f, fill=255, anchor=anchor, stroke_width=stroke, stroke_fill=255)
    return np.asarray(m, dtype=np.float32)


def _shift(a, dx, dy):
    out = np.zeros_like(a)
    h, w = a.shape
    out[max(0, dy):h + min(0, dy), max(0, dx):w + min(0, dx)] = a[max(0, -dy):h - max(0, dy), max(0, -dx):w - max(0, dx)]
    return out


def _dilate(a, r):
    """Round (disk) dilation of an anti-aliased mask by r px."""
    out = a.copy()
    for dy in range(-r, r + 1):
        span = int((r * r - dy * dy) ** 0.5)
        for dx in range(-span, span + 1):
            np.maximum(out, _shift(a, dx, dy), out=out)
    return out


def _base_of(text, i):
    """Index of the consonant a run of upper marks sits on."""
    j = i - 1
    while j >= 0 and text[j] in UPPER:
        j -= 1
    return j if j >= 0 else None


def line_masks(canvas_size, xy, text, f, anchor, stroke):
    """(stroke_mask, fill_mask) float arrays for one line with upper marks kept clear of ascending ink."""
    clusters = {}
    for i, ch in enumerate(text):
        if ch in UPPER and _base_of(text, i) is not None:
            clusters.setdefault(_base_of(text, i), []).append(i)
    if not clusters:
        return _mask(canvas_size, xy, text, f, anchor, stroke), _mask(canvas_size, xy, text, f, anchor)
    every = {i for v in clusters.values() for i in v}
    drop = lambda t, idx, twin_at=None: "".join(  # noqa: E731
        (TALL.get(ch, ch) if k == twin_at else ch) for k, ch in enumerate(t) if k not in idx)
    base_fill = _mask(canvas_size, xy, drop(text, every), f, anchor)
    fills, strokes = base_fill.copy(), _mask(canvas_size, xy, drop(text, every), f, anchor, stroke)
    need = max(4, round(f.size * MIN_GAP))        # clearance from ascending ink
    need_any = 1                                 # other ink: just must not touch
    # Ink above the x-height (tall-consonant ascenders, heads of ไ ใ โ) is what an
    # upper mark visually fuses with; measure that line from the top of "น".
    xh_top = xy[1] + text_box("น", f, 0)[1] - round(f.size * 0.04)
    for j, own in clusters.items():
        others = every - set(own)
        # Visible part of this cluster's marks at their real shaped position.
        visible = np.clip(_mask(canvas_size, xy, drop(text, others), f, anchor) - base_fill, 0, 255)
        # Full mark shape, taken from the ascender-less twin consonant.
        shape = np.clip(_mask(canvas_size, xy, drop(text, others, j), f, anchor)
                        - _mask(canvas_size, xy, drop(text, every, j), f, anchor), 0, 255)
        ys, xs = np.nonzero(shape > 8)
        pad = round(f.size * 0.45) + stroke
        y0, y1 = max(0, ys.min() - pad), min(shape.shape[0], ys.max() + pad)
        x0, x1 = max(0, xs.min() - pad), min(shape.shape[1], xs.max() + pad)
        S, V, B = shape[y0:y1, x0:x1], visible[y0:y1, x0:x1] > 128, base_fill[y0:y1, x0:x1] > 128
        tall_base = text[j] in TALL
        if not ((_dilate(np.where(V, 255.0, 0.0).astype(np.float32), 1) > 128) & B).any():
            # Not touching any other ink, so it is complete: use its exact shaped pixels
            # (Mitr swaps in pre-shifted mark glyphs on some tall consonants).
            real, where = visible[y0:y1, x0:x1], None
        elif not tall_base:
            # Mitr's own design joins this mark to its (non-tall) base: keep it as rendered.
            real, where = visible[y0:y1, x0:x1], "native"
        else:
            # Fused: find where the full twin-shaped mark sits in the real shaping.
            best, where = None, (0, 0)
            for dy in range(-round(f.size * 0.12), round(f.size * 0.12) + 1):
                for dx in range(-round(f.size * 0.35), round(f.size * 0.15) + 1):
                    s = _shift(S, dx, dy) > 128
                    score = int((s & V).sum()) - int((s & ~V & ~B).sum())
                    if best is None or score > best:
                        best, where = score, (dx, dy)
            real = _shift(S, *where)
        tall = B.copy()
        tall[max(0, xh_top - y0):, :] = False
        if tall_base:
            # The ascender is exactly what the tall consonant has and its twin lacks.
            asc = np.clip(_mask(canvas_size, xy, drop(text, every), f, anchor)
                          - _mask(canvas_size, xy, drop(text, every, j), f, anchor), 0, 255)[y0:y1, x0:x1]
            tall |= asc > 128
        near = (_dilate(np.where(tall, 255.0, 0.0).astype(np.float32), need) > 128) | (
            _dilate(B.astype(np.float32) * 255, need_any) > 128)
        for extra in range(round(f.size * 0.45)):
            moved = _shift(real, -extra, 0)
            if where == "native" or not ((moved > 128) & near).any():
                break
        else:
            raise RuntimeError(f"cannot clear mark cluster {text[j:own[-1] + 1]!r} in {text!r}")
        PLACEMENTS.append((text, text[j:own[-1] + 1], f.size, where, extra))
        full = np.zeros_like(shape)
        full[y0:y1, x0:x1] = moved
        halo = np.zeros_like(shape)
        halo[y0:y1, x0:x1] = _dilate(moved, stroke)
        np.maximum(fills, full, out=fills)
        np.maximum(strokes, halo, out=strokes)
    return strokes, fills


def layout(lines, f, stroke, gap):
    """Baselines stacking the lines by their outlined ink `gap` px apart (Mitr's
    line height reserves far more room than the actual marks need)."""
    baselines, y = [], 0
    for ln in lines:
        _, top, _, bottom = text_box(ln, f, stroke)
        baselines.append(y - top)
        y += (bottom - top) + gap
    return baselines, y - gap


def draw_block(canvas, lines, f, stroke, fill, x, top, align, gap):
    """Outlined text block with a soft drop shadow; returns the ink bbox."""
    anchor = "ms" if align == "center" else "ls"
    baselines, _ = layout(lines, f, stroke, gap)
    size = canvas.size
    strokes = np.zeros((size[1], size[0]), np.float32)
    fills = np.zeros_like(strokes)
    for ln, b in zip(lines, baselines):
        s, fl = line_masks(size, (x, top + b), ln, f, anchor, stroke)
        if align == "center":
            # Centre by the visible outlined ink, not by the glyph advances.
            cols = np.nonzero(s.max(axis=0) > 8)[0]
            dx = round(x - (cols.min() + cols.max() + 1) / 2)
            s, fl = _shift(s, dx, 0), _shift(fl, dx, 0)
        np.maximum(strokes, s, out=strokes)
        np.maximum(fills, fl, out=fills)
    stroke_img = Image.fromarray(strokes.astype(np.uint8))
    shadow_a = ImageChops.offset(stroke_img, 6, 9).filter(ImageFilter.GaussianBlur(7)).point(lambda v: int(v * 0.8))
    canvas.alpha_composite(Image.merge("RGBA", (*[Image.new("L", size, 0)] * 3, shadow_a)))
    black = Image.new("RGBA", size, (*BLACK, 255))
    black.putalpha(stroke_img)
    canvas.alpha_composite(black)
    colour = Image.new("RGBA", size, (*fill, 255))
    colour.putalpha(Image.fromarray(fills.astype(np.uint8)))
    canvas.alpha_composite(colour)
    bbox = stroke_img.getbbox()
    return bbox


# --- background / model ------------------------------------------------------
def background(src, crop, size):
    img = src.crop(crop).convert("RGB").resize(size, Image.Resampling.LANCZOS)
    # Slides carry big titles; blur hard enough that no word stays readable.
    img = img.filter(ImageFilter.GaussianBlur(46 if size[0] > size[1] else 60))
    img = ImageEnhance.Color(img).enhance(1.15)
    img = ImageEnhance.Brightness(img).enhance(0.5)
    return img.convert("RGBA")


def shade(canvas, portrait):
    """Dark gradients behind the text so the outlined lines stay the only readable text."""
    w, h = canvas.size
    if portrait:
        col = Image.new("L", (1, h))
        for y in range(h):
            p = y / (h - 1)
            text_band = max(0.0, 1 - abs(p - 0.28) / 0.32)
            bottom = max(0.0, (p - 0.80) / 0.20)
            col.putpixel((0, y), int(min(210, 50 + 120 * text_band + 90 * bottom)))
        mask = col.resize((w, h))
    else:
        row = Image.new("L", (w, 1))
        for x in range(w):
            row.putpixel((x, 0), int(max(0.0, 1 - (x / (w - 1)) / 0.62) * 185))
        col = Image.new("L", (1, h))
        for y in range(h):
            col.putpixel((0, y), int(max(0.0, (y / (h - 1) - 0.45) / 0.55) * 140))
        mask = ImageChops.lighter(row.resize((w, h)), col.resize((w, h)))
    canvas.alpha_composite(Image.merge("RGBA", (*[Image.new("L", (w, h), 0)] * 3, mask)))


def load_model(name, bust=1500):
    src = Image.open(MODELS / name).convert("RGBA")
    if name.startswith("vts_"):
        # Bust crop of the 4K VTube Studio capture down to the shirt; the crop's
        # bottom edge becomes the canvas bottom, so only the lower body is trimmed.
        _, t, _, b = src.getchannel("A").getbbox()
        src = src.crop((0, t, src.width, min(b, t + bust)))
        src = _drop_cut_islands(src)
    return src.crop(src.getchannel("A").getbbox())


def _drop_cut_islands(img, keep_share=0.02):
    """Remove small alpha islands touching the bottom crop edge (cut-off hair tips)."""
    alpha = img.getchannel("A")
    solid = alpha.point(lambda v: 255 if v > 24 else 0)
    total = int((np.asarray(solid) > 0).sum())
    bottom = np.asarray(solid)[-1]
    drop = Image.new("L", img.size, 0)
    seen = np.zeros(img.width, bool)
    for x in np.nonzero(bottom > 0)[0]:
        if seen[x]:
            continue
        probe = solid.copy()
        ImageDraw.floodfill(probe, (int(x), img.height - 1), 128)
        comp = np.asarray(probe) == 128
        seen |= comp[-1]
        if comp.sum() < keep_share * total:
            drop.paste(255, mask=Image.fromarray((comp * 255).astype(np.uint8)))
    if drop.getbbox():
        grown = drop.filter(ImageFilter.MaxFilter(5))
        img = img.copy()
        img.putalpha(ImageChops.subtract(alpha, grown))
    return img


def outline(model, width, colour=(255, 255, 255)):
    pad = width + 60  # room for the blurred shadow on every side
    base = Image.new("RGBA", (model.width + 2 * pad, model.height + 2 * pad), (0, 0, 0, 0))
    base.paste(model, (pad, pad))
    a = base.getchannel("A")
    grown = a.filter(ImageFilter.MaxFilter(2 * width + 1))
    grown = grown.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 110 else int(v * 2.2))
    edge = Image.new("RGBA", base.size, (*colour, 255))
    edge.putalpha(grown)
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 255))
    shadow.putalpha(grown.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.55)))
    out = Image.new("RGBA", base.size, (0, 0, 0, 0))
    out.alpha_composite(shadow)
    out.alpha_composite(edge)
    out.alpha_composite(base)
    return out, pad


def place_model(canvas, cfg, portrait):
    m = load_model(cfg["model"], cfg.get("short_bust", 1560) if portrait else cfg.get("bust", 1500))
    vts = cfg["model"].startswith("vts_")
    if portrait:
        max_w, max_h = (1000, 880) if not vts else (1060, 900)
    else:
        max_w, max_h = (1000, 900) if not vts else (1400, 1000)
    scale = min(max_w / m.width, max_h / m.height)
    m = m.resize((round(m.width * scale), round(m.height * scale)), Image.Resampling.LANCZOS)
    if scale > 1.05:
        m = m.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
    framed, pad = outline(m, 12 if portrait else 13)
    if portrait:
        x = canvas.width // 2 - m.width // 2 - pad          # alpha bbox centred on x=540
    elif vts:
        # Face near x=1460; at most 110 px of side hair may run past the right edge.
        x = min(1460 - m.width // 2, canvas.width + 110 - m.width) - pad
    else:
        x = min(1450 - m.width // 2 - pad, canvas.width - m.width - pad - 20)
    y = canvas.height - m.height - pad                      # model bottom = canvas bottom
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.paste(framed, (x, y))                             # paste clips at the canvas edges
    canvas.alpha_composite(layer)
    return (x + pad, y + pad, x + pad + m.width, canvas.height), scale


def build(idx, cfg, name, src, portrait):
    size = (1080, 1920) if portrait else (1920, 1080)
    canvas = background(src, cfg["short_crop" if portrait else "land_crop"], size)
    shade(canvas, portrait)
    model_box, scale = place_model(canvas, cfg, portrait)
    texts = cfg["short" if portrait else "land"]
    if portrait:
        x, align, max_w = size[0] // 2, "center", 960
        area_top, area_bottom = 150, model_box[1] - 90      # keep stroke + shadow clear of the ears
    else:
        x, align, max_w = 80, "left", min(1000, model_box[0] - 80 - 30)
        area_top, area_bottom = 110, size[1] - 75
    hook_start, sec_start = (190, 92) if portrait else (200, 96)
    while True:
        sec_f, sec_s = fit(texts["sec"], max_w, sec_start, 50, 0.13)
        hook_f, hook_s = fit(texts["hook"], max_w, hook_start, 80, 0.12)
        sec_gap, hook_gap, block_gap = round(sec_f.size * 0.10), round(hook_f.size * 0.06), round(hook_f.size * 0.16)
        _, sec_h = layout(texts["sec"], sec_f, sec_s, sec_gap)
        _, hook_h = layout(texts["hook"], hook_f, hook_s, hook_gap)
        block = sec_h + block_gap + hook_h
        if block <= area_bottom - area_top or hook_start <= 100:
            break
        hook_start -= 4
        sec_start = max(70, sec_start - 2)
    if portrait:
        top = area_top + max(0, (area_bottom - area_top - block) // 2)
    else:
        top = area_bottom - block
    sec_ink = draw_block(canvas, texts["sec"], sec_f, sec_s, WHITE, x, top, align, sec_gap)
    hook_ink = draw_block(canvas, texts["hook"], hook_f, hook_s, RED, x, top + sec_h + block_gap, align, hook_gap)
    out = JPG / f"{name}{'-short' if portrait else ''}.jpg"
    canvas.convert("RGB").save(out, "JPEG", quality=94, subsampling=0, optimize=True)
    return {
        "timeline": name, "timeline_index": idx, "orientation": "portrait" if portrait else "landscape",
        "size": list(size), "path": str(out), "hook": texts["hook"], "secondary": texts["sec"],
        "hook_font": hook_f.size, "secondary_font": sec_f.size, "hook_ink": list(hook_ink), "secondary_ink": list(sec_ink),
        "model": cfg["model"], "model_box": list(model_box), "model_scale": round(scale, 3), "mood": cfg["mood"],
        "background": cfg["bg"], "evidence": cfg["evidence"],
    }


def main():
    JPG.mkdir(parents=True, exist_ok=True)
    audit = json.loads((ROOT / "timeline-audit.json").read_text(encoding="utf-8"))
    manifest = []
    for t in audit["timelines"]:
        idx = t["index"]
        src = Image.open(ROOT / TL[idx]["bg"]).convert("RGB")
        for portrait in (False, True):
            manifest.append(build(idx, TL[idx], t["name"], src, portrait))
            print(Path(manifest[-1]["path"]).name, manifest[-1]["hook_font"], manifest[-1]["secondary_font"])
    (OUT / "delivery-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
