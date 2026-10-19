"""Deterministic calculations for a public opportunity scan.

Reads a case file (see references/case-schema.md) and returns the analysis:
per-company metrics, peer statistics, ratings, bucket sizing, totals, the EBIT
bridge and a flat table of facts that narrative text cites with {{key}} tokens.

The model never does this arithmetic itself. Every number on the poster comes
from here, from figures the case file attributes to a public source.
"""

from __future__ import annotations

import json
import math
import re
import statistics
from dataclasses import dataclass

# --------------------------------------------------------------------------
# Metric catalogue
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Metric:
    key: str
    label: str
    short: str
    direction: str  # "higher", "lower" or "context" (no better or worse)
    unit: str       # "pct" or "days"


METRICS = [
    Metric("revenue_cagr", "Revenue growth (CAGR)", "Growth", "higher", "pct"),
    Metric("gross_margin", "Gross margin", "Gross margin", "higher", "pct"),
    Metric("sga_pct", "SG&A as % of revenue", "SG&A %", "lower", "pct"),
    Metric("rnd_pct", "R&D as % of revenue", "R&D %", "context", "pct"),
    Metric("ebit_margin", "EBIT margin", "EBIT margin", "higher", "pct"),
    Metric("dso", "Days sales outstanding", "DSO", "lower", "days"),
    Metric("dio", "Days inventory outstanding", "DIO", "lower", "days"),
    Metric("dpo", "Days payables outstanding", "DPO", "higher", "days"),
    Metric("ccc", "Cash conversion cycle", "CCC", "lower", "days"),
    Metric("tsr", "Total shareholder return", "TSR", "higher", "pct"),
    Metric("organic_growth", "Organic growth", "Organic growth", "higher", "pct"),
    Metric("valuation", "Valuation multiple", "Multiple", "higher", "x"),
]
# Metrics taken as published, per company, rather than computed from line items
DIRECT = ["tsr", "organic_growth", "valuation"]
METRIC = {m.key: m for m in METRICS}

LINE_ITEMS = ["revenue", "cogs", "gross_profit", "sga", "rnd", "ebit", "receivables", "inventory", "payables"]
# Ratios a company publishes itself, used only when the amounts behind them are not available
REPORTED_RATIOS = ["ebit_margin", "gross_margin"]


class CaseError(ValueError):
    """The case file cannot be computed as written."""


# --------------------------------------------------------------------------
# Reading values
# --------------------------------------------------------------------------

def read_value(raw):
    """Return (value or None, source id or None, reason or None)."""
    if raw is None:
        return None, None, "not reported"
    if isinstance(raw, (int, float)):
        return float(raw), None, None
    if isinstance(raw, dict):
        v = raw.get("value")
        src = raw.get("src")
        reason = raw.get("na_reason")
        if v is None:
            return None, src, reason or "not reported"
        return float(v), src, None
    raise CaseError(f"unreadable value: {raw!r}")


def year_of(period: str) -> int:
    m = re.search(r"(\d{4})", period)
    if not m:
        m2 = re.search(r"(\d{2})$", period)
        if not m2:
            raise CaseError(f"period key {period!r} has no year")
        return 2000 + int(m2.group(1))
    return int(m.group(1))


def short_period(period: str) -> str:
    return f"FY{str(year_of(period))[2:]}"


# --------------------------------------------------------------------------
# Formatting
# --------------------------------------------------------------------------

CURRENCY_SYMBOL = {"USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "CNY": "¥", "CHF": "CHF ", "INR": "₹", "KRW": "₩"}


def fmt_money(v, currency, unit="millions"):
    if v is None:
        return "n/a"
    sym = CURRENCY_SYMBOL.get(currency, currency + " ")
    sign = "−" if v < 0 else ""
    a = abs(v)
    if unit == "millions":
        if a >= 1000:
            return f"{sign}{sym}{a / 1000:,.1f}B"
        if a >= 100:
            return f"{sign}{sym}{a:,.0f}M"
        return f"{sign}{sym}{a:,.1f}M"
    return f"{sign}{sym}{a:,.0f}"


def fmt_range(lo, hi, currency):
    if lo is None:
        return "n/a"
    if hi is not None and abs(lo) < 1e-9 < hi:
        return f"up to {fmt_money(hi, currency)}"
    if hi is None or abs(hi - lo) < 1e-9:
        return fmt_money(lo, currency)
    a, b = fmt_money(lo, currency), fmt_money(hi, currency)
    sym = CURRENCY_SYMBOL.get(currency, currency + " ")
    # "$1.2B–$1.8B" reads better as "$1.2–1.8B" when the suffix matches
    if a[-1] == b[-1] and a.startswith(sym) and b.startswith(sym):
        return f"{a[:-1]}–{b[len(sym):]}"
    return f"{a}–{b}"


def fmt_metric(v, unit):
    if v is None:
        return "n/a"
    if unit == "pct":
        return f"{v * 100:.1f}%"
    if unit == "x":
        return f"{v:.1f}x"
    return f"{v:.0f} days"


def fmt_pp(v):
    if v is None:
        return "n/a"
    return f"{v * 100:+.1f} pp"


def fmt_pct_range(lo, hi):
    if lo is None:
        return "n/a"
    if hi is None or abs(hi - lo) < 1e-9:
        return f"{lo * 100:.1f}%"
    return f"{lo * 100:.1f}–{hi * 100:.1f}%"


# --------------------------------------------------------------------------
# Statistics
# --------------------------------------------------------------------------

def percentile(values, p):
    """Linear interpolation between closest ranks (Excel PERCENTILE.INC)."""
    xs = sorted(values)
    if not xs:
        return None
    if len(xs) == 1:
        return xs[0]
    k = (len(xs) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return xs[int(k)]
    return xs[f] + (xs[c] - xs[f]) * (k - f)


def better(a, b, direction):
    """True when a is at least as good as b."""
    return a >= b if direction == "higher" else a <= b


# --------------------------------------------------------------------------
# The computation
# --------------------------------------------------------------------------

def compute(case: dict) -> dict:
    meta = case.get("meta", {})
    currency = meta.get("currency", "USD")
    unit = meta.get("unit", "millions")
    cagr_years = int(meta.get("cagr_years", 3))
    min_peers = int(meta.get("min_peers", 4))
    warnings: list[str] = []

    companies = case.get("companies", [])
    if not companies:
        raise CaseError("no companies")
    targets = [c for c in companies if c.get("role") == "target"]
    if len(targets) != 1:
        raise CaseError("exactly one company must have role 'target'")
    target = targets[0]
    tid = target["id"]
    peers = [c for c in companies if c.get("role") == "peer"]
    if len(peers) < min_peers:
        warnings.append(f"only {len(peers)} peers; benchmarks need {min_peers} with data")

    source_ids = {s["id"] for s in case.get("sources", [])}
    fin = case.get("financials", {})

    # exclusions: {(company, metric): reason}
    exclusions = {(e["company"], e["metric"]): e.get("reason", "excluded") for e in case.get("exclusions", [])}

    # ---- per-company line items, latest period, converted to case currency
    rows = {}
    for c in companies:
        cid = c["id"]
        periods = fin.get(cid, {})
        if not periods:
            warnings.append(f"{cid}: no financials")
            rows[cid] = {"periods": {}, "latest": None}
            continue
        fx = c.get("fx_to_case")
        if c.get("currency", currency) != currency and fx is None:
            raise CaseError(f"{cid} reports in {c.get('currency')} but has no fx_to_case")
        fx = float(fx) if fx is not None else 1.0
        fx *= float(c.get("scale", 1.0))  # e.g. 0.001 when a company reports in thousands
        parsed = {}
        for p, items in periods.items():
            parsed[p] = {}
            for li in LINE_ITEMS:
                v, src, reason = read_value(items.get(li))
                if src and src not in source_ids:
                    warnings.append(f"{cid} {p} {li}: source {src!r} is not in sources[]")
                if v is not None and src is None:
                    warnings.append(f"{cid} {p} {li}: value has no source")
                parsed[p][li] = {"value": v * fx if v is not None else None, "src": src, "na_reason": reason}
            # cost of sales from gross profit, when that is what the filing shows
            if parsed[p]["cogs"]["value"] is None and parsed[p]["gross_profit"]["value"] is not None \
                    and parsed[p]["revenue"]["value"] is not None:
                parsed[p]["cogs"] = {"value": parsed[p]["revenue"]["value"] - parsed[p]["gross_profit"]["value"],
                                     "src": parsed[p]["gross_profit"]["src"], "na_reason": None,
                                     "derived": "revenue less gross profit"}
            parsed[p]["_ratios"] = {}
            for rk in REPORTED_RATIOS:
                v, src, _ = read_value((items.get("reported_ratios") or {}).get(rk))
                if v is not None:
                    if src and src not in source_ids:
                        warnings.append(f"{cid} {p} reported {rk}: source {src!r} is not in sources[]")
                    parsed[p]["_ratios"][rk] = {"value": v, "src": src}
        latest = max(parsed, key=year_of)
        rows[cid] = {"periods": parsed, "latest": latest}

    def li(cid, period, item):
        r = rows[cid]["periods"].get(period, {}).get(item)
        return (r or {}).get("value")

    # ---- metrics per company
    metric_values = {}  # cid -> metric -> {value, period, na_reason, display}
    for c in companies:
        cid = c["id"]
        out = {}
        latest = rows[cid]["latest"]
        if latest is None:
            for m in METRICS:
                out[m.key] = {"value": None, "period": None, "na_reason": "no financials"}
            metric_values[cid] = out
            continue
        rev = li(cid, latest, "revenue")
        cogs = li(cid, latest, "cogs")

        def ratio(num_item, denom, label):
            n = li(cid, latest, num_item)
            if n is None:
                reason = rows[cid]["periods"][latest].get(num_item, {}).get("na_reason") or "not reported"
                return None, f"{label}: {reason}"
            if not denom:
                return None, "denominator not reported"
            return n / denom, None

        def days(item, denom, label):
            v, reason = ratio(item, denom, label)
            return (v * 365 if v is not None else None), reason

        vals = {}
        if rev:
            ebit = li(cid, latest, "ebit")
            vals["ebit_margin"] = (ebit / rev, None) if ebit is not None else (None, "EBIT not reported")
            vals["gross_margin"] = ((rev - cogs) / rev, None) if cogs is not None else (None, "cost of sales not reported (costs by nature, or not split)")
            vals["sga_pct"] = ratio("sga", rev, "SG&A")
            vals["rnd_pct"] = ratio("rnd", rev, "R&D")
            vals["dso"] = days("receivables", rev, "receivables")
        else:
            for k in ("ebit_margin", "gross_margin", "sga_pct", "rnd_pct", "dso"):
                vals[k] = (None, "revenue not reported")
        if cogs:
            vals["dio"] = days("inventory", cogs, "inventory")
            vals["dpo"] = days("payables", cogs, "payables")
        else:
            vals["dio"] = (None, "cost of sales not reported")
            vals["dpo"] = (None, "cost of sales not reported")
        reported = rows[cid]["periods"][latest].get("_ratios", {})
        ratio_notes = {}
        for rk, rv in reported.items():
            if vals.get(rk, (None,))[0] is None:
                vals[rk] = (rv["value"], None)
                ratio_notes[rk] = "margin as published by the company; amounts not available"
        if all(vals.get(k, (None,))[0] is not None for k in ("dso", "dio", "dpo")):
            vals["ccc"] = (vals["dso"][0] + vals["dio"][0] - vals["dpo"][0], None)
        else:
            vals["ccc"] = (None, "needs DSO, DIO and DPO")

        # CAGR over up to cagr_years, using only years with revenue
        years = sorted((year_of(p), p) for p in rows[cid]["periods"] if li(cid, p, "revenue"))
        cagr_label = None
        if len(years) >= 2:
            end_y, end_p = years[-1]
            cands = [(y, p) for y, p in years if end_y - y <= cagr_years]
            start_y, start_p = cands[0]
            n = end_y - start_y
            if n >= 1:
                r0, r1 = li(cid, start_p, "revenue"), li(cid, end_p, "revenue")
                vals["revenue_cagr"] = ((r1 / r0) ** (1 / n) - 1, None)
                cagr_label = f"{short_period(start_p)}–{short_period(end_p)}"
                if n < cagr_years:
                    warnings.append(f"{cid}: growth over {n} year(s), not {cagr_years}")
            else:
                vals["revenue_cagr"] = (None, "fewer than two years of revenue")
        else:
            vals["revenue_cagr"] = (None, "fewer than two years of revenue")

        direct_period = {}
        for dk in DIRECT:
            raw = c.get(dk)
            dv, dsrc, dreason = read_value(raw)
            if dv is not None and dsrc is None:
                warnings.append(f"{cid} {dk}: value has no source")
            if dsrc and dsrc not in source_ids:
                warnings.append(f"{cid} {dk}: source {dsrc!r} is not in sources[]")
            vals[dk] = (dv, None if dv is not None else (dreason if raw is not None else "not provided"))
            direct_period[dk] = (raw or {}).get("period") if isinstance(raw, dict) else None
        if c.get("tsr_window"):
            direct_period["tsr"] = c["tsr_window"]

        for m in METRICS:
            v, reason = vals.get(m.key, (None, "not computed"))
            period = cagr_label if m.key == "revenue_cagr" else (
                direct_period.get(m.key) if m.key in DIRECT else short_period(latest))
            ex = exclusions.get((cid, m.key))
            entry = {"value": v, "period": period, "na_reason": reason, "display": fmt_metric(v, m.unit)}
            if m.key in ratio_notes:
                entry["note"] = ratio_notes[m.key]
            if ex:
                entry["excluded"] = ex
            out[m.key] = entry
        metric_values[cid] = out

    # ---- peer statistics and target rating
    stats = {}
    for m in METRICS:
        peer_vals = [
            (p["id"], metric_values[p["id"]][m.key]["value"])
            for p in peers
            if metric_values[p["id"]][m.key]["value"] is not None and (p["id"], m.key) not in exclusions
        ]
        tv = metric_values[tid][m.key]["value"]
        st = {"n": len(peer_vals), "median": None, "top_quartile": None, "bottom_quartile": None,
              "rating": None, "rank": None, "rank_of": None, "gap_to_median": None, "gap_to_tq": None,
              "invalid_reason": None, "p25": None, "p75": None}
        if len(peer_vals) < min_peers:
            st["invalid_reason"] = f"only {len(peer_vals)} peers report it (need {min_peers})"
        else:
            vs = [v for _, v in peer_vals]
            st["median"] = statistics.median(vs)
            hi_q, lo_q = percentile(vs, 0.75), percentile(vs, 0.25)
            st["p25"], st["p75"] = lo_q, hi_q
            if m.direction == "lower":
                st["top_quartile"], st["bottom_quartile"] = lo_q, hi_q
            else:
                st["top_quartile"], st["bottom_quartile"] = hi_q, lo_q
            if tv is not None and m.direction != "context":
                if better(tv, st["top_quartile"], m.direction):
                    st["rating"] = "top quartile"
                elif better(tv, st["median"], m.direction):
                    st["rating"] = "above median"
                elif better(tv, st["bottom_quartile"], m.direction):
                    st["rating"] = "below median"
                else:
                    st["rating"] = "bottom quartile"
                pool = sorted(vs + [tv], reverse=(m.direction == "higher"))
                st["rank"] = pool.index(tv) + 1
                st["rank_of"] = len(pool)
                sign = 1 if m.direction == "higher" else -1
                st["gap_to_median"] = max(0.0, sign * (st["median"] - tv))
                st["gap_to_tq"] = max(0.0, sign * (st["top_quartile"] - tv))
        periods = sorted({metric_values[c["id"]][m.key]["period"] for c in companies
                          if metric_values[c["id"]][m.key]["value"] is not None and metric_values[c["id"]][m.key]["period"]})
        st["periods"] = periods
        stats[m.key] = st

    # ---- sizing
    sz = case.get("sizing", {})
    horizon = int(sz.get("horizon_years", 3))
    capture = float(sz.get("capture", 1.0))
    size_rnd = bool(sz.get("size_rnd", False))
    practitioner = sz.get("practitioner_ranges", {})

    latest_t = rows[tid]["latest"]
    R = li(tid, latest_t, "revenue")
    C = li(tid, latest_t, "cogs")
    SGA = li(tid, latest_t, "sga")
    RND = li(tid, latest_t, "rnd")
    EBIT = li(tid, latest_t, "ebit")
    if R is None:
        raise CaseError("target has no latest revenue")
    if EBIT is not None and EBIT <= 0:
        warnings.append("target EBIT is zero or negative on this basis; consider meta.ebit_basis 'adjusted' for every company")
    end_label = f"FY{str(year_of(latest_t) + horizon)[2:]}"

    def prac_leg(bucket_id, baseline):
        p = practitioner.get(bucket_id)
        if not p:
            return None
        if p.get("src") and p["src"] not in source_ids:
            warnings.append(f"practitioner range for {bucket_id}: source {p['src']!r} is not in sources[]")
        if not p.get("src"):
            warnings.append(f"practitioner range for {bucket_id} has no source; ignored")
            return None
        base = R if p.get("basis") == "revenue" else baseline
        return {"low": p["low_pct"] * base, "high": p["high_pct"] * base, "src": p["src"],
                "pct_display": fmt_pct_range(p["low_pct"], p["high_pct"]),
                "basis": p.get("basis", "cost")}

    buckets = []

    def finish(b, peer_lo, peer_hi, baseline_cost, prac=None):
        b["peer"] = None if peer_lo is None else {"low": peer_lo * capture, "high": peer_hi * capture}
        b["practitioner"] = prac
        if b["state"] == "sized":
            lo = b["peer"]["low"] if b["peer"] else 0.0
            hi = b["peer"]["high"] if b["peer"] else 0.0
            if prac:
                lo, hi = max(lo, prac["low"]), max(hi, prac["high"])
            b["opportunity"] = {"low": lo, "high": hi, "display": fmt_range(lo, hi, currency)}
            if baseline_cost:
                b["pct_of_baseline"] = {"low": lo / baseline_cost, "high": hi / baseline_cost,
                                        "display": fmt_pct_range(lo / baseline_cost, hi / baseline_cost)}
            b["margin_bps"] = {"low": lo / R * 1e4, "high": hi / R * 1e4,
                               "display": f"{lo / R * 1e4:.0f}–{hi / R * 1e4:.0f} bps" if hi - lo > 0.5 * R / 1e4 else f"{lo / R * 1e4:.0f} bps"}
        else:
            b["opportunity"] = None
        buckets.append(b)

    def cost_bucket(bid, name, metric_key, baseline, base_label, kind="pnl"):
        st = stats[metric_key]
        tv = metric_values[tid][metric_key]["value"]
        b = {"id": bid, "name": name, "kind": kind, "metric": metric_key,
             "baseline": {"value": baseline, "display": fmt_money(baseline, currency), "label": base_label,
                          "period": short_period(latest_t)},
             "target_value": tv, "median": st["median"], "top_quartile": st["top_quartile"]}
        prac = prac_leg(bid, baseline)
        if tv is None or baseline is None:
            b["state"] = "na"
            b["reason"] = metric_values[tid][metric_key]["na_reason"] or f"{base_label} not reported"
            return finish(b, None, None, baseline, prac)
        if st["invalid_reason"]:
            b["state"] = "na" if not prac else "sized"
            b["reason"] = f"no peer benchmark: {st['invalid_reason']}"
            return finish(b, None, None, baseline, prac)
        g_med, g_tq = st["gap_to_median"], st["gap_to_tq"]
        if METRIC[metric_key].direction == "context":
            # sized only on request (R&D): lower treated as better, against the lower quartile
            g_med, g_tq = max(0.0, tv - st["median"]), max(0.0, tv - st["p25"])
            st = {**st, "rating": "above peer median" if g_med > 0 else "at or below peer median"}
        b["gap_display"] = (f"{fmt_pp(g_med)} to median · {fmt_pp(g_tq)} to top quartile" if g_med > 0
                            else f"above median · {fmt_pp(g_tq)} to top quartile")
        if g_tq <= 0 and not prac:
            b["state"] = "no_gap"
            b["reason"] = f"already {st['rating']} on {METRIC[metric_key].short}"
            return finish(b, None, None, baseline, prac)
        b["state"] = "sized"
        if g_med <= 0:
            b["note"] = "above the peer median; the range is the gap to the top quartile only"
        return finish(b, g_med * R, g_tq * R, baseline, prac)

    # A. Commercial: grow at the benchmark rate instead of the target's own
    growth_key = sz.get("growth_metric", "revenue_cagr")
    if growth_key not in ("revenue_cagr", "organic_growth"):
        raise CaseError("sizing.growth_metric must be 'revenue_cagr' or 'organic_growth'")
    st = stats[growth_key]
    t_cagr = metric_values[tid][growth_key]["value"]
    margin = sz.get("commercial_margin")
    if margin is None or margin == "ebit_margin":
        margin = metric_values[tid]["ebit_margin"]["value"]
        margin_label = "target EBIT margin"
    else:
        margin = float(margin)
        margin_label = "margin set in the case file"
    a = {"id": "commercial", "name": "Commercial: revenue growth", "kind": "pnl", "metric": growth_key,
         "baseline": {"value": R, "display": fmt_money(R, currency), "label": "Revenue", "period": short_period(latest_t)},
         "target_value": t_cagr, "median": st["median"], "top_quartile": st["top_quartile"], "horizon_label": end_label}
    if t_cagr is None or margin is None:
        a["state"] = "na"
        a["reason"] = "growth or margin not available"
        finish(a, None, None, None)
    elif margin <= 0:
        a["state"] = "na"
        a["reason"] = "target EBIT margin is zero or negative; use an adjusted EBIT basis or set sizing.commercial_margin"
        warnings.append(a["reason"])
        finish(a, None, None, None)
    elif st["invalid_reason"]:
        a["state"] = "na"
        a["reason"] = f"no peer benchmark: {st['invalid_reason']}"
        finish(a, None, None, None)
    elif st["gap_to_tq"] <= 0:
        a["state"] = "no_gap"
        a["reason"] = f"already {st['rating']} on growth"
        finish(a, None, None, None)
    else:
        base_rev = R * (1 + t_cagr) ** horizon

        def incr(gap):
            return R * (1 + t_cagr + gap) ** horizon - base_rev

        r_lo, r_hi = incr(st["gap_to_median"]), incr(st["gap_to_tq"])
        a["state"] = "sized"
        a["incremental_revenue"] = {"low": r_lo * capture, "high": r_hi * capture,
                                    "display": fmt_range(r_lo * capture, r_hi * capture, currency),
                                    "pct_display": fmt_pct_range(r_lo / base_rev, r_hi / base_rev)}
        a["margin_applied"] = {"value": margin, "label": margin_label}
        a["gap_display"] = (f"{fmt_pp(st['gap_to_median'])} a year to median · {fmt_pp(st['gap_to_tq'])} to top quartile"
                            if st["gap_to_median"] > 0 else f"above median · {fmt_pp(st['gap_to_tq'])} a year to top quartile")
        basis = "organic growth rate" if growth_key == "organic_growth" else "revenue CAGR"
        a["method"] = (f"Revenue grown at the benchmark {basis} instead of the target's own, for {horizon} years "
                       f"to {end_label}, times the {margin_label}.")
        finish(a, r_lo * margin, r_hi * margin, None)

    cost_bucket("operations", "Operations: cost of sales", "gross_margin", C, "Cost of sales")
    cost_bucket("sga", "SG&A efficiency", "sga_pct", SGA, "SG&A")
    if size_rnd:
        cost_bucket("rnd", "R&D efficiency", "rnd_pct", RND, "R&D")

    # D. Working capital: one-off cash release
    nwc_levers = []
    for key, item, denom, denom_label in (("dso", "receivables", R, "revenue"), ("dio", "inventory", C, "cost of sales"),
                                          ("dpo", "payables", C, "cost of sales")):
        stx = stats[key]
        tv = metric_values[tid][key]["value"]
        bal = li(tid, latest_t, item)
        lever = {"metric": key, "label": METRIC[key].short, "balance": bal, "balance_display": fmt_money(bal, currency),
                 "target_days": tv, "median": stx["median"], "top_quartile": stx["top_quartile"]}
        if tv is None or bal is None or not denom:
            lever.update(state="na", reason=metric_values[tid][key]["na_reason"] or f"{item} not reported")
        elif stx["invalid_reason"]:
            lever.update(state="na", reason=f"no peer benchmark: {stx['invalid_reason']}")
        elif stx["gap_to_tq"] <= 0:
            lever.update(state="no_gap", reason=f"already {stx['rating']}")
        else:
            per_day = denom / 365
            lo, hi = stx["gap_to_median"] * per_day * capture, stx["gap_to_tq"] * per_day * capture
            word = "longer" if key == "dpo" else "shorter"
            gd = (f"{stx['gap_to_median']:.0f}–{stx['gap_to_tq']:.0f} days {word}" if stx["gap_to_median"] > 0
                  else f"up to {stx['gap_to_tq']:.0f} days {word}")
            lever.update(state="sized", low=lo, high=hi, display=fmt_range(lo, hi, currency),
                         gap_display=gd,
                         method=f"gap in days × {denom_label} ÷ 365")
        nwc_levers.append(lever)
    sized_levers = [lv for lv in nwc_levers if lv["state"] == "sized"]
    nwc = {"id": "working_capital", "name": "Working capital", "kind": "cash", "levers": nwc_levers,
           "baseline": {"value": None, "display": "", "label": "Receivables, inventory, payables", "period": short_period(latest_t)}}
    if sized_levers:
        lo = sum(lv["low"] for lv in sized_levers)
        hi = sum(lv["high"] for lv in sized_levers)
        nwc.update(state="sized", opportunity={"low": lo, "high": hi, "display": fmt_range(lo, hi, currency)},
                   peer={"low": lo, "high": hi}, practitioner=None)
    else:
        nwc.update(state="no_gap" if any(lv["state"] == "no_gap" for lv in nwc_levers) else "na",
                   opportunity=None, peer=None, practitioner=None,
                   reason="no working-capital gap to peers" if any(lv["state"] == "no_gap" for lv in nwc_levers) else "working-capital data not available")
    buckets.append(nwc)

    # ---- totals: the sum of the rows shown, P&L and cash never added together
    pnl = [b for b in buckets if b["kind"] == "pnl" and b["state"] == "sized"]
    pnl_lo = sum(b["opportunity"]["low"] for b in pnl)
    pnl_hi = sum(b["opportunity"]["high"] for b in pnl)
    cash = nwc["opportunity"]
    totals = {
        "pnl": {"low": pnl_lo, "high": pnl_hi, "display": fmt_range(pnl_lo, pnl_hi, currency) if pnl else "n/a",
                "count": len(pnl)},
        "cash": {"low": cash["low"] if cash else 0.0, "high": cash["high"] if cash else 0.0,
                 "display": cash["display"] if cash else "n/a"},
    }

    # ---- EBIT bridge
    incr_rev = next((b["incremental_revenue"] for b in pnl if b["id"] == "commercial"), {"low": 0.0, "high": 0.0})
    bridge = None
    if EBIT is not None:
        steps = [{"id": b["id"], "name": b["name"], "low": b["opportunity"]["low"], "high": b["opportunity"]["high"]} for b in pnl]
        t_lo, t_hi = EBIT + pnl_lo, EBIT + pnl_hi
        bridge = {
            "latest": {"ebit": EBIT, "margin": EBIT / R, "period": short_period(latest_t),
                       "display": fmt_money(EBIT, currency)},
            "steps": steps,
            "target": {"low": t_lo, "high": t_hi, "display": fmt_range(t_lo, t_hi, currency),
                       "margin_low": t_lo / (R + incr_rev["low"]), "margin_high": t_hi / (R + incr_rev["high"])},
        }
    else:
        warnings.append("target EBIT not reported: no bridge")

    # ---- facts for {{tokens}}
    facts = {}

    def put(key, value, display):
        facts[key] = {"value": value, "display": display}

    t_name = target.get("short_name") or target["name"]
    put("target.name", None, t_name)
    put("target.period", None, short_period(latest_t))
    put("case.currency", None, currency)
    put("peers.count", len(peers), str(len(peers)))
    put("target.revenue", R, fmt_money(R, currency))
    if EBIT is not None:
        put("target.ebit", EBIT, fmt_money(EBIT, currency))
    for m in METRICS:
        tvm = metric_values[tid][m.key]
        put(f"target.{m.key}", tvm["value"], tvm["display"])
        stm = stats[m.key]
        put(f"median.{m.key}", stm["median"], fmt_metric(stm["median"], m.unit))
        put(f"tq.{m.key}", stm["top_quartile"], fmt_metric(stm["top_quartile"], m.unit))
        if stm["rating"]:
            put(f"rating.{m.key}", None, stm["rating"])
            put(f"rank.{m.key}", stm["rank"], f"{stm['rank']} of {stm['rank_of']}")
        if stm["gap_to_median"] is not None:
            g = stm["gap_to_median"]
            put(f"gap.{m.key}", g, fmt_pp(g).lstrip("+") if m.unit == "pct" else (f"{g:.1f}x" if m.unit == "x" else f"{g:.0f} days"))
        for c in companies:
            v = metric_values[c["id"]][m.key]
            put(f"{c['id']}.{m.key}", v["value"], v["display"])
    for b in buckets:
        if b.get("opportunity"):
            put(f"bucket.{b['id']}", b["opportunity"]["low"], b["opportunity"]["display"])
        if b.get("pct_of_baseline"):
            put(f"bucket.{b['id']}.pct", b["pct_of_baseline"]["low"], b["pct_of_baseline"]["display"])
        if b.get("margin_bps"):
            put(f"bucket.{b['id']}.bps", b["margin_bps"]["low"], b["margin_bps"]["display"])
    put("total.pnl", pnl_lo, totals["pnl"]["display"])
    put("total.cash", totals["cash"]["low"], totals["cash"]["display"])
    if bridge:
        put("bridge.target_margin", bridge["target"]["margin_low"],
            fmt_pct_range(bridge["target"]["margin_low"], bridge["target"]["margin_high"]))
        put("bridge.latest_margin", bridge["latest"]["margin"], fmt_metric(bridge["latest"]["margin"], "pct"))
    put("horizon.end", None, end_label)

    return {
        "meta": {**meta, "currency": currency, "unit": unit, "horizon_years": horizon, "capture": capture,
                 "growth_metric": growth_key,
                 "horizon_end": end_label, "target_id": tid, "target_period": short_period(latest_t)},
        "metrics": [m.__dict__ for m in METRICS],
        "values": metric_values,
        "stats": stats,
        "buckets": buckets,
        "totals": totals,
        "bridge": bridge,
        "facts": facts,
        "warnings": warnings,
    }


TOKEN = re.compile(r"\{\{\s*([A-Za-z0-9_.\-]+)\s*\}\}")


def resolve_tokens(text: str, facts: dict, missing: list) -> str:
    def sub(m):
        key = m.group(1)
        f = facts.get(key)
        if f is None:
            missing.append(key)
            return f"[missing: {key}]"
        return f["display"]
    return TOKEN.sub(sub, text)


BARE_NUMBER = re.compile(r"(?<![\w{])(?:[$€£¥]\s?\d[\d,.]*\s?(?:[BMK]|bn|m|million|billion)?|\d[\d,.]*\s?(?:%|pp|bps|x\b|days|bn|million|billion))")
QUOTED = re.compile(r"“[^”]*”|\"[^\"]*\"")


def lint_numbers(text: str) -> list[str]:
    """Numbers typed into narrative instead of cited with a token."""
    stripped = QUOTED.sub("", TOKEN.sub("", text))
    return BARE_NUMBER.findall(stripped)


if __name__ == "__main__":
    import sys
    case = json.load(open(sys.argv[1]))
    print(json.dumps(compute(case), indent=2, default=str))
