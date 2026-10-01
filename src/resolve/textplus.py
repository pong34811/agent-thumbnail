"""Headless extraction of Text+ / AutoSubs captions from a DaVinci Resolve .drp backup.
Does not require launching Fusion inside Resolve.
"""
import json
import re
import sys
import zipfile
import zlib
from pathlib import Path
from typing import Dict, List, Optional


def extract_textplus_from_drp(drp_path: str, output_path: Optional[str] = None) -> Dict[str, List[Optional[str]]]:
    """Reads Text+ captions out of a Resolve .drp backup file."""
    z = zipfile.ZipFile(drp_path)
    res: Dict[str, List[Optional[str]]] = {}

    for n in z.namelist():
        if not n.startswith("SeqContainer"):
            continue
        s = z.read(n).decode("utf-8", "replace")
        blobs = re.findall(r"<CompositionBA>(.*?)</CompositionBA>", s, re.S)
        if not blobs:
            continue
        texts: List[Optional[str]] = []
        for blob in blobs:
            try:
                outer = zlib.decompress(bytes.fromhex(blob.strip())[4:])
                k = outer.find(b"Compressed = true")
                start = outer.find(b"\x78\xda", k)
                data = zlib.decompressobj().decompress(outer[start:]).decode("utf-8", "replace")
                m = re.search(r'Text = Input \{ Value = "((?:[^"\\]|\\.)*)"', data)
                texts.append(m.group(1) if m else None)
            except Exception:
                texts.append(None)
        res[n] = texts

    if output_path:
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)

    return res


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.resolve.textplus <backup.drp> [output.json]")
        sys.exit(1)
    drp_arg = sys.argv[1]
    out_arg = sys.argv[2] if len(sys.argv) > 2 else "textplus_extracted.json"
    result = extract_textplus_from_drp(drp_arg, out_arg)
    print(f"Extracted {len(result)} sequence containers to {out_arg}")
