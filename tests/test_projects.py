import pytest
from projects.aomi_debut.mapping import TIMELINES as AOMI_TL
from projects.tygarina.mapping import TIMELINES as TYGARINA_TL
from projects.armigon.mapping import TIMELINES as ARMIGON_TL, ACCENTS as ARMIGON_ACCENTS


def test_aomi_timelines():
    assert len(AOMI_TL) == 8
    for idx, tl in AOMI_TL.items():
        assert "title" in tl
        assert "land" in tl
        assert "short" in tl
        assert len(tl["land"]["hook"]) > 0


def test_tygarina_timelines():
    assert len(TYGARINA_TL) == 6
    for tl in TYGARINA_TL:
        assert "name" in tl
        assert "hook" in tl
        assert "sec" in tl
        assert len(tl["hook"]) > 0


def test_armigon_timelines():
    assert len(ARMIGON_TL) == 16
    for idx in range(1, 17):
        assert idx in ARMIGON_TL
        tl = ARMIGON_TL[idx]
        assert "avatar" in tl
        assert "game" in tl
        assert tl["game"] in ARMIGON_ACCENTS


def test_armigon_has_hooks_and_resolves_models():
    from cli.build import resolve_text
    from projects.armigon import mapping

    for tl in ARMIGON_TL.values():
        assert resolve_text(tl, "hook", "landscape")
        assert resolve_text(tl, "sec", "landscape")
    assert mapping.MODEL_DIR.endswith("armigon")
