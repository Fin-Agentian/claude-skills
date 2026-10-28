#!/usr/bin/env python3
"""QC for generated video clips: a contact sheet per clip plus scene-change detection.

A generated clip is meant to be one continuous shot, so any detected scene change inside it
usually means the model switched composition or spawned a duplicate person mid-clip.
Those timestamps tell you where to trim (cutting the bad part is faster than regenerating).

Usage:
    qc_sheet.py clip1.mp4 [clip2.mp4 ...] [--out-dir qc] [--threshold 0.3] [--cols 4 --rows 3]

Prints one JSON object per clip. Exit 0 = all clean, 1 = a clip has a mid-clip scene change,
2 = a clip could not be read (missing, empty, no video stream); the other clips are still checked.
Needs ffmpeg and ffprobe on PATH (or set FFMPEG / FFPROBE).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
FFPROBE = os.environ.get("FFPROBE", "ffprobe")
_PTS = re.compile(r"pts_time:([0-9.]+)")


def duration(video: Path) -> float:
    out = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def scene_changes(video: Path, threshold: float = 0.3) -> list[float]:
    """Timestamps (seconds) where the picture changes more than `threshold` (0-1)."""
    proc = subprocess.run(
        [FFMPEG, "-hide_banner", "-nostats", "-i", str(video),
         "-filter:v", f"select='gt(scene,{threshold})',showinfo", "-an", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    )
    return [round(float(m), 3) for m in _PTS.findall(proc.stderr)]


def contact_sheet(video: Path, out: Path, cols: int = 4, rows: int = 3, width: int = 320) -> Path:
    """Evenly spaced frames tiled into one image, to eyeball drift, duplicates and text."""
    frames = cols * rows
    rate = frames / max(duration(video), 0.1)
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(video),
         "-vf", f"fps={rate:.6f},scale={width}:-2,tile={cols}x{rows}",
         "-frames:v", "1", str(out)],
        check=True,
    )
    return out


def check(video: Path, out_dir: Path, threshold: float, cols: int, rows: int) -> dict:
    sheet = contact_sheet(video, out_dir / f"{video.stem}_sheet.jpg", cols, rows)
    cuts = scene_changes(video, threshold)
    return {
        "clip": str(video),
        "duration_sec": round(duration(video), 3),
        "scene_changes_sec": cuts,
        "suspect": bool(cuts),
        "sheet": str(sheet),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("clips", nargs="+", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("qc"))
    parser.add_argument("--threshold", type=float, default=0.3,
                        help="scene score 0-1; lower finds subtler changes (default 0.3)")
    parser.add_argument("--cols", type=int, default=4)
    parser.add_argument("--rows", type=int, default=3)
    args = parser.parse_args(argv)
    suspect = failed = False
    for clip in args.clips:
        try:
            result = check(clip, args.out_dir, args.threshold, args.cols, args.rows)
            suspect |= result["suspect"]
        except (subprocess.CalledProcessError, ValueError, OSError) as exc:
            failed = True
            result = {"clip": str(clip), "error": f"cannot read: {type(exc).__name__}"}
        print(json.dumps(result, ensure_ascii=False))
    return 2 if failed else 1 if suspect else 0


if __name__ == "__main__":
    sys.exit(main())
