# QC brief: Tygarina 2026-09-30 covers (read-only QC; do NOT build/edit images, mapping, or git)

Repo: C:/Users/warit/Desktop/agent-thumbnail (Windows git-bash; use `py`, not `python`). Write prose in Thai.
Images: outputs/tygarina/2026-09-30/<file> (landscape 1920x1080 and `_9x16` Shorts 1080x1920). Your slice file (JSON list: file, orientation, hook, secondary, evidence, flag, model) names the covers you own.

## Method
1. Load skill `vtuber-thumbnail-qc` (skill_view) and its references/qc-checklist.md for the rubric (severity: CRITICAL / IMPORTANT / OPTIONAL).
2. Run previews for your files in ONE call: `py .agents/skills/davinci-thumbnails/scripts/../../vtuber-thumbnail-qc/scripts/qc_previews.py <files...> --out C:/Users/warit/AppData/Local/hermes/cache/scratch/tygqc_<slice>` (find the script under .agents/skills/vtuber-thumbnail-qc/scripts/). Use native C:/ paths.
3. Use vision_analyze on contact sheets you build with PIL (e.g. 6 landscape per sheet at 640x360, or 6 Shorts per sheet at 270x480) and zoom (region) on any suspect cover at full size. Never judge from filenames.

## What counts as CRITICAL (must be fixed before shipping)
- Thai text cut off / overlapped by avatar / outside frame; wrong or garbled Thai spelling; stroke eating tone marks
- Hook not readable at ~320x180 (landscape) / 180x320 (Shorts), e.g. red text on red/orange area with no contrast
- Avatar cut off oddly, covers face-less, or overlaps the hook; text under the YouTube duration badge zone (bottom-right ~ x>1560,y>940) or Shorts unsafe zone (bottom 25%, right 15%)
- Background wrong: mostly black/empty frame with no scene, loading screen, black bars, a baked-in stream avatar duplicating the big avatar
- Hook claims something the evidence field does not support
- Placeholder boxes or leftover template text anywhere
House rules (AGENTS.md): hook 1-4 words red #EC1C24 (or gold) with thick black stroke; secondary white; avatar right side 35-50% (landscape); Shorts text centered, upper/mid, avatar bottom center.
Do NOT flag as problems: the layout itself (avatar bust at bottom-right, white sticker outline, Shorts middle strip of gameplay over a blurred background), or that only 3 avatar poses exist (known limitation: real emotion PNGs were not available).

## Output
Write reports/tygarina/2026-09-30/qc_part_<N>.md containing:
- A table: file | score /100 (rough) | CRITICAL count | top fix (concrete: verb + number/position or new Thai wording)
- A section "CRITICAL list" with one line per CRITICAL cover: file, issue, concrete fix (for text changes give 3 alternative Thai hooks, 1-4 words, evidence-safe)
- A line "Tool limits:" stating what you could NOT verify.
Final reply (short, Thai): number of covers checked, number with CRITICAL, the file path. Do not paste the table.
