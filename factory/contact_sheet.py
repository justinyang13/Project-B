#!/usr/bin/env python3
"""Make contact sheets (HTML -> PNG via headless Chrome) for reviewing illustrations.
usage: contact_sheet.py <slug> [per_sheet=20]   -> books/<slug>/sheets/sheet1.png ..."""
import json, pathlib, subprocess, sys
from lib.common import *
slug = sys.argv[1]; per = int(sys.argv[2]) if len(sys.argv) > 2 else 20
B = book_dir(slug); S = B / "sheets"; S.mkdir(exist_ok=True)
imgs = sorted((B / "images").glob("p[0-9][0-9][0-9].png"))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for i in range(0, len(imgs), per):
    chunk = imgs[i:i + per]
    cells = "".join(f'<div class="c"><img src="file://{p}"><b>{int(p.stem[1:])}</b></div>' for p in chunk)
    html = f'<html><body style="margin:0;background:#222"><style>body{{display:grid;grid-template-columns:repeat(5,300px);gap:6px;padding:6px;width:1530px}}.c{{position:relative}}img{{width:300px;height:300px;display:block}}b{{position:absolute;left:4px;top:4px;background:#000c;color:#fff;font:bold 16px sans-serif;padding:2px 6px;border-radius:4px}}</style>{cells}</body></html>'
    hp = S / f"sheet{i//per+1}.html"; hp.write_text(html)
    rows = (len(chunk) + 4) // 5
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files", f"--window-size=1542,{rows*306+12}",
                    f"--screenshot={S}/sheet{i//per+1}.png", f"file://{hp}"], capture_output=True)
    print("sheet", i // per + 1)
