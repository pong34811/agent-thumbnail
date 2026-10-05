# Katy404 thumbnail production — approved 2026-10-04

User approved the brief in audit/timeline-audit.md. Produce one final JPEG for every live timeline: 30 landscape and 30 portrait; keep original timeline spelling in filenames and sanitize invalid filesystem characters only.

## Constraints

- Project identity KT404_2026-09-29; media and avatar paths supplied by user.
- Source files are read-only. Do not edit timelines, media, subtitles, or render configuration. Temporarily selecting timelines for read-only audit is permitted; restore initial selection.
- Use source frames and subtitle/marker evidence. Markers are candidates, not proof. Source offsets must use source FPS verified by ffprobe. Dragon markers and duplicate Hell City/boss-grab timelines require explicit reconciliation.
- Mitr Bold with RAQM; red #EC1C24 primary hook, white secondary, black stroke about 8%; 0px gameplay blur.
- Landscape text center-left, avatar right; portrait composed independently with key face/text above bottom 25% and left of right 15% danger region.
- No invention of events, characters, numbers, or emotions. No guarantee about CTR.
- Export JPG with sRGB profile, exact dimensions, <=2MB. Manifest ties each file to actual timeline/source time/asset/hook.

## Tasks

1. Current project audit: verify track enabled state on each selected timeline; source frames, pairing, footage duration, and notable mismatches. Parent owns audit reports.
2. Evidence selection A: timelines 1–15. Subagent extracts several source candidates into evidence/a, views real frames, checks subtitles, writes selection-a.json with short hook, secondary, source timestamp, file, avatar suffix and rationale.
3. Evidence selection B: timelines 16–30. Same contract, evidence/b and selection-b.json. Resolve duplicate clips and dragon FPS before selection.
4. Production renderer: independent script render_covers.py consuming merged selection.json + audit inventory; create flat JPGs, manifest, preview/contact sheets, geometric checks. Reuse existing Thai typography; do not alter core engine. Run on final selection after evidence tasks.
5. Verification and QC: cli.verify, full/mobile/grayscale/squint/badge previews on all 60 finals; inspect all finals with shared rubric using delegated reviewers; fix critical issues and recheck changed images. Scope parity and sRGB/geometric checks in addition to generic verify.
6. Package: cli.package, verify manifest membership, archive CRC and decode all JPEGs; deliver ZIP, preview sheets, QC and audit report.

## Shared interfaces

Tasks 2/3 -> 4: selection rows keyed by landscape timeline index; fields index, hook_lines, secondary_lines, source_path, source_time_seconds, frame_path, avatar_file, rationale, caveats. Task 4 applies each row to paired actual 9x16 timeline.
Tasks 1/4 -> 5/6: exact 60-name inventory; timeline fps is distinct from actual source stream fps. Duplicate content still gets separate output per timeline with truthful hooks.

## Progress

- Preflight: generic cli.build is placeholder; use task-specific renderer and existing Thai utilities. Generic cli.verify does not enforce scope or visual safe zones; add explicit geometry/scope checks and visual QC.
- Design approved by user. Read-only initial audit complete; scene validation and production pending.
