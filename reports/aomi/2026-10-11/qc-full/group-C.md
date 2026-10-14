# QC group C — Aomi-mama 2026-10-11 (14 covers, read-only)

Method: vtuber-thumbnail-qc `qc_previews.py` (out: `AppData/Local/hermes/cache/scratch/qc-C`) + `vision_analyze` on every full-size landscape and 9x16 cover, plus mobile (10%/20%) contact sheets for both orientations. Thai text zoom was done on the full-size reads. Safe-zone / edge claims are vision estimates; I checked a few with numpy pixel scans (below). Scores are vision-based /100 and approximate. The first vision pass on 9x16 #21, #23 and #26 returned an unreliable "100/100", so I discarded it and re-ran those with a stricter prompt.

## Summary table
| id | game | landscape | shorts | worst | top fix |
|---|---|---|---|---|---|
| 20 | LoL | 86 | 78 | IMPORTANT | Frame is a quiet 03:28 scene with no fight (evidence is "game voice only"). Use a frame with champions clashing, or verify the clip. |
| 21 | LoL | 72 | 68 | IMPORTANT | Title-only: no double-kill or death is visible. Verify "ดับเบิลคิล" in the clip (src 4570s). Otherwise swap to a frame with a kill banner or grey death screen. |
| 22 | LoL | 82 | 78 | OPTIONAL | Avatar is smug while the secondary text says "ตกใจหมด" (shocked). Try a shocked pose. Hook crowds the fight cluster. |
| 23 | LoL | 78 | 68 | IMPORTANT | Frame timer reads 07:22 against hook "ไฟต์ท้ายเกม" (late game). Fix the frame or reword to "ไฟต์กลางเกม". The hook also covers the "ป้อมของพันธมิตรถูกทำลาย!" banner. |
| 25 | MC | 66 | 58 | IMPORTANT | No zombie in frame (empty cave, pickaxe). Pick a frame at subtitle cue 10 or 17 ("ซอมบี้เต็มเลย" / "มันมาได้ไงวะ") that shows zombies. |
| 26 | MC | 83 | 68 | OPTIONAL | Dark scene accepted. Shorts gameplay band is about 70% black and the hook text is small. Lift exposure about 30% on the band. |
| 27 | MC | 76 | 80 | OPTIONAL | No boat in frame, but the question hook tolerates it. White secondary text sits on white snow and is weak on mobile. Thicken the black stroke. |
| 28 | MC | 72 | 66 | OPTIONAL | No mob or house visible and the footage is muddy. Brighten, or use the frame near cue 0 or 3 showing the village. |
| 29 | MC | 60 | 60 | CRITICAL (until verified) | Title-only hook "ออกไม่ได้เลย!" is not backed by the frame (open water and boat, no emerald, no enclosure). The avatar's smile contradicts it. Verify at src 7350s; if unsupported, change the frame or hook. |
| 30 | LoL | 80 | 68 | IMPORTANT | Title-only: "เลเวลสูงสุด" at 13:40 with 127 CS and a minion skirmish looks implausible. Verify cue 0, or reword to "เลเวลพุ่ง". |
| 31 | LoL | 72 | 66 | IMPORTANT | Title-only: no shutdown banner (only "Unstoppable") and no teamfight. Hook top crowds the "jackkill26 ได้ Unstoppable!" banner. Verify at src 2560s, or move the hook down about 60px. |
| 32 | LoL | 87 | 66 | OPTIONAL | Hook is close to the "Aomi mama ได้ Rampage!" banner. On shorts the chin sits about 110px below y1440 (the largest of the set); raise the avatar. |
| 39 | MC | 72 | 66 | IMPORTANT | Lava is not visible (title partly backed). Use a frame at cue 16 ("อุดลาวาแล้วเหรอ") that shows orange lava. |
| 41 | MC (talk) | 86 | 58 | OPTIONAL | Talk clip, blur is by design. Shorts: mouth and chin about 120px below y1440, and the middle of the cover (y520–1060) is empty. Raise the avatar and add a small Minecraft cue. |

CRITICAL: 1 (#29, conditional on verification). IMPORTANT: #21, #23, #25, #30, #31, #39. The shared Shorts chin-below-y1440 issue is also IMPORTANT on all 14. #20's missing-fight frame is a soft IMPORTANT (table lists it as IMPORTANT).

## Thai spell/tone check (full-size, all 14 × 2)
No misspellings, and no tone marks, vowels or thanthakhat swallowed by the stroke, in any cover. Items read: ไฟต์ใหญ่ / ในอารีนา, ดับเบิลคิล / แล้วโดนฝัง, ไฟต์หน้าป้อม / ตกใจหมด, ไฟต์ท้ายเกม / ไม่ขยับเลย, ซอมบี้มาได้ไง?! / เต็มไปหมด, อยากเปลี่ยนร่าง / เสียงในหัวบ่นไม่หยุด, เรือไปไหน?! / พี่จ๋าช่วยด้วย (จ๋ is small, so check at 100%), วิ่งหนีมอน / มืดแล้วเจอบ้าน, ออกไม่ได้เลย / เจอเอเมอรัลด์แรก, ไฟต์ในเลน / เลเวลสูงสุดแล้ว, โดนชัตดาวน์ / ทีมไฟต์พัง, ตายก่อนเลย / หัวยังไม่ฟู, เกือบจมลาวา / อย่าใส่ร้ายผม, ลืมเปิดเสียง / คุยกับผีมาตั้งนาน.
- OPTIONAL: at 10% mobile size the tone marks blur on every cover. "ฝัง" (#21) can be misread as "ฟัง", and "ฟู" and "ก่อน" (#32) are soft. All of them are fine at 20%.

## Findings across all covers
- **Hook colour/contrast.** Every hook is red with a white inner stroke or a dark outline. All hooks are readable, but red on dark brown, purple or black relies only on the outline (#23, #25, #39, #26 on shorts). OPTIONAL: add a thin gold or white inner stroke, or brighten the red slightly. #32 red-on-brown is accepted per the house note.
- **Avatar cutouts (landscape).** The white sticker outline is clean and has no halo. Vision flagged a "hard vertical edge" near x≈862, y>1000 on the bottom-left of #23, #29, #31, #39 and #41. A pixel scan shows white outline pixels at x=862–865 on rows 1060 and 1079 for #23, #29, #31 and #39 (they share the same pose model), so it may be a natural hair tip. I cannot confirm an artifact. OPTIONAL: inspect that corner at 100% in `avatar_06` and `avatar_07`.
- **Avatar cutouts (shorts).** Vision repeatedly claimed hair cut by vertical lines near x≈37 and x≈1042. A pixel scan of rows 1860–1919 shows the white outline extends to x=23–70 on the left and 996–1057 on the right with irregular ends, not a single straight line, and it is not canvas-clipped. I could not confirm this. OPTIONAL: check the lower corners at 100%.
- **Text vs avatar overlap.** There is none on any cover. On landscape the hook runs close to the avatar's ears on #22, #25 and #31 (visible at mobile size). OPTIONAL: nudge the hook left by 20–40px or shrink it 5%.
- **Shorts safe zone.** No hook text sits in the bottom 25% (y>1440) or the right 15% (x>918); every hook ends at about x≈880–895. The face sits clear of the right 15%, with only hair and outline entering it. IMPORTANT (all 14, layout is shared): the avatar's mouth and chin cross y1440 by about 20–120px (smallest on #20, #21 and #26; largest on #32 and #41, 110–120px). The Shorts caption will cover them. Fix: raise the avatar 60–120px, or scale it down about 8%, per cover. Eyes stay above the line on every cover.
- **Cropped HUD on the shorts gameplay band.** The HUD clock and ping are cut at the right edge on #20–23, #30–32 (LoL), and the FPS counter shows. OPTIONAL: pan the band 40px left or scale up so the timer is fully hidden or fully shown.
- **No menu, black or loading frames.** All 14 frames are live gameplay (or a deliberate blur for #41). #26 and #39 are very dark (accepted).
- **Footage sharpness.** All gameplay is soft and upscaled, with small action in LoL. OPTIONAL: crop the LoL band 1.15× on the action.
- **Shorts secondary line.** At 10% size every secondary line is too small to read (long lines on #26, #29, #41 are worst). OPTIONAL: increase secondary size about 15% or shorten it.
- **Repetition.** Three poses repeat within this group: avatar_06 (#23, #29, #39), avatar_09 (#20, #30), avatar_04 (#22, #25, #32) and avatar_12 (#21, #27). Accepted (13 poses reused).

## Per-id notes (landscape / shorts)
- **#20** LoL 03:28, 8v10, no fight. Hook "ไฟต์ใหญ่" is not shown; evidence is only "enemy slain" game voice, so verify. Landscape 86, shorts 78 (chin about 20px past 1440, cropped HUD).
- **#21** Ekko 36v37, 7/9/15 KDA, 10:54. Story of kill then death rests on text only. Avatar playful (cheerful) mismatches "โดนฝัง". Landscape 72, shorts 68.
- **#22** Howling Abyss ARAM 08:53, fight cluster visible. Cleanest LoL cover. Landscape 82, shorts 78 (FPS counter visible in the band).
- **#23** 07:22, 15v22, turret-destroyed message behind the hook. See table. Landscape 78 (-8 for overlap with the game Thai text), shorts 68.
- **#25** Cave with pickaxe and torch. No zombie. Avatar is smug against a "?!" hook. Landscape 66, shorts 58.
- **#26** Dark cave, lava glow, red mob shape. Good avatar-hook fit (tired smirk). Landscape 83, shorts 68 (black band).
- **#27** Snowy village, bright. Switch pose fits. No boat in frame. Landscape 76, shorts 80 (best Minecraft shorts cover).
- **#28** Dusk snow forest, murky. No mob or house. Landscape 72, shorts 66.
- **#29** Open water, wooden dock, teal block (not an emerald). Landscape 60, shorts 60. Lowest in the set.
- **#30** Minion wave, 0/2/1, 13:40. Landscape 80, shorts 68.
- **#31** Minion wave, "Unstoppable" banner, 1/3/1. Landscape 72, shorts 66.
- **#32** 34:35, Rampage banner and "ตายก่อนเลย" are ironic but may read as contradictory. Landscape 87, shorts 66.
- **#39** Brown/teal blocks, no lava. Landscape 72, shorts 66.
- **#41** Talk clip, blurred amber, no game cue. Switch pose fits the topic. Landscape 86; shorts 58 (face lowest in the set, empty middle).

## Flagged title-only ids: what to verify
- **#29 (ออกไม่ได้เลย):** plausible as a joke title, but the frame shows no enclosure. Watch around src 7350s (2:02:30) for a stuck or emerald moment; subs only back "เอเมอรัลด์แรก" at cue 0.
- **#30 (ไฟต์ในเลน):** plausible. Check "เลเวลสูงสุดแล้ว" is a claim about the streamer's level, not the "max level" the frame implies at 13:40.
- **#31 (โดนชัตดาวน์):** plausible (subs "ตายละ", "หมาไม่โดน"). Confirm a shutdown/gold-bounty announcement near src 2560s.
- **#21 (ดับเบิลคิล):** plausible but "ดับเบิลคิล" is not in subs; confirm a double kill occurs near src 4570s.
- **#20 / #23 / #39:** #20 and #23 have no strong subtitle evidence for fight claims; #39 is partly backed (cue 16 lava). Confirm each at its src time.

## Limits
Pixel positions (chin y, hook x) are vision estimates and varied between passes for the same cover (for example #20 chin ≈ y1490 in one pass). Treat the chin finding as directionally correct on all covers, not as an exact pixel figure. No covers, mapping or sources were modified.
