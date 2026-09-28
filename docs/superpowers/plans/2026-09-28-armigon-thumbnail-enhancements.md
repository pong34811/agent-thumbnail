# Armigon Thumbnail Enhancements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Elevate all 32 Armigon YouTube thumbnails (16 Landscape + 16 Shorts) by shifting text to the center-left, adding KATY404-style red focus circles and anime emotion markers, and deploying all 6 avatar expressions across the 16 storylines.

**Architecture:** Python + Pillow rendering pipeline that composites unblurred (0 px) game footage, center-left gradient shading, organic brush-style focus circles, anime emotion badges, diverse avatar expressions with accent outlines, and multi-line Mitr Bold text.

**Tech Stack:** Python 3.12+, Pillow 12+, NumPy, Git.

## Global Constraints
- Target output directory: `D:\agent-thumbnail\outputs\armigon-20260920-final-20260928\jpg\`
- Model assets directory: `I:\My Drive\Dreamlight_projects\GEN-Sercet\armigon\`
- Font file: `D:\agent-thumbnail\outputs\timeline-covers\fonts\Mitr-Bold.ttf`
- Output image specifications: 1920×1080 (Landscape) and 1080×1920 (Shorts), JPEG quality 95, subsampling 0
- Background blur: `0 px` (unblurred), Brightness: `0.90`, Color: `1.12`, Contrast: `1.08`
- Hook text color: `#EC1C24` (Red), Secondary text color: `#FFFFFF` (White), Outline: `#000000` (Black)

---

### Task 1: Graphic Storytelling Renderer Module

**Files:**
- Create: `D:\agent-thumbnail\.work\armigon-20260920\graphics_overlay.py`
- Test: `D:\agent-thumbnail\.work\armigon-20260920\test_graphics_overlay.py`

**Interfaces:**
- Produces:
  - `draw_hand_drawn_circle(canvas: Image.Image, center: tuple[int, int], radius: int, color=(236, 28, 36), stroke_width=12) -> None`
  - `draw_emotion_marker(canvas: Image.Image, marker_type: str, pos: tuple[int, int], size=130, angle=-12) -> None`
- Consumes: Pillow (`Image`, `ImageDraw`, `ImageFilter`, `ImageFont`)

- [ ] **Step 1: Write the failing unit test for graphics overlay**

```python
# D:\agent-thumbnail\.work\armigon-20260920\test_graphics_overlay.py
import pytest
from PIL import Image
from graphics_overlay import draw_hand_drawn_circle, draw_emotion_marker

def test_draw_hand_drawn_circle():
    canvas = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw_hand_drawn_circle(canvas, (500, 400), 120, color=(236, 28, 36), stroke_width=12)
    bbox = canvas.getbbox()
    assert bbox is not None
    # Circle bounds should roughly surround center (500, 400) with r=120
    assert 350 <= bbox[0] <= 400
    assert 250 <= bbox[1] <= 300
    assert 600 <= bbox[2] <= 660
    assert 500 <= bbox[3] <= 560

def test_draw_emotion_marker_exclamation():
    canvas = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw_emotion_marker(canvas, "!", pos=(1150, 250), size=140, angle=-12)
    bbox = canvas.getbbox()
    assert bbox is not None
    assert 1100 <= bbox[0] <= 1200
    assert 200 <= bbox[1] <= 300

def test_draw_emotion_marker_question():
    canvas = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw_emotion_marker(canvas, "?", pos=(1150, 250), size=140, angle=10)
    bbox = canvas.getbbox()
    assert bbox is not None
    assert 1100 <= bbox[0] <= 1200
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest "D:\agent-thumbnail\.work\armigon-20260920\test_graphics_overlay.py" -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'graphics_overlay'`

- [ ] **Step 3: Implement graphics_overlay.py**

```python
# D:\agent-thumbnail\.work\armigon-20260920\graphics_overlay.py
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_PATH = Path(r"D:\agent-thumbnail\outputs\timeline-covers\fonts\Mitr-Bold.ttf")

def draw_hand_drawn_circle(canvas: Image.Image, center: tuple[int, int], radius: int, color=(236, 28, 36), stroke_width=12):
    """Draws an organic, imperfect hand-drawn brush loop with slight ovality and overlap."""
    cx, cy = center
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Generate points along an organic loop that overlaps itself
    points = []
    num_steps = 72
    total_angle = 2 * math.pi + 0.45  # slight overlap at ends
    for i in range(num_steps):
        theta = (i / (num_steps - 1)) * total_angle
        # Organic perturbation
        r_perturb = radius * (1.0 + 0.05 * math.sin(3 * theta) - 0.03 * math.cos(5 * theta))
        # Slight horizontal stretch to emulate quick hand-drawing
        x = cx + r_perturb * 1.08 * math.cos(theta - 0.2)
        y = cy + r_perturb * 0.94 * math.sin(theta - 0.2)
        points.append((x, y))
        
    # Draw thicker black outline for contrast against game backgrounds
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=(0, 0, 0, 220), width=stroke_width + 8)
    # Draw core red brush line
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=(*color, 255), width=stroke_width)
        
    # Soft drop shadow for depth
    shadow = overlay.filter(ImageFilter.GaussianBlur(6))
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(overlay)

def draw_emotion_marker(canvas: Image.Image, marker_type: str, pos: tuple[int, int], size=130, angle=-12):
    """Draws a bold anime-style exclamation '!' or question '?' badge with drop shadow."""
    if not FONT_PATH.exists():
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(str(FONT_PATH), size)
        
    badge_w = size * 2
    badge_h = size * 2
    badge = Image.new("RGBA", (badge_w, badge_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    
    fill_color = (255, 46, 46, 255) if marker_type == "!" else (0, 229, 255, 255)
    center_xy = (badge_w // 2, badge_h // 2)
    
    # Thick black stroke
    draw.text(center_xy, marker_type, font=font, anchor="mm",
              fill=(0, 0, 0, 255), stroke_width=14, stroke_fill=(0, 0, 0, 255))
    # Vibrant fill
    draw.text(center_xy, marker_type, font=font, anchor="mm",
              fill=fill_color, stroke_width=2, stroke_fill=(255, 255, 255, 200))
              
    rotated = badge.rotate(angle, resample=Image.Resampling.BILINEAR, expand=True)
    # Soft drop shadow
    shadow = Image.new("RGBA", rotated.size, (0, 0, 0, 0))
    alpha = rotated.getchannel("A").filter(ImageFilter.GaussianBlur(8))
    shadow.putalpha(alpha.point(lambda p: round(p * 0.6)))
    
    paste_x = pos[0] - rotated.width // 2
    paste_y = pos[1] - rotated.height // 2
    canvas.alpha_composite(shadow, (paste_x + 8, paste_y + 10))
    canvas.alpha_composite(rotated, (paste_x, paste_y))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest "D:\agent-thumbnail\.work\armigon-20260920\test_graphics_overlay.py" -v`
Expected: PASS with 2 passed

- [ ] **Step 5: Commit graphics overlay module**

```bash
git add .work/armigon-20260920/graphics_overlay.py .work/armigon-20260920/test_graphics_overlay.py
git commit -m "feat(thumbnails): add hand-drawn red circle and anime emotion markers module"
```

---

### Task 2: Layout & Typography Upgrade in Generator

**Files:**
- Modify: `D:\agent-thumbnail\.work\armigon-20260920\rebuild_bg_v2.py` -> Create: `D:\agent-thumbnail\.work\armigon-20260920\build_armigon_covers_v3.py`
- Test: `D:\agent-thumbnail\.work\armigon-20260920\test_layout_positioning.py`

**Interfaces:**
- Produces:
  - `draw_text_block(canvas: Image.Image, hook: str, secondary: str, portrait: bool) -> dict` with center-left positioning (`y_center ≈ 460` in Landscape)
  - `add_gradient(canvas: Image.Image, portrait: bool) -> None` with upper-left/center-left coverage
- Consumes: Pillow (`Image`, `ImageDraw`, `ImageFont`)

- [ ] **Step 1: Write test for center-left text positioning**

```python
# D:\agent-thumbnail\.work\armigon-20260920\test_layout_positioning.py
import pytest
from PIL import Image
from build_armigon_covers_v3 import draw_text_block

def test_landscape_text_vertical_centering():
    canvas = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    info = draw_text_block(canvas, "ใครก็ได้ แบกโฮชิหน่อย", "ชุบได้ไหม", portrait=False)
    bbox = canvas.getbbox()
    assert bbox is not None
    # Text must be vertically centered in the upper-mid area (y between 300 and 650)
    # NOT in the old bottom-heavy area (y > 700)
    top_y = bbox[1]
    bottom_y = bbox[3]
    center_y = (top_y + bottom_y) // 2
    assert 380 <= center_y <= 540
    # Left edge must respect margin
    assert 70 <= bbox[0] <= 110
    # Text font size should be large and prominent
    assert info["hook_font"] >= 130
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest "D:\agent-thumbnail\.work\armigon-20260920\test_layout_positioning.py" -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'build_armigon_covers_v3'`

- [ ] **Step 3: Implement build_armigon_covers_v3.py with updated text layout & gradient**

```python
# Implementation incorporates:
# 1. Landscape hook_y=420, sec_y=580 with start font size 165
# 2. Gradient that protects x=0..950 smoothly
# 3. Import and integration with graphics_overlay.py
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest "D:\agent-thumbnail\.work\armigon-20260920\test_layout_positioning.py" -v`
Expected: PASS

- [ ] **Step 5: Commit layout and generator script**

```bash
git add .work/armigon-20260920/build_armigon_covers_v3.py .work/armigon-20260920/test_layout_positioning.py
git commit -m "feat(thumbnails): elevate text layout to center-left and adjust gradient"
```

---

### Task 3: Avatar Expression Matrix & Per-Timeline Storytelling Mapping

**Files:**
- Modify: `D:\agent-thumbnail\.work\armigon-20260920\build_armigon_covers_v3.py`
- Test: `D:\agent-thumbnail\.work\armigon-20260920\test_timeline_mappings.py`

**Interfaces:**
- Produces:
  - `TIMELINE_CONFIG: dict[int, dict]` mapping `timeline_index (1..16)` to:
    - `avatar`: one of `[cry.png, angry.png, hello.png, great.png, sadistic.png, adore.png]`
    - `focus_circle`: `(center_x, center_y, radius)` or `None`
    - `emotion_marker`: `("!" | "?", (x, y))` or `None`

- [ ] **Step 1: Write test verifying complete mapping of all 16 timelines**

```python
# D:\agent-thumbnail\.work\armigon-20260920\test_timeline_mappings.py
from pathlib import Path
from build_armigon_covers_v3 import TIMELINE_CONFIG, AVATAR_DIR

def test_all_16_timelines_configured():
    assert len(TIMELINE_CONFIG) == 16
    for idx in range(1, 17):
        assert idx in TIMELINE_CONFIG
        cfg = TIMELINE_CONFIG[idx]
        avatar_path = AVATAR_DIR / cfg["avatar"]
        assert avatar_path.exists(), f"Missing avatar file: {avatar_path}"
        if cfg.get("focus_circle"):
            cx, cy, r = cfg["focus_circle"]
            assert 0 < cx < 1920 and 0 < cy < 1080 and r > 30
        if cfg.get("emotion_marker"):
            m_type, (mx, my) = cfg["emotion_marker"]
            assert m_type in ["!", "?"]
            assert 0 < mx < 1920 and 0 < my < 1080

def test_avatar_expression_diversity():
    used_avatars = {cfg["avatar"] for cfg in TIMELINE_CONFIG.values()}
    # All 6 avatar expressions must be utilized
    expected = {"cry.png", "angry.png", "hello.png", "great.png", "sadistic.png", "adore.png"}
    assert used_avatars == expected
```

- [ ] **Step 2: Run test to verify failure**

Run: `python -m pytest "D:\agent-thumbnail\.work\armigon-20260920\test_timeline_mappings.py" -v`
Expected: FAIL (missing `TIMELINE_CONFIG`)

- [ ] **Step 3: Define TIMELINE_CONFIG in build_armigon_covers_v3.py**

Populate the exact mapping table defined in Section 3 & 4 of the Design Spec:
- 1: `cry.png`, circle at `(520, 360, 110)`, marker `("!", (1180, 240))`
- 2: `hello.png`, circle `None`, marker `("?", (1180, 240))`
- 3: `angry.png`, circle `None`, marker `("!", (1180, 240))`
- 4: `cry.png`, circle at `(910, 290, 120)`, marker `("!", (1180, 240))`
- 5: `great.png`, circle `None`, marker `None`
- 6: `sadistic.png`, circle at `(700, 350, 130)`, marker `("!", (1180, 240))`
- 7: `cry.png`, circle `None`, marker `("!", (1180, 240))`
- 8: `adore.png`, circle `None`, marker `None`
- 9: `great.png`, circle at `(840, 350, 115)`, marker `("!", (1180, 240))`
- 10: `angry.png`, circle at `(640, 600, 120)`, marker `("!", (1180, 240))`
- 11: `hello.png`, circle at `(870, 360, 125)`, marker `("?", (1180, 240))`
- 12: `angry.png`, circle at `(620, 520, 135)`, marker `("!", (1180, 240))`
- 13: `sadistic.png`, circle `None`, marker `None`
- 14: `cry.png`, circle at `(850, 480, 110)`, marker `("!", (1180, 240))`
- 15: `angry.png`, circle `None`, marker `("!", (1180, 240))`
- 16: `hello.png`, circle `None`, marker `("?", (1180, 240))`

- [ ] **Step 4: Run test to verify passes**

Run: `python -m pytest "D:\agent-thumbnail\.work\armigon-20260920\test_timeline_mappings.py" -v`
Expected: PASS

- [ ] **Step 5: Commit timeline mappings**

```bash
git add .work/armigon-20260920/build_armigon_covers_v3.py .work/armigon-20260920/test_timeline_mappings.py
git commit -m "feat(thumbnails): map 16 timelines to 6 avatar expressions and storytelling graphics"
```

---

### Task 4: Full Rendering Pipeline Execution & Packaging

**Files:**
- Execute: `D:\agent-thumbnail\.work\armigon-20260920\build_armigon_covers_v3.py`
- Modify: `D:\agent-thumbnail\outputs\armigon-20260920-final-20260928\delivery-manifest.json`
- Output: 32 JPG files in `D:\agent-thumbnail\outputs\armigon-20260920-final-20260928\jpg\`
- Contact Sheets: `review-landscape.jpg` and `review-shorts.jpg`
- Archive: `D:\agent-thumbnail\outputs\armigon-20260920-final-20260928\Armigon-2026-09-20-32Timelines-20260928.zip`

- [ ] **Step 1: Execute full 32-cover render pipeline**

Run: `python "D:\agent-thumbnail\.work\armigon-20260920\build_armigon_covers_v3.py"`
Expected: All 32 covers built without errors.

- [ ] **Step 2: Regenerate contact sheet overviews**

Run: Python script generating `review-landscape.jpg` (4x4 grid of 16 landscape covers) and `review-shorts.jpg` (4x4 grid of 16 shorts covers).

- [ ] **Step 3: Update delivery manifest and zip archive**

Run: Python packager updating `delivery-manifest.json` and zipping all 32 JPGs into `Armigon-2026-09-20-32Timelines-20260928.zip`.

- [ ] **Step 4: Visual verification check**

Use `view_file` to inspect `review-landscape.jpg` and `review-shorts.jpg`, plus at least 3 individual high-incident thumbnails (e.g. 01 Peak, 04 MC RPG, 06 Mecha Chameleon) to verify zero text collision, crisp focus circles, and clean avatar outlines.

- [ ] **Step 5: Commit final pipeline changes**

```bash
git add docs/superpowers/plans/2026-09-28-armigon-thumbnail-enhancements.md .work/armigon-20260920/
git commit -m "feat(thumbnails): complete v3 production render of 32 enhanced Armigon covers"
```
