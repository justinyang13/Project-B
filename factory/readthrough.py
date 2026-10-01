#!/usr/bin/env python3
"""Qwen continuity/quality read-through: chunks of 4 chapters vs the bible. Writes books/<slug>/review.md
usage: readthrough.py <slug> [model]"""
import sys
from lib.common import *
slug = sys.argv[1]; model = sys.argv[2] if len(sys.argv) > 2 else "qwen3.8:27b"
B = book_dir(slug); bible = (B / "bible.md").read_text(); outline = load_json(B / "outline.json")["chapters"]
chs = [load_json(f) for f in sorted((B / "chapters").glob("ch*.json"))]
SYS = "You are a meticulous continuity editor for a middle-grade novel (ages 10-12). Be concrete and terse. Only report REAL problems; do not pad."
out = ["# Read-through review\n"]
for i in range(0, len(chs), 4):
    grp = chs[i:i + 4]
    text = "\n\n".join(f"## CHAPTER {c['n']}: {c['title']}\n" + "\n".join(f"[p{j+1}] {p['text']}" for j, p in enumerate(c["pages"])) for c in grp)
    beats = "\n".join(f"Ch{c['n']} {c['title']}: {c['synopsis']}" for c in outline[i:i + 4])
    prompt = f"""STORY BIBLE:\n{bible}\n\nINTENDED CONTENT OF THESE CHAPTERS:\n{beats}\n\nCHAPTERS AS WRITTEN:\n{text}\n\nList concrete problems, one per line, in this format:
CH<n> p<page>: <problem type> | QUOTE: "<exact short phrase>" | FIX: <replacement phrase or instruction>
Problem types: CONTINUITY (contradicts bible/other chapters/timeline), LOGIC (nonsensical action, e.g. a time that doesn't fit), TENSE (slips out of past tense), VOICE (adult vocabulary or wrong narrator), MISSING (a required beat from the intended content is absent), TIC (repeated cliche construction such as 'It wasn't X. It was Y.'), SPOOKY (anything ghostly or scary), TYPO.
Maximum 12 lines. If there are no real problems in a chapter say nothing about it."""
    print("reviewing chapters", grp[0]["n"], "-", grp[-1]["n"], flush=True)
    r = ollama(model, SYS, prompt, temperature=0.3, num_ctx=32768, num_predict=1500)
    out.append(f"\n## Chapters {grp[0]['n']}-{grp[-1]['n']}\n{r.strip()}\n")
(B / "review.md").write_text("\n".join(out)); print("wrote review.md")
