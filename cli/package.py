"""Packages delivered thumbnails into a verified zip file with delivery manifest.
"""
import argparse
import io
import json
import zipfile
from pathlib import Path
from PIL import Image


def package_delivery(
    jpg_dir: str,
    manifest_path: str,
    output_zip: str,
) -> dict:
    """Zips delivered JPGs along with the manifest and validates CRC and image decodability."""
    jpg_p = Path(jpg_dir)
    manifest_p = Path(manifest_path)
    zip_p = Path(output_zip)
    zip_p.parent.mkdir(parents=True, exist_ok=True)

    jpg_files = list(jpg_p.glob("*.jpg"))
    if not jpg_files:
        raise ValueError(f"No JPG files found in {jpg_dir}")

    with zipfile.ZipFile(zip_p, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in jpg_files:
            zf.write(p, arcname=p.name)
        if manifest_p.exists():
            zf.write(manifest_p, arcname=manifest_p.name)

    # Verification of the generated ZIP
    with zipfile.ZipFile(zip_p) as zf:
        crc_err = zf.testzip()
        if crc_err is not None:
            raise RuntimeError(f"ZIP CRC test failed on file: {crc_err}")
        packaged_jpgs = [n for n in zf.namelist() if n.endswith(".jpg")]
        for n in packaged_jpgs:
            with Image.open(io.BytesIO(zf.read(n))) as im:
                im.load()
                assert im.format == "JPEG", f"{n} is not a valid JPEG"

    return {
        "zip_path": str(zip_p),
        "file_size_bytes": zip_p.stat().st_size,
        "total_images": len(packaged_jpgs),
        "status": "VERIFIED_PASS",
    }


def main():
    parser = argparse.ArgumentParser(description="Package and verify thumbnail deliverables.")
    parser.add_argument("--jpg-dir", required=True, help="Directory containing finalized JPG thumbnails")
    parser.add_argument("--manifest", required=True, help="Path to delivery manifest JSON")
    parser.add_argument("--out-zip", required=True, help="Path for generated ZIP package")
    args = parser.parse_args()

    res = package_delivery(args.jpg_dir, args.manifest, args.out_zip)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
