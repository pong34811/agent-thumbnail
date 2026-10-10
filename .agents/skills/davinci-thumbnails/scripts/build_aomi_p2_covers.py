"""Build Aomi p2 covers (44 clips x 16:9 + 9:16) from real source frames and RGBA avatars.

Usage: python build_aomi_p2_covers.py <frames_dir> [date] [--only N,N]
frames_dir holds NN.png from aomi_p2_extract_frames.py. Hook/sec/model come from
projects/aomi_p2/mapping.py only.
"""
import datetime
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from src.engine import ThumbnailCompositor  # noqa: E402  (loads text_thai / raqm first)
from src.engine.graphics import apply_avatar_separation  # noqa: E402
from projects.aomi_p2.mapping import TIMELINES, MODEL_DIR  # noqa: E402

FRAMES = Path(sys.argv[1])
DATE = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else datetime.date.today().isoformat()
ONLY = None
if "--only" in sys.argv:
    ONLY = {int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")}

OUT = ROOT / "outputs" / "aomi" / DATE
REP = ROOT / "reports" / "aomi" / DATE
OUT.mkdir(parents=True, exist_ok=True)
REP.mkdir(parents=True, exist_ok=True)

comp = ThumbnailCompositor()
_cache = {}


def safe(name):
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip()


def avatar(path, target_h):
    key = (path, target_h)
    if key not in _cache:
        im = Image.open(Path(MODEL_DIR) / path).convert("RGBA")
        im = im.crop(im.split()[3].getbbox())  # visible bbox only
        w = round(im.width * target_h / im.height)
        _cache[key] = im.resize((w, target_h), Image.Resampling.LANCZOS)
    return _cache[key]


def land_bg(frame, talk):
    if talk:  # intermission / chat scenes: heavy blur so the stream overlay vanishes
        bg = frame.resize((1920, 1080), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(40))
        bg = ImageEnhance.Brightness(bg).enhance(0.55)
        return ImageEnhance.Color(bg).enhance(1.15)
    # gameplay: crop away the in-stream avatar overlay (bottom-left) and scale to 16:9, 0px blur
    return frame.crop((640, 0, 1920, 720)).resize((1920, 1080), Image.Resampling.LANCZOS)


def short_bg(frame, talk):
    bg = frame.resize((1080, 1920), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(36))
    bg = ImageEnhance.Brightness(bg).enhance(0.5)
    bg = ImageEnhance.Color(bg).enhance(1.15).convert("RGBA")
    if talk:  # intermission scenes already contain the stream avatar; no sharp panel
        return bg
    panel = frame.crop((640, 0, 1920, 720)).resize((1080, 607), Image.Resampling.LANCZOS).convert("RGBA")
    bg.alpha_composite(panel, (0, 600))
    return bg


manifest = []
for t in TIMELINES:
    if ONLY and t["id"] not in ONLY:
        continue
    frame = Image.open(FRAMES / f"{t['id']:02d}.png").convert("RGB")
    land_av = avatar(t["model_file"], 900)
    land = comp.composite_landscape(
        bg_image=land_bg(frame, t["talk"]).convert("RGBA"),
        avatar_image=land_av,
        hook_lines=t["hook"], secondary_lines=t["sec"],
        avatar_pos=(1920 - land_av.width - 20, 1080 - 900),
        is_gameplay=True,  # bg already prepared (talk scenes pre-blurred in land_bg)
    )
    # Shorts: text is drawn by the compositor, avatar is pasted flush to the bottom edge
    # (the compositor's own placement leaves the separation padding as a visible gap).
    short = comp.composite_shorts(
        bg_image=short_bg(frame, t["talk"]), avatar_image=None,
        hook_lines=t["hook"], secondary_lines=t["sec"],
    ).convert("RGBA")
    s_av = avatar(t["model_file"], 860)
    s_sep = apply_avatar_separation(s_av)
    pad = (s_sep.height - s_av.height) // 2
    short.alpha_composite(s_sep, ((1080 - s_sep.width) // 2, 1920 - s_sep.height + pad))
    short = short.convert("RGB")
    for img, nm, ori in ((land, t["name"], "landscape"), (short, t["tl_short"], "shorts")):
        fn = safe(nm) + ".jpg"
        img.save(OUT / fn, quality=92)
        manifest.append({
            "timeline": nm, "file": fn, "orientation": ori, "size": list(img.size),
            "hook": t["hook"], "secondary": t["sec"], "model": t["model_file"],
            "source": t["src"], "source_time_s": round(t["src_start"] + t["frame_tl"], 3),
            "evidence": t["evidence"], "flag": t["flag"],
        })

(REP / "delivery-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print("built", len(manifest), "images ->", OUT)
