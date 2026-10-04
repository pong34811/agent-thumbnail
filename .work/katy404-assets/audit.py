from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import json, hashlib

root = Path('G:/My Drive/Projects/Katy404/1.picture')
out = Path(__file__).resolve().parent
files = sorted((p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.gif','.bmp','.tif','.tiff'}), key=lambda p: str(p.relative_to(root)).lower())
rows = []
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 20)
for i,p in enumerate(files,1):
    print(f'{i}/{len(files)} {p.name}',flush=True)
    data=p.read_bytes()
    with Image.open(p) as im:
        im.load()
        rgba=im.convert('RGBA')
        alpha=rgba.getchannel('A')
        bbox=alpha.getbbox()
        rows.append(dict(id=i,old=str(p.relative_to(root)),width=im.width,height=im.height,mode=im.mode,alpha_extrema=alpha.getextrema(),bbox=bbox,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))
        thumb=rgba.crop(bbox) if bbox else rgba
        thumb.thumbnail((375,355))
        tile=Image.new('RGB',(400,420),(220,224,230))
        d=ImageDraw.Draw(tile)
        for y in range(0,370,20):
            for x in range(0,400,20):
                if (x//20+y//20)%2: d.rectangle((x,y,x+19,y+19),fill=(190,196,204))
        tile.paste(thumb,((400-thumb.width)//2,(370-thumb.height)//2),thumb)
        d.text((10,375),f'{i:03d}  {im.width}x{im.height}',font=font,fill='black')
        d.text((10,399),p.stem[:33],font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14),fill='black')
        tile.save(out/f'tile-{i:03d}.jpg')
for start in range(0,len(rows),12):
    sheet=Image.new('RGB',(1600,1260),'white')
    for j in range(min(12,len(rows)-start)):
        with Image.open(out/f'tile-{start+j+1:03d}.jpg') as tile: sheet.paste(tile,((j%4)*400,(j//4)*420))
    sheet.save(out/f'sheet-{start//12+1:02d}.jpg',quality=94)
(out/'inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'COMPLETE {len(rows)} images',flush=True)
