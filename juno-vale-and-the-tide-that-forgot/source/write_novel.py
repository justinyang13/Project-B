#!/usr/bin/env python3
"""Have local qwen3.8:27b write the novel chapter by chapter (direct Ollama HTTP API).
usage: write_novel.py [first [last]]   (chapter numbers, 1-20)"""
import json, re, sys, time, urllib.request, pathlib

ROOT = pathlib.Path(__file__).parent
BIBLE = (ROOT / "bible.md").read_text()
MODEL = "qwen3.8:27b"
PAGES = 5
MIN_WORDS, MAX_WORDS = 150, 380

# split outline into chapters
outline = BIBLE.split("## Chapter outline", 1)[1]
CHAPTERS = {}
part = ""
for line in outline.splitlines():
    if line.startswith("PART"):
        part = line.strip()
    m = re.match(r"(\d+)\. \*\*(.+?)\.\*\* (.*)", line)
    if m:
        CHAPTERS[int(m[1])] = dict(title=m[2], beats=m[3], part=part)

SYSTEM = f"""You are an award-winning middle-grade novelist writing for readers aged 10 to 12.
You are writing the novel described in this story bible. Follow it faithfully: names, looks, traits, magic rules.

{BIBLE.split('## Chapter outline')[0]}
"""

def chat(prompt, temperature=0.8):
    body = json.dumps(dict(model=MODEL, stream=True, think=False,
        options=dict(temperature=temperature, num_ctx=16384, num_predict=6000),
        messages=[dict(role="system", content=SYSTEM), dict(role="user", content=prompt)])).encode()
    req = urllib.request.Request("http://localhost:11434/api/chat", body, {"Content-Type": "application/json"})
    out = []
    with urllib.request.urlopen(req, timeout=3600) as r:
        for line in r:
            d = json.loads(line)
            out.append(d.get("message", {}).get("content", ""))
            if d.get("done"): break
    return "".join(out)

def parse(text):
    pages = []
    for blk in re.split(r"=== PAGE \d+ ===", text)[1:]:
        blk = blk.split("=== SUMMARY ===")[0]
        m = re.search(r"^IMAGE:\s*(.+)$", blk, re.M | re.S)
        img = m.group(1).strip() if m else ""
        body = blk[:m.start()] if m else blk
        pages.append(dict(text=body.strip(), image=" ".join(img.split())))
    s = re.search(r"=== SUMMARY ===\s*(.+)", text, re.S)
    return pages, (s.group(1).strip() if s else "")

def wc(s): return len(s.split())

# first chapter in which each term may appear (keeps later plot out of early chapters)
FIRST_ALLOWED = {"Grubb":5, "Teo":4, "Fathom":8, "Nautilia":11, "Dolly Marigold":8, "Barnacle":3}
def leaks(n, pages):
    txt = " ".join(p["text"] for p in pages).lower()
    return [k for k, first in FIRST_ALLOWED.items() if n < first and k.lower() in txt]

def write_chapter(n, prev_summaries, prev_tail):
    c = CHAPTERS[n]
    ctx = ""
    if prev_summaries:
        ctx += "STORY SO FAR (summaries of earlier chapters):\n" + "\n".join(prev_summaries) + "\n\n"
    if prev_tail:
        ctx += "THE LAST PAGE OF THE PREVIOUS CHAPTER (continue naturally from it, do not repeat it):\n" + prev_tail + "\n\n"
    later = "\n".join(f"- Ch{k}: {CHAPTERS[k]['beats']}" for k in (n + 1, n + 2) if k in CHAPTERS)
    prompt = f"""{ctx}Now write CHAPTER {n} of 20: "{c['title']}" ({c['part']}).
Chapter beats to cover: {c['beats']}

These events happen in LATER chapters. Do NOT include, hint at by name, or start them in this chapter:
{later}

Requirements:
- Exactly {PAGES} book pages. Each page is about 190-230 words of polished story prose (hard limit: never more than 260 words per page): vivid sensory detail, lots of natural dialogue, humor, feeling. Short paragraphs. Do not summarize; dramatize scenes.
- Each page must feel like a page of a real novel and end on a small hook, laugh or emotional beat. The chapter's final page ends with a stronger hook (unless it is the last chapter).
- Stay strictly inside this chapter's beats. Do not reveal, resolve or foreshadow-by-showing objects or events that belong to later chapters (respect the Secrets section of the bible). Keep the timeline: the story spans nine days, so tell the reader the day when it matters.
- Do NOT write the chapter heading; start straight into the story text. No markdown, no bold, no headings inside the prose.
- After each page's text add one line beginning with "IMAGE:" containing a 25-40 word prompt for a small spot illustration of the most visual moment on that page. Describe it as a single clear scene in plain visual language (subject, setting, action, mood). When a main character appears, restate their look (Juno: curly dark-brown hair in two puffs, freckles, yellow raincoat; Teo: round glasses, messy black hair, green cap, tool belt; Grandpa Ozzie: tall, bushy white beard, blue knitted hat, driftwood cane; Biscuit: fat orange cat with a chewed left ear; Barnacle: small hermit crab in a chipped blue teapot shell). No text or lettering in the picture.
- Then a final "=== SUMMARY ===" section with a 3-sentence summary of what happened in this chapter (names, objects, facts that later chapters need).

Use exactly this format:
=== PAGE 1 ===
(page text)
IMAGE: (image prompt)
=== PAGE 2 ===
...
=== PAGE {PAGES} ===
...
=== SUMMARY ===
(3 sentences)"""
    fallback = None
    for attempt in range(4):
        t0 = time.time()
        raw = chat(prompt)
        pages, summary = parse(raw)
        counts = [wc(p["text"]) for p in pages]
        print(f"ch{n} attempt {attempt+1}: {len(pages)} pages, words {counts}, {time.time()-t0:.0f}s", flush=True)
        (ROOT / "tmp" / f"ch{n:02d}_attempt{attempt+1}.txt").write_text(raw)
        bad = leaks(n, pages)
        if bad: print("  leaked future terms:", bad, flush=True)
        ok = not bad and len(pages) == PAGES and all(MIN_WORDS <= x <= MAX_WORDS for x in counts) \
             and all(p["image"] for p in pages) and summary
        if ok:
            return dict(n=n, title=c["title"], part=c["part"], pages=pages, summary=summary)
        if len(pages) == PAGES and all(p["image"] for p in pages) and all(100 <= x <= 450 for x in counts):
            fallback = min(fallback or [99, None], [len(bad), dict(n=n, title=c["title"], part=c["part"], pages=pages, summary=summary)], key=lambda z: z[0])
    if fallback:
        print(f"ch{n}: using best fallback ({fallback[0]} leaks)", flush=True); return fallback[1]
    raise SystemExit(f"chapter {n} failed quality gate after retries")

if __name__ == "__main__":
    first = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    last = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    (ROOT / "chapters").mkdir(exist_ok=True)
    for n in range(first, last + 1):
        f = ROOT / "chapters" / f"ch{n:02d}.json"
        if f.exists():
            print(f"ch{n} exists, skipping", flush=True); continue
        sums = []
        for k in range(1, n):
            sums.append(f"Ch{k} ({CHAPTERS[k]['title']}): {CHAPTERS[k]['beats']}")
        tail = ""
        if n > 1:
            d = json.loads((ROOT / "chapters" / f"ch{n-1:02d}.json").read_text())
            tail = d["pages"][-1]["text"]
        ch = write_chapter(n, sums, tail)
        f.write_text(json.dumps(ch, indent=1, ensure_ascii=False))
        print(f"ch{n} saved: {ch['title']}", flush=True)
