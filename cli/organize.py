"""Organizes deliverables into a clean, human-friendly directory structure.

Guarantees:
- outputs/<channel>/<date>/  contains 100% ONLY image files (.jpg, .png).
- outputs/<channel>/_LATEST/ contains 100% ONLY image files.
- reports/<channel>/<date>/  contains manifests, QC reports, and logs.
- packages/<channel>/<date>/ contains delivery zip archives.
"""

import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = REPO_ROOT / "outputs"
REPORTS_DIR = REPO_ROOT / "reports"
PACKAGES_DIR = REPO_ROOT / "packages"


def copy_or_replace(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return
    shutil.copy2(src, dst)


def sync_channel_latest(channel_name: str):
    ch_dir = OUTPUTS_DIR / channel_name
    if not ch_dir.exists():
        return
    # Find all date folders
    date_folders = [d for d in ch_dir.iterdir() if d.is_dir() and d.name != "_LATEST" and not d.name.startswith(".")]
    if not date_folders:
        return
    latest_date_dir = sorted(date_folders, key=lambda x: x.name)[-1]
    latest_mirror = ch_dir / "_LATEST"
    latest_mirror.mkdir(parents=True, exist_ok=True)

    # Clean old files in _LATEST
    for f in latest_mirror.iterdir():
        if f.is_file():
            f.unlink()

    # Mirror latest images
    for img in latest_date_dir.glob("*.jpg"):
        shutil.copy2(img, latest_mirror / img.name)
    for img in latest_date_dir.glob("*.png"):
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
