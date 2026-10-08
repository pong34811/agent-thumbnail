# Agent-Thumbnail: Intelligent VTuber & Gaming YouTube Thumbnail Engine

> **ระบบ AI และไปป์ไลน์วิศวกรรมการผลิตปก YouTube ประสิทธิภาพสูง (High-CTR) สำหรับ VTuber และสตรีมเมอร์เกมมิ่ง ที่ผสานหลักจิตวิทยาการรับรู้ของมนุษย์, การสกัดหลักฐานจากวิดีโอไทม์ไลน์, และความประณีตของระบบ Typography ภาษาไทย**

---

## 1. Executive Summary & Vision

**Agent-Thumbnail** คือระบบอัตโนมัติสำหรับการสร้าง ตรวจสอบ และเพิ่มประสิทธิภาพภาพปก YouTube (Thumbnail Optimization) ที่เปลี่ยนผ่านจากการออกแบบด้วยมือที่ซ้ำซ้อน ไปสู่ **ระบบเอเจนต์ที่ชาญฉลาด (Autonomous Thumbnail Agent)** 

ระบบไม่ได้มองว่าปกคลิปเป็นเพียง "ภาพประกอบสวยงาม" แต่มองเป็น **"วิศวกรรมการดึงดูดสายตาและการตัดสินใจใน 3 วินาที (Glance Economy & Pre-attentive Processing)"** โดยมุ่งเน้นการสร้างภาพปกที่หยุดสายตาผู้ใช้งานบนหน้าฟีด YouTube (Mobile & Desktop), หลบเลี่ยง UI ของแพลตฟอร์มอย่างสมบูรณ์แบบ, รักษาระดับคอนทราสต์ในทุกสภาพแวดล้อม และยึดโยงกับเหตุการณ์จริงในวิดีโอ (Evidence-based Storytelling) เพื่อเพิ่มทั้งอัตราการคลิก (**CTR**) และการรับชมต่อเนื่อง (**AVD**)

---

## 2. Core Pillars & Design Philosophy (เสาหลักของระบบ)

1. **Evidence Over Hallucination (ความจริงจากฟุตเทจ):**
   - Hook และฉากบนปกต้องมีหลักฐานจริงจาก Timeline, Subtitle หรือบทพูดในคลิป ไม่ใช้การอนุมานหรือการแต่งเรื่องที่ไม่เกิดขึ้นจริง
   - ไม่ใช้ Deceptive Clickbait ที่ทำลายค่า Average View Duration (AVD)
2. **Dual-Surface Independent Engineering (แยกสัดส่วนเด็ดขาด):**
   - แนวนอน 16:9 (`1920×1080`) และแนวตั้ง 9:16 Shorts (`1080×1920`) เป็นงานจัดวางคนละบริบท
   - **ห้ามครอปแนวนอนเป็นแนวตั้งโดยเด็ดขาด** Shorts ต้องถูกจัดวางใหม่โดยยึดแกนกลางแนวนอนและคำนึงถึง Channel Grid 4:5 Crop
3. **Cognitive Psychology & The 3-Second Rule:**
   - **Gaze Cuing & Avatar Psychology:** ใช้อวาตาร์สบตาตรง (Direct Eye Contact) เพื่อสร้างความสนิทสนม หรือหันสายตามองจุดเกิดเหตุ (Gaze Cuing) เพื่อชี้นำสายตาคนดู
   - **Avatar Expression Matrix:** แมตช์สีหน้าสุดขั้ว (Shock, Horror, Smug, Laugh, Despair) ให้ตรงกับจุดพีกของคลิป หลีกเลี่ยงอาการหน้าแข็งทื่อ (Deadpan Doll Effect)
   - **Hand-drawn Red Brush Loop (`#EC1C24`):** วงเน้นจุดผิดปกติ/บั๊ก/มอนสเตอร์ด้วยเส้นพู่กันวาดมือจำลองความเร่งด่วนหน้างาน
4. **Title-Thumbnail Synergy (หมัด 1-2):**
   - ภาพปกทำหน้าที่เป็น **"หมัด 1 (Emotion / Mystery Trigger)"** ใช้คำ Hook สั้นเพียง 1–4 คำ กระตุกต่อมอยากรู้
   - ชื่อคลิปทำหน้าที่เป็น **"หมัด 2 (Context / Logic Anchor)"** อธิบายชื่อเกมและคีย์เวิร์ดค้นหา โดยห้ามนำคำบนปกมาซ้ำกับชื่อคลิป
5. **Precision Thai Typography (ความประณีตของฟอนต์ไทย):**
   - เรนเดอร์ด้วย Pillow + `libraqm` (RAQM Layout Engine) เพื่อตำแหน่งสระ-วรรณยุกต์ที่ถูกต้อง 100%
   - คำนวณความสูงตาม Ink Bounding Box ซ้อนบรรทัดกระชับแน่น
   - มีอัลกอริทึม Nudge Offset แยกเลเยอร์วรรณยุกต์เพื่อเคลียร์ปัญหาสระชนหางอักษรสูง (`ป, ฝ, ฟ`) และสระนำหน้า (`ไ, ใ, โ`)

---

## 3. Current Architecture & Production Pipeline (สถานะปัจจุบัน)

ปัจจุบันระบบทำงานในรูปแบบ **Hybrid Production Engine** ประกอบด้วย 4 กลไกหลัก:

```
[DaVinci Resolve Project (.drp) / Video / Subtitles]
                         │
                         ▼
   ┌───────────────────────────────────────────────┐
   │ 1. RESOLVE & MEDIA EXTRACTION PIPELINE        │
   │    - resolve_timeline_audit.py (สแกนไทม์ไลน์) │
   │    - extract_textplus.py (ดึงแคปชัน Text+)     │
   │    - sample_frames.py (สุ่มเฟรมตามคิวบทพูด)   │
   └───────────────────────────────────────────────┘
                         │
                         ▼
   ┌───────────────────────────────────────────────┐
   │ 2. PROGRAMMATIC COMPOSITING ENGINE            │
   │    - build_covers.py (Pillow + RAQM Engine)    │
   │    - Avatar 5-Layer Separation (Stroke+Shadow)│
   │    - Backdrop Gradient Mask (ฉากเกม 0px blur) │
   │    - Safe Zone Enforcement (Center-Left y:380)│
   └───────────────────────────────────────────────┘
                         │
                         ▼
   ┌───────────────────────────────────────────────┐
   │ 3. CANVA & AGENT INTEGRATION                  │
   │    - davinci-thumbnails skill                 │
   │    - Canva API Page Duplication & Layer Sync  │
   │    - Automated Contact Sheets & Delivery Pack │
   └───────────────────────────────────────────────┘
                         │
                         ▼
   ┌───────────────────────────────────────────────┐
   │ 4. QUALITY CONTROL & VERIFICATION             │
   │    - verify_covers.py (ตรวจมิติ, ขอบ, collision)│
   │    - Mobile Squint Test (320x180 & 160x90)    │
   │    - package.py & CRC Integrity Check         │
   └───────────────────────────────────────────────┘
```

### คลังเครื่องมือและสคริปต์ในระบบ:
* `(ลบแล้ว) tools/timeline-covers/resolve_timeline_audit.py`: เชื่อมต่อ Resolve API อ่าน Metadata ทุก Timeline แบบ Headless
* `(ลบแล้ว) tools/timeline-covers/extract_textplus.py`: ถอดรหัสโครงสร้าง `.drp` ดึงข้อความ Text+ โดยตรงโดยไม่ต้องเปิด Fusion
* `(ลบแล้ว) tools/timeline-covers/sample_frames.py`: แคปเฟรมภาพความละเอียดสูงจาก `src.mp4` ตรงตามจุดเวลาของ Subtitle
* `(ลบแล้ว) tools/timeline-covers/build_covers.py`: เอนจินประกอบภาพแบบ Batch อัตโนมัติ รองรับพารามิเตอร์ Hook, Secondary, Crop, และ Expression
* `(ลบแล้ว) tools/timeline-covers/verify_covers.py`: ระบบตรวจรับประกันคุณภาพอัตโนมัติ (Automated QA Gatekeeper)
* `.agents/skills/davinci-thumbnails/`: ทักษะเอเจนต์พร้อมคู่มือยุทธศาสตร์ [vtuber-thumbnail-engagement-guide.md](.agents/skills/davinci-thumbnails/references/vtuber-thumbnail-engagement-guide.md)

---

## 4. Production History & Deliverables (ประวัติผลงานที่ส่งมอบแล้ว)

ระบบถูกใช้งานจริงและส่งมอบผลงานคุณภาพสูงในระดับอุตสาหกรรมแล้วหลายโปรเจกต์:
1. **Aomi Debut Stream (`outputs/aomi-debut-20260731/`):** 8 ไทม์ไลน์เดบิวต์ × 2 สัดส่วน (แนวนอน 16:9 + Shorts 9:16) พร้อมระบบแก้ปัญหาสระไทย
2. **Tygarina Project (`outputs/tygarina-20260801/`):** การทำปกไฮไลท์วาไรตี้และโมเมนต์เด็ด
3. **Armigon Enhancement Batch (`outputs/armigon-20260920-final-20260928/`):** 32 ชิ้นงาน (16 แนวนอน + 16 แนวตั้ง) ยกระดับสู่ Center-Left Elevation, Avatar Expression Matrix ครบ 6 อารมณ์, วงกลมพู่กันแดง และเครื่องหมาย `!` / `?` สไตล์อนิเมะ

---

## 5. Product Evolution Roadmap (แผนการพัฒนาสู่ Autonomous Agent)

```
[Phase 1: Specialized Batch Engine] ──► [Phase 2: Portable Configurable CLI] ──► [Phase 3: Autonomous AI Agent]
       (สถานะปัจจุบัน: สำเร็จแล้ว)                (ระยะใกล้: ไตรมาสถัดไป)                    (เป้าหมายสูงสุด)
```

### Phase 1: Specialized Batch Engine (Current State - Completed)
- [x] ไปป์ไลน์สกัดข้อมูลจาก DaVinci Resolve Timeline และ Subtitles
- [x] เอนจินเรนเดอร์ Pillow + RAQM สำหรับฟอนต์ไทย Mitr Bold พร้อมระบบแก้ปัญหาสระลอย/วรรณยุกต์ติดหาง
- [x] ผัง Safe Zone แนวนอน 16:9 และ Shorts 9:16 หลบ UI แพลตฟอร์มสมบูรณ์
- [x] ทักษะเอเจนต์ Canva Workflows และ Reference Guides เชิงลึก

### Phase 2: Portable & Configurable CLI (Near-Term Focus)
- [ ] **Decouple Machine Paths:** แปลงพาธเฉพาะเครื่อง (`D:\...`, `C:\...`) เข้าสู่ไฟล์คอนฟิกสากล `project.yaml`
- [ ] **Unified CLI Interface:** รวมคำสั่งให้อยู่ใน CLI กลาง (เช่น `agent-thumbnail audit`, `agent-thumbnail build`, `agent-thumbnail verify`)
- [ ] **Dynamic Avatar Library Manager:** ระบบจัดการคลังภาพอวาตาร์แยกตามสีหน้า (Expression Tags: `shock`, `angry`, `smug`, `cry`) เพื่อให้ระบบเลือกภาพที่ตรงกับอารมณ์ของคลิปอัตโนมัติ

### Phase 3: Autonomous End-to-End AI Agent (Ultimate Vision)
- [ ] **Multimodal Climax Detection:** วิเคราะห์เสียง (หาจุดกรีดร้อง/หัวเราะ) และภาพวิดีโอเพื่อระบุจุด Climax ประจำคลิปโดยอัตโนมัติ
- [ ] **LLM Hook Strategist:** ถอดบทพูด (Speech-to-Text) แล้วระดมความคิดสร้าง Hook ไทยสั้น 1–4 คำ ที่สร้าง Curiosity Gap สูงสุด พร้อมตั้งชื่อคลิปแบบหมัด 1-2
- [ ] **Computer Vision Composition Scoring:** ตรวจจับใบหน้าและจุดโฟกัสเพื่อคำนวณคะแนน Visual Clarity และ Contrast Score ก่อนส่งออก
- [ ] **YouTube Studio A/B Test Integration:** อัปโหลดปกหลายเวอร์ชันขึ้นระบบ "Test & Compare" ของ YouTube ผ่าน API และเก็บสถิติ CTR จริงเพื่อป้อนกลับมาเทรนโมเดล (Reinforcement Learning from CTR Data)

---

## 6. Technical Stack & Environment

* **Language:** Python 3.10+
* **Core Libraries:**
  * `Pillow` (พร้อม `libraqm` สำหรับ Complex Text Layout ภาษาไทย)
  * `NumPy` (สำหรับ Matrix Manipulation และ Alpha Channel Bounding Box)
  * `ffmpeg` (สำหรับ High-speed Video Frame Extraction)
* **Video Editor Integration:** DaVinci Resolve Scripting API (Python)
* **Design Platform:** Canva API & Canva Design Templates
* **Agent Harness:** Google Antigravity Agent Framework (Superpowers Subagent-Driven Development)
