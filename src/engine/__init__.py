"""Rendering, typography, graphics, and compositing engine modules.
"""
from .text_thai import fit_text, render_thai_lines, get_font
from .graphics import (
    draw_hand_drawn_circle,
    draw_emotion_marker,
    create_backdrop_gradient,
)
from .layout import (
    LANDSCAPE_DIMS,
    SHORTS_DIMS,
    LandscapeLayout,
    ShortsLayout,
)
from .compositor import ThumbnailCompositor

__all__ = [
    "fit_text",
    "render_thai_lines",
    "get_font",
    "draw_hand_drawn_circle",
    "draw_emotion_marker",
    "create_backdrop_gradient",
    "LANDSCAPE_DIMS",
    "SHORTS_DIMS",
    "LandscapeLayout",
    "ShortsLayout",
    "ThumbnailCompositor",
]
