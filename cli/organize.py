"""Organizes raw output folders into a human-friendly, channel-based directory structure.

Outputs are organized into:
    outputs/channels/<channel_name>/<date>/
        ├── 16x9_Landscape/
        ├── 9x16_Shorts/
        ├── _summary_previews/
        ├── _reports/
        └── <package>.zip

Also creates/updates:
    outputs/channels/<channel_name>/_LATEST
    outputs/_LATEST_DELIVERY
"""

import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = REPO_ROOT / "outputs"
CHANNELS_DIR = OUTPUTS_DIR / "channels"


def copy_or_link(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return
    # Use copyfile so Windows without dev privileges works seamlessly
    shutil.copy2(src, dst)


def organize_katy404():
    source_dir = OUTPUTS_DIR / "2026-10-04" / "Katy404-2026-09-29"
    if not source_dir.exists():
        source_dir = OUTPUTS_DIR / "katy404-20260929"
    if not source_dir.exists():
        return None

    target_date = "2026-09-29"
    target_dir = CHANNELS_DIR / "katy404" / target_date
    land_dir = target_dir / "16x9_Landscape"
    shorts_dir = target_dir / "9x16_Shorts"
    previews_dir = target_dir / "_summary_previews"
    reports_dir = target_dir / "_reports"

    # Landscape
    src_land = source_dir / "jpg"
    if src_land.exists():
        for f in src_land.glob("*.jpg"):
            copy_or_link(f, land_dir / f.name)

    # Shorts
    src_shorts = source_dir / "jpg-shorts-v2"
    if not src_shorts.exists():
        src_shorts = source_dir / "jpg"
    if src_shorts.exists():
        for f in src_shorts.glob("*.jpg"):
            if "9x16" in f.name or src_shorts.name == "jpg-shorts-v2":
                copy_or_link(f, shorts_dir / f.name)

    # Zip
    for zip_file in source_dir.glob("*.zip"):
        copy_or_link(zip_file, target_dir / zip_file.name)

    # Previews
    src_prev = source_dir / "previews-shorts-v2"
    if src_prev.exists():
        for f in src_prev.glob("*.jpg"):
            copy_or_link(f, previews_dir / f.name)

    # Reports
    for r in ["delivery-manifest.json", "delivery-manifest-shorts-v2.json", "qc-summary.md", "qc-shorts-v2.md"]:
        f = source_dir / r
        if f.exists():
            copy_or_link(f, reports_dir / f.name)

    # Channel Latest
    update_latest(CHANNELS_DIR / "katy404" / "_LATEST", target_dir)
    return target_dir


def organize_tygarina():
    # Use latest version v7
    source_dir = OUTPUTS_DIR / "tygarina-20260801-v7"
    if not source_dir.exists():
        source_dir = OUTPUTS_DIR / "tygarina-20260801"
    if not source_dir.exists():
        return None

    target_date = "2026-08-01"
    target_dir = CHANNELS_DIR / "tygarina" / target_date
    land_dir = target_dir / "16x9_Landscape"
    shorts_dir = target_dir / "9x16_Shorts"
    previews_dir = target_dir / "_summary_previews"
    reports_dir = target_dir / "_reports"

    src_jpg = source_dir / "jpg"
    if src_jpg.exists():
        for f in src_jpg.glob("*.jpg"):
            if "_9x16" in f.name or "-short" in f.name:
                copy_or_link(f, shorts_dir / f.name)
            else:
                copy_or_link(f, land_dir / f.name)

    for zip_file in source_dir.glob("*.zip"):
        copy_or_link(zip_file, target_dir / zip_file.name)

    for prev in source_dir.glob("overview-*.jpg"):
        copy_or_link(prev, previews_dir / prev.name)

    for r in ["delivery-manifest.json", "timeline-audit.json"]:
        f = source_dir / r
        if f.exists():
            copy_or_link(f, reports_dir / f.name)

    update_latest(CHANNELS_DIR / "tygarina" / "_LATEST", target_dir)
    return target_dir


def organize_armigon():
    source_dir = OUTPUTS_DIR / "armigon-20260920-final-20260928"
    if not source_dir.exists():
        return None

    target_date = "2026-09-20"
    target_dir = CHANNELS_DIR / "armigon" / target_date
    land_dir = target_dir / "16x9_Landscape"
    shorts_dir = target_dir / "9x16_Shorts"
    previews_dir = target_dir / "_summary_previews"
    reports_dir = target_dir / "_reports"

    src_jpg = source_dir / "jpg"
    if src_jpg.exists():
        for f in src_jpg.glob("*.jpg"):
            if "-short" in f.name or "_9x16" in f.name:
                copy_or_link(f, shorts_dir / f.name)
            else:
                copy_or_link(f, land_dir / f.name)

    for zip_file in source_dir.glob("*.zip"):
        copy_or_link(zip_file, target_dir / zip_file.name)

    for prev in list(source_dir.glob("review-*.jpg")) + list(source_dir.glob("crop-*.jpg")):
        copy_or_link(prev, previews_dir / prev.name)

    for r in ["delivery-manifest.json", "cover-plan.json", "resolve-audit.json"]:
        f = source_dir / r
        if f.exists():
            copy_or_link(f, reports_dir / f.name)

    update_latest(CHANNELS_DIR / "armigon" / "_LATEST", target_dir)
    return target_dir


def organize_aomi():
    source_dir = OUTPUTS_DIR / "aomi-debut-20260731-noblur"
    if not source_dir.exists():
        source_dir = OUTPUTS_DIR / "aomi-debut-20260731"
    if not source_dir.exists():
        return None

    target_date = "2026-07-31"
    target_dir = CHANNELS_DIR / "aomi_debut" / target_date
    land_dir = target_dir / "16x9_Landscape"
    shorts_dir = target_dir / "9x16_Shorts"
    previews_dir = target_dir / "_summary_previews"
    reports_dir = target_dir / "_reports"

    src_jpg = source_dir / "jpg"
    if src_jpg.exists():
        for f in src_jpg.glob("*.jpg"):
            if "-short" in f.name or "_9x16" in f.name:
                copy_or_link(f, shorts_dir / f.name)
            else:
                copy_or_link(f, land_dir / f.name)

    for zip_file in source_dir.glob("*.zip"):
        copy_or_link(zip_file, target_dir / zip_file.name)

    for prev in source_dir.glob("overview-*.jpg"):
        copy_or_link(prev, previews_dir / prev.name)

    for r in ["delivery-manifest.json"]:
        f = source_dir / r
        if f.exists():
            copy_or_link(f, reports_dir / f.name)

    update_latest(CHANNELS_DIR / "aomi_debut" / "_LATEST", target_dir)
    return target_dir


def update_latest(link_target: Path, actual_target: Path):
    """Creates a shortcut folder or syncs a mirror directory for instant access."""
    link_target.mkdir(parents=True, exist_ok=True)
    # Write a quick text pointer and readme
    readme = link_target / "OPEN_LATEST.url"
    url_content = f"[InternetShortcut]\nURL=file:///{str(actual_target.resolve()).replace(chr(92), '/')}\n"
    readme.write_text(url_content, encoding="utf-8")

    # Also mirror the landscape and shorts folders for zero-click access
    for sub in ["16x9_Landscape", "9x16_Shorts"]:
        src_sub = actual_target / sub
        dst_sub = link_target / sub
        if src_sub.exists():
            dst_sub.mkdir(parents=True, exist_ok=True)
            for f in src_sub.glob("*.jpg"):
                copy_or_link(f, dst_sub / f.name)


def main():
    print("=== Organizing Outputs by Channel ===")
    res_katy = organize_katy404()
    if res_katy:
        print(f"[OK] Katy404 -> {res_katy}")

    res_tyg = organize_tygarina()
    if res_tyg:
        print(f"[OK] Tygarina -> {res_tyg}")

    res_arm = organize_armigon()
    if res_arm:
        print(f"[OK] Armigon -> {res_arm}")

    res_aomi = organize_aomi()
    if res_aomi:
        print(f"[OK] Aomi Debut -> {res_aomi}")

    # Top-level global latest
    latest_global = OUTPUTS_DIR / "_LATEST_DELIVERY"
    latest_global.mkdir(parents=True, exist_ok=True)
    if res_katy:
        update_latest(latest_global, res_katy)
        print(f"[OK] Global Latest updated -> Katy404 ({res_katy})")

    print("\nAll channel deliverables organized successfully!")
    print(f"Directory: {CHANNELS_DIR.resolve()}")


if __name__ == "__main__":
    main()
