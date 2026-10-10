"""Extract one source frame per Aomi p2 timeline (source time = src_start + frame_tl) and a contact sheet."""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from projects.aomi_p2.mapping import TIMELINES  # noqa: E402

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)


def grab(t):
    dst = OUT / f"{t['id']:02d}.png"
    if not dst.exists():
        ts = t["src_start"] + t["frame_tl"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ts:.3f}", "-i", t["src"], "-frames:v", "1", str(dst)], check=True)
    return dst


with ThreadPoolExecutor(6) as ex:
    list(ex.map(grab, TIMELINES))

W, H, C = 480, 270, 6
rows = (len(TIMELINES) + C - 1) // C
sheet = Image.new("RGB", (W * C, H * rows))
for i, t in enumerate(TIMELINES):
    im = Image.open(OUT / f"{t['id']:02d}.png").convert("RGB").resize((W, H))
    sheet.paste(im, ((i % C) * W, (i // C) * H))
sheet.save(OUT / "contact.jpg", quality=80)
print("done", len(TIMELINES))
