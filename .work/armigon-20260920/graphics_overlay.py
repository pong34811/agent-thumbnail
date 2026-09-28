import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_PATH = Path(r"D:\agent-thumbnail\outputs\timeline-covers\fonts\Mitr-Bold.ttf")

def draw_hand_drawn_circle(canvas: Image.Image, center: tuple[int, int], radius: int, color=(236, 28, 36), stroke_width=12):
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
        draw.line([points[i], points[i+1]], fill=(0, 0, 0, 220), width=stroke_width + 8)
    # Draw core red brush line
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=(*color, 255), width=stroke_width)
        
    # Soft drop shadow for depth
    shadow = overlay.filter(ImageFilter.GaussianBlur(6))
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(overlay)

def draw_emotion_marker(canvas: Image.Image, marker_type: str, pos: tuple[int, int], size=130, angle=-12):
    """Draws a bold anime-style exclamation '!' or question '?' badge with drop shadow."""
    if not FONT_PATH.exists():
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(str(FONT_PATH), size)
        
    badge_w = size * 2
    badge_h = size * 2
    badge = Image.new("RGBA", (badge_w, badge_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    
    fill_color = (255, 46, 46, 255) if marker_type == "!" else (0, 229, 255, 255)
    center_xy = (badge_w // 2, badge_h // 2)
    
    # Thick black stroke
    draw.text(center_xy, marker_type, font=font, anchor="mm",
              fill=(0, 0, 0, 255), stroke_width=14, stroke_fill=(0, 0, 0, 255))
    # Vibrant fill
    draw.text(center_xy, marker_type, font=font, anchor="mm",
              fill=fill_color, stroke_width=2, stroke_fill=(255, 255, 255, 200))
              
    rotated = badge.rotate(angle, resample=Image.Resampling.BILINEAR, expand=True)
    # Soft drop shadow
    shadow = Image.new("RGBA", rotated.size, (0, 0, 0, 0))
    alpha = rotated.getchannel("A").filter(ImageFilter.GaussianBlur(8))
    shadow.putalpha(alpha.point(lambda p: round(p * 0.6)))
    
    paste_x = pos[0] - rotated.width // 2
    paste_y = pos[1] - rotated.height // 2
    canvas.alpha_composite(shadow, (paste_x + 8, paste_y + 10))
    canvas.alpha_composite(rotated, (paste_x, paste_y))
