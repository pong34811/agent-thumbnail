"""Helper command to open thumbnail deliverables directly in Windows Explorer.

Usage:
    python -m cli.open katy404    # Opens Katy404's latest images folder
    python -m cli.open tygarina   # Opens Tygarina's latest images folder
    python -m cli.open            # Opens outputs/ directory
    python -m cli.open --list     # Lists all available channels and paths
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = REPO_ROOT / "outputs"


def list_channels():
    print("\n=== Available Channel Deliverables (Images Only) ===")
    if not OUTPUTS_DIR.exists():
        print("outputs/ directory not found.")
        return

    for ch in OUTPUTS_DIR.iterdir():
        if ch.is_dir() and not ch.name.startswith("."):
            latest = ch / "_LATEST"
            dates = [d.name for d in ch.iterdir() if d.is_dir() and d.name != "_LATEST" and not d.name.startswith(".")]
            img_count = len(list(latest.glob("*.jpg"))) + len(list(latest.glob("*.png"))) if latest.exists() else 0
            print(f"- {ch.name.upper()}:")
            print(f"    Latest:   file:///{str(latest.resolve()).replace(chr(92), '/')}")
            print(f"    Images:   {img_count} images in _LATEST")
            print(f"    Batches:  {', '.join(sorted(dates))}")


def open_folder(target_path: Path):
    if not target_path.exists():
        print(f"Error: Target path does not exist: {target_path}")
        return False

    url = f"file:///{str(target_path.resolve()).replace(chr(92), '/')}"
    print(f"\n[Folder Link]: {url}")
    print(f"[Windows Path]: {target_path.resolve()}")

    if sys.platform == "win32":
        try:
            os.startfile(str(target_path.resolve()))
            print("[Opened]: Windows File Explorer has opened the folder.")
        except Exception:
            subprocess.run(["explorer.exe", str(target_path.resolve())], check=False)
            print("[Opened]: Launched explorer.exe")
    return True


def main():
    parser = argparse.ArgumentParser(description="Open thumbnail deliverables folder.")
    parser.add_argument("channel", nargs="?", help="Channel name (e.g. katy404, tygarina, armigon)")
    parser.add_argument("--list", action="store_true", help="List all channel paths")
    args = parser.parse_args()

    if args.list:
        list_channels()
        return

    if not args.channel:
        open_folder(OUTPUTS_DIR)
        return

    ch_clean = args.channel.lower().replace("-", "_")
    target = OUTPUTS_DIR / ch_clean / "_LATEST"
    if not target.exists():
        target = OUTPUTS_DIR / args.channel / "_LATEST"

    if not target.exists():
        print(f"Channel '{args.channel}' not found.")
        list_channels()
        return

    open_folder(target)


if __name__ == "__main__":
    main()
