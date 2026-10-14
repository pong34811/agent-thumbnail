# QC group D — ids 33,34,35,40,42,47,48 (LoL) + repetition (read-only)
Method: qc_previews.py (scratch qc-D) + full-size/zoom vision. Scores are my estimates from vision reads (scored per rubric, not summed sub-scores). Vision tends to over-flag; items marked (verified) were zoom-checked.

| id | L | S | worst | top fix |
|---|---|---|---|---|
| 33 | 82 | 74 | IMPORTANT | frame is 00:08, 0/0/0 calm start; does not show "ออกไปก็ตาย" -> pick a fight/death frame; Shorts: mouth/chin/Switch in bottom 25% |
| 34 | 85 | 78 | IMPORTANT | Cover shows NO profanity (no chat/subs; hook "ทีมกากมาก!" only, mild). HUD 7v6 undercuts "กาก"; Shorts hair clipped by straight cut x~50/x~1030 (verified) |
| 35 | 84 | 76 | IMPORTANT | blurred bg, OK for last-stream; Shorts: face/console below y1440, dead gap y500-1050, tiny white fragment bottom-right corner, flat ear tips |
| 40 | 80 | 76 | IMPORTANT | pentakill not proven by frame (Tab scoreboard 51v46, 8/14/24, enemy-slain banner); stray mouse cursor bottom; hook top touches in-game banner, "แพ้" touches portrait/timer; Shorts strip cropped mid-HUD |
| 42 | 83 | 78 | IMPORTANT | sec line repeats hook ("ตีกันตั้งแต่ต้น"); text covers the skirmish (01:43, 0v0); Shorts HUD cut "01:4…", Smolder cut |
| 47 | 84 | 80 | IMPORTANT | text OK: "โอ๊ยๆๆ!" has mai tri + exactly 2 ๆ (verified). Sec "แย่มาก" small, hook over health bars; Shorts right-edge hair cut ~x1048 y1800-1900 |
| 48 | 78 | 76 | IMPORTANT | LoL confirmed (ARAM, Yasuo/Viego/Morgana, 29v51). Hook sits ~50px under in-game "พันธมิตรถูกสังหาร" banner (reads as negative, not "คุยกันสนุก"; title-only, thin subs) -> pick calmer frame or lower hook |

CRITICAL: none. Spelling/tone marks correct on all 14 covers (no change needed): ออกไปก็ตาย!/หนีไม่เป็นแล้ว, ทีมกากมาก!/ออกของไม่ดูเลย, ขอบคุณทุกคน/ปิดสตรีมแล้ว, เพนตาคิล!/แต่ยังพ่ายแพ้, เริ่มเกมก็ไฟต์!/ตีกันตั้งแต่ต้น, โอ๊ยๆๆ!/แย่มาก, เมาท์สายเกม!/คุยกันสนุก.
Common IMPORTANT (all 7 Shorts): avatar layer clipped by straight vertical cut at x~50 and x~1030 (verified on 34) -> widen avatar canvas/scale so hair bleeds off-frame; mouth/chin ~y1450-1510 in bottom-25% zone (raise avatar 40-150px). OPTIONAL: crop/blur FPS/ms readout; enlarge sec line 10-15%.

## Repetition (49 landscape; sheets: scratch qc-D/sheet1.png ids1-25, sheet2.png ids26-49)
Vision on the sheets was unreliable (hallucinated counts), so groups are from mapping.py poses + pixel correlation. Layout is identical by design; pose is the variable (12 of 13 poses used; 03 is a triptych sheet, unusable).
- Pose 04 (veiled subtle fang) x8: 4,13,22,25,32,36,46,47. Most overused. Same-stream pairs: 22+47 (hskX LoL).
- Pose 11 (switch gaze down) x7: 6,9,11,19,28,33,37. Same-source pair: 6+37 (alien shooter last hope).
- Pose 09 x6: 1,12,20,30,38,45; same-source pair 1+38. Pose 13 x5, pose 06 x5 (same-source pair 14+39 Minecraft X6E3).
- Under-used: 02 (only 48), 01 (3,43), 07 (10,31).
- Dark/blurred-bg lookalikes (corr 0.88-0.90): 3,9,10; also 7,35,13; 15,26.
Suggestions (pose files in G:/My Drive/Projects/Aomi-mama/1.picture):
- 22 -> vts_avatar_07_bust_confident_smug (breaks pose 04 pair with 47)
- 37 -> vts_avatar_12_switch_playful_forward_grin (breaks 6+37)
- 38 -> vts_avatar_02_bust_camisole_relaxed (breaks 1+38)
- 14 -> vts_avatar_01_bust_gentle_smile (breaks 14+39)
- 13 -> vts_avatar_02 or 01 (pose 04 x8 -> 6); 32 -> vts_avatar_01
- 9/10/3 (same-looking dark bg): shift 10 frame_tl offset ~+10 frames or change 9 to pose 07 (note 9 is 11-pose; 10 is pose 07 already).
Leave 33,34,35,40,42,47,48 poses unchanged (all distinct within their group).
