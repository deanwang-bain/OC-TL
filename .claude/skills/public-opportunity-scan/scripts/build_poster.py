#!/usr/bin/env python3
"""Build an A1 landscape opportunity-scan poster from a case file.

    python build_poster.py case.json -o poster.html

Writes poster.html and analysis.json (every computed number, for audit) beside
it. Prints warnings: missing sources, unresolved {{tokens}}, and numbers typed
into narrative instead of cited. Exit code 2 when a token does not resolve,
because a poster with "[missing: ...]" on it is not finished.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from opscan_calc import (METRIC, CaseError, compute, fmt_metric, fmt_money,  # noqa: E402
                         fmt_pct_range, fmt_range, lint_numbers, resolve_tokens)

# Colours by role. Swap these for a house style; nothing else needs to change.
TOKENS = {
    "surface": "#fcfcfb", "page": "#f9f9f7", "ink": "#0b0b0b", "ink2": "#52514e", "muted": "#898781",
    "grid": "#e1e0d9", "axis": "#c3c2b7", "target": "#2a78d6", "target_light": "#9ec5f4",
    "target_dark": "#184f95", "peer": "#b4b2a9", "peer_na": "#e1e0d9", "tq": "#eb6834",
    "good": "#006300", "bad": "#b42323",
}

esc = html.escape


def nice_ticks(lo, hi, n=4):
    """Round tick values covering lo..hi, about n intervals."""
    import math
    span = (hi - lo) or 1.0
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    start = math.floor(lo / step) * step
    ticks, v = [], start
    while True:
        ticks.append(round(v, 10))
        if v >= hi - step * 1e-9:
            break
        v += step
    return ticks


class Renderer:
    def __init__(self, case, analysis):
        self.case = case
        self.a = analysis
        self.facts = analysis["facts"]
        self.missing: list[str] = []
        self.typed_numbers: list[tuple[str, str]] = []
        self.cur = analysis["meta"]["currency"]
        self.sources = case.get("sources", [])
        self.src_num = {s["id"]: i + 1 for i, s in enumerate(self.sources)}
        self.signals = {g["id"]: g for g in case.get("signals", [])}
        self.companies = {c["id"]: c for c in case["companies"]}
        self.tid = analysis["meta"]["target_id"]

    # ---- text helpers --------------------------------------------------
    def text(self, s, where=""):
        """Escape, check for typed numbers, resolve {{tokens}}, allow **bold**."""
        if not s:
            return ""
        for n in lint_numbers(s):
            self.typed_numbers.append((where, n))
        out = resolve_tokens(esc(s), self.facts, self.missing)
        out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
        return out

    def cite(self, src_id):
        n = self.src_num.get(src_id)
        return f'<sup class="cite">[{n}]</sup>' if n else ""

    def name(self, cid):
        c = self.companies[cid]
        return c.get("short_name") or c["name"]

    # ---- charts --------------------------------------------------------
    def bar_chart(self, key, width=300):
        m = METRIC[key]
        st = self.a["stats"][key]
        vals = self.a["values"]
        rows, na_rows = [], []
        for cid, c in self.companies.items():
            v = vals[cid][key]
            if v["value"] is None:
                na_rows.append((cid, v.get("na_reason")))
            else:
                rows.append((cid, v["value"], cid == self.tid, v.get("excluded")))
        if not rows:
            return '<p class="na">No company reports this metric.</p>'
        rows.sort(key=lambda r: r[1], reverse=(m.direction != "lower"))
        row_h, bar_h, label_w, right_pad, top = 15, 9, 92, 44, 16
        h = top + row_h * len(rows) + 6
        lo = min(0.0, min(r[1] for r in rows), st["median"] or 0, st["top_quartile"] or 0)
        hi = max(0.0, max(r[1] for r in rows), st["median"] or 0, st["top_quartile"] or 0)
        span = (hi - lo) or 1.0
        plot_w = width - label_w - right_pad

        def x(v):
            return label_w + (v - lo) / span * plot_w

        T = TOKENS
        parts = [f'<svg viewBox="0 0 {width} {h}" class="chart" role="img" aria-label="{esc(m.label)} by company">']
        x0 = x(0)
        for i, (cid, v, is_t, excl) in enumerate(rows):
            y = top + i * row_h + (row_h - bar_h) / 2
            fill = T["target"] if is_t else (T["peer_na"] if excl else T["peer"])
            parts.append(self._hbar(x0, x(v), y, bar_h, fill, f"{self.name(cid)}: {fmt_metric(v, m.unit)}"))
            weight = ' font-weight="700"' if is_t else ""
            label = self.name(cid)
            if len(label) > 17:
                label = label[:16] + "…"
            parts.append(f'<text x="{label_w - 4}" y="{y + bar_h - 1.5}" text-anchor="end" class="lab"{weight}>{esc(label)}</text>')
            tip = max(x(v), x0) + 3
            vtxt = fmt_metric(v, m.unit) + (" (excl.)" if excl else "") + (" †" if vals[cid][key].get("note") else "")
            parts.append(f'<text x="{tip}" y="{y + bar_h - 1.5}" class="val"{weight}>{esc(vtxt)}</text>')
        parts.append(f'<line x1="{x0}" x2="{x0}" y1="{top - 2}" y2="{h - 4}" stroke="{T["axis"]}" stroke-width="1"/>')
        if st["median"] is not None:
            for val, color, lab, anchor_dy in ((st["median"], T["ink2"], "Median", 0), (st["top_quartile"], T["tq"], "Top quartile", 0)):
                xv = x(val)
                parts.append(f'<line x1="{xv}" x2="{xv}" y1="{top - 2}" y2="{h - 4}" stroke="{color}" stroke-width="1.5"/>')
            xm, xq = x(st["median"]), x(st["top_quartile"])
            # keep the two reference labels apart
            left_first = xm <= xq
            parts.append(f'<text x="{xm}" y="{top - 5}" text-anchor="{"end" if left_first else "start"}" class="ref">Median {esc(fmt_metric(st["median"], m.unit))}</text>')
            parts.append(f'<text x="{xq}" y="{top - 5}" text-anchor="{"start" if left_first else "end"}" class="ref tq">Top quartile {esc(fmt_metric(st["top_quartile"], m.unit))}</text>')
        parts.append("</svg>")
        out = "".join(parts)
        if any(vals[c][key].get("note") for c, *_ in rows):
            out_note = '<p class="chart-na">† margin as published by the company; the amounts behind it are not available</p>'
        else:
            out_note = ""
        if na_rows:
            items = "; ".join(f"{esc(self.name(c))} ({esc(r or 'not reported')})" for c, r in na_rows)
            out += f'<p class="chart-na">n/a: {items}</p>'
        return out + out_note

    @staticmethod
    def _hbar(xa, xb, y, h, fill, title):
        """Horizontal bar, square at the baseline, 2-unit rounded data end."""
        r = min(2.0, abs(xb - xa) / 2)
        if xb >= xa:
            d = (f"M{xa},{y} H{xb - r} Q{xb},{y} {xb},{y + r} V{y + h - r} Q{xb},{y + h} {xb - r},{y + h} H{xa} Z")
        else:
            d = (f"M{xa},{y} H{xb + r} Q{xb},{y} {xb},{y + r} V{y + h - r} Q{xb},{y + h} {xb + r},{y + h} H{xa} Z")
        return f'<path d="{d}" fill="{fill}"><title>{esc(title)}</title></path>'

    def segments(self, segs):
        """Segment table: reported figures, each with its source."""
        rows = []
        for sg in segs:
            from opscan_calc import read_value
            rv, rsrc, _ = read_value(sg.get("revenue"))
            gv, gsrc, _ = read_value(sg.get("growth"))
            mv, msrc, _ = read_value(sg.get("margin"))
            for v, src, what in ((rv, rsrc, "revenue"), (gv, gsrc, "growth"), (mv, msrc, "margin")):
                if v is not None and not src:
                    self.typed_numbers.append((f"segment {sg.get('name')}", f"{what} without a source"))
            cites = "".join(self.cite(x) for x in dict.fromkeys(x for x in (rsrc, gsrc, msrc) if x))
            rows.append(f"<tr><td>{esc(sg.get('name', ''))}{cites}</td><td class='num'>{esc(fmt_money(rv, self.cur))}</td>"
                        f"<td class='num'>{esc(fmt_metric(gv, 'pct'))}</td><td class='num'>{esc(fmt_metric(mv, 'pct'))}</td>"
                        f"<td>{self.text(sg.get('note', ''), 'segments')}</td></tr>")
        per = segs[0].get("period", "") if segs else ""
        return (f'<h3>Where the business sits{(" · " + esc(per)) if per else ""}</h3><table class="segs"><thead><tr><th>Segment</th><th>Revenue</th>'
                f'<th>Growth</th><th>Margin</th><th></th></tr></thead><tbody>{"".join(rows)}</tbody></table>')

    def scatter(self, growth_key, width=300):
        """Valuation multiple against growth: what the market pays for growth."""
        T = TOKENS
        vals = self.a["values"]
        pts = [(cid, vals[cid][growth_key]["value"], vals[cid]["valuation"]["value"]) for cid in self.companies
               if vals[cid][growth_key]["value"] is not None and vals[cid]["valuation"]["value"] is not None]
        label = self.case.get("meta", {}).get("valuation_label", "Valuation multiple")
        head = (f'<figure class="fig"><figcaption><strong>{esc(label)} against {esc(METRIC[growth_key].label.lower())}</strong><br>'
                f'<span class="sub">what the market pays for growth · market data as dated in sources</span></figcaption>')
        if len(pts) < 4:
            return head + '<p class="na">Fewer than four companies have both figures.</p></figure>'
        h, l, r, t, b = 200, 30, 12, 12, 26
        xs, ys = [p[1] for p in pts], [p[2] for p in pts]
        xt = nice_ticks(min(xs + [0.0]), max(xs + [0.0]))
        yt = nice_ticks(0.0, max(ys) * 1.05)
        x_lo, x_hi = min(xt[0], min(xs)), max(xt[-1], max(xs))
        y_lo, y_hi = 0.0, max(yt[-1], max(ys))

        def X(v):
            return l + (v - x_lo) / (x_hi - x_lo) * (width - l - r)

        def Y(v):
            return t + (1 - (v - y_lo) / (y_hi - y_lo)) * (h - t - b)

        parts = [f'<svg viewBox="0 0 {width} {h}" class="chart" role="img" aria-label="{esc(label)} against growth">']
        for yv in yt:
            parts.append(f'<line x1="{l}" x2="{width - r}" y1="{Y(yv)}" y2="{Y(yv)}" stroke="{T["grid"]}"/>'
                         f'<text x="{l - 4}" y="{Y(yv) + 3}" text-anchor="end" class="lab">{yv:.0f}x</text>')
        parts.append(f'<line x1="{X(0)}" x2="{X(0)}" y1="{t}" y2="{h - b}" stroke="{T["axis"]}"/>')
        for xv in xt:
            parts.append(f'<text x="{X(xv)}" y="{h - b + 11}" text-anchor="middle" class="lab">{xv * 100:.0f}%</text>')
        parts.append(f'<text x="{(l + width - r) / 2}" y="{h - 3}" text-anchor="middle" class="lab">{esc(METRIC[growth_key].short)}</text>')
        placed = []

        def place(xa, ya, text_w, anchor):
            x1 = xa - text_w if anchor == "end" else xa
            for dy in (0, -9, 9, -18, 18, -27, 27):
                y1 = ya + dy
                if all(not (x1 < bx2 and x1 + text_w > bx1 and abs(y1 - by) < 9) for bx1, bx2, by in placed):
                    placed.append((x1, x1 + text_w, y1))
                    return y1
            placed.append((x1, x1 + text_w, ya))
            return ya

        for cid, gx, vy in sorted(pts, key=lambda p: (p[0] != self.tid, -p[2])):
            is_t = cid == self.tid
            fill = T["target"] if is_t else T["peer"]
            rad = 4.5 if is_t else 3.5
            parts.append(f'<circle cx="{X(gx)}" cy="{Y(vy)}" r="{rad}" fill="{fill}" stroke="{T["surface"]}" stroke-width="2">'
                         f'<title>{esc(self.name(cid))}: {esc(fmt_metric(gx, "pct"))}, {vy:.1f}x</title></circle>')
            anchor = "end" if X(gx) > width - 70 else "start"
            dx = -6 if anchor == "end" else 6
            w = ' font-weight="700"' if is_t else ""
            txt = f"{self.name(cid)} {vy:.1f}x"
            ly = place(X(gx) + dx, Y(vy) + 3, len(txt) * 4.4, anchor)
            parts.append(f'<text x="{X(gx) + dx}" y="{ly}" text-anchor="{anchor}" class="val"{w}>{esc(txt)}</text>')
        parts.append("</svg>")
        return head + "".join(parts) + "</figure>"

    def waterfall(self, width=340):
        b = self.a["bridge"]
        if not b:
            return '<p class="na">No EBIT bridge: the target does not report EBIT.</p>'
        T = TOKENS
        cols = [("latest", f"EBIT {b['latest']['period']}", b["latest"]["ebit"], b["latest"]["ebit"], 0.0)]
        run_lo = b["latest"]["ebit"]
        run_hi = b["latest"]["ebit"]
        for s in b["steps"]:
            cols.append(("step", s["name"].split(":")[0], s["low"], s["high"], run_lo))
            run_lo += s["low"]
            run_hi += s["high"]
        cols.append(("target", "EBIT potential", b["target"]["low"], b["target"]["high"], 0.0))
        top_v = max(run_hi, b["latest"]["ebit"]) * 1.12
        h, top, base_h = 230, 26, 40
        plot_h = h - top - base_h
        n = len(cols)
        slot = (width - 20) / n
        bw = min(46.0, slot * 0.62)

        def y(v):
            return top + plot_h - v / top_v * plot_h

        parts = [f'<svg viewBox="0 0 {width} {h}" class="chart" role="img" aria-label="EBIT bridge">']
        parts.append(f'<line x1="10" x2="{width - 10}" y1="{y(0)}" y2="{y(0)}" stroke="{T["axis"]}"/>')
        prev_top = None
        for i, (kind, label, lo, hi, start) in enumerate(cols):
            cx = 10 + slot * i + slot / 2
            x0 = cx - bw / 2
            if kind in ("latest", "target"):
                fill = T["target_dark"]
                parts.append(f'<rect x="{x0}" y="{y(lo)}" width="{bw}" height="{y(0) - y(lo)}" fill="{fill}" rx="2"><title>{esc(label)}: {esc(fmt_money(lo, self.cur))}</title></rect>')
                if hi > lo:
                    parts.append(f'<rect x="{x0}" y="{y(hi)}" width="{bw}" height="{y(lo) - y(hi)}" fill="{T["target_light"]}" rx="2"/>')
                txt = fmt_money(lo, self.cur) if kind == "latest" else fmt_range(lo, hi, self.cur)
                parts.append(f'<text x="{cx}" y="{y(hi) - 5}" text-anchor="middle" class="val strong">{esc(txt)}</text>')
            else:
                parts.append(f'<rect x="{x0}" y="{y(start + lo)}" width="{bw}" height="{max(0.5, y(start) - y(start + lo))}" fill="{T["target"]}" rx="2"><title>{esc(label)}: {esc(fmt_range(lo, hi, self.cur))}</title></rect>')
                if hi > lo:
                    parts.append(f'<rect x="{x0}" y="{y(start + hi)}" width="{bw}" height="{y(start + lo) - y(start + hi)}" fill="{T["target_light"]}" rx="2"/>')
                parts.append(f'<text x="{cx}" y="{y(start + hi) - 5}" text-anchor="middle" class="val">+{esc(fmt_range(lo, hi, self.cur))}</text>')
            if prev_top is not None:
                parts.append(f'<line x1="{prev_top[0]}" x2="{x0}" y1="{prev_top[1]}" y2="{prev_top[1]}" stroke="{T["axis"]}" stroke-width="1"/>')
            prev_top = (x0 + bw, y(start + lo) if kind == "step" else y(lo))
            words = label.split()
            lines, line = [], ""
            for w in words:
                if len(line) + len(w) > 12 and line:
                    lines.append(line)
                    line = w
                else:
                    line = (line + " " + w).strip()
            lines.append(line)
            for j, ln in enumerate(lines[:3]):
                parts.append(f'<text x="{cx}" y="{y(0) + 13 + j * 11}" text-anchor="middle" class="lab">{esc(ln)}</text>')
        parts.append("</svg>")
        m0 = fmt_metric(b["latest"]["margin"], "pct")
        m1 = fmt_pct_range(b["target"]["margin_low"], b["target"]["margin_high"])
        legend = (f'<p class="legend"><span class="sw" style="background:{T["target"]}"></span>gap to peer median '
                  f'<span class="sw" style="background:{T["target_light"]}"></span>further to top quartile</p>')
        return "".join(parts) + legend + f'<p class="margin-row">EBIT margin {esc(m0)} → <strong>{esc(m1)}</strong></p>'

    def cash_bars(self, width=340):
        nwc = next(b for b in self.a["buckets"] if b["id"] == "working_capital")
        sized = [lv for lv in nwc["levers"] if lv["state"] == "sized"]
        T = TOKENS
        out = []
        if sized:
            top_v = max(lv["high"] for lv in sized) * 1.05
            label_w, row_h, bar_h = 132, 18, 10
            h = row_h * len(sized) + 6
            plot_w = width - label_w - 62
            parts = [f'<svg viewBox="0 0 {width} {h}" class="chart" role="img" aria-label="Working-capital release">']
            for i, lv in enumerate(sized):
                y0 = 3 + i * row_h + (row_h - bar_h) / 2
                xl = label_w + lv["low"] / top_v * plot_w
                xh = label_w + lv["high"] / top_v * plot_w
                parts.append(self._hbar(label_w, xl, y0, bar_h, T["target"], f'{lv["label"]}: {lv["display"]}'))
                if xh > xl:
                    parts.append(f'<rect x="{xl}" y="{y0}" width="{xh - xl}" height="{bar_h}" fill="{T["target_light"]}" rx="2"/>')
                parts.append(f'<text x="{label_w - 4}" y="{y0 + bar_h - 2}" text-anchor="end" class="lab">{esc(lv["label"])}: {esc(lv["gap_display"])}</text>')
                parts.append(f'<text x="{xh + 4}" y="{y0 + bar_h - 2}" class="val">{esc(lv["display"])}</text>')
            parts.append("</svg>")
            out.append("".join(parts))
        for lv in nwc["levers"]:
            if lv["state"] != "sized":
                out.append(f'<p class="chart-na">{esc(lv["label"])}: {esc(lv.get("reason", ""))}</p>')
        return "".join(out)

    # ---- sections ------------------------------------------------------
    def header(self):
        meta = self.a["meta"]
        cm = self.case.get("meta", {})
        nar = self.case.get("narrative", {})
        t = self.a["totals"]
        tgt = self.companies[self.tid]
        chips = [
            "Public sources only",
            f"As of {cm.get('as_of', 'n/a')}",
            f"{meta['currency']} millions",
            f"Latest fiscal year {meta['target_period']}",
            f"{len([c for c in self.case['companies'] if c.get('role') == 'peer'])} peers",
        ]
        chips.append("EBIT: adjusted operating income" if cm.get("ebit_basis") == "adjusted" else "EBIT: reported operating income")
        if cm.get("fx_note"):
            chips.append(cm["fx_note"])
        unchecked = [x for x in self.sources if x.get("checked") is False]
        if unchecked:
            chips.append(f"{len(unchecked)} of {len(self.sources)} sources read from search extracts: verify before client use")
        b = self.a["bridge"]
        margin_tile = ""
        if b:
            margin_tile = (f'<div class="tile"><div class="tl">EBIT margin</div><div class="tv">{esc(fmt_metric(b["latest"]["margin"], "pct"))}'
                           f' → {esc(fmt_pct_range(b["target"]["margin_low"], b["target"]["margin_high"]))}</div>'
                           f'<div class="ts">today → with the gaps closed</div></div>')
        return f"""
<header class="hdr">
  <div class="hdr-main">
    <div class="eyebrow">Opportunity scan{(' · for ' + esc(cm['audience'])) if cm.get('audience') else ''}</div>
    <h1>{esc(tgt['name'])}</h1>
    <p class="question">{self.text(cm.get('question', ''), 'meta.question')}</p>
    <p class="headline">{self.text(nar.get('headline', ''), 'headline')}</p>
    <div class="chips">{''.join(f'<span>{esc(c)}</span>' for c in chips)}</div>
  </div>
  <div class="tiles">
    <div class="tile hero"><div class="tl">Recurring EBIT opportunity</div><div class="tv">{esc(t['pnl']['display'])}</div>
      <div class="ts">a year by {esc(meta['horizon_end'])}, from {t['pnl']['count']} sized bucket{'s' if t['pnl']['count'] != 1 else ''}</div></div>
    <div class="tile"><div class="tl">One-off cash release</div><div class="tv">{esc(t['cash']['display'])}</div>
      <div class="ts">working capital; never added to EBIT</div></div>
    {margin_tile}
  </div>
</header>"""

    def col_situation(self):
        nar = self.case.get("narrative", {})
        out = ['<section class="col"><h2><span class="n">1</span>The situation</h2>']
        if nar.get("exec_summary"):
            out.append('<h3>In short</h3><ol class="exec">')
            out += [f"<li>{self.text(x, 'exec_summary')}</li>" for x in nar["exec_summary"]]
            out.append("</ol>")
        if nar.get("situation"):
            out.append('<h3>What the company is facing</h3><ul class="bul">')
            for x in nar["situation"]:
                if isinstance(x, dict):
                    out.append(f"<li>{self.text(x.get('text', ''), 'situation')}{self.cite(x.get('src'))}</li>")
                else:
                    out.append(f"<li>{self.text(x, 'situation')}</li>")
            out.append("</ul>")
        if nar.get("segments"):
            out.append(self.segments(nar["segments"]))
        if nar.get("priorities"):
            out.append('<h3>What management says it is prioritising</h3>')
            for p in nar["priorities"]:
                out.append(f'<div class="prio"><p class="prio-t">{self.text(p.get("text", ""), "priorities")}</p>')
                for gid in p.get("signals", []):
                    out.append(self.signal(gid))
                out.append("</div>")
        others = [g for g in self.case.get("signals", []) if g.get("kind") in ("analyst", "industry") and g.get("show", True)
                  and g["id"] not in {s for p in nar.get("priorities", []) for s in p.get("signals", [])}]
        if others:
            out.append('<h3>Outside view: analysts and industry</h3>')
            out += [self.signal(g["id"]) for g in others[:4]]
        out.append("</section>")
        return "".join(out)

    def signal(self, gid):
        g = self.signals.get(gid)
        if not g:
            self.missing.append(f"signal:{gid}")
            return f'<p class="na">[missing signal {esc(gid)}]</p>'
        who = ", ".join(x for x in (g.get("speaker"), g.get("role")) if x)
        when = g.get("date", "")
        body = esc(g.get("text", ""))
        if g.get("verbatim", True):
            body = f"“{body}”"
            kind = ""
        else:
            kind = '<span class="tag">summary</span>'
        return (f'<blockquote class="sig sig-{esc(g.get("kind", "management"))}">{body}'
                f'<footer>{kind}{esc(who)}{" · " if who and when else ""}{esc(when)}{self.cite(g.get("src"))}</footer></blockquote>')

    def col_performance(self):
        cm = self.case.get("meta", {})
        out = ['<section class="col"><h2><span class="n">2</span>Performance against peers</h2>']
        out.append('<h3>Peer set</h3><table class="peers"><thead><tr><th>Company</th><th>Revenue</th><th>FY</th><th>Why it is a peer</th></tr></thead><tbody>')
        vals = self.a["values"]
        for c in self.case["companies"]:
            cid = c["id"]
            latest = None
            fin = self.case["financials"].get(cid, {})
            if fin:
                from opscan_calc import year_of, read_value
                lp = max(fin, key=year_of)
                rv, _, _ = read_value(fin[lp].get("revenue"))
                fx = c.get("fx_to_case") or 1.0
                latest = (rv * fx if rv is not None else None, lp)
            rev = fmt_money(latest[0], self.cur) if latest else "n/a"
            per = vals[cid]["ebit_margin"]["period"] or ""
            cls = ' class="is-target"' if cid == self.tid else ""
            why = "Target" if cid == self.tid else self.text(c.get("rationale", ""), f"rationale {cid}")
            basis = f'<div class="basis">{esc(c["basis_note"])}</div>' if c.get("basis_note") else ""
            out.append(f"<tr{cls}><td>{esc(c['name'])}{basis}</td><td class='num'>{esc(rev)}</td><td>{esc(per)}</td><td>{why}</td></tr>")
        out.append("</tbody></table>")
        growth_key = self.a["meta"].get("growth_metric", "revenue_cagr")
        keys = cm.get("charts") or ["ebit_margin", growth_key, "gross_margin", "sga_pct", "ccc", "rnd_pct"]

        def has(k):
            return sum(self.a["values"][c["id"]][k]["value"] is not None for c in self.case["companies"]) >= 3
        extras = [k for k in ("valuation_vs_growth", "tsr") if k not in keys and has("valuation" if k == "valuation_vs_growth" else k)]
        for k in extras:
            for drop in ("rnd_pct", "ccc"):
                if drop in keys:
                    keys[keys.index(drop)] = k
                    break
        out.append('<div class="charts">')
        for k in keys:
            if k == "valuation_vs_growth":
                out.append(self.scatter(growth_key))
                continue
            m = METRIC[k]
            st = self.a["stats"][k]
            dirn = {"higher": "higher is better", "lower": "lower is better", "context": "context only, not rated"}[m.direction]
            rating = ""
            if st.get("rating"):
                rating = f'<span class="chip chip-{st["rating"].replace(" ", "-")}">{esc(st["rating"])} · {st["rank"]} of {st["rank_of"]}</span>'
            elif st.get("invalid_reason"):
                rating = f'<span class="chip">benchmark n/a: {esc(st["invalid_reason"])}</span>'
            periods = st.get("periods") or []
            per = periods[0] if len(periods) == 1 else (f"latest FY each ({periods[0]} to {periods[-1]})" if periods else "")
            out.append(f'<figure class="fig"><figcaption><strong>{esc(m.label)}</strong> {rating}<br><span class="sub">{esc(dirn)} · {esc(per)} · sorted best to worst</span></figcaption>{self.bar_chart(k)}</figure>')
        out.append("</div>")
        out.append(self.appendix())
        out.append("</section>")
        return "".join(out)

    def col_case(self):
        nar = self.case.get("narrative", {})
        out = ['<section class="col"><h2><span class="n">3</span>Case for change</h2>']
        for i, f in enumerate(nar.get("framings", []), start=1):
            lens = f.get("lens")
            st = self.a["stats"].get(lens, {}) if lens else {}
            chip = ""
            if st.get("rating"):
                chip = f'<span class="chip chip-{st["rating"].replace(" ", "-")}">{esc(METRIC[lens].short)}: {esc(st["rating"])}</span>'
            nums = []
            for k in f.get("metrics", [lens] if lens else []):
                if k not in METRIC:
                    continue
                s2 = self.a["stats"][k]
                tv = self.a["values"][self.tid][k]["value"]
                nums.append(f'<div class="kn"><div class="kl">{esc(METRIC[k].short)}</div><div class="kv">{esc(fmt_metric(tv, METRIC[k].unit))}</div>'
                            f'<div class="ks">median {esc(fmt_metric(s2["median"], METRIC[k].unit))} · top quartile {esc(fmt_metric(s2["top_quartile"], METRIC[k].unit))}</div></div>')
            lead = ' <span class="lead">recommended lead</span>' if f.get("lead") else ""
            out.append(f'<article class="framing"><div class="fr-h"><span class="rank">{i}</span><h3>{self.text(f.get("title", ""), "framing.title")}</h3></div>'
                       f'<div class="fr-meta">{chip}{lead}</div>')
            if nums:
                out.append(f'<div class="knums">{"".join(nums)}</div>')
            out.append(f'<p>{self.text(f.get("story", ""), "framing.story")}</p>')
            for gid in f.get("signals", []):
                out.append(self.signal(gid))
            if f.get("readiness"):
                out.append(f'<p class="ready"><span class="ready-l ready-{esc(f["readiness"])}">Client readiness: {esc(f["readiness"])}</span> {self.text(f.get("readiness_reason", ""), "readiness")}</p>')
            out.append("</article>")
        out.append("</section>")
        return "".join(out)

    def col_prize(self):
        nar = self.case.get("narrative", {})
        meta = self.a["meta"]
        notes = nar.get("bucket_notes", {})
        out = ['<section class="col"><h2><span class="n">4</span>Size of prize</h2>']
        out.append(f'<h3>EBIT bridge to {esc(meta["horizon_end"])}</h3>')
        out.append(self.waterfall())
        has_prac = any(b.get("practitioner") for b in self.a["buckets"])
        out.append('<table class="prize"><thead><tr><th>Bucket and gap to peers</th><th>Baseline</th>')
        if has_prac:
            out.append("<th>Published range</th>")
        out.append('<th>Opportunity</th><th>As %</th></tr></thead><tbody>')
        for b in self.a["buckets"]:
            if b["kind"] != "pnl":
                continue
            base = f'{esc(b["baseline"]["display"])}<div class="basis">{esc(b["baseline"]["label"])}, {esc(b["baseline"]["period"])}</div>'
            if b["state"] == "sized":
                gap = f'<div class="basis">{esc(b.get("gap_display", ""))}</div>'
                if b.get("note"):
                    gap += f'<div class="basis">{esc(b["note"])}</div>'
                opp = f"<strong>{esc(b['opportunity']['display'])}</strong>"
                if b["id"] == "commercial":
                    pct = (f'{esc(b["incremental_revenue"]["pct_display"])} more revenue'
                           f'<div class="basis">+{esc(b["incremental_revenue"]["display"])} sales in {esc(b["horizon_label"])}</div>')
                else:
                    pct = (f'{esc(b["pct_of_baseline"]["display"])} of {esc(b["baseline"]["label"].lower())}'
                           f'<div class="basis">{esc(b["margin_bps"]["display"])} of margin</div>') if b.get("pct_of_baseline") else ""
            else:
                gap = f'<div class="basis">{esc(b.get("reason", ""))}</div>'
                opp = "—" if b["state"] == "no_gap" else "n/a"
                pct = ""
            prac = ""
            if has_prac:
                p = b.get("practitioner")
                prac = f"<td>{esc(p['pct_display'])}{self.cite(p['src'])}</td>" if p else "<td></td>"
            out.append(f"<tr><td><strong>{esc(b['name'])}</strong>{gap}</td><td class='num'>{base}</td>{prac}<td class='num'>{opp}</td><td>{pct}</td></tr>")
        t = self.a["totals"]
        cols = 5 if has_prac else 4
        out.append(f'<tr class="tot"><td colspan="{cols - 2}">Recurring EBIT, sum of the rows above</td><td class="num"><strong>{esc(t["pnl"]["display"])}</strong></td><td></td></tr>')
        out.append("</tbody></table>")
        out.append(f'<h3>One-off cash: working capital <span class="h-val">{esc(t["cash"]["display"])}</span></h3>')
        out.append(self.cash_bars())
        if notes:
            out.append('<h3>Why the value is real</h3><dl class="notes">')
            names = {b["id"]: b["name"] for b in self.a["buckets"]}
            for bid, note in notes.items():
                if isinstance(note, dict):
                    sigs = "".join(self.signal(g) for g in note.get("signals", []))
                    out.append(f'<dt>{esc(names.get(bid, bid))}</dt><dd>{self.text(note.get("text", ""), "bucket_notes")}{sigs}</dd>')
                else:
                    out.append(f'<dt>{esc(names.get(bid, bid))}</dt><dd>{self.text(note, "bucket_notes")}</dd>')
            out.append("</dl>")
        if nar.get("next_steps"):
            out.append('<h3>Questions to test with management</h3><ul class="bul">')
            out += [f"<li>{self.text(x, 'next_steps')}</li>" for x in nar["next_steps"]]
            out.append("</ul>")
        out.append("</section>")
        return "".join(out)

    def col_method(self):
        nar = self.case.get("narrative", {})
        meta = self.a["meta"]
        cap = meta["capture"]
        out = ['<section class="col method"><h2><span class="n">5</span>Method and sources</h2>']
        method = [
            "Every figure comes from a public filing, results release or investor presentation, listed below. Nothing is estimated to fill a gap: a missing value shows as n/a with its reason.",
            "Benchmarks are the median and top quartile of the peers that report the metric; the target is never in its own benchmark. Top quartile follows the metric's direction.",
            ("EBIT is each company's own adjusted operating income, from its non-GAAP reconciliation; definitions differ and are noted where they matter."
             if self.case.get("meta", {}).get("ebit_basis") == "adjusted" else
             "EBIT is reported operating income unless a company note says otherwise.")
            + " Gross margin is revenue less cost of sales. SG&A is benchmarked as one combined line, because peers split it differently.",
            f"Sizing closes the gap to the peer median (low) and the top quartile (high), on the latest year's revenue{'' if cap == 1 else f', at a {cap:.0%} capture rate'}. Growth ({'organic, as each company reports it' if meta.get('growth_metric') == 'organic_growth' else 'reported revenue CAGR'}) compounds for {meta['horizon_years']} years to {meta['horizon_end']} and converts to EBIT at the stated margin. Cash is one-off and never added to EBIT.",
            "Totals are the sum of the rows shown. This is a sniff test of where value may sit, not a commitment: it has no practitioner experience, case examples or management data behind it.",
        ]
        out.append('<ul class="bul small">' + "".join(f"<li>{esc(x)}</li>" for x in method) + "</ul>")
        lim = list(nar.get("limitations", []))
        excl = self.case.get("exclusions", [])
        if excl:
            lim += [f"{self.name(e['company'])} left out of the {METRIC[e['metric']].short} benchmark: {e.get('reason', '')}" for e in excl if e.get("metric") in METRIC]
        unchecked = [x for x in self.sources if x.get("checked") is False]
        if unchecked:
            lim.append(f"{len(unchecked)} of {len(self.sources)} sources could not be opened and were read from search extracts (marked ◦ below). Check those figures and quotes against the documents before client use.")
        if lim:
            out.append('<h3>Limitations</h3><ul class="bul small">' + "".join(f"<li>{self.text(x, 'limitations')}</li>" for x in lim) + "</ul>")
        two = " two" if len(self.sources) > 14 else ""
        out.append(f'<h3>Sources</h3><ol class="sources{two}">')
        for s in self.sources:
            bits = [s.get("publisher"), s.get("date"), s.get("locator")]
            meta_line = " · ".join(esc(b) for b in bits if b)
            url = s.get("url", "")
            link = f'<a href="{esc(url)}">{esc(url)}</a>' if url else ""
            mark = "◦ " if s.get("checked") is False else ""
            out.append(f'<li>{mark}<strong>{esc(s.get("title", ""))}</strong> {meta_line}<br>{link}</li>')
        out.append("</ol>")
        out.append("</section>")
        return "".join(out)

    def appendix(self):
        keys = [self.a["meta"].get("growth_metric", "revenue_cagr"), "gross_margin", "sga_pct", "ebit_margin", "dso", "dio", "dpo"]
        head = "".join(f"<th>{esc(METRIC[k].short)}</th>" for k in keys)
        rows = []
        for c in self.case["companies"]:
            v = self.a["values"][c["id"]]
            cls = ' class="is-target"' if c["id"] == self.tid else ""
            cells = "".join(f"<td class='num'>{esc(v[k]['display'])}</td>" for k in keys)
            rows.append(f"<tr{cls}><td>{esc(self.name(c['id']))}</td>{cells}</tr>")
        med = "".join(f"<td class='num'>{esc(fmt_metric(self.a['stats'][k]['median'], METRIC[k].unit))}</td>" for k in keys)
        return (f'<h3>Data table</h3><table class="appx"><thead><tr><th></th>{head}</tr></thead><tbody>{"".join(rows)}'
                f'<tr class="tot"><td>Peer median</td>{med}</tr></tbody></table>')

    def render(self):
        body = (self.header() + '<main class="grid">' + self.col_situation() + self.col_performance()
                + self.col_case() + self.col_prize() + self.col_method() + "</main>")
        cm = self.case.get("meta", {})
        footer = (f'<footer class="ftr"><span>Prepared {esc(cm.get("prepared_on", cm.get("as_of", "")))}'
                  f'{(" by " + esc(cm["prepared_by"])) if cm.get("prepared_by") else ""}</span>'
                  f'<span>Built from public information only. Figures are as reported by each company for its own fiscal year.</span></footer>')
        title = f"Opportunity scan: {self.companies[self.tid]['name']}"
        return PAGE.replace("__TITLE__", esc(title)).replace("__CSS__", CSS).replace("__BODY__", body + footer)


CSS = """
:root{--surface:%(surface)s;--page:%(page)s;--ink:%(ink)s;--ink2:%(ink2)s;--muted:%(muted)s;--grid:%(grid)s;
--axis:%(axis)s;--target:%(target)s;--target-light:%(target_light)s;--target-dark:%(target_dark)s;--tq:%(tq)s;--good:%(good)s;--bad:%(bad)s}
@page{size:841mm 594mm;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#e9e8e3;color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.stage{transform-origin:0 0}
.sheet{width:841mm;height:594mm;background:var(--surface);padding:14mm 16mm 10mm;display:flex;flex-direction:column;gap:7mm;overflow:hidden;position:relative}
.hdr{display:flex;gap:12mm;align-items:stretch;border-bottom:0.6mm solid var(--ink);padding-bottom:6mm}
.hdr-main{flex:1;min-width:0}
.eyebrow{font-size:13pt;letter-spacing:.08em;text-transform:uppercase;color:var(--ink2);font-weight:600}
h1{font-size:54pt;line-height:1;margin:2mm 0 3mm;font-weight:700;letter-spacing:-.01em}
.question{font-size:15pt;color:var(--ink2);margin:0 0 2mm}
.headline{font-size:21pt;line-height:1.25;margin:0 0 4mm;font-weight:600;max-width:420mm}
.chips{display:flex;flex-wrap:wrap;gap:2mm}
.chips span{font-size:10.5pt;border:0.3mm solid var(--axis);border-radius:10mm;padding:1mm 3.5mm;color:var(--ink2)}
.tiles{display:flex;gap:5mm;align-items:stretch}
.tile{min-width:62mm;max-width:92mm;border:0.3mm solid var(--grid);border-radius:3mm;padding:4mm 5mm;background:var(--page);display:flex;flex-direction:column;justify-content:center}
.tile.hero{width:78mm;border-color:var(--target);border-width:.6mm}
.tl{font-size:11pt;color:var(--ink2);font-weight:600}
.tv{font-size:24pt;font-weight:700;margin:1.5mm 0;white-space:nowrap}
.tile.hero .tv{font-size:32pt;color:var(--target-dark)}
.ts{font-size:9.5pt;color:var(--muted)}
.grid{flex:1;display:grid;grid-template-columns:1.2fr 1.9fr 1.3fr 1.6fr 1fr;gap:8mm;min-height:0}
.col{min-width:0;overflow:hidden;font-size:11pt;line-height:1.38}
.col.over{outline:1mm dashed var(--bad)}
h2{font-size:19pt;margin:0 0 3mm;display:flex;align-items:center;gap:3mm;border-bottom:.3mm solid var(--grid);padding-bottom:2mm}
h2 .n{display:inline-flex;width:9mm;height:9mm;border-radius:50%%;background:var(--ink);color:var(--surface);font-size:13pt;align-items:center;justify-content:center}
h3{font-size:12.5pt;margin:4mm 0 1.5mm;color:var(--ink)}
.h-val{color:var(--target-dark);font-weight:700;margin-left:2mm}
p{margin:0 0 2mm}
.exec{padding-left:5mm;margin:0}
.exec li{margin-bottom:1.6mm;font-weight:500}
.bul{padding-left:4.5mm;margin:0}
.bul li{margin-bottom:1.2mm}
.small{font-size:9.5pt;line-height:1.32}
.prio{margin-bottom:2.5mm}
.prio-t{font-weight:600;margin-bottom:1mm}
blockquote.sig{margin:0 0 1.8mm;padding:1.6mm 3mm;border-left:.8mm solid var(--target);background:var(--page);font-size:10pt;line-height:1.32}
blockquote.sig-analyst,blockquote.sig-industry{border-left-color:var(--axis)}
blockquote.sig footer{font-size:8.5pt;color:var(--muted);margin-top:.8mm}
.tag{display:inline-block;font-size:7.5pt;text-transform:uppercase;letter-spacing:.06em;border:.25mm solid var(--axis);border-radius:1mm;padding:0 1mm;margin-right:1.5mm}
.cite{color:var(--target-dark);font-size:7.5pt;margin-left:.5mm}
table{border-collapse:collapse;width:100%%;font-size:9.5pt}
th{text-align:left;font-weight:600;color:var(--ink2);border-bottom:.3mm solid var(--axis);padding:1mm 1.5mm}
td{border-bottom:.2mm solid var(--grid);padding:1mm 1.5mm;vertical-align:top}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr.is-target td{background:#eef4fc;font-weight:600}
tr.tot td{border-top:.4mm solid var(--ink);border-bottom:none;font-weight:600}
.basis{font-size:8pt;color:var(--muted);font-weight:400}
.peers td:last-child{font-size:8.5pt;color:var(--ink2)}
.segs{margin-bottom:2mm}.segs td:last-child{font-size:8.5pt;color:var(--ink2)}
.charts{display:grid;grid-template-columns:1fr 1fr;gap:4mm 6mm;margin-top:3mm}
.fig{margin:0}
figcaption{font-size:10.5pt;margin-bottom:1mm;line-height:1.3}
figcaption .sub{font-size:8.5pt;color:var(--muted)}
.chart{width:100%%;height:auto;display:block;overflow:visible}
.chart .lab{font-size:8.6px;fill:var(--ink2)}
.chart .val{font-size:8.2px;fill:var(--ink2);font-variant-numeric:tabular-nums;paint-order:stroke;stroke:var(--surface);stroke-width:2.6px;stroke-linejoin:round}
.chart .val.strong{font-weight:700;fill:var(--ink)}
.chart .ref{font-size:7.6px;fill:var(--ink2);font-weight:600;paint-order:stroke;stroke:var(--surface);stroke-width:2.6px;stroke-linejoin:round}
.chart .ref.tq{fill:#b3471c}
.chart-na{font-size:8pt;color:var(--muted);margin:.5mm 0 0}
.chip{display:inline-block;font-size:8.5pt;font-weight:600;border-radius:1.2mm;padding:.3mm 1.6mm;background:var(--page);border:.25mm solid var(--axis);color:var(--ink2);vertical-align:middle}
.chip-top-quartile{background:#e6f2e6;border-color:#9bc89b;color:var(--good)}
.chip-above-median{background:#eef6ee;border-color:#c4dfc4;color:var(--good)}
.chip-below-median{background:#fbefe9;border-color:#efc2ad;color:#9a3d17}
.chip-bottom-quartile{background:#fbe7e7;border-color:#eaa9a9;color:var(--bad)}
.framing{border:.3mm solid var(--grid);border-radius:2.5mm;padding:3mm 3.5mm;margin-bottom:3.5mm}
.fr-h{display:flex;gap:2.5mm;align-items:flex-start}
.fr-h h3{margin:0;font-size:12.5pt;line-height:1.25}
.rank{flex:none;width:6.5mm;height:6.5mm;border-radius:50%%;border:.4mm solid var(--ink);display:inline-flex;align-items:center;justify-content:center;font-size:9pt;font-weight:700}
.fr-meta{margin:1.5mm 0 2mm 9mm}
.lead{font-size:8.5pt;font-weight:700;color:var(--target-dark);margin-left:2mm;text-transform:uppercase;letter-spacing:.05em}
.knums{display:flex;gap:2mm;margin-bottom:2mm}
.kn{flex:1;background:var(--page);border-radius:1.5mm;padding:1.5mm 2mm}
.kl{font-size:8pt;color:var(--muted);font-weight:600}
.kv{font-size:14pt;font-weight:700}
.ks{font-size:7.5pt;color:var(--muted)}
.ready{font-size:9.5pt;color:var(--ink2);margin:1.5mm 0 0}
.ready-l{font-weight:700;color:var(--ink)}
.legend{font-size:8.5pt;color:var(--muted);margin:1mm 0}
.sw{display:inline-block;width:3.5mm;height:3.5mm;border-radius:.6mm;vertical-align:-0.6mm;margin:0 1mm 0 2.5mm}
.margin-row{font-size:11pt;margin:0 0 2mm}
.prize{margin-top:2mm}
.notes dt{font-weight:700;margin-top:1.5mm;font-size:10pt}
.notes dd{margin:0 0 1mm;font-size:10pt}
.na{color:var(--muted);font-size:9pt}
.method{font-size:9.5pt}
.sources{padding-left:5mm;margin:0;font-size:7.6pt;line-height:1.3;word-break:break-word}
.sources li{margin-bottom:.9mm;break-inside:avoid}
.sources.two{columns:2;column-gap:4mm;font-size:7pt}
.sources a{color:var(--ink2);text-decoration:none}
.appx{font-size:7.6pt}
.appx td,.appx th{padding:.6mm 1mm}
.ftr{display:flex;justify-content:space-between;font-size:8.5pt;color:var(--muted);border-top:.3mm solid var(--grid);padding-top:2mm}
@media screen{body{padding:0}.sheet{box-shadow:0 2px 18px rgba(0,0,0,.12)}}
@media print{html,body{background:none}.stage{transform:none!important}.col.over{outline:none}}
""" % TOKENS

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title><style>__CSS__</style></head>
<body><div class="stage" id="stage"><div class="sheet" id="sheet">__BODY__</div></div>
<script>
(function(){
  var stage=document.getElementById('stage'),sheet=document.getElementById('sheet');
  function fit(){var w=window.innerWidth,s=w/sheet.offsetWidth;stage.style.transform='scale('+s+')';
    document.body.style.height=(sheet.offsetHeight*s)+'px';}
  var grid=document.querySelector('.grid'),cols=document.querySelectorAll('.col');
  function overfull(){for(var i=0;i<cols.length;i++){if(cols[i].scrollHeight>cols[i].clientHeight+2||cols[i].scrollWidth>cols[i].clientWidth+2)return true;}return false;}
  // Scale the body of the poster to fill the sheet: the largest zoom at which every column still fits.
  function autofit(){
    grid.style.zoom='';grid.style.width='';grid.style.height='';
    var W=grid.clientWidth,H=grid.clientHeight,best=0.8;
    for(var z=1.5;z>=0.8;z-=0.025){grid.style.zoom=z;grid.style.width=(W/z)+'px';grid.style.height=(H/z)+'px';
      if(!overfull()){best=z;break;}}
    grid.style.zoom=best;grid.style.width=(W/best)+'px';grid.style.height=(H/best)+'px';
    document.documentElement.setAttribute('data-zoom',best.toFixed(3));}
  // Flag any column whose content still runs past the sheet, so an overfull poster is visible on screen.
  function check(){var over=[];
    cols.forEach(function(c){if(c.scrollHeight>c.clientHeight+2||c.scrollWidth>c.clientWidth+2){c.classList.add('over');over.push(c.querySelector('h2').textContent);}});
    document.documentElement.setAttribute('data-overflow',over.join('|'));}
  window.addEventListener('resize',fit);window.addEventListener('load',function(){autofit();fit();check();});
  window.addEventListener('beforeprint',function(){stage.style.transform='none';});
  window.addEventListener('afterprint',fit);
})();
</script></body></html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("case")
    ap.add_argument("-o", "--out", default="poster.html")
    args = ap.parse_args()
    case = json.load(open(args.case, encoding="utf-8"))
    try:
        analysis = compute(case)
    except CaseError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    r = Renderer(case, analysis)
    page = r.render()
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(page)
    out_dir = os.path.dirname(os.path.abspath(args.out))
    with open(os.path.join(out_dir, "analysis.json"), "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, default=str)
    for w in analysis["warnings"]:
        print(f"warning: {w}")
    for where, n in r.typed_numbers:
        print(f"warning: number typed into narrative ({where}): {n!r}; cite it with a {{{{token}}}} or quote the source")
    if r.missing:
        for k in sorted(set(r.missing)):
            print(f"error: unresolved token or signal: {k}", file=sys.stderr)
        return 2
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
