# Design Specification: Armigon Thumbnail Enhancements (Batch 2026-09-20)

> **Document:** `docs/superpowers/specs/2026-09-28-armigon-thumbnail-enhancements-design.md`  
> **Date:** 2026-09-28  
> **Status:** Approved by User  
> **Target Directory:** `D:\agent-thumbnail\outputs\armigon-20260920-final-20260928\jpg`  

---

## 1. Overview & Objectives

This design elevates the 32 YouTube thumbnails (16 Landscape 1920×1080 and 16 Shorts 1080×1920) of VTuber character **Armigon** from a uniform, bottom-heavy template into dynamic, high-CTR thumbnails matching the proven standards of KATY404 clips and top-viewed Thai VTuber gaming highlights.

### Core Goals:
1. **Optimize Layout & Hierarchy:** Relocate text from the bottom-left corner (`y=700..885`) to the vertical center-left zone (`y=380..520`), expanding Hook size by 10–15% for immediate readability on mobile feed previews (320×180).
2. **Graphic Storytelling:** Introduce organic hand-drawn red focus circles (`#EC1C24`) on in-game incident focal points and anime-style emotional reaction markers (`!` and `?`) near the avatar's head.
3. **Diverse Avatar Expressions:** Map the 16 unique storylines across all 6 high-resolution avatar expressions (`cry`, `angry`, `hello`, `great`, `sadistic`, `adore`) rather than repeating the same 2 poses.
4. **Preserve High-Clarity Footage:** Keep background blur at `0 px` (unblurred) with `0.90` brightness, paired with an adjusted smooth gradient mask on the left half to guarantee 100% text legibility.

---

## 2. Layout & Typography Specification

### 2.1 Landscape (1920×1080)
- **Safe Zone & Placement:**
  - Left Margin: `80 px`
  - Text Width Limit: `850 px` (stops at least `40 px` before the avatar's outline at `x ≈ 980`)
  - Vertical Placement: Vertically centered in the upper-mid area (`y_center ≈ 460 px`), leaving the bottom-left free from clutter and safely clear of YouTube's timeline hover bar.
- **Hook Text (Mitr Bold):**
  - Font Size: Dynamic auto-fit starting at `165 px` down to `130 px`
  - Color: Red (`#EC1C24` / `RGB(236, 28, 36)`)
  - Stroke: Black (`#000000`), `12 px` width with soft drop shadow (`dx=6, dy=9, blur=7, alpha=0.8`)
- **Secondary Text (Mitr Bold):**
  - Font Size: Dynamic auto-fit starting at `100 px` down to `75 px`
  - Color: White (`#FFFFFF`)
  - Stroke: Black (`#000000`), `8 px` width
  - Spacing: `0.12 em` below Hook block
- **Backdrop Gradient Mask:**
  - Smooth vertical/horizontal gradient covering `x=0..950` with alpha tapering from `0.65` on the far left to `0.0` at `x=980`, ensuring zero contrast competition from sharp game background details.

### 2.2 Shorts / Portrait (1080×1920)
- **Text Zone (Top Half):**
  - Centered horizontally (`x = 540 px`)
  - Vertical bounds: `y = 280..580 px`
  - Max text width: `940 px`
  - Hook font size starting at `150 px` down to `110 px`
- **Avatar Zone (Bottom Half):**
  - Centered horizontally (`x = 540 px`), anchored to the bottom edge (`y_anchor = 1140..1920 px`)
  - Scaled to fit `max_w = 920 px, max_h = 800 px`

---

## 3. Graphic Storytelling Elements

### 3.1 Hand-Drawn Red Focus Circle (KATY404 Style)
- **Visual Style:** Organic, hand-drawn brush loop with slightly tapered overlap ends, stroke width `10–14 px`, color `#EC1C24` with subtle outer glow.
- **Placement Rules:** Applied exclusively to key incident timelines where an in-game subject drives the comedy or drama:
  1. **01-01 Peak:** Centered on teammate Hoshi / the rescue spot (`center=(520, 360), r=110`)
  2. **03-01 Starbound:** Centered on the defeated boss in snow (`center=(910, 290), r=120`)
  3. **04-01 MC RPG:** Centered on the inventory character model / punishment item (`center=(700, 350), r=130`)
  4. **06-01 Mecha Chameleon:** Centered on the disguised player behind signs (`center=(840, 350), r=115`)
  5. **06-02 Mecha Chameleon:** Centered on the green box hiding spot on ceiling (`center=(640, 600), r=120`)
  6. **07-01 Palworld:** Centered on the glitchy wooden stairs placing preview (`center=(870, 360), r=125`)
  7. **08-01 MC เลือดเดียวกัน:** Centered on the mysterious giant pit entrance (`center=(620, 520), r=135`)
  8. **09-01 Backrooms:** Centered on the eerie corridor silhouette (`center=(850, 480), r=110`)

### 3.2 Emotional Reaction Markers (`!` & `?`)
- **Visual Style:** Manga-style cartoon markers, bold black outline (`8 px`), dropped shadow, angled `10°–15°`.
  - **`!` (Exclamation):** Red-orange gradient fill (`#FF2E2E` to `#FF8A00`), paired with high-energy/panic/attack/shock moments.
  - **`?` (Question):** Cyan-blue to white fill (`#00E5FF` to `#FFFFFF`), paired with confusion/glitch/baffled moments.
- **Anchor Point:** Positioned near Armigon’s hat/ear (`x ≈ 1120–1220, y ≈ 220–320` in Landscape; beside head in Shorts), never overlapping the facial features or main text.

---

## 4. Avatar Expression Matrix (16 Timelines)

All 6 avatar assets located at `I:\My Drive\Dreamlight_projects\GEN-Sercet\armigon\` are utilized:

| Index | Timeline Name | Hook Text | Avatar Asset | Rationale |
|:---:|---|---|:---:|---|
| **01** | `01-01 Peak` | ใครก็ได้ แบกโฮชิหน่อย | `cry.png` | Panicking, crying for help to carry knocked teammate |
| **02** | `02-01 Linxicon` | เชื่อมไส้ติ่งด้วย | `hello.png` | Absurd meme word connection, lighthearted sweatdrop |
| **03** | `02-02 Linxicon` | ฉันสามารถนะ | `angry.png` | Rage/frustration at petty grudge loop |
| **04** | `03-01 Starbound` | บอสแพ้ก่อน | `cry.png` | Disappointed weeping that boss died before gun testing |
| **05** | `03-02 Starbound` | ชิ้นใหญ่เท่าควาย | `great.png` | Thumbs-up pride, successfully wired massive mechanism |
| **06** | `04-01 MC RPG 005` | กลับมารับโทษ! | `sadistic.png` | Holding bloody knife, hunting down runner to punish them |
| **07** | `05-01 Roblox วันเกิด` | ยิงหัวแดง | `cry.png` | Horror game panic, crying while being hunted |
| **08** | `05-02 Roblox วันเกิด` | พี่เลน! | `adore.png` | Birthday special, hugging heart, sweet character pick |
| **09** | `06-01 Mecha Chameleon`| ไม่เห็นจริงอะ | `great.png` | Smug victory, successfully hid in plain sight |
| **10** | `06-02 Mecha Chameleon`| ทำไมมาแอบอยู่ หลังกล่อง | `angry.png` | Indignant rage at being discovered on ceiling |
| **11** | `07-01 Palworld` | มันติดตัว | `hello.png` | Hilarious glitch, waving helplessly with stuck stairs |
| **12** | `08-01 MC เลือดเดียวกัน` | ผีหาย! | `angry.png` | Tense, suspicious scouting of mystery hole & ghost |
| **13** | `08-02 MC เลือดเดียวกัน` | ห้องน้ำนี้ ห้ามเข้า | `sadistic.png` | Evil grin with knife, claiming bathroom while host sleeps |
| **14** | `09-01 Backrooms` | อะไร อะไร ถอย! | `cry.png` | Pure horror, screaming at entity behind in dark |
| **15** | `10-01 Valorant` | ยังไม่ตาย! | `angry.png` | Clutch combat focus, gritting teeth to rotate site |
| **16** | `10-02 Valorant` | เล่นได้ไม่กี่ตัว | `hello.png` | Self-deprecating laugh about narrow agent pool |

---

## 5. Background & Composition Integrity

1. **Footage Clarity:** `ImageFilter.GaussianBlur(0)` (no blur), retaining full 1080p game scene definition.
2. **Color Enhancement:** `Color = 1.12`, `Contrast = 1.08`, `Brightness = 0.90` (vibrant, natural).
3. **Accent Colored Border:** Rounded rectangle (`radius=22, width=6 px` in Landscape, `5 px` in Shorts) with game-specific palette matching `ACCENTS` table.
4. **Character Silhouette Isolation:** White inner contour (`17 px maxfilter`) + ambient accent halo + subtle directional shadow (`offset=(12, 18), blur=14`) ensuring crisp separation from the sharp background.

---

## 6. Implementation Deliverables

1. **Automation Script:** `D:\agent-thumbnail\.work\armigon-20260920\build_armigon_covers_v3.py`
2. **Re-rendered Images:** 32 JPEG files in `D:\agent-thumbnail\outputs\armigon-20260920-final-20260928\jpg\`
3. **Contact Sheet Previews:**
   - Landscape: `review-landscape.jpg`
   - Shorts: `review-shorts.jpg`
4. **Updated Manifest & Archive:**
   - `delivery-manifest.json` (with updated avatar mappings, text ink bboxes, graphic flags)
   - `Armigon-2026-09-20-32Timelines-20260928.zip` (compressed package for deployment)
