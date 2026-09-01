#!/usr/bin/env python3
"""Mirror a Confluence Cloud space into the repository as markdown.

Reads every page in the configured space via the Confluence Cloud v2 REST API,
converts the storage-format body to markdown, and writes one file per page under
OUTPUT_DIR, laid out to match the page tree in Confluence.

A manifest (`.manifest.json`) records each page's version number so re-runs only
refetch pages that actually changed, and pages deleted in Confluence are removed
from the mirror.

Configuration comes from the environment:

    CONFLUENCE_SITE       e.g. bainco.atlassian.net
    CONFLUENCE_SPACE      space key, e.g. OI30
    CONFLUENCE_EMAIL      Atlassian account email
    CONFLUENCE_API_TOKEN  token from id.atlassian.com/manage-profile/security/api-tokens
    OUTPUT_DIR            defaults to ./confluence

Stdlib only, so it runs on a bare CI runner with no pip step.
"""

from __future__ import annotations

import base64
import html
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

TIMEOUT = 60
PAGE_LIMIT = 100
MAX_RETRIES = 5

# Bump when the markdown output changes. Pages are normally skipped while their
# Confluence version is unchanged, which would otherwise leave the whole mirror
# frozen at the old rendering; a bump forces one full rewrite.
CONVERTER_VERSION = 5


class ConfluenceError(RuntimeError):
    pass


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------


class Client:
    def __init__(self, site: str, email: str, token: str):
        self.base = f"https://{site}"
        credentials = base64.b64encode(f"{email}:{token}".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {credentials}",
            "Accept": "application/json",
            "User-Agent": "oc-tl-confluence-sync/1.0",
        }

    def get(self, path: str, params: dict | None = None) -> dict:
        """GET a Confluence API path, retrying on rate limits and transient errors.

        `path` may be absolute or site-relative; the v2 API returns site-relative
        `_links.next` values for pagination, so both forms show up in practice.
        """
        url = path if path.startswith("http") else urllib.parse.urljoin(self.base, path)
        if params:
            url = f"{url}{'&' if '?' in url else '?'}{urllib.parse.urlencode(params)}"

        for attempt in range(MAX_RETRIES):
            request = urllib.request.Request(url, headers=self.headers)
            try:
                with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                # 401/403 mean the credentials or permissions are wrong; retrying
                # cannot fix that, so surface it immediately with a usable message.
                if exc.code in (401, 403):
                    raise ConfluenceError(
                        f"{exc.code} {exc.reason} for {url}. Check CONFLUENCE_EMAIL and "
                        f"CONFLUENCE_API_TOKEN, and that the account can read the space."
                    ) from exc
                if exc.code == 429 or exc.code >= 500:
                    if attempt == MAX_RETRIES - 1:
                        raise ConfluenceError(f"{exc.code} {exc.reason} for {url}") from exc
                    delay = _retry_delay(exc, attempt)
                    print(f"  {exc.code}; retrying in {delay}s", file=sys.stderr)
                    time.sleep(delay)
                    continue
                raise ConfluenceError(f"{exc.code} {exc.reason} for {url}") from exc
            except urllib.error.URLError as exc:
                if attempt == MAX_RETRIES - 1:
                    raise ConfluenceError(
                        f"Could not reach {self.base}: {exc.reason}. If this is running "
                        f"inside a sandboxed session, the host is probably not on the "
                        f"network allowlist."
                    ) from exc
                time.sleep(2**attempt)
        raise ConfluenceError(f"exhausted retries for {url}")

    def download_candidates(self, link: str) -> list[str]:
        """Absolute URLs to try for an attachment download link.

        The v2 API returns `downloadLink` relative to the Confluence context
        path (`/wiki`), not the site root, so joining it against the bare host
        yields a 404. Try the context-qualified form first and fall back, since
        the shape differs between Cloud and Server.
        """
        if link.startswith("http"):
            return [link]
        path = link if link.startswith("/") else f"/{link}"
        candidates = []
        if not path.startswith("/wiki/"):
            candidates.append(urllib.parse.urljoin(self.base, f"/wiki{path}"))
        candidates.append(urllib.parse.urljoin(self.base, path))
        return candidates

    def get_binary(self, url: str) -> bytes:
        """Download an attachment. Download links redirect, which urllib follows."""
        for attempt in range(MAX_RETRIES):
            request = urllib.request.Request(url, headers=self.headers)
            try:
                with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                    return response.read()
            except urllib.error.HTTPError as exc:
                if exc.code in (401, 403, 404):
                    raise ConfluenceError(f"{exc.code} for attachment {url}") from exc
                if attempt == MAX_RETRIES - 1:
                    raise ConfluenceError(f"{exc.code} for attachment {url}") from exc
                time.sleep(_retry_delay(exc, attempt))
            except urllib.error.URLError as exc:
                if attempt == MAX_RETRIES - 1:
                    raise ConfluenceError(f"attachment {url}: {exc.reason}") from exc
                time.sleep(2**attempt)
        raise ConfluenceError(f"exhausted retries for {url}")

    def paginate(self, path: str, params: dict | None = None):
        """Yield results across every page of a v2 collection endpoint."""
        payload = self.get(path, params)
        while True:
            yield from payload.get("results", [])
            next_link = payload.get("_links", {}).get("next")
            if not next_link:
                return
            payload = self.get(next_link)


def _retry_delay(exc: urllib.error.HTTPError, attempt: int) -> int:
    """Honour Retry-After when the server sends it, else back off exponentially."""
    retry_after = exc.headers.get("Retry-After") if exc.headers else None
    if retry_after:
        try:
            return max(1, min(int(retry_after), 120))
        except ValueError:
            pass
    return 2**attempt


# --------------------------------------------------------------------------
# Storage format -> markdown
# --------------------------------------------------------------------------

BLOCK_TAGS = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "tr"}
HEADINGS = {f"h{n}": "#" * n for n in range(1, 7)}
# Confluence wraps rich content in ac:-namespaced macro tags. A few carry content
# worth keeping; the rest are chrome that would only add noise to the mirror.
SKIP_CONTENT = {"ac:parameter", "ac:emoticon"}

# Macros that render as a visual or generated block. They carry no text, so
# without a placeholder the page mirrors as blank and a reader cannot tell an
# empty page from one whose whole content is a diagram.
VISUAL_MACROS = {
    "drawio": "draw.io diagram",
    "gliffy": "Gliffy diagram",
    "excalidraw": "Excalidraw diagram",
    "whiteboard": "whiteboard",
    "mermaid": "Mermaid diagram",
    "children": "child page index",
    "excerpt-include": "excerpt from another page",
    "include": "included page",
    "jira": "Jira issue embed",
    "attachments": "attachment list",
    "viewpdf": "embedded PDF",
    "viewxls": "embedded spreadsheet",
    "widget": "embedded widget",
    "iframe": "embedded iframe",
}


class StorageConverter(HTMLParser):
    """Convert Confluence storage format (XHTML plus ac:/ri: macros) to markdown.

    This is deliberately lossy: it preserves structure an LLM needs to read the
    page (headings, lists, tables, code, links) and drops presentational markup.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.list_stack: list[str] = []
        self.skip_depth = 0
        self.in_pre = False
        self.pending_link: str | None = None
        self.link_text: list[str] = []
        self.row_is_header = False
        self.row_cells = 0
        self.in_code_macro = False
        self.code_language = ""
        self.capture_language = False
        # Confluence wraps cell and list-item content in <p>. Treating those as
        # block elements would break a table row across lines and detach a
        # bullet from its text, so inside them block tags render inline.
        self.cell_depth = 0
        self.li_depth = 0
        self.in_image = False

    # -- helpers ----------------------------------------------------------

    def _emit(self, text: str) -> None:
        if self.skip_depth == 0:
            self.out.append(text)

    def _inline_context(self) -> bool:
        """True where a newline would corrupt the structure (cells, list items)."""
        return self.cell_depth > 0 or self.li_depth > 0

    def _space(self) -> None:
        if self.out and not self.out[-1].endswith((" ", "\n", "|")):
            self._emit(" ")

    def _collapse_cell(self) -> None:
        """Flatten the current cell's emitted text onto a single line."""
        for index in range(len(self.out) - 1, -1, -1):
            if self.out[index].endswith("|"):
                break
            if "\n" in self.out[index]:
                self.out[index] = re.sub(r"\s*\n\s*", " ", self.out[index])

    def _newline(self, count: int = 1) -> None:
        if not self.out:
            return
        existing = len(self.out[-1]) - len(self.out[-1].rstrip("\n"))
        if existing < count:
            self.out.append("\n" * (count - existing))

    # -- parser hooks -----------------------------------------------------

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        # The code macro records its language in a parameter that is otherwise
        # skipped, so capture it before the generic skip rule applies.
        if tag == "ac:parameter" and self.in_code_macro:
            if attrs.get("ac:name") == "language":
                self.capture_language = True

        if tag in SKIP_CONTENT:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return

        if tag in HEADINGS:
            self._newline(2)
            self._emit(f"{HEADINGS[tag]} ")
        elif tag in ("p", "div"):
            if self._inline_context():
                self._space()
            else:
                self._newline(2)
        elif tag == "br":
            self._emit(" " if self._inline_context() else "\n")
        elif tag in ("strong", "b"):
            self._emit("**")
        elif tag in ("em", "i"):
            self._emit("*")
        elif tag == "code" and not self.in_pre:
            self._emit("`")
        elif tag == "blockquote":
            self._newline(2)
            self._emit("> ")
        elif tag in ("ul", "ol"):
            self._newline(1)
            self.list_stack.append(tag)
        elif tag == "li":
            self._newline(1)
            depth = max(0, len(self.list_stack) - 1)
            marker = "- " if (self.list_stack or ["ul"])[-1] == "ul" else "1. "
            self._emit("  " * depth + marker)
            self.li_depth += 1
        elif tag == "a":
            self.pending_link = attrs.get("href")
            self.link_text = []
        elif tag == "table":
            self._newline(2)
        elif tag == "tr":
            self._newline(1)
            self.row_is_header = False
            self.row_cells = 0
            self._emit("|")
        elif tag in ("td", "th"):
            self.row_is_header = self.row_is_header or tag == "th"
            self.row_cells += 1
            self.cell_depth += 1
            self._emit(" ")
        elif tag == "ac:image":
            self.in_image = True
        elif tag == "ri:attachment":
            name = attrs.get("ri:filename", "file")
            label = "image" if self.in_image else "attachment"
            self._emit(f"_[{label}: {name}]_")
        elif tag == "ri:url":
            if self.in_image:
                self._emit(f"_[image: {attrs.get('ri:value', 'external')}]_")
        elif tag == "ri:page":
            # A cross-reference to another Confluence page.
            title = attrs.get("ri:content-title")
            if title:
                self._emit(f"[{title}]")
        elif tag == "ac:structured-macro":
            name = attrs.get("ac:name", "")
            if name == "code":
                self.in_code_macro = True
                self.code_language = ""
            elif name in VISUAL_MACROS:
                self._newline(2)
                self._emit(f"_[{VISUAL_MACROS[name]}]_")
                self._newline(2)
        elif tag == "ac:plain-text-body":
            # The fence opens here, not at the macro tag, because the language
            # parameter is only known once it has been parsed.
            if self.in_code_macro:
                self._newline(2)
                self._emit(f"```{self.code_language}\n")
                self.in_pre = True
        elif tag == "ac:rich-text-body":
            pass
        elif tag.startswith("ac:") or tag.startswith("ri:"):
            # Unknown macro: keep any text inside, drop the tag itself.
            pass

    def handle_endtag(self, tag):
        if tag in SKIP_CONTENT:
            self.skip_depth = max(0, self.skip_depth - 1)
            self.capture_language = False
            return
        if self.skip_depth:
            return

        if tag in ("p", "div"):
            self._space() if self._inline_context() else self._newline(2)
        elif tag in HEADINGS:
            self._newline(2)
        elif tag == "li":
            self.li_depth = max(0, self.li_depth - 1)
        elif tag in ("strong", "b"):
            self._emit("**")
        elif tag in ("em", "i"):
            self._emit("*")
        elif tag == "code" and not self.in_pre:
            self._emit("`")
        elif tag == "blockquote":
            self._newline(2)
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
            if not self.list_stack:
                self._newline(2)
        elif tag == "a":
            text = "".join(self.link_text).strip()
            href = self.pending_link
            self.pending_link = None
            self.link_text = []
            if text and href:
                self._emit(f"[{text}]({href})")
            elif text:
                self._emit(text)
        elif tag in ("td", "th"):
            self.cell_depth = max(0, self.cell_depth - 1)
            # A newline inside a cell would break the row, so flatten what the
            # cell produced back onto one line.
            self._collapse_cell()
            self._emit(" |")
        elif tag == "tr":
            # Markdown tables need a delimiter row after the header row.
            if self.row_is_header and self.row_cells:
                self._emit("\n|" + "---|" * self.row_cells)
        elif tag == "table":
            self._newline(2)
        elif tag == "ac:plain-text-body" and self.in_pre:
            self.in_pre = False
            self._newline(1)
            self._emit("```")
            self._newline(2)
        elif tag == "ac:image":
            self.in_image = False
        elif tag == "ac:structured-macro":
            self.in_code_macro = False

    def unknown_decl(self, data):
        # Code macro bodies arrive as CDATA sections, which HTMLParser reports
        # here rather than through handle_data.
        if self.skip_depth:
            return
        if data.startswith("CDATA["):
            self._emit(data[len("CDATA[") :])

    def handle_data(self, data):
        if self.capture_language:
            self.code_language = data.strip()
            return
        if self.skip_depth:
            return
        if self.in_pre:
            self._emit(data)
            return
        # Collapse whitespace outside code blocks; storage format is full of
        # incidental newlines from Confluence's own serialisation.
        text = re.sub(r"\s+", " ", data)
        if not text.strip():
            if self.out and not self.out[-1].endswith((" ", "\n")):
                self._emit(" ")
            return
        if self.pending_link is not None:
            self.link_text.append(text)
        else:
            self._emit(text)

    def result(self) -> str:
        text = "".join(self.out)
        # Only trailing whitespace is safe to touch here. Collapsing runs of
        # spaces globally would flatten list indentation and corrupt code
        # blocks; inline runs are already collapsed in handle_data.
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def storage_to_markdown(storage: str) -> str:
    if not storage:
        return ""
    converter = StorageConverter()
    try:
        converter.feed(storage)
        converter.close()
    except Exception as exc:  # a malformed page must not abort the whole sync
        print(f"  warning: conversion failed ({exc}); keeping raw body", file=sys.stderr)
        return storage
    return converter.result()


# --------------------------------------------------------------------------
# Mirror layout
# --------------------------------------------------------------------------


ATTACHMENT_DIR = "_attachments"
# Everything is downloaded, subject to a size cap. An allowlist of media types
# silently dropped whatever it did not anticipate: a page reading "here is the
# industry mapping" with no mapping beside it looks identical to a page that
# never had one. Anything skipped is now reported rather than dropped.
MAX_ATTACHMENT_BYTES = 25 * 1024 * 1024


def sync_attachments(client: Client, page_id: str, root: str) -> dict[str, str]:
    """Download a page's attachments; return {filename: path relative to root}."""
    target_dir = os.path.join(root, ATTACHMENT_DIR, page_id)
    downloaded: dict[str, str] = {}
    try:
        attachments = list(
            client.paginate(f"/wiki/api/v2/pages/{page_id}/attachments", {"limit": 100})
        )
    except ConfluenceError as exc:
        print(f"  warning: could not list attachments for {page_id}: {exc}", file=sys.stderr)
        return downloaded

    for attachment in attachments:
        title = attachment.get("title") or ""
        link = attachment.get("downloadLink")
        if not title or not link:
            continue
        size = attachment.get("fileSize")
        if isinstance(size, int) and size > MAX_ATTACHMENT_BYTES:
            print(
                f"  skipping {title}: {size // (1024 * 1024)}MB exceeds the "
                f"{MAX_ATTACHMENT_BYTES // (1024 * 1024)}MB cap",
                file=sys.stderr,
            )
            continue

        safe = re.sub(r"[^\w.\-]+", "_", title)[:120]
        destination = os.path.join(target_dir, safe)
        relative = f"{ATTACHMENT_DIR}/{page_id}/{safe}"
        if os.path.exists(destination):
            downloaded[title] = relative
            continue
        data = None
        errors = []
        for candidate in client.download_candidates(link):
            try:
                data = client.get_binary(candidate)
                break
            except ConfluenceError as exc:
                errors.append(str(exc))
        if data is None:
            print(f"  warning: could not download {title}: {errors}", file=sys.stderr)
            continue
        os.makedirs(target_dir, exist_ok=True)
        with open(destination, "wb") as handle:
            handle.write(data)
        downloaded[title] = relative
    return downloaded


def link_attachments(markdown: str, attachments: dict[str, str], page_path: str) -> str:
    """Turn the converter's attachment placeholders into real relative links.

    Placeholders are emitted during conversion, before the attachment list is
    known, so resolving them is a separate pass.
    """
    depth = page_path.count("/")
    prefix = "../" * depth

    def replace(match: re.Match) -> str:
        kind, name = match.group(1), match.group(2)
        relative = attachments.get(name)
        if not relative:
            return f"_[{kind}: {name} — not downloaded]_"
        target = prefix + relative
        return f"![{name}]({target})" if kind == "image" else f"[{name}]({target})"

    return re.sub(r"_\[(image|attachment): ([^\]]+?)\]_", replace, markdown)


def slugify(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title.lower()).strip()
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug[:80] or "untitled"


def build_paths(pages: list[dict]) -> dict[str, str]:
    """Map each page id to a repo-relative file path mirroring the page tree.

    Titles collide often in Confluence, so the page id is appended to keep every
    path unique and stable across renames of sibling pages.
    """
    by_id = {page["id"]: page for page in pages}
    paths: dict[str, str] = {}

    def segments(page_id: str, seen: frozenset[str] = frozenset()) -> list[str]:
        # `seen` guards against a parent cycle, which would otherwise recurse forever.
        page = by_id.get(page_id)
        if page is None or page_id in seen:
            return []
        parent_id = page.get("parentId")
        prefix = segments(parent_id, seen | {page_id}) if parent_id else []
        return prefix + [slugify(page.get("title", ""))]

    for page in pages:
        parts = segments(page["id"])
        directory = "/".join(parts[:-1])
        filename = f"{parts[-1]}-{page['id']}.md"
        paths[page["id"]] = f"{directory}/{filename}" if directory else filename
    return paths


def render(page: dict, site: str, space_key: str, body: str) -> str:
    """Render one page as markdown with front matter linking back to Confluence."""
    page_id = page["id"]
    title = page.get("title", "Untitled")
    version = page.get("version", {}) or {}
    url = f"https://{site}/wiki/spaces/{space_key}/pages/{page_id}"
    front_matter = [
        "---",
        f'title: "{title.replace(chr(34), chr(39))}"',
        f"confluence_id: {page_id}",
        f"confluence_url: {url}",
        f"version: {version.get('number', 'unknown')}",
        f"updated: {version.get('createdAt', 'unknown')}",
        "---",
        "",
        f"# {title}",
        "",
        f"[View in Confluence]({url})",
        "",
        "",
    ]
    return "\n".join(front_matter) + body + "\n"


# --------------------------------------------------------------------------
# Sync
# --------------------------------------------------------------------------


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ConfluenceError(f"{name} is not set")
    return value


def main() -> int:
    site = os.environ.get("CONFLUENCE_SITE", "bainco.atlassian.net").strip()
    space_key = os.environ.get("CONFLUENCE_SPACE", "OI30").strip()
    output_dir = os.environ.get("OUTPUT_DIR", "confluence").strip()
    sync_media = os.environ.get("SYNC_ATTACHMENTS", "1").strip().lower() not in (
        "0",
        "false",
        "no",
    )

    try:
        email = require_env("CONFLUENCE_EMAIL")
        token = require_env("CONFLUENCE_API_TOKEN")
    except ConfluenceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        print(
            "\nSet CONFLUENCE_EMAIL and CONFLUENCE_API_TOKEN. Create a token at\n"
            "https://id.atlassian.com/manage-profile/security/api-tokens",
            file=sys.stderr,
        )
        return 2

    client = Client(site, email, token)
    print(f"Syncing {space_key} from {site}")

    spaces = list(client.paginate("/wiki/api/v2/spaces", {"keys": space_key}))
    if not spaces:
        print(
            f"error: space {space_key!r} not found, or the account cannot see it.",
            file=sys.stderr,
        )
        return 1
    space = spaces[0]
    print(f"  space: {space.get('name', space_key)} (id {space['id']})")

    pages = list(
        client.paginate(
            f"/wiki/api/v2/spaces/{space['id']}/pages",
            {"limit": PAGE_LIMIT, "body-format": "storage", "status": "current"},
        )
    )
    print(f"  found {len(pages)} pages")
    if not pages:
        print("  nothing to write", file=sys.stderr)
        return 0

    root = os.path.abspath(output_dir)
    manifest_path = os.path.join(root, ".manifest.json")
    try:
        with open(manifest_path, encoding="utf-8") as handle:
            stored = json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError):
        stored = {}

    # Manifests written before versioning are a bare id -> record mapping.
    previous = stored.get("pages", stored if "converter_version" not in stored else {})
    if stored.get("converter_version") != CONVERTER_VERSION:
        if previous:
            print(f"  converter v{CONVERTER_VERSION}: rewriting all pages")
        # Keep the records so stale paths can still be pruned, but drop the
        # version numbers so every page is re-rendered.
        previous = {pid: {**rec, "version": None} for pid, rec in previous.items()}

    paths = build_paths(pages)
    manifest: dict[str, dict] = {}
    written = unchanged = 0

    for page in pages:
        page_id = page["id"]
        relative = paths[page_id]
        target = os.path.join(root, relative)
        version = (page.get("version", {}) or {}).get("number")

        record = previous.get(page_id)
        # Skip the rewrite only when the version and the destination both match;
        # a moved or renamed page changes its path without bumping its version.
        if (
            record
            and record.get("version") == version
            and record.get("path") == relative
            and os.path.exists(target)
        ):
            manifest[page_id] = record
            unchanged += 1
            continue

        storage = ((page.get("body", {}) or {}).get("storage", {}) or {}).get("value", "")
        body = storage_to_markdown(storage)
        if sync_media:
            attachments = sync_attachments(client, page_id, root)
            body = link_attachments(body, attachments, relative)
        markdown = render(page, site, space_key, body)

        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(markdown)

        manifest[page_id] = {
            "path": relative,
            "version": version,
            "title": page.get("title", ""),
        }
        written += 1

    # Drop files for pages that were deleted, archived, or moved out of the space.
    removed = 0
    live_paths = {entry["path"] for entry in manifest.values()}
    for page_id, record in previous.items():
        stale = record.get("path")
        if stale and stale not in live_paths:
            stale_path = os.path.join(root, stale)
            if os.path.exists(stale_path):
                os.remove(stale_path)
                removed += 1
    _prune_empty_dirs(root)

    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(
            {"converter_version": CONVERTER_VERSION, "pages": manifest},
            handle,
            indent=2,
            sort_keys=True,
        )

    _write_index(root, space, space_key, site, manifest)

    print(f"  wrote {written}, unchanged {unchanged}, removed {removed}")
    return 0


def _prune_empty_dirs(root: str) -> None:
    for current, directories, files in os.walk(root, topdown=False):
        if current == root:
            continue
        if not directories and not files:
            shutil.rmtree(current, ignore_errors=True)


def _write_index(root: str, space: dict, space_key: str, site: str, manifest: dict) -> None:
    """Write an index so a reader can see the whole space without walking the tree."""
    lines = [
        f"# {space.get('name', space_key)} ({space_key})",
        "",
        f"Mirror of <https://{site}/wiki/spaces/{space_key}/>, generated by "
        "`tools/confluence_sync.py`. Do not edit by hand: edits are overwritten on "
        "the next sync. Change the page in Confluence instead.",
        "",
        f"{len(manifest)} pages.",
        "",
    ]
    for entry in sorted(manifest.values(), key=lambda item: item["path"]):
        title = entry.get("title") or entry["path"]
        lines.append(f"- [{title}]({entry['path']})")
    lines.append("")
    with open(os.path.join(root, "INDEX.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ConfluenceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)
