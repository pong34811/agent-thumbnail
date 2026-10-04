import pytest

from src.engine.shorts_titles import (
    canonical_title_from_timeline,
    fit_single_line_size,
    validate_title_parts,
)


@pytest.mark.parametrize(
    ("timeline_name", "expected"),
    [
        ("หนีฝ่าความหนาว_Minecraft-vdo_9x16", "หนีฝ่าความหนาว"),
        ("กองทัพโอลด์วัน_Terraria-vdo_9x16", "กองทัพโอลด์วัน"),
        ("เสียงสะท้อนสยองขวัญ_Soul Walker-vdo_9x16", "เสียงสะท้อนสยองขวัญ"),
        ("สุ่มปี่สก็อตเหล็ก_Monster Hunter World-vdo_9x16", "สุ่มปี่สก็อตเหล็ก"),
    ],
)
def test_canonical_title_strips_only_timeline_format_and_group_suffix(timeline_name, expected):
    assert canonical_title_from_timeline(timeline_name) == expected


def test_title_parts_preserve_full_title_and_allow_red_only_for_short_titles():
    validate_title_parts("คุยกับเพื่อน ลืมเสียง", "คุยกับเพื่อน ", "ลืมเสียง")
    validate_title_parts("คูลูยาคู", "คูลูยาคู", "")


@pytest.mark.parametrize(
    ("title", "red", "white"),
    [
        ("ชื่อคลิป", "ชื่อ", "คลิป\nเพิ่มอีกบรรทัด"),
        ("ชื่อคลิป", "ชื่ออื่น", "คลิป"),
        ("ชื่อคลิป", "", "ชื่อคลิป"),
    ],
)
def test_title_parts_reject_wrapped_or_incomplete_text(title, red, white):
    with pytest.raises(ValueError):
        validate_title_parts(title, red, white)


def test_fit_single_line_size_uses_largest_size_inside_range():
    measure = lambda text, size: len(text) * size
    assert fit_single_line_size("ab", 500, 150, 100, measure) == 150
    assert fit_single_line_size("ab", 250, 150, 100, measure) == 124
    assert fit_single_line_size("ab", 100, 150, 100, measure) is None


def test_fit_single_line_size_rejects_line_breaks():
    with pytest.raises(ValueError):
        fit_single_line_size("ชื่อ\nเพิ่ม", 500, 150, 100, lambda text, size: 1)
