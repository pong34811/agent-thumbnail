"""Generate projects/aomi_p1/mapping.py from the Resolve inventory of project aomimama-2026-09-p1.

49 landscape timelines (+ 49 _9x16 twins). Hook text follows the timeline name, shortened to 1-4 words;
profanity from ASR subtitles is never used. flag != "" means the subtitle does not fully back the title.
"""
import json
import pprint
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
INV = json.loads((ROOT / "reports/aomi/2026-10-11/timeline-inventory-new.json").read_text(encoding="utf-8"))
LAND = [r for r in INV if str(r["res"][0]) == "1920"]

TT = "title-only"
# n: (hook, sec, frame_tl_sec, model_no, talk, evidence, flag)
H = {
    1: (["บอสตัวเหนียว!"], ["ล่อจนเหนื่อย"], 18, 9, False, "48 'ย้าาาาา'; 92 'มันหายไปไหนเนี่ย'", ""),
    2: (["เตรียมป้อมสู้!"], ["ศึกใหญ่กำลังมา"], 14, 10, False, "14 'เนี่ยมันคืออะไรวะ'", TT),
    3: (["ฮัลโหล!"], ["เปิดไลฟ์ Alien Shooter"], 27, 1, True, "10 'ฮัลโหล'; 27 'Alien Shooter'", ""),
    4: (["ฝูงเอเลี่ยนบุก!"], ["ร้องลั่นเลย"], 36, 4, False, "subs are chat talk (0-44)", "title mismatch: subs are chat talk -> check clip"),
    5: (["มีหลานแล้ว?!"], ["เพื่อนแต่งงานเร็วมาก"], 3, 8, False, "0 'เพื่อนมีหลานแล้ว'", ""),
    6: (["เงินขาดพันเดียว!"], ["ซื้อปืนไม่ได้"], 22, 11, False, "22 'ขาดไป 1,000 เดียว'", "shop/inventory screen is the content"),
    7: (["วันนี้เมื่อยมาก"], ["คุยแชทต้นไลฟ์"], 20, 13, False, "20 'ปวด เมื่อยวันนี้วิ่งเยอะ'", ""),
    8: (["เกมยากไหม?"], ["เล่นโหมดฮาร์ด"], 48, 5, False, "45 'เล่นง่ายมั้ยพี่'; 48 'โหมดฮาร์ด'", ""),
    9: (["จบซะที!"], ["เหนื่อยจนสมองหมด"], 12, 11, False, "4 'เหนื่อยจบซะที'; 17 'สมองหมด'", ""),
    10: (["ลืมแชร์จอ!"], ["จุดจบคนไม่เตรียมตัว"], 10, 7, True, "10 'จุดจบคนไม่ยอมแชร์จอ'", ""),
    11: (["หนาวตายจริง!"], ["ติดลบ 12 องศา"], 0, 11, False, "9 'หนาวตาย ติดลบ 12'", "title says -16, subs say -12 -> follow subs"),
    12: (["ลาวาร่วง!"], ["ถือถังกันหนาว"], 38, 9, False, "20 'ลาวาร่วง'; 25 'อุบัติเหตุลาวา'", "no lava on screen anywhere in the clip (lava bucket held only) -> hook unsupported by pixels"),
    13: (["พี่น้องไม่ช่วย!"], ["มาถูกเวลาจริงๆ"], 8, 4, False, "8 'พี่น้องไม่เคยช่วย'", ""),
    14: (["เจอเพชรแล้ว!"], ["ขุดตรงมากเลย"], 0, 1, False, "17 'ขุดตรงมาก'; 21 'ขอให้เจอ'", "frame is F3-free cave (F3 overlay shows server+coords in every in-clip frame); no diamond on screen"),
    15: (["เจอทางกลับบ้าน!"], ["เพื่อนไปห้องน้ำพอดี"], 80, 13, False, "8 'เจอทางกลับบ้าน'; 18 'ไปห้องน้ำ'", ""),
    16: (["เข้าได้สองทาง?"], ["ลุยฐานใต้ดิน"], 11, 10, False, "14 'มันมี 2 ทางหรอ'", ""),
    17: (["ยิงหลายตัวมาก!"], ["กวาดศัตรูฐานมืด"], 43, 8, False, "43 'ยิงหลายตัวมาก'", "subs thin (3 cues)"),
    18: (["ลองหมดแล้ว!"], ["XP Vista 8"], 31, 5, False, "1 'Windows 8 ยังไม่ลอง'", ""),
    19: (["ไม่รอดอ่ะ!"], ["ลองปรับความละเอียด"], 12, 11, False, "12 'ไม่รอดอ่ะพี่'; 8 '1,000/1,080'", ""),
    20: (["ไฟต์ใหญ่!"], ["ในอารีนา"], 1, 9, False, "0-1 game voice 'enemy slain'", "game voice only"),
    21: (["ดับเบิลคิล!"], ["แล้วโดนฝัง"], 27, 12, False, "27 'รู้แล้วคนนี้เขาเก่ง'", TT + ": 'ดับเบิลคิล' not in subs"),
    22: (["ไฟต์หน้าป้อม!"], ["ตกใจหมด"], 17, 4, False, "17 'โอ๊ย อะไรวะเนี่ย'", ""),
    23: (["ไฟต์ท้ายเกม!"], ["ไม่ขยับเลย"], 6, 6, False, "6 'ไม่ได้ขยับเลย'", "subs thin"),
    24: (["ลืมเอาของกิน!"], ["ต้องกินเนื้อซอมบี้"], 33, 8, False, "30 'ลืมเอาของกินมา'; 39 'เนื้อซอมบี้'", ""),
    25: (["ซอมบี้มาได้ไง?!"], ["เต็มไปหมด"], 5, 4, False, "10 'ซอมบี้เต็มเลย'; 17 'มันมาได้ไงวะ'", "no zombie on screen anywhere in the clip -> hook rests on subtitles only"),
    26: (["อยากเปลี่ยนร่าง!"], ["เสียงในหัวบ่นไม่หยุด"], 14, 5, False, "3 'อยากจะเปลี่ยนร่าง'; 8 'บ่นไม่หยุด'", ""),
    27: (["เรือไปไหน?!"], ["พี่จ๋าช่วยด้วย"], 10, 12, False, "7 'ต้องดันหรือต้องพาย'; 10 'คุมเรือเป็นไหม'", ""),
    28: (["วิ่งหนีมอน!"], ["มืดแล้วเจอบ้าน"], 3, 11, False, "0 'ไปหมู่บ้าน'; 3 'เพราะว่ามืดแล้ว'", ""),
    29: (["ออกไม่ได้เลย!"], ["เจอเอเมอรัลด์แรก"], 1, 6, False, "0 'เอเมอรัลด์แรก'", TT + ": 'ออกไม่ได้' not in first cues; no stuck/enclosure frame found in clip -> UNVERIFIED, consider retitle"),
    30: (["ไฟต์ในเลน!"], ["เลเวลสูงสุดแล้ว"], 1, 9, False, "0 'เลเวลสูงสุดแล้ว'", TT + ": 'เฮ้ย' not in subs"),
    31: (["โดนชัตดาวน์!"], ["ทีมไฟต์พัง"], 13, 7, False, "13 'หมาไม่โดน'; 17 'ตายละ'", TT + ": 'ชัตดาวน์' not in subs"),
    32: (["ตายก่อนเลย!"], ["หัวยังไม่ฟู"], 28, 4, False, "28 'เฮ้ยตายจริง'; 40 'ยังไม่ฟู'", ""),
    33: (["ออกไปก็ตาย!"], ["หนีไม่เป็นแล้ว"], 58, 11, False, "13 'หนีไปไม่เป็นแล้ว'", ""),
    34: (["ทีมกากมาก!"], ["ออกของไม่ดูเลย"], 40, 5, False, "5 'ทีมโคตรกาก'; 26 'ออกของไม่ดู'", ""),
    35: (["ขอบคุณทุกคน"], ["ปิดสตรีมแล้ว"], 23, 13, True, "23 'ขอบคุณท...'", "subs partial"),
    36: (["เกมแครช!"], ["ลบแล้วโหลดใหม่"], 13, 4, False, "13 'เกมแครช'; 16 'ลบเกมโหลดใหม่'", ""),
    37: (["หาไม่เจอ!"], ["ห้องสุดท้ายหายไป"], 32, 11, False, "2 'กุญแจหาย'; 32 'หาไม่เจอห้องสุดท้าย'", ""),
    38: (["จบแล้ว!"], ["จบเกมในไลฟ์เดียว"], 12, 1, False, "12 'จบแล้ว'; 37 'จบไปได้ไลฟ์เดียว'", ""),
    39: (["เกือบจมลาวา!"], ["อย่าใส่ร้ายผม"], 13, 6, False, "16 'อุดลาวาแล้วเหรอ'", "title partly backed"),
    40: (["เพนตาคิล!"], ["แต่ยังพ่ายแพ้"], 1, 12, False, "2 cues only", TT),
    41: (["ลืมเปิดเสียง!"], ["คุยกับผีมาตั้งนาน"], 8, 13, True, "0 'ลืมเอาเสียงเข้า'; 10 'เหมือนผีเลย'", ""),
    42: (["เริ่มเกมก็ไฟต์!"], ["ตีกันตั้งแต่ต้น"], 23, 10, False, "23 'มานี่มา'", TT),
    43: (["เซฟยังนะ?"], ["เช็กของแล้วลุยต่อ"], 40, 1, False, "37 'เก็บปืนก่อน'; 87 'โอ้ย'", TT + ": 'เซฟ' not in subs"),
    44: (["เจอวิธีใหม่!"], ["ตั้งค่าหน้าจอไลฟ์"], 53, 6, True, "49 'ใช้ของพรีเมียมได้'; 53 'จีเนียส'", "check scene"),
    45: (["จบภารกิจ!"], ["กวาดห้องหมดแล้ว"], 30, 9, False, "46 'โอเคเพื่อนเดี๋ยวมานะ'", TT),
    46: (["จอดับ!"], ["ด่านเขียวสุดท้าย"], 84, 4, False, "81-84 'เฮ้ยเดี๋ยวนะ'", TT),
    47: (["โอ๊ยๆๆ!"], ["แย่มาก"], 25, 4, False, "25 'แย่เลย'; 33 'โดนหลบ'", ""),
    48: (["เมาท์สายเกม!"], ["คุยกันสนุก"], 43, 2, False, "2 cues only", TT),
    49: (["แชร์จอได้แล้ว!"], ["เหมือนคนปกติสักที"], 24, 13, False, "13 'น่าจะใช้วิธีนี้แต่แรก'", ""),
}
# Absolute source second for frames that must sit outside the timeline range (id -> src seconds).
# #14: F3 debug overlay (server name + XYZ) is on for the whole timeline range; 3085s is the nearest F3-free gameplay.
FRAME_ABS = {14: 3085.0}
assert len(H) == len(LAND) == 49, (len(H), len(LAND))
MODEL_DIR = Path("G:/My Drive/Projects/Aomi-mama/1.picture")
MODELS = {int(p.name.split("_")[2]): p.name for p in MODEL_DIR.glob("vts_avatar_*.png")}
assert {m[3] for m in H.values()} <= set(MODELS), set(m[3] for m in H.values()) - set(MODELS)
TWIN = {r["name"] for r in INV if str(r["res"][0]) != "1920"}

rows = []
for n, t in enumerate(LAND, 1):
    hook, sec, ftl, mno, talk, ev, flag = H[n]
    assert t["name"] + "_9x16" in TWIN, t["name"]
    assert 1 <= len(hook[0].split()) <= 4 or len(hook[0]) <= 20
    rows.append(dict(
        id=n, name=t["name"], tl_short=t["name"] + "_9x16",
        src=t["src"].replace("\\", "/"), src_start=round(t["srcstart"] / t["fps"], 3), frame_tl=ftl,
        frame_abs=FRAME_ABS.get(n), model_file=MODELS[mno], talk=talk, hook=hook, sec=sec, evidence=ev, flag=flag))

out = '"""Aomi 2026-09 p1 mapping (49 clips x 2 orientations). Generated by gen_aomi_p1_mapping.py."""\n'
out += 'PROJECT_NAME = "aomi-2026-09-p1"\nCHARACTER_NAME = "aomi"\nMODEL_DIR = "G:/My Drive/Projects/Aomi-mama/1.picture"\n\n'
out += "TIMELINES = " + pprint.pformat(rows, width=140, sort_dicts=False) + "\n"
(ROOT / "projects/aomi_p1").mkdir(exist_ok=True)
(ROOT / "projects/aomi_p1/mapping.py").write_text(out, encoding="utf-8")
(ROOT / "projects/aomi_p1/__init__.py").write_text("", encoding="utf-8")
print(len(rows), "rows;", sum(1 for r in rows if r["flag"]), "flagged")
