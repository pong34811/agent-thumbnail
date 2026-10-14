# Aomi p1 2026-10-11 – fix report

Backup before any change: `C:/Users/warit/AppData/Local/hermes/cache/scratch/aomi-p1-backup-155422/` (outputs + manifest).
Edited: `gen_aomi_p1_mapping.py` (+ regenerated `projects/aomi_p1/mapping.py`), `build_aomi_p1_covers.py` (BOX_OVERRIDE, `frame_abs`), `aomi_p1_extract_frames.py` (`frame_abs`). Full rebuild, 98/98 verify PASS, pytest 36 passed, package + organize run, 13 ids (26 files) re-copied to G:/Thumbnails.
Method: for each id, 6 offsets on a contact sheet (scratch `p1fix/`), vision as hypothesis, then full-size composite check.
Only 13 ids changed pixel-wise (md5 vs backup): 1,11,12,14,15,16,18,25,26,33,38,39,49.

## CRITICAL
- **#11** Old frame (5 of 6 sampled offsets are inventory/chest menus). Clip is indoors; only cold cues are `[-9°C]` readout and a snowy window top-left. Now frame_tl 0 + box (0,0,912,513) so the snowy window is in the crop. No menu/tooltip. Cold cue is subtle (no true blizzard exists in the clip).
- **#14** F3 overlay (server "Alice-Magic (Purpur)", XYZ, CPU/GPU) is on for the WHOLE timeline range (white-pixel scan 0-78s, every 2s). Switched to the F3-free frame at src 3085s (= -150s relative), new optional `frame_abs` field (tests require frame_tl >= 0). Pose 06->01. Result: no F3 text. **No diamond on screen** in any F3-free frame; hook "เจอเพชรแล้ว!" unsupported by pixels (flag added in mapping).
- **#18** Frame 1s (white Explorer) -> 31s (Steam banner, AS2 logo). Box (340,80,1430,693): below username bar, left of avatar. Vision: no username, no Explorer, logo visible.
- **#49** Frame 13s (bare Explorer, black strip) -> 24s (AS2 title menu with logo). Box (600,0,1920,743): right of room panel, above the black fade. Vision: game identity visible, no black strip/room panel.
- **#29** Sampled 6 offsets: villager trading hall/outdoors, no enclosure/stuck/boat-trap moment. Subs ("เอเมอรัลด์แรก" only) do not back "ออกไม่ได้เลย". Not invented: frame left, flag text strengthened to UNVERIFIED. (Timeline name itself is "ออกไม่ได้เลยวะ ฮ่าๆๆ", so hook follows it; consider retitle/manual check.)

## IMPORTANT frame swaps
- #1 frame 48->18 (fight visible, no MISSION COMPLETE banner; banner appears from ~26s).
- #12 -> 38s (bright snowy gameplay). **No lava anywhere in clip** (dense orange scan; the lava is a held bucket). Hook "ลาวาร่วง!" stays unsupported; flag added.
- #39 -> 13s + box (0,0,912,513): lava block top-left now visible.
- #25 -> 5s (brightest). **No zombie in any frame** (checked 1..63s + teal scan); flag added.
- #15 -> 80s (crafting table/furnace/lava lake, brighter). #26 -> 14s (lava-lit, brightest). #16 -> 11s (kill + lit doorway; still dark, HUD top clip remains: left, noted).
- #33 -> 58s (first actual skirmish, health 366/650). Clip is 60s; fight only starts at ~56s.

## Shorts avatar placement (engine untouched)
Measured: avatar H=860 flush bottom, top y=1056. Chin 45-110 px and mouth 15-50 px below y1440 on 5 covers (13,32,41,20,16); eyes above. Real, but chin sits at ~53% of avatar height, so with flush-bottom placement only a larger avatar (H>=~1020, +19%) raises it, which would clip the sides more. Not a small safe parameter change -> left, needs a design decision.
Hair "straight vertical edge": source PNGs have no straight clip (side columns ≤35 px). Only canvas-clipping seen: pose 02 (x -34..1137) and 11 (-7..1106); poses 06/07/08 spill 5-6 px. Blunt hair tips of ~60 px at the extremes are model art, not an engine clip. Because of that I did NOT use pose 02 for #38.

## Repetition
Applied: #14 06->01 (breaks 14+39 same-source pair), #38 09->01 (breaks 1+38; group-D proposed 02 but 02 is wider than the Shorts canvas). Skipped (emotion mismatch): #22->07 (smug vs "ตกใจหมด"), #37->12, #13/#32->02/01.

## Not fixed / left
Hook-vs-pixel gaps (#12 lava, #14 diamond, #25 zombie, #29 stuck) are footage limitations; #16 dark + HUD top clip; #11 cold cue subtle; Shorts chin-below-1440; items not in scope (#36 username, #44/#45/#46, LoL title-only checks, #23 timer).
