"""Zip the delivered JPGs (named after the timelines) plus the manifest, then re-open every JPG from the zip."""
import io
import json
import zipfile
from pathlib import Path

from PIL import Image

OUT = Path(r"D:\agent-thumbnail\outputs\aomi-debut-20260731")
ZIP = OUT / "AOMI-MAMA-Debut-2026-07-31-Timeline-Covers.zip"
items = json.loads((OUT / "delivery-manifest.json").read_text(encoding="utf-8"))
with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for it in items:
        p = Path(it["path"])
        zf.write(p, arcname=p.name)
    zf.write(OUT / "delivery-manifest.json", arcname="delivery-manifest.json")
with zipfile.ZipFile(ZIP) as zf:
    assert zf.testzip() is None
    jpgs = [n for n in zf.namelist() if n.endswith(".jpg")]
    for n in jpgs:
        with Image.open(io.BytesIO(zf.read(n))) as im:
            im.load()
            assert im.format == "JPEG"
print(json.dumps({"zip": str(ZIP), "bytes": ZIP.stat().st_size, "jpgs": len(jpgs)}, ensure_ascii=False))
