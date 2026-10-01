"""Unified CLI to build thumbnails for a project using the core compositing engine.
"""
import argparse
import importlib
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

from PIL import Image

# Add repository root to path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.engine import (
    ThumbnailCompositor,
    LANDSCAPE_DIMS,
    SHORTS_DIMS,
)


def load_project_mapping(project_name: str) -> Dict[str, Any]:
    """Dynamically loads the mapping module for the given project."""
    module_path = f"projects.{project_name}.mapping"
    try:
        mod = importlib.import_module(module_path)
        return {
            "name": getattr(mod, "PROJECT_NAME", project_name),
            "timelines": getattr(mod, "TIMELINES", {}),
            "accents": getattr(mod, "ACCENTS", {}),
        }
    except ModuleNotFoundError as e:
        raise ValueError(f"Project mapping '{project_name}' not found under projects/ ({e})")


def build_thumbnails(
    project_name: str,
    out_dir: Optional[str] = None,
    orientation: str = "all",
    font_path: Optional[str] = None,
    assets_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """Builds thumbnails for the specified project."""
    mapping = load_project_mapping(project_name)
    timelines = mapping["timelines"]

    output_root = Path(out_dir) if out_dir else REPO_ROOT / "outputs" / mapping["name"]
    jpg_dir = output_root / "jpg"
    jpg_dir.mkdir(parents=True, exist_ok=True)

    compositor = ThumbnailCompositor(font_path=font_path)
    manifest = []
    built_count = 0

    # timelines can be a dict (by ID) or a list
    items = timelines.values() if isinstance(timelines, dict) else timelines

    for idx, tl in enumerate(items, start=1):
        tl_title = tl.get("title") or tl.get("name") or f"timeline_{idx}"
        safe_title = "".join(c if c.isalnum() or c in " -_ก-๙" else "_" for c in tl_title).strip()

        # Text lines
        hook = tl.get("hook")
        if isinstance(hook, str):
            hook = [hook]
        sec = tl.get("sec")
        if isinstance(sec, str):
            sec = [sec]

        # Extract options
        focus_circle = tl.get("focus_circle")
        emotion_marker = tl.get("emotion_marker")

        # Fallback placeholder background if media assets are on client machine
        dummy_bg = Image.new("RGB", LANDSCAPE_DIMS, (20, 24, 38))

        # 1. Landscape
        if orientation in ("all", "landscape"):
            land_img = compositor.composite_landscape(
                bg_image=dummy_bg,
                avatar_image=None,
                hook_lines=hook,
                secondary_lines=sec,
                focus_circle=focus_circle,
                emotion_marker=emotion_marker,
            )
            land_file = jpg_dir / f"{safe_title}.jpg"
            land_img.save(land_file, quality=92)
            built_count += 1
            manifest.append({
                "title": tl_title,
                "file": land_file.name,
                "path": str(land_file),
                "orientation": "landscape",
                "size": list(LANDSCAPE_DIMS),
                "hook": hook,
                "secondary": sec,
            })

        # 2. Shorts
        if orientation in ("all", "short", "shorts"):
            shorts_dummy = Image.new("RGB", SHORTS_DIMS, (20, 24, 38))
            short_img = compositor.composite_shorts(
                bg_image=shorts_dummy,
                avatar_image=None,
                hook_lines=hook,
                secondary_lines=sec,
                emotion_marker=emotion_marker,
            )
            short_file = jpg_dir / f"{safe_title}-short.jpg"
            short_img.save(short_file, quality=92)
            built_count += 1
            manifest.append({
                "title": tl_title,
                "file": short_file.name,
                "path": str(short_file),
                "orientation": "shorts",
                "size": list(SHORTS_DIMS),
                "hook": hook,
                "secondary": sec,
            })

    # Write manifest
    manifest_file = output_root / "delivery-manifest.json"
    manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "project": project_name,
        "built_images": built_count,
        "output_dir": str(output_root),
        "manifest": str(manifest_file),
    }


def main():
    parser = argparse.ArgumentParser(description="Build thumbnails for a configured project.")
    parser.add_argument("--project", required=True, choices=["aomi-debut", "tygarina", "armigon"],
                        help="Project name to build")
    parser.add_argument("--out-dir", help="Custom output directory")
    parser.add_argument("--orientation", choices=["all", "landscape", "short"], default="all",
                        help="Target orientation (default: all)")
    parser.add_argument("--font", help="Custom path to Mitr-Bold.ttf")
    args = parser.parse_args()

    result = build_thumbnails(
        project_name=args.project,
        out_dir=args.out_dir,
        orientation=args.orientation,
        font_path=args.font,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
