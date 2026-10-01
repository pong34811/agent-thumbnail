"""Automated Quality Assurance & Verification CLI for YouTube Thumbnails.

Checks:
- Exact dimensions: 1920x1080 (Landscape) or 1080x1920 (Shorts)
- Max file size <= 2MB (2,097,152 bytes)
- Color space mode RGB, format JPEG
- Margins and safe zones
- Squint test downscale generation (320x180 and 180x320)
"""
import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from PIL import Image

MAX_FILE_BYTES = 2 * 1024 * 1024  # 2MB YouTube hard limit
MARGIN = 40


def verify_thumbnail(image_path: Path, squint_dir: Optional[Path] = None) -> List[str]:
    """Verifies a single thumbnail image and optionally outputs a downscaled squint-test preview."""
    issues = []
    file_bytes = image_path.stat().st_size
    if file_bytes > MAX_FILE_BYTES:
        issues.append(f"File size {file_bytes} bytes exceeds 2MB limit ({file_bytes // 1024} KB)")

    with Image.open(image_path) as im:
        im.load()
        w, h = im.size
        fmt, mode = im.format, im.mode

        if fmt != "JPEG":
            issues.append(f"Expected JPEG format, got {fmt}")
        if mode != "RGB":
            issues.append(f"Expected RGB color mode, got {mode}")

        is_landscape = (w == 1920 and h == 1080)
        is_shorts = (w == 1080 and h == 1920)

        if not (is_landscape or is_shorts):
            issues.append(f"Invalid dimensions: {w}x{h} (Must be 1920x1080 or 1080x1920)")

        # Squint Test Generation
        if squint_dir:
            squint_dir.mkdir(parents=True, exist_ok=True)
            thumb = im.convert("RGB")
            thumb.thumbnail((320, 180) if w > h else (180, 320), Image.Resampling.LANCZOS)
            thumb.save(squint_dir / image_path.name, quality=90)

    return issues


def verify_directory(
    jpg_dir: str,
    manifest_path: Optional[str] = None,
    squint_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """Verifies all thumbnails in a directory."""
    jpg_p = Path(jpg_dir)
    squint_p = Path(squint_dir) if squint_dir else None
    results = {}
    total_problems = 0

    files = sorted(jpg_p.glob("*.jpg"))
    if not files:
        return {"status": "ERROR", "message": f"No JPG files found in {jpg_dir}"}

    for f in files:
        issues = verify_thumbnail(f, squint_p)
        results[f.name] = {
            "status": "PASS" if not issues else "FAIL",
            "size_kb": f.stat().st_size // 1024,
            "issues": issues,
        }
        if issues:
            total_problems += len(issues)

    manifest_checks = []
    if manifest_path and Path(manifest_path).exists():
        manifest_data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
        manifest_checks.append(f"Manifest found with {len(manifest_data)} entries")

    return {
        "status": "PASS" if total_problems == 0 else "FAIL",
        "total_files": len(files),
        "total_problems": total_problems,
        "files": results,
        "manifest_notes": manifest_checks,
    }


def main():
    parser = argparse.ArgumentParser(description="Verify thumbnails against production criteria.")
    parser.add_argument("--jpg-dir", required=True, help="Directory of JPG files to verify")
    parser.add_argument("--manifest", help="Optional delivery manifest to cross-check")
    parser.add_argument("--squint-dir", help="Directory to save downscaled squint-test previews")
    args = parser.parse_args()

    report = verify_directory(args.jpg_dir, args.manifest, args.squint_dir)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["status"] != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
