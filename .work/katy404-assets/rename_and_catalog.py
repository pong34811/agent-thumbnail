from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, csv, hashlib, html, base64, shutil
from collections import Counter

work=Path(__file__).resolve().parent
root=Path('G:/My Drive/Projects/Katy404/1.picture').resolve()
rows=json.loads((work/'inventory.json').read_text(encoding='utf-8'))
labels=json.loads((work/'labels.json').read_text(encoding='utf-8'))
assert len(rows)==len(labels)==50
preferred={1,2,6,9,13,14,26,30,40,41,44,45,46,48}
for r,(kind,expr,pose,tags,use) in zip(rows,labels):
    r.update(kind=kind,expression=expr,pose=pose,tags_th=tags,suggested_use_th=use,preferred=r['id'] in preferred)
    r['new']=f"katy404_{kind}_{expr}_{pose}_{r['id']:03d}.png"
    r['notes_th']='มีข้อความฝังในภาพ เลือกใช้เมื่อข้อความตรงเรื่อง' if kind=='chibi-sticker' else 'สีหน้าเป็นคำบรรยายภาพ; เลือกให้ตรงเหตุการณ์คลิป'
names=[r['new'].casefold() for r in rows]
assert len(set(names))==len(names)
for r in rows:
    old=root/r['old']; new=root/r['new']
    assert old.resolve().is_relative_to(root) and new.resolve().is_relative_to(root)
    assert old.is_file() and not new.exists(),r
    assert hashlib.sha256(old.read_bytes()).hexdigest()==r['sha256'],r
manifest=dict(channel='Katy404 / KT404',root=str(root),date='2026-10-03',count=len(rows),naming='katy404_<kind>_<expression>_<pose>_<stable-id>.png',direction='left/right refer to the image as viewed',files=rows)
(work/'rename-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
log=[]
try:
    for r in rows:
        (root/r['old']).rename(root/r['new'])
        log.append(r)
        (work/'rename-progress.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
except Exception:
    for r in reversed(log):
        if not (root/r['old']).exists(): (root/r['new']).rename(root/r['old'])
    raise
for r in rows:
    p=root/r['new']
    assert not (root/r['old']).exists()
    assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
    with Image.open(p) as im:
        im.load()
        assert list(im.size)==[r['width'],r['height']]
        assert im.convert('RGBA').getchannel('A').getextrema()==(0,255)
print('Verified 50 renames: identical SHA256, dimensions, alpha and decodability.',flush=True)
catalog=root/'_asset-catalog'
catalog.mkdir(exist_ok=True)
shutil.copy2(work/'rename-manifest.json',catalog/'rename-manifest.json')
fields=['id','new','old','kind','expression','pose','tags_th','suggested_use_th','preferred','width','height','mode','bytes','sha256','notes_th']
with (catalog/'asset-index.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
cards=[]
for r in rows:
    preview=(work/f"tile-{r['id']:03d}.jpg").read_bytes()
    uri='data:image/jpeg;base64,'+base64.b64encode(preview).decode()
    name=html.escape(r['new'])
    tags=html.escape(r['tags_th']); use=html.escape(r['suggested_use_th'])
    search=html.escape(' '.join([r['new'],r['old'],r['tags_th'],r['suggested_use_th']]),quote=True)
    cards.append(f'<article data-search="{search}" data-preferred="{int(r["preferred"])}"><a href="../{name}"><img src="{uri}" loading="lazy" alt="{tags}"></a><b>{name}</b><p>{tags}</p><p>ใช้กับ: {use}</p><small>{r["width"]}×{r["height"]} · PNG โปร่งใส'+(' · ★ ตัวเลือกเริ่มต้น' if r['preferred'] else '')+'</small></article>')
page='''<!doctype html><html lang="th"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Katy404 Character Assets</title><style>body{font:16px system-ui;background:#171923;color:#eee;margin:24px}h1{margin-bottom:8px}input{width:min(650px,85%);padding:14px;border-radius:8px;font-size:18px}label{display:inline-block;margin:15px}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:16px}article{background:#252938;border-radius:12px;padding:12px}img{width:100%;border-radius:6px}b{display:block;overflow-wrap:anywhere;font-size:14px}p{margin:10px 0}small{color:#b9c4da}[hidden]{display:none!important}a{color:#a9c9ff}</style><h1>Katy404 / KT404 — คลังตัวละคร 50 ภาพ</h1><p>ค้นหาจากสีหน้า ท่าทาง อุปกรณ์ หรือประเภท เช่น งง / ร้องไห้ / ถือจอย / ไมค์ / หัวใจ / chibi</p><input id="search" placeholder="ค้นหาภาพ…"><label><input type="checkbox" id="preferred" style="width:auto"> เฉพาะตัวเลือกเริ่มต้น ★</label><p id="count"></p><p>คลิกภาพเพื่อเปิด PNG ต้นฉบับ • ภาพตัวอย่างใช้พื้นตารางเพื่อแสดงความโปร่งใส • ซ้าย/ขวาอ้างอิงด้านของภาพที่มองเห็น</p><main>'''+''.join(cards)+'''</main><script>const q=document.querySelector('#search'),p=document.querySelector('#preferred'),cards=[...document.querySelectorAll('article')];function filter(){const words=q.value.toLowerCase().trim().split(/\s+/).filter(Boolean);let n=0;cards.forEach(c=>{c.hidden=!words.every(w=>c.dataset.search.toLowerCase().includes(w))||(p.checked&&c.dataset.preferred!=='1');if(!c.hidden)n++});document.querySelector('#count').textContent=`แสดง ${n} / 50 ภาพ`}q.addEventListener('input',filter);p.addEventListener('change',filter);filter();</script></html>'''
(catalog/'index.html').write_text(page,encoding='utf-8')
for start in range(0,len(rows),10):
    sheet=Image.new('RGB',(1600,1050),'white')
    for j,r in enumerate(rows[start:start+10]):
        tile=Image.open(work/f"tile-{r['id']:03d}.jpg").crop((0,0,400,370))
        tile.thumbnail((320,370))
        x=(j%5)*320;y=(j//5)*525
        sheet.paste(tile,(x,y))
        d=ImageDraw.Draw(sheet)
        lines=[f"{r['id']:03d}  {r['kind']}",r['expression'],r['pose'],f"{r['width']}x{r['height']}"+('  * recommended' if r['preferred'] else '')]
        for k,line in enumerate(lines):d.text((x+8,y+305+k*25),line,font=font,fill='black')
    sheet.save(catalog/f'contact-sheet-{start//10+1:02d}.jpg',quality=94)
restore='''from pathlib import Path
import json, hashlib, argparse
p=argparse.ArgumentParser(description="Restore original asset filenames; dry run by default")
p.add_argument('--apply',action='store_true');args=p.parse_args()
catalog=Path(__file__).resolve().parent;root=catalog.parent
rows=json.loads((catalog/'rename-manifest.json').read_text(encoding='utf-8'))['files']
for r in rows:
    src=root/r['new'];dst=root/r['old']
    assert src.resolve().is_relative_to(root) and dst.resolve().is_relative_to(root)
    assert src.is_file() and not dst.exists(),f"Missing source or occupied destination: {r['new']}"
    assert hashlib.sha256(src.read_bytes()).hexdigest()==r['sha256'],f"File has changed: {r['new']}"
print(f'Validated {len(rows)} files.')
if args.apply:
    for r in rows:(root/r['new']).rename(root/r['old'])
    print('Restored original filenames. Catalog now records rename history; image links refer to renamed filenames.')
else:print('Dry run only. Use --apply to restore original names.')
'''
(catalog/'restore-original-names.py').write_text(restore,encoding='utf-8')
report='''# คลังภาพตัวละคร Katy404 / KT404

ตรวจและเปลี่ยนชื่อวันที่ 3 ตุลาคม 2026 จำนวน 50 PNG

- เปิดและถอดรหัสได้ครบ 50 ภาพ มี alpha โปร่งใสครบทุกภาพ
- ดูภาพทั้งหมดผ่าน contact sheet เพื่อติดคำค้นตามสีหน้า ท่าทาง อุปกรณ์ และข้อความที่เห็น
- ไม่พบไฟล์ซ้ำแบบ SHA256 ตรงกัน แต่มีท่าใกล้เคียงกันหลายภาพ จึงเก็บทั้งหมดและให้รหัสแยก
- หลังเปลี่ยนชื่อ ตรวจ SHA256 ตรงกับต้นฉบับครบ 50 ไฟล์: เนื้อภาพ ขนาด และความโปร่งใสเหมือนเดิม
- illustration 3 ภาพ, chibi-sticker 10 ภาพ, avatar-mic 26 ภาพ, avatar 11 ภาพ

เปิด `index.html` เพื่อดูภาพและค้นหาด้วยคำภาษาไทยหรืออังกฤษ คลิกภาพเพื่อเปิดต้นฉบับ
ชื่อไฟล์ใช้ `katy404_<ประเภท>_<สีหน้า>_<ท่าทาง>_<รหัส>.png` และใช้ katy404 เป็นชื่อมาตรฐานของช่อง Katy404 / KT404
ซ้าย/ขวาหมายถึงด้านของภาพที่มองเห็น ไม่ใช่ด้านร่างกายของตัวละคร
`asset-index.csv` เปิดใน Excel ได้ มีชื่อเดิม–ใหม่ คำค้น การใช้งาน ขนาด และ SHA256
`rename-manifest.json` เก็บข้อมูลต้นฉบับและพิกัด alpha bbox สำหรับจัดตำแหน่งตอนทำปก

## ตัวเลือกเริ่มต้น

- เล่นเกม: 044 ถือจอยสีม่วง
- ใช้ทั่วไป/พูดคุย: 045 หน้าปกติ ไม่มีพร็อพ
- งง/ตกใจ: 048 ตาโต ปากอ้า เครื่องหมายคำถาม ไม่มีไมค์
- งอน/สงสัย: 046 ตาปรือ ปากจู๋ เครื่องหมายคำถาม ไม่มีไมค์
- โกรธ/เขิน: 001 ภาพวาดกำหมัด หน้าบลัช
- ขอบคุณ/แฟนคลับ: 041 หลับตายิ้ม ทำมือหัวใจ
- ร้องเพลง/พูดคุย: 014 ถือไมค์ หันซ้ายภาพ
- ขำ: 026 ถือไมค์ ตาหยี ปากอ้า
- เงิน/กาชา: 030 ถือไมค์พร้อมสัญลักษณ์เงิน
- ชิบิตกใจ: 006 มีคำว่า ตกใจ ฝังในภาพ

## ข้อสังเกตสำหรับทำปก

- ภาพ VTS มีพื้นที่โปร่งใสรอบตัวมาก ให้อ่าน alpha bbox และวางจากตัวละครที่มองเห็น
- กลุ่ม avatar-mic ถือไมค์ทุกภาพ ใช้เมื่อพร็อพเข้ากับเนื้อหา
- กลุ่ม shaded มีเงาบนใบหน้าอยู่ในต้นฉบับแล้ว
- กลุ่ม chibi-sticker มีข้อความและกราฟิกฝังในภาพ ควรเลือกเมื่อคำเหล่านั้นตรงเรื่อง
- ไม่พบไฟล์เสียจากการถอดรหัส การตรวจครั้งนี้เป็นการจัดคลัง asset ไม่ใช่ QC ภาพปกที่ประกอบเสร็จ

## ย้อนกลับชื่อเดิม

รัน `python restore-original-names.py` ในโฟลเดอร์นี้เพื่อตรวจแบบไม่เปลี่ยนชื่อ
รัน `python restore-original-names.py --apply` เพื่อคืนชื่อเดิม สคริปต์จะตรวจไฟล์และปลายทางก่อน และไม่เขียนทับไฟล์อื่น
'''
(catalog/'README-th.md').write_text(report,encoding='utf-8')
print('Catalog complete:',catalog,flush=True)
print(Counter(r['kind'] for r in rows))
