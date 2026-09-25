#!/usr/bin/env python3
"""Assemble the finished book: web-size images + a self-contained reader (index.html)."""
import html, json, pathlib, subprocess

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "book"; (OUT / "img").mkdir(parents=True, exist_ok=True)
TITLE, SUB = "Juno Vale and the Tide That Forgot", "A Saltmarsh Harbor Adventure"

def small(src, dst, px):
    if not dst.exists() and src.exists():
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", "-Z", str(px), str(src), "--out", str(dst)],
                       capture_output=True, check=True)

pages, chapters, n = [], [], 0
for f in sorted((ROOT / "chapters").glob("ch*.json")):
    ch = json.loads(f.read_text())
    chapters.append(dict(n=ch["n"], title=ch["title"], part=ch["part"], page=n + 1))
    for i, p in enumerate(ch["pages"]):
        n += 1
        small(ROOT / "images" / f"p{n:03d}.png", OUT / "img" / f"p{n:03d}.jpg", 640)
        pages.append(dict(no=n, ch=ch["n"], ctitle=ch["title"] if i == 0 else "", part=ch["part"] if i == 0 else "",
                          paras=[" ".join(x.split()) for x in p["text"].split("\n\n") if x.strip()],
                          img=f"img/p{n:03d}.jpg"))
for name in ("front", "back"):
    src = ROOT / "images" / f"cover_{name}_final.png"
    small(src, OUT / "img" / f"cover_{name}.jpg", 1400)

data = json.dumps(dict(title=TITLE, sub=SUB, pages=pages, chapters=chapters), ensure_ascii=False)
tpl = (ROOT / "reader_template.html").read_text()
(OUT / "index.html").write_text(tpl.replace("/*__DATA__*/null", data).replace("__TITLE__", html.escape(TITLE)))
print(f"built {len(pages)} pages, {len(chapters)} chapters -> {OUT/'index.html'}")
