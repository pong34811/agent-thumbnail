# QC full-size — Group B (14 covers x 2 orientations)

Method: `vtuber-thumbnail-qc`. For each cover `qc_previews.py` was run (output: `C:/Users/warit/AppData/Local/hermes/cache/scratch/qc-B`). I then ran `vision_analyze` on every full-size JPG (28 images), on mobile-preview contact sheets (14 landscape, 14 Shorts), and on zoomed crops where a claim needed checking.
Covers, mapping and sources were not modified. Scores are /100 estimates and are secondary to the fix list.
Known accepted issues are not re-reported: hook red on red/brown for #32 and #36; softness on #18/#19/#36; avatar poses reused.

## Summary table

| id | game | landscape | shorts | worst | top fix |
|---|---|---|---|---|---|
| 10 | MC | 82 | 80 | OPTIONAL | Hook is correct ("จอ"), but จ and อ look alike at 10% in Mitr Bold, so two reviews misread it as "ออ". Enlarge the hook ~10% and thin the stroke 1-2px. |
| 11 | MC | 68 | 66 | CRITICAL | The frame is an inventory menu with a "Lava Bucket" tooltip, which contradicts "หนาวตายจริง". Replace it with a snow/blizzard gameplay frame near src 1422s. |
| 12 | MC | 78 | 76 | IMPORTANT | The hook says "ลาวาร่วง" but the frame is a dark snowy cave with no lava. Use a frame with lava, or lift the exposure. |
| 13 | MC | 84 | 82 | OPTIONAL | Shorts: the avatar's chin and mouth sit in the bottom 25%. Raise or shrink the avatar ~100px. |
| 14 | MC | 65 | 63 | CRITICAL | The F3 debug overlay shows server name, XYZ coordinates and CPU/GPU, and the avatar cuts it mid-word. There is also no diamond in frame. Use a frame with F3 hidden and ore visible, or mask the text. |
| 15 | MC | 70 | 68 | IMPORTANT | The frame is almost black and shows no "home" cue. Brighten gamma/shadows 40-60%. On Shorts there is a visible seam at x665/y765 between the inset clip and the blurred fill. |
| 24 | MC | 80 | 77 | OPTIONAL | Zombie and food are not in frame, and the avatar covers the held tool. On Shorts, move line 1 down 40-60px. |
| 16 | AS2 | 76 | 74 | IMPORTANT | The frame is very dark and does not show "2 ways in". The "LOCATE EXPLOSIVES" HUD is clipped at the top edge. Use a brighter frame or crop 20px lower. |
| 17 | AS2 | 80 | 78 | OPTIONAL | Clipped HUD ("GO TO THE ELEVATOR", round icon at top-left) and a black wedge on the right. Crop 30px lower. |
| 18 | AS2 | 62 | 60 | CRITICAL | The frame is a Steam Library desktop with a white Explorer window left at the right edge, which swallows the avatar's white outline. "XP Vista 8" overlaps the game logo. The username is visible. Crop out the Explorer window and blur the username. |
| 19 | AS2 | 70 | 68 | IMPORTANT | The frame is a title/key-art splash, not gameplay or a settings screen. The logo is cropped ("ALIE/SHOOT") and the avatar ear touches it. The subline has no visual support. Pick a gameplay or settings frame. |
| 36 | AS2 | 70 | 68 | IMPORTANT | The frame is the Steam Library page, with a stray cursor and the username "AOMIMAMAGD47" visible, and it does not show a crash. Blur the username, remove the cursor, and tighten the subline/logo gap. |
| 43 | AS2 | 78 | 76 | IMPORTANT | The avatar covers the game dialogue ("QUARTE…"), and the HUD "SECURE SURVIVORS" is clipped on Shorts. The save pad is small. Shift the crop and avatar. The landscape avatar is ~52% wide, so scale it down 5%. |
| 49 | AS2 | 60 | 58 | CRITICAL | The frame is a bare File Explorer file list with no game identity. It has a black strip at the top (~30px) and a scrollbar at the right. Swap in a gameplay or share-screen frame, or re-crop. |

## Cross-cutting findings
- **Avatar cutout (landscape, IMPORTANT, all 14):** at the bottom-left (x≈850-920, y≈1000-1080) the hair and outline end in a straight vertical slice. I confirmed it by zooming on #24. Likely a bbox clip in the shared avatar layer. Extend the layer's left bound or feather it.
- **Avatar cutout (Shorts, OPTIONAL):** hair at the bottom corners ends near x≈22 and x≈1058. The reviewer read it as a vertical cut, but the zoom on #24 did not confirm it.
- **Hook spelling (#10, #49):** two reviews read "จอ" as "ออ". I checked #10's pixels against Mitr-Bold `จ`/`อ` renders: the glyph is `จ` (2.5% mismatch vs 6.7% for `อ`). Spelling is correct and matches `mapping.py`. This is a legibility risk only.
- **Spelling and tone marks:** all other hooks and sublines are correct and no tone mark is swallowed. Riskiest at mobile size: #13 (พี่น้องไม่ช่วย), #15 and #19 (long sublines), #49.
- **Shorts layout:** the game band is 1080x~640, not 608 (1.69:1). Treat it as an intentional layout. The crosshairs and logos look unstretched. The AS2 desktop crops show no leftover small stream avatar.
- **Hook contrast:** red on dark navy/black is OK because of the stroke. White-on-dark sublines are fine. Sublines are the weak link at 10% for #10, #15, #19, #24, #49.
- **Safe zone:** no text sits in the bottom 25% or right 15%. Hook right edges are 30-50px inside the 918px line. Avatar faces sit at or just above y≈1440 on #13, #15, #24 and #16.
- **Feed repetition:** #18 and #36 are near-identical Steam Library layouts in the feed.

## Per-cover notes
- **#10** Blurred background is by design (talk=True). Avatar is ~55% wide, slightly over. Empty bottom-left space.
- **#11** Avatar ~57% wide. Hair clips the tooltip. Subline sits over the search field. Gameplay is darkened. The flag "title -16, subs -12" is followed ("12"); that is fine.
- **#12** The cyan pixel snowflakes at the top right are coarser than the game pixels. The hook is strong. The Shorts band shows frost, which suits "หนาว".
- **#13** Passes. The avatar is ~46%. The softness is mild. Lava on the Shorts band causes a slight orange glow behind "ช่วย!".
- **#14** Avatar spreads to ~55% including hair. The hook-to-subline gap is ~120px. "ขุดตรงมากเลย" is weak copy for a find. The privacy issue (coordinates, server, GPU) is why this is CRITICAL.
- **#15** The hook is the longest ("เจอทางกลับบ้าน!") and the smallest at 10%. The Shorts hook "!" ends at x≈900, only ~18px from the 918px line.
- **#24** The subline stroke is heavy. A torch sits behind the hook. "เนื้อซอมบี้" is colloquial, not the in-game "เนื้อเน่า".
- **#16** The hook has a white inner stroke, which is good. The avatar is ~49%.
- **#17** Avatar ~55% including hair. Few enemies visible against "ยิงหลายตัวมาก".
- **#18** Avatar ~52% wide. The hook "ลองหมดแล้ว!" is clear. Alien Shooter 2 appears only as Steam UI.
- **#19** The hook and avatar expression conflict (despair vs smirk). Avatar ~50%.
- **#36** Spelling is correct. The 46% avatar width is within spec. The calm expression does not match "crash".
- **#43** "เช็ก" is the correct spelling. The title-only flag ("เซฟ" not in subs) is acknowledged. The hook is only loosely supported (a terminal pad is visible). Avatar expression is flat.
- **#49** Avatar ~48%. The Shorts version has the same Explorer frame, and the avatar's ears overlap file rows.

## Limits
Vision checks are visual estimates (pixel coordinates are approximate). The hard-cut and ear-tip claims were verified by zoom on #24 only; other covers were not individually zoomed. Clip content was checked against mapping `evidence`, not against the footage.
