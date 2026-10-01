## What's Changed in v1.1.0

### 🚀 Modular Core Engine (`src/`)
- **`src/engine/text_thai.py`**: Thai typography rendering engine using Pillow + libraqm with complex OpenType layout, Mitr-Bold auto-fitting, ink bounding box line stacking, and collision avoidance for upper marks (`ป, ฝ, ฟ` & `ไ, ใ, โ`).
- **`src/engine/graphics.py`**: Reusable graphic drama accents including hand-drawn red circles (`#EC1C24`), anime emotion badges (`!`/`?`), 0px unblurred gameplay backdrop gradient masks, and 5-layer avatar separation with rim light and drop shadow.
- **`src/engine/layout.py`**: Safe zone coordinates and YouTube UI danger zone offsets (bottom-right timestamp badge, red scrubber, Shorts 4:5 channel grid crop).
- **`src/engine/compositor.py`**: `ThumbnailCompositor` pipeline orchestrating 16:9 Landscape (1920x1080) and 9:16 Shorts (1080x1920) thumbnail generation.
- **`src/resolve/`**: Headless DaVinci Resolve project/timeline scanner (`audit.py`) and `.drp` Text+ subtitle extractor (`textplus.py`).

### 🛠️ Unified CLI Tools (`cli/`)
- **`cli/build.py`**: Batch build thumbnails for configured projects (`python -m cli.build --project <name>`).
- **`cli/verify.py`**: Automated QA verification tool checking dimensions, 2MB file limit, RGB mode, safe margins, and generates downscaled squint-test previews (320x180 / 180x320).
- **`cli/package.py`**: Delivery ZIP packager with automated CRC32 and image decodability verification.
- **`cli/sample_frames.py`**: High-resolution video frame extractor using ffmpeg based on timeline subtitle cues.

### 📁 Decoupled Project Mappings (`projects/`)
- Centralized configuration packages for:
  - `projects/aomi_debut/` (8 timelines, Thai typography)
  - `projects/tygarina/` (6 variety & gaming highlight timelines)
  - `projects/armigon/` (16 gaming timelines, emotion matrix, and accents)

### 🧠 DaVinci Thumbnails Skill (`.agents/skills/davinci-thumbnails/`)
- Unified skill location as Single Source of Truth under `.agents/skills/davinci-thumbnails/`.
- Updated comprehensive strategy guide: `vtuber-thumbnail-engagement-guide.md` covering:
  - Avatar Gaze Cuing, Emotional Exaggeration & Silhouette Separation
  - Thai Hook Hierarchy, Curiosity Gap, and Title-Thumbnail Synergy
  - YouTube UI Safe Zones & Mobile Squint Downscale Testing
  - Storytelling Accents and VTuber Content Archetypes

### 🧪 Automated Quality Assurance (`tests/`)
- Complete pytest unit test suite passing 16/16 tests (`python -m pytest tests/`).
- Standardized `requirements.txt` (`Pillow`, `numpy`, `pytest`).
