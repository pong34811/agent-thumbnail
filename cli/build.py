"""Unified CLI to build VTuber thumbnails for YouTube Landscape (16:9) and Shorts (9:16).

Enforces:
- outputs/<channel>/<date>/ contains 100% ONLY image files.
- reports/<channel>/<date>/ stores manifests and QC logs.
- Auto-opens Windows File Explorer for the user.
"""

import argparse
import datetime
import importlib
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.engine import (
    ThumbnailCompositor,
    LANDSCAPE_DIMS,
    SHORTS_DIMS,
)
from cli.open import open_folder
from cli.organize import sync_channel_latest

OUTPUTS_DIR = REPO_ROOT / "outputs"
REPORTS_DIR = REPO_ROOT / "reports"


def load_project_mapping(project_name: str) -> Dict[str, Any]:
    """Dynamically loads the mapping module for the given project."""
    norm_name = project_name.lower().replace("-", "_")
    module_path = f"projects.{norm_name}.mapping"
    try:
        mod = importlib.import_module(module_path)
        return {
            "name": getattr(mod, "PROJECT_NAME", norm_name),
            "channel": getattr(mod, "CHARACTER_NAME", norm_name),
            "timelines": getattr(mod, "TIMELINES", {}),
            "accents": getattr(mod, "ACCENTS", {}),
        }
    except ModuleNotFoundError:
        for p in (REPO_ROOT / "projects").iterdir():
            if p.is_dir() and p.name.lower().replace("-", "_") == norm_name:
                mod = importlib.import_module(f"projects.{p.name}.mapping")
                return {
                    "name": getattr(mod, "PROJECT_NAME", p.name),
                    "channel": getattr(mod, "CHARACTER_NAME", p.name),
                    "timelines": getattr(mod, "TIMELINES", {}),
                    "accents": getattr(mod, "ACCENTS", {}),
                }
        raise ValueError(f"Project mapping '{project_name}' not found under projects/")


def _lines(value) -> Optional[List[str]]:
    if isinstance(value, str):
        return [value]
    return list(value) if value else None


def resolve_text(tl: Dict[str, Any], key: str, orientation: str) -> Optional[List[str]]:
    """Reads hook/sec for one orientation: nested `land`/`short` block first, then top level."""
    nested = tl.get("land" if orientation == "landscape" else "short")
    if isinstance(nested, dict) and nested.get(key):
        return _lines(nested[key])
    value = _lines(tl.get(key))
    if value is None and key == "hook" and " - " in (tl.get("title") or ""):
        value = [tl["title"].split(" - ", 1)[1].strip()]
    return value


def load_image_safe(path: Optional[str], default_dims: Tuple[int, int]) -> Image.Image:
    if path and Path(path).is_file():
        try:
            return Image.open(path).convert("RGBA")
        except Exception as e:
            print(f"Warning: Failed to load image {path}: {e}")
    return Image.new("RGBA", default_dims, (20, 24, 38, 255))


def build_adhoc_thumbnail(
    channel: str,
    hook: List[str],
    sec: Optional[List[str]] = None,
    bg_path: Optional[str] = None,
    avatar_path: Optional[str] = None,
    date_str: Optional[str] = None,
    orientation: str = "all",
    font_path: Optional[str] = None,
    focus_circle: Optional[Tuple[int, int, int]] = None,
    emotion_marker: Optional[Tuple[str, Tuple[int, int]]] = None,
    auto_open: bool = True,
) -> Dict[str, Any]:
    """Builds an ad-hoc thumbnail and places image files directly in outputs/<channel>/<date>/."""
    ch_clean = channel.lower().replace("-", "_")
    target_date = date_str or datetime.date.today().strftime("%Y-%m-%d")
    output_dir = OUTPUTS_DIR / ch_clean / target_date
    reports_dir = REPORTS_DIR / ch_clean / target_date

    output_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    compositor = ThumbnailCompositor(font_path=font_path)

    bg_img = load_image_safe(bg_path, LANDSCAPE_DIMS)
    avatar_img = Image.open(avatar_path).convert("RGBA") if avatar_path and Path(avatar_path).is_file() else None

    safe_title = "_".join(hook)
    safe_title = "".join(c if c.isalnum() or c in " -_ก-๙" else "_" for c in safe_title).strip() or "thumbnail"

    manifest = []
    # 1. Landscape
    if orientation in ("all", "landscape"):
        img = compositor.composite_landscape(
            bg_image=bg_img,
            avatar_image=avatar_img,
            hook_lines=hook,
            secondary_lines=sec,
            focus_circle=focus_circle,
            emotion_marker=emotion_marker,
        )
        out_file = output_dir / f"{safe_title}.jpg"
        img.save(out_file, quality=92)
        manifest.append({
            "title": safe_title,
            "file": out_file.name,
            "path": str(out_file),
            "orientation": "landscape",
            "size": list(LANDSCAPE_DIMS),
        })

    # 2. Shorts
    if orientation in ("all", "short", "shorts"):
        shorts_bg = load_image_safe(bg_path, SHORTS_DIMS)
        img = compositor.composite_shorts(
            bg_image=shorts_bg,
            avatar_image=avatar_img,
            hook_lines=hook,
            secondary_lines=sec,
            emotion_marker=emotion_marker,
        )
        out_file = output_dir / f"{safe_title}-short.jpg"
        img.save(out_file, quality=92)
        manifest.append({
            "title": safe_title,
            "file": out_file.name,
            "path": str(out_file),
            "orientation": "shorts",
            "size": list(SHORTS_DIMS),
        })

    # Write manifest into reports/
    man_file = reports_dir / "delivery-manifest.json"
    man_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # Update latest mirror
    sync_channel_latest(ch_clean)

    latest_dir = OUTPUTS_DIR / ch_clean / "_LATEST"
    if auto_open:
        open_folder(latest_dir)

    return {
        "status": "success",
        "channel": channel,
        "date": target_date,
        "output_dir": str(output_dir),
        "latest_link": f"file:///{str(latest_dir.resolve()).replace(chr(92), '/')}",
        "generated_count": len(manifest),
    }


def build_project_batch(
    project_name: str,
    orientation: str = "all",
    font_path: Optional[str] = None,
    auto_open: bool = True,
) -> Dict[str, Any]:
    """Builds full timeline batch from a project mapping file."""
    mapping = load_project_mapping(project_name)
    timelines = mapping["timelines"]
    channel_name = mapping.get("channel", project_name).lower().replace("-", "_")

    target_date = datetime.date.today().strftime("%Y-%m-%d")
    output_dir = OUTPUTS_DIR / channel_name / target_date
    reports_dir = REPORTS_DIR / channel_name / target_date

    output_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    compositor = ThumbnailCompositor(font_path=font_path)
    manifest = []

    items = timelines.values() if isinstance(timelines, dict) else timelines

    for idx, tl in enumerate(items, start=1):
        tl_title = tl.get("title") or tl.get("name") or f"timeline_{idx}"
        safe_title = "".join(c if c.isalnum() or c in " -_ก-๙" else "_" for c in tl_title).strip()

        focus_circle = tl.get("focus_circle")
        emotion_marker = tl.get("emotion_marker")

        av_img = None
        av_path = tl.get("avatar") or tl.get("model_file") or tl.get("model")
        if av_path and Path(av_path).is_file():
            av_img = Image.open(av_path).convert("RGBA")

        bg_path = tl.get("frame_path") or tl.get("bg") or tl.get("video")
        dummy_bg = load_image_safe(bg_path, LANDSCAPE_DIMS)

        # 1. Landscape
        if orientation in ("all", "landscape"):
            land_img = compositor.composite_landscape(
                bg_image=dummy_bg,
                avatar_image=av_img,
                hook_lines=resolve_text(tl, "hook", "landscape"),
                secondary_lines=resolve_text(tl, "sec", "landscape"),
                focus_circle=focus_circle,
                emotion_marker=emotion_marker,
            )
            land_file = output_dir / f"{safe_title}.jpg"
            land_img.save(land_file, quality=92)
            manifest.append({
                "title": tl_title,
                "file": land_file.name,
                "orientation": "landscape",
                "path": str(land_file),
            })

        # 2. Shorts
        if orientation in ("all", "short", "shorts"):
            dummy_shorts = load_image_safe(bg_path, SHORTS_DIMS)
            short_img = compositor.composite_shorts(
                bg_image=dummy_shorts,
                avatar_image=av_img,
                hook_lines=resolve_text(tl, "hook", "shorts"),
                secondary_lines=resolve_text(tl, "sec", "shorts"),
                emotion_marker=emotion_marker,
            )
            short_file = output_dir / f"{safe_title}-short.jpg"
            short_img.save(short_file, quality=92)
            manifest.append({
                "title": tl_title,
                "file": short_file.name,
                "orientation": "shorts",
                "path": str(short_file),
            })

    # Save manifest into reports/
    man_file = reports_dir / "delivery-manifest.json"
    man_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    sync_channel_latest(channel_name)

    latest_dir = OUTPUTS_DIR / channel_name / "_LATEST"
    if auto_open:
        open_folder(latest_dir)

    return {
        "status": "success",
        "project": project_name,
        "channel": channel_name,
        "output_dir": str(output_dir),
        "latest_link": f"file:///{str(latest_dir.resolve()).replace(chr(92), '/')}",
        "total_generated": len(manifest),
    }


def main():
    parser = argparse.ArgumentParser(description="Unified VTuber Thumbnail Builder CLI.")
    parser.add_argument("--project", help="Preconfigured project mapping name (e.g. tygarina, armigon, aomi_debut)")
    parser.add_argument("--channel", help="Channel name for ad-hoc build (e.g. katy404, tygarina)")
    parser.add_argument("--hook", nargs="+", help="Primary hook text line(s)")
    parser.add_argument("--sec", nargs="+", help="Secondary text line(s)")
    parser.add_argument("--bg", help="Background frame image or video path")
    parser.add_argument("--avatar", help="Avatar cutout PNG image path")
    parser.add_argument("--date", help="Date string YYYY-MM-DD")
    parser.add_argument("--orientation", choices=["all", "landscape", "shorts"], default="all")
    parser.add_argument("--font", help="Path to Mitr-Bold.ttf")
    parser.add_argument("--no-open", action="store_true", help="Do not auto-open Windows Explorer")
    args = parser.parse_args()

    if args.project:
        result = build_project_batch(
            project_name=args.project,
            orientation=args.orientation,
            font_path=args.font,
            auto_open=not args.no_open,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.channel and args.hook:
        result = build_adhoc_thumbnail(
            channel=args.channel,
            hook=args.hook,
            sec=args.sec,
            bg_path=args.bg,
            avatar_path=args.avatar,
            date_str=args.date,
            orientation=args.orientation,
            font_path=args.font,
            auto_open=not args.no_open,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
