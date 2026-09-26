import json
import re
import sys
import zipfile
import zlib

# Reads Text+ / AutoSubs captions out of a Resolve .drp backup without opening
# Fusion inside Resolve (which hung the app when read through the API).
drp = sys.argv[1]
out = sys.argv[2]
z = zipfile.ZipFile(drp)
res = {}
for n in z.namelist():
    if not n.startswith("SeqContainer"):
        continue
    s = z.read(n).decode("utf-8", "replace")
    blobs = re.findall(r"<CompositionBA>(.*?)</CompositionBA>", s, re.S)
    if not blobs:
        continue
    texts = []
    for blob in blobs:
        outer = zlib.decompress(bytes.fromhex(blob.strip())[4:])
        k = outer.find(b"Compressed = true")
        start = outer.find(b"\x78\xda", k)
        data = zlib.decompressobj().decompress(outer[start:]).decode("utf-8", "replace")
        m = re.search(r'Text = Input \{ Value = "((?:[^"\\]|\\.)*)"', data)
        texts.append(m.group(1) if m else None)
    res[n] = texts
    print(n, len(texts))
    print("   " + " | ".join(str(t) for t in texts))
open(out, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
