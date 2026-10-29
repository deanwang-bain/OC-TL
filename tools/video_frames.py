#!/usr/bin/env python3
"""Pull the readable frames out of a mirrored meeting recording.

    python3 tools/video_frames.py <file.mp4> [-o DIR] [--threshold 0.25] [--max 40]
    python3 tools/video_frames.py <file.mp4> --at 04:40,1:31:58 [-o DIR]
    python3 tools/video_frames.py --list

The OI30 space records planning sessions as video and nothing else: the Sprint 3
and Sprint 4 planning sessions are thirteen `.mp4` files and about two hours, with
no written summary. Decisions taken in them are otherwise unreachable.

These are screen shares. The speech carries the argument, but the shared screen
carries the artefact -- the Sprint 4 backlog, with its user stories and acceptance
criteria, is on screen and written down nowhere else. The mirrored recordings have
no transcript, so this tool takes the screen; where a Teams `.vtt` sits beside the
video (the Sprint 5 workshops in `videos/`), `tools/transcript_text.py` reads the
speech.

By default it uses ffmpeg's scene-change filter rather than a fixed interval,
because a spreadsheet being scrolled for ten minutes is one frame worth reading,
not three hundred. Each surviving frame is a materially different view.

`--at` takes frames at given times instead, at full resolution. Scene detection
fails in one known way: on the 28 October workshop it spent its whole cap on Miro
zooms and caught almost none of fifty minutes of code walkthrough, where a dark
editor scrolling barely registers as a change. When a transcript says where the
screen is worth reading, ask for those moments directly.

ffmpeg is not in the base image. `pip install imageio-ffmpeg` provides a static
build and this finds it automatically; a system ffmpeg on PATH is used if present.
Nothing else in `tools/` needs it, and the daily sync does not run this.

Reading the frames still costs a model that can see them, one call each, so start
with `--max` low and raise it only if the sampled frames look worth more.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys

MIRROR_ATTACHMENTS = os.path.join("confluence", "_attachments")
# Recordings handed over directly rather than attached to a page. Gitignored.
LOCAL_VIDEOS = "videos"
DEFAULT_OUT = os.path.join("context", "video-frames")
STAMP = re.compile(r"^\d{1,2}(:\d{2}){1,2}$")


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
    for base in (MIRROR_ATTACHMENTS, LOCAL_VIDEOS):
        for root, _, files in os.walk(base):
            for name in sorted(files):
                if name.lower().endswith((".mp4", ".mov", ".m4v", ".webm")):
                    found.append(os.path.join(root, name))
    return sorted(found)


def at_times(exe: str, path: str, out_dir: str, stamps: list[str]) -> list[str]:
    """One full-resolution frame per timestamp, named after the time it was taken."""
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(path))[0]
    made = []
    for stamp in stamps:
        target = os.path.join(out_dir, f"{stem}-at-{stamp.replace(':', '')}.png")
        if os.path.exists(target):
            os.remove(target)  # so a failed seek cannot pass off an old frame as new
        result = subprocess.run(
            [exe, "-hide_banner", "-loglevel", "error", "-ss", stamp, "-i", path,
             "-frames:v", "1", target, "-y"],
            capture_output=True, text=True, check=False,
        )
        if result.returncode == 0 and os.path.exists(target):
            made.append(target)
        else:
            # A seek past the end exits cleanly and writes nothing.
            print(f"{stamp}: no frame ({result.stderr.strip() or 'past the end?'})",
                  file=sys.stderr)
    return made


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
    parser.add_argument("video", nargs="?", help="path to an .mp4 in the mirror or videos/")
    parser.add_argument("-o", "--out", default=DEFAULT_OUT)
    parser.add_argument("--threshold", type=float, default=0.15,
                        help="scene-change sensitivity, 0-1; lower keeps more (default 0.15, tuned on the planning recordings)")
    parser.add_argument("--max", type=int, default=40, help="frame cap (default 40)")
    parser.add_argument("--at", help="comma-separated times (MM:SS or H:MM:SS): full-resolution frames there instead of scene detection")
    parser.add_argument("--list", action="store_true", help="list recordings in the mirror and videos/")
    args = parser.parse_args(argv)

    stamps = [s.strip() for s in args.at.split(",") if s.strip()] if args.at else []
    bad = [s for s in stamps if not STAMP.match(s)]
    if bad:
        print(f"not a timestamp: {', '.join(bad)} (use MM:SS or H:MM:SS)", file=sys.stderr)
        return 1

    exe = ffmpeg()
    if args.list or not args.video:
        found = videos()
        print(f"{len(found)} recording(s) in the mirror and {LOCAL_VIDEOS}/:")
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

    if stamps:
        made = at_times(exe, args.video, args.out, stamps)
        print(f"{len(made)} of {len(stamps)} frame(s) -> {args.out}/")
        for path in made:
            print(f"  {path}")
        return 0 if len(made) == len(stamps) else 1

    made = extract(exe, args.video, args.out, args.threshold, args.max)
    print(f"{len(made)} frame(s) -> {args.out}/")
    print(f"index: {os.path.join(args.out, os.path.splitext(os.path.basename(args.video))[0] + '.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
