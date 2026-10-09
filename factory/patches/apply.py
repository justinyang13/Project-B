#!/usr/bin/env python3
"""Apply (chapter, old, new) text patches to books/<slug>/chapters/chNN.json; each old string must exist exactly.
usage: patches/apply.py <slug>   (reads patches/<slug>.py defining PATCHES = [(ch, old, new), ...]; use ch=0 for 'any chapter')"""
import json, sys, importlib.util, pathlib
slug = sys.argv[1]; here = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("p", here / f"{slug}.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
B = here.parent / "books" / slug / "chapters"
done = 0
for ch, old, new in m.PATCHES:
    files = [B / f"ch{ch:02d}.json"] if ch else sorted(B.glob("ch*.json"))
    hit = 0
    for f in files:
        d = json.loads(f.read_text()); changed = False
        for p in d["pages"]:
            if old in p["text"]:
                p["text"] = p["text"].replace(old, new); changed = True; hit += 1
            if old in p.get("image", ""):
                p["image"] = p["image"].replace(old, new); changed = True; hit += 1
        if changed: f.write_text(json.dumps(d, indent=1, ensure_ascii=False))
    if not hit: print("NOT FOUND:", ch, old[:60])
    else: done += 1
print(f"{done}/{len(m.PATCHES)} patches applied")
