# -*- coding: utf-8 -*-
"""Контактні аркуші ілюстрацій глибокого навчання — щоб швидко переглянути їх очима.

Запуск:  python figcheck.py route kitchen bytes      (лише ці)
         python figcheck.py --all                     (усі, по 6 на аркуш)
         python figcheck.py --dark route              (темна тема)
Результат: PNG у папці _figcheck поруч із цим файлом (не публікується).
"""
import pathlib
import re
import shutil
import sys

import build

OUT = build.SRC / "_figcheck"
DEFS = re.search(r'<svg class="svg-defs".*?</svg>', build.PAGE, re.S).group(0)


def sheet(names, path, dark=False):
    cells, heights = [], []
    for n in names:
        svg = (build.SRC / "deep" / "fig" / f"{n}.svg").read_text(encoding="utf-8")
        cells.append(f'<div class="cell"><div class="nm">{n}</div>{svg}</div>')
        m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
        heights.append(float(m.group(2)) * 386 / float(m.group(1)) if m else 360)
    theme = ' data-theme="dark"' if dark else ""
    page = (f'<!DOCTYPE html><html{theme}><head><meta charset="utf-8"><style>{build.CSS}'
            'body{padding:8px;margin:0}.grid{display:grid;grid-template-columns:400px 400px;gap:8px;align-items:start}'
            '.cell{background:var(--surface-2);border:1px solid var(--border);border-radius:10px;padding:6px}'
            '.cell svg{display:block;width:100%;height:auto}.nm{font:600 11px sans-serif;color:var(--muted)}'
            f'</style></head><body>{DEFS}<div class="grid">{"".join(cells)}</div></body></html>')
    tmp = OUT / "sheet.html"
    tmp.write_text(page, encoding="utf-8")
    height = int(24 + sum(max(heights[k:k + 2]) + 36 for k in range(0, len(heights), 2)))
    work = build.run_browser(lambda w: ["--hide-scrollbars", f"--window-size=830,{height}",
                                        f"--screenshot={w / 'shot.png'}", tmp.as_uri()])
    shutil.copyfile(work / "shot.png", path)
    shutil.rmtree(work, ignore_errors=True)
    print(path)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dark = "--dark" in sys.argv
    OUT.mkdir(exist_ok=True)
    names = sorted(p.stem for p in (build.SRC / "deep" / "fig").glob("*.svg")) if "--all" in sys.argv else args
    for k in range(0, len(names), 6):
        sheet(names[k:k + 6], OUT / f"sheet_{k // 6 + 1:02d}{'_dark' if dark else ''}.png", dark)


if __name__ == "__main__":
    main()
