"""Frame Sampling CLI using ffmpeg to extract high-res frames matching timeline subtitle cues.
"""
import argparse
import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional, List


def extract_frame_at_timestamp(
    video_path: str,
    timestamp_str: str,
    output_image_path: str,
    ffmpeg_bin: Optional[str] = None,
) -> bool:
    """Extracts a single high-quality frame from a video file at a given timestamp."""
    ffmpeg = ffmpeg_bin or shutil.which("ffmpeg") or "ffmpeg"
    out_p = Path(output_image_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        ffmpeg,
        "-y",
        "-ss", timestamp_str,
        "-i", str(video_path),
        "-vframes", "1",
        "-q:v", "2",
        str(out_p),
    ]

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return out_p.exists()
    except Exception as e:
        print(f"Error sampling frame at {timestamp_str}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Extract video frames at timestamps using ffmpeg.")
    parser.add_argument("--video", required=True, help="Path to input video file")
    parser.add_argument("--time", required=True, help="Timestamp (e.g. 00:00:05 or seconds)")
    parser.add_argument("--out", required=True, help="Path to output image file (.png / .jpg)")
    parser.add_argument("--ffmpeg", help="Custom path to ffmpeg binary")
    args = parser.parse_args()

    ok = extract_frame_at_timestamp(args.video, args.time, args.out, args.ffmpeg)
    if ok:
        print(f"Successfully extracted frame to {args.out}")
    else:
        print(f"Failed to extract frame")
        exit(1)


if __name__ == "__main__":
    main()
