# v1.6.0: Repository Cleanup, Code-Review Fixes & `cli.doctor`

## What's Changed

### 🧹 Repository Cleanup
- Removed legacy `tools/timeline-covers/` scripts (superseded by `cli/` and `src/`).
- Removed `.work/` scratch directory; the two Armigon example scripts still referenced by the skill moved to `.agents/skills/davinci-thumbnails/scripts/` (`build_armigon_covers_v3.py`, `armigon_graphics_overlay.py`).
- Removed empty `scripts/`, `.superpowers/`, `__pycache__/`, `.pytest_cache/` and stale Claude worktrees.
- Updated stale path references in `jpg-render-notes.md` and `IDEA.md`.

### 🧠 Skills
- General-purpose skills (38) now live as real directories in `.claude/skills/`, tracked together with `skills-lock.json`.
- `.agents/skills/` keeps only the project skills: `davinci-thumbnails`, `vtuber-thumbnail-layout`, `vtuber-thumbnail-qc`.
- `davinci-thumbnails` v1.2.0: added Tygarina v7 examples and the good-thumbnail patterns/checklist; build guidance now matches the current `cli.build`.

### 🐛 Bug Fixes (code review)
- `cli.build --project`:
  - Reads per-orientation `hook`/`sec` from nested `land`/`short` blocks (Aomi Debut previously rendered with no text).
  - Falls back to the text after `" - "` in the title when no hook is defined.
  - Accepts `model` and `bg` keys; resolves avatar filenames against the project's `MODEL_DIR` and warns when a file is missing.
- `cli.organize`: only date-named folders are considered; `_LATEST` is never wiped when the newest batch contains no images.
- `cli.verify`: fails when the manifest lists a file that is not on disk.
- `cli.package`: replaced `assert` with explicit errors so validation survives `python -O`.
- `text_thai.py`: removed hard-coded `D:\...` and `outputs/...` font/runtime paths; now warns when the font or libraqm is unavailable instead of silently degrading.
- Shorts covers: text is now horizontally centered on `ShortsLayout.CENTER_X` (was left-aligned at x=70).

### 🛠 New Tooling
- `python -m cli.doctor`: checks Pillow, numpy, libraqm, Mitr Bold font and ffmpeg; exits non-zero on missing required dependencies.

### 🎨 Project Data
- Armigon: hook and secondary lines for all 16 timelines imported from `reports/armigon/2026-09-20/cover-plan.json`; added `MODEL_DIR`.
- Tygarina: wording fixes in `projects/tygarina/mapping.py`.

### 📋 Agent Protocol (`AGENTS.md`)
- Rewritten around gotchas: start with `cli.doctor`, libraqm import order, supported mapping shapes, no junctions between `.claude/skills` and `.agents/skills`.
- Mandatory QC, images-only `outputs/`, `cli.open` and clickable-link handover rules unchanged.

### ✅ Tests
- 34 passed (was 26): new `tests/test_cli.py`, Shorts centering test, Armigon mapping test.

### ⚠️ Notes
- Previously delivered Shorts covers in `outputs/` were not re-rendered and keep the old left-aligned text.
- Armigon covers still need real background frames (`bg`/`frame_path`) and access to the model drive.
