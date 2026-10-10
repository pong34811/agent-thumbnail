"""Generate projects/aomi_p2/mapping.py from the Resolve inventory + hand-picked hooks.

Hook text comes only from subtitle cues (evidence, timeline seconds) or, where subtitles
are thin, from the timeline title (flag starts with 'title-only').
"""
import json
import pprint
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
INV = json.loads((ROOT / "reports/aomi/2026-10-10/timeline-inventory.json").read_text(encoding="utf-8"))

# idx: (hook, sec, frame_tl_sec, model_no, talk, evidence, flag)
H = {
    1: (["เหนื่อยมาก!"], ["เล่นแบบลำบาก"], 30, 11, False, "27.7 'เหนื่อย'; 46.3 'เล่นแบบลำบาก'", ""),
    2: (["แพ้ก็ไม่เสียดาย"], ["เกมที่ต้องการทีมเวิร์ก"], 14, 13, True, "12.0 'เราแพ้อ่ะ'; 13.9 'ไม่เสียดาย'", ""),
    3: (["สู้ทางแคบ?!"], ["ลำบากมาก มุมก้มโหด"], 38, 5, False, "36.4 'ไปสู้กันตรงทางแคบ'; 44.1 'ลำบาก'", ""),
    4: (["เดินไปไหนเนี่ย?!"], ["ทีมอ้อมทางไกลกว่า"], 38, 10, False, "33 'ไปไหนวะ'; 38 'ทำไมอ่ะ'", ""),
    5: (["ตายอีกแล้ว!"], ["ไม่เคยเรียนรู้เลย"], 68, 8, False, "67 'อีกครั้ง'; 70 'ไม่เคยเรียนรู้'", ""),
    6: (["ไม่มีทางแล้ว!"], ["ทีมโหวตยอมแพ้"], 1, 4, False, "0 'คือมันไม่มีทาง'", "title-only: 'ยอมแพ้' not in subs (4 cues)"),
    7: (["หมายความว่าไง?!"], ["เพื่อนยืนหลังคนแทน"], 55, 7, False, "55 'อยู่หลังคนแทน'; 56 'หมายความว่าไงวะ'", "title says 'แพน', subtitle says 'แทน' -> follow subtitle"),
    8: (["พักซีรีส์ก่อนนะ"], ["เล่นเท่าที่ไหว"], 8, 1, True, "7 'หยุดพักซีรีส์กันก่อน'; 21 'เท่าที่พอไหว'", ""),
    9: (["ลุ้นสุดตัว!"], ["ปะทะกันในรอบ"], 3, 12, False, "0-4 'มาถึงแล้วแหละ'", "title-only"),
    10: (["ไม่มีทาง!"], ["ไล่ล่ากลางแมป"], 70, 9, False, "70 'ไม่มีทาง'", ""),
    11: (["สงสัยโดนโกง?!"], ["จนต้องกดรีพอร์ต"], 42, 5, False, "3 'รีพอร์ต'; 39 'ออโต้ไฟล์'", ""),
    12: (["โอ๊ย! เจ็บ!"], ["โดนยิงรัวจนเสียงหลุด"], 5, 6, False, "2 'โอ๊ย'; 5 'เจ็บ'", ""),
    13: (["เหมือนอยู่คนเดียว"], ["ทีมไม่พูดอะไรเลย"], 62, 2, False, "60 'ไม่มีใครพูดไรเลย'; 62 'เหมือนกูอยู่คนเดียว'", ""),
    14: (["เหลือคนเดียว!"], ["รอบสุดท้ายสุดระทึก"], 54, 12, False, "54 'Only one ally remains' (game voice)", "game voice only, no Thai speech"),
    15: (["ทำไมโดนโฟกัส?!"], ["เกลียดโดนคนเดียว"], 15, 2, False, "14 'ทำไมโดนโฟกัส'; 47 'เกลียด'", ""),
    16: (["โดนลาวาเผา!"], ["ตายกลางเกม"], 16, 9, False, "15 'โดนลาวาเผาได้ยังไงวะ'", ""),
    17: (["เล่นเกมในห้องน้ำ?"], ["เพื่อนในเซิร์ฟคุยเรื่องนอน"], 40, 6, False, "72 'พี่จะเล่นเกมในห้องน้ำ'", ""),
    18: (["ใช้พลังแอดมิน!"], ["วาร์ปย่นเวลา"], 11, 13, False, "9 'ใช้พลังแอดมิน'; 11 'วาร์ป'", ""),
    19: (["หนาวตาย!"], ["หนีหนาวด้วยความตาย"], 46, 11, False, "45 'หนีความหนาวด้วยความตาย'", ""),
    20: (["เกือบร่วง!"], ["ขุดถ้ำหาเหล็ก"], 74, 10, False, "73 'ถ้าลื่นก็ร่วงลงไป'", ""),
    21: (["เสียวสันหลัง!"], ["เกือบตกเหวในถ้ำ"], 40, 3, False, "37 'เกือบไปแล้ว'; 41 'เสียวสันหลัง'", ""),
    22: (["ทายมีมกัน!"], ["มุกเพื่อนในเซิร์ฟ"], 23, 6, False, "22 'มีมให้ทายสักอันไหม'", ""),
    23: (["อ่านว่าอะไร?!"], ["เกมวันนี้ชื่อยากมาก"], 16, 12, True, "13 'เกมชื่ออะไร'; 17 'อ่านว่าอะไรอ่ะ'", ""),
    24: (["งงมาก!"], ["ลองเล่นครั้งแรก"], 26, 4, False, "26 'โอ้โห' (2 cues only)", "title-only"),
    25: (["โอ๊ย! แย่แล้ว!"], ["กำแพงถูกบุก"], 39, 1, False, "39 'โอ๊ย'", "title-only: 'คนตาย' not in subs"),
    26: (["ไม่บอกให้ทำรั้ว!"], ["รั้วราคาเท่าไหร่ล่ะ"], 130, 7, False, "124-133 'ไม่บอกให้กูทำรั้ว'", "title says bridge defence; subtitle is about fence cost -> follow subtitle"),
    27: (["ใครเนี่ย?!"], ["งงในเกมอีกแล้ว"], 60, 5, False, "58-60 'กากไหนวะ' (sparse)", "title-only"),
    28: (["ฮัดชิ้ว!"], ["ด่านหิมะศัตรูเต็มจอ"], 57, 13, False, "57 'ฮัดชิ้ว'", ""),
    29: (["ไม่รู้เพราะอะไร"], ["คุยสรุปเกม"], 138, 3, True, "137 'ไม่รู้เหมือนกัน'; 139 'เพราะอะไร'", "title says closing, subtitle is a greeting"),
    30: (["เครื่องมีปัญหา!"], ["ลบไฟล์แล้วโหลดค้าง"], 38, 8, True, "33 'มีปัญหานิดหน่อย'; 37 'ไปลบไฟล์'", ""),
    31: (["ไม่เอา กลัว!"], ["ตัวจริงหรือตัวปลอม?"], 21, 1, False, "16 'ไม่เอากลัว'; 40 'ตัวปลอม'", "title says wall building, subtitle is about fake/real -> follow subtitle"),
    32: (["ศึกกลางคืน!"], ["ศัตรูรุกเข้ากำแพง"], 45, 10, False, "41 'ละเมิด' (ASR doubtful)", "title-only"),
    33: (["ขึ้นมาได้ไง?!"], ["ไฟลุกกลางศึก"], 44, 12, False, "43 'มึงขึ้นมาได้ยังไงอะ'", ""),
    34: (["ย้าาา!"], ["ปะทะบนกำแพงหิมะ"], 20, 9, False, "4-78 'ย้า!' repeated", ""),
    35: (["ปราสาทแตก!"], ["แพ้เกมแล้ว"], 143, 4, False, "111 'มันตายหรอ'", "title-only"),
    36: (["เริ่มใหม่ทั้งหมด"], ["Becastled รอบใหม่"], 41, 6, True, "39 'เริ่มใหม่ทั้งหมด'", ""),
    37: (["ไม้ไม่พอ!"], ["งบก็ไม่พอ"], 148, 11, False, "148 'ปัญหา...แพงซื้อ' (thin)", "title-only"),
    38: (["ยืนตรงนี้ใช่มั้ย?"], ["ลองสับตรงนี้ดู"], 21, 13, False, "19 'ต้องมายืนตรงนี้ใช่มั้ย'", "title mismatch -> follow subtitle"),
    39: (["ทำไมไม่ได้?!"], ["กำแพงโดนตี"], 25, 5, False, "23 'ทำไมไม่ได้วะ'", ""),
    40: (["เคลียร์ตรงนี้!"], ["ไล่เคลียร์หมาก"], 29, 7, False, "28 'เคลียร์ตรงนี้ เร็วๆ'", ""),
    41: (["ไม่มีไม้ขาย!"], ["ทำยังไงดี?"], 26, 2, False, "25 'เราไม่มีไม้'; 2 'ขายไม้'", ""),
    42: (["บอสเป็นมังกร!"], ["ถอยไม่ได้ งั้นลุย"], 45, 12, False, "44 'เป็นมังกรว่ะ'; 158 'ถอยไม่ได้งั้นลุย'", ""),
    43: (["เกมเพลินดี!"], ["คุยส่งท้ายสตรีม"], 16, 13, True, "4 'เป็นเกมที่เพลิน'; 16 'เพลินๆดี'", ""),
    44: (["ดีเฟนด์ไม่รอด!"], ["รอบสุดท้ายจนแพ้"], 40, 8, False, "40 'Defend your position' (game voice)", "game voice + sparse Thai"),
}
MODELS = {
    1: "vts_avatar_01_bust_gentle_smile", 2: "vts_avatar_02_bust_camisole_relaxed",
    3: "vts_avatar_03_sheet_triptych_smug", 4: "vts_avatar_04_bust_veiled_subtle_fang",
    5: "vts_avatar_05_bust_half_lidded_smirk", 6: "vts_avatar_06_bust_cheerful_fang_smile",
    7: "vts_avatar_07_bust_confident_smug", 8: "vts_avatar_08_bust_narrow_eyes_smirk",
    9: "vts_avatar_09_bust_wide_grin_bright_eyes", 10: "vts_avatar_10_bust_smug_half_lidded",
    11: "vts_avatar_11_switch_gaze_down", 12: "vts_avatar_12_switch_playful_forward_grin",
    13: "vts_avatar_13_switch_soft_content_smile",
}

rows = []
for t in INV:
    hook, sec, ft, m, talk, ev, flag = H[t["i"]]
    rows.append(dict(
        id=t["i"], name=t["name"], tl_short=t["name"].replace("-vdo", "-vdo_9x16", 1),
        src=t["src"].replace("\\", "/"), src_start=round(t["srcstart"] / 60, 3), frame_tl=ft,
        model_file=MODELS[m] + ".png", talk=talk, hook=hook, sec=sec, evidence=ev, flag=flag))

out = '"""Aomi 2026-09 p2 mapping (44 clips x 2 orientations). Generated by gen_aomi_p2_mapping.py."""\n'
out += 'PROJECT_NAME = "aomi-2026-09-p2"\nCHARACTER_NAME = "aomi"\n'
out += 'MODEL_DIR = "G:/My Drive/Projects/Aomi-mama/1.picture"\n\nTIMELINES = ' + pprint.pformat(rows, width=140, sort_dicts=False) + "\n"
(ROOT / "projects/aomi_p2").mkdir(exist_ok=True)
(ROOT / "projects/aomi_p2/mapping.py").write_text(out, encoding="utf-8")
(ROOT / "projects/aomi_p2/__init__.py").write_text("", encoding="utf-8")
print(len(rows), "rows;", sum(1 for r in rows if r["flag"]), "flagged")
