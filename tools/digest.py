#!/usr/bin/env python3
"""Summarise what changed in the Confluence mirror since a given commit.

Emits markdown for the daily update: what moved, and what looks like it needs
the Tech Lead's attention. Intended to run straight after a sync commit.

    python3 tools/digest.py <base-ref> [<head-ref>]

Prints the digest to stdout. Exits 0 with a "no changes" digest when the range
is empty, so the caller decides whether that is worth sending.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

MIRROR = "confluence"

# Phrases that mean a page is unsettled. Matched case-insensitively against page
# titles and body text; each is something a Tech Lead would want to look at
# rather than a general-purpose keyword sweep.
ATTENTION_PATTERNS = [
    (r"\bto be signed off\b", "awaiting sign-off"),
    (r"\bupdate in progress\b", "in flux"),
    (r"\bTBD\b", "TBD"),
    (r"\bTBC\b", "to be confirmed"),
    (r"\bopen question", "open question"),
    (r"\bdecision needed\b", "decision needed"),
    (r"\bblocked\b", "blocked"),
    (r"\bpending .{0,30}review\b", "pending review"),
    (r"\bnot yet (decided|defined|agreed)\b", "undecided"),
]


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        print(f"git {' '.join(args)} failed: {result.stderr.strip()}", file=sys.stderr)
        return ""
    return result.stdout


def changed_files(base: str, head: str) -> dict[str, list[str]]:
    """Group changed mirror pages by git status letter."""
    raw = git("diff", "--name-status", f"{base}..{head}", "--", MIRROR)
    groups: dict[str, list[str]] = {"A": [], "M": [], "D": []}
    for line in raw.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status, path = parts[0][:1], parts[-1]
        if not path.endswith(".md") or path.endswith("INDEX.md"):
            continue
        groups.setdefault(status, []).append(path)
    return groups


def page_meta(path: str) -> tuple[str, str]:
    """Return (title, confluence_url) from a page's front matter."""
    try:
        with open(path, encoding="utf-8") as handle:
            head = handle.read(1200)
    except OSError:
        return os.path.basename(path), ""
    title = re.search(r'^title:\s*"(.*)"', head, re.M)
    url = re.search(r"^confluence_url:\s*(\S+)", head, re.M)
    return (
        title.group(1) if title else os.path.basename(path),
        url.group(1) if url else "",
    )


def link(path: str) -> str:
    title, url = page_meta(path)
    return f"[{title}]({url})" if url else title


def body_of(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as handle:
            return "\n".join(handle.read().split("\n")[11:])
    except OSError:
        return ""


def attention_flags(path: str) -> list[str]:
    text = f"{page_meta(path)[0]}\n{body_of(path)}"
    found = []
    for pattern, label in ATTENTION_PATTERNS:
        if re.search(pattern, text, re.I) and label not in found:
            found.append(label)
    return found


MEDIA = r"_\[[^\]]*\]_|!\[[^\]]*\]\([^)]*\)"


def classify(path: str) -> str:
    """One of: 'text', 'diagram-only', 'empty'.

    Stripping the media markup is what decides whether prose exists, so the
    check for media has to happen before that strip, not after.
    """
    body = body_of(path)
    has_media = bool(re.search(MEDIA, body))
    has_text = bool(re.sub(MEDIA, "", body).strip())
    if has_text:
        return "text"
    return "diagram-only" if has_media else "empty"


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    base, head = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "HEAD")

    groups = changed_files(base, head)
    added, modified, deleted = groups["A"], groups["M"], groups["D"]
    total = len(added) + len(modified) + len(deleted)

    out: list[str] = []
    if not total:
        out.append("No Confluence pages changed since the last update.")
        print("\n".join(out))
        return 0

    out.append(
        f"**{total} page{'s' if total != 1 else ''} changed** — "
        f"{len(added)} added, {len(modified)} updated, {len(deleted)} removed."
    )
    out.append("")

    # Attention first: this is the part worth reading if nothing else is.
    flagged: list[tuple[str, list[str]]] = []
    empty: list[str] = []
    diagram_only: list[str] = []
    for path in added + modified:
        if not os.path.exists(path):
            continue
        kind = classify(path)
        if kind == "empty":
            empty.append(path)
        elif kind == "diagram-only":
            diagram_only.append(path)
        flags = attention_flags(path)
        if flags:
            flagged.append((path, flags))

    if flagged or empty or deleted:
        out.append("## Needs attention")
        out.append("")
        for path, flags in flagged:
            out.append(f"- {link(path)} — {', '.join(flags)}")
        for path in empty:
            out.append(f"- {link(path)} — **page is empty** (no text, no diagram)")
        for path in deleted:
            title = os.path.basename(path).rsplit("-", 1)[0].replace("-", " ")
            out.append(f"- ~~{title}~~ — removed from Confluence")
        out.append("")

    if diagram_only:
        out.append("## Diagram only")
        out.append("")
        out.append("Content exists but carries no prose, so it will not turn up in a search.")
        out.append("")
        for path in sorted(diagram_only):
            out.append(f"- {link(path)}")
        out.append("")

    for label, paths in (("Added", added), ("Updated", modified)):
        if not paths:
            continue
        out.append(f"## {label}")
        out.append("")
        for path in sorted(paths):
            out.append(f"- {link(path)}")
        out.append("")

    return_code = 0
    print("\n".join(out).rstrip())
    return return_code


if __name__ == "__main__":
    sys.exit(main())
