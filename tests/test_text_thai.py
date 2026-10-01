from PIL import Image
from src.engine.text_thai import fit_text, render_thai_lines, text_box, get_font


def test_fit_text():
    lines = ["ช่วยด้วย!", "อย่าหันไปมอง"]
    font, stroke = fit_text(lines, max_w=800, start_size=165, min_size=80)
    assert font is not None
    assert stroke >= 4
    # Ensure text fits within max_w
    for ln in lines:
        bbox = text_box(ln, font, stroke)
        width = bbox[2] - bbox[0]
        assert width <= 800


def test_render_thai_lines():
    canvas_size = (1920, 1080)
    font = get_font(120)
    lines = ["ปาฏิหาริย์", "ฝันร้าย"]
    rendered = render_thai_lines(
        canvas_size,
        (100, 400),
        lines,
        font,
        fill_color=(236, 28, 36),
        stroke_color=(0, 0, 0),
        stroke_width=10,
    )
    assert rendered.size == canvas_size
    assert rendered.mode == "RGBA"
    # Ensure not all pixels are transparent
    alpha = rendered.split()[3]
    extrema = alpha.getextrema()
    assert extrema[1] > 0
