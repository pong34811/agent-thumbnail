# Project Instructions

โปรเจกต์สร้าง ตรวจสอบ และแพ็กเกจภาพปก YouTube ของ VTuber ทั้ง 16:9 (1920x1080) และ Shorts 9:16 (1080x1920) ประกอบด้วย Core Engine (`src/`), CLI (`cli/`), ค่าคอนฟิกรายโปรเจกต์ (`projects/<ชื่อ>/mapping.py`, `projects/channels.json`) และ Pytest (`tests/`)

## Start Here

เริ่มทุกงานด้วย `python -m cli.doctor` (Pillow, numpy, libraqm, ฟอนต์ Mitr Bold, ffmpeg) ถ้า FAIL ให้แก้ก่อนสร้างปก เพราะ Thai layout จะเพี้ยนเงียบๆ

องค์ความรู้ด้านการออกแบบอยู่ใน `.agents/skills/` (`davinci-thumbnails`, `vtuber-thumbnail-layout`, `vtuber-thumbnail-qc`) skill ทั่วไปอยู่ใน `.claude/skills/` พร้อม `skills-lock.json` เป็นโฟลเดอร์จริง ห้ามทำ junction/symlink ข้ามสองที่นี้ เพราะการลบฝั่งหนึ่งจะลบอีกฝั่งตามไปด้วย

## Gotchas & Channels

- **ช่องงานหลักในระบบ (`projects/channels.json`):**
  - `aomi`: Aomi-mama (`outputs/aomi/`)
  - `armigon`: Armigon (`outputs/armigon/`)
  - `tygarina`: Tygarina (`outputs/tygarina/`)
  - `katy404`: Katy404 (`outputs/katy404/`)
  - `sakuyako`: Sakuyako-Cheris (`G:\My Drive\Projects\Sakuyako-Cheris`)
  - *หมายเหตุ:* `projects/lumina/references/` เป็นคลังอ้างอิงและกรณีศึกษามาตรฐานของค่าย VTuber (Reference Benchmark) ไม่ใช่ช่องงานสร้างปก
- **libraqm ต้อง import `src.engine.text_thai` ก่อน** เพราะโมดูลนี้โหลด `fribidi` จาก `src/engine/runtime/` ถ้าเช็ก `features.check("raqm")` ก่อน import จะได้ `False` ทั้งที่ใช้ได้
- **รูปแบบ mapping ต่างกันตามโปรเจกต์** `cli/build.py` (`resolve_text`) รองรับ `hook`/`sec` ระดับบนสุด, บล็อก `land`/`short` (Aomi) และดึง hook จากข้อความหลัง `" - "` ในชื่อ (Armigon) เมื่อเพิ่มโปรเจกต์ใหม่ ให้ใช้รูปแบบใดรูปแบบหนึ่งนี้
- **mapping ต้องระบุพาธเฟรมพื้นหลัง (`bg`/`frame_path`) และโมเดล RGBA จริง** ไม่เช่นนั้นปกจะเป็นพื้นสีเรียบไม่มีโมเดล โปรเจกต์ที่มี `MODEL_DIR` (Armigon) จะ resolve ชื่อไฟล์โมเดลจากโฟลเดอร์นั้น และ `cli.build` เตือนเมื่อหาไฟล์ไม่เจอ
- **กฎเหล็กฉากหลังเกม (Clean Background):** ห้ามใช้เฟรม Live ที่ติดกล้องสตรีม (Facecam), แถบเป้าหมายโดเนท, หรือแชต โดยเด็ดขาด หากฟุตเทจต้นฉบับมี ให้ทำ Clean Crop เจาะเฉพาะโซนเกมเพลย์ 100% (0px blur) ป้องกันไม่ให้เกิดตัวละครซ้อนสองตัว
- **ปก Shorts จัดข้อความกึ่งกลางที่ `ShortsLayout.CENTER_X`** (มีเทสต์ล็อกไว้)
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

## Design Conventions (มาตรฐาน Golden Pipeline)

- **The 1-2 Punch:** ปก = อารมณ์และปมสงสัย (Hook สั้น 1–4 คำ), ชื่อคลิป = บริบทและคีย์เวิร์ด ห้ามก็อปปี้ชื่อคลิปมาวางบนปก
- **Hook สั้น 1-4 คำ:** ตัวหลักแดง `#EC1C24` หรือเหลืองทอง ขอบดำหนา (stroke ~8%), ตัวรองขาวขอบดำ
- **Avatar 5-Layer Separation:** ฝั่งขวาของปกแนวนอน สัดส่วน 35-50% ของเฟรม หลบมุมขวาล่าง (Timestamp) มี White Rim Light (10–16px) และ Drop Shadow นุ่มลึก
- **Unblurred Footage (Clean Background):** ฉากเกมเพลย์ 0px blur เสมอ ใช้ Gradient Mask ด้านซ้ายรองรับตัวหนังสือ ห้ามติดกล้องสตรีม/Facecam, แถบโดเนท, แชต หรือลายน้ำสตรีมเด็ดขาด
- **No Clashing Graphical Elements:** Focus Circle (วงกลมแดง) หรือ Emotion Marker ต้องไม่ทับซ้อนกับตัวหนังสือ หากจุดสนใจในเกมชัดเจนอยู่แล้ว ให้งดใส่วงกลมเพื่อไม่ให้ภาพรก
- **Shorts 3-Tier Architecture:** จัดองค์ประกอบใหม่ใน Safe Zone (หลบแถบบน 10%, แถบล่าง 25% และขวา 15%) โดยใช้ Ambient Blur หลังสุด + กรอบเกมเพลย์ 1080×680 ตรงกลาง + Hook บน Safe Zone (`y ≈ 380px`) + Avatar กลางล่าง ห้ามครอปปกแนวนอนตรงๆ
- **Shorts Avatar Sizing:** ตัวละครในปก Shorts ต้องมีขนาดใหญ่และเด่นชัดเสมอ (สเกลความสูง **1,100–1,250px** หรือกว้าง 70–80% ของความกว้างจอ) ฐานยึดที่ขอบล่าง ใบหน้าและตาต้องอยู่ใน Safe Zone กลางจอ ห้ามทำตัวละครขนาดเล็กหรือปล่อยให้ลอยเคว้ง
- **Armigon Shorts:** ก่อนทำปกแนวตั้งของ Armigon ให้อ่าน [portrait style reference](projects/armigon/references/portrait-style-reference.md) และใช้ภาพตัวอย่างที่ผู้ใช้เลือกเป็น baseline โดยเปลี่ยนฉาก ข้อความ และสีหน้าตามแต่ละ Timeline

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
