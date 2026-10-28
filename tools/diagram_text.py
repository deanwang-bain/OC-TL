#!/usr/bin/env python3
"""Extract the text out of mirrored SVG diagrams.

    python3 tools/diagram_text.py            # write context/diagrams/*.txt
    python3 tools/diagram_text.py --check    # report drift, write nothing
    python3 tools/diagram_text.py <file.svg> # print one, for a quick look

An SVG is XML, so its labels are readable without looking at the picture. That
matters here because the OI 3.0 architecture diagrams carry decisions that appear
on no prose page -- the technical architecture SVG names a **Claude SDK**
orchestrator, which contradicts ADR-008's choice of Microsoft Agent Framework and
which no text search could ever have found.

Raster diagrams (PNG) need a model that can see, so they are listed in
`context/diagrams/README.md` for a reading pass rather than extracted here.

Output goes to `context/diagrams/`, not into `confluence/`, because the mirror is
regenerated on every sync and anything written there is lost.
"""

from __future__ import annotations

import hashlib
import os
import re
import sys
from xml.etree import ElementTree as ET

MIRROR = "confluence"
ATTACHMENTS = os.path.join(MIRROR, "_attachments")
OUT = os.path.join("context", "diagrams")


def svg_text(path: str) -> list[str] | None:
    """Every <text> node, in document order. None if the file will not parse."""
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError):
        return None
    found = []
    for el in root.iter():
        if el.tag.endswith("}text") or el.tag == "text":
            line = " ".join("".join(el.itertext()).split())
            if line:
                found.append(line)
    return found


def page_for(page_id: str) -> tuple[str, str]:
    """The title and path of the page an attachment belongs to."""
    for root, dirs, files in os.walk(MIRROR):
        dirs[:] = [d for d in dirs if d != "_attachments"]
        for name in files:
            if not name.endswith(f"-{page_id}.md"):
                continue
            path = os.path.join(root, name)
            head = open(path, encoding="utf-8").read(400)
            match = re.search(r'^title:\s*"(.*)"', head, re.M)
            return (match.group(1) if match else name), path
    return page_id, ""


def diagrams() -> list[tuple[str, str, list[str]]]:
    """(path, page_id, text) for every SVG under the mirror.

    Ordered so that when the same diagram appears more than once, the better
    copy is the one kept: a descriptive filename beats `svgviewer-output_7_.svg`,
    and a real page beats one titled "to be delete". Both drafts carry the whole
    Future Scope and Present Working diagram sets under export filenames, so
    without this the extracted set would be named after the discard pile.
    """
    found = []
    for root, _, files in os.walk(ATTACHMENTS):
        for name in sorted(files):
            if not name.lower().endswith(".svg"):
                continue
            path = os.path.join(root, name)
            text = svg_text(path)
            if text:
                found.append((path, os.path.basename(root), text))

    def preference(item: tuple[str, str, list[str]]) -> tuple[int, int, str]:
        path, page_id, _ = item
        title, _page = page_for(page_id)
        anonymous = 1 if re.match(r"svgviewer-output", os.path.basename(path), re.I) else 0
        discarded = 1 if "to be delete" in title.lower() else 0
        return (discarded, anonymous, path)

    return sorted(found, key=preference)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def main(argv: list[str]) -> int:
    if argv and argv[0].endswith(".svg"):
        text = svg_text(argv[0])
        if text is None:
            print(f"could not parse {argv[0]}", file=sys.stderr)
            return 1
        print("\n".join(text))
        return 0

    check = "--check" in argv
    found = diagrams()
    if not found:
        print("no SVG diagrams in the mirror", file=sys.stderr)
        return 0

    # Several pages carry byte-identical copies of the same diagram -- the two
    # "to be delete" drafts duplicate the Future Scope and Present Working sets.
    # Keep the first occurrence and record the rest as copies, so the extracted
    # set is one file per distinct diagram.
    seen: dict[str, str] = {}
    written, copies = [], []
    for path, page_id, text in found:
        digest = hashlib.sha1("\n".join(text).encode()).hexdigest()[:10]
        if digest in seen:
            copies.append((path, seen[digest]))
            continue
        seen[digest] = path
        title, _ = page_for(page_id)
        name = f"{slug(title)}--{slug(os.path.basename(path)[:-4])}.txt"
        written.append((name, path, page_id, title, text))

    if check:
        missing = [n for n, *_ in written if not os.path.exists(os.path.join(OUT, n))]
        print(f"{len(found)} SVGs, {len(written)} distinct, {len(copies)} duplicate copies")
        if missing:
            print(f"{len(missing)} not yet extracted:")
            for name in missing:
                print(f"  {name}")
        return 0

    os.makedirs(OUT, exist_ok=True)
    for name, path, page_id, title, text in written:
        url = f"https://bainco.atlassian.net/wiki/spaces/OI30/pages/{page_id}"
        body = [
            f"# {os.path.basename(path)}",
            "",
            f"Diagram text extracted from `{path}`.",
            f"Page: [{title}]({url})",
            "",
            "Labels in document order. Layout and arrows are lost -- open the SVG",
            "itself when the relationships matter, not only the words.",
            "",
            "---",
            "",
        ]
        body.extend(text)
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as handle:
            handle.write("\n".join(body) + "\n")

    print(f"wrote {len(written)} files to {OUT}/ ({len(copies)} duplicates skipped)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
