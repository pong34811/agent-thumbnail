from pathlib import Path
from PIL import Image
import re,base64,io,json
root=Path('G:/My Drive/Projects/Katy404/1.picture')
catalog=root/'_asset-catalog'
page=(catalog/'index.html').read_text(encoding='utf-8')
images=re.findall(r'data:image/jpeg;base64,([^"\s]+)',page)
for encoded in images:
    with Image.open(io.BytesIO(base64.b64decode(encoded))) as im:
        buf=io.BytesIO()
        im.crop((0,0,400,370)).save(buf,format='JPEG',quality=90)
    page=page.replace(encoded,base64.b64encode(buf.getvalue()).decode())
(catalog/'index.html').write_text(page,encoding='utf-8')
manifest=json.loads((catalog/'rename-manifest.json').read_text(encoding='utf-8'))
rows=manifest['files']
assert len(images)==len(rows)==page.count('<article ')==50
assert all((root/r['new']).is_file() for r in rows)
assert len(list(root.glob('*.png')))==50
assert len(re.findall(r'<a href="\.\./',page))==50
manifest['date']='2026-10-04'
(catalog/'rename-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
report=(catalog/'README-th.md').read_text(encoding='utf-8').replace('3 ตุลาคม 2026','4 ตุลาคม 2026')
(catalog/'README-th.md').write_text(report,encoding='utf-8')
print('PASS: 50 source images, 50 catalog cards, 50 valid original-file links; previews cleaned.')
