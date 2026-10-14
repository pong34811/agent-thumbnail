"""Build Tygarina 0930 covers (44 clips x 16:9 + 9:16) from real source frames and RGBA avatars.

Usage: python build_tygarina_0930_covers.py <frames_dir> [date] [--only N,N]
frames_dir holds NN.png from tygarina_0930_extract_frames.py. Hook/sec/model come from
projects/tygarina_0930/mapping.py only.
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
from src.engine.graphics import apply_avatar_separation, create_backdrop_gradient  # noqa: E402
from projects.tygarina_0930.mapping import TIMELINES, MODEL_DIR  # noqa: E402

FRAMES = Path(sys.argv[1])
DATE = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else datetime.date.today().isoformat()
ONLY = None
if "--only" in sys.argv:
    ONLY = {int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")}

OUT = ROOT / "outputs" / "tygarina" / DATE
REP = ROOT / "reports" / "tygarina" / DATE
OUT.mkdir(parents=True, exist_ok=True)
REP.mkdir(parents=True, exist_ok=True)

from src.engine.layout import ShortsLayout  # noqa: E402
ShortsLayout.TEXT_MAX_WIDTH = 700  # centred hook must stay left of the Shorts right-15% zone (x<=918)
comp = ThumbnailCompositor()
_cache = {}
CROP_BOTTOM = {"dsasa.png": 2750, "dsadadsad.png": 2750}
ALPHA_CLEAR = {"dsadadsad.png": [(500, 2240, 960, 2800)]}


def safe(name):
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip()


def avatar(path, target_h, cap=None):
    cap = cap or target_h
    key = (path, target_h, cap)
    if key not in _cache:
        im = Image.open(Path(MODEL_DIR) / path).convert("RGBA")
        if path in CROP_BOTTOM:  # full-body render -> bust-up
            a = im.split()[3]
            for box in ALPHA_CLEAR.get(path, []):  # faint uncoloured line-art in the asset
                a.paste(0, box)
            im.putalpha(a)
            im = im.crop((0, 0, im.width, CROP_BOTTOM[path]))
        im = im.crop(im.split()[3].getbbox())  # visible bbox only
        w = round(im.width * target_h / im.height)
        if w > cap:  # wide bust crops (21.png): cap width so the avatar never reaches the hook text
            w, target_h = cap, round(im.height * cap / im.width)
        _cache[key] = im.resize((w, target_h), Image.Resampling.LANCZOS)
    return _cache[key]


def land_bg(frame, talk):
    if talk:  # intermission / chat scenes: heavy blur so the stream overlay vanishes
        bg = frame.resize((1920, 1080), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(28))
        bg = ImageEnhance.Brightness(bg).enhance(0.5)
        bg = ImageEnhance.Color(bg).enhance(1.15).convert("RGBA")
        # extra left scrim so the red hook does not sit on a warm (red/orange) blur
        bg.alpha_composite(create_backdrop_gradient((1920, 1080), fade_start_x=0, fade_end_x=1100, max_alpha=0.6))
        return bg
    # gameplay: crop away the in-stream avatar overlay (bottom-left) and scale to 16:9, 0px blur
    return frame.crop((640, 0, 1920, 720)).resize((1920, 1080), Image.Resampling.LANCZOS)


def short_bg(frame, talk):
    bg = frame.resize((1080, 1920), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(36))
    bg = ImageEnhance.Brightness(bg).enhance(0.4)
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
    if frame.size != (1920, 1080):  # some sources are 1280x720; the crop boxes below assume 1920x1080
        frame = frame.resize((1920, 1080), Image.Resampling.LANCZOS)
    land_av = avatar(t["model_file"], 900)
    land = comp.composite_landscape(
        bg_image=land_bg(frame, t["talk"]).convert("RGBA"),
        avatar_image=land_av,
        hook_lines=t["hook"], secondary_lines=t["sec"],
        avatar_pos=(1920 - land_av.width - 20, 1080 - land_av.height),
        is_gameplay=True,  # bg already prepared (talk scenes pre-blurred in land_bg)
    )
    # Shorts: text is drawn by the compositor, avatar is pasted flush to the bottom edge
    # (the compositor's own placement leaves the separation padding as a visible gap).
    short = comp.composite_shorts(
        bg_image=short_bg(frame, t["talk"]), avatar_image=None,
        hook_lines=t["hook"], secondary_lines=t["sec"],
    ).convert("RGBA")
    s_av = avatar("dsadadsad.png" if t["model_file"] == "21.png" else t["model_file"], 860)  # 21.png close-up puts the face in the Shorts bottom 25%
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
