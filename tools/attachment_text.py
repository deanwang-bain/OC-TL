#!/usr/bin/env python3
"""Read the text out of a mirrored attachment: pptx, xlsx, docx, html, csv.

    python3 tools/attachment_text.py <file> [...]        # print text
    python3 tools/attachment_text.py --list              # what is readable, by type

Several of the most decision-dense artefacts in the OI30 space are attachments on
otherwise empty pages -- the sprint retrospectives are decks, the ARC assessment is
two workbooks, the GLS output sample is an HTML file. Confluence shows them; the
markdown mirror only links them. This makes the contents greppable without
leaving the repo, and without rewriting a parser each time.

Stdlib only, like the rest of `tools/`: an Office file is a zip of XML, and HTML
is stripped with a regex rather than a parser because the goal is reading, not
fidelity.

For SVG diagrams use `tools/diagram_text.py`. Raster diagrams (PNG) need a model
that can see them -- `context/diagrams/README.md` lists the ones worth a pass.
"""

from __future__ import annotations

import csv as csvmod
import html as htmlmod
import io
import os
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
DRAW = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
WORD = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
NS = {"m": MAIN, "r": REL}


def _squash(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text).strip()


def pptx(path: str) -> str:
    """Slide text, in slide order. Speaker notes are skipped."""
    zf = zipfile.ZipFile(path)
    slides = sorted(
        (n for n in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
        key=lambda n: int(re.search(r"(\d+)", n.rsplit("/", 1)[-1]).group(1)),
    )
    out = []
    for name in slides:
        out.append(f"\n===== {name.rsplit('/', 1)[-1]} =====")
        for para in ET.fromstring(zf.read(name)).iter():
            if not para.tag.endswith("}p"):
                continue
            line = _squash("".join(t.text or "" for t in para.iter(DRAW + "t")))
            if line:
                out.append(line)
    return "\n".join(out)


def xlsx(path: str) -> str:
    """Every sheet as pipe-separated rows. Formulas render as their cached value."""
    zf = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in zf.namelist():
        for si in ET.fromstring(zf.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter(f"{{{MAIN}}}t")))
    book = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))}
    out = []
    for sheet in book.find("m:sheets", NS):
        target = rels[sheet.get(f"{{{REL}}}id")]
        if not target.startswith("xl/"):
            target = "xl/" + target.lstrip("/")
        out.append(f"\n########## SHEET: {sheet.get('name')}")
        for row in ET.fromstring(zf.read(target)).iter(f"{{{MAIN}}}row"):
            cells = []
            for cell in row.findall("m:c", NS):
                value, kind = cell.find("m:v", NS), cell.get("t")
                if kind == "inlineStr":
                    inline = cell.find("m:is", NS)
                    text = "".join(x.text or "" for x in inline.iter(f"{{{MAIN}}}t")) if inline is not None else ""
                elif value is None:
                    text = ""
                elif kind == "s":
                    text = shared[int(value.text)]
                else:
                    text = value.text or ""
                cells.append(_squash(re.sub(r"\s+", " ", text)))
            while cells and not cells[-1]:
                cells.pop()
            if cells:
                out.append(" | ".join(cells))
    return "\n".join(out)


def docx(path: str) -> str:
    zf = zipfile.ZipFile(path)
    out = []
    for para in ET.fromstring(zf.read("word/document.xml")).iter(WORD + "p"):
        line = _squash("".join(t.text or "" for t in para.iter(WORD + "t")))
        if line:
            out.append(line)
    return "\n".join(out)


def html_text(path: str) -> str:
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"(?is)<(script|style|svg)\b.*?</\1>", " ", raw)
    raw = htmlmod.unescape(re.sub(r"<[^>]+>", " ", raw))
    return re.sub(r"[ \t]{2,}", " ", re.sub(r"\n{3,}", "\n\n", raw)).strip()


def csv_text(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace", newline="") as handle:
        return "\n".join(" | ".join(row) for row in csvmod.reader(handle))


READERS = {
    ".pptx": pptx, ".xlsx": xlsx, ".xlsm": xlsx, ".docx": docx,
    ".html": html_text, ".htm": html_text, ".csv": csv_text,
}
# Known-unreadable here, so --list can say why rather than staying silent.
OPAQUE = {
    ".png": "raster diagram -- needs a model that can see it",
    ".jpg": "image", ".jpeg": "image", ".jfif": "image",
    ".mp4": "video -- no transcript in the mirror",
    ".pdf": "PDF -- no stdlib reader; convert or read page images",
    ".zip": "archive -- unzip into its own empty directory first",
    ".svg": "use tools/diagram_text.py",
}


def listing() -> int:
    counts: dict[str, list[str]] = {}
    for root, _, files in os.walk(os.path.join("confluence", "_attachments")):
        for name in files:
            counts.setdefault(os.path.splitext(name)[1].lower(), []).append(
                os.path.join(root, name)
            )
    print("readable by this tool:")
    for ext in sorted(e for e in counts if e in READERS):
        print(f"  {ext:7} {len(counts[ext]):3d}")
    print("\nnot readable here:")
    for ext in sorted(e for e in counts if e not in READERS):
        print(f"  {ext:7} {len(counts[ext]):3d}   {OPAQUE.get(ext, 'unknown type')}")
    return 0


def main(argv: list[str]) -> int:
    if not argv or "--list" in argv:
        return listing()
    status = 0
    for path in argv:
        reader = READERS.get(os.path.splitext(path)[1].lower())
        if reader is None:
            why = OPAQUE.get(os.path.splitext(path)[1].lower(), "unsupported type")
            print(f"{path}: {why}", file=sys.stderr)
            status = 1
            continue
        if len(argv) > 1:
            print(f"\n######## {path}")
        try:
            print(reader(path))
        except (OSError, zipfile.BadZipFile, ET.ParseError, KeyError) as exc:
            print(f"{path}: could not read ({exc})", file=sys.stderr)
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
