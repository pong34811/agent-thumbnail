# Project Instructions

โปรเจกต์นี้เป็นชุดโมดูล Core Engine (`src/`), ชุดคำสั่ง CLI (`cli/`), ค่าคอนฟิกโปรเจกต์ (`projects/`), และชุดทดสอบ (`tests/`) สำหรับสร้าง ตรวจสอบ และแพ็กเกจภาพปก YouTube (16:9 Landscape 1920x1080 และ 9:16 Shorts 1080x1920) ของ VTuber พร้อมเอกสารทฤษฎี CTR และศิลปะการจัดวางใน `.agents/skills/davinci-thumbnails/`

## Repository Map

- `src/engine/` — Core Engine สำหรับประมวลผลปก YouTube:
  - `text_thai.py` — Pillow + libraqm Thai layout, stroke ratio, ink bbox line stacking, upper mark collision avoidance สำหรับ `ป, ฝ, ฟ` และ `ไ, ใ, โ`
  - `graphics.py` — องค์ประกอบเล่าเรื่อง (Hand-drawn Red Circle `#EC1C24`, Anime Badges `!`/`?`, Dark Gradient Mask สำหรับคงความคมชัดเกม 0px blur, Avatar 5-layer separation)
  - `layout.py` — กฎ Safe Zone และ YouTube UI Danger Zone (หลบ Timestamp มุมขวาล่าง, Scrubber ล่างสุด, Crop 4:5 บน Channel Grid สำหรับ Shorts)
  - `compositor.py` — `ThumbnailCompositor` ไพป์ไลน์หลักสำหรับประกอบภาพปก Landscape และ Shorts
  - `shorts_titles.py` — จัดชื่อคลิปแบบ 1 บรรทัดต่อสี (แดง/ขาว) สำหรับปก Shorts พร้อมตรวจว่าต่อกันได้ชื่อไทม์ไลน์เดิม
- `src/resolve/` — โมดูลเชื่อมต่อ DaVinci Resolve:
  - `audit.py` — ตรวจสอบและดึงข้อมูล Project / Timeline แบบ Headless
  - `textplus.py` — สกัดข้อความ Text+ และ Subtitle จาก `.drp`
- `projects/` — การตั้งค่าและ Mapping ข้อมูลเฉพาะแต่ละโปรเจกต์:
  - `channels.json` — Central Registry รวบรวมข้อมูลแบรนด์ สีประจำตัว และ Asset ของทุกช่อง
  - `aomi_debut/` — Timeline และข้อมูลปก Aomi Debut
  - `tygarina/` — Timeline และ Hook สำหรับ Tygarina
  - `armigon/` — Timeline 16 ชุด และ Accents สำหรับ Armigon
- `outputs/` — แกลเลอรีภาพปก (100% Images Only):
  - `katy404/` — ปกของ Katy404 (`_LATEST/` และโฟลเดอร์วันที่)
  - `tygarina/` — ปกของ Tygarina
  - `armigon/` — ปกของ Armigon
  - `aomi_debut/` — ปกของ Aomi Debut
- `reports/` — ที่จัดเก็บไฟล์ `.json` Manifest, รายงาน QC, และ Audit logs
- `packages/` — ที่จัดเก็บไฟล์บีบอัด `.zip` สำหรับส่งมอบงาน
- `cli/` — เครื่องมือ Command Line กลาง:
  - `build.py` — สั่งสร้างปกด้วย `--project <name>` หรือ Ad-hoc `--channel <name> --hook "..."`
  - `open.py` — เปิดโฟลเดอร์ภาพปกใน Windows File Explorer ทันที (`python -m cli.open [channel]`)
  - `organize.py` — จัดระเบียบภาพและซิงก์โฟลเดอร์ `_LATEST`
  - `verify.py` — ตรวจสอบคุณภาพอัตโนมัติ (Dimensions, Max 2MB, sRGB/RGB, Margins, Squint Preview 320x180)
  - `package.py` — ตรวจสอบและบีบอัด ZIP พร้อม Manifest และทดสอบ CRC + Decodability
  - `sample_frames.py` — ดึงเฟรมจากวิดีโอด้วย ffmpeg ตาม Timestamp
- `tests/` — ชุดการทดสอบระบบอัตโนมัติ (Pytest)
- `.agents/skills/` — องค์ความรู้ด้าน Thumbnail Psychology, CTR Strategy, Channel Profiles, Canva Workflow และ YouTube Surface Guides

## Environment & Dependencies

- ระบุใน `requirements.txt`:
  - `Pillow >= 10.0.0` (แนะนำให้คอมไพล์พร้อม libraqm เพื่อรองรับ complex Thai OpenType layout)
  - `numpy >= 1.24.0` (ใช้ในการคำนวณ Mask, Dilation, Morphological Shift)
  - `pytest >= 7.0.0`
- `ffmpeg` ต้องมีอยู่ใน `PATH` สำหรับการรัน `cli/sample_frames.py`
- ฟอนต์หลัก: `Mitr Bold` (ค้นหาอัตโนมัติจาก environment variable, Windows Fonts, หรือในไดเรกทอรี `outputs/timeline-covers/fonts/`)

## Testing & Quality Assurance

- รันชุดการทดสอบทั้งหมดด้วย:
  ```bash
  python -m pytest tests/
  ```
- ตรวจสอบไฟล์ผลลัพธ์ภาพปก:
  ```bash
  python -m cli.verify --jpg-dir outputs/<project>/jpg --manifest outputs/<project>/delivery-manifest.json
  ```
- **QC ปกอัตโนมัติ (บังคับทุกครั้งหลังทำปกเสร็จ):** หลัง `cli.verify` ผ่าน ให้โหลด skill `vtuber-thumbnail-qc` ด้วย `skill_view` แล้ว QC ปกทุกใบที่เพิ่งทำ (แนวนอนและ Shorts) โดยไม่ต้องรอผู้ใช้สั่ง แก้ปัญหา 🔴 CRITICAL แล้ว build + verify + QC ซ้ำจนผ่าน จากนั้นจึงแพ็กเกจและส่งมอบพร้อมรายงาน QC
- ทดสอบบีบอัดและตรวจความสมบูรณ์ของแพ็กเกจส่งมอบ:
  ```bash
  python -m cli.package --jpg-dir outputs/<project>/jpg --manifest outputs/<project>/delivery-manifest.json --out-zip outputs/<project>/package.zip
  ```

## Design & Engineering Conventions

- **Hook สั้นกระชับ (1-4 คำ):** ตัวหนังสือหลักสีแดงสด `#EC1C24` หรือเหลืองทอง ขอบดำหนา (Stroke ratio ~8%), ตัวรองสีขาว ขอบดำ
- **Avatar Silhouette & Gaze:** อวาตาร์วางฝั่งขวาบนปกแนวนอน (สัดส่วน 35-50% ของเฟรม) หลบ UI มุมขวาล่าง มี White Rim Light และ Drop Shadow ดึงโมเดลลอยออกจากฉาก
- **Unblurred Footage:** ฉากเกมเพลย์คงความคมชัด 0px blur เสมอ แล้วใช้ Gradient Mask ด้านซ้ายเพื่อรองรับตัวหนังสือ
- **Shorts Composition:** ขนาด 1080x1920 จัดองค์ประกอบให้อวาตาร์และข้อความอยู่ใน Safe Zone ครึ่งบนและกลาง (หลบแถบล่าง 25% และขวา 15%) โดยไม่นำปกแนวนอนมาครอปตรงๆ

## Channel Output & User Handover Protocol (กฎเหล็กการส่งมอบงาน)

ทุกครั้งที่ Agent ทำปกคลิปเสร็จ ไม่ว่าจะเป็นช่องใด (Katy404, Tygarina, Armigon, หรือช่องใหม่):

1. **โฟลเดอร์ outputs ต้องมี "เฉพาะรูปภาพเท่านั้น" (100% Images Only):**
   - **`outputs/<channel_name>/<YYYY-MM-DD>/`**: รวมภาพปกทั้งหมด (ทั้ง 16:9 แนวนอน และ 9:16 Shorts) อยู่ในโฟลเดอร์นี้ด้วยกัน **โดยไม่ต้องแยกโฟลเดอร์ย่อย** และ **ห้ามมีไฟล์อื่นที่ไม่ใช่รูปภาพ (.jpg, .png) ใน outputs เด็ดขาด!**
   - **`outputs/<channel_name>/_LATEST/`**: โฟลเดอร์ทางลัดรวมภาพของรอบล่าสุด
   - **`reports/<channel_name>/<YYYY-MM-DD>/`**: สำหรับเก็บไฟล์ `.json`, `.md`, `.log` (Manifest และ QC)
   - **`packages/<channel_name>/<YYYY-MM-DD>/`**: สำหรับเก็บไฟล์ `.zip` สำหรับส่งมอบ

2. **เปิดหน้าต่างไฟล์ให้ผู้ใช้ดูอัตโนมัติ (บังคับ):**
   เมื่อทำภาพเสร็จ Agent ต้องรันคำสั่ง:
   ```bash
   python -m cli.open <channel_name>
   ```
   คำสั่งนี้จะเปิดหน้าต่าง Windows File Explorer ไปยังโฟลเดอร์ `outputs/<channel>/_LATEST` บนหน้าจอของผู้ใช้ทันที โดยที่ผู้ใช้ไม่ต้องไปค้นหาเอง

3. **ส่งมอบด้วย Clickable Link ในข้อความสุดท้ายเสมอ:**
   ในข้อความตอบกลับผู้ใช้ Agent ต้องใส่ลิงก์ Markdown ตรงไปยังโฟลเดอร์ภาพ เช่น:
   - `[เปิดโฟลเดอร์ภาพปกทั้งหมด](file:///C:/Users/warit/Desktop/agent-thumbnail/outputs/<channel>/_LATEST)`


