# QC Full – Group A (ids 1-9, 37, 38, 44-46) – Aomi-mama 2026-10-11

Method: vtuber-thumbnail-qc; qc_previews.py → scratch/qc-A; vision on full-size L (1920x1080) and S (1080x1920) for all 14 (28 images), mobile preview checked for ids 1, 6, 37 only. Zoom checks on 5S, 6L, 46L. Covers READ-ONLY (nothing edited).
Not reported (accepted): hook red-on-red/brown on #1,#4,#37,#45; 13 reused avatar poses. 9:16 avatar in bottom 25% is the layout (VTuber Bottom), not flagged.
Spelling: all 28 images – hook and sub match mapping.py, tone marks/ั ิ ื ์ intact (zoom on 6L confirmed ซื้อ/ไม่/ได้). No misspelling found.
Caveat: first-pass vision claimed "hard vertical cut at avatar lower-left (x≈820-865)" on 5L,6L,7L,38L; zooms on 6L contradicted it (curved hair edge) → treated as NOT confirmed.

| id | game / clip | L | S | worst | top fix |
|---|---|---|---|---|---|
| 1 | LH boss lure | 78 | 82 | IMPORTANT | Frame is MISSION COMPLETE panel (not the lure fight); sub white OK; hook already accepted-red. Pick frame ~3-5 s earlier showing boss, or accept |
| 2 | LH prep fort (title-only) | 80 | 83 | IMPORTANT | Frame shows MISSION COMPLETE/TAP HERE banner, contradicts "ศึกใหญ่กำลังมา"; S: avatar overlaps banner. Move frame to a pre-wave moment |
| 3 | LH greeting (talk) | 88 | 86 | OPTIONAL | none blocking; avatar left edge ~52% (slightly right of 50%) – fine |
| 4 | LH alien swarm | 84 | 85 | IMPORTANT | Frame shows swarm (good) but flag "subs are chat talk" – verify clip audio vs title "ร้องลั่น" |
| 5 | LH grandkid chat (talk) | 86 | 84 | OPTIONAL | S: stray white outline blob next to avatar ear (zoom-confirmed) – cut outline fragment ~10 px; L fine |
| 6 | LH gun money short | 80 | 76 | IMPORTANT | Shop UI tiny/unreadable at 10% mobile; L: avatar covers last shop item; S: ears/hair cover bottom-row prices (4900$/8000$) and 300 px empty gap above shop. Enlarge/crop shop to price row incl. 26400$ vs MONEY 25220 (evidence does support hook) |
| 7 | AS chat (talk) | 88 | 84 | OPTIONAL | S: tiny white fragment at bottom-right corner – remove; hook right edge ~885px near 85% limit (918) |
| 8 | AS hard? | 82 | 84 | IMPORTANT | No difficulty/hard-mode label visible in frame ("เล่นโหมดฮาร์ด" unsupported by pixels); S: HUD cropped. Verify clip says hard mode or reword sub (e.g. "ตอบแชทระหว่างเล่น") |
| 9 | AS finish talk | 88 | 85 | OPTIONAL | S: hook top at y≈190 close to top UI zone – shift down 30-40 px |
| 37 | LH missing room | 76 | 80 | IMPORTANT | MISSION COMPLETE banner in frame (clutter, "SECRETS 7/8" actually supports "room missing" – keep but crop banner to ~40%); L avatar ~55% width (house 35-50%) – scale -10%; sub small at 10% – enlarge 10% |
| 38 | LH finish talk | 87 | 82 | OPTIONAL | S: avatar ear tips clipped flat at y≈1060 per vision – inspect; L ok |
| 44 | AS screen setup (talk, flag check scene) | 84 | 82 | IMPORTANT | Blurred bg is unrecognisable – cannot confirm it is live-screen setup (flag "check scene" unresolved); S: hook y≈200 high, large empty middle (500 px) |
| 45 | AS room clear (title-only) | 83 | 82 | IMPORTANT | Live gameplay, but no mission-complete visible and aliens alive in lower right → weak evidence for "จบภารกิจ"; S: hook y≈210 borderline top zone, HUD clipped left |
| 46 | AS green level | 80 | 77 | IMPORTANT | L: possible duplicate avatar fragment at far right edge (x≈1870+, y≈700-1030) and S: blue hair sliver at right edge of game strip – vision-flagged on both, unverified by pixel; inspect and erase. S: large black lower-right area; "จอดับ" is not a dark screen (green night-vision level) – hook/frame mismatch, consider "ด่านมืดสุดท้าย"/frame choice |

Severity totals: CRITICAL 0 · IMPORTANT 9 (ids 1,2,4,6,8,37,44,45,46) · OPTIONAL 5.
Scores are my estimate from vision output (sub-score sum not itemised per cover); no cover < 75.

## Cross-cutting
- No CRITICAL: no misspellings, no black/loading frames, no text–avatar overlap, text inside Shorts safe zone (hook y≥190 in S is borderline top only).
- Frames 1, 2, 37 sit on MISSION COMPLETE panels: evidence-weak for 1 and 2, acceptable for 37.
- Talk clips (3,5,7,9,38,44) blur is by design; 44 is the only one where blur hides all context.
- Shorts: empty 300-500 px band between hook and game strip on talk covers (5,7,9,44) – by layout, optional to tighten.
- Hook red vs sub white: red weaker on mid-gray bg (38L) but outline holds; optional.
