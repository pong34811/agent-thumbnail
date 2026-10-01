from PIL import Image
from src.engine.compositor import ThumbnailCompositor
from src.engine.layout import LANDSCAPE_DIMS, SHORTS_DIMS


def test_composite_landscape():
    compositor = ThumbnailCompositor()
    bg = Image.new("RGBA", (1920, 1080), (30, 30, 40, 255))
    avatar = Image.new("RGBA", (600, 900), (255, 180, 120, 255))
    
    result = compositor.composite_landscape(
        bg_image=bg,
        avatar_image=avatar,
        hook_lines=["ระวังหลัง!"],
        secondary_lines=["ไม่รอดแน่"],
        focus_circle=(500, 400, 80),
        emotion_marker=("!", (1300, 200)),
        is_gameplay=True,
    )
    
    assert result.size == LANDSCAPE_DIMS
    assert result.mode == "RGB"


def test_composite_shorts():
    compositor = ThumbnailCompositor()
    bg = Image.new("RGBA", (1080, 1920), (20, 20, 30, 255))
    avatar = Image.new("RGBA", (500, 700), (200, 150, 100, 255))
    
    result = compositor.composite_shorts(
        bg_image=bg,
        avatar_image=avatar,
        hook_lines=["ช็อตฟีล!"],
        brightness=0.9,
    )
    
    assert result.size == SHORTS_DIMS
    assert result.mode == "RGB"
