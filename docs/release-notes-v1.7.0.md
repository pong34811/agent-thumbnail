# v1.7.0: Golden Pipeline Standardization, Multi-Channel Mappings (Katy404 & Aomi-mama) & QC Engine

## What's Changed

### 🎨 Channel Support & Production Mappings
- **Katy404 (`projects/katy404/`):**
  - Added full project mapping (`projects/katy404/mapping.py`) covering Minecraft and Terraria live gameplay clips.
  - Added comprehensive production reference guide (`projects/katy404/references/production-examples.md`).
  - Added channel configuration and asset hints in `projects/channels.json`.
- **Aomi-mama (`projects/aomi/`):**
  - Added full project mapping (`projects/aomi/mapping.py`) for live streams (Minecraft, Becastled, Strinova).
  - Added production reference guide (`projects/aomi/references/production-examples.md`) with clean crop geometry and avatar separation parameters.
  - Updated channel configuration in `projects/channels.json` and channel profile in `.agents/skills/davinci-thumbnails/references/channel-profiles/aomi-mama.md`.
- **Sakuyako-Cheris (`projects/sakuyako/`):**
  - Added Sakuyako channel profile and asset directory hints.
- **Armigon:**
  - Added portrait layout and reference documentation (`projects/armigon/references/portrait-style-reference.md`).

### 📐 Design & Layout Standards (Golden Pipeline)
- **The 1-2 Punch Typography:**
  - Primary hook: 1–4 words in `#EC1C24` (Red) or `#FFE600` (Radiant Gold) with ~8% black stroke and soft drop shadow.
  - Secondary context: White `#FFFFFF` with ~8% black stroke.
  - Enforced `anchor="ls"` (Left-baseline) for 16:9 Landscape and `anchor="ms"` (Middle-baseline) for 9:16 Shorts.
- **Clean Gameplay Backgrounds (0px Blur Rule):**
  - Strict elimination of stream facecams, donate bars, chat overlays, and hotbars via precision cropping (`(540, 0, 1920, 776)` for Aomi), maintaining 100% crisp gameplay.
  - Backdrop gradient mask for typography legibility.
- **Shorts 3-Tier Architecture:**
  - Tier 1: Ambient background blur (36px, brightness 0.50, color 1.15).
  - Tier 2: Centered 1080×612 gameplay panel with crisp border lines.
  - Tier 3: Large centered avatar ($h \ge 1250\text{px}$, centered at $x = 540$) firmly anchored to the bottom (`target_bottom = 1960px`).
- **Avatar 5-Layer Separation:**
  - White rim light (12–14px) and soft deep drop shadow (`(10, 14)`, blur 16, opacity 0.70).
  - Bleed past bottom canvas to eliminate floating avatar cutoffs.

### 🔍 Automated QC Engine (`vtuber-thumbnail-qc`)
- Integrated automated post-build QC workflow generating:
  - Mobile feed previews (10% and 20% zoom).
  - Grayscale contrast check.
  - Squint test (silhouette and eye flow).
  - YouTube duration badge & Shorts safe zone overlay check.
  - Multi-cover contact feed sheet.
- Added automated QC summary reports in `reports/<channel>/<date>/qc-summary.md`.

### 🛠 Core Engine & Build Tooling
- **`src.engine.text_thai`:**
  - Enforced correct import precedence so `fribidi` runtime initializes before Pillow loads, ensuring `libraqm` is always active.
  - Added support for RGB 3-tuples in text fill color.
- **CLI & Packaging:**
  - `cli.package` and `cli.verify` verified across 100% of newly generated thumbnails.
  - `outputs/<channel>/` strictly constrained to image assets only (`.jpg`, `.png`).
- **Tests:**
  - Pytest test suite expanded and passing 39/39 tests.
