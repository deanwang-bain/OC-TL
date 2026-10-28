#!/usr/bin/env python3
"""Pull the readable frames out of a mirrored meeting recording.

    python3 tools/video_frames.py <file.mp4> [-o DIR] [--threshold 0.25] [--max 40]
    python3 tools/video_frames.py --list

The OI30 space records planning sessions as video and nothing else: the Sprint 3
and Sprint 4 planning sessions are thirteen `.mp4` files and about two hours, with
no written summary. Decisions taken in them are otherwise unreachable.

These are screen shares. The speech carries the argument, but the shared screen
carries the artefact -- the Sprint 4 backlog, with its user stories and acceptance
criteria, is on screen and written down nowhere else. There is no speech-to-text
here, so this tool takes the screen.

It uses ffmpeg's scene-change filter rather than a fixed interval, because a
spreadsheet being scrolled for ten minutes is one frame worth reading, not three
hundred. Each surviving frame is a materially different view.

ffmpeg is not in the base image. `pip install imageio-ffmpeg` provides a static
build and this finds it automatically; a system ffmpeg on PATH is used if present.
Nothing else in `tools/` needs it, and the daily sync does not run this.

Reading the frames still costs a model that can see them, one call each, so start
with `--max` low and raise it only if the sampled frames look worth more.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys

MIRROR_ATTACHMENTS = os.path.join("confluence", "_attachments")
DEFAULT_OUT = os.path.join("context", "video-frames")


def ffmpeg() -> str | None:
    """A usable ffmpeg: the bundled wheel first, then PATH."""
    try:
        import imageio_ffmpeg

        path = imageio_ffmpeg.get_ffmpeg_exe()
        if path and os.path.exists(path):
            return path
    except ImportError:
        pass
    return shutil.which("ffmpeg")


def duration(exe: str, path: str) -> str:
    result = subprocess.run([exe, "-hide_banner", "-i", path],
                            capture_output=True, text=True, check=False)
    for line in result.stderr.splitlines():
        if "Duration:" in line:
            return line.strip().split("Duration:")[1].split(",")[0].strip()
    return "unknown"


def videos() -> list[str]:
    found = []
    for root, _, files in os.walk(MIRROR_ATTACHMENTS):
        for name in sorted(files):
            if name.lower().endswith((".mp4", ".mov", ".m4v", ".webm")):
                found.append(os.path.join(root, name))
    return sorted(found)


def extract(exe: str, path: str, out_dir: str, threshold: float, limit: int) -> list[str]:
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(path))[0]
    pattern = os.path.join(out_dir, f"{stem}-%03d.png")
    # `select` keeps scene changes; `showinfo` prints each kept frame's timestamp
    # to stderr, which is the only way to know where in the recording it came from.
    command = [
        exe, "-hide_banner", "-loglevel", "info", "-i", path,
        "-vf", f"select='gt(scene,{threshold})',showinfo,scale=1280:-1",
        "-vsync", "vfr", "-frames:v", str(limit), pattern, "-y",
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    times = []
    for line in result.stderr.splitlines():
        if "pts_time:" in line:
            raw = line.split("pts_time:")[1].split()[0]
            try:
                seconds = float(raw)
            except ValueError:
                continue
            times.append(f"{int(seconds) // 60:02d}:{int(seconds) % 60:02d}")
    made = sorted(f for f in os.listdir(out_dir) if f.startswith(stem) and f.endswith(".png"))
    index = os.path.join(out_dir, f"{stem}.md")
    with open(index, "w", encoding="utf-8") as handle:
        handle.write(f"# Frames from {os.path.basename(path)}\n\n")
        handle.write(f"Source: `{path}` ({duration(exe, path)})\n\n")
        handle.write(f"Scene-change frames, threshold {threshold}, capped at {limit}.\n")
        handle.write("Timestamps are where each frame appears in the recording.\n\n")
        for i, name in enumerate(made):
            when = times[i] if i < len(times) else "?"
            handle.write(f"- `{name}` — {when}\n")
    return made


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("video", nargs="?", help="path to an .mp4 in the mirror")
    parser.add_argument("-o", "--out", default=DEFAULT_OUT)
    parser.add_argument("--threshold", type=float, default=0.15,
                        help="scene-change sensitivity, 0-1; lower keeps more (default 0.15, tuned on the planning recordings)")
    parser.add_argument("--max", type=int, default=40, help="frame cap (default 40)")
    parser.add_argument("--list", action="store_true", help="list recordings in the mirror")
    args = parser.parse_args(argv)

    exe = ffmpeg()
    if args.list or not args.video:
        found = videos()
        print(f"{len(found)} recording(s) in the mirror:")
        for path in found:
            length = duration(exe, path) if exe else "?"
            print(f"  {length}  {path}")
        if not exe:
            print("\nffmpeg not found -- `pip install imageio-ffmpeg` to extract frames.",
                  file=sys.stderr)
        return 0

    if exe is None:
        print("ffmpeg not found. Install it with `pip install imageio-ffmpeg`.", file=sys.stderr)
        return 1
    if not os.path.exists(args.video):
        print(f"no such file: {args.video}", file=sys.stderr)
        return 1

    made = extract(exe, args.video, args.out, args.threshold, args.max)
    print(f"{len(made)} frame(s) -> {args.out}/")
    print(f"index: {os.path.join(args.out, os.path.splitext(os.path.basename(args.video))[0] + '.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
