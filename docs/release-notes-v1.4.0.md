# v1.4.0: KATY404 Shorts v2 & Delivery Set

## What's Changed

### 🎬 KATY404 Shorts v2 (30 vertical covers, 2026-09-29)
- New layout: crisp unblurred gameplay window (downscaled, no 2× upscale), large uniform red hook (132px) + white secondary line above it, half-body avatar centred with the torso bleeding off the bottom edge.
- Fixes in the old set: pixelated upscaled background, small hooks colliding with in-game text, floating avatar.
- `cli.verify` PASS 30/30 · `cli.package` VERIFIED_PASS · visual QC found no 🔴 critical issues. Known 🟠/🟡 notes: avatar head covers ~half of the gameplay window, mouth sits below y1440, repeated avatar poses.

### 🧩 Engine
- `src/engine/shorts_titles.py` + `tests/test_shorts_titles.py`: canonical title from timeline name, one-line-per-colour validation (red + white must concatenate to the title), single-line size fitting. Test suite: 26 passed.

### 🧠 Skill: `davinci-thumbnails` (v1.2.0)
- New example `references/examples/katy404-shorts-v2.md` with layout recipe, lessons learned, 6 sample previews and `scripts/katy404_render_shorts_v2.py` (default data path is repo-relative).
- `AGENTS.md` repo map updated.

### 📦 Delivery files (`outputs/2026-10-04/Katy404-2026-09-29/`)
- 60 original covers (`jpg/`) + 30 Shorts v2 (`jpg-shorts-v2/`), both manifests, both ZIPs, selection/audit/geometry reports, QC reports, `render_covers.py` (repo-root path fixed).
- Not included (local only): evidence frames, QC preview PNGs, runtime DLLs, `.work/aomi-noblur`.
