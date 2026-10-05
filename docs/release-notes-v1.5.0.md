# v1.5.0: Multi-Channel Organization & Handover Protocol

## What's Changed

### 📂 Multi-Channel Deliverables Hub (`outputs/channels/`)
- Introduced clean, human-friendly directory structure separating channels and aspect ratios:
  - `outputs/channels/<channel_name>/<YYYY-MM-DD>/`
    - `16x9_Landscape/` (16:9 thumbnails)
    - `9x16_Shorts/` (9:16 vertical Shorts covers)
    - `_summary_previews/` (Overview sheets)
    - `_reports/` (Internal manifest, QC logs, audit data)
- Instant access shortcuts:
  - `outputs/channels/<channel_name>/_LATEST`
  - `outputs/_LATEST_DELIVERY`

### 🚀 CLI & Developer Tools
- **`cli/build.py`**: Upgraded to unified CLI supporting both predefined projects (`--project tygarina`, etc.) and ad-hoc multi-channel builds (`--channel <name> --hook "..." --sec "..." --bg "..." --avatar "..."`). Automatically delivers into `outputs/channels/` and opens File Explorer.
- **`cli/open.py`**: Instant Windows File Explorer launcher (`python -m cli.open [channel]`) that opens the deliverables folder and displays clickable links.
- **`cli/organize.py`**: Automated channel organization and `_LATEST` sync tool.
- **`projects/channels.json`**: Central registry for channel brand colors, fonts, and asset locations.

### 🧩 Typography Engine (Raqm on Windows)
- Bundled FriBidi runtime DLL (`src/engine/runtime/libfribidi-0.dll`) and configured `src/engine/text_thai.py` with automatic DLL discovery on Windows.
- Full libraqm OpenType complex text layout enabled with 0 warnings.
- Pytest suite: 26 passed, 0 warnings.

### 📋 Agent Protocol (`AGENTS.md`)
- Added mandatory **Channel Output & User Handover Protocol**:
  1. Always organize deliverables by channel and aspect ratio.
  2. Always execute `python -m cli.open <channel>` upon completion to open the folder on the user's screen.
  3. Always provide clickable markdown links in the final message.
