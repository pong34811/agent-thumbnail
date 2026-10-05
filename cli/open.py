"""Helper command to open the deliverables folder directly in Windows Explorer
and display clickable URLs.

Usage:
    python -m cli.open            # Opens the latest delivery across all channels
    python -m cli.open katy404    # Opens Katy404's latest thumbnails
    python -m cli.open tygarina   # Opens Tygarina's latest thumbnails
    python -m cli.open --list     # Lists all available channels and their paths
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = REPO_ROOT / "outputs"
CHANNELS_DIR = OUTPUTS_DIR / "channels"


def list_channels():
    print("\n=== Available Channel Deliverables ===")
    if not CHANNELS_DIR.exists():
        print("No channels found. Run 'python -m cli.organize' first.")
        return

    for ch in CHANNELS_DIR.iterdir():
        if ch.is_dir():
            latest = ch / "_LATEST"
            dates = [d.name for d in ch.iterdir() if d.is_dir() and not d.name.startswith("_")]
            print(f"- {ch.name.upper()}:")
            print(f"    Latest:   file:///{str(latest.resolve()).replace(chr(92), '/')}")
            print(f"    Batches:  {', '.join(sorted(dates))}")
    print(f"\nGlobal Latest: file:///{str((OUTPUTS_DIR / '_LATEST_DELIVERY').resolve()).replace(chr(92), '/')}")


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
        except Exception as e:
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
        target = OUTPUTS_DIR / "_LATEST_DELIVERY"
        if not target.exists():
            target = CHANNELS_DIR
        open_folder(target)
        return

    ch_name = args.channel.lower().replace("-", "_")
    target = CHANNELS_DIR / ch_name / "_LATEST"
    if not target.exists():
        # Try direct match
        target = CHANNELS_DIR / args.channel / "_LATEST"

    if not target.exists():
        print(f"Channel '{args.channel}' not found.")
        list_channels()
        return

    open_folder(target)


if __name__ == "__main__":
    main()
