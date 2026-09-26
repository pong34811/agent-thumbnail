"""Sample source frames for every timeline cue and build one labelled sheet per timeline."""
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
SRC = ROOT / "src.mp4"
FONT = r"D:\agent-thumbnail\outputs\timeline-covers\fonts\Mitr-Bold.ttf"
FPS = 60.0
audit = json.loads((ROOT / "timeline-audit.json").read_text(encoding="utf-8"))
textplus = json.loads((ROOT / "notes" / "textplus_before_improve.json").read_text(encoding="utf-8"))
ROV_TEXTS = textplus["SeqContainer/08403901-e3ad-4141-bd8b-97b6130daac1.xml"]


def cues(t):
    for tr in t["tracks"]["subtitle"]:
        if tr["items"]:
            return [(it["start"], it["end"], it["name"]) for it in tr["items"]]
    # "เคยเล่น Rov ไหม" has no subtitle track: its captions are 17 Text+ items.
    for tr in t["tracks"]["video"]:
        items = [it for it in tr["items"] if it["name"] == "Text+"]
        if items:
            assert len(items) == len(ROV_TEXTS)
            return [(it["start"], it["end"], txt) for it, txt in zip(items, ROV_TEXTS)]
    return []


def source_frame(t, tf):
    for it in t["tracks"]["video"][0]["items"]:
        if it["start"] <= tf < it["end"] and "src_start" in it:
            zoom = (it.get("xf") or {}).get("ZoomX", 1.0)
            return it["src_start"] + (tf - it["start"]), zoom
    return None, None


def overlays(t, tf):
    names = []
    for tr in t["tracks"]["video"][1:]:
        for it in tr["items"]:
            if it["start"] <= tf < it["end"] and it["name"] != "Text+":
                names.append(it["name"])
    return names


def main():
    font = ImageFont.truetype(FONT, 18)
    plan = {}
    for t in audit["timelines"]:
        idx = t["index"]
        out_dir = ROOT / "frames" / f"tl{idx}"
        out_dir.mkdir(parents=True, exist_ok=True)
        cs = cues(t)
        step = max(1, len(cs) // 30 + (1 if len(cs) % 30 else 0)) if len(cs) > 30 else 1
        picks = cs[::step]
        recs = []
        for n, (a, b, text) in enumerate(picks):
            tf = (a + b) // 2
            sf, zoom = source_frame(t, tf)
            if sf is None:
                continue
            path = out_dir / f"tf{tf:05d}.jpg"
            if not path.exists():
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{sf / FPS:.4f}",
                                "-i", str(SRC), "-frames:v", "1", "-vf", "scale=640:-2", "-q:v", "3", str(path)], check=True)
            recs.append({"tf": tf, "sf": sf, "sec": round(sf / FPS, 3), "zoom": zoom, "text": text,
                         "overlays": overlays(t, tf), "path": str(path)})
        plan[idx] = {"name": t["name"], "frames": recs}
        cols = 5
        cw, ch = 640, 360 + 64
        rows = (len(recs) + cols - 1) // cols
        sheet = Image.new("RGB", (cw * cols, ch * rows), (24, 24, 30))
        d = ImageDraw.Draw(sheet)
        for n, r in enumerate(recs):
            x, y = (n % cols) * cw, (n // cols) * ch
            with Image.open(r["path"]) as im:
                sheet.paste(im.convert("RGB"), (x, y + 64))
            d.text((x + 6, y + 4), f"#{n + 1} tf{r['tf']} z{r['zoom']} {'+'.join(r['overlays'])[:40]}", font=font, fill=(255, 220, 90))
            d.text((x + 6, y + 30), r["text"][:40], font=font, fill="white")
        sheet.save(ROOT / "frames" / f"sheet-tl{idx}.jpg", quality=82)
        print(idx, t["name"], len(recs))
    (ROOT / "frames" / "sample-plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
