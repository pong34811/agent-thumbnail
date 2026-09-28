import pytest
from PIL import Image
from graphics_overlay import draw_hand_drawn_circle, draw_emotion_marker

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
    assert 1050 <= bbox[0] <= 1250
    assert 150 <= bbox[1] <= 350

def test_draw_emotion_marker_question():
    canvas = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw_emotion_marker(canvas, "?", pos=(1150, 250), size=140, angle=10)
    bbox = canvas.getbbox()
    assert bbox is not None
    assert 1050 <= bbox[0] <= 1250
    assert 150 <= bbox[1] <= 350
