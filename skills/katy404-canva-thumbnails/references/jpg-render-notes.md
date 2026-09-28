# บันทึกการทำปกเป็น JPG นอก Canva (Technical Render Notes)

บทเรียนเชิงเทคนิคจากการผลิตงานจริงสองโปรเจกต์:
1. `outputs/aomi-debut-20260731` (AOMI-MAMA Debut: 8 Timelines × แนวนอน + Shorts)
2. `outputs/tygarina-20260801` (Tygarina First Pass: 6 Topics / 12 Timelines × แนวนอน + Shorts)

สคริปต์ที่ใช้งานจริงเก็บอยู่ที่ `tools/timeline-covers/build_covers.py` และ `tools/timeline-covers/build_tygarina_covers.py`

---

## 1. การเชื่อมต่อและอ่าน DaVinci Resolve บน Windows

- การรันสคริปต์ Python ภายนอกเข้าหา DaVinci Resolve ที่เปิดอยู่ ต้องตั้ง Environment Variables:
  ```python
  import os, sys
  os.environ['RESOLVE_SCRIPT_API'] = r'C:\Program Files\Blackmagic Design\DaVinci Resolve\Developer\Scripting'
  os.environ['RESOLVE_SCRIPT_LIB'] = r'C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll'
  os.environ['PYTHONPATH'] = r'C:\Program Files\Blackmagic Design\DaVinci Resolve\ResolvePython\lib\modules'
  sys.path.append(r'C:\Program Files\Blackmagic Design\DaVinci Resolve\ResolvePython\lib\modules')
  import DaVinciResolveScript as dvr
  resolve = dvr.scriptapp('Resolve')
  project = resolve.GetProjectManager().GetCurrentProject()
  ```
- **ข้อควรระวัง:** อย่าเปิด Fusion Comp ของ Text+ ผ่าน API ทีละ item ใน Resolve 21.1 เพราะทำให้โปรแกรมค้าง ให้ดึงจากไฟล์สำรอง `.drp` หรือไฟล์ Subtitle `.srt` แทน

---

## 2. การจัดการโมเดลตัวละคร: แปลง "เต็มตัว" เป็น "ครึ่งตัว" (Half-Body)

- **ปัญหา:** ไฟล์โมเดลที่ได้จากศิลปินหรือริกเกอร์มักเป็นภาพทั้งตัว (Full-body 3000×4700px ขึ้นไปถึงปลายเท้า) เมื่อนำมาย่อลงกรอบ 1080p ทั้งตัว หัวจะเหลือเพียง 200–300px ทำให้แววตาและสีหน้ากลืนหายไป
- **วิธีคำนวณการครอปครึ่งตัว (Half-body Crop):**
  1. คำนวณขอบเขตโปร่งใส (Alpha Bounding Box) เพื่อหาตำแหน่งบนสุดของศีรษะ/หู (`top = bbox[1]`)
  2. กำหนดระดับล่างสุดที่ช่วงเอว เข็มขัด หรือสะโพกบน (`bottom = min(img.height, top + 2700)` หรือประมาณ 55–60% ของความสูงทั้งหมด)
  3. ตัดภาพตามกรอบ `(0, top, img.width, bottom)` แล้วคำนวณ Alpha Bounding Box ใหม่อีกครั้ง
- **การปรับขนาดและการวางตำแหน่ง (Landscape):**
  - กำหนดความสูงเป้าหมายของโมเดลที่ 1000–1040px (คิดเป็น ~92–96% ของความสูง 1080p)
  - วางโมเดลชิดขอบล่าง (`my = canvas.height - target_h - pad`) และจัดเยื้องขวา ให้พื้นที่ตัวละครกินประมาณ 45–50% ของความกว้าง

---

## 3. การทำความสะอาดเม็ดพิกเซลลอย (Stray Pixel Cleaning)

- **ปัญหา:** ไฟล์ PNG มักมีพิกเซลโปร่งแสงเดี่ยวๆ ลอยอยู่ในอากาศ (เช่น ที่มุมบนขวาหรือนอกกรอบเส้นผม) เมื่อรันฟิลเตอร์ขยายขอบ (MaxFilter Dilation) ตัวกรองจะสร้างเส้นขอบขาวและเงาขนาดใหญ่ลอยอยู่กลางอากาศ
- **วิธีแก้ไข:**
  - ตรวจสอบพิกเซลในช่อง Alpha ของภาพต้นฉบับก่อนทำขอบขาว
  - ล้างพิกเซลลอยในโซนว่าง เช่น:
    ```python
    a = np.array(img.getchannel("A"))
    # ตัดพิกเซลหลงเหลือที่พิกัดลอย
    a[600:720, 3050:3200] = 0
    img.putalpha(Image.fromarray(a))
    ```

---

## 4. เทคนิคการทำเส้นขอบขาวและเงานุ่ม (High Contrast Outline & Drop Shadow)

- ต้องเผื่อ Padding รอบตัวภาพก่อน (`pad = width + 50`) เพื่อไม่ให้รัศมีของเงาเบลอถูกตัดเป็นเส้นตรงที่ขอบภาพ
- ลำดับเลเยอร์จากหลังมาหน้า:
  1. **เงาดำนุ่ม (Drop Shadow):** ขยายจาก Alpha ด้วย MaxFilter + GaussianBlur(20) ความทึบ 65–70%
  2. **ขอบขาวคมชัด (White Outline):** ขยายจาก Alpha ด้วย MaxFilter (ความหนา 12–16px) + Threshold ให้ขอบคมกริบ
  3. **ภาพโมเดลตัวละครต้นฉบับ:** วางทับด้านบนสุด

---

## 5. การจัดการพื้นหลังและเกรเดียนท์มืด (Background Gradient Shading)

- ดึงเฟรมจากวิดีโอคลิปต้นทางด้วย FFmpeg (`-ss <timestamp> -vframes 1 -q:v 2`)
- เบลอฉากหลังด้วย `ImageFilter.GaussianBlur(36)` และลดแสง `ImageEnhance.Brightness(0.40)`
- **แนวนอน (16:9):** ใส่ Dark Gradient Layer ในแนวนอน:
  - ฝั่งซ้าย (x=0 ถึง x=1150) ให้มืดทึบ (Alpha 180–200) เพื่อเป็นผืนหลังให้ข้อความสีขาวและแดงลอยเด่น
  - ฝั่งขวา (บริเวณตัวละคร) ปล่อยให้แสงสว่างและสีสันของฉากหลังขับตัวละคร
- **แนวตั้ง (9:16 Shorts):** ใส่ Dark Gradient Layer ในแนวตั้ง:
  - ด้านบน (y=0 ถึง y=700) ให้มืดทึบ เพื่อรองรับข้อความ Hook ที่อยู่ช่วง 1/3 บน

---

## 6. ข้อกำหนดฟอนต์และตัวอักษรไทย (Thai Typography Rules)

- ฟอนต์หลัก: **`Mitr-Bold.ttf`**
- ขนาดข้อความบน 1080p:
  - Hook หลัก (สีแดง `#EC1C24`): ขนาด 130–145px, Stroke สีดำ 16–18px, Shadow ชดเชย (8, 11) เบลอ 8px
  - ข้อความรอง (สีขาว `#FFFFFF`): ขนาด 76–84px, Stroke สีดำ 10–12px, Shadow ชดเชย (8, 11) เบลอ 8px
- กรณีใช้งาน Pillow โดยไม่มี libraqm: ให้ตรวจสอบระยะห่างระหว่างวรรณยุกต์กับสระ และตัดบรรทัดตามกลุ่มคำภาษาไทย (Word Wrap / Phrase Breaking) เพื่อไม่ให้คำขาดกลางพยางค์
