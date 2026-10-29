#!/usr/bin/env python3
"""Turn a meeting transcript (.vtt) into one readable line per utterance.

    python3 tools/transcript_text.py <file.vtt> [...]     # print transcript
    python3 tools/transcript_text.py --list               # transcripts in the repo

The Sprint 5 workshops arrive as Teams recordings with a WebVTT transcript beside
the .mp4. Teams splits each utterance into several cues sharing one id prefix
(`<uuid>-0`, `<uuid>-1`, ...), which makes the raw file about twice the size of
the speech and hard to read. This joins them back up and stamps each utterance
with its start time, so the result can be read straight through and every claim
pointed back at a moment in the recording -- where `tools/video_frames.py --at`
then fetches what was on screen.

Teams transcripts carry no speaker labels unless the meeting had them on; when a
cue does carry a `<v Name>` voice tag it is kept. The captions are automatic, so
names and product terms come out garbled ("Port Key" for Portkey, "intro ID" for
Entra ID) -- check anything load-bearing against the screen.

Stdlib only, like the rest of `tools/`.
"""

from __future__ import annotations

import os
import re
import sys

SEARCH = ("videos", os.path.join("confluence", "_attachments"))
CUE_ID = re.compile(r"^(?P<utt>[0-9a-fA-F-]{36})-\d+$")
TIMING = re.compile(r"^(\d{2}:)?(\d{2}):(\d{2})\.\d{3}\s+-->")
VOICE = re.compile(r"<v\s+([^>]+)>")
TAG = re.compile(r"</?[^>]+>")


def utterances(path: str) -> list[tuple[str, str, str]]:
    """(start, speaker, text) per utterance, fragments of one utterance joined."""
    with open(path, encoding="utf-8-sig") as handle:
        blocks = handle.read().replace("\r\n", "\n").split("\n\n")
    out: list[tuple[str, str, str]] = []
    last_key = None
    for block in blocks:
        lines = [line for line in block.split("\n") if line.strip()]
        timing = next((i for i, line in enumerate(lines) if TIMING.match(line)), None)
        if timing is None:
            continue  # the WEBVTT header, NOTE and STYLE blocks
        match = CUE_ID.match(lines[timing - 1]) if timing else None
        key = match.group("utt") if match else None
        hours, minutes, seconds = TIMING.match(lines[timing]).groups()
        start = f"{(hours or '00:')}{minutes}:{seconds}"
        raw = " ".join(lines[timing + 1:])
        voice = VOICE.search(raw)
        speaker = voice.group(1).strip() if voice else ""
        text = re.sub(r"\s+", " ", TAG.sub("", raw)).strip()
        if key is not None and key == last_key and out:
            first, who, said = out[-1]
            out[-1] = (first, who, f"{said} {text}")
        else:
            out.append((start, speaker, text))
        last_key = key
    return out


def render(path: str) -> str:
    rows = []
    for start, speaker, text in utterances(path):
        rows.append(f"[{start}] {speaker + ': ' if speaker else ''}{text}")
    return "\n".join(rows)


def listing() -> int:
    found = []
    for base in SEARCH:
        for root, _, files in os.walk(base):
            found.extend(os.path.join(root, name) for name in sorted(files)
                         if name.lower().endswith(".vtt"))
    print(f"{len(found)} transcript(s):")
    for path in sorted(found):
        count = len(utterances(path))
        print(f"  {count:>5} utterances  {path}")
    return 0


def main(argv: list[str]) -> int:
    if not argv or "--list" in argv:
        return listing()
    status = 0
    for path in argv:
        if len(argv) > 1:
            print(f"\n######## {path}")
        try:
            print(render(path))
        except (OSError, UnicodeDecodeError) as exc:
            print(f"{path}: could not read ({exc})", file=sys.stderr)
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
