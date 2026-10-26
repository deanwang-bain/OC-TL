#!/usr/bin/env python3
"""Build the post-GLS team structure diagrams as editable .drawio.svg files.

Each output file is an ordinary SVG that renders as an image anywhere (Confluence
attachment, browser, GitHub) and also carries the draw.io model in its `content`
attribute, so the draw.io Confluence app or diagrams.net opens it for editing.

    python3 tools/drawio_charts.py [OUTPUT_DIR]

OUTPUT_DIR defaults to context/post-gls-team-structure/diagrams. The charts are
defined in code below; edit them here, or edit the files in draw.io directly once
the page is published -- the files then become the source of truth.
"""

from __future__ import annotations

import datetime as dt
import html
import os
import sys
from dataclasses import dataclass, field

FONT = "Helvetica, Arial, sans-serif"
FONT_SIZE = 12
LINE_HEIGHT = 16
CHAR_WIDTH = 6.6  # average glyph width at FONT_SIZE, for sizing boxes

# Fill, stroke and text colour per party. Kept light so the charts print well and
# stay legible as images on Confluence's light and dark themes.
PALETTE = {
    "bain": ("#dbe8f5", "#2f6a9e", "#13293d"),
    "new": ("#ffffff", "#2f6a9e", "#13293d"),
    "sn": ("#fbe3cf", "#b8641c", "#3d2208"),
    "bcn": ("#dcefdc", "#3d8a3d", "#163316"),
    "ngss": ("#e6e0f5", "#6a4fb0", "#251a40"),
    "tsg": ("#ececec", "#6b6b6b", "#262626"),
    "neutral": ("#ffffff", "#9aa3ad", "#262626"),
}
GROUP_FILL = {
    "bain": "#f2f7fc",
    "sn": "#fdf4ec",
    "bcn": "#f1f8f1",
    "ngss": "#f5f2fb",
    "tsg": "#f7f7f7",
    "neutral": "#fafafa",
}


@dataclass
class Node:
    id: str
    label: str
    x: float
    y: float
    w: float = 0
    h: float = 0
    party: str = "bain"
    bold: bool = False  # heavier border, for the new hire

    def __post_init__(self) -> None:
        lines = self.label.split("\n")
        if not self.w:
            self.w = max(110, max(len(s) for s in lines) * CHAR_WIDTH + 24)
        if not self.h:
            self.h = len(lines) * LINE_HEIGHT + 16


@dataclass
class Group:
    id: str
    title: str
    x: float
    y: float
    w: float
    h: float
    party: str


@dataclass
class Edge:
    source: str
    target: str
    dashed: bool = False
    bend: float = 0.5  # where the horizontal run sits between source and target, 0 to 1


@dataclass
class Bar:
    """A timeline bar or milestone, drawn on the date axis."""
    row: int
    start: dt.date
    end: dt.date | None
    label: str
    party: str


@dataclass
class Chart:
    name: str
    title: str
    width: float
    height: float
    groups: list[Group] = field(default_factory=list)
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    legend: list[tuple[str, str]] = field(default_factory=list)
    texts: list[tuple[float, float, str, str]] = field(default_factory=list)  # x, y, text, anchor
    lines: list[tuple[float, float, float, float, bool]] = field(default_factory=list)  # x1,y1,x2,y2,dashed


# ---------------------------------------------------------------------------
# Layout helpers


def column(group: Group, items: list[tuple[str, str]], party: str, top: float = 34, gap: float = 12,
           width: float | None = None) -> list[Node]:
    """Stack boxes down the middle of a group, sizing the group to fit."""
    nodes, y = [], group.y + top
    w = width or group.w - 32
    for nid, label in items:
        n = Node(nid, label, 0, y, w=w, party=party)
        n.x = group.x + (group.w - n.w) / 2
        nodes.append(n)
        y += n.h + gap
    group.h = max(group.h, y - group.y + 4)
    return nodes


def legend_for(*parties: str) -> list[tuple[str, str]]:
    names = {
        "bain": "Bain (existing)",
        "new": "New Bain hire",
        "sn": "StatusNeo",
        "bcn": "BCN",
        "ngss": "NGSS",
        "tsg": "Bain shared service",
    }
    return [(p, names[p]) for p in parties]


def leadership_row(y: float, extra: list[Node] | None = None) -> tuple[Group, list[Node]]:
    g = Group("lead", "Bain product leadership", 40, y, 0, 0, "bain")
    nodes = [
        Node("pm", "Product Manager\nKasia Mrowca", 0, 0),
        Node("tl", "Tech Lead\nDean Wang", 0, 0),
        Node("arch", "Architect\nSandeep Uppal", 0, 0),
    ] + (extra or [])
    x = g.x + 16
    for n in nodes:
        n.x, n.y = x, y + 34
        x += n.w + 16
    g.w = x - g.x
    g.h = max(n.h for n in nodes) + 34 + 16
    return g, nodes


# ---------------------------------------------------------------------------
# Chart definitions


def chart_today() -> Chart:
    c = Chart("01-today", "Today: Sprint 5, Support and Hardening", 1060, 0)
    lead, ln = leadership_row(60, [Node("ux", "Designer\nJoanna Soh", 0, 0),
                                   Node("tlb", "Tech Lead back-up\nMichelle Flood", 0, 0)])
    lead.x = (c.width - lead.w) / 2
    shift = lead.x - 40
    for n in ln:
        n.x += shift
    top = lead.y + lead.h + 60
    bain = Group("g_bain", "Bain", 40, top, 300, 0, "bain")
    bn = column(bain, [("data", "Data pipeline\nSandeep, Siva"),
                       ("bcn0", "BCN\ngolden data set, OI domain")], "bain")
    tsg = Group("g_tsg", "Bain shared services", 40, 0, 300, 0, "tsg")
    tsg.y = bain.y + bain.h + 24
    tn = column(tsg, [("tsg0", "TSG / Andromeda\ninfra templates, MCP")], "tsg")
    sn = Group("g_sn", "StatusNeo delivery squad", 380, top, 640, 0, "sn")
    left = [("snfe", "Frontend and BFF"), ("snbe", "Backend services"), ("sncalc", "Calc engine and grammar")]
    right = [("snag", "Agents: peer, narrative, chat"), ("snops", "Infra-as-code, CI/CD"), ("snqa", "QA")]
    half_l = Group("tmp", "", sn.x, top, sn.w / 2, 0, "sn")
    half_r = Group("tmp", "", sn.x + sn.w / 2, top, sn.w / 2, 0, "sn")
    sl = column(half_l, left, "sn", width=270)
    sr = column(half_r, right, "sn", width=270)
    sn.h = max(half_l.h, half_r.h)
    c.groups = [lead, bain, tsg, sn]
    c.nodes = ln + bn + tn + sl + sr
    c.edges = [Edge("tl", "g_sn", bend=0.65), Edge("arch", "g_bain", bend=0.3)]
    c.legend = legend_for("bain", "sn", "tsg")
    c.height = max(tsg.y + tsg.h, sn.y + sn.h) + 70
    return c


def target_chart(name: str, title: str, pods: list[tuple[Group, list[tuple[str, str]]]],
                 services: list[tuple[str, str, str]], dotted: list[tuple[str, str]],
                 legend: list[str]) -> Chart:
    c = Chart(name, title, 1060, 0)
    lead, ln = leadership_row(60, [Node("stew", "Content steward\nbusiness, 0.2", 0, 0)])
    lead.x = (c.width - lead.w) / 2
    shift = lead.x - 40
    for n in ln:
        n.x += shift
    le = Node("le", "Lead Engineer / Platform Owner\nnew Bain FTE, 1.0", 0, lead.y + lead.h + 40,
              party="new", bold=True)
    le.x = (c.width - le.w) / 2
    top = le.y + le.h + 50
    nodes = ln + [le]
    groups = [lead]
    edges = [Edge("tl", "le")]
    for g, items in pods:
        g.y = top
        nodes += column(g, items, g.party)
        groups.append(g)
        edges.append(Edge("le", g.id))
    sg = Group("g_svc", "Bain shared services", 0, top, 230, 0, "tsg")
    sg.x = c.width - sg.w - 40
    nodes += column(sg, [(i, l) for i, l, _ in services], "tsg")
    groups.append(sg)
    edges.append(Edge("le", "g_svc", dashed=True))
    edges += [Edge(s, t, dashed=True) for s, t in dotted]
    c.groups, c.nodes, c.edges = groups, nodes, edges
    c.legend = legend_for(*legend)
    c.height = max(g.y + g.h for g in groups) + 70
    return c


SERVICES = [("tsg", "TSG / Andromeda\ninfra, CI/CD 0.3", ""), ("desk", "Bain service desk\nL1 support 0.2", "")]


def chart_a() -> Chart:
    pod = Group("g_bcn", "BCN pod: build and run", 40, 0, 560, 0, "bcn")
    items = [("a1", "App engineers: frontend, backend\nL3 fixes 0.8 + feature build"),
             ("a2", "Calc engine and agents engineer(s)\nmodel and prompt changes 0.4"),
             ("a3", "Data engineer\ndata maintenance 0.6"),
             ("a4", "Analysts\ngolden data, output review 0.3\ncontent changes 0.5 to 0.1"),
             ("a5", "L2 run and release")]
    return target_chart("02-option-a-bcn", "Option A: BCN owns build and run", [(pod, items)], SERVICES, [],
                        ["bain", "new", "bcn", "tsg"])


def chart_b() -> Chart:
    pod = Group("g_ngss", "NGSS pod: build and run", 40, 0, 460, 0, "ngss")
    items = [("b1", "App engineers: frontend, backend\nL3 fixes 0.8 + feature build"),
             ("b2", "Calc engine and agents engineer(s)\nmodel and prompt changes 0.4"),
             ("b3", "Data engineer\ndata maintenance 0.6"),
             ("b4", "QA and eval harness"),
             ("b5", "L2 run, release, on-call")]
    bcn = Group("g_bcnf", "BCN, fractional", 520, 0, 230, 0, "bcn")
    bitems = [("bf", "Analysts\ngolden data, output\nreview 0.3")]
    return target_chart("03-option-b-ngss", "Option B: NGSS owns build and run",
                        [(pod, items), (bcn, bitems)], SERVICES, [], ["bain", "new", "ngss", "bcn", "tsg"])


def chart_c() -> Chart:
    ngss = Group("g_ngss", "NGSS: engineering and run", 40, 0, 360, 0, "ngss")
    nitems = [("c1", "App engineers: frontend, backend\nL3 fixes 0.8 + feature build"),
              ("c2", "Calc engine and agents\nengineer(s), model and\nprompt changes 0.4"),
              ("c3", "L2 run, release, on-call")]
    bcn = Group("g_bcn", "BCN: data and content", 430, 0, 330, 0, "bcn")
    bitems = [("c4", "Data engineer\ndata maintenance 0.6"),
              ("c5", "Analysts\ngolden data, output review 0.3"),
              ("c6", "Content changes\n0.5 to 0.1")]
    return target_chart("04-option-c-split", "Option C (recommended): NGSS engineers, BCN owns data and content",
                        [(ngss, nitems), (bcn, bitems)], SERVICES, [("stew", "g_bcn")],
                        ["bain", "new", "ngss", "bcn", "tsg"])


def chart_transition() -> Chart:
    c = Chart("05-transition-mid-january", "Transition in mid-January: Scenario 2 on Option C", 1060, 0)
    tl = Node("tl", "Tech Lead\nDean Wang", 0, 60)
    tl.x = (c.width - tl.w) / 2
    le = Node("le", "Lead Engineer / Platform Owner\nnew Bain FTE", 0, tl.y + tl.h + 40, party="new", bold=True)
    le.x = (c.width - le.w) / 2
    top = le.y + le.h + 50
    g1 = Group("g1", "Bain-led, StatusNeo shadows", 40, top, 320, 0, "bain")
    n1 = column(g1, [("t1", "Frontend and BFF: NGSS"), ("t2", "QA, golden data: BCN"),
                     ("t3", "Content changes: BCN")], "bain")
    g2 = Group("g2", "StatusNeo-led, Bain shadows", 380, top, 320, 0, "sn")
    n2 = column(g2, [("t4", "Backend services"), ("t5", "Calc engine and grammar"), ("t6", "Agents")], "sn")
    g3 = Group("g3", "Handing over to TSG", 720, top, 300, 0, "tsg")
    n3 = column(g3, [("t7", "Terraform, CI/CD")], "tsg")
    c.groups = [g1, g2, g3]
    c.nodes = [tl, le] + n1 + n2 + n3
    c.edges = [Edge("tl", "le"), Edge("le", "g1"), Edge("le", "g2"), Edge("le", "g3")]
    c.legend = legend_for("bain", "new", "sn", "tsg")
    c.height = max(g.y + g.h for g in c.groups) + 70
    return c


def chart_timeline() -> Chart:
    start, end = dt.date(2026, 10, 19), dt.date(2027, 7, 5)
    x0, x1, label_w = 230, 1180, 190
    scale = (x1 - x0) / (end - start).days

    def x(d: dt.date) -> float:
        return x0 + (d - start).days * scale

    D = dt.date
    rows = [
        ("Milestones", [Bar(0, D(2026, 10, 26), None, "GLS 26 Oct", "bain"),
                        Bar(0, D(2026, 11, 30), D(2026, 12, 11), "50+ partner rollout", "bain")]),
        ("Industrialisation SOW", [Bar(1, D(2026, 11, 23), D(2027, 2, 15), "~23 Nov to ~15 Feb", "neutral")]),
        ("S1 Hard stop", [Bar(2, D(2027, 1, 4), D(2027, 1, 8), "W1", "sn"),
                          Bar(2, D(2027, 1, 25), D(2027, 1, 29), "W2", "sn"),
                          Bar(2, D(2027, 2, 8), D(2027, 2, 15), "W3", "sn")]),
        ("S2 Reverse shadow (rec.)", [Bar(3, D(2027, 1, 4), D(2027, 1, 15), "W1", "sn"),
                                      Bar(3, D(2027, 1, 18), D(2027, 2, 5), "W2", "sn"),
                                      Bar(3, D(2027, 2, 5), D(2027, 2, 15), "W3", "sn"),
                                      Bar(3, D(2027, 2, 15), D(2027, 3, 15), "Advisory tail", "tsg")]),
        ("S3 Capability-gated", [Bar(4, D(2027, 1, 4), D(2027, 2, 15), "Frontend, backend", "sn"),
                                 Bar(4, D(2027, 2, 15), D(2027, 4, 1), "Infra, run", "sn"),
                                 Bar(4, D(2027, 4, 1), D(2027, 6, 30), "Calc engine, agents", "sn")]),
        ("S4 Platform first", [Bar(5, D(2026, 12, 1), D(2026, 12, 18), "Infra to TSG", "tsg"),
                               Bar(5, D(2027, 1, 11), D(2027, 1, 29), "W2", "sn"),
                               Bar(5, D(2027, 2, 1), D(2027, 2, 15), "W3", "sn"),
                               Bar(5, D(2027, 2, 15), D(2027, 3, 15), "Tail", "tsg")]),
    ]
    c = Chart("06-roll-off-timeline", "StatusNeo roll-off by scenario (indicative)", x1 + 40, 0)
    row_h, top = 46, 100
    # Month gridlines and labels.
    m = D(2026, 11, 1)
    while m < end:
        c.lines.append((x(m), top - 14, x(m), top + row_h * len(rows), True))
        c.texts.append((x(m) + 4, top - 20, m.strftime("%b %Y" if m.month == 1 else "%b"), "start"))
        m = D(m.year + (m.month == 12), m.month % 12 + 1, 1)
    for i, (name, bars) in enumerate(rows):
        y = top + i * row_h
        c.texts.append((40, y + 27, name, "start"))
        c.lines.append((40, y + row_h, x1, y + row_h, False))
        for j, b in enumerate(bars):
            if b.end is None:
                n = Node(f"r{i}b{j}", b.label, x(b.start) - 4, y + 8, w=8, h=30, party="bain")
                c.nodes.append(n)
                continue
            w = max((b.end - b.start).days * scale, 26)
            n = Node(f"r{i}b{j}", b.label, x(b.start), y + 8, w=w, h=30, party=b.party)
            c.nodes.append(n)
    c.legend = legend_for("bain", "sn", "tsg")
    c.height = top + row_h * len(rows) + 70
    c.texts.append((40, c.height - 20, "W = wave. Late December counts as about two lost weeks. Dates are indicative.",
                    "start"))
    return c


CHARTS = [chart_today, chart_a, chart_b, chart_c, chart_transition, chart_timeline]


# ---------------------------------------------------------------------------
# Rendering


def lookup(chart: Chart) -> dict[str, tuple[float, float, float, float]]:
    boxes = {g.id: (g.x, g.y, g.w, g.h) for g in chart.groups}
    boxes.update({n.id: (n.x, n.y, n.w, n.h) for n in chart.nodes})
    return boxes


def fits(n: Node) -> bool:
    """Whether a single-line label fits inside its box; if not it is drawn to the right."""
    return "\n" in n.label or len(n.label) * CHAR_WIDTH + 12 <= n.w


def edge_path(chart: Chart, e: Edge) -> str:
    boxes = lookup(chart)
    sx, sy, sw, sh = boxes[e.source]
    tx, ty, tw, th = boxes[e.target]
    x1, y1 = sx + sw / 2, sy + sh
    x2, y2 = tx + tw / 2, ty
    if ty < sy + sh:  # target sits beside the source: leave from the side
        y1 = sy + sh / 2
        x1 = sx + sw if tx > sx else sx
        return f"M{x1:.1f},{y1:.1f} H{x2:.1f} V{y2:.1f}"
    mid = y1 + (y2 - y1) * e.bend
    return f"M{x1:.1f},{y1:.1f} V{mid:.1f} H{x2:.1f} V{y2:.1f}"


def text_block(cx: float, cy: float, label: str, colour: str, weight: str = "normal") -> str:
    lines = label.split("\n")
    first = cy - (len(lines) - 1) * LINE_HEIGHT / 2 + 4
    spans = "".join(
        f'<tspan x="{cx:.1f}" y="{first + i * LINE_HEIGHT:.1f}">{html.escape(s)}</tspan>'
        for i, s in enumerate(lines))
    return (f'<text text-anchor="middle" font-family="{FONT}" font-size="{FONT_SIZE}" '
            f'font-weight="{weight}" fill="{colour}">{spans}</text>')


def render_svg(chart: Chart) -> str:
    out = [f'<rect x="0" y="0" width="{chart.width}" height="{chart.height}" fill="#ffffff"/>',
           f'<text x="40" y="36" font-family="{FONT}" font-size="18" font-weight="bold" fill="#13293d">'
           f'{html.escape(chart.title)}</text>']
    for x1, y1, x2, y2, dashed in chart.lines:
        dash = ' stroke-dasharray="3 4"' if dashed else ""
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#d5dae0"{dash}/>')
    for g in chart.groups:
        _, stroke, ink = PALETTE[g.party]
        out.append(f'<rect x="{g.x:.1f}" y="{g.y:.1f}" width="{g.w:.1f}" height="{g.h:.1f}" rx="8" '
                   f'fill="{GROUP_FILL[g.party]}" stroke="{stroke}" stroke-dasharray="6 4"/>')
        out.append(f'<text x="{g.x + 14:.1f}" y="{g.y + 22:.1f}" font-family="{FONT}" font-size="12" '
                   f'font-weight="bold" fill="{ink}">{html.escape(g.title)}</text>')
    for e in chart.edges:
        dash = ' stroke-dasharray="4 4"' if e.dashed else ""
        out.append(f'<path d="{edge_path(chart, e)}" fill="none" stroke="#4a5562" stroke-width="1.4"'
                   f'{dash} marker-end="url(#arrow)"/>')
    for n in chart.nodes:
        fill, stroke, ink = PALETTE[n.party]
        sw = 2.4 if n.bold else 1.2
        out.append(f'<rect x="{n.x:.1f}" y="{n.y:.1f}" width="{n.w:.1f}" height="{n.h:.1f}" rx="5" '
                   f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        if not fits(n):  # milestone marker or a short bar: put the label after it
            out.append(f'<text x="{n.x + n.w + 6:.1f}" y="{n.y + n.h / 2 + 4:.1f}" font-family="{FONT}" '
                       f'font-size="{FONT_SIZE}" fill="{ink}">{html.escape(n.label)}</text>')
        else:
            out.append(text_block(n.x + n.w / 2, n.y + n.h / 2, n.label, ink,
                                  "bold" if n.bold else "normal"))
    for x, y, t, anchor in chart.texts:
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{FONT}" '
                   f'font-size="12" fill="#3b4652">{html.escape(t)}</text>')
    lx = 40
    ly = chart.height - 40 if not chart.name.endswith("timeline") else chart.height - 48
    for party, name in chart.legend:
        fill, stroke, _ = PALETTE[party]
        sw = 2.4 if party == "new" else 1.2
        out.append(f'<rect x="{lx}" y="{ly}" width="16" height="12" rx="2" fill="{fill}" stroke="{stroke}" '
                   f'stroke-width="{sw}"/>')
        out.append(f'<text x="{lx + 22}" y="{ly + 10}" font-family="{FONT}" font-size="11" fill="#3b4652">'
                   f'{html.escape(name)}</text>')
        lx += 22 + len(name) * 6.2 + 22
    if chart.edges:
        out.append(f'<line x1="{lx}" y1="{ly + 6}" x2="{lx + 28}" y2="{ly + 6}" stroke="#4a5562" '
                   f'stroke-width="1.4"/><text x="{lx + 34}" y="{ly + 10}" font-family="{FONT}" font-size="11" '
                   f'fill="#3b4652">reports to</text>')
        lx += 110
        out.append(f'<line x1="{lx}" y1="{ly + 6}" x2="{lx + 28}" y2="{ly + 6}" stroke="#4a5562" '
                   f'stroke-width="1.4" stroke-dasharray="4 4"/><text x="{lx + 34}" y="{ly + 10}" '
                   f'font-family="{FONT}" font-size="11" fill="#3b4652">draws on / coordinates with</text>')
    return "".join(out)


def drawio_xml(chart: Chart) -> str:
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']

    def vertex(cid: str, value: str, style: str, x: float, y: float, w: float, h: float) -> None:
        cells.append(f'<mxCell id="{cid}" value="{html.escape(value)}" style="{style}" vertex="1" parent="1">'
                     f'<mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/></mxCell>')

    vertex("title", chart.title, "text;html=1;fontSize=18;fontStyle=1;align=left;verticalAlign=middle;"
           "fontColor=#13293d;", 40, 18, 900, 28)
    for i, (x1, y1, x2, y2, dashed) in enumerate(chart.lines):
        style = f"endArrow=none;html=1;strokeColor=#d5dae0;{'dashed=1;' if dashed else ''}"
        cells.append(f'<mxCell id="line{i}" style="{style}" edge="1" parent="1"><mxGeometry relative="1" '
                     f'as="geometry"><mxPoint x="{x1:.1f}" y="{y1:.1f}" as="sourcePoint"/>'
                     f'<mxPoint x="{x2:.1f}" y="{y2:.1f}" as="targetPoint"/></mxGeometry></mxCell>')
    for g in chart.groups:
        _, stroke, ink = PALETTE[g.party]
        vertex(g.id, g.title, f"rounded=1;arcSize=4;whiteSpace=wrap;html=1;dashed=1;fillColor={GROUP_FILL[g.party]};"
               f"strokeColor={stroke};fontColor={ink};fontStyle=1;align=left;verticalAlign=top;spacingLeft=10;"
               f"spacingTop=4;container=0;", g.x, g.y, g.w, g.h)
    for n in chart.nodes:
        fill, stroke, ink = PALETTE[n.party]
        label = n.label.replace("\n", "<br>")
        bold = "strokeWidth=2.5;fontStyle=1;" if n.bold else ""
        if not fits(n):
            bold += "labelPosition=right;verticalLabelPosition=middle;align=left;spacingLeft=4;"
        cells.append(f'<mxCell id="{n.id}" value="{html.escape(label)}" style="rounded=1;whiteSpace=wrap;html=1;'
                     f'fillColor={fill};strokeColor={stroke};fontColor={ink};fontSize={FONT_SIZE};{bold}" '
                     f'vertex="1" parent="1"><mxGeometry x="{n.x:.1f}" y="{n.y:.1f}" width="{n.w:.1f}" '
                     f'height="{n.h:.1f}" as="geometry"/></mxCell>')
    for i, e in enumerate(chart.edges):
        style = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;strokeColor=#4a5562;"
                 f"{'dashed=1;' if e.dashed else ''}")
        cells.append(f'<mxCell id="e{i}" style="{style}" edge="1" parent="1" source="{e.source}" '
                     f'target="{e.target}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    for i, (x, y, t, _) in enumerate(chart.texts):
        vertex(f"t{i}", t, "text;html=1;align=left;verticalAlign=middle;fontColor=#3b4652;", x, y - 14,
               max(80, len(t) * CHAR_WIDTH), 20)
    lx = 40
    ly = chart.height - 40 if not chart.name.endswith("timeline") else chart.height - 48
    for party, name in chart.legend:
        fill, stroke, _ = PALETTE[party]
        vertex(f"lg_{party}", "", f"rounded=1;fillColor={fill};strokeColor={stroke};"
               f"{'strokeWidth=2.5;' if party == 'new' else ''}", lx, ly, 16, 12)
        vertex(f"lgt_{party}", name, "text;html=1;align=left;verticalAlign=middle;fontSize=11;fontColor=#3b4652;",
               lx + 20, ly - 4, len(name) * 6.2 + 10, 20)
        lx += 22 + len(name) * 6.2 + 22
    model = (f'<mxGraphModel dx="{chart.width:.0f}" dy="{chart.height:.0f}" grid="1" gridSize="10" guides="1" '
             f'tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" math="0" shadow="0">'
             f'<root>{"".join(cells)}</root></mxGraphModel>')
    return (f'<mxfile host="OC-TL tools/drawio_charts.py"><diagram id="{chart.name}" name="{html.escape(chart.title)}">'
            f'{model}</diagram></mxfile>')


def write(chart: Chart, out_dir: str) -> str:
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{chart.width:.0f}" '
           f'height="{chart.height:.0f}" viewBox="0 0 {chart.width:.0f} {chart.height:.0f}" '
           f'content="{html.escape(drawio_xml(chart), quote=True)}">'
           '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
           'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#4a5562"/></marker></defs>'
           f'{render_svg(chart)}</svg>\n')
    path = os.path.join(out_dir, f"{chart.name}.drawio.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    return path


def main() -> int:
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join("context", "post-gls-team-structure", "diagrams")
    os.makedirs(out_dir, exist_ok=True)
    for build in CHARTS:
        print(write(build(), out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
