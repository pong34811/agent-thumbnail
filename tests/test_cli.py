import json
import zipfile

from PIL import Image

from cli import organize, package, verify
from cli.build import resolve_text
from cli.doctor import run_checks


def _jpg(path, size=(1920, 1080)):
    Image.new("RGB", size, (10, 20, 30)).save(path, quality=90)


def test_resolve_text_prefers_nested_orientation_block():
    tl = {"land": {"hook": ["A"], "sec": ["B"]}, "short": {"hook": ["C"]}}
    assert resolve_text(tl, "hook", "landscape") == ["A"]
    assert resolve_text(tl, "sec", "landscape") == ["B"]
    assert resolve_text(tl, "hook", "shorts") == ["C"]


def test_resolve_text_top_level_and_title_fallback():
    assert resolve_text({"hook": "X"}, "hook", "landscape") == ["X"]
    assert resolve_text({"title": "01 Peak - ช่วยโฮชิ"}, "hook", "landscape") == ["ช่วยโฮชิ"]
    assert resolve_text({"title": "plain"}, "hook", "landscape") is None


def test_sync_latest_skips_empty_newer_batch(tmp_path, monkeypatch):
    monkeypatch.setattr(organize, "OUTPUTS_DIR", tmp_path)
    ch = tmp_path / "chan"
    (ch / "2026-01-01").mkdir(parents=True)
    (ch / "2026-02-01").mkdir()
    (ch / "notes").mkdir()
    _jpg(ch / "2026-01-01" / "a.jpg")
    organize.sync_channel_latest("chan")
    assert [p.name for p in (ch / "_LATEST").iterdir()] == ["a.jpg"]


def test_verify_flags_manifest_entry_missing_on_disk(tmp_path):
    _jpg(tmp_path / "a.jpg")
    manifest = tmp_path / "m.json"
    manifest.write_text(json.dumps([{"file": "a.jpg"}, {"file": "gone.jpg"}]), encoding="utf-8")
    report = verify.verify_directory(str(tmp_path), str(manifest))
    assert report["status"] == "FAIL"
    assert any("gone.jpg" in note for note in report["manifest_notes"])


def test_package_roundtrip(tmp_path):
    _jpg(tmp_path / "a.jpg")
    result = package.package_delivery(str(tmp_path), str(tmp_path / "m.json"), str(tmp_path / "out" / "p.zip"))
    assert result["status"] == "VERIFIED_PASS" and result["total_images"] == 1
    assert "a.jpg" in zipfile.ZipFile(tmp_path / "out" / "p.zip").namelist()


def test_doctor_reports_required_dependencies():
    names = {name for name, *_ in run_checks()}
    assert {"Pillow", "libraqm (Thai layout)", "Mitr-Bold font"} <= names
