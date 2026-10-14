# คู่มือและตัวอย่างมาตรฐานภาพปก Aomi-mama (Production Examples & Style Reference)

เอกสารบันทึกมาตรฐานการออกแบบ จัดวาง และเรนเดอร์ภาพปก YouTube ของช่อง **Aomi-mama【DL】** (`aomi`) ทั้งขนาด 16:9 (1920×1080) และ 9:16 Shorts (1080×1920) ตามเกณฑ์ Golden Pipeline

---

## 1. ผลงานตัวอย่างที่ผ่านเกณฑ์มาตรฐาน (Golden Pipeline Examples)

| ลำดับ | ตอน / เนื้อเรื่อง | สัดส่วน | ไฟล์ผลลัพธ์ใน `outputs/aomi/_LATEST/` | The 1-2 Punch (Hook / Secondary) | โมเดลสีหน้า (Avatar Expression) | ฉากหลังเกม (Clean Gameplay 0px blur) |
|:---:|:---|:---:|:---|:---|:---|:---|
| **1** | ตกลาวาตายกลางเกม | 16:9<br>9:16 | `ตกลาวาตายกลางเกม-Minecraft-vdo.jpg`<br>`ตกลาวาตายกลางเกม-Minecraft-vdo_9x16.jpg` | **"โดนลาวาเผา!"** (แดง `#EC1C24`)<br>"ของตกหมดตัว?!" (ขาว) | `game_first_livestream_08_chibi_flustered_pointing.png`<br>(ชิบิชี้นิ้วร้องไห้ มีหยดเหงื่อ ตกใจไฟลุก) | Clean Crop บ่อลาวาสีส้มสด แปลงผัก ภูเขาหิมะ คมชัด ไร้ Facecam/Hotbar |
| **2** | แพ้เกม! ปราสาทแตก | 16:9<br>9:16 | `แพ้เกม! ปราสาทแตก-Becastled-vdo.jpg`<br>`แพ้เกม! ปราสาทแตก-Becastled-vdo_9x16.jpg` | **"ปราสาทแตก!"** (แดง `#EC1C24`)<br>"แพ้ยับเยินเลย" (ขาว) | `vts_avatar_11_switch_gaze_down.png`<br>(ถือ Nintendo Switch ก้มหน้าเศร้า แพ้เกม) | Clean Crop เปลวไฟระเบิดถล่มกำแพงปราสาท และมังกรไฟโจมตี |
| **3** | ชนะรอบแล้วบ่นเหนื่อย | 16:9<br>9:16 | `ชนะรอบแล้วบ่นเหนื่อย-strinova-vdo.jpg`<br>`ชนะรอบแล้วบ่นเหนื่อย-strinova-vdo_9x16.jpg` | **"ชนะแบบหอบ!"** (แดง `#EC1C24`)<br>"เล่นเหนื่อยมาก" (ขาว) | `vts_avatar_05_bust_half_lidded_smirk.png`<br>(ตาหรี่ ยิ้มเหนื่อยหอบ หลังสู้ศึกหนัก) | Clean Crop ป้าย VICTORY เรืองแสงสีแดง พร้อมตัวละครในโถงทางเดิน |
| **4** | ขุดถ้ำเกือบตก | 16:9<br>9:16 | `ขุดถ้ำเกือบตก-Minecraft-vdo.jpg`<br>`ขุดถ้ำเกือบตก-Minecraft-vdo_9x16.jpg` | **"เกือบร่วงเหว!"** (แดง `#EC1C24`)<br>"ใจหายแว้บ?!" (ขาว) | `game_first_livestream_03.png`<br>(ชิบิแตะคาง ตาโตตกใจ มีเครื่องหมาย `?`) | Clean Crop ขอบหน้าผาหิมะยามเย็น และธารลาวาดิ่งลงสู่เหวลึก |
| **5** | ใช้พลังแอดมินโกงเวลา | 16:9<br>9:16 | `ใช้พลังแอดมินโกงเวลา-Minecraft-vdo.jpg`<br>`ใช้พลังแอดมินโกงเวลา-Minecraft-vdo_9x16.jpg` | **"พลังแอดมิน!"** (ทอง `#FFE600`)<br>"แอบเสกของเฉย?!" (ขาว) | `vts_avatar_07_bust_confident_smug.png`<br>(ยิ้มมุมปากมั่นใจ แอบใช้พลังพระเจ้าเสกของ) | Clean Crop ถ้ำหินใต้ดิน คบเพลิง และถังลาวาในมือ |

---

## 2. พารามิเตอร์การจัดวางและกฎเหล็กเฉพาะช่อง Aomi-mama

### ก. การสกัดฉากหลังเกมเพลย์ 100% (Clean Crop Parameters)
- สตรีมของ Aomi จะมีกล้อง Facecam อยู่ที่มุมล่างซ้าย ($x \in [0, 480], y \in [450, 1080]$) และแถบโดเนท/Hotbar ด้านล่าง
- **สูตร Clean Crop (16:9 Native Ratio):**
  - พิกัด Crop: `(540, 0, 1920, 776)` (กว้าง 1380px, สูง 776.25px = สัดส่วน 16:9)
  - Resize ด้วย `LANCZOS` สู่ `(1920, 1080)`
  - ผลลัพธ์: ฉากเกมเพลย์คมชัด **0px blur 100%** ไร้ Facecam, ไร้แชต, ไร้แถบเงินโดเนท และไร้ Hotbar หมดปัญหาตัวละครซ้อน

### ข. ปกแนวนอน (16:9, 1920×1080)
- **Gradient Backdrop:** ด้านซ้ายเกลี่ยดำ `fade_start_x=100`, `fade_end_x=1150`, `max_alpha=0.68`
- **Avatar Zone:** ฝั่งขวา (`av_h = 960–980px`), หักหลบ Timestamp ขวาล่าง
  - **การยึดฐาน:** ฐานตัวละครทะลุขอบล่าง `target_bottom = 1115px`
  - **5-Layer Separation:** เส้นขอบขาว White Rim Light ($12\text{px}$) + Soft Drop Shadow (Offset $(10, 14)$, Blur $16$, Opacity $0.7$)
- **ตัวอักษรไทย (Typography):**
  - พิกัดเริ่มต้น: `(90, 360)` ด้วย `anchor="ls"` (Left-baseline) ห้ามใช้ `anchor="ms"` ใน 16:9
  - Hook หลัก (แดง `#EC1C24` หรือทอง `#FFE600`): ขนาด $150–165\text{px}$, เส้นขอบดำหนา $8\%$
  - ข้อความรอง (ขาว `#FFFFFF`): ขนาด $85–100\text{px}$, เส้นขอบดำ $8\%$

### ค. ปกแนวตั้ง (9:16 Shorts, 1080×1920)
- **Shorts 3-Tier Architecture:**
  1. **Tier 1 (Ambient Background):** ขยายฟุตเทจเต็ม 1080×1920 + Gaussian Blur ($36\text{px}$) + Darken ($0.50$) + Saturate ($1.15$)
  2. **Tier 2 (Center Gameplay Panel):** ขนาด $1080 \times 612\text{px}$ วางที่ $y = 590\text{px}$ ซูมเจาะไฮไลต์เกมเพลย์ ขนาบด้วยเส้นขาวขอบบน-ล่าง $4\text{px}$
  3. **Tier 3 (Large Centered Avatar):**
     - **กึ่งกลางจอเป๊ะ:** $x = (1080 - \text{width}) // 2$ (แกนกลางใบหน้าอยู่ที่ $x = 540\text{px}$)
     - **สเกลใหญ่เด่น:** ความสูง $1260–1280\text{px}$
     - **ยึดฐานขอบล่างแน่น:** ทะลุขอบล่างที่ `target_bottom = 1960px` (จมขอบล่าง 40px) ไม่ลอยเคว้ง
- **ข้อความ Top Safe Zone:**
  - วางกึ่งกลางจอที่ $x = 540\text{px}$ ด้วย `anchor="ms"` (Middle-baseline)
  - Hook หลักที่ $y = 350\text{px}$
  - ข้อความรองที่ $y \approx 530–550\text{px}$

---

## 3. กฎเหล็กการส่งมอบ (Channel Handover Protocol)
1. โฟลเดอร์ `outputs/aomi/` เก็บเฉพาะไฟล์รูปภาพ `.jpg`, `.png` เท่านั้น
2. รัน `python -m cli.verify` ตรวจขนาด $\le 2\text{MB}$, สัดส่วนตรง, และตรงกับ `delivery-manifest.json`
3. รัน `python -m cli.package` สร้างไฟล์ ZIP สำหรับส่งมอบ
4. ซิงก์โฟลเดอร์ `_LATEST` และเปิดโฟลเดอร์ด้วย `python -m cli.open aomi`
5. จบด้วยลิงก์ที่คลิกได้เสมอ: `[เปิดโฟลเดอร์ภาพปกทั้งหมด](file:///C:/Users/warit/Desktop/agent-thumbnail/outputs/aomi/_LATEST)`
