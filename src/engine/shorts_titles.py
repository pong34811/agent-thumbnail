"""Title handling for one-line-per-color Shorts thumbnail typography."""

from __future__ import annotations

from collections.abc import Callable


_TIMELINE_GROUP_SUFFIXES = (
    "_Monster Hunter World",
    "_Soul Walker",
    "_Minecraft",
    "_Terraria",
)


def canonical_title_from_timeline(timeline_name: str) -> str:
    """Remove only Shorts/export and known game-group suffixes from a timeline name."""
    title = timeline_name
    if title.endswith("_9x16"):
        title = title[:-5]
    for suffix in ("-vdo", "_vdo"):
        if title.endswith(suffix):
            title = title[: -len(suffix)]
            break
    for suffix in _TIMELINE_GROUP_SUFFIXES:
        if title.endswith(suffix):
            title = title[: -len(suffix)]
            break
    return title.rstrip()


def validate_title_parts(title: str, red: str, white: str) -> None:
    """Require one visual line per color whose concatenation preserves the title."""
    if not all(isinstance(value, str) for value in (title, red, white)):
        raise ValueError("Title and colored title parts must be strings")
    if not title or not red:
        raise ValueError("The canonical title and red title line must not be empty")
    if any("\n" in value or "\r" in value for value in (red, white)):
        raise ValueError("Each colored title part must be a single line")
    if red + white != title:
        raise ValueError("Red and white title parts must preserve the canonical title exactly")


def fit_single_line_size(
    text: str,
    max_width: int,
    preferred_size: int,
    minimum_size: int,
    measure_width: Callable[[str, int], int],
) -> int | None:
    """Return the largest even-step font size that fits, or None inside the range."""
    if "\n" in text or "\r" in text:
        raise ValueError("Text must be a single line")
    if max_width <= 0 or minimum_size <= 0 or preferred_size < minimum_size:
        raise ValueError("Invalid width or font-size range")
    sizes = range(preferred_size, minimum_size - 1, -2)
    for size in sizes:
        if measure_width(text, size) <= max_width:
            return size
    if (preferred_size - minimum_size) % 2:
        if measure_width(text, minimum_size) <= max_width:
            return minimum_size
    return None
