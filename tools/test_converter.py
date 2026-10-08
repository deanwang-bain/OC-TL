#!/usr/bin/env python3
"""Checks on the storage-format converter.

    python3 tools/test_converter.py

Each case here is a bug the mirror actually shipped. The converter is lossy by
design, so the question is never "is this faithful" but "does a reader of the
markdown reach the same conclusion as a reader of the page". These are the
places where they did not.

No test framework: the sync is stdlib-only and so is this.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from confluence_sync import StorageConverter  # noqa: E402


def convert(storage: str) -> str:
    converter = StorageConverter()
    converter.feed(storage)
    return converter.result()


def check(name: str, condition: bool, detail: str = "") -> bool:
    print(f"{'ok  ' if condition else 'FAIL'}  {name}" + (f" -- {detail}" if not condition and detail else ""))
    return condition


# A native-tabs extension, shaped on the GLS deployment tracker. Confluence ships
# the body twice: once as `ac:adf-content`, and again as `ac:adf-fallback` for
# clients that cannot render the extension. Emitting both gave the tracker five
# copies of the same TSG table, and `ac:adf-attribute` spilled the extension's
# own parameters into the page as a run of unreadable text.
ADF_TABS = """
<h2>Portal and access</h2>
<ac:adf-extension>
  <ac:adf-node type="extension">
    <ac:adf-attribute key="extension-key">native-tabs</ac:adf-attribute>
    <ac:adf-attribute key="parameters">
      <ac:adf-parameter key="local-id">eozril</ac:adf-parameter>
      <ac:adf-parameter key="title">Angel (DevOps)</ac:adf-parameter>
    </ac:adf-attribute>
    <ac:adf-content>
      <table><tbody>
        <tr><th>Step</th><th>Change</th></tr>
        <tr><td>1</td><td>GitHub sign-in trust</td></tr>
      </tbody></table>
      <table><tbody>
        <tr><th>Step</th><th>Change</th></tr>
        <tr><td>1</td><td>Add redirect URIs</td></tr>
      </tbody></table>
    </ac:adf-content>
  </ac:adf-node>
  <ac:adf-fallback>
    <table><tbody>
      <tr><th>Step</th><th>Change</th></tr>
      <tr><td>1</td><td>Add redirect URIs</td></tr>
    </tbody></table>
  </ac:adf-fallback>
</ac:adf-extension>
"""

# Regression guards for fidelity bugs fixed earlier: a paragraph inside a table
# cell used to break the row, and a code macro's body arrives as CDATA.
TABLE_WITH_PARAGRAPHS = """
<table><tbody>
<tr><th>Area</th><th>Note</th></tr>
<tr><td><p>Terraform</p></td><td><p>Subnet</p><p>cannot change later</p></td></tr>
</tbody></table>
"""

CODE_MACRO = """
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">python</ac:parameter>
  <ac:plain-text-body><![CDATA[chosen = foundry.ask_agent(prompt)]]></ac:plain-text-body>
</ac:structured-macro>
"""


def main() -> int:
    results = []

    tabs = convert(ADF_TABS)
    results.append(check(
        "adf: extension metadata does not reach the page",
        not any(j in tabs for j in ("native-tabs", "eozril", "Angel (DevOps)")),
        tabs[:120],
    ))
    results.append(check(
        "adf: fallback copy does not duplicate the body",
        tabs.count("Add redirect URIs") == 1,
        f"{tabs.count('Add redirect URIs')} copies",
    ))
    results.append(check(
        "adf: real tab content survives",
        "GitHub sign-in trust" in tabs,
    ))

    table = convert(TABLE_WITH_PARAGRAPHS)
    rows = [ln for ln in table.splitlines() if ln.startswith("|")]
    results.append(check(
        "table: a paragraph in a cell does not break the row",
        len(rows) == 3 and "cannot change later" in rows[2],
        f"{len(rows)} rows: {rows}",
    ))

    code = convert(CODE_MACRO)
    results.append(check(
        "code: CDATA body is kept, with its language",
        "foundry.ask_agent(prompt)" in code and "```python" in code,
        code[:120],
    ))

    failed = results.count(False)
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
