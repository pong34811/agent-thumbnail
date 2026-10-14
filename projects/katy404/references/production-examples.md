# คู่มือและตัวอย่างมาตรฐานภาพปก Katy404 (Production Examples & Style Reference)

เอกสารบันทึกมาตรฐานการออกแบบ จัดวาง และเรนเดอร์ภาพปก YouTube ของช่อง **Katy404** ทั้งขนาด 16:9 (1920×1080) และ 9:16 Shorts (1080×1920) ตามเกณฑ์ Golden Pipeline

---

## 1. ผลงานตัวอย่างที่ผ่านเกณฑ์มาตรฐาน (Golden Pipeline Examples)

| ลำดับ | ตอน / เนื้อเรื่อง | สัดส่วน | ไฟล์ผลลัพธ์ใน `outputs/katy404/_LATEST/` | The 1-2 Punch (Hook / Secondary) | โมเดลสีหน้า (Avatar Expression) | ฉากหลังเกม (Clean Gameplay) |
|---|---|---|---|---|---|---|
| **1** | ครีปเปอร์ระเบิดข้างกรง แต่กรงยังรอด | 16:9<br>9:16 | `ครีปเปอร์ระเบิดข้างกรง แต่กรงยังรอด_Minecraft-vdo.jpg`<br>`ครีปเปอร์ระเบิดข้างกรง แต่กรงยังรอด_Minecraft-vdo_9x16.jpg` | **"ครีปเปอร์ระเบิด!"** (แดง)<br>"กรงยังรอดได้ไง?" (ขาว) | `katy404_avatar_wide-eyes-open-mouth_question-mark-front_048.png`<br>(ตาโตอ้าปากตกใจสุดขีด มี `?`) | Clean Crop ซูมกรงสปอว์นเนอร์มอนสเตอร์ตรงกลาง ไร้ Facecam/Hotbar |
| **2** | ขุดมั่วเจอเหล็กกองใหญ่ | 16:9<br>9:16 | `ขุดมั่วเจอเหล็กกองใหญ่_Minecraft-vdo.jpg`<br>`ขุดมั่วเจอเหล็กกองใหญ่_Minecraft-vdo_9x16.jpg` | **"ขุดมั่วเจอเหล็ก!"** (แดง)<br>"กองเบ้อเริ่ม?!" (ขาว) | `katy404_avatar-mic_wide-eyes-open-mouth_money-symbols-front_028.png`<br>(ตาประกายสัญลักษณ์เงินเยน/ดอลลาร์ ถือไมค์ดีใจ) | Clean Crop ถ้ำหิน แร่เหล็ก คบเพลิง ธารลาวา |
| **3** | ลืมเสบียง จนต้องกินเนื้อซอมบี้ | 16:9<br>9:16 | `ลืมเสบียง จนต้องกินเนื้อซอมบี้_Minecraft-vdo.jpg`<br>`ลืมเสบียง จนต้องกินเนื้อซอมบี้_Minecraft-vdo_9x16.jpg` | **"ลืมเสบียง?!"** (แดง)<br>"ต้องกินเนื้อซอมบี้" (ขาว) | `katy404_avatar_pout_question-mark-front_050.png`<br>(หน้าบึ้ง ปากคว่ำ สับสน กลืนไม่เข้าคายไม่ออก) | Clean Crop เหมืองลึกมืดๆ บรรยากาศเอาตัวรอดกดดัน |
| **4** | ปราบมูนลอร์ดได้ครั้งแรก | 16:9<br>9:16 | `ปราบมูนลอร์ดได้ครั้งแรก_Terraria-vdo.jpg`<br>`ปราบมูนลอร์ดได้ครั้งแรก_Terraria-vdo_9x16.jpg` | **"มูนลอร์ดล้ม!"** (แดง)<br>"ครั้งแรกในชีวิต?!" (ขาว) | `katy404_avatar-mic_squeezed-eyes-laugh_front_026.png`<br>(หลับตาหัวเราะสะใจสุดพลัง ถือไมค์ร้องเย่!) | Clean Crop บอสใหญ่ Moon Lord กึ่งกลางจอ พร้อมเอฟเฟกต์แสงเรือง |

---

## 2. พารามิเตอร์การจัดวาง (Geometric & Visual Parameters)

### ก. ปกแนวนอน (16:9, 1920×1080)
- **ฉากหลังเกม:** 0px blur เสมอ เจาะ Clean Crop เฉพาะโซนเกมเพลย์เพื่อตัด Facecam สตรีมสด และ Hotbar ออก ป้องกันตัวละครซ้อน
- **Gradient Backdrop:** ด้านซ้ายเกลี่ยดำ `fade_start_x=100`, `fade_end_x=1150`, `max_alpha=0.68` เพื่อรองรับการอ่านข้อความ
- **การจัดวางตัวละคร (Avatar Zone):**
  - ฝั่งขวา สัดส่วนกว้าง 35–45% ของเฟรม (`h ≈ 980–1020px`)
  - หลบ Timestamp มุมขวาล่าง ($1580 \le x \le 1900$, $980 \le y \le 1060$)
  - **การยึดฐาน (Anchoring):** ฐานเสื้อยืดออกนอกกรอบขอบล่าง ($y \approx 1115\text{px}$) ป้องกันเส้นขอบขาวลอย
  - **5-Layer Separation:** เส้นขอบขาว White Rim Light ($12\text{px}$) + Soft Drop Shadow (Offset $(10, 14)$, Blur $16$, Opacity $0.7$)
- **ตัวอักษรไทย (Typography):**
  - พิกัดเริ่มต้น: `(90, 360)` ด้วย `anchor="ls"` (Left-baseline)
  - **Hook หลัก (แดง `#EC1C24`):** ฟอนต์ Mitr Bold ขนาด $160–165\text{px}$, เส้นขอบดำหนา $8\%$
  - **ข้อความรอง (ขาว `#FFFFFF`):** ขนาด $95–100\text{px}$, เส้นขอบดำ $8\%$, ห่างจากบรรทัดแรก $y + \text{fontSize} \times 1.18 + 25\text{px}$

### ข. ปกแนวตั้ง (9:16 Shorts, 1080×1920)
- **Shorts 3-Tier Architecture:**
  1. **Tier 1 (Ambient Background):** ขยายฟุตเทจเต็ม 1080×1920 + Gaussian Blur ($28\text{px}$) + Darken ($0.55$) + Saturate ($1.2$)
  2. **Tier 2 (Center Gameplay Panel):** ขนาด $1080 \times 612\text{px}$ วางที่ $y = 590\text{px}$ ซูมเจาะไฮไลต์เกมเพลย์ ขนาบด้วยเส้นขาวขอบบน-ล่าง $4\text{px}$
  3. **Tier 3 (Large Centered Avatar):** 
     - **กึ่งกลางจอเป๊ะ:** $x = (1080 - \text{width}) // 2$ (หรือจุดกึ่งกลางใบหน้าอยู่ที่ $x = 540\text{px}$)
     - **ขนาดใหญ่เด่น:** ความสูง $1280–1300\text{px}$
     - **ยึดฐานขอบล่างแน่น:** ชายเสื้อยื่นทะลุขอบล่างที่ $y = 1960\text{px}$ (เกินขอบล่าง $1920\text{px}$) หมดปัญหาตัวลอย
- **ข้อความ Top Safe Zone:**
  - วางกึ่งกลางจอที่ $x = 540\text{px}$ ด้วย `anchor="ms"` (Middle-baseline)
  - Hook หลักที่ $y = 350\text{px}$ (แดง `#EC1C24`, Mitr Bold $150–152\text{px}$, ขอบดำ $8\%$)
  - ข้อความรองที่ $y \approx 540\text{px}$ (ขาว `#FFFFFF`, Mitr Bold $85–88\text{px}$, ขอบดำ $8\%$)

---

## 3. กฎเหล็กการส่งมอบ (Channel Handover Protocol)
1. โฟลเดอร์ `outputs/katy404/` เก็บเฉพาะไฟล์รูปภาพ `.jpg`, `.png` เท่านั้น
2. รัน `python -m cli.verify` ตรวจขนาด $\le 2\text{MB}$, สัดส่วนตรง, และตรงกับ `delivery-manifest.json`
3. รัน `python -m cli.package` สร้างไฟล์ ZIP สำหรับส่งมอบ
4. ซิงก์โฟลเดอร์ `_LATEST` และเปิดโฟลเดอร์ด้วย `python -m cli.open katy404`
5. จบด้วยลิงก์ที่คลิกได้เสมอ: `[เปิดโฟลเดอร์ภาพปกทั้งหมด](file:///C:/Users/warit/Desktop/agent-thumbnail/outputs/katy404/_LATEST)`
