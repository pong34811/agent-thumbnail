"""Environment check for the thumbnail toolchain.

Usage:
    python -m cli.doctor
Exits with status 1 when a required dependency is missing.
"""
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def run_checks() -> list:
    """Returns (name, ok, detail, required) tuples."""
    from src.engine.text_thai import raqm_available, resolve_font_path  # loads fribidi first

    import PIL
    import numpy

    font = resolve_font_path()
    return [
        ("Pillow", True, PIL.__version__, True),
        ("numpy", True, numpy.__version__, True),
        ("libraqm (Thai layout)", raqm_available(), "enabled" if raqm_available() else "missing: run in an environment with libraqm/fribidi", True),
        ("Mitr-Bold font", font is not None, str(font) if font else "not found; set THUMBNAIL_FONT_PATH", True),
        ("ffmpeg", shutil.which("ffmpeg") is not None, shutil.which("ffmpeg") or "not on PATH (needed by cli.sample_frames)", False),
    ]


def main() -> int:
    failed = False
    for name, ok, detail, required in run_checks():
        mark = "OK  " if ok else ("FAIL" if required else "WARN")
        print(f"[{mark}] {name}: {detail}")
        failed = failed or (not ok and required)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
