#!/usr/bin/env python3
"""Detect where the distilled layer in `context/` has fallen behind the mirror.

The digest reports what changed in Confluence. This reports something different:
where *our own notes* have gone stale relative to it. Every check here exists
because the corresponding mistake was actually made — a page read as empty when
its content was an attachment, a model provider named in prose that no position
table mentioned, a standing agenda still asking for things the team had settled.

    python3 tools/drift.py

Prints a markdown section, or nothing at all when there is no drift, so the
caller can append it unconditionally.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys

MIRROR = "confluence"
CONTEXT = "context"
AGENDA = os.path.join(CONTEXT, "standing-agenda.md")
ROOT_DOC = "CLAUDE.md"
REGISTER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "known_tools.json")

MEDIA = r"_\[[^\]]*\]_|!\[[^\]]*\]\([^)]*\)|\[[^\]]*\]\([^)]*_attachments[^)]*\)"

# Providers whose appearance anywhere is a governance question. Kept in step with
# the same list in digest.py.
PROVIDERS = [
    "OpenAI", "ChatGPT", "GPT-4", "GPT-5", "Gemini", "Vertex AI", "Bedrock",
    "Mistral", "Cohere", "Hugging Face", "Perplexity",
]


def pages() -> list[str]:
    found = []
    for root, dirs, files in os.walk(MIRROR):
        dirs[:] = [d for d in dirs if d != "_attachments"]
        for name in files:
            if name.endswith(".md") and name != "INDEX.md":
                found.append(os.path.join(root, name))
    return sorted(found)


def page_id(path: str) -> str:
    match = re.search(r"-(\d+)\.md$", path)
    return match.group(1) if match else ""


def meta(path: str) -> tuple[str, str]:
    try:
        head = open(path, encoding="utf-8").read(1200)
    except OSError:
        return os.path.basename(path), ""
    title = re.search(r'^title:\s*"(.*)"', head, re.M)
    url = re.search(r"^confluence_url:\s*(\S+)", head, re.M)
    return (title.group(1) if title else os.path.basename(path),
            url.group(1) if url else "")


def link(path: str) -> str:
    title, url = meta(path)
    return f"[{title}]({url})" if url else title


def body(path: str) -> str:
    try:
        return "\n".join(open(path, encoding="utf-8").read().split("\n")[11:])
    except OSError:
        return ""


def classify(path: str) -> str:
    text = body(path)
    has_media = bool(re.search(MEDIA, text)) or os.path.isdir(
        os.path.join(MIRROR, "_attachments", page_id(path))
    )
    if re.sub(MEDIA, "", text).strip():
        return "text"
    return "attachment" if has_media else "empty"


def context_text() -> str:
    """Everything the distilled layer says, concatenated for membership checks."""
    chunks = []
    for root, _, files in os.walk(CONTEXT):
        for name in files:
            if name.endswith(".md") and not root.endswith("daily"):
                chunks.append(open(os.path.join(root, name), encoding="utf-8").read())
    for extra in (ROOT_DOC, "reviews", "decisions", "requests"):
        if os.path.isfile(extra):
            chunks.append(open(extra, encoding="utf-8").read())
        elif os.path.isdir(extra):
            for root, _, files in os.walk(extra):
                for name in files:
                    if name.endswith(".md"):
                        chunks.append(open(os.path.join(root, name), encoding="utf-8").read())
    return "\n".join(chunks)


def last_reviewed() -> str:
    """The date the standing agenda claims it was last checked against the mirror."""
    try:
        text = open(AGENDA, encoding="utf-8").read()
    except OSError:
        return ""
    match = re.search(r"Last full review against the mirror:\s*(\d{4}-\d{2}-\d{2})", text)
    return match.group(1) if match else ""


def added_since(date: str) -> list[str]:
    """Pages first committed since `date`."""
    result = subprocess.run(
        ["git", "log", f"--since={date}", "--diff-filter=A", "--name-only",
         "--format=", "--", MIRROR],
        capture_output=True, text=True, check=False,
    )
    seen = {
        line for line in result.stdout.splitlines()
        if line.endswith(".md") and not line.endswith("INDEX.md")
    }
    return sorted(p for p in seen if os.path.exists(p))


def changed_since(date: str) -> list[str]:
    if not date:
        return []
    result = subprocess.run(
        ["git", "log", f"--since={date}", "--name-only", "--format=", "--", MIRROR],
        capture_output=True, text=True, check=False,
    )
    seen = {
        line for line in result.stdout.splitlines()
        if line.endswith(".md") and not line.endswith("INDEX.md")
    }
    return sorted(p for p in seen if os.path.exists(p))


def main() -> int:
    all_pages = pages()
    if not all_pages:
        return 0

    notes = context_text()
    findings: list[str] = []

    # 1. Pages that ARRIVED since the last review and are still not referenced in
    #    the notes. Scoping to new pages is what keeps this quiet: a long-standing
    #    page nobody needed to cite is not drift, a new one nobody has read is.
    reviewed = last_reviewed()
    arrived = added_since(reviewed) if reviewed else []
    unseen = []
    for path in arrived:
        pid, (title, _) = page_id(path), meta(path)
        if (pid and pid in notes) or (title and title in notes):
            continue
        unseen.append(path)
    if unseen:
        findings.append(f"**{len(unseen)} new page(s) not yet referenced in `context/`** — unread:")
        findings.append("")
        findings.extend(f"- {link(p)}" for p in unseen[:10])
        if len(unseen) > 10:
            findings.append(f"- …and {len(unseen) - 10} more")
        findings.append("")

    # 2. The recorded page counts, which are quoted in CLAUDE.md and cited in
    #    conversation, drifting from what the mirror actually holds.
    counts = {"text": 0, "attachment": 0, "empty": 0}
    for path in all_pages:
        counts[classify(path)] += 1
    try:
        root_doc = open(ROOT_DOC, encoding="utf-8").read()
        claimed = re.search(
            r"Of (\d+) pages, \*\*(\d+) carry text, (\d+) hold only an attachment or diagram, and (\d+)",
            root_doc,
        )
    except OSError:
        claimed = None
    if claimed:
        want = tuple(int(g) for g in claimed.groups())
        have = (len(all_pages), counts["text"], counts["attachment"], counts["empty"])
        if want != have:
            findings.append(
                f"**Page counts in `{ROOT_DOC}` are stale** — recorded "
                f"{want[0]} pages ({want[1]} text, {want[2]} attachment, {want[3]} empty); "
                f"mirror now holds {have[0]} ({have[1]}, {have[2]}, {have[3]})."
            )
            findings.append("")

    # 3. Model providers named in prose. The position-table scan cannot see these.
    try:
        register = {k.lower() for k in json.load(open(REGISTER, encoding="utf-8")).get("tools", {})}
    except (OSError, ValueError):
        register = set()
    hits: dict[str, list[str]] = {}
    for path in (changed_since(reviewed) if reviewed else []):
        text = body(path)
        for provider in PROVIDERS:
            if provider.lower() in register:
                continue
            if re.search(rf"\b{re.escape(provider)}\b", text, re.I):
                hits.setdefault(provider, []).append(path)
    unruled = {p: v for p, v in hits.items() if p.lower() not in notes.lower()}
    if unruled:
        findings.append("**External model provider named in the space with no recorded ruling:**")
        findings.append("")
        for provider, paths in sorted(unruled.items()):
            findings.append(f"- **{provider}** — {link(paths[0])}"
                            + (f" and {len(paths) - 1} other page(s)" if len(paths) > 1 else ""))
        findings.append("")

    # 4. Pages edited since the agenda last claimed to be current. Not drift by
    #    itself, but it is what makes an agenda item quietly go out of date.
    if reviewed:
        moved = changed_since(reviewed)
        if moved:
            findings.append(
                f"**{len(moved)} page(s) changed since the standing agenda was last "
                f"reviewed ({reviewed})** — the agenda may be asking for things already settled:"
            )
            findings.append("")
            findings.extend(f"- {link(p)}" for p in moved[:8])
            if len(moved) > 8:
                findings.append(f"- …and {len(moved) - 8} more")
            findings.append("")
    else:
        findings.append(
            f"**`{AGENDA}` has no 'Last full review against the mirror' date**, so "
            f"staleness cannot be measured. Add one when the agenda is next reviewed."
        )
        findings.append("")

    # 5. Pages filed outside the OI3.0 tree, which do not appear in the hierarchy
    #    and are easy to miss when reading the space by navigation.
    root_page = re.compile(rf"^{re.escape(MIRROR)}/oi30-\d+\.md$")
    orphans = [
        p for p in all_pages
        if not p.startswith(f"{MIRROR}/oi30/") and not root_page.match(p)
    ]
    if orphans:
        findings.append("**Page(s) filed outside the OI3.0 tree**, so absent from the page hierarchy:")
        findings.append("")
        findings.extend(f"- {link(p)}" for p in orphans)
        findings.append("")

    if not findings:
        return 0

    print("## Knowledge base drift")
    print()
    print(
        "Mechanical checks on whether the distilled layer in `context/` still matches "
        "the mirror. These need a reading pass, not a script."
    )
    print()
    print("\n".join(findings).rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
