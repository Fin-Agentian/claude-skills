"""Run with: python -m pytest scripts/test_qc_sheet.py (needs ffmpeg on PATH)."""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import qc_sheet

pytestmark = pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg not installed")


def _clip(path: Path, *sources: str) -> Path:
    """Concatenate 2-second lavfi sources into one 24 fps clip."""
    args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for src in sources:
        sep = ":" if "=" in src else "="
        args += ["-f", "lavfi", "-t", "2", "-i", f"{src}{sep}size=320x180:rate=24"]
    n = len(sources)
    chain = "".join(f"[{i}:v]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
    subprocess.run(args + ["-filter_complex", chain, "-map", "[v]", str(path)], check=True)
    return path


def test_steady_clip_has_no_scene_change(tmp_path):
    clip = _clip(tmp_path / "steady.mp4", "testsrc")
    assert qc_sheet.scene_changes(clip) == []
    assert qc_sheet.duration(clip) == pytest.approx(2.0, abs=0.1)


def test_hard_change_is_found_near_the_cut(tmp_path):
    clip = _clip(tmp_path / "drift.mp4", "testsrc", "color=c=red")
    cuts = qc_sheet.scene_changes(clip)
    assert len(cuts) == 1 and cuts[0] == pytest.approx(2.0, abs=0.1)


def test_contact_sheet_and_cli(tmp_path, capsys):
    good = _clip(tmp_path / "good.mp4", "testsrc")
    bad = _clip(tmp_path / "bad.mp4", "testsrc", "color=c=blue")
    out = tmp_path / "qc"
    assert qc_sheet.main([str(good), "--out-dir", str(out)]) == 0
    assert qc_sheet.main([str(good), str(bad), "--out-dir", str(out), "--cols", "3",
                          "--rows", "2"]) == 1
    lines = [json.loads(x) for x in capsys.readouterr().out.splitlines()]
    assert [x["suspect"] for x in lines] == [False, False, True]
    sheet = Path(lines[-1]["sheet"])
    assert sheet.exists() and sheet.stat().st_size > 0


def test_unreadable_clip_is_reported_and_others_still_run(tmp_path, capsys):
    good = _clip(tmp_path / "good.mp4", "testsrc")
    broken = tmp_path / "broken.mp4"
    broken.write_bytes(b"not a video")
    out = tmp_path / "qc"
    code = qc_sheet.main([str(tmp_path / "missing.mp4"), str(broken), str(good),
                          "--out-dir", str(out)])
    assert code == 2
    lines = [json.loads(x) for x in capsys.readouterr().out.splitlines()]
    assert "error" in lines[0] and "error" in lines[1]
    assert lines[2]["suspect"] is False
