## What's Changed in v1.2.0

### 🔍 New Skill: VTuber Thumbnail QC (`.agents/skills/vtuber-thumbnail-qc/`)
- **`SKILL.md`**: Senior YouTube Thumbnail QC Director workflow for Thai VTuber covers — content match, character/expression, composition, Thai spelling & stacked-mark readability, contrast, color, safe area, curiosity gap, title–thumbnail pairing, clickbait classification, and technical QC.
- **`references/qc-checklist.md`**: 23-step checklist with severity examples (🔴 CRITICAL / 🟠 IMPORTANT / 🟡 OPTIONAL) and 14 QC rules.
- **`templates/qc-report.md`**: Fixed 12-section Thai report with /100 scoring (Character 15 · Expression 10 · Composition 10 · Text 10 · Thai Typography 10 · Contrast 10 · Color 5 · Relevance 10 · Curiosity 10 · Mobile 5 · Brand 5), A/B/C comparison, best-moment picker, and 3-concept redesign block.
- **`scripts/qc_previews.py`**: Generates real test previews instead of imagined ones — mobile 10%/20%, grayscale, squint blur, duration-badge overlay (Shorts: bottom 25% / right 15% danger zones + 4:5 grid crop), feed sheet for A/B/C, and `tech_report.json` (dimensions, ratio, 2MB limit, color mode).

### 🔁 Auto-QC After Every Build
- **`AGENTS.md`**: Pipeline is now build → `cli.verify` → **auto QC every cover** → fix 🔴 CRITICAL and re-run until clean → `cli.package` → deliver with QC report.
- **`.agents/skills/davinci-thumbnails/SKILL.md`**: New mandatory section “QC อัตโนมัติหลังทำปกเสร็จ” — agent runs `vtuber-thumbnail-qc` on its own once all covers are exported; unfixable CRITICAL issues are reported, never marked as passed.

### 🧪 Quality Assurance
- `python -m pytest tests/` — 16/16 passing.
- `qc_previews.py` verified on real Tygarina landscape (1920×1080) and Shorts (1080×1920) outputs.
