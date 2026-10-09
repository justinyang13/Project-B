#!/usr/bin/env python3
"""Assemble a finished book: web-size images + self-contained reader.
usage: build_html.py <slug>  -> books/<slug>/book/{index.html,img/}
books/<slug>/meta.json: {title, subtitle, ages, genre, blurb}"""
import html, json, pathlib, subprocess, sys
from lib.common import *
slug = sys.argv[1]; B = book_dir(slug); OUT = B / "book"; (OUT / "img").mkdir(parents=True, exist_ok=True)
M = load_json(B / "meta.json")

def small(src, dst, px):
    if src.exists() and (not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime):
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", "-Z", str(px), str(src), "--out", str(dst)],
                       capture_output=True, check=True)

pages, chapters, n = [], [], 0
for f in sorted((B / "chapters").glob("ch*.json")):
    ch = load_json(f)
    chapters.append(dict(n=ch["n"], title=ch["title"], part=ch["part"], page=n + 1))
    for i, p in enumerate(ch["pages"]):
        n += 1
        words = ch.get("words") if i == len(ch["pages"]) - 1 else None
        small(B / "images" / f"p{n:03d}.png", OUT / "img" / f"p{n:03d}.jpg", 640)
        pages.append(dict(no=n, ch=ch["n"], ctitle=ch["title"] if i == 0 else "", part=ch["part"] if i == 0 else "",
                          paras=[" ".join(x.split()) for x in p["text"].split("\n\n") if x.strip()] + (["\u25c6 Words to know: " + "; ".join(f"{w} \u2013 {d}" for w, d in words)] if words else []), img=f"img/p{n:03d}.jpg"))
for name in ("front", "back"):
    small(B / "images" / f"cover_{name}_final.png", OUT / "img" / f"cover_{name}.jpg", 1400)
data = json.dumps(dict(title=M["title"], sub=M["subtitle"], author=M.get("author", ""), publisher=M.get("publisher", ""), pages=pages, chapters=chapters), ensure_ascii=False)
tpl = (FACTORY / "reader_template.html").read_text()
(OUT / "index.html").write_text(tpl.replace("/*__DATA__*/null", data).replace("__TITLE__", html.escape(M["title"])))
print(f"built {len(pages)} pages, {len(chapters)} chapters -> {OUT/'index.html'}")
