from pathlib import Path
from build_armigon_covers_v3 import TIMELINE_CONFIG, AVATAR_DIR

def test_all_16_timelines_configured():
    assert len(TIMELINE_CONFIG) == 16
    for idx in range(1, 17):
        assert idx in TIMELINE_CONFIG, f"Timeline index {idx} missing from config"
        cfg = TIMELINE_CONFIG[idx]
        avatar_path = AVATAR_DIR / cfg["avatar"]
        assert avatar_path.exists(), f"Missing avatar file: {avatar_path}"
        if cfg.get("focus_circle"):
            cx, cy, r = cfg["focus_circle"]
            assert 0 < cx < 1920 and 0 < cy < 1080 and r > 30
        if cfg.get("emotion_marker"):
            m_type, (mx, my) = cfg["emotion_marker"]
            assert m_type in ["!", "?"]
            assert 0 < mx < 1920 and 0 < my < 1080

def test_avatar_expression_diversity():
    used_avatars = {cfg["avatar"] for cfg in TIMELINE_CONFIG.values()}
    # All 6 avatar expressions must be utilized
    expected = {"cry.png", "angry.png", "hello.png", "great.png", "sadistic.png", "adore.png"}
    assert used_avatars == expected
