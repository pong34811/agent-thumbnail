"""Build High-CTR Half-Body Covers for Tygarina 2026-08-01 Timelines.

Generates 6 Landscape (1920x1080) + 6 Shorts (1080x1920) covers
using Tygarina character assets cropped to Half-Body (ครึ่งตัว),
authentic video background frames, and Mitr Bold typography (Red Hook + White Secondary).
"""
import os
import sys
import json
import zipfile
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

# Paths
MODELS_DIR = Path(r"C:\Users\warit\Downloads\โม_")
GDRIVE_DIR = Path(r"G:\My Drive\Projects\Tygarina\2026-08-01")
OUT_DIR = Path(r"c:\Users\warit\Desktop\agent-thumbnail\outputs\tygarina-20260801")
JPG_DIR = OUT_DIR / "jpg"
GDRIVE_THUMB_DIR = GDRIVE_DIR / "thumbnails"
FONT_PATH = r"C:\Windows\Fonts\Mitr-Bold.ttf"
FFMPEG = r"C:\Users\warit\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"

os.makedirs(JPG_DIR, exist_ok=True)
os.makedirs(GDRIVE_THUMB_DIR, exist_ok=True)

# Configuration for the 6 clips
CLIPS = [
    {
        "id": 1,
        "name": "กินแต่เซเว่นทุกวัน",
        "video": "กินแต่เซเว่นทุกวัน.mov",
        "tl_land": "กินแต่เซเว่นทุกวัน-vdo",
        "tl_short": "กินแต่เซเว่นทุกวัน-vdo_9x16",
        "model_file": "4.png",
        "is_bust": True,
        "mood": "หัวเราะตาปิด ขำตัวเองที่กินวนลูป 3 เมนูเดิมๆ",
        "sec": "วนลูป 3 เมนูทุกเช้า",
        "hook": "กินแต่เซเว่น!",
        "ss_time": "00:00:06"
    },
    {
        "id": 2,
        "name": "ของับหูไทกะหน่อยสิ",
        "video": "ของับหูไทกะหน่อยสิ.mov",
        "tl_land": "ของับหูไทกะหน่อยสิ-vdo",
        "tl_short": "ของับหูไทกะหน่อยสิ-vdo_9x16",
        "model_file": "3.png",
        "is_bust": True,
        "mood": "ยิ้มตาปิด เขินปนกวน เมื่อโดนขอของับหู",
        "sec": "เสือจีบหญิงเลเวลอัป?!",
        "hook": "ของับหูหน่อย!",
        "ss_time": "00:00:05"
    },
    {
        "id": 3,
        "name": "ถ้าคุณคามิเป็นผู้สาวละก็",
        "video": "ถ้าคุณคามิเป็นผู้สาวละก็.mov",
        "tl_land": "ถ้าคุณคามิเป็นผู้สาวละก็-vdo",
        "tl_short": "ถ้าคุณคามิเป็นผู้สาวละก็-vdo_9x16",
        "model_file": "1.png",
        "is_bust": True,
        "mood": "ยิ้มหวาน ตาประกาย หยอดหวานใส่คนดู",
        "sec": "ถ้าคุณคามิเป็นผู้สาว...",
        "hook": "ได้ใจหนูไปแล้ว!",
        "ss_time": "00:00:08"
    },
    {
        "id": 4,
        "name": "รักแม่เขามา 10 ปี",
        "video": "รักแม่เขามา 10 ปี.mov",
        "tl_land": "รักแม่เขามา 10 ปี-vdo",
        "tl_short": "รักแม่เขามา 10 ปี-vdo_9x16",
        "model_file": "dsada.png",
        "is_bust": False,
        "crop_bottom": 2750,
        "mood": "หน้ามืด มีเงาดำตกกระทบหน้า ช็อก ดาร์ก สไตล์มาเฟีย",
        "sec": "มาเฟียอยากได้ก็แค่คว้า",
        "hook": "รักแม่เขามา 10 ปี?!",
        "ss_time": "00:00:05"
    },
    {
        "id": 5,
        "name": "รู้จักกะทงทองไหม",
        "video": "รู้จักกะทงทองไหม.mov",
        "tl_land": "รู้จักกะทงทองไหม-vdo",
        "tl_short": "รู้จักกะทงทองไหม-vdo_9x16",
        "model_file": "dsadadsad.png",
        "is_bust": False,
        "crop_bottom": 2750,
        "mood": "ดันแว่น ท่าทางเล่าเรื่อง ชวนคุยถามคนดูอย่างมั่นใจ",
        "sec": "รู้จักกระทงทองไหม?",
        "hook": "กินครั้งเดียวในชีวิต!",
        "ss_time": "00:00:07"
    },
    {
        "id": 6,
        "name": "อยากจับทำเมีย",
        "video": "อยากจับทำเมีย.mov",
        "tl_land": "อยากจับทำเมีย-vdo",
        "tl_short": "อยากจับทำเมีย-vdo_9x16",
        "model_file": "dsadsadas.png",
        "is_bust": False,
        "crop_bottom": 2750,
        "mood": "แลบลิ้น ขี้เล่น กวนๆ แฟรงค์ๆ ชมว่าน้องน่ารักมาก",
        "sec": "ขอพูดตรงๆ เลยนะ",
        "hook": "น่าทำเมียมาก!",
        "ss_time": "00:00:09"
    }
]

def extract_frame(video_path, time_str, out_path):
    """Extract 1 high quality frame from video."""
    if not os.path.exists(out_path):
        cmd = [FFMPEG, "-y", "-ss", time_str, "-i", str(video_path), "-vframes", "1", "-q:v", "2", str(out_path)]
        subprocess.run(cmd, capture_output=True, check=True)

def load_and_crop_model(clip_info):
    """Load character model and crop to Half-Body (ครึ่งตัว) with stray pixel removal."""
    p = MODELS_DIR / clip_info["model_file"]
    img = Image.open(p).convert("RGBA")
    
    # Remove rogue pixel island present in 1.png, 3.png, 4.png around row 640..675, col 3100..3150
    a = np.array(img.getchannel("A"))
    a[600:720, 3050:3200] = 0
    img.putalpha(Image.fromarray(a))

    bbox = img.getchannel("A").getbbox()
    
    if clip_info.get("is_bust", False):
        # Already bust-up, crop to alpha bounds
        cropped = img.crop(bbox)
    else:
        # Full body: crop from top of ears to waist/belt (y = crop_bottom)
        top = bbox[1]
        bottom = min(img.height, clip_info.get("crop_bottom", 2750))
        cropped = img.crop((0, top, img.width, bottom))
        abox = cropped.getchannel("A").getbbox()
        if abox:
            cropped = cropped.crop(abox)
            
    return cropped

def outline_model(model, width=14, colour=(255, 255, 255)):
    """Add crisp white outline + soft black shadow."""
    pad = width + 50
    base = Image.new("RGBA", (model.width + 2 * pad, model.height + 2 * pad), (0, 0, 0, 0))
    base.paste(model, (pad, pad))
    a = base.getchannel("A")
    grown = a.filter(ImageFilter.MaxFilter(2 * width + 1))
    grown = grown.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 110 else int(v * 2.2))
    edge = Image.new("RGBA", base.size, (*colour, 255))
    edge.putalpha(grown)
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 255))
    shadow.putalpha(grown.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.70)))
    out = Image.new("RGBA", base.size, (0, 0, 0, 0))
    out.alpha_composite(shadow)
    out.alpha_composite(edge)
    out.alpha_composite(base)
    return out, pad

def make_landscape_background(frame_path, size=(1920, 1080)):
    """Prepare darkened blurred landscape background with left gradient."""
    bg = Image.open(frame_path).convert("RGB").resize(size, Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(36))
    bg = ImageEnhance.Color(bg).enhance(1.20)
    bg = ImageEnhance.Brightness(bg).enhance(0.40)
    bg = bg.convert("RGBA")

    # Dark gradient on left for text readability
    w, h = size
    grad = Image.new("L", (w, 1))
    for x in range(w):
        # Deep dark from x=0 to x=1150
        v = int(max(0.0, 1.0 - (x / (w * 0.62))) * 200)
        grad.putpixel((x, 0), v)
    dark_layer = Image.new("RGBA", size, (10, 10, 15, 0))
    dark_layer.putalpha(grad.resize((w, h)))
    bg.alpha_composite(dark_layer)
    return bg

def make_portrait_background(frame_path, size=(1080, 1920)):
    """Prepare darkened blurred portrait background with top gradient."""
    src = Image.open(frame_path).convert("RGB")
    src_w, src_h = src.size
    target_aspect = size[0] / size[1]
    crop_w = int(src_h * target_aspect)
    x0 = max(0, (src_w - crop_w) // 2)
    bg = src.crop((x0, 0, x0 + crop_w, src_h)).resize(size, Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(44))
    bg = ImageEnhance.Color(bg).enhance(1.20)
    bg = ImageEnhance.Brightness(bg).enhance(0.38)
    bg = bg.convert("RGBA")

    # Dark gradient on top for text readability
    w, h = size
    grad = Image.new("L", (1, h))
    for y in range(h):
        v = int(max(0.0, 1.0 - (y / (h * 0.42))) * 210)
        grad.putpixel((0, y), v)
    dark_layer = Image.new("RGBA", size, (10, 10, 15, 0))
    dark_layer.putalpha(grad.resize((w, h)))
    bg.alpha_composite(dark_layer)
    return bg

def draw_text_line(canvas, text, f, fill, stroke_fill, stroke_width, x, y, align="left"):
    """Draw text with stroke and drop shadow."""
    anchor = "ls" if align == "left" else "ms"
    # Shadow
    shadow_img = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d_sh = ImageDraw.Draw(shadow_img)
    d_sh.text((x + 8, y + 11), text, font=f, fill=(0, 0, 0, 230),
              stroke_width=stroke_width + 4, stroke_fill=(0, 0, 0, 230), anchor=anchor)
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(8))
    canvas.alpha_composite(shadow_img)

    # Main text with stroke
    d = ImageDraw.Draw(canvas)
    d.text((x, y), text, font=f, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill, anchor=anchor)

def build_landscape_cover(clip_info, frame_path):
    """Generate 1920x1080 landscape cover with half-body character."""
    canvas = make_landscape_background(frame_path)
    
    # Model: height around 1020px (fills vertical space beautifully)
    model = load_and_crop_model(clip_info)
    target_h = 1020
    scale = target_h / model.height
    target_w = round(model.width * scale)
    scaled_m = model.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    framed, pad = outline_model(scaled_m, width=14)
    mx = canvas.width - target_w - pad + 50
    my = canvas.height - target_h - pad
    canvas.alpha_composite(framed, (mx, my))

    # Text: Big, bold, impactful (Mitr Bold)
    f_sec = ImageFont.truetype(FONT_PATH, 80)
    f_hook = ImageFont.truetype(FONT_PATH, 135)

    # Left zone positioning
    draw_text_line(canvas, clip_info["sec"], f_sec, (255, 255, 255), (0, 0, 0), 12, 90, 470, align="left")
    draw_text_line(canvas, clip_info["hook"], f_hook, (236, 28, 36), (0, 0, 0), 18, 90, 640, align="left")

    return canvas.convert("RGB")

def build_portrait_cover(clip_info, frame_path):
    """Generate 1080x1920 portrait cover with centered half-body character."""
    canvas = make_portrait_background(frame_path)

    # Model: height around 1180px, centered
    model = load_and_crop_model(clip_info)
    target_h = 1180
    scale = target_h / model.height
    target_w = round(model.width * scale)
    scaled_m = model.resize((target_w, target_h), Image.Resampling.LANCZOS)

    framed, pad = outline_model(scaled_m, width=14)
    mx = (canvas.width - target_w) // 2 - pad
    my = canvas.height - target_h - pad
    canvas.alpha_composite(framed, (mx, my))

    # Text in upper zone (centered)
    f_sec = ImageFont.truetype(FONT_PATH, 74)
    f_hook = ImageFont.truetype(FONT_PATH, 125)

    cx = canvas.width // 2
    draw_text_line(canvas, clip_info["sec"], f_sec, (255, 255, 255), (0, 0, 0), 12, cx, 360, align="center")
    draw_text_line(canvas, clip_info["hook"], f_hook, (236, 28, 36), (0, 0, 0), 18, cx, 520, align="center")

    return canvas.convert("RGB")

def main():
    manifest = {
        "project": "2026-08-01_First_Pass_v2",
        "character": "Tygarina",
        "style": "Half-Body (ครึ่งตัว) High-CTR Thai VTuber",
        "total_timelines": len(CLIPS) * 2,
        "items": []
    }

    frames_cache_dir = OUT_DIR / "frames"
    os.makedirs(frames_cache_dir, exist_ok=True)

    land_images = []
    port_images = []

    for c in CLIPS:
        print(f"Processing Clip {c['id']}: {c['name']}...")
        video_p = GDRIVE_DIR / c["video"]
        frame_p = frames_cache_dir / f"frame_{c['id']}.jpg"
        extract_frame(video_p, c["ss_time"], frame_p)

        # 1. Landscape
        land_img = build_landscape_cover(c, frame_p)
        land_fn_tl = f"{c['tl_land']}.jpg"
        land_fn_num = f"{c['id']:02d}_{c['name']}_16x9.png"
        
        # Save to local repo output
        land_img.save(JPG_DIR / land_fn_tl, quality=92)
        # Save to GDrive thumbnails folder
        land_img.save(GDRIVE_THUMB_DIR / land_fn_num)
        land_img.save(GDRIVE_THUMB_DIR / f"{c['id']:02d}_{c['name']}_16x9.jpg", quality=92)
        land_images.append((land_fn_tl, land_img))

        # 2. Portrait (Shorts)
        port_img = build_portrait_cover(c, frame_p)
        port_fn_tl = f"{c['tl_short']}.jpg"
        port_fn_num = f"{c['id']:02d}_{c['name']}_9x16.png"

        # Save to local repo output
        port_img.save(JPG_DIR / port_fn_tl, quality=92)
        # Save to GDrive thumbnails folder
        port_img.save(GDRIVE_THUMB_DIR / port_fn_num)
        port_img.save(GDRIVE_THUMB_DIR / f"{c['id']:02d}_{c['name']}_9x16.jpg", quality=92)
        port_images.append((port_fn_tl, port_img))

        manifest["items"].append({
            "id": c["id"],
            "name": c["name"],
            "timeline_landscape": c["tl_land"],
            "timeline_shorts": c["tl_short"],
            "model_file": c["model_file"],
            "mood": c["mood"],
            "hook_primary": c["hook"],
            "hook_secondary": c["sec"],
            "landscape_file": land_fn_tl,
            "shorts_file": port_fn_tl,
            "gdrive_16x9": land_fn_num,
            "gdrive_9x16": port_fn_num
        })

    # Save manifest
    manifest_p = OUT_DIR / "delivery-manifest.json"
    with open(manifest_p, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("Saved delivery manifest.")

    # Create Overview Contact Sheets
    # Landscape: 3 cols x 2 rows
    w, h = 640, 360
    ov_land = Image.new("RGB", (w * 3, h * 2))
    for i, (_, im) in enumerate(land_images):
        resized = im.resize((w, h), Image.Resampling.LANCZOS)
        ov_land.paste(resized, ((i % 3) * w, (i // 3) * h))
    ov_land.save(OUT_DIR / "overview-landscape.jpg", quality=88)

    # Portrait: 3 cols x 2 rows
    pw, ph = 360, 640
    ov_port = Image.new("RGB", (pw * 3, ph * 2))
    for i, (_, im) in enumerate(port_images):
        resized = im.resize((pw, ph), Image.Resampling.LANCZOS)
        ov_port.paste(resized, ((i % 3) * pw, (i // 3) * ph))
    ov_port.save(OUT_DIR / "overview-portrait.jpg", quality=88)
    print("Saved overview contact sheets.")

    # Create Zip Package
    zip_path = OUT_DIR / "Tygarina-2026-08-01-Timeline-Covers.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in JPG_DIR.glob("*.jpg"):
            zf.write(f, arcname=f"jpg/{f.name}")
        zf.write(OUT_DIR / "overview-landscape.jpg", arcname="overview-landscape.jpg")
        zf.write(OUT_DIR / "overview-portrait.jpg", arcname="overview-portrait.jpg")
        zf.write(manifest_p, arcname="delivery-manifest.json")
    print(f"Packaged ZIP: {zip_path} ({os.path.getsize(zip_path):,} bytes)")

if __name__ == "__main__":
    main()
