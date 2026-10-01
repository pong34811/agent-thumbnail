import pytest
from src.engine.layout import (
    LANDSCAPE_DIMS,
    SHORTS_DIMS,
    LandscapeLayout,
    ShortsLayout,
)


def test_dimensions():
    assert LANDSCAPE_DIMS == (1920, 1080)
    assert SHORTS_DIMS == (1080, 1920)


def test_landscape_margins():
    # Box inside safe area
    safe_box = (100, 100, 1800, 950)
    assert LandscapeLayout.check_margins(safe_box) is True

    # Box violating left margin (< 40)
    unsafe_left = (20, 100, 500, 500)
    assert LandscapeLayout.check_margins(unsafe_left) is False


def test_landscape_timestamp_danger_zone():
    # Box completely outside bottom-right
    safe_box = (100, 380, 800, 520)
    assert LandscapeLayout.is_safe_from_timestamp(safe_box) is True

    # Box inside timestamp badge (1580..1900, 980..1060)
    danger_box = (1600, 990, 1850, 1050)
    assert LandscapeLayout.is_safe_from_timestamp(danger_box) is False


def test_shorts_centering():
    # Exactly centered (center_x = 540)
    centered_box = (440, 300, 640, 500)
    assert ShortsLayout.is_horizontally_centered(centered_box, tolerance=5) is True

    # Off-center box
    off_center = (200, 300, 600, 500)
    assert ShortsLayout.is_horizontally_centered(off_center, tolerance=5) is False


def test_shorts_grid_crop():
    # Fits within 4:5 crop (y: 285..1635)
    safe_grid = (100, 350, 980, 1500)
    assert ShortsLayout.is_channel_grid_safe(safe_grid) is True

    # Violates top crop
    violates_top = (100, 100, 980, 800)
    assert ShortsLayout.is_channel_grid_safe(violates_top) is False
