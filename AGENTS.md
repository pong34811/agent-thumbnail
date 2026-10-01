# Project Instructions

โปรเจกต์นี้เป็นชุดโมดูล Core Engine (`src/`), ชุดคำสั่ง CLI (`cli/`), ค่าคอนฟิกโปรเจกต์ (`projects/`), และชุดทดสอบ (`tests/`) สำหรับสร้าง ตรวจสอบ และแพ็กเกจภาพปก YouTube (16:9 Landscape 1920x1080 และ 9:16 Shorts 1080x1920) ของ VTuber พร้อมเอกสารทฤษฎี CTR และศิลปะการจัดวางใน `.agents/skills/davinci-thumbnails/`

## Repository Map

- `src/engine/` — Core Engine สำหรับประมวลผลปก YouTube:
  - `text_thai.py` — Pillow + libraqm Thai layout, stroke ratio, ink bbox line stacking, upper mark collision avoidance สำหรับ `ป, ฝ, ฟ` และ `ไ, ใ, โ`
  - `graphics.py` — องค์ประกอบเล่าเรื่อง (Hand-drawn Red Circle `#EC1C24`, Anime Badges `!`/`?`, Dark Gradient Mask สำหรับคงความคมชัดเกม 0px blur, Avatar 5-layer separation)
  - `layout.py` — กฎ Safe Zone และ YouTube UI Danger Zone (หลบ Timestamp มุมขวาล่าง, Scrubber ล่างสุด, Crop 4:5 บน Channel Grid สำหรับ Shorts)
  - `compositor.py` — `ThumbnailCompositor` ไพป์ไลน์หลักสำหรับประกอบภาพปก Landscape และ Shorts
- `src/resolve/` — โมดูลเชื่อมต่อ DaVinci Resolve:
  - `audit.py` — ตรวจสอบและดึงข้อมูล Project / Timeline แบบ Headless
  - `textplus.py` — สกัดข้อความ Text+ และ Subtitle จาก `.drp`
- `projects/` — การตั้งค่าและ Mapping ข้อมูลเฉพาะแต่ละโปรเจกต์:
  - `aomi_debut/` — Timeline และข้อมูลปก Aomi Debut
  - `tygarina/` — Timeline และ Hook สำหรับ Tygarina
  - `armigon/` — Timeline 16 ชุด และ Accents สำหรับ Armigon
- `cli/` — เครื่องมือ Command Line กลาง:
  - `build.py` — สั่งสร้างปกด้วย `--project <name>`
  - `verify.py` — ตรวจสอบคุณภาพอัตโนมัติ (Dimensions, Max 2MB, sRGB/RGB, Margins, Squint Preview 320x180)
  - `package.py` — ตรวจสอบและบีบอัด ZIP พร้อม Manifest และทดสอบ CRC + Decodability
  - `sample_frames.py` — ดึงเฟรมจากวิดีโอด้วย ffmpeg ตาม Timestamp
- `tests/` — ชุดการทดสอบระบบอัตโนมัติ (Pytest)
- `outputs/` — ภาพ JPG, preview, manifest และ ZIP ที่ส่งมอบแล้ว
- `.agents/skills/davinci-thumbnails/` — องค์ความรู้ด้าน Thumbnail Psychology, CTR Strategy, Canva Workflow และ YouTube Surface Guides

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
- ทดสอบบีบอัดและตรวจความสมบูรณ์ของแพ็กเกจส่งมอบ:
  ```bash
  python -m cli.package --jpg-dir outputs/<project>/jpg --manifest outputs/<project>/delivery-manifest.json --out-zip outputs/<project>/package.zip
  ```

## Design & Engineering Conventions

- **Hook สั้นกระชับ (1-4 คำ):** ตัวหนังสือหลักสีแดงสด `#EC1C24` หรือเหลืองทอง ขอบดำหนา (Stroke ratio ~8%), ตัวรองสีขาว ขอบดำ
- **Avatar Silhouette & Gaze:** อวาตาร์วางฝั่งขวาบนปกแนวนอน (สัดส่วน 35-50% ของเฟรม) หลบ UI มุมขวาล่าง มี White Rim Light และ Drop Shadow ดึงโมเดลลอยออกจากฉาก
- **Unblurred Footage:** ฉากเกมเพลย์คงความคมชัด 0px blur เสมอ แล้วใช้ Gradient Mask ด้านซ้ายเพื่อรองรับตัวหนังสือ
- **Shorts Composition:** ขนาด 1080x1920 จัดองค์ประกอบให้อวาตาร์และข้อความอยู่ใน Safe Zone ครึ่งบนและกลาง (หลบแถบล่าง 25% และขวา 15%) โดยไม่นำปกแนวนอนมาครอปตรงๆ
