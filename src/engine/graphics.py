"""Graphic storytelling elements, badges, and gradient masks for thumbnails.
"""
import math
from typing import Tuple, Optional
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .text_thai import get_font

RED_COLOR = (236, 28, 36)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)


def draw_hand_drawn_circle(
    canvas: Image.Image,
    center: Tuple[int, int],
    radius: int,
    color: Tuple[int, int, int] = RED_COLOR,
    stroke_width: int = 12,
) -> None:
    """Draws an organic, imperfect hand-drawn brush loop with slight ovality and overlap."""
    cx, cy = center
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Generate points along an organic loop that overlaps itself
    points = []
    num_steps = 72
    total_angle = 2 * math.pi + 0.45  # slight overlap at ends
    for i in range(num_steps):
        theta = (i / (num_steps - 1)) * total_angle
        # Organic perturbation
        r_perturb = radius * (1.0 + 0.05 * math.sin(3 * theta) - 0.03 * math.cos(5 * theta))
        # Slight horizontal stretch to emulate quick hand-drawing
        x = cx + r_perturb * 1.08 * math.cos(theta - 0.2)
        y = cy + r_perturb * 0.94 * math.sin(theta - 0.2)
        points.append((x, y))

    # Draw thicker black outline for contrast against game backgrounds
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=(0, 0, 0, 220), width=stroke_width + 8)
    # Draw core red brush line
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=(*color, 255), width=stroke_width)

    # Soft drop shadow for depth
    shadow = overlay.filter(ImageFilter.GaussianBlur(6))
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(overlay)


def draw_emotion_marker(
    canvas: Image.Image,
    marker_type: str,
    pos: Tuple[int, int],
    size: int = 130,
    angle: float = -12,
    font_path: Optional[str] = None,
) -> None:
    """Draws a bold anime-style exclamation '!' or question '?' badge with drop shadow."""
    font = get_font(size, font_path)
    badge_w = size * 2
    badge_h = size * 2
    badge = Image.new("RGBA", (badge_w, badge_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)

    fill_color = (255, 46, 46, 255) if marker_type == "!" else (0, 229, 255, 255)
    center_xy = (badge_w // 2, badge_h // 2)

    # Thick black stroke
    draw.text(
        center_xy,
        marker_type,
        font=font,
        anchor="mm",
        fill=(0, 0, 0, 255),
        stroke_width=14,
        stroke_fill=(0, 0, 0, 255),
    )
    # Vibrant fill
    draw.text(
        center_xy,
        marker_type,
        font=font,
        anchor="mm",
        fill=fill_color,
        stroke_width=2,
        stroke_fill=(255, 255, 255, 200),
    )

    rotated = badge.rotate(angle, resample=Image.Resampling.BILINEAR, expand=True)
    # Soft drop shadow
    shadow = Image.new("RGBA", rotated.size, (0, 0, 0, 0))
    alpha = rotated.getchannel("A").filter(ImageFilter.GaussianBlur(8))
    shadow.putalpha(alpha.point(lambda p: round(p * 0.6)))

    paste_x = pos[0] - rotated.width // 2
    paste_y = pos[1] - rotated.height // 2
    canvas.alpha_composite(shadow, (paste_x + 8, paste_y + 10))
    canvas.alpha_composite(rotated, (paste_x, paste_y))


def create_backdrop_gradient(
    canvas_size: Tuple[int, int],
    fade_start_x: int = 0,
    fade_end_x: int = 980,
    max_alpha: float = 0.65,
    color: Tuple[int, int, int] = (4, 8, 20),
) -> Image.Image:
    """Creates a smooth horizontal gradient mask for the text zone (protects 0px unblurred footage)."""
    w, h = canvas_size
    gradient = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    grad_array = np.zeros((h, w, 4), dtype=np.uint8)

    # Compute alpha values along width
    alphas = np.zeros(w, dtype=np.float32)
    for x in range(w):
        if x <= fade_start_x:
            alphas[x] = max_alpha
        elif x >= fade_end_x:
            alphas[x] = 0.0
        else:
            t = (x - fade_start_x) / (fade_end_x - fade_start_x)
            # Smooth cosine curve
            alphas[x] = max_alpha * 0.5 * (1.0 + math.cos(math.pi * t))

    alpha_uint8 = np.clip(alphas * 255, 0, 255).astype(np.uint8)
    for c in range(3):
        grad_array[:, :, c] = color[c]
    grad_array[:, :, 3] = np.tile(alpha_uint8, (h, 1))

    return Image.fromarray(grad_array, mode="RGBA")


def apply_avatar_separation(
    avatar_img: Image.Image,
    stroke_width: int = 12,
    stroke_color: Tuple[int, int, int] = (255, 255, 255),
    shadow_offset: Tuple[int, int] = (10, 14),
    shadow_blur: int = 16,
    shadow_opacity: float = 0.7,
) -> Image.Image:
    """Applies a 5-layer separation (White/Accent Contour Stroke + Soft Drop Shadow) to an avatar."""
    if avatar_img.mode != "RGBA":
        avatar_img = avatar_img.convert("RGBA")

    w, h = avatar_img.size
    pad = stroke_width + shadow_blur * 2
    canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))

    # Alpha mask
    alpha = avatar_img.getchannel("A")
    alpha_arr = np.asarray(alpha, dtype=np.float32)

    # Stroke mask by dilation
    from .text_thai import _dilate
    stroke_mask_arr = _dilate(alpha_arr, stroke_width)
    stroke_mask = Image.fromarray(np.clip(stroke_mask_arr, 0, 255).astype(np.uint8), mode="L")

    # Drop shadow
    shadow_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    expanded_stroke = Image.new("L", canvas.size, 0)
    expanded_stroke.paste(stroke_mask, (pad + shadow_offset[0], pad + shadow_offset[1]))
    blurred_shadow = expanded_stroke.filter(ImageFilter.GaussianBlur(shadow_blur))
    shadow_alpha = blurred_shadow.point(lambda p: round(p * shadow_opacity))
    shadow_color = Image.new("RGBA", canvas.size, (0, 0, 0, 255))
    shadow_color.putalpha(shadow_alpha)

    # Stroke layer
    stroke_layer = Image.new("RGBA", canvas.size, (*stroke_color, 255))
    expanded_clean_stroke = Image.new("L", canvas.size, 0)
    expanded_clean_stroke.paste(stroke_mask, (pad, pad))
    stroke_layer.putalpha(expanded_clean_stroke)

    # Composite
    canvas.alpha_composite(shadow_color)
    canvas.alpha_composite(stroke_layer)
    canvas.paste(avatar_img, (pad, pad), avatar_img)

    return canvas
