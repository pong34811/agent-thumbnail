"""Thai Typography Rendering Engine for VTuber Thumbnails.

Supports:
- Pillow + libraqm OpenType complex text layout (RAQM)
- Mitr Bold auto-fit and stroke thickness ratio
- Precise Ink Bounding Box line stacking
- Upper mark collision detection and left-nudging on tall consonants (ป, ฝ, ฟ)
"""
import os
import warnings
from pathlib import Path
from typing import List, Tuple, Optional

# Ensure libraqm / FriBidi is loaded on Windows for complex Thai OpenType layout
if os.name == "nt":
    RUNTIME_DIRS = [
        Path(__file__).resolve().parent / "runtime",
    ]
    for rdir in RUNTIME_DIRS:
        if rdir.is_dir():
            try:
                os.add_dll_directory(str(rdir))
                import ctypes
                for dll_name in ("fribidi.dll", "libfribidi-0.dll"):
                    dll_path = rdir / dll_name
                    if dll_path.is_file():
                        ctypes.WinDLL(str(dll_path))
                break
            except Exception:
                pass

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Candidate font locations
DEFAULT_FONT_CANDIDATES = [
    os.environ.get("THUMBNAIL_FONT_PATH"),
    os.environ.get("ARMIGON_FONT_PATH"),
    r"D:\agent-thumbnail\outputs\timeline-covers\fonts\Mitr-Bold.ttf",
    r"C:\Windows\Fonts\Mitr-Bold.ttf",
    str(Path(__file__).resolve().parents[2] / "outputs" / "timeline-covers" / "fonts" / "Mitr-Bold.ttf"),
]

TALL = {"ป": "บ", "ฝ": "ผ", "ฟ": "พ"}  # same advance, no ascender
UPPER = set("ัิีึื็่้๊๋์ํ")
MIN_GAP = 0.05  # em, fill gap kept between a mark and the ascender


def resolve_font_path(custom_path: Optional[str] = None) -> Optional[Path]:
    """Finds an existing font path from custom path, env var, or known defaults."""
    if custom_path and Path(custom_path).exists():
        return Path(custom_path)
    for cand in DEFAULT_FONT_CANDIDATES:
        if cand and Path(cand).exists():
            return Path(cand)
    return None


def raqm_available() -> bool:
    """True when Pillow can use libraqm (required for correct Thai mark positioning)."""
    from PIL import features

    return bool(features.check("raqm"))


_warned = set()


def _warn_once(key: str, message: str) -> None:
    if key not in _warned:
        _warned.add(key)
        warnings.warn(message, RuntimeWarning, stacklevel=3)


def get_font(size: int, font_path: Optional[str] = None) -> ImageFont.FreeTypeFont:
    """Loads Mitr Bold with the RAQM layout engine, warning loudly when degraded."""
    resolved = resolve_font_path(font_path)
    if resolved is None:
        _warn_once("font", "Mitr-Bold.ttf not found; Thai text will render with a fallback font. "
                           "Set THUMBNAIL_FONT_PATH or pass --font.")
        return ImageFont.load_default(size)
    if not raqm_available():
        _warn_once("raqm", "libraqm is unavailable; Thai vowels/tone marks may be mispositioned. "
                           "Run `python -m cli.doctor` for details.")
        return ImageFont.truetype(str(resolved), size)
    return ImageFont.truetype(str(resolved), size, layout_engine=ImageFont.Layout.RAQM)


def text_box(text: str, font: ImageFont.ImageFont, stroke_width: int = 0) -> Tuple[int, int, int, int]:
    """Computes exact text bbox for a given line."""
    dummy = Image.new("L", (8, 8))
    draw = ImageDraw.Draw(dummy)
    return draw.textbbox((0, 0), text, font=font, anchor="ls", stroke_width=stroke_width)


def fit_text(
    lines: List[str],
    max_w: int,
    start_size: int = 165,
    min_size: int = 90,
    stroke_ratio: float = 0.08,
    font_path: Optional[str] = None,
) -> Tuple[ImageFont.ImageFont, int]:
    """Auto-fits font size and stroke width to stay within max width."""
    size = start_size
    while size > min_size:
        f = get_font(size, font_path)
        stroke = max(4, round(size * stroke_ratio))
        widths = [(b[2] - b[0]) for b in (text_box(ln, f, stroke) for ln in lines)]
        if all(w <= max_w for w in widths):
            return f, stroke
        size -= 2
    f = get_font(min_size, font_path)
    return f, max(4, round(min_size * stroke_ratio))


def _mask(size: Tuple[int, int], xy: Tuple[int, int], text: str, f: ImageFont.ImageFont, anchor: str, stroke: int = 0) -> np.ndarray:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).text(xy, text, font=f, fill=255, anchor=anchor, stroke_width=stroke, stroke_fill=255)
    return np.asarray(m, dtype=np.float32)


def _shift(a: np.ndarray, dx: int, dy: int) -> np.ndarray:
    out = np.zeros_like(a)
    h, w = a.shape
    out[max(0, dy):h + min(0, dy), max(0, dx):w + min(0, dx)] = a[
        max(0, -dy):h - max(0, dy), max(0, -dx):w - max(0, dx)
    ]
    return out


def _dilate(a: np.ndarray, r: int) -> np.ndarray:
    out = a.copy()
    for dy in range(-r, r + 1):
        span = int((r * r - dy * dy) ** 0.5)
        for dx in range(-span, span + 1):
            np.maximum(out, _shift(a, dx, dy), out=out)
    return out


def _base_of(text: str, i: int) -> Optional[int]:
    j = i - 1
    while j >= 0 and text[j] in UPPER:
        j -= 1
    return j if j >= 0 else None


def line_masks(
    canvas_size: Tuple[int, int],
    xy: Tuple[int, int],
    text: str,
    f: ImageFont.ImageFont,
    anchor: str,
    stroke: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """Generates (stroke_mask, fill_mask) float arrays with mark clearing over tall consonants."""
    clusters = {}
    for i, ch in enumerate(text):
        if ch in UPPER and _base_of(text, i) is not None:
            clusters.setdefault(_base_of(text, i), []).append(i)
    if not clusters:
        return _mask(canvas_size, xy, text, f, anchor, stroke), _mask(canvas_size, xy, text, f, anchor)

    every = {i for v in clusters.values() for i in v}
    drop = lambda t, idx, twin_at=None: "".join(
        (TALL.get(ch, ch) if k == twin_at else ch) for k, ch in enumerate(t) if k not in idx
    )
    base_fill = _mask(canvas_size, xy, drop(text, every), f, anchor)
    fills = base_fill.copy()
    strokes = _mask(canvas_size, xy, drop(text, every), f, anchor, stroke)
    f_size = getattr(f, "size", 100)
    need = max(4, round(f_size * MIN_GAP))

    xh_top = xy[1] + text_box("น", f, 0)[1] - round(f_size * 0.04)
    for j, own in clusters.items():
        others = every - set(own)
        visible = np.clip(_mask(canvas_size, xy, drop(text, others), f, anchor) - base_fill, 0, 255)
        shape = np.clip(
            _mask(canvas_size, xy, drop(text, others, j), f, anchor)
            - _mask(canvas_size, xy, drop(text, every, j), f, anchor),
            0,
            255,
        )
        ys, xs = np.nonzero(shape > 8)
        if len(ys) == 0 or len(xs) == 0:
            continue
        pad = round(f_size * 0.45) + stroke
        y0, y1 = max(0, ys.min() - pad), min(shape.shape[0], ys.max() + pad)
        x0, x1 = max(0, xs.min() - pad), min(shape.shape[1], xs.max() + pad)
        S, V, B = shape[y0:y1, x0:x1], visible[y0:y1, x0:x1] > 128, base_fill[y0:y1, x0:x1] > 128
        tall_base = text[j] in TALL

        if not ((_dilate(np.where(V, 255.0, 0.0).astype(np.float32), 1) > 128) & B).any():
            real = visible[y0:y1, x0:x1]
        elif not tall_base:
            real = visible[y0:y1, x0:x1]
        else:
            best, where = None, (0, 0)
            for dy in range(-round(f_size * 0.12), round(f_size * 0.12) + 1):
                for dx in range(-round(f_size * 0.35), round(f_size * 0.15) + 1):
                    s = _shift(S, dx, dy) > 128
                    score = int((s & V).sum()) - int((s & ~V & ~B).sum())
                    if best is None or score > best:
                        best, where = score, (dx, dy)
            real = _shift(S, *where)

        tall = B.copy()
        tall[max(0, xh_top - y0):, :] = False
        shifted, cleared = real, False
        for step in range(round(f_size * 0.45) + 1):
            cand = _shift(real, -step, 0)
            if not ((_dilate(cand, need) > 128) & tall).any() and not ((_dilate(cand, 1) > 128) & (B & ~tall)).any():
                shifted, cleared = cand, True
                break
        if not cleared:
            shifted = real

        fills[y0:y1, x0:x1] = np.maximum(fills[y0:y1, x0:x1], shifted)
        strokes[y0:y1, x0:x1] = np.maximum(strokes[y0:y1, x0:x1], _dilate(shifted, stroke))

    return strokes, fills


def render_thai_lines(
    canvas_size: Tuple[int, int],
    xy_baseline: Tuple[int, int],
    lines: List[str],
    font: ImageFont.ImageFont,
    fill_color: Tuple[int, int, int],
    stroke_color: Tuple[int, int, int] = (0, 0, 0),
    stroke_width: int = 12,
    anchor: str = "ls",
    line_spacing_ratio: float = 0.12,
) -> Image.Image:
    """Renders multi-line Thai text with stroke and fill onto a transparent RGBA image."""
    layer = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    x, y = xy_baseline
    f_size = getattr(font, "size", 100)

    for line in lines:
        s_mask, f_mask = line_masks(canvas_size, (x, y), line, font, anchor=anchor, stroke=stroke_width)
        s_img = Image.fromarray(np.clip(s_mask, 0, 255).astype(np.uint8), mode="L")
        f_img = Image.fromarray(np.clip(f_mask, 0, 255).astype(np.uint8), mode="L")

        stroke_layer = Image.new("RGBA", canvas_size, (*stroke_color, 255))
        stroke_layer.putalpha(s_img)
        fill_layer = Image.new("RGBA", canvas_size, (*fill_color, 255))
        fill_layer.putalpha(f_img)

        layer = Image.alpha_composite(layer, stroke_layer)
        layer = Image.alpha_composite(layer, fill_layer)

        # Move to next line using ink height
        bbox = text_box(line, font, stroke_width)
        line_height = (bbox[3] - bbox[1]) + round(f_size * line_spacing_ratio)
        y += line_height

    return layer
