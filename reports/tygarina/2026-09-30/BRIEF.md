# Brief: hook plan for Tygarina 2026-09-30 covers (shared by 5 agents)

Repo: C:/Users/warit/Desktop/agent-thumbnail (Windows, git-bash; use `py` not `python`). Reply/notes in Thai where prose; JSON keys in English.
Do NOT edit any file outside your own output files. Do NOT touch git. Do NOT open Resolve / DaVinciResolveScript (inventory is already extracted).

## Input
reports/tygarina/2026-09-30/timeline-inventory.json = list of dicts
  {project, i, name, frames, fps(60), res:[w,h], src (video path), srcstart (source frame offset @60fps), subs:[[timeline_frame, text],...]}
Each Resolve project has N landscape timelines (res 1920x1080, name ends `-vdo` or similar) and N portrait twins (1080x1920, name + `_9x16`, same src/srcstart/subs). Work only on LANDSCAPE rows of YOUR projects; the twin inherits the plan.
Subtitle frame / 60 = timeline seconds. Source time (s) = (srcstart + timeline_frame) / 60.

## Your job (per landscape timeline of your projects)
1. Read the subtitle cues, pick ONE real moment/emotion with evidence in the cues.
2. hook: 1-4 Thai words (list of 1-2 lines), punchy, only claims supported by cues. NO invented names/numbers. No spaces between Thai words except around Latin names/after "!" "?" as in `เหลือคนเดียว!`.
   sec: ONE short Thai secondary line (<= ~14 chars preferred, max 20) that adds context, not a copy of the timeline name.
   Spell-check Thai (ASR subtitles can be wrong; if cue looks doubtful, use title + other cues and set flag).
3. frame_tl: timeline SECOND (integer) of the best frame (the peak of the hook moment). Extract it to verify:
   ffmpeg -v error -y -ss <(srcstart/60 + frame_tl)> -i "<src>" -frames:v 1 "<scratch>/<project>_<i>.png"
   (scratch = C:/Users/warit/AppData/Local/hermes/cache/scratch/tyg0930/). Look at the frame with vision_analyze if available. The frame must show gameplay/the scene (not black, not loading, not an overlay-only screen). Adjust frame_tl until it does.
4. talk = true if the scene is chat / free talk / slide / mostly the streamer overlay (background will be heavily blurred); false for gameplay (0px blur).
5. emotion model: choose ONE of 01_neutral 02_smile 03_shock 04_angry 05_smug 06_cry 07_panic (.png) matching the moment; vary across the set (do not use one pose for everything; max ~35% same pose within your group).
6. flag: "" if cues strongly support hook, else "title-only: <reason>" or "subs doubtful: <reason>" or "game voice only". evidence: short string with cue seconds + quoted words.

Avoid repeating the same hook text across timelines (within and, as far as you can tell, across your group).
Read .agents/skills/davinci-thumbnails/references/channel-profiles/tygarina.md and a few lines of references/style-guide.md for tone before writing hooks.

## Output (write exactly this file; UTF-8, JSON list, one object per landscape timeline, in inventory order)
reports/tygarina/2026-09-30/hooks_<GROUP>.json  with objects:
{"project": "...", "i": <inventory i of the LANDSCAPE row>, "name": "<landscape timeline name>", "tl_short": "<portrait twin name>", "hook": ["..."], "sec": ["..."], "frame_tl": <int>, "talk": <bool>, "model": "05_smug.png", "evidence": "...", "flag": ""}
Validate with: py -c "import json;d=json.load(open('<file>',encoding='utf-8'));print(len(d))" and check count equals the number of landscape timelines in your projects.
Final reply (short, Thai): file path, count, number of flagged rows, any problem. Do not paste the JSON.
