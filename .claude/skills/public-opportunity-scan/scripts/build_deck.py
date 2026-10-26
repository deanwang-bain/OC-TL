#!/usr/bin/env python3
"""Build the opportunity scan as a PowerPoint deck.

    python build_deck.py case.json -o deck.pptx [--style auto|bain|neutral] [--bain-skill DIR]

The deck carries the same numbers as the poster, from the same calculation:
title, executive summary, performance against peers, case for change, size of
prize, EBIT bridge, the invitation to the full Opportunity Catalyst, and a
backup slide of sources. A chart-data.xlsx file is written beside the deck.

--style bain builds on the Bain Core template through the bain-slides skill,
which places chart placeholders (charts are pasted from chart-data.xlsx, the
Bain way). --style neutral builds a plain deck with native PowerPoint charts.
--style auto (default) uses Bain when the bain-slides skill can be found.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_poster import load_teaser  # noqa: E402
from opscan_calc import METRIC, CaseError, compute, fmt_metric, fmt_money, fmt_pct_range, fmt_range, resolve_tokens  # noqa: E402

BAIN_SEARCH_ROOTS = ["/mnt/skills", os.path.expanduser("~/.claude/skills"), "/root/.claude/skills"]


# --------------------------------------------------------------------------
# Content: plain text for every slide, built once and rendered in either style
# --------------------------------------------------------------------------

# a full stop after these is not the end of a sentence ("No. 1 priority", "vs. peers", "e.g. Toyota")
_SENT_END = re.compile(r"(?<!\bNo)(?<!\bvs)(?<!\bMr)(?<!\bMs)(?<!\bDr)(?<!\bSt)(?<!\bInc)(?<!\bCo)(?<!\be\.g)(?<!\bi\.e)(?<=[.!?])\s+(?=[A-Z“\"])")


def first_sentence(text, max_words=34):
    """The first sentence, kept whole when it fits; otherwise cut at the last clause break that fits."""
    s = _SENT_END.split(text.strip(), maxsplit=1)[0]
    words = s.split()
    if len(words) <= max_words:
        return s
    head = " ".join(words[:max_words])
    cut = max(head.rfind(", "), head.rfind("; "), head.rfind(": "))
    if cut > len(head) * 0.5:
        return head[:cut]
    return head.rstrip(",;:") + "…"


def short_header(text, limit=42):
    """Keep the longest leading clause that fits the limit; a long header wraps into the status sticker."""
    if len(text) <= limit:
        return text
    breaks = [m.start() for m in re.finditer(r"[,;:] ", text) if 12 < m.start() <= limit]
    return text[:breaks[-1]] if breaks else text


def label_in_sentence(label):
    """'Gross margin' -> 'gross margin', but 'EBIT margin' and 'SG&A as % of revenue' keep their capitals."""
    label = re.sub(r"\s*\([^)]*\)", "", label)  # "Revenue growth (CAGR)" reads as "revenue growth" in a sentence
    return label if len(label) > 1 and label[1].isupper() else label[0].lower() + label[1:]


def clean(text):
    """Deck text: no trailing full stop on fragments, unspaced dashes are left to the Bain builder."""
    return text.strip()


class Content:
    def __init__(self, case, analysis, tight=0):
        # tight: 0 full text; 1 shorter stories; 2 no readiness reasons; 3 no quotes, fewer bullets
        self.tight = tight
        self.case, self.a = case, analysis
        self.missing = []
        self.cur = analysis["meta"]["currency"]
        self.tid = analysis["meta"]["target_id"]
        self.companies = {c["id"]: c for c in case["companies"]}
        self.target = self.companies[self.tid]
        self.name = self.target.get("short_name") or self.target["name"]
        self.signals = {g["id"]: g for g in case.get("signals", [])}
        self.sources = case.get("sources", [])
        self.teaser = load_teaser(case)
        unchecked = [s for s in self.sources if s.get("checked") is False]
        self.sticker = "Preliminary" if unchecked else "Draft"
        self.unchecked = len(unchecked)

    def t(self, s):
        return resolve_tokens(s or "", self.a["facts"], self.missing)

    # ---- titles that state the finding
    def perf_title(self):
        order = ["top quartile", "above median", "below median", "bottom quartile"]
        keys = ["ebit_margin", self.a["meta"].get("growth_metric", "revenue_cagr"), "gross_margin", "sga_pct", "ccc"]
        rated = [(k, self.a["stats"][k]) for k in keys if self.a["stats"][k].get("rating")]
        if not rated:
            return f"{self.name} against {len(self.case['companies']) - 1} listed peers on margin, growth and cash"
        best = min(rated, key=lambda kv: order.index(kv[1]["rating"]))
        worst = max(rated, key=lambda kv: order.index(kv[1]["rating"]))
        bv = self.a["values"][self.tid][best[0]]["display"]
        wv = self.a["values"][self.tid][worst[0]]["display"]
        if best[1]["rating"] == worst[1]["rating"]:
            if len(rated) == 2:
                (k1, _), (k2, _) = rated
                return (f"{self.name} is {best[1]['rating']} on {label_in_sentence(METRIC[k1].label)} ({self.a['values'][self.tid][k1]['display']}) "
                        f"and on {label_in_sentence(METRIC[k2].label)} ({self.a['values'][self.tid][k2]['display']})")
            return f"{self.name} is {best[1]['rating']} on {label_in_sentence(METRIC[best[0]].label)} ({bv}) and across the other benchmarks"
        return (f"{self.name} is {best[1]['rating']} on {label_in_sentence(METRIC[best[0]].label)} ({bv}) "
                f"but {worst[1]['rating']} on {label_in_sentence(METRIC[worst[0]].label)} ({wv})")

    def build(self):
        a, nar, cm = self.a, self.case.get("narrative", {}), self.case.get("meta", {})
        t = a["totals"]
        horizon = a["meta"]["horizon_end"]
        out = {"sticker": self.sticker, "company": self.target["name"]}
        out["title"] = {"title": f"{self.target['name']}: where the value is",
                        "subtitle": (f"{self.t(cm.get('question', ''))}\nOutside-in view from public information, as of "
                                     f"{cm.get('as_of', '')} ({self.cur} millions)")}
        ex = [self.t(nar.get("headline", ""))] + [self.t(x) for x in nar.get("exec_summary", [])[:4]]
        out["exec"] = [clean(x) for x in ex if x][: 5 if self.tight < 3 else 4]

        # performance
        growth = a["meta"].get("growth_metric", "revenue_cagr")
        bullets = []
        for k in ["ebit_margin", growth, "gross_margin", "sga_pct", "dso", "dio", "ccc"]:
            st, v = a["stats"][k], a["values"][self.tid][k]
            if v["value"] is None:
                continue
            if st.get("rating"):
                bullets.append(f"**{METRIC[k].label}: {st['rating']}** ({v['display']}, {st['rank']} of {st['rank_of']}; "
                               f"median {fmt_metric(st['median'], METRIC[k].unit)})")
            elif st.get("median") is not None:
                bullets.append(f"**{METRIC[k].label}:** {v['display']} (median {fmt_metric(st['median'], METRIC[k].unit)}, not rated)")
            if len(bullets) == (6 if self.tight < 3 else 4):
                break
        per = a["values"][self.tid]["ebit_margin"]["period"] or ""
        out["perf"] = {"title": self.perf_title(), "chart_header": f"EBIT margin by company ({per})",
                       "chart_text": "[Chart: bar, EBIT margin by company, sorted best to worst, with peer median and top quartile; data in chart-data.xlsx]",
                       "bullets": bullets}

        # case for change: up to three framings
        cols = []
        story_words = [30, 22, 18, 16][self.tight]
        for f in nar.get("framings", [])[:3]:
            items = [first_sentence(self.t(f.get("story", "")), story_words)]
            for gid in (f.get("signals", [])[:1] if self.tight < 3 else []):
                g = self.signals.get(gid)
                if g and len(g.get("text", "").split()) <= (28 if self.tight == 0 else 18):
                    who = ", ".join(x for x in (g.get("speaker"), g.get("role")) if x)
                    q = f"“{g['text']}”" if g.get("verbatim", True) else g["text"]
                    items.append(f"**Management:** {q} ({who}{', ' + g['date'] if g.get('date') else ''})")
            if f.get("readiness"):
                if self.tight < 2:
                    items.append(f"**Client readiness: {f['readiness']}** ({first_sentence(self.t(f.get('readiness_reason', '')), 14 if self.tight else 18).rstrip('.')})")
                else:
                    items.append(f"**Client readiness: {f['readiness']}**")
            cols.append({"header": short_header(self.t(f.get("title", ""))), "items": items})
        lead = next((f for f in nar.get("framings", []) if f.get("lead")), (nar.get("framings") or [{}])[0])
        lead_t = short_header(self.t(lead.get("title", "")), 60).rstrip(".")
        out["cfc"] = {"title": f"The strongest framing for {self.name}: {lead_t[0].lower() + lead_t[1:]}",
                      "cols": cols}

        # size of prize table
        rows = []
        for b in a["buckets"]:
            if b["kind"] != "pnl":
                continue
            if b["state"] == "sized":
                if b["id"] == "commercial":
                    pct = f"{b['incremental_revenue']['pct_display']} more revenue"
                else:
                    pct = (f"{b['pct_of_baseline']['display']} of {b['baseline']['label'].lower()}; {b['margin_bps']['display']}"
                           if b.get("pct_of_baseline") else "")
                rows.append([b["name"], b["baseline"]["display"], b.get("gap_display", ""), b["opportunity"]["display"], pct])
            else:
                rows.append([b["name"], b["baseline"]["display"], b.get("reason", ""), "no gap" if b["state"] == "no_gap" else "n/a", ""])
        rows.append(["Recurring EBIT", "", "Sum of the rows above", t["pnl"]["display"], ""])
        nwc = next(b for b in a["buckets"] if b["id"] == "working_capital")
        lev = "; ".join(f"{lv['label']} {lv['gap_display']}" for lv in nwc["levers"] if lv["state"] == "sized") or nwc.get("reason", "")
        rows.append(["One-off cash: working capital", "", lev, t["cash"]["display"], "not added to EBIT"])
        growth_sized = any(x["id"] == "commercial" and x["state"] == "sized" for x in a["buckets"])
        when = f"a year by {horizon}" if growth_sized else "a year"
        cash_clause = f" and {t['cash']['display']} of one-off cash" if t["cash"]["display"] != "n/a" else ""
        out["prize"] = {"title": f"Closing the gaps to peers is worth {t['pnl']['display']} of recurring EBIT {when}{cash_clause}",
                        "headers": ["Bucket", "Baseline", "Gap to peers", "Opportunity", "As %"], "rows": rows,
                        "footnote": ("Note: low end closes the gap to the peer median, high end to the top quartile, on the latest year; "
                                     "recurring EBIT and one-off cash are never added\nSource: Company filings and results releases; "
                                     "public-data opportunity scan")}

        # bridge
        b = a["bridge"]
        notes = []
        names = {x["id"]: x["name"] for x in a["buckets"]}
        for bid, note in (nar.get("bucket_notes") or {}).items():
            text = note.get("text", "") if isinstance(note, dict) else note
            if text:
                notes.append(f"**{names.get(bid, bid).split(':')[0]}:** {first_sentence(self.t(text), [26, 22, 18, 14][self.tight]).rstrip('.')}")
        if b:
            m0 = fmt_metric(b["latest"]["margin"], "pct")
            m1 = fmt_pct_range(b["target"]["margin_low"], b["target"]["margin_high"])
            title = f"EBIT could rise from {b['latest']['display']} to {b['target']['display']} as the gaps close (margin {m0} to {m1})"
        else:
            title = "No EBIT bridge: the target's EBIT is not reported on this basis"
        bridge_head = f"EBIT bridge to {horizon}" if growth_sized else "EBIT bridge, latest year"
        out["bridge"] = {"title": title, "chart_header": f"{bridge_head} ({self.cur} millions)",
                         "chart_text": "[Chart: waterfall, latest EBIT plus each sized bucket to EBIT potential, low end solid and high end light; data in chart-data.xlsx]",
                         "bullets": notes[: (5 if self.tight < 3 else 3)] or ["**Method:** each bucket closes the gap to the peer median (low) and top quartile (high)"]}

        # invitation
        if self.teaser:
            tz = self.teaser
            rows = [[r[0], r[1], r[2]] for r in tz.get("compare_short", [])[:4]]
            out["invite"] = {"title": tz.get("deck_title") or
                             f"{tz.get('product', 'Opportunity Catalyst')} adds Bain experience behind every lever, live changes and a source behind every figure",
                             "headers": ["", "This scan", tz.get("product", "Opportunity Catalyst")], "rows": rows,
                             "footnote": (f"Refer to {tz['opcat_url']} for the full {tz.get('product', 'Opportunity Catalyst')} experience. "
                                          f"{tz.get('compare_label', 'What the full version adds')}: {tz.get('compare_url', '')}")}
        # sources (backup)
        src = [f"{i + 1}. {s.get('title', '')}" + (f" ({s.get('publisher')}, {s.get('date')})" if s.get("publisher") else "")
               for i, s in enumerate(self.sources)]
        # keep the list inside the slide: about 1,100 characters, or 10 lines, whichever comes first
        kept, used = [], 0
        for line in src:
            if len(kept) == 10 or used + len(line) > 1100:
                break
            kept.append(line)
            used += max(len(line), 90)
        if len(kept) < len(src):
            kept.append(f"…and {len(src) - len(kept)} more, listed in case.json and on the poster")
        src = kept
        caveat = (f"{self.unchecked} of {len(self.sources)} sources were read from search extracts; check them against the documents before client use"
                  if self.unchecked else "Figures as reported by each company for its own fiscal year")
        out["sources"] = {"title": "Every figure comes from a public filing, results release or management statement listed here",
                          "items": src, "note": caveat}
        return out


# --------------------------------------------------------------------------
# chart-data.xlsx: the data behind every chart placeholder
# --------------------------------------------------------------------------

def write_chart_data(case, a, path):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    bold, body = Font(bold=True, name="Arial", size=10), Font(name="Arial", size=10)
    names = {c["id"]: c.get("short_name") or c["name"] for c in case["companies"]}
    growth = a["meta"].get("growth_metric", "revenue_cagr")
    for k in ["ebit_margin", growth, "gross_margin", "sga_pct", "dso", "dio", "dpo", "ccc"]:
        m, st = METRIC[k], a["stats"][k]
        rows = [(names[c], a["values"][c][k]["value"], c == a["meta"]["target_id"]) for c in names if a["values"][c][k]["value"] is not None]
        if not rows:
            continue
        rows.sort(key=lambda r: r[1], reverse=(m.direction != "lower"))
        ws = wb.create_sheet(m.short[:31])
        for col, h in enumerate(["Company", m.label + (" (%)" if m.unit == "pct" else " (days)"), "Peer median", "Top quartile", "Target"], 1):
            ws.cell(row=1, column=col, value=h).font = bold
        scale = 100 if m.unit == "pct" else 1
        for r, (n, v, is_t) in enumerate(rows, 2):
            vals = [n, round(v * scale, 2), round(st["median"] * scale, 2) if st["median"] is not None else None,
                    round(st["top_quartile"] * scale, 2) if st["top_quartile"] is not None else None, "yes" if is_t else ""]
            for c, val in enumerate(vals, 1):
                ws.cell(row=r, column=c, value=val).font = body
        ws.cell(row=len(rows) + 3, column=1, value=f"Sorted best to worst ({'higher' if m.direction != 'lower' else 'lower'} is better). "
                "Source: company filings; public-data opportunity scan").font = Font(name="Arial", size=8, italic=True)
    b = a["bridge"]
    if b:
        ws = wb.create_sheet("EBIT bridge")
        for col, h in enumerate(["Step", "Low", "High"], 1):
            ws.cell(row=1, column=col, value=h).font = bold
        steps = [("EBIT " + b["latest"]["period"], b["latest"]["ebit"], b["latest"]["ebit"])] + \
                [(s["name"], s["low"], s["high"]) for s in b["steps"]] + [("EBIT potential", b["target"]["low"], b["target"]["high"])]
        for r, (n, lo, hi) in enumerate(steps, 2):
            for c, val in enumerate([n, round(lo, 1), round(hi, 1)], 1):
                ws.cell(row=r, column=c, value=val).font = body
    nwc = next(x for x in a["buckets"] if x["id"] == "working_capital")
    sized = [lv for lv in nwc["levers"] if lv["state"] == "sized"]
    if sized:
        ws = wb.create_sheet("Working capital")
        for col, h in enumerate(["Lever", "Gap", "Cash low", "Cash high"], 1):
            ws.cell(row=1, column=col, value=h).font = bold
        for r, lv in enumerate(sized, 2):
            for c, val in enumerate([lv["label"], lv["gap_display"], round(lv["low"], 1), round(lv["high"], 1)], 1):
                ws.cell(row=r, column=c, value=val).font = body
    wb.save(path)


# --------------------------------------------------------------------------
# Bain style, through the bain-slides skill
# --------------------------------------------------------------------------

def find_bain_skill(explicit=None):
    if explicit:
        return explicit if os.path.exists(os.path.join(explicit, "scripts", "prepare_deck.py")) else None
    for root in BAIN_SEARCH_ROOTS:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, files in os.walk(root):
            if os.path.basename(dirpath) == "bain-slides" and "SKILL.md" in files and \
                    os.path.exists(os.path.join(dirpath, "scripts", "prepare_deck.py")):
                return dirpath
            if dirpath.count(os.sep) - root.count(os.sep) > 4:
                dirnames[:] = []
    return None


def _run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{os.path.basename(cmd[1])} failed:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
    return r.stdout


def _table_slide(bain, title, headers, rows, footnote, col_widths_ratio):
    """A plain text table on the Bain symbol-table template; returns (zip bytes, slide index)."""
    sys.path.insert(0, os.path.join(bain, "scripts"))
    from slide_editor import SAFE_WIDTH, SlideEditor, duplicate_slide, normalize_symbol_table_style, write_output
    with open(os.path.join(bain, "templates", "symbol-tables-template.pptx"), "rb") as f:
        zb = f.read()
    zb = duplicate_slide(zb, 0)
    with zipfile.ZipFile(io.BytesIO(zb)) as z:
        pres_xml = z.read("ppt/presentation.xml").decode()
        pres_rels = z.read("ppt/_rels/presentation.xml.rels").decode()
    rids = re.findall(r'<p:sldId[^>]+r:id="([^"]+)"', pres_xml)
    r2t = dict(re.findall(r'Id="([^"]+)"[^>]+Target="([^"]+)"', pres_rels))
    paths = ["ppt/" + r2t[r] for r in rids]
    target = paths[-1]
    with zipfile.ZipFile(io.BytesIO(zb)) as z:
        slide_xml = z.read(target)
        rels = z.read(target.replace("ppt/slides/", "ppt/slides/_rels/").replace(".xml", ".xml.rels")).decode()
    ed = SlideEditor(slide_xml, slide_rels_xml=rels)
    ed.set_title(title)
    n_cols, n_rows = len(headers), len(rows) + 1
    if n_cols < 9:
        ed.delete_cols(list(range(n_cols, 9)))
    if n_rows < 9:
        ed.delete_rows(list(range(n_rows, 9)))
    while n_rows > 9:
        ed.add_row()
        n_rows -= 1
    total = sum(col_widths_ratio)
    widths = [round(SAFE_WIDTH * w / total) for w in col_widths_ratio]
    widths[-1] = SAFE_WIDTH - sum(widths[:-1])
    ed.set_col_widths(widths)
    for c, h in enumerate(headers):
        ed.set_cell_text(0, c, h)
    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            ed.set_cell_text(r, c, val)
    ed.update_legend([])
    ed.set_footnote(footnote)
    ed.remove_comment_boxes()
    normalize_symbol_table_style(ed)
    from lxml import etree
    tree = etree.fromstring(ed.get_bytes())
    ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
          "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    for gf in tree.findall(".//p:graphicFrame", ns):
        name = gf.find(".//p:cNvPr", ns).get("name", "")
        if gf.find(".//a:tbl", ns) is not None and not name.startswith("btfpTable"):
            gf.getparent().remove(gf)  # the legend table, which a plain text table has no use for
    slide_bytes = etree.tostring(tree, xml_declaration=True, encoding="UTF-8", standalone=True)
    tmp = tempfile.mktemp(suffix=".pptx")
    write_output(zb, {target: slide_bytes}, tmp)
    with open(tmp, "rb") as f:
        data = f.read()
    os.unlink(tmp)
    return data, len(paths) - 1


def _chart_placeholder(deck_path, slide_index, text):
    """Dashed placeholder in the chart column (column 0) below its header, as the Bain charts runbook does."""
    from lxml import etree
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.oxml.ns import qn
    from pptx.util import Pt
    prs = Presentation(deck_path)
    slide = prs.slides[slide_index]
    headers = sorted([s for s in slide.shapes if "btfpColumnHeader" in s.name], key=lambda s: s.left)
    if not headers:
        return
    h = headers[0]
    notes = [s.top for s in slide.shapes if "NotesBox" in s.name or "Source" in s.name]
    top = h.top + h.height + 91440
    bottom = (min(notes) if notes else int(prs.slide_height * 0.88)) - 182880
    box = slide.shapes.add_textbox(h.left, top, h.width, max(bottom - top, 1_500_000))
    box.name = "Chart placeholder"
    tf = box.text_frame
    tf.word_wrap = True
    from pptx.enum.text import MSO_AUTO_SIZE
    tf.auto_size = MSO_AUTO_SIZE.NONE  # keep the full column height, so the space for the chart is visible
    p = tf.paragraphs[0]
    p.text = text
    run = p.runs[0]
    run.font.size = Pt(11)
    run.font.italic = True
    run.font.name = "Arial"
    run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
    ln = etree.SubElement(box._element.spPr, qn("a:ln"))
    ln.set("w", "12700")
    sf = etree.SubElement(ln, qn("a:solidFill"))
    etree.SubElement(sf, qn("a:srgbClr")).set("val", "AAAAAA")
    etree.SubElement(ln, qn("a:prstDash")).set("val", "dash")
    prs.save(deck_path)


def build_bain(c, out_path, bain):
    work = tempfile.mkdtemp(prefix="opscan-deck-")
    deck = os.path.join(work, "deck.pptx")
    plan = ["exec-summary", "column-2", "column-3", "table", "column-2"] + (["table"] if "invite" in c else []) + ["column-1"]
    _run([sys.executable, os.path.join(bain, "scripts", "prepare_deck.py"), deck, "--plan", ",".join(plan),
          "--build-type", "no-charts"], work)
    manifest_path = os.path.join(work, "deck_manifest.json")
    man = json.load(open(manifest_path))
    content_idx = [s["index"] for s in man["slide_map"] if s["type"] in ("content", "exec_summary")]
    exec_i, perf_i, cfc_i, bridge_i, src_i = content_idx[:5]
    bl, hdr = ("btfpBulletedList.pptx", "btfpBulletedList216308"), ("btfpColumnHeaderBox.pptx", "btfpColumnHeaderBox145096")

    def shapes(n, with_headers=True):
        s = []
        for col in range(n):
            if with_headers:
                s.append({"file": hdr[0], "shape": hdr[1], "column": col})
            s.append({"file": bl[0], "shape": bl[1], "column": col})
        return s
    sticker = c["sticker"]
    src_line = "Source: Company filings, results releases and earnings calls; public-data opportunity scan"
    spec = [
        {"slide_index": 0, "title": c["title"]["title"], "subtitle": c["title"]["subtitle"]},
        {"slide_index": exec_i, "slide_type": "exec_summary", "title": "Executive summary", "status_sticker": sticker,
         "bullets": [{"column": 0, "items": [{"level": 0, "text": x} for x in c["exec"]]}]},
        {"slide_index": perf_i, "title": c["perf"]["title"], "status_sticker": sticker,
         "headers": [{"column": 0, "text": c["perf"]["chart_header"]}, {"column": 1, "text": "Commentary"}],
         "bullets": [{"column": 1, "items": [{"level": 0, "text": x} for x in c["perf"]["bullets"]]}],
         "source": src_line, "shapes": [{"file": hdr[0], "shape": hdr[1], "column": 0}, {"file": hdr[0], "shape": hdr[1], "column": 1},
                                        {"file": bl[0], "shape": bl[1], "column": 1}]},
        {"slide_index": cfc_i, "title": c["cfc"]["title"], "status_sticker": sticker,
         "headers": [{"column": i, "text": col["header"]} for i, col in enumerate(c["cfc"]["cols"])],
         "bullets": [{"column": i, "items": [{"level": 0, "text": x} for x in col["items"]]} for i, col in enumerate(c["cfc"]["cols"])],
         "source": src_line, "shapes": shapes(len(c["cfc"]["cols"]))},
        {"slide_index": bridge_i, "title": c["bridge"]["title"], "status_sticker": sticker,
         "headers": [{"column": 0, "text": c["bridge"]["chart_header"]}, {"column": 1, "text": "Why the value is real"}],
         "bullets": [{"column": 1, "items": [{"level": 0, "text": x} for x in c["bridge"]["bullets"]]}],
         "source": src_line, "shapes": [{"file": hdr[0], "shape": hdr[1], "column": 0}, {"file": hdr[0], "shape": hdr[1], "column": 1},
                                        {"file": bl[0], "shape": bl[1], "column": 1}]},
        {"slide_index": src_i, "title": c["sources"]["title"], "status_sticker": "Backup",
         "bullets": [{"column": 0, "items": [{"level": 0, "text": x} for x in c["sources"]["items"]]}],
         "note": c["sources"]["note"], "shapes": [{"file": bl[0], "shape": bl[1], "column": 0}]},
    ]
    if len(c["cfc"]["cols"]) < 3:
        raise CaseError("the Bain deck needs three framings for the case-for-change slide")
    spec_path = os.path.join(work, "slides.json")
    json.dump(spec, open(spec_path, "w"), ensure_ascii=False, indent=1)
    _run([sys.executable, os.path.join(bain, "scripts", "build_slide.py"), deck, "--spec", spec_path,
          "--manifest", manifest_path, "--quiet", "--auto-approve"], work)
    _chart_placeholder(deck, perf_i, c["perf"]["chart_text"])
    _chart_placeholder(deck, bridge_i, c["bridge"]["chart_text"])

    # tables, injected in plan order
    sys.path.insert(0, os.path.join(bain, "scripts"))
    from inject_table_slide import inject_table_slide
    tables = [e for e in json.load(open(manifest_path))["plan"] if e["type"] == "table"]
    specs = [("prize", [2.2, 1.1, 2.6, 1.3, 2.0])] + ([("invite", [1.2, 2.2, 3.2])] if "invite" in c else [])
    for (key, widths), entry in zip(specs, tables):
        tbl = c[key]
        data, idx = _table_slide(bain, tbl["title"], tbl["headers"], tbl["rows"], tbl["footnote"], widths)
        inject_table_slide(deck_path=deck, sym_zb=data, slide_index=idx, after_index=entry["after_index"])
    _run([sys.executable, os.path.join(bain, "scripts", "finalize_deck.py"), deck, "--copy-to", out_path, "--validate", "warn"], work)
    shutil.rmtree(work, ignore_errors=True)


# --------------------------------------------------------------------------
# Neutral style: python-pptx with native charts
# --------------------------------------------------------------------------

def build_neutral(c, a, case, out_path):
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
    from pptx.util import Emu, Pt
    INK, INK2, BLUE, LIGHT, GREY = (RGBColor(0x16, 0x18, 0x1D), RGBColor(0x52, 0x51, 0x4E), RGBColor(0x2A, 0x78, 0xD6),
                                    RGBColor(0x9E, 0xC5, 0xF4), RGBColor(0xB4, 0xB2, 0xA9))
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    W, H, M = prs.slide_width, prs.slide_height, Emu(457200)
    blank = prs.slide_layouts[6]

    def text(slide, x, y, w, h, paras, size=14, color=INK, bold_first=False):
        box = slide.shapes.add_textbox(x, y, w, h)
        tf = box.text_frame
        tf.word_wrap = True
        for i, ptxt in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            parts = re.split(r"(\*\*.+?\*\*)", ptxt)
            for part in parts:
                if not part:
                    continue
                r = p.add_run()
                r.text = part.strip("*") if part.startswith("**") else part
                r.font.size, r.font.name, r.font.color.rgb = Pt(size), "Arial", color
                r.font.bold = part.startswith("**") or (bold_first and i == 0)
            p.space_after = Pt(6)
        return box

    def slide_with_title(title, sticker=None):
        s = prs.slides.add_slide(blank)
        text(s, M, Emu(300000), W - 2 * M, Emu(900000), [title], size=24)
        if sticker:
            text(s, W - M - Emu(1600000), Emu(80000), Emu(1600000), Emu(260000), [sticker.upper()], size=9, color=INK2)
        return s

    s = prs.slides.add_slide(blank)
    text(s, M, Emu(2200000), W - 2 * M, Emu(1000000), [c["title"]["title"]], size=36, bold_first=True)
    text(s, M, Emu(3300000), W - 2 * M, Emu(1200000), c["title"]["subtitle"].split("\n"), size=16, color=INK2)
    s = slide_with_title("Executive summary", c["sticker"])
    text(s, M, Emu(1300000), W - 2 * M, H - Emu(1800000), ["• " + x for x in c["exec"]], size=15)

    # performance: native bar chart of EBIT margin, sorted best to worst
    s = slide_with_title(c["perf"]["title"], c["sticker"])
    names = {x["id"]: x.get("short_name") or x["name"] for x in case["companies"]}
    rows = sorted([(names[i], a["values"][i]["ebit_margin"]["value"]) for i in names if a["values"][i]["ebit_margin"]["value"] is not None],
                  key=lambda r: r[1], reverse=True)
    cd = CategoryChartData()
    cd.categories = [r[0] for r in rows]
    cd.add_series("EBIT margin", [round(r[1] * 100, 1) for r in rows])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, M, Emu(1400000), Emu(5600000), Emu(4600000), cd)
    ch = gf.chart
    ch.has_legend = False
    ch.plots[0].has_data_labels = True
    ch.plots[0].data_labels.number_format, ch.plots[0].data_labels.number_format_is_linked = '0.0"%"', False
    ch.plots[0].data_labels.font.size = Pt(10)
    ch.category_axis.reverse_order = True
    ch.category_axis.tick_labels.font.size = Pt(10)
    ch.value_axis.visible = False
    ch.value_axis.has_major_gridlines = False
    target_name = names[a["meta"]["target_id"]]
    for i, pt in enumerate(ch.plots[0].series[0].points):
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = BLUE if rows[i][0] == target_name else GREY
    text(s, Emu(6400000), Emu(1400000), W - Emu(6400000) - M, Emu(4600000), ["**Commentary**"] + ["• " + x for x in c["perf"]["bullets"]], size=12)

    s = slide_with_title(c["cfc"]["title"], c["sticker"])
    colw = (W - 2 * M - Emu(400000)) // 3
    for i, col in enumerate(c["cfc"]["cols"]):
        x = M + i * (colw + Emu(200000))
        text(s, x, Emu(1350000), colw, Emu(700000), [f"**{col['header']}**"], size=14)
        text(s, x, Emu(2100000), colw, Emu(4000000), ["• " + it for it in col["items"]], size=11)

    def table_slide(tbl, widths):
        s = slide_with_title(tbl["title"], c["sticker"])
        n_r, n_c = len(tbl["rows"]) + 1, len(tbl["headers"])
        shape = s.shapes.add_table(n_r, n_c, M, Emu(1400000), W - 2 * M, Emu(400000 * n_r))
        t = shape.table
        tot = sum(widths)
        for j, w in enumerate(widths):
            t.columns[j].width = Emu(int((W - 2 * M) * w / tot))
        for j, h in enumerate(tbl["headers"]):
            t.cell(0, j).text = h
        for i, row in enumerate(tbl["rows"], 1):
            for j, v in enumerate(row):
                t.cell(i, j).text = v
        for i in range(n_r):
            for j in range(n_c):
                for p in t.cell(i, j).text_frame.paragraphs:
                    for r in p.runs:
                        r.font.size, r.font.name = Pt(11), "Arial"
                        r.font.bold = i == 0
        text(s, M, H - Emu(800000), W - 2 * M, Emu(600000), tbl["footnote"].split("\n"), size=9, color=INK2)

    table_slide(c["prize"], [2.2, 1.1, 2.6, 1.3, 2.0])

    s = slide_with_title(c["bridge"]["title"], c["sticker"])
    b = a["bridge"]
    if b:
        cats, base, low, ext = [], [], [], []
        run_lo = b["latest"]["ebit"]
        cats.append("EBIT " + b["latest"]["period"]); base.append(0); low.append(b["latest"]["ebit"]); ext.append(0)
        for st in b["steps"]:
            cats.append(st["name"].split(":")[0]); base.append(run_lo); low.append(st["low"]); ext.append(st["high"] - st["low"])
            run_lo += st["low"]
        cats.append("EBIT potential"); base.append(0); low.append(b["target"]["low"]); ext.append(b["target"]["high"] - b["target"]["low"])
        cd = CategoryChartData()
        cd.categories = cats
        cd.add_series("base", [round(v, 1) for v in base])
        cd.add_series("Gap to peer median", [round(v, 1) for v in low])
        cd.add_series("Further to top quartile", [round(v, 1) for v in ext])
        gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, M, Emu(1400000), Emu(6200000), Emu(4500000), cd)
        ch = gf.chart
        ch.has_legend, ch.legend.position, ch.legend.include_in_layout = True, XL_LEGEND_POSITION.BOTTOM, False
        ch.legend.font.size = Pt(10)
        ch.value_axis.has_major_gridlines = False
        ch.category_axis.tick_labels.font.size = Pt(10)
        ch.value_axis.tick_labels.font.size = Pt(9)
        sers = ch.plots[0].series
        sers[0].format.fill.background()
        from pptx.oxml.ns import qn
        from lxml import etree
        leg = ch._chartSpace.find(".//" + qn("c:legend"))
        entry = etree.SubElement(leg, qn("c:legendEntry"))  # hide the invisible base series from the legend
        etree.SubElement(entry, qn("c:idx")).set("val", "0")
        etree.SubElement(entry, qn("c:delete")).set("val", "1")
        leg.remove(entry)
        leg.insert(1, entry)
        for ser, col in ((sers[1], BLUE), (sers[2], LIGHT)):
            ser.format.fill.solid()
            ser.format.fill.fore_color.rgb = col
        ch.plots[0].gap_width = 60
    text(s, Emu(7000000), Emu(1400000), W - Emu(7000000) - M, Emu(4600000), ["**Why the value is real**"] + ["• " + x for x in c["bridge"]["bullets"]], size=12)
    if "invite" in c:
        table_slide(c["invite"], [1.2, 2.2, 3.2])
    s = slide_with_title(c["sources"]["title"], "Backup")
    text(s, M, Emu(1300000), W - 2 * M, H - Emu(2000000), c["sources"]["items"], size=10)
    text(s, M, H - Emu(700000), W - 2 * M, Emu(500000), [c["sources"]["note"]], size=9, color=INK2)
    prs.save(out_path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("case")
    ap.add_argument("-o", "--out", default="deck.pptx")
    ap.add_argument("--style", choices=["auto", "bain", "neutral"], default="auto")
    ap.add_argument("--bain-skill", help="folder of the bain-slides skill, if it is not found automatically")
    args = ap.parse_args()
    case = json.load(open(args.case, encoding="utf-8"))
    try:
        a = compute(case)
        c = Content(case, a).build()
    except CaseError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    xlsx = os.path.join(os.path.dirname(os.path.abspath(args.out)), "chart-data.xlsx")
    write_chart_data(case, a, xlsx)
    style = args.style
    bain = find_bain_skill(args.bain_skill) if style in ("auto", "bain") else None
    if style == "bain" and not bain:
        print("error: --style bain needs the bain-slides skill; pass --bain-skill or use --style neutral", file=sys.stderr)
        return 1
    if bain:
        # The Bain pipeline refuses text that overflows a column. Tighten the text a step at a time and rebuild.
        for tight in range(4):
            c = Content(case, a, tight).build()
            try:
                build_bain(c, os.path.abspath(args.out), bain)
                break
            except RuntimeError as e:
                if "overflow" not in str(e).lower() or tight == 3:
                    print(f"error: {e}", file=sys.stderr)
                    return 1
                print(f"text too long for a slide at level {tight}; tightening and rebuilding")
        print(f"wrote {args.out} (Bain Core template; charts are placeholders, data in {xlsx})")
    else:
        build_neutral(c, a, case, args.out)
        print(f"wrote {args.out} (neutral template with native charts; chart data also in {xlsx})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
