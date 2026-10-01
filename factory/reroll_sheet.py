#!/usr/bin/env python3
"""Contact sheet of selected pages (after a reroll batch). usage: reroll_sheet.py <slug> N [N..] -> books/<slug>/sheets/reroll.png"""
import pathlib, subprocess, sys
from lib.common import *
slug = sys.argv[1]; ns = [int(x) for x in sys.argv[2:]]
B = book_dir(slug); S = B / "sheets"; S.mkdir(exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cells = "".join(f'<div class="c"><img src="file://{B}/images/p{n:03d}.png"><b>{n}</b></div>' for n in ns)
html = f'<html><body style="margin:0;background:#222"><style>body{{display:grid;grid-template-columns:repeat(5,300px);gap:6px;padding:6px;width:1530px}}.c{{position:relative}}img{{width:300px;height:300px;display:block}}b{{position:absolute;left:4px;top:4px;background:#000c;color:#fff;font:bold 16px sans-serif;padding:2px 6px;border-radius:4px}}</style>{cells}</body></html>'
hp = S / "reroll.html"; hp.write_text(html); rows = (len(ns) + 4) // 5
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files", f"--window-size=1542,{rows*306+12}", f"--screenshot={S}/reroll.png", f"file://{hp}"], capture_output=True)
print(S / "reroll.png")
