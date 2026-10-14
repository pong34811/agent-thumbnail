# Portrait 9:16 Shorts (1080×1920) — Layout Rules

Source: `src/engine/layout.py::ShortsLayout`, `compositor.py::composite_shorts`, engagement guide §4.2, style guide Shorts section.

## Zones

| Zone | Bounds | Purpose |
|---|---|---|
| Text Safe Zone (Top) | `x: centered`, `y: 280–650` | Hook + ข้อความรอง |
| Avatar Zone (Bottom) | `y: 700–1100` (head), ฐานยึดขอบล่าง | VTuber model |
| Feed UI Bottom (DANGER) | `y: 1350–1920` | ชื่อคลิป, แอคเคาท์, เพลง |
| Feed Action Stack | `x: 880–1080`, `y: 800–1750` | Like/Comment/Share |
| Channel Grid 4:5 Crop | `y: 285–1635` | ตัดบน-ล่างด้านละ 285 px |
| Search 3:4 Crop | `y: 240–1680` | ตัดบน-ล่างด้านละ 240 px |

## Layer Order & 3-Tier Architecture (Golden Pipeline)

1. **Ambient Background:** เฟรมหลักขยายเต็ม 1080×1920 + Gaussian Blur (36px) + Brightness (0.48) + Color Saturation (1.15x) สร้างบรรยากาศมืดและไม่อึดอัด
2. **Sharp Center Gameplay Panel:** กรอบภาพเกมเพลย์คมชัด 0px blur ขนาด 1080×680 วางที่ `y: 560–1240` เพื่อให้เห็นหลักฐานเกมชัดเจน
3. **Top Safe Zone Hook:** ข้อความ Hook สีแดง `#EC1C24` + ข้อความรองสีขาว วางกึ่งกลางแนวนอนช่วงบน `y ≈ 280–540` (`y_cursor` เริ่มต้น 380px)
4. **Bottom Safe Zone Avatar:** โมเดลอวาตาร์ขนาดใหญ่และเด่นชัดเสมอ สเกลความสูง **1,100–1,250 px** (คิดเป็น 70–80% ของความกว้างจอ) วางกึ่งกลางแนวนอนช่วงล่าง ฐานยึดที่ขอบล่าง (`y: 1920 - height`) พร้อม White Rim Light 10–16px และ Drop Shadow ชัดเจน ไม่จมเข้าฉากหลัง ใบหน้าและดวงตาต้องอยู่ใน Safe Zone กลางจออย่างชัดเจน

## Text Rendering

- Hook: Mitr Bold, 150–100 px (fit_text auto-shrink), stroke 8%
- Secondary: Mitr Bold, 90–60 px, stroke 8%
- `x` เริ่ม 70, `y_cursor` เริ่ม 380 (baseline) เพื่อหลบขอบบน 10%
- Max width 760–940 px, กึ่งกลางแนวนอน `x=540` tolerance 15 px

## Shorts-Specific Rules

- **Avatar Sizing:** โมเดลต้องมีขนาดใหญ่สะดุดตาเสมอ สเกลความสูง **1,100–1,250 px** (70–80% ของความกว้างจอ 1080px) ห้ามใช้ตัวละครขนาดเล็ก (< 1,000 px) เพราะจะลอยเคว้งและขาด Visual Impact บนหน้าจอมือถือ
- จัดข้อความ + โมเดลให้อยู่กึ่งกลางแนวนอน — อย่าชิดขอบ
- หลีกเลี่ยงขอบบน 10%, ขอบล่าง 25% และขวา 15%
- ตรวจ 4:5 Channel Grid Crop: องค์ประกอบสำคัญอยู่ใน `y 285–1635`
- Shorts ต่างจากแนวนอน: จัดใหม่ตาม 9:16 ไม่ครอปแนวนอนแล้วอ้างว่าเป็น Shorts
- Hook Zone อยู่บน, Avatar Zone อยู่ล่าง — เล่าเรื่อง top→bottom

## Channel Profile Note

- KATY404 Shorts: ใบหน้าขนาดใหญ่เด่น (หน้า 86, 171), hook เหนือศีรษะ, อวาตาร์ล่าง
- อย่าตัดขอบปกแนวนอนมาทำ Shorts — เลือกหน้าคู่กันจากคอลเลกชัน Shorts แล้วจัดจุดเด่นใหม่
