# Project Instructions

โปรเจกต์สร้าง ตรวจสอบ และแพ็กเกจภาพปก YouTube ของ VTuber ทั้ง 16:9 (1920x1080) และ Shorts 9:16 (1080x1920) ประกอบด้วย Core Engine (`src/`), CLI (`cli/`), ค่าคอนฟิกรายโปรเจกต์ (`projects/<ชื่อ>/mapping.py`, `projects/channels.json`) และ Pytest (`tests/`)

## Start Here

เริ่มทุกงานด้วย `python -m cli.doctor` (Pillow, numpy, libraqm, ฟอนต์ Mitr Bold, ffmpeg) ถ้า FAIL ให้แก้ก่อนสร้างปก เพราะ Thai layout จะเพี้ยนเงียบๆ

องค์ความรู้ด้านการออกแบบอยู่ใน `.agents/skills/` (`davinci-thumbnails`, `vtuber-thumbnail-layout`, `vtuber-thumbnail-qc`) skill ทั่วไปอยู่ใน `.claude/skills/` พร้อม `skills-lock.json` เป็นโฟลเดอร์จริง ห้ามทำ junction/symlink ข้ามสองที่นี้ เพราะการลบฝั่งหนึ่งจะลบอีกฝั่งตามไปด้วย

## Gotchas

- **libraqm ต้อง import `src.engine.text_thai` ก่อน** เพราะโมดูลนี้โหลด `fribidi` จาก `src/engine/runtime/` ถ้าเช็ก `features.check("raqm")` ก่อน import จะได้ `False` ทั้งที่ใช้ได้
- **รูปแบบ mapping ต่างกันตามโปรเจกต์** `cli/build.py` (`resolve_text`) รองรับ `hook`/`sec` ระดับบนสุด, บล็อก `land`/`short` (Aomi) และดึง hook จากข้อความหลัง `" - "` ในชื่อ (Armigon) เมื่อเพิ่มโปรเจกต์ใหม่ ให้ใช้รูปแบบใดรูปแบบหนึ่งนี้
- **mapping ต้องระบุพาธเฟรมพื้นหลัง (`bg`/`frame_path`) และโมเดล RGBA จริง** ไม่เช่นนั้นปกจะเป็นพื้นสีเรียบไม่มีโมเดล (Armigon ตอนนี้ยังมีแค่ชื่อไฟล์ลอยๆ เช่น `cry.png`)
- **`_LATEST` ซิงก์จากโฟลเดอร์วันที่ล่าสุดที่มีรูปจริง** (`cli/organize.py`) โฟลเดอร์ว่างจะไม่ล้างของเดิม
- สคริปต์ตัวอย่างเก่าของ Armigon อยู่ที่ `.agents/skills/davinci-thumbnails/scripts/` ส่วน `tools/` และ `.work/` ถูกลบแล้ว (ดู git history)

## Testing & QA

```bash
python -m pytest tests/
python -m cli.verify --jpg-dir outputs/<channel>/<date> --manifest reports/<channel>/<date>/delivery-manifest.json
python -m cli.package --jpg-dir outputs/<channel>/<date> --manifest reports/<channel>/<date>/delivery-manifest.json --out-zip packages/<channel>/<date>/package.zip
```

`cli.verify` ตรวจขนาด ≤2MB, RGB/JPEG, สัดส่วน และไฟล์ที่ manifest อ้างถึงต้องมีอยู่จริงในโฟลเดอร์

**QC ปกอัตโนมัติ (บังคับทุกครั้งหลังทำปกเสร็จ):** หลัง `cli.verify` ผ่าน ให้โหลด skill `vtuber-thumbnail-qc` แล้ว QC ปกทุกใบที่เพิ่งทำ (แนวนอนและ Shorts) โดยไม่ต้องรอผู้ใช้สั่ง แก้ปัญหา 🔴 CRITICAL แล้ว build + verify + QC ซ้ำจนไม่เหลือ CRITICAL จากนั้นจึงแพ็กเกจและส่งมอบพร้อมรายงาน QC

## Design Conventions

- **Hook สั้น 1-4 คำ:** ตัวหลักแดง `#EC1C24` หรือเหลืองทอง ขอบดำหนา (stroke ~8%), ตัวรองขาวขอบดำ
- **Avatar:** ฝั่งขวาของปกแนวนอน สัดส่วน 35-50% ของเฟรม หลบมุมขวาล่าง (Timestamp) มี White Rim Light และ Drop Shadow
- **Unblurred Footage:** ฉากเกมเพลย์ 0px blur เสมอ ใช้ Gradient Mask ด้านซ้ายรองรับตัวหนังสือ
- **Shorts:** จัดองค์ประกอบใหม่ใน Safe Zone ครึ่งบนและกลาง (หลบแถบล่าง 25% และขวา 15%) ห้ามครอปปกแนวนอนตรงๆ

## Channel Output & Handover Protocol (กฎเหล็ก)

ทุกครั้งที่ทำปกเสร็จ ไม่ว่าช่องใด:

1. **`outputs/` เก็บเฉพาะรูปภาพ (.jpg, .png) เท่านั้น**
   - `outputs/<channel>/<YYYY-MM-DD>/` รวมปก 16:9 และ 9:16 ไว้ด้วยกัน ไม่แยกโฟลเดอร์ย่อย
   - `outputs/<channel>/_LATEST/` ทางลัดของรอบล่าสุด
   - `reports/<channel>/<YYYY-MM-DD>/` เก็บ `.json`, `.md`, `.log` (Manifest, QC)
   - `packages/<channel>/<YYYY-MM-DD>/` เก็บ `.zip`
2. **เปิดโฟลเดอร์ให้ผู้ใช้ทันที:** รัน `python -m cli.open <channel>` (เปิด `outputs/<channel>/_LATEST` ใน Windows File Explorer)
3. **ข้อความสุดท้ายต้องมีลิงก์ที่คลิกได้:**
   `[เปิดโฟลเดอร์ภาพปกทั้งหมด](file:///C:/Users/warit/Desktop/agent-thumbnail/outputs/<channel>/_LATEST)`
