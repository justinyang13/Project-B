#!/usr/bin/env python3
"""Publish a finished book into the Project-B repo (does NOT push; prints next steps).
usage: release.py <slug>"""
import json, pathlib, shutil, subprocess, sys
from lib.common import *
slug = sys.argv[1]; B = book_dir(slug); M = load_json(B / "meta.json")
REPO = FACTORY.parent; D = REPO / slug  # factory lives in Project-B/factory
import datetime
# release date = the day of the FIRST release; kept on every re-release (from the old book.json, else meta.json, else today)
released = (load_json(D / "book.json").get("released") if (D / "book.json").exists() else None) or M.get("released") or datetime.date.today().isoformat()
if D.exists(): shutil.rmtree(D)
(D / "source").mkdir(parents=True)
shutil.copytree(B / "book", D, dirs_exist_ok=True)
for n in ("front", "back"): shutil.copy(B / "images" / f"cover_{n}_final.png", D / f"cover_{n}.png")
shutil.copy(B / "bible.md", D / "source"); shutil.copy(B / "outline.md", D / "source")
shutil.copytree(B / "chapters", D / "source" / "chapters")
chs = sorted((B / "chapters").glob("ch*.json"))
book = dict(title=M["title"], subtitle=M["subtitle"], cover="img/cover_front.jpg", ages=M["ages"], pages=sum(len(load_json(c)["pages"]) for c in chs), chapters=len(chs), genre=M["genre"], blurb=M["blurb"], released=released)
for k in ("author", "publisher", "shelf"):
    if M.get(k): book[k] = M[k]
(D / "book.json").write_text(json.dumps(book, indent=1, ensure_ascii=False))
subprocess.run([sys.executable, str(REPO / "build_index.py")], check=True)
(FACTORY / "dist").mkdir(exist_ok=True); zp = FACTORY / "dist" / f"{slug}.zip"
subprocess.run(["zip", "-qr", str(zp), slug, "-x", "*/source/*"], cwd=REPO, check=True)
print("released into", D, "| zip:", zp)
