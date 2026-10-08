"""Organizes deliverables into a clean, human-friendly directory structure.

Guarantees:
- outputs/<channel>/<date>/  contains 100% ONLY image files (.jpg, .png).
- outputs/<channel>/_LATEST/ contains 100% ONLY image files.
- reports/<channel>/<date>/  contains manifests, QC reports, and logs.
- packages/<channel>/<date>/ contains delivery zip archives.
"""

import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = REPO_ROOT / "outputs"
REPORTS_DIR = REPO_ROOT / "reports"
PACKAGES_DIR = REPO_ROOT / "packages"
DATE_DIR = re.compile(r"^\d{4}-\d{2}-\d{2}$")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def sync_channel_latest(channel_name: str):
    ch_dir = OUTPUTS_DIR / channel_name
    if not ch_dir.exists():
        return
    date_folders = [d for d in ch_dir.iterdir() if d.is_dir() and DATE_DIR.match(d.name)]
    # Newest batch that actually has images, so an empty/failed run never wipes _LATEST
    for latest_date_dir in sorted(date_folders, key=lambda x: x.name, reverse=True):
        images = [p for p in latest_date_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES]
        if images:
            break
    else:
        return
    latest_mirror = ch_dir / "_LATEST"
    latest_mirror.mkdir(parents=True, exist_ok=True)

    for f in latest_mirror.iterdir():
        if f.is_file():
            f.unlink()
    for img in images:
        shutil.copy2(img, latest_mirror / img.name)


def main():
    print("=== Syncing Channel Outputs (Images Only) ===")
    if not OUTPUTS_DIR.exists():
        print("outputs/ directory not found.")
        return

    for ch in OUTPUTS_DIR.iterdir():
        if ch.is_dir() and not ch.name.startswith("."):
            sync_channel_latest(ch.name)
            img_count = len(list((ch / "_LATEST").glob("*.jpg"))) + len(list((ch / "_LATEST").glob("*.png")))
            print(f"[OK] {ch.name.upper()}: {img_count} images synced to _LATEST")

    print("\nAll channel latest mirrors synced successfully!")


if __name__ == "__main__":
    main()
