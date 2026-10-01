# timeline-covers

สคริปต์ที่ใช้ทำปก JPG ของ 【DEBUT STREAM】AOMI-MAMA｜31⧸07⧸2026 (8 Timeline × แนวนอน 1920×1080 + Shorts 1080×1920) ผลงานอยู่ที่ `outputs/aomi-debut-20260731/` บทเรียนและกติกาอยู่ใน `.agents/skills/davinci-thumbnails/references/jpg-render-notes.md`

ต้องใช้ Python ที่มี Pillow (พร้อม libraqm), numpy และ ffmpeg ใน PATH

## ลำดับการรัน

ทุกไฟล์ทำงานในโฟลเดอร์งานเดียวกัน (ค่าเดิม `D:\agent-thumbnail\.work\aomi-debut`)

1. `resolve_timeline_audit.py`: รันใน Resolve เพื่อเขียน `timeline-audit.json` (อ่านอย่างเดียว ไม่เปิด Fusion)
2. `extract_textplus.py <backup.drp> notes/textplus_before_improve.json`: ดึงข้อความ Text+ จากไฟล์ backup `.drp`
3. `sample_frames.py`: ดึงเฟรมตามคิว subtitle/Text+ ของทุก Timeline จาก `src.mp4` แล้วทำ contact sheet ไว้เลือกฉาก
4. `build_covers.py`: ตั้งค่า `TL` (ข้อความ hook/secondary, ไฟล์โมเดล, พื้นหลัง, crop) แล้วสร้าง JPG และ `delivery-manifest.json`
5. `verify_covers.py`: ตรวจชื่อไฟล์เทียบกับชื่อ Timeline, ขนาด, ขอบข้อความ, การทับโมเดล และการจัดกึ่งกลางของ Shorts
6. `make_overview.py`, `package.py`: ทำภาพรวมและ ZIP แล้วเปิด JPG ทุกไฟล์จาก ZIP อีกรอบ

ไฟล์ input ที่ต้องมีในโฟลเดอร์งาน:
- `models/` (ภาพโมเดล)
- `bg/tlN.png` (เฟรมเต็มจาก `src.mp4`)
- `stills/` (ภาพที่แทรกใน Timeline)
- `notes/`

ไฟล์เหล่านี้ไม่ได้เก็บไว้ใน repo
