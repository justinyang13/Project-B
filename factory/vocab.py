#!/usr/bin/env python3
"""Add a 'words to know' list (5 SAT-level words used in the chapter, with short definitions) to every chapters/chNN.json lacking 'words'.
usage: vocab.py <slug>   (Qwen picks words that actually appear in the chapter text; each is verified to occur)"""
import json, re, sys
from lib.common import *
slug = sys.argv[1]; B = book_dir(slug)
CFG = load_json(B / "config.json"); MODEL = CFG.get("model", "qwen3.8:27b")
SYS = "You are a careful high-school English teacher building SAT-style vocabulary lists. Output only the list."
for f in sorted((B / "chapters").glob("ch*.json")):
    ch = load_json(f)
    if ch.get("words"): continue
    txt = "\n\n".join(p["text"] for p in ch["pages"])
    pr = f"""Chapter text:
{txt}

Pick exactly 5 words that appear IN THIS TEXT (exact spelling as written, base form allowed only if it appears) and that a strong high-school reader should learn for the SAT: advanced, useful, general-purpose words (not character names, not invented fantasy words, not proper nouns, not simple words). For each give a short plain definition (under 12 words) that fits how the word is used here.
Format, one per line, nothing else:
word: definition"""
    for attempt in range(3):
        out = ollama(MODEL, SYS, pr, temperature=0.4, num_predict=500)
        words = []
        for line in out.splitlines():
            m = re.match(r"\s*[-*\d.)]*\s*\**([A-Za-z'-]+)\**\s*[:–-]\s*(.+)", line)
            if m and re.search(r"\b" + re.escape(m[1][:max(4, len(m[1]) - 2)]), txt, re.I): words.append([m[1].lower(), m[2].strip().rstrip(".")])
        if len(words) >= 4: break
    ch["words"] = words[:5]; f.write_text(json.dumps(ch, indent=1, ensure_ascii=False))
    print(f.name, [w[0] for w in ch["words"]])
