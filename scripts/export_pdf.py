#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_pdf.py — Render a report HTML into a single long-image PNG and a
long-page PDF (mobile-friendly, share via chat).

Requires: Google Chrome (headless) + Python Pillow (PIL).
Usage:
    python3 export_pdf.py <report.html> [out_basename]

Produces  <base>-long.png  and  <base>.pdf  next to the HTML.

How it works: Chrome headless renders the full page into an oversized window,
then we detect the real document height by scanning bottom-up for the last row
that differs from the page background colour, crop there, and save PNG + PDF.
"""
import os
import sys
import subprocess

try:
    from PIL import Image
except ImportError:
    sys.exit("需要 Pillow：pip install Pillow")

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome", "chromium", "chromium-browser",
]
PAGE_BG = (244, 246, 249)   # must match --bg in build_report.py CSS
TOL = 8


def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.sep in c:
            if os.path.exists(c):
                return c
        else:
            from shutil import which
            if which(c):
                return c
    sys.exit("找不到 Chrome / Chromium，请先安装。")


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 export_pdf.py <report.html> [out_basename]")
    html = os.path.abspath(sys.argv[1])
    base = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(html)[0]
    raw = "/tmp/_report_full.png"
    chrome = find_chrome()
    subprocess.run([chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=1200,16000",
                    f"--screenshot={raw}", f"file://{html}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    im = Image.open(raw).convert("RGB")
    W, H = im.size
    px = im.load()

    def differs(p):
        return (abs(p[0] - PAGE_BG[0]) > TOL or abs(p[1] - PAGE_BG[1]) > TOL or abs(p[2] - PAGE_BG[2]) > TOL)

    bottom = H
    for y in range(H - 1, 0, -1):
        if any(differs(px[x, y]) for x in range(0, W, 6)):
            bottom = min(H, y + 30)
            break
    crop = im.crop((0, 0, W, bottom))
    png_out, pdf_out = base + "-long.png", base + ".pdf"
    crop.save(png_out, "PNG")
    crop.save(pdf_out, "PDF", resolution=200.0)
    print(f"✓ 长图 {png_out}  ({crop.size[0]}x{crop.size[1]})")
    print(f"✓ PDF  {pdf_out}")


if __name__ == "__main__":
    main()
