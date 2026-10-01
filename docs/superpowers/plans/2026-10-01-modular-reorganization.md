# Modular Architecture Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the repository from fragmented machine-specific batch scripts into a clean, modular Python architecture with reusable core engine, decoupled project batch configs, standardized CLI, and clean skill references.

**Architecture:**
- `src/engine/`: Core compositing, Thai typography with libraqm, layout geometry, and graphic storytelling accents.
- `src/resolve/`: DaVinci Resolve timeline metadata extraction and headless Text+ caption extraction.
- `projects/`: Decoupled project configs and timeline mappings (Aomi, Tygarina, Armigon).
- `cli/`: Standardized CLI commands (`build.py`, `verify.py`, `package.py`, `sample_frames.py`).
- `tests/`: Centralized test suite migrated from `.work/`.
- `skills/`: Canonical source for `katy404-canva-thumbnails` skill and references.

**Tech Stack:** Python 3.10+, Pillow (with libraqm / RAQM engine), NumPy, pytest.

## Global Constraints
- Preserve all existing deliverables in `outputs/` without any modifications or deletions.
- Ensure all Thai text rendering retains strict compatibility with `libraqm` and Mitr Bold.
- Keep absolute backward compatibility so previous deliverables could be reproduced identically.
- Remove foreign untracked clutter (`.agents/skills/ECC/` and `.agents/skills/ponytail/`).

---

### Task 1: Clean Up Foreign Clutter and Duplicate Skills
- Remove untracked foreign directories `.agents/skills/ECC` and `.agents/skills/ponytail`.
- Synchronize `.agents/skills/katy404-canva-thumbnails` with `skills/katy404-canva-thumbnails`.

### Task 2: Implement Core Engine (`src/engine/`)
- Create `src/__init__.py` and `src/engine/__init__.py`.
- Create `src/engine/text_thai.py`: Font loading, RAQM layout, text bounding box calculation, stroke sizing, and Thai upper mark clearing for `ป, ฝ, ฟ` and `ไ, ใ, โ`.
- Create `src/engine/graphics.py`: Hand-drawn red brush circle (`#EC1C24`) with glow and dark outline, anime exclamation/question markers (`!`, `?`), and smooth backdrop gradient masks.
- Create `src/engine/layout.py`: Safe zones, dimensions, coordinate calculations for 16:9 Landscape and 9:16 Shorts.
- Create `src/engine/compositor.py`: Unified compositing pipeline assembling background, avatar 5-layer separation, text, and graphic accents.

### Task 3: Implement Resolve Extraction Modules (`src/resolve/`)
- Create `src/resolve/__init__.py`.
- Create `src/resolve/audit.py`: Headless DaVinci Resolve timeline audit.
- Create `src/resolve/textplus.py`: Headless `.drp` Text+ title parser.

### Task 4: Decouple Project Batches (`projects/`)
- Create `projects/aomi-debut/mapping.py`: Timeline mapping, cues, and crops from `build_covers.py`.
- Create `projects/tygarina/mapping.py`: Timeline mapping, cues, and crops from `build_tygarina_covers.py`.
- Create `projects/armigon/mapping.py`: Timeline mapping, cues, and crops from `build_armigon_covers_v3.py`.

### Task 5: Implement Standardized CLI (`cli/`)
- Create `cli/build.py`: Unified build CLI accepting project name, output directory, and orientation.
- Create `cli/verify.py`: Unified verification script checking dimensions, margins, text-avatar collisions, and Shorts centering.
- Create `cli/package.py`: Delivery packager generating manifest and verified ZIP.
- Create `cli/sample_frames.py`: High-resolution frame sampler from video footage.

### Task 6: Centralize Test Suite (`tests/`)
- Migrate and refactor tests into `tests/test_graphics.py`, `tests/test_layout.py`, and `tests/test_text_thai.py`.
- Run tests with `pytest` or Python unittest to verify that the core engine passes all tests.

### Task 7: Update Environment, Requirements & Documentation
- Create `requirements.txt`.
- Update `AGENTS.md` to document the new architecture and file locations.
- Update `.gitignore` to keep the workspace clean.
