"""Safe zones, platform dimensions, and coordinate geometry for YouTube thumbnails.
"""
from typing import Tuple, Dict, Any, List

LANDSCAPE_DIMS: Tuple[int, int] = (1920, 1080)
SHORTS_DIMS: Tuple[int, int] = (1080, 1920)


class LandscapeLayout:
    """Standard 16:9 Landscape Layout (1920x1080) for YouTube VOD and Highlights."""
    WIDTH = 1920
    HEIGHT = 1080

    # Recommended Text Safe Zone (Center-Left Elevation)
    TEXT_X_MIN = 80
    TEXT_X_MAX = 930
    TEXT_Y_CENTER_MIN = 380
    TEXT_Y_CENTER_MAX = 520
    TEXT_MAX_WIDTH = 850

    # Recommended Avatar Zone (Right Side)
    AVATAR_X_MIN = 950
    AVATAR_X_MAX = 1850

    # Danger Zones (YouTube Platform UI Overlays)
    TIMESTAMP_BADGE = (1580, 980, 1900, 1060)
    BOTTOM_SCRUBBER = (0, 1062, 1920, 1080)
    HOVER_ACTIONS = (1780, 20, 1900, 160)
    MIN_OUTER_MARGIN = 40

    @classmethod
    def is_safe_from_timestamp(cls, bbox: Tuple[int, int, int, int]) -> bool:
        """Returns True if bbox does not intersect with the bottom-right timestamp badge."""
        x0, y0, x1, y1 = bbox
        tx0, ty0, tx1, ty1 = cls.TIMESTAMP_BADGE
        return not (x0 < tx1 and x1 > tx0 and y0 < ty1 and y1 > ty0)

    @classmethod
    def check_margins(cls, bbox: Tuple[int, int, int, int]) -> bool:
        """Returns True if bbox satisfies outer boundary margins."""
        x0, y0, x1, y1 = bbox
        return (
            x0 >= cls.MIN_OUTER_MARGIN
            and y0 >= cls.MIN_OUTER_MARGIN
            and x1 <= cls.WIDTH - cls.MIN_OUTER_MARGIN
            and y1 <= cls.HEIGHT - cls.MIN_OUTER_MARGIN
        )


class ShortsLayout:
    """Standard 9:16 Portrait Layout (1080x1920) for YouTube Shorts."""
    WIDTH = 1080
    HEIGHT = 1920
    CENTER_X = 540

    # Recommended Text Safe Zone (Top Half, Horizontally Centered)
    TEXT_Y_MIN = 280
    TEXT_Y_MAX = 650
    TEXT_MAX_WIDTH = 940

    # Recommended Avatar Safe Zone (Bottom Half, Horizontally Centered)
    AVATAR_Y_BASE = 1920
    AVATAR_HEAD_Y_MIN = 700
    AVATAR_HEAD_Y_MAX = 1100

    # 4:5 Channel Grid Crop Bounds (Top/Bottom 285px removed)
    GRID_4_5_Y_MIN = 285
    GRID_4_5_Y_MAX = 1635

    # 3:4 Search Crop Bounds (Top/Bottom 240px removed)
    GRID_3_4_Y_MIN = 240
    GRID_3_4_Y_MAX = 1680

    # Shorts Feed UI Overlays (Full Screen Player)
    FEED_UI_BOTTOM = (0, 1350, 1080, 1920)     # Title, channel handle, sound
    FEED_ACTION_STACK = (880, 800, 1080, 1750)  # Like, comment, share buttons

    @classmethod
    def is_channel_grid_safe(cls, bbox: Tuple[int, int, int, int]) -> bool:
        """Returns True if key elements (face, text) fit inside the 4:5 channel tab crop."""
        _, y0, _, y1 = bbox
        return y0 >= cls.GRID_4_5_Y_MIN and y1 <= cls.GRID_4_5_Y_MAX

    @classmethod
    def is_horizontally_centered(cls, bbox: Tuple[int, int, int, int], tolerance: int = 15) -> bool:
        """Returns True if element's midpoint is aligned with the center axis."""
        x0, _, x1, _ = bbox
        mid_x = (x0 + x1) / 2.0
        return abs(mid_x - cls.CENTER_X) <= tolerance
