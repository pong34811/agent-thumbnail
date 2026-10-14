"""Build Aomi p1 covers (49 clips x 16:9 + 9:16) from real source frames and RGBA avatars.

Usage: python build_aomi_p1_covers.py <frames_dir> [date] [--only N,N]
frames_dir holds NN.png from aomi_p1_extract_frames.py. Hook/sec/model come from
projects/aomi_p1/mapping.py only.
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
from projects.aomi_p1.mapping import TIMELINES, MODEL_DIR  # noqa: E402

FRAMES = Path(sys.argv[1])
DATE = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else datetime.date.today().isoformat()
ONLY = None
if "--only" in sys.argv:
    ONLY = {int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")}

OUT = ROOT / "outputs" / "aomi" / DATE
REP = ROOT / "reports" / "aomi" / DATE
OUT.mkdir(parents=True, exist_ok=True)
REP.mkdir(parents=True, exist_ok=True)

from src.engine.layout import ShortsLayout  # noqa: E402
ShortsLayout.TEXT_MAX_WIDTH = 700  # centred hook must stay left of the Shorts right-15% zone (x<=918)
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


# Desktop screen-share frames (Steam / File Explorer): boxes measured on a coordinate grid so the small
# stream avatar (#18/#36 bottom-right x>=1430,y>=596; #19/#49 bottom-left x<=720,y>=530) stays outside.
# #18 (Steam banner @31s): below the username bar (y>=80), left of the avatar; #49 (game title menu @24s): right of the room panel/avatar hair (x>=600).
# #11 (@0s): top-left corner keeps the snowy window, ears of the stream avatar start at y~530.
# #39 (@13s): lava block sits in the top-left corner (x 80-410, y 5-180).
BOX_OVERRIDE = {11: (0, 0, 912, 513), 39: (0, 0, 912, 513), 18: (340, 80, 1430, 693), 36: (0, 0, 1430, 804), 19: (216, 16, 1442, 530), 49: (600, 0, 1920, 743)}


def game_box(frame, src, tid=None):
    """Game area inside the OBS scene. Alien Shooter files shrink the game top-left with a room panel
    (right) + teal bar (bottom) and the stream avatar bottom-RIGHT; other clips are full-screen with the
    avatar bottom-LEFT. Boxes were measured from frame edges (alien shooter 2 is 4:3, alien shooter 16:9)."""
    if tid in BOX_OVERRIDE:
        return BOX_OVERRIDE[tid]
    r, g, b = frame.getpixel((frame.width // 2, frame.height - 5))
    if abs(r - 45) < 25 and abs(g - 127) < 25 and abs(b - 126) < 25:  # teal bottom bar
        return (0, 0, 1305, 978) if "alien shooter 2" in src else (0, 0, 1668, 938)
    return (640, 0, 1920, 720)  # crop away the bottom-left stream avatar


def cover(im, size):
    """Scale to cover `size` (no stretch) and centre-crop."""
    k = max(size[0] / im.width, size[1] / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.Resampling.LANCZOS)
    x, y = (im.width - size[0]) // 2, (im.height - size[1]) // 2
    return im.crop((x, y, x + size[0], y + size[1]))


def land_bg(frame, talk, src, tid=None):
    if talk:  # intermission / chat scenes: heavy blur so the stream overlay vanishes
        bg = frame.resize((1920, 1080), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(40))
        bg = ImageEnhance.Brightness(bg).enhance(0.55)
        return ImageEnhance.Color(bg).enhance(1.15)
    return cover(frame.crop(game_box(frame, src, tid)), (1920, 1080))  # gameplay, 0px blur


def short_bg(frame, talk, src, tid=None):
    bg = frame.resize((1080, 1920), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(36))
    bg = ImageEnhance.Brightness(bg).enhance(0.5)
    bg = ImageEnhance.Color(bg).enhance(1.15).convert("RGBA")
    if talk:  # intermission scenes already contain the stream avatar; no sharp panel
        return bg
    panel = cover(frame.crop(game_box(frame, src, tid)), (1080, 640)).convert("RGBA")
    bg.alpha_composite(panel, (0, 600))
    return bg


manifest = []
for t in TIMELINES:
    if ONLY and t["id"] not in ONLY:
        continue
    frame = Image.open(FRAMES / f"{t['id']:02d}.png").convert("RGB")
    land_av = avatar(t["model_file"], 900)
    land = comp.composite_landscape(
        bg_image=land_bg(frame, t["talk"], t["src"], t["id"]).convert("RGBA"),
        avatar_image=land_av,
        hook_lines=t["hook"], secondary_lines=t["sec"],
        avatar_pos=(1920 - land_av.width - 20, 1080 - 900),
        is_gameplay=True,  # bg already prepared (talk scenes pre-blurred in land_bg)
    )
    # Shorts: text is drawn by the compositor, avatar is pasted flush to the bottom edge
    # (the compositor's own placement leaves the separation padding as a visible gap).
    short = comp.composite_shorts(
        bg_image=short_bg(frame, t["talk"], t["src"], t["id"]), avatar_image=None,
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
            "source": t["src"], "source_time_s": round(t.get("frame_abs") or (t["src_start"] + t["frame_tl"]), 3),
            "evidence": t["evidence"], "flag": t["flag"],
        })

(REP / "delivery-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print("built", len(manifest), "images ->", OUT)
