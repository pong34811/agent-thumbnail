"""High-level thumbnail compositing pipeline.
"""
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

from PIL import Image, ImageEnhance, ImageFilter

from .layout import LANDSCAPE_DIMS, SHORTS_DIMS, LandscapeLayout, ShortsLayout
from .text_thai import fit_text, render_thai_lines
from .graphics import (
    draw_hand_drawn_circle,
    draw_emotion_marker,
    create_backdrop_gradient,
    apply_avatar_separation,
    RED_COLOR,
    WHITE_COLOR,
    BLACK_COLOR,
)


class ThumbnailCompositor:
    """Orchestrates compositing of background, avatar, typography, and graphic drama accents."""

    def __init__(self, font_path: Optional[str] = None):
        self.font_path = font_path

    def composite_landscape(
        self,
        bg_image: Image.Image,
        avatar_image: Optional[Image.Image] = None,
        hook_lines: Optional[List[str]] = None,
        secondary_lines: Optional[List[str]] = None,
        avatar_pos: Optional[Tuple[int, int]] = None,
        focus_circle: Optional[Tuple[int, int, int]] = None,  # (cx, cy, radius)
        emotion_marker: Optional[Tuple[str, Tuple[int, int]]] = None,  # ("!" or "?", (x, y))
        is_gameplay: bool = True,
        blur_radius: int = 0,
        brightness: float = 0.90,
        contrast: float = 1.08,
    ) -> Image.Image:
        """Builds a 1920x1080 Landscape thumbnail."""
        canvas = bg_image.convert("RGBA").resize(LANDSCAPE_DIMS, Image.Resampling.LANCZOS)

        # Background processing
        if is_gameplay:
            if brightness != 1.0:
                canvas = ImageEnhance.Brightness(canvas).enhance(brightness)
            if contrast != 1.0:
                canvas = ImageEnhance.Contrast(canvas).enhance(contrast)
            if blur_radius > 0:
                canvas = canvas.filter(ImageFilter.GaussianBlur(blur_radius))
            # Left gradient mask to ensure text readability without blurring gameplay
            grad = create_backdrop_gradient(LANDSCAPE_DIMS, fade_start_x=0, fade_end_x=980, max_alpha=0.65)
            canvas.alpha_composite(grad)
        else:
            # Talk/Chat/Debut: heavy blur and dim
            canvas = canvas.filter(ImageFilter.GaussianBlur(blur_radius or 50))
            dim = Image.new("RGBA", LANDSCAPE_DIMS, (0, 0, 0, 128))
            canvas.alpha_composite(dim)

        # Draw focus circle on gameplay incident if specified
        if focus_circle:
            cx, cy, r = focus_circle
            draw_hand_drawn_circle(canvas, (cx, cy), r, color=RED_COLOR)

        # Place avatar on right side if provided
        if avatar_image:
            av_with_effects = apply_avatar_separation(avatar_image)
            if avatar_pos is None:
                # Default right-aligned placement
                av_x = LANDSCAPE_DIMS[0] - av_with_effects.width + 60
                av_y = LANDSCAPE_DIMS[1] - av_with_effects.height
                avatar_pos = (av_x, av_y)
            canvas.alpha_composite(av_with_effects, avatar_pos)

        # Draw emotion marker near avatar head if specified
        if emotion_marker:
            m_type, m_pos = emotion_marker
            draw_emotion_marker(canvas, m_type, m_pos, font_path=self.font_path)

        # Render Thai text on Center-Left
        text_layer = Image.new("RGBA", LANDSCAPE_DIMS, (0, 0, 0, 0))
        y_cursor = 380

        if hook_lines:
            f_hook, s_hook = fit_text(
                hook_lines,
                max_w=LandscapeLayout.TEXT_MAX_WIDTH,
                start_size=165,
                min_size=120,
                stroke_ratio=0.08,
                font_path=self.font_path,
            )
            hook_rendered = render_thai_lines(
                LANDSCAPE_DIMS,
                (LandscapeLayout.TEXT_X_MIN, y_cursor),
                hook_lines,
                f_hook,
                fill_color=RED_COLOR,
                stroke_color=BLACK_COLOR,
                stroke_width=s_hook,
            )
            text_layer.alpha_composite(hook_rendered)
            y_cursor += len(hook_lines) * round(f_hook.size * 1.15) + 20

        if secondary_lines:
            f_sec, s_sec = fit_text(
                secondary_lines,
                max_w=LandscapeLayout.TEXT_MAX_WIDTH,
                start_size=95,
                min_size=70,
                stroke_ratio=0.08,
                font_path=self.font_path,
            )
            sec_rendered = render_thai_lines(
                LANDSCAPE_DIMS,
                (LandscapeLayout.TEXT_X_MIN, y_cursor),
                secondary_lines,
                f_sec,
                fill_color=WHITE_COLOR,
                stroke_color=BLACK_COLOR,
                stroke_width=s_sec,
            )
            text_layer.alpha_composite(sec_rendered)

        canvas.alpha_composite(text_layer)
        return canvas.convert("RGB")

    def composite_shorts(
        self,
        bg_image: Image.Image,
        avatar_image: Optional[Image.Image] = None,
        hook_lines: Optional[List[str]] = None,
        secondary_lines: Optional[List[str]] = None,
        emotion_marker: Optional[Tuple[str, Tuple[int, int]]] = None,
        brightness: float = 0.90,
        text_y: int = ShortsLayout.TEXT_Y_START,
        avatar_height: Optional[int] = None,
        avatar_pos: Optional[Tuple[int, int]] = None,
        three_tier: bool = False,
        game_panel_crop: Optional[Tuple[int, int, int, int]] = None,
        game_panel_y: int = 610,
    ) -> Image.Image:
        """Builds a 1080x1920 Shorts thumbnail with support for 3-tier architecture."""
        if three_tier or bg_image.width > bg_image.height:
            ambient = bg_image.convert("RGBA").resize(SHORTS_DIMS, Image.Resampling.LANCZOS)
            ambient = ambient.filter(ImageFilter.GaussianBlur(ShortsLayout.AMBIENT_BLUR_RADIUS))
            ambient = ImageEnhance.Brightness(ambient).enhance(ShortsLayout.AMBIENT_BRIGHTNESS)
            ambient = ImageEnhance.Color(ambient).enhance(ShortsLayout.AMBIENT_COLOR)

            panel_w, panel_h = ShortsLayout.GAME_PANEL_DIMS[0], 612
            if game_panel_crop:
                panel_crop = bg_image.crop(game_panel_crop).resize((panel_w, panel_h), Image.Resampling.LANCZOS)
            else:
                panel_crop = bg_image.resize((panel_w, panel_h), Image.Resampling.LANCZOS)

            panel_canvas = Image.new("RGBA", (panel_w, panel_h), (0, 0, 0, 0))
            panel_canvas.paste(panel_crop.convert("RGBA"), (0, 0))
            from PIL import ImageDraw
            draw = ImageDraw.Draw(panel_canvas)
            draw.line([(0, 0), (panel_w, 0)], fill=(255, 255, 255, 220), width=4)
            draw.line([(0, panel_h - 2), (panel_w, panel_h - 2)], fill=(255, 255, 255, 220), width=4)

            ambient.alpha_composite(panel_canvas, (0, game_panel_y))
            canvas = ambient
        else:
            canvas = bg_image.convert("RGBA").resize(SHORTS_DIMS, Image.Resampling.LANCZOS)
            if brightness != 1.0:
                canvas = ImageEnhance.Brightness(canvas).enhance(brightness)

        # Place avatar in bottom half, horizontally centered
        if avatar_image:
            if avatar_height is not None:
                bbox = avatar_image.split()[3].getbbox() if avatar_image.mode == "RGBA" else None
                if bbox:
                    avatar_image = avatar_image.crop(bbox)
                w = round(avatar_image.width * avatar_height / avatar_image.height)
                avatar_image = avatar_image.resize((w, avatar_height), Image.Resampling.LANCZOS)

            av_with_effects = apply_avatar_separation(avatar_image)
            if avatar_pos is None:
                av_x = (SHORTS_DIMS[0] - av_with_effects.width) // 2
                av_y = SHORTS_DIMS[1] - av_with_effects.height
                avatar_pos = (av_x, av_y)
            canvas.alpha_composite(av_with_effects, avatar_pos)

        if emotion_marker:
            m_type, m_pos = emotion_marker
            draw_emotion_marker(canvas, m_type, m_pos, font_path=self.font_path)

        # Render Thai text in upper half, centered horizontally
        text_layer = Image.new("RGBA", SHORTS_DIMS, (0, 0, 0, 0))
        y_cursor = text_y

        if hook_lines:
            f_hook, s_hook = fit_text(
                hook_lines,
                max_w=ShortsLayout.TEXT_MAX_WIDTH,
                start_size=150,
                min_size=100,
                stroke_ratio=0.08,
                font_path=self.font_path,
            )
            hook_rendered = render_thai_lines(
                SHORTS_DIMS,
                (ShortsLayout.CENTER_X, y_cursor),
                hook_lines,
                f_hook,
                fill_color=RED_COLOR,
                stroke_color=BLACK_COLOR,
                stroke_width=s_hook,
                anchor="ms",
            )
            text_layer.alpha_composite(hook_rendered)
            y_cursor += len(hook_lines) * round(f_hook.size * 1.15) + 20

        if secondary_lines:
            f_sec, s_sec = fit_text(
                secondary_lines,
                max_w=ShortsLayout.TEXT_MAX_WIDTH,
                start_size=90,
                min_size=60,
                stroke_ratio=0.08,
                font_path=self.font_path,
            )
            sec_rendered = render_thai_lines(
                SHORTS_DIMS,
                (ShortsLayout.CENTER_X, y_cursor),
                secondary_lines,
                f_sec,
                fill_color=WHITE_COLOR,
                stroke_color=BLACK_COLOR,
                stroke_width=s_sec,
                anchor="ms",
            )
            text_layer.alpha_composite(sec_rendered)

        canvas.alpha_composite(text_layer)
        return canvas.convert("RGB")
