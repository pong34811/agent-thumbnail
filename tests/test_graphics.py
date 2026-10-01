import pytest
from PIL import Image
from src.engine.graphics import (
    draw_hand_drawn_circle,
    draw_emotion_marker,
    create_backdrop_gradient,
)


def test_draw_hand_drawn_circle():
    canvas = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw_hand_drawn_circle(canvas, (500, 400), 120, color=(236, 28, 36), stroke_width=12)
    bbox = canvas.getbbox()
    assert bbox is not None
    # Circle bounds should roughly surround center (500, 400) with r=120
    assert 340 <= bbox[0] <= 420
    assert 240 <= bbox[1] <= 320
    assert 580 <= bbox[2] <= 670
    assert 480 <= bbox[3] <= 570


def test_draw_emotion_marker_exclamation():
    canvas = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw_emotion_marker(canvas, "!", pos=(1150, 250), size=140, angle=-12)
    bbox = canvas.getbbox()
    assert bbox is not None
    assert 1000 <= bbox[0] <= 1300
    assert 100 <= bbox[1] <= 400


def test_draw_emotion_marker_question():
    canvas = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw_emotion_marker(canvas, "?", pos=(1150, 250), size=140, angle=10)
    bbox = canvas.getbbox()
    assert bbox is not None
    assert 1000 <= bbox[0] <= 1300
    assert 100 <= bbox[1] <= 400


def test_create_backdrop_gradient():
    grad = create_backdrop_gradient((1920, 1080), fade_start_x=0, fade_end_x=980, max_alpha=0.65)
    assert grad.size == (1920, 1080)
    assert grad.mode == "RGBA"
    # Far left should be opaque (alpha around 165)
    left_pixel = grad.getpixel((10, 500))
    assert left_pixel[3] > 100
    # Far right should be completely transparent (alpha 0)
    right_pixel = grad.getpixel((1500, 500))
    assert right_pixel[3] == 0
