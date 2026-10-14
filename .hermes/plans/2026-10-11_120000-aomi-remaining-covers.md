---
name: aomi-2026-09-remaining-covers-plan
description: Plan to build covers for 7 uncovered Aomi-mama MP4s + full pipeline
---

# Plan: Aomi-mama 2026-09 Remaining Covers

## Goal
สร้างปก YouTube (16:9 + 9:16) สำหรับ 7 คลิปที่ยังไม่มีปกในโฟลเดอร์ `2026-09-aomimama` โดยเชื่อมต่อกับ `aomi_p2` mapping ที่มีอยู่แล้ว และเพิ่มเข้า pipeline build/QC/delivery

## Current Context
- **Project ที่มีอยู่:** `projects/aomi_p2/mapping.py` มี 44 timelines (6 แหล่งวิดีโอ) ครอบคลุม Strinova 2 ไฟล์, Minecraft 003, Becastled 3 ไฟล์ → 88 ปกสร้างเสร็จแล้ว QC ผ่าน
- **คลิปที่ยังไม่มีปก (7 ไฟล์):**
  1. `20260906_【LIVE】alien shooter last hope_[7LTPPtZMUcU].mp4` (~6.4 GB)
  2. `20260906_【LIVE】alien shooter_[Qpmx0v-3Xcg].mp4` (~2.3 GB)
  3. `20260907_【LIVE】Minecraft Server Dreamlight - 001 #aomimama_[X6E3DjqX8c8].mp4` (~4.9 GB)
  4. `20260910_【LIVE】alien shooter 2_[M0oO81RLbA8].mp4` (~2.8 GB)
  5. `20260911_หงุดหงิด ฉุนเฉียว_[hskX-AdzKFw].mp4` (~4.8 GB)
  6. `20260914_【LIVE】Minecraft Server Dreamlight - 002 #aomimama_[x4NRaygzFc4].mp4` (~6.6 GB)
  7. `20260915_【LIVE】League of Legends - 003_[dKPqq7UGwuA].mp4` (~6.7 GB)
- **Asset โมเดล:** `G:/My Drive/Projects/Aomi-mama/1.picture/` มี vts_avatar 13 ท่า + chibi_emote 6 ท่า + game_first_livestream 8 ภาพ
- **Tools ที่มี:** `src.engine.ThumbnailCompositor`, `cli/build.py`, `cli/verify.py`, `cli/doctor`, ffmpeg, `vtuber-thumbnail-qc` skill
- **Constraints:**
  - ไม่มี subtitle สำหรับ 7 ไฟล์ใหม่ (ต้องสร้างผ่าน Resolve ASR หรือใช้ชื่อ Timeline เป็น hook เบื้องต้น)
  - ไม่มี Timeline ใน DaVinci Resolve สำหรับคลิปเหล่านี้ (ต้องสร้างจากต้นฉบับหรือข้ามขั้นตอนนี้ไปใช้คลิปตรง)
  - `python3` ไม่มีใน PATH ใช้ `python` (Hermes-bundled 3.14.7) แทน

## Assumptions
1. ผู้ใช้ต้องการใช้ตัวละคร **Aomi-mama** (ตามโฟลเดอร์ `1.picture`) ไม่ใช่ Tygarina (ข้อความ "ใช้ตัวละคร Tygarina" ในคำสั่งเป็น template error)
2. ชื่อโฟลเดอร์จริงคือ `2026-09-aomimama` (a ตัวเดียว) ไม่ใช่ `2026-09-aomimamaa`
3. หากไม่มี subtitle จะใช้ชื่อ Timeline เป็น hook หลัก โดยติด flag `title-only` และแนะนำให้ตรวจเนื้อหากับคลิปจริงก่อนอัปโหลด
4. ปกใหม่จะบันทึกแยกวันที่ (เช่น `2026-10-11`) หรือรวมกับ `aomi_p2` เดิม — ใช้วันที่แยกเพื่อไม่ให้ปะปน

## Proposed Approach
1. **Inventory & Subtitle Extraction:** สร้าง timeline-inventory.json สำหรับ 7 ไฟล์ใหม่ โดยใช้ ffprobe ตรวจความยาว และใช้ชื่อไฟล์เป็นชื่อ Timeline เบื้องต้น
2. **Hook Assignment:** สร้าง mapping entries สำหรับคลิปใหม่ ใช้ชื่อ Timeline (ตัดส่วน YouTube ID) เป็น hook + sec เบื้องต้น ติด flag `title-only` ทุกใบ
3. **Frame Extraction:** ดึง 1 เฟรมต่อ Timeline จาก `src_start + frame_tl` ด้วย ffmpeg
4. **Build Covers:** ใช้ `ThumbnailCompositor` + `build_aomi_p2_covers.py` pattern สร้างปก 16:9 + 9:16 ทุกคลิป
5. **Verify + QC:** รัน `cli.verify` → `vtuber-thumbnail-qc` → แก้ CRITICAL → `cli.package`
6. **เปิดโฟลเดอร์:** `python -m cli.open aomi` + ลิงก์ไฟล์

## Step-by-Step Tasks

### Task 1: ตรวจสอบ environment และ assets
```bash
python -m cli.doctor
ls "G:/My Drive/Projects/Aomi-mama/1.picture/" | grep -c ".png$"
```
Expected: doctor ผ่านทั้งหมด (Pillow, numpy, libraqm, Mitr Bold, ffmpeg), พบ PNG >= 20 ไฟล์

### Task 2: สร้าง timeline inventory สำหรับ 7 ไฟล์ใหม่
- เขียนสคริปต์ `scratch/aomi_remaining_inventory.py` ใช้ ffprobe ตรวจ duration/size ของแต่ละ MP4
- สร้าง JSON list: `[{name, src, duration_s, frames_60fps}]`
- บันทึกเป็น `reports/aomi/2026-10-11/timeline-inventory-new.json`

### Task 3: สร้าง mapping entries สำหรับคลิปใหม่
- อ่าน `projects/aomi_p2/mapping.py` เพื่อหารูปแบบ
- สำหรับแต่ละคลิปใหม่ สร้าง TIMELINES entries:
  - `name` = ชื่อไฟล์ (ตัด `_['...'].mp4`)
  - `tl_short` = `name + "_9x16"`
  - `src` = พาธเต็ม
  - `src_start` = 0 (เริ่มคลิป)
  - `frame_tl` = 30 (ค่าเริ่มต้น)
  - `model_file` = เลือกจาก vts_avatar ที่มี (วนใช้ไม่ซ้ำ)
  - `talk` = False (เกมเพลย์) ยกเว้นคลิป "หงุดหงิด ฉุนเฉียว" อาจเป็น talk
  - `hook` = [ตัด 1-4 คำจากชื่อคลิป]
  - `sec` = [ตัดส่วนเกมที่เหลือ]
  - `flag` = "title-only: no subtitle data"
- เพิ่ม entries เข้า `projects/aomi_p2/mapping.py` หรือสร้าง `projects/aomi_p2/mapping_remaining.py` แยก

### Task 4: Extract frames
- ใช้ `aomi_p2_extract_frames.py` pattern หรือเขียนสคริปต์ใหม่
- ดึงเฟรมจาก `src_start + frame_tl` ของแต่ละคลิป
- บันทึกเป็น `scratch/aomi-remaining-frames/<id>.png` + contact sheet

### Task 5: Build covers
- ใช้ pattern จาก `build_aomi_p2_covers.py`
- สร้าง 16:9 + 9/16 สำหรับแต่ละ Timeline
- บันทึก `outputs/aomi/2026-10-11/` + manifest `reports/aomi/2026-10-11/delivery-manifest.json`

### Task 6: Verify
```bash
python -m cli.verify --jpg-dir outputs/aomi/2026-10-11 --manifest reports/aomi/2026-10-11/delivery-manifest.json
```
Expected: 100% pass (JPEG RGB, <=2MB, correct dimensions)

### Task 7: Auto-QC
- โหลด `vtuber-thumbnail-qc` skill
- รัน `qc_previews.py` บนทุกใบ
- ตรวจ CRITICAL → แก้ → rebuild → re-QC จนหมด 🔴
- บันทึก `reports/aomi/2026-10-11/qc-summary.md`

### Task 8: Package & Deliver
```bash
python -m cli.package --jpg-dir outputs/aomi/2026-10-11 --manifest reports/aomi/2026-10-11/delivery-manifest.json --out-zip packages/aomi/2026-10-11/package.zip
python -m cli.open aomi
```
- รายงานผล: จำนวนปกที่สร้าง, ผ่าน QC, ลิงก์โฟลเดอร์

## Tests / Validation
- `python -m pytest tests/test_projects.py` ผ่าน (รวม test ใหม่ถ้ามี)
- `cli.verify` 100% pass
- QC summary ไม่มี 🔴 CRITICAL
- Manifest count == 2 * number of new timelines
- ทุกไฟล์ใน manifest มีอยู่จริงใน `outputs/`

## Risks & Tradeoffs
| Risk | Mitigation |
|------|------------|
| ไม่มี subtitle สำหรับ 7 ไฟล์ | ใช้ชื่อ Timeline เป็น hook ติด flag title-only; แนะนำให้ตรวจเนื้อหากับคลิปจริง |
| ขนาดไฟล์ใหญ่ (4-7 GB) | ffmpeg seek ไปจุดที่ต้องการโดยไม่ต้อง decode ทั้งไฟล์ (`-ss` ก่อน `-i`) |
| โมเดลซ้ำท่า (13 ท่า / 7 คลิป) | เลือกท่าต่างกันตามอารมณ์ที่คาดจากชื่อคลิป; ใช้ chibi_emote เสริม |
| คลิป "หงุดหงิด ฉุนเฉียว" ไม่มีชื่อเกม | ตรวจว่าเป็นเกมอะไรจากเฟรม; ถ้าไม่ชัดเจนใช้ blur หนัก (talk mode) |
| ไม่มี Timeline ใน Resolve | ข้ามขั้น Resolve; ทำงานกับ MP4 ตรงผ่าน ffmpeg |

## Open Questions
1. ผู้ใช้ต้องการให้สร้าง Timeline ใหม่ใน DaVinci Resolve ด้วยหรือไม่? (ตอนนี้มีแต่ MP4)
2. "หงุดหงิด ฉุนเฉียว" คือเกมอะไร? (ต้องดูเฟรมหรือถามผู้ใช้)
3. ต้องการแยกวันที่ `2026-10-11` หรือรวมกับ `2026-10-10` (aomi_p2 เดิม)?
4. ต้องการให้ใช้ chibi_emote ด้วยหรือไม่? (ตอนนี้ยังไม่ได้ใช้)

</content>