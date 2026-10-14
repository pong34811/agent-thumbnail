"""Project mapping for LuminaVProject demo covers with clean custom key visuals.
"""
from pathlib import Path

PROJECT_NAME = "lumina-demo"
CHARACTER_NAME = "lumina"

MODEL_DIR = str(Path(__file__).resolve().parents[2] / "scratch")

ACCENTS = {
    "First Myth": (220, 38, 38),
    "Mutelu": (234, 179, 8),
}

TIMELINES = {
    1: {
        "title": "01 Draki Kona - มังกรตื่นแล้ว!",
        "hook": ["มังกรตื่นแล้ว!"],
        "sec": ["หนีไม่ทันแน่"],
        "unit": "First Myth",
        "member": "Draki Kona",
        "avatar": "draki_avatar_cutout.png",
        "bg": r"C:\Users\warit\.gemini\antigravity\brain\cfb54a3b-7604-4891-862b-dde107a7d811\minecraft_dragon_arena_bg_1791952135325.jpg",
        "bg_short": r"C:\Users\warit\.gemini\antigravity\brain\cfb54a3b-7604-4891-862b-dde107a7d811\gothic_dungeon_background_1791952145680.jpg",
        "focus_circle": (1330, 240, 130),
        "emotion_marker": ("!", (1350, 120)),
    },
    2: {
        "title": "02 Draki Kona - อย่าเปิดประตู!",
        "hook": ["อย่าเปิดประตู!"],
        "sec": ["ข้างในมีคำสาป"],
        "unit": "First Myth",
        "member": "Draki Kona",
        "avatar": "draki_avatar_cutout.png",
        "bg": r"C:\Users\warit\.gemini\antigravity\brain\cfb54a3b-7604-4891-862b-dde107a7d811\gothic_dungeon_background_1791952145680.jpg",
        "bg_short": r"C:\Users\warit\.gemini\antigravity\brain\cfb54a3b-7604-4891-862b-dde107a7d811\gothic_dungeon_background_1791952145680.jpg",
        "focus_circle": (540, 480, 140),
        "emotion_marker": ("?", (1350, 120)),
    },
}
