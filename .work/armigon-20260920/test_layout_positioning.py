import pytest
from PIL import Image
from build_armigon_covers_v3 import draw_text_block

def test_landscape_text_vertical_centering():
    canvas = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    info = draw_text_block(canvas, "ใครก็ได้ แบกโฮชิหน่อย", "ชุบได้ไหม", portrait=False)
    bbox = canvas.getbbox()
    assert bbox is not None
    # Text must be vertically centered in the upper-mid area (y between 300 and 650)
    # NOT in the old bottom-heavy area (y > 700)
    top_y = bbox[1]
    bottom_y = bbox[3]
    center_y = (top_y + bottom_y) // 2
    assert 360 <= center_y <= 560
    # Left edge must respect margin
    assert 60 <= bbox[0] <= 120
    # Text font size should be large and prominent
    assert info["hook_font"] >= 130
