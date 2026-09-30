"""Build enhanced Armigon covers (v3) with center-left text, graphic storytelling,
and 6-expression avatar matrix.
"""
import argparse
import json
import os
import re
import zipfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

from graphics_overlay import draw_hand_drawn_circle, draw_emotion_marker

# --- Paths -------------------------------------------------------------------
# Overridable via environment so the module imports and runs on any machine:
#   ARMIGON_FINAL_DIR  -> output root (default: author's D: drive location)
#   ARMIGON_FONT_PATH  -> Mitr-Bold.ttf
#   ARMIGON_AVATAR_DIR -> 6-expression avatar PNGs
# Rendered output is unchanged when the variables are unset.
WORK = Path(__file__).parent
FINAL = Path(os.environ.get("ARMIGON_FINAL_DIR", r"D:\agent-thumbnail\outputs\armigon-20260920-final-20260928"))
OUT_JPG = FINAL / "jpg"
FONT = Path(os.environ.get("ARMIGON_FONT_PATH", r"D:\agent-thumbnail\outputs\timeline-covers\fonts\Mitr-Bold.ttf"))
AVATAR_DIR = Path(os.environ.get("ARMIGON_AVATAR_DIR", r"I:\My Drive\Dreamlight_projects\GEN-Sercet\armigon"))

# --- Tuning knobs (Design Spec) ---------------------------------------------
BLUR_LANDSCAPE = 0       # 0 px unblurred
BLUR_PORTRAIT = 0        # 0 px unblurred
BRIGHTNESS = 0.90        # 0.90 brightness
COLOR_ENHANCE = 1.12     # natural color
CONTRAST = 1.08          # crisp contrast

# --- Accent colours per game ------------------------------------------------
ACCENTS = {
    "Peak": (74, 196, 255), "Linxicon": (255, 102, 184), "Starbound": (167, 119, 255),
    "MC RPG 005": (69, 208, 121), "Roblox": (255, 72, 72), "Mecha Chameleon": (59, 222, 174),
    "Palworld": (255, 182, 64), "MC เลือดเดียวกัน": (91, 178, 255), "Backrooms": (207, 207, 207),
    "Valorant": (255, 92, 132),
}

# --- 16-Timeline Storytelling Mapping (Design Spec Section 3 & 4) ------------
TIMELINE_CONFIG = {
    1: {  # 01-01 Peak - ช่วยโฮชิให้รอดจากเขา
        "avatar": "cry.png",
        "focus_circle": (520, 360, 110),
        "emotion_marker": ("!", (1180, 240)),
    },
    2: {  # 02-01 Linxicon - ต่อคำจนโยงไปถึงไส้ติ่ง
        "avatar": "hello.png",
        "focus_circle": None,
        "emotion_marker": ("?", (1180, 240)),
    },
    3: {  # 02-02 Linxicon - คำว่าแค้นวนจนขำ
        "avatar": "angry.png",
        "focus_circle": None,
        "emotion_marker": ("!", (1180, 240)),
    },
    4: {  # 03-01 Starbound - บอสแพ้ก่อนเทสลาจะได้ลงมือ
        "avatar": "cry.png",
        "focus_circle": (910, 290, 120),
        "emotion_marker": ("!", (1180, 240)),
    },
    5: {  # 03-02 Starbound - ของชิ้นใหญ่เท่าควาย
        "avatar": "great.png",
        "focus_circle": None,
        "emotion_marker": None,
    },
    6: {  # 04-01 MC RPG 005 - กลับมารับโทษเดี๋ยวนี้
        "avatar": "sadistic.png",
        "focus_circle": (700, 350, 130),
        "emotion_marker": ("!", (1180, 240)),
    },
    7: {  # 05-01 Roblox วันเกิด - หลงทางในเกมผี
        "avatar": "cry.png",
        "focus_circle": None,
        "emotion_marker": ("!", (1180, 240)),
    },
    8: {  # 05-02 Roblox วันเกิด - เดาตัวละครให้ถูกสิ
        "avatar": "adore.png",
        "focus_circle": None,
        "emotion_marker": None,
    },
    9: {  # 06-01 Mecha Chameleon - ซ่อนเนียนจนเพื่อนหาไม่เจอ
        "avatar": "great.png",
        "focus_circle": (840, 350, 115),
        "emotion_marker": ("!", (1180, 240)),
    },
    10: {  # 06-02 Mecha Chameleon - ซ่อนหลังกล่องเขียว
        "avatar": "angry.png",
        "focus_circle": (640, 600, 120),
        "emotion_marker": ("!", (1180, 240)),
    },
    11: {  # 07-01 Palworld - วางของแล้วดันติดตัว
        "avatar": "hello.png",
        "focus_circle": (870, 360, 125),
        "emotion_marker": ("?", (1180, 240)),
    },
    12: {  # 08-01 MC เลือดเดียวกัน - หลุมยักษ์กับผีที่หายไป
        "avatar": "angry.png",
        "focus_circle": (620, 520, 135),
        "emotion_marker": ("!", (1180, 240)),
    },
    13: {  # 08-02 MC เลือดเดียวกัน - ห้องน้ำนี้ห้ามใครเข้า
        "avatar": "sadistic.png",
        "focus_circle": None,
        "emotion_marker": None,
    },
    14: {  # 09-01 Backrooms - หันมาเจออะไรอยู่ข้างหลัง
        "avatar": "cry.png",
        "focus_circle": (850, 480, 110),
        "emotion_marker": ("!", (1180, 240)),
    },
    15: {  # 10-01 Valorant - ยังไม่ตาย รีบหมุนไซต์
        "avatar": "angry.png",
        "focus_circle": None,
        "emotion_marker": ("!", (1180, 240)),
    },
    16: {  # 10-02 Valorant - เพื่อนเลือกเอเจนต์ตามที่ถนัด
        "avatar": "hello.png",
        "focus_circle": None,
        "emotion_marker": ("?", (1180, 240)),
    },
}


def safe_name(name):
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", name).rstrip(" .")


def fit_lines_font(draw, lines, max_width, start, minimum=34, stroke=8):
    """Finds the largest font size where every line fits within max_width."""
    size = start
    while size >= minimum:
        font = ImageFont.truetype(str(FONT), size)
        if all(draw.textbbox((0, 0), ln, font=font, stroke_width=stroke)[2] <= max_width for ln in lines if ln):
            return font
        size -= 2
    return ImageFont.truetype(str(FONT), minimum)


def wrap_text(draw, text_or_lines, max_width, start, minimum, stroke):
    """Splits text into balanced lines and fits them at the largest possible font size."""
    if isinstance(text_or_lines, list):
        candidate_lines = text_or_lines
    elif "\n" in text_or_lines:
        candidate_lines = text_or_lines.split("\n")
    elif " " in text_or_lines:
        words = text_or_lines.split(" ")
        if len(words) == 2:
            candidate_lines = words
        else:
            # Try 1 line first with start font
            f_test = ImageFont.truetype(str(FONT), start)
            if draw.textbbox((0, 0), text_or_lines, font=f_test, stroke_width=stroke)[2] <= max_width:
                candidate_lines = [text_or_lines]
            else:
                mid = len(words) // 2
                candidate_lines = [" ".join(words[:mid]), " ".join(words[mid:])]
    else:
        candidate_lines = [text_or_lines]

    font = fit_lines_font(draw, candidate_lines, max_width, start, minimum, stroke)
    return candidate_lines, font


def crop_background(image, size, blur_px, focus_x=0.5):
    """Crop, resize, color-enhance, and adjust brightness."""
    image = ImageOps.fit(image.convert("RGB"), size, method=Image.Resampling.LANCZOS, centering=(focus_x, 0.5))
    if blur_px > 0:
        image = image.filter(ImageFilter.GaussianBlur(blur_px))
    image = ImageEnhance.Color(image).enhance(COLOR_ENHANCE)
    image = ImageEnhance.Contrast(image).enhance(CONTRAST)
    image = ImageEnhance.Brightness(image).enhance(BRIGHTNESS)
    return image.convert("RGBA")


def add_gradient(canvas, portrait):
    """Add smooth gradient that guarantees text contrast on center-left."""
    w, h = canvas.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    if portrait:
        col = Image.new("L", (1, h))
        for y in range(h):
            p = y / max(1, h - 1)
            text_band = max(0.0, 1.0 - abs(p - 0.24) / 0.28)
            bottom = max(0.0, (p - 0.75) / 0.25)
            alpha = int(min(210, 40 + 130 * text_band + 70 * bottom))
            col.putpixel((0, y), alpha)
        mask = col.resize((w, h), Image.Resampling.BILINEAR)
        gradient = Image.new("RGBA", (w, h), (6, 10, 24, 0))
        gradient.putalpha(mask)
        canvas.alpha_composite(gradient)
    else:
        # Landscape: protect left 55% where text sits, tapering to transparent by x=980
        row = Image.new("L", (w, 1))
        for x in range(w):
            p_x = x / max(1, w - 1)
            # Full darkness on left, smooth curve down to 0 at x ≈ 980 (p_x ≈ 0.51)
            if p_x < 0.52:
                alpha = int(195 * (1.0 - (p_x / 0.52) ** 1.3))
            else:
                alpha = 0
            row.putpixel((x, 0), alpha)
            
        col = Image.new("L", (1, h))
        for y in range(h):
            p_y = y / max(1, h - 1)
            # slight bottom darkening
            bottom = max(0.0, (p_y - 0.60) / 0.40) * 110
            col.putpixel((0, y), int(bottom))
            
        h_mask = row.resize((w, h), Image.Resampling.BILINEAR)
        v_mask = col.resize((w, h), Image.Resampling.BILINEAR)
        mask = ImageChops.lighter(h_mask, v_mask)
        
        gradient = Image.new("RGBA", (w, h), (4, 8, 20, 0))
        gradient.putalpha(mask)
        canvas.alpha_composite(gradient)


def avatar_layer(path, max_w, max_h):
    src = Image.open(path).convert("RGBA")
    alpha = src.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        raise RuntimeError(f"avatar has no visible pixels: {path}")
    trimmed = src.crop(bbox)
    scale = min(max_w / trimmed.width, max_h / trimmed.height)
    size = (max(1, round(trimmed.width * scale)), max(1, round(trimmed.height * scale)))
    trimmed = trimmed.resize(size, Image.Resampling.LANCZOS)
    return trimmed


def paste_avatar(canvas, path, portrait, accent):
    if portrait:
        avatar = avatar_layer(path, 920, 800)
        x = (canvas.width - avatar.width) // 2
        y = 1140
    else:
        avatar = avatar_layer(path, 980, 975)
        x = 1460 - avatar.width // 2
        y = canvas.height - avatar.height + 15
    alpha = avatar.getchannel("A")
    expanded = alpha.filter(ImageFilter.MaxFilter(17))
    white_edge = Image.new("RGBA", avatar.size, (255, 255, 255, 0))
    white_edge.putalpha(Image.eval(ImageChops.subtract(expanded, alpha), lambda p: min(245, p)))
    halo = Image.new("RGBA", avatar.size, (*accent, 0))
    halo.putalpha(expanded.filter(ImageFilter.GaussianBlur(22)).point(lambda p: round(p * 0.34)))
    shadow = Image.new("RGBA", avatar.size, (0, 0, 0, 0))
    shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(14)).point(lambda p: round(p * 0.56)))
    canvas.alpha_composite(halo, (x, y))
    canvas.alpha_composite(shadow, (x + 12, y + 18))
    canvas.alpha_composite(white_edge, (x, y))
    canvas.alpha_composite(avatar, (x, y))


def draw_text_block(canvas, hook, secondary, portrait):
    """Draws hook and secondary text with center-left elevation and high-contrast stroke."""
    draw = ImageDraw.Draw(canvas)
    if portrait:
        max_width = 940
        hook_lines, hook_font = wrap_text(draw, hook, max_width, 150, 60, 12)
        sec_lines, sec_font = wrap_text(draw, secondary, max_width, 92, 45, 9)
        hook_y, sec_y = 360, 640
        anchor = "mm"
        x = canvas.width // 2
    else:
        max_width = 850
        # Elevate to center-left (y_center ≈ 450)
        hook_lines, hook_font = wrap_text(draw, hook, max_width, 165, 75, 14)
        sec_lines, sec_font = wrap_text(draw, secondary, max_width, 105, 52, 10)
        
        # Calculate dynamic vertical centering
        line_h_hook = hook_font.size + 24
        line_h_sec = sec_font.size + 18
        total_block_h = (len(hook_lines) * line_h_hook) + (len(sec_lines) * line_h_sec) + 35
        
        target_center_y = 460
        block_top = max(140, target_center_y - total_block_h // 2)
        
        hook_y = block_top + (len(hook_lines) * line_h_hook) // 2
        sec_y = block_top + (len(hook_lines) * line_h_hook) + 35 + (len(sec_lines) * line_h_sec) // 2
        
        anchor = "lm"
        x = 88

    def block(lines, font, y, fill, stroke):
        line_h = font.size + (20 if portrait else 24)
        for i, line in enumerate(lines):
            yy = y + (i - (len(lines) - 1) / 2) * line_h
            # Outer dark drop shadow
            draw.text((x + (5 if not portrait else 0), yy + 8), line, font=font, anchor=anchor,
                      fill=(0, 0, 0, 210), stroke_width=stroke + 8, stroke_fill=(0, 0, 0, 220))
            # Black border stroke
            draw.text((x, yy), line, font=font, anchor=anchor, fill=fill,
                      stroke_width=stroke, stroke_fill=(0, 0, 0, 255))

    block(hook_lines, hook_font, hook_y, (236, 28, 36, 255), 11 if portrait else 13)
    block(sec_lines, sec_font, sec_y, (255, 255, 255, 255), 8 if portrait else 10)
    
    return {
        "hook_lines": hook_lines, "secondary_lines": sec_lines,
        "hook_font": hook_font.size, "secondary_font": sec_font.size
    }


def game_key(name):
    for key in ACCENTS:
        if key in name:
            return key
    return "Backrooms"


def build_cover(rec, cfg, portrait=False):
    """Build a single enhanced cover from manifest record and timeline config."""
    name = rec["timeline_name"]
    key = game_key(name)
    frame_path = FINAL / rec["source_frame_file"]
    frame = Image.open(frame_path)

    size = (1080, 1920) if portrait else (1920, 1080)
    blur_px = BLUR_PORTRAIT if portrait else BLUR_LANDSCAPE

    canvas = crop_background(frame, size, blur_px, focus_x=0.5)
    
    # 1. Hand-drawn focus circle on incident point (Landscape only, or adjusted for Shorts)
    if not portrait and cfg.get("focus_circle"):
        cx, cy, r = cfg["focus_circle"]
        draw_hand_drawn_circle(canvas, (cx, cy), r, color=(236, 28, 36), stroke_width=13)
        
    # 2. Gradient overlay to protect center-left text
    add_gradient(canvas, portrait)

    # 3. Text block
    hook = " ".join(rec["hook_lines"]) if isinstance(rec["hook_lines"], list) else rec["hook_lines"]
    secondary = " ".join(rec["secondary_lines"]) if isinstance(rec["secondary_lines"], list) else rec["secondary_lines"]
    text_info = draw_text_block(canvas, hook, secondary, portrait)

    # 4. Avatar from 6-expression matrix
    avatar_file = cfg["avatar"]
    avatar_path = AVATAR_DIR / avatar_file
    paste_avatar(canvas, avatar_path, portrait, ACCENTS[key])

    # 5. Anime emotion marker
    if cfg.get("emotion_marker"):
        m_type, (mx, my) = cfg["emotion_marker"]
        if portrait:
            # Shift beside head in Shorts
            draw_emotion_marker(canvas, m_type, pos=(880, 1220), size=120, angle=12 if m_type == "!" else -10)
        else:
            draw_emotion_marker(canvas, m_type, pos=(mx, my), size=135, angle=12 if m_type == "!" else -12)

    # 6. Accent colored border
    d = ImageDraw.Draw(canvas)
    border = 5 if portrait else 6
    d.rounded_rectangle((border, border, size[0] - border - 1, size[1] - border - 1),
                        radius=22, outline=(*ACCENTS[key], 205), width=border)

    return canvas, name, text_info, avatar_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", type=int, default=0, help="Only rebuild N landscape covers for preview")
    args = parser.parse_args()

    OUT_JPG.mkdir(parents=True, exist_ok=True)

    manifest = json.loads((FINAL / "delivery-manifest.json").read_text(encoding="utf-8"))
    outputs = manifest["outputs"]

    landscape = [o for o in outputs if o["orientation"] == "landscape"]
    portrait = [o for o in outputs if o["orientation"] == "portrait"]

    if args.preview > 0:
        landscape = landscape[:args.preview]
        portrait = []

    total = len(landscape) + len(portrait)
    count = 0

    for rec in landscape:
        idx = rec["story_index"]
        cfg = TIMELINE_CONFIG.get(idx, {"avatar": "hello.png", "focus_circle": None, "emotion_marker": None})
        canvas, name, text_info, avatar_file = build_cover(rec, cfg, portrait=False)
        out = OUT_JPG / rec["filename"]
        canvas.convert("RGB").save(out, "JPEG", quality=95, subsampling=0, optimize=True)
        rec["model"] = avatar_file
        rec["background_blur_radius_px"] = BLUR_LANDSCAPE
        count += 1
        print(f"[{count}/{total}] {rec['filename']} (model: {avatar_file})")

    for rec in portrait:
        idx = rec["story_index"]
        cfg = TIMELINE_CONFIG.get(idx, {"avatar": "hello.png", "focus_circle": None, "emotion_marker": None})
        canvas, name, text_info, avatar_file = build_cover(rec, cfg, portrait=True)
        out = OUT_JPG / rec["filename"]
        canvas.convert("RGB").save(out, "JPEG", quality=95, subsampling=0, optimize=True)
        rec["model"] = avatar_file
        rec["background_blur_radius_px"] = BLUR_PORTRAIT
        count += 1
        print(f"[{count}/{total}] {rec['filename']} (model: {avatar_file})")

    if args.preview == 0:
        manifest["version"] = "v3-enhanced"
        manifest["enhancements"] = (
            "Center-left elevated text, hand-drawn focus circles on key game incidents, "
            "anime emotion markers (!/?), and complete 6-avatar expression matrix."
        )
        (FINAL / "delivery-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nCompleted: {count} covers rebuilt in v3 style.")


if __name__ == "__main__":
    main()
