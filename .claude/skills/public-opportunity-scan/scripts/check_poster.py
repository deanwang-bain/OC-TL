#!/usr/bin/env python3
"""Check that a poster fits its A1 sheet, and take a screenshot to look at.

    python check_poster.py poster.html [--png poster.png] [--chrome /path/to/chrome]

Uses a headless Chromium. Reports any column whose content runs past the sheet
(the page marks those itself on load), and writes a PNG of the whole poster.
Without a browser it says so and exits 3: then check the layout by eye.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys

CANDIDATES = [
    os.environ.get("CHROME"),
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    shutil.which("chromium"), shutil.which("chromium-browser"), shutil.which("google-chrome"),
    shutil.which("chrome"), "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_chrome(explicit=None):
    for c in [explicit] + CANDIDATES:
        if c and os.path.exists(c):
            return c
    for root in ("/opt/pw-browsers", os.path.expanduser("~/.cache/ms-playwright")):
        if os.path.isdir(root):
            for dirpath, _, files in os.walk(root):
                if "chrome" in files and dirpath.endswith("chrome-linux"):
                    return os.path.join(dirpath, "chrome")
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("poster")
    ap.add_argument("--png")
    ap.add_argument("--chrome")
    a = ap.parse_args()
    chrome = find_chrome(a.chrome)
    if not chrome:
        print("no headless Chromium found; open the poster and check every column ends inside the sheet")
        return 3
    url = "file://" + os.path.abspath(a.poster)
    base = [chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=4000"]
    # A1 landscape is 841 x 594 mm, about 3179 x 2245 CSS px at 96 dpi
    dom = subprocess.run(base + ["--window-size=3179,2245", "--dump-dom", url], capture_output=True, text=True, timeout=120)
    m = re.search(r'data-overflow="([^"]*)"', dom.stdout)
    over = [x for x in (m.group(1).split("|") if m else []) if x]
    png = a.png or os.path.splitext(a.poster)[0] + ".png"
    # a taller window than the sheet: headless screenshots lose the bottom of the viewport otherwise
    subprocess.run(base + ["--window-size=3179,2400", f"--screenshot={os.path.abspath(png)}", url],
                   capture_output=True, text=True, timeout=120)
    print(f"screenshot: {png}")
    # the real test of "one sheet": print to PDF and count pages
    pdf = os.path.splitext(png)[0] + ".pdf"
    subprocess.run(base + ["--no-pdf-header-footer", f"--print-to-pdf={os.path.abspath(pdf)}", url],
                   capture_output=True, text=True, timeout=120)
    pages = None
    if os.path.exists(pdf):
        pages = len(re.findall(rb"/Type\s*/Page[^s]", open(pdf, "rb").read()))
        print(f"pdf: {pdf} ({pages} page{'s' if pages != 1 else ''})")
    if m is None:
        print("could not read the overflow check from the page; look at the screenshot")
        return 3
    if pages and pages > 1:
        print("overflow: the print runs to more than one A1 page; shorten the content, then rebuild")
        return 1
    if over:
        print("overflow: these columns run past the sheet: " + "; ".join(over))
        print("shorten their text, drop a chart, or cut quotes, then rebuild")
        return 1
    z = re.search(r'data-zoom="([^"]*)"', dom.stdout)
    print("fits: every column ends inside the A1 sheet" + (f" (body scaled to {z.group(1)})" if z else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
