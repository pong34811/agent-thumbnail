# Design Specification: Modular Architecture Reorganization for Agent-Thumbnail

> **Document:** `docs/superpowers/specs/2026-10-01-modular-reorganization-design.md`  
> **Date:** 2026-10-01  
> **Status:** Approved by User  
> **Target:** Restructure codebase into a clean, modular, maintainable production architecture.

---

## 1. Overview & Objectives

This design reorganizes the `agent-thumbnail` project from a collection of fragmented, machine-specific batch scripts into a clean, modular Python architecture. It eliminates redundancy, standardizes the high-CTR visual engine, decouples project configurations from rendering logic, and removes thousands of untracked foreign files.

### Key Goals:
1. **Clean Workspace:** Remove foreign untracked repositories (`.agents/skills/ECC/` and `.agents/skills/ponytail/`).
2. **Core Reusable Engine (`src/`):** Unify Thai text rendering (Pillow+RAQM), graphic storytelling (hand-drawn circles and anime markers), layout geometry, and compositing into reusable modules.
3. **Decoupled Project Batches (`projects/`):** Move timeline mappings and metadata for Aomi, Tygarina, and Armigon into dedicated project folders.
4. **Standardized CLI (`cli/`):** Provide clean CLI entrypoints for building thumbnails, sampling frames, verifying QC, and packaging deliverables.
5. **Centralized Testing (`tests/`):** Migrate isolated tests from `.work/` to a standard `tests/` directory.
6. **Synchronized Skills:** Maintain `skills/katy404-canva-thumbnails` as the single authoritative source of truth.

---

## 2. Directory Structure

```
agent-thumbnail/
├── src/
│   ├── __init__.py
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── text_thai.py       # Pillow + libraqm Thai text rendering & mark adjustment
│   │   ├── graphics.py        # Hand-drawn red brush loops, anime ! / ?, gradient masks
│   │   ├── layout.py          # 16:9 & 9:16 safe zones, dimensions, coordinate calculations
│   │   └── compositor.py      # Main compositing orchestrator
│   └── resolve/
│       ├── __init__.py
│       ├── audit.py           # DaVinci Resolve timeline metadata extraction
│       └── textplus.py        # Headless .drp Text+ title extraction
│
├── cli/
│   ├── build.py               # Main CLI to build thumbnails per project
│   ├── sample_frames.py       # Extract high-res frames matching subtitle cues
│   ├── verify.py              # Automated QC (dimensions, safe zones, text collision)
│   └── package.py             # Packaging deliverables, manifest, and zip verification
│
├── projects/
│   ├── aomi-debut/
│   │   └── mapping.py         # 8 timelines mapping & cues for Aomi
│   ├── tygarina/
│   │   └── mapping.py         # 6 timelines mapping & cues for Tygarina
│   └── armigon/
│       └── mapping.py         # 16 timelines mapping & cues for Armigon
│
├── tests/
│   ├── test_graphics.py       # Tests for red circles and markers
│   ├── test_layout.py         # Tests for text & avatar positioning
│   └── test_text_thai.py      # Tests for Thai typography rendering
│
├── skills/
│   └── katy404-canva-thumbnails/
│       ├── SKILL.md
│       └── references/
│           ├── vtuber-thumbnail-engagement-guide.md
│           ├── style-guide.md
│           ├── canva-workflow.md
│           ├── jpg-render-notes.md
│           └── previews/
│
├── outputs/                   # Preserved deliverables (Armigon, Tygarina)
├── docs/                      # Specs, implementation plans, architecture
├── requirements.txt           # Python dependencies (Pillow, numpy)
├── AGENTS.md                  # Project rules & conventions
└── IDEA.md                    # Product blueprint & vision
```

---

## 3. Module Specifications

### 3.1 `src/engine/text_thai.py`
- Uses `ImageFont.Layout.RAQM` for Thai glyph shaping.
- Auto-fits font size within bounds with stroke ratio calculation.
- Calculates ink bounding box for tight vertical line stacking (`0.06–0.12 em` spacing).
- Clears overlapping upper marks on tall consonants (`ป, ฝ, ฟ`) and initial vowels (`ไ, ใ, โ`).

### 3.2 `src/engine/graphics.py`
- `draw_hand_drawn_brush_circle(...)`: Organic hand-drawn brush loop with stroke width `10–14 px`, `#EC1C24` red fill, dark backing stroke, and subtle Gaussian glow.
- `draw_anime_marker(...)`: Renders `!` (orange-red) and `?` (cyan) with angle tilt (-10° to 15°) and thick black stroke.
- `create_backdrop_gradient(...)`: Smooth left-side alpha gradient (`0.65` to `0.0`) protecting text legibility without blurring gameplay footage.

### 3.3 `src/engine/layout.py`
- Defines safe coordinates for 16:9 Landscape (`x=80..930`, `y=380..520` for text; `x=950..1850` for avatar; clears bottom-right timestamp `1580..1900, 980..1060`).
- Defines safe coordinates for 9:16 Shorts (horizontal center `x=540`, text top `y=280..650`, avatar bottom `y=1140..1920`, channel grid 4:5 tolerance).

### 3.4 `src/engine/compositor.py`
- Takes background image, avatar image (with alpha preservation), text lines, graphic markers, and orientation.
- Assembles composite with 5-layer character separation (avatar + contour stroke + rim light + drop shadow).

---

## 4. Migration Plan

1. **Step 1: Clean Up Foreign Clutter**
   - Remove `.agents/skills/ECC/` and `.agents/skills/ponytail/`.
   - Ensure `.agents/skills/katy404-canva-thumbnails` is synchronized with `skills/katy404-canva-thumbnails`.
2. **Step 2: Create Core Engine (`src/`)**
   - Implement `text_thai.py`, `graphics.py`, `layout.py`, `compositor.py`.
   - Implement `src/resolve/` modules.
3. **Step 3: Extract Project Configurations (`projects/`)**
   - Extract mappings for Aomi, Tygarina, and Armigon into standardized Python mappings.
4. **Step 4: Create Unified CLI Tools (`cli/`)**
   - Implement `build.py`, `verify.py`, `package.py`, `sample_frames.py`.
5. **Step 5: Migrate Tests (`tests/`)**
   - Move test scripts from `.work/armigon-20260920/` to `tests/`.
6. **Step 6: Update Environment & Documentation**
   - Add `requirements.txt`.
   - Update `AGENTS.md` with new project layout map and conventions.
   - Run tests to verify zero regressions.
