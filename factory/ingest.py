#!/usr/bin/env python3
"""Ingest hand-finished chapter source (books/<slug>/src/chNN.txt) into chapters/chNN.json and print the lint report.
usage: ingest.py <slug> [chapter numbers...]   (default: all in src/)
Source format: === PAGE n === / prose (blank-line paragraphs) / IMAGE: one-line illustration prompt"""
import json, re, sys
from lib.common import *
from lib.lint import lint
slug = sys.argv[1]; B = book_dir(slug); (B / "chapters").mkdir(exist_ok=True)
CFG = load_json(B / "config.json"); OUT = {c["n"]: c for c in load_json(B / "outline.json")["chapters"]}
want = [int(x) for x in sys.argv[2:]] or sorted(int(re.search(r"ch(\d+)", f.name)[1]) for f in (B / "src").glob("ch*.txt"))
used = []
for f in sorted((B / "chapters").glob("ch*.json")):
    used += lint(" ".join(p["text"] for p in load_json(f)["pages"]))[1]
for n in want:
    raw = (B / "src" / f"ch{n:02d}.txt").read_text()
    pages = parse_chapter(raw)
    ws = [wc(p["text"]) for p in pages]
    txt = " ".join(p["text"] for p in pages)
    issues, sims = lint(txt, CFG.get("extra_banned", []), [])
    if len(pages) != 5: issues.append(f"{len(pages)} pages")
    issues += [f"page {i+1} has no IMAGE" for i, p in enumerate(pages) if not p["image"]]
    for term, first in CFG.get("first_allowed", {}).items():
        if n < first and term.lower() in txt.lower(): issues.append(f"leaks '{term}'")
    (B / "chapters" / f"ch{n:02d}.json").write_text(json.dumps(dict(n=n, title=OUT[n]["title"], part=OUT[n]["part"], pages=pages), indent=1, ensure_ascii=False))
    print(f"ch{n:02d} {OUT[n]['title']}: words {ws} total {sum(ws)}" + (" | " + "; ".join(issues) if issues else " | clean"))
