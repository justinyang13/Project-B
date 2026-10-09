#!/usr/bin/env python3
"""Draft -> lint -> edit-revise each chapter with local Qwen (Ollama HTTP API).
usage: write_book.py <slug> [first [last]] [--model NAME] [--out DIRNAME] [--no-edit]
books/<slug>/{bible.md, outline.json, config.json}"""
import json, re, sys, time
from lib.common import *
from lib.lint import lint, starter_runs, short_share, SIMILE

args = [a for a in sys.argv[1:] if not a.startswith("--")]
flags = sys.argv[1:]
def flag(name, default=None):
    return flags[flags.index(name) + 1] if name in flags else default
SLUG = args[0]
B = book_dir(SLUG)
BIBLE = (B / "bible.md").read_text()
OUTLINE = {c["n"]: c for c in load_json(B / "outline.json")["chapters"]}
CFG = load_json(B / "config.json")
MODEL = flag("--model", CFG.get("model", "qwen3.8:27b"))
OUTDIR = B / flag("--out", "chapters"); OUTDIR.mkdir(exist_ok=True)
TMP = B / "tmp"; TMP.mkdir(exist_ok=True)
MINW, MAXW = CFG.get("min_words", 170), CFG.get("max_words", 320)
AUD = CFG.get("audience", "middle-grade readers aged 10 to 12")
WORLD = CFG.get("audience_world", "an 11-year-old's world (cereal, school, video games, siblings)")
TARGET = CFG.get("target_words", "150-200"); HARD = CFG.get("hard_words", 240)
SHORT_LO, SHORT_HI = CFG.get("short_lo", 0.12), CFG.get("short_hi", 0.40)
LONG_S = CFG.get("long_sentence", 50); SIM_MAX = CFG.get("sim_max", 2)
EXTRA_CRAFT = CFG.get("extra_craft", "")
EDIT = "--no-edit" not in flags
N = len(OUTLINE)
EXEMPLAR = ""
_ex = B / "src" / "ch01.txt"
if _ex.exists():
    EXEMPLAR = "\n\nGOLD-STANDARD EXAMPLE: chapter 1, finished by the senior editor. Match its voice, humor, specificity, rhythm, paragraphing and dialogue style exactly (do not copy its events):\n<example>\n" + _ex.read_text() + "\n</example>\n"

SYSTEM = f"""You are an award-winning, best-selling novelist writing for {AUD}.
You are writing the novel described in this bible. Follow it faithfully: names, looks, voice, rules.

{BIBLE}

CRAFT RULES (apply to every page):
- Specific beats general. One surprising, concrete detail beats three adjectives. Name the exact thing (not "a snack": "a squashed cheese sandwich").
- Show feelings through action, body, and what a character notices or avoids. Never name a feeling and then explain it.
- Fresh comparisons only, drawn from the hero's own world. Never use a comparison that could appear in any other book. Avoid stock phrases from thrillers and romance.
- Dialogue is quick, with interruptions; each character speaks in their own distinct way. No speeches. Adults are not wise-sages.
- Vary rhythm. Mix short sentences with long, flowing, comic ones. NEVER string together three or more short declarative sentences in a row, and never start three sentences in a row with the same word (no 'It was. It was. It was.' or 'I looked. I looked.'). Combine them, add a clause, cut some.
- Humor comes from character and specifics, not from the narrator announcing something is funny.
- Do not use em dashes. Use commas, periods, or parentheses.
- At most two comparisons (like / as if) per page, each fresh and specific to {WORLD}. Otherwise use plain, exact description. No sentence longer than 40 words.
- The book's life lesson must be DRAMATIZED through choices and consequences, never stated by the narrator as a moral.
{EXTRA_CRAFT}
{EXEMPLAR}"""

def synopsis(c): return f"Ch{c['n']} \"{c['title']}\": {c['synopsis']}"

def build_prompt(n, tail, used):
    c = OUTLINE[n]
    ctx = "STORY SO FAR (outline of earlier chapters, in order):\n" + ("\n".join(synopsis(OUTLINE[k]) for k in range(1, n)) or "(this is the first chapter)") + "\n\n"
    if tail: ctx += "THE LAST PAGE OF THE PREVIOUS CHAPTER (continue naturally from it; do not repeat it):\n" + tail + "\n\n"
    later = "\n".join(synopsis(OUTLINE[k]) for k in (n + 1, n + 2) if k in OUTLINE)
    beats = "\n".join(f"PAGE {i+1}: {b}" for i, b in enumerate(c["beats"]))
    sim = ""
    if used: sim = "COMPARISONS ALREADY USED IN THIS BOOK (do not reuse or echo any of them):\n" + "; ".join(used[-60:]) + "\n\n"
    hdr = f"\nThe chapter's header line ({c['header']!r}) is added automatically: do NOT write it or any similar line; start straight into the story.\n" if c.get("header") else ""
    return f"""{ctx}{sim}Now write CHAPTER {n} of {N}: "{c['title']}" ({c['part']}).{hdr}
The five pages, with what must happen on each:
{beats}

These happen in LATER chapters. Do NOT include, name, or hint at them here:
{later or '(none)'}

Requirements:
- Exactly 5 book pages, each about {TARGET} words (hard limit {HARD}) of polished story prose that dramatizes its beat as a scene with dialogue and concrete detail. Do not summarize.
- Every page ends on a hook, a laugh or a feeling; the chapter's last page ends stronger.
- Do not write the chapter heading; start straight into the story. No markdown or bold.
- After each page add one line beginning "IMAGE:" with a 25-40 word prompt for a small spot illustration of the most visual moment on that page: a single clear scene in plain visual language (subject, setting, action, mood), restating main characters' looks per the bible. No text, letters, signs or writing in the picture.

Use exactly this format:
=== PAGE 1 ===
(page text)
IMAGE: (image prompt)
=== PAGE 2 ===
...
=== PAGE 5 ===
..."""

def check(n, pages, used):
    issues = []
    if len(pages) != 5: issues.append(f"has {len(pages)} pages, need 5")
    for i, p in enumerate(pages, 1):
        w = wc(p["text"])
        if w < MINW: issues.append(f"page {i} too short ({w} words)")
        if w > MAXW: issues.append(f"page {i} too long ({w} words)")
        if not p["image"]: issues.append(f"page {i} missing IMAGE")
    txt = " ".join(p["text"] for p in pages)
    for term, first in CFG.get("first_allowed", {}).items():
        if n < first and term.lower() in txt.lower(): issues.append(f"leaks future term '{term}'")
    f, sims = lint(txt, CFG.get("extra_banned", []), used)
    f = [x for x in f if not x.startswith(("staccato", "too many very short"))]
    return issues + f, sims

def score(issues):  # structural problems weigh more than style tics
    return sum(5 if re.search(r"pages, need|too short|too long|missing IMAGE|leaks", s) else 1 for s in issues)

def revise_prompt(n, pages, issues):
    draft = "\n".join(f"=== PAGE {i+1} ===\n{p['text']}\nIMAGE: {p['image']}" for i, p in enumerate(pages))
    fix = "\n".join(f"- {s}" for s in issues) or "- (no automatic problems found)"
    return f"""Here is a draft of chapter {n} ("{OUTLINE[n]['title']}"). You are the senior editor. Rewrite it into its best final form.

DRAFT:
{draft}

AUTOMATIC PROBLEMS TO FIX:
{fix}

You MUST actually rewrite the prose: do not return the draft unchanged. At least half of the sentences must be reworded. In particular, join runs of short sentences into longer, funnier ones (use commas, "and", "which", parentheses), replace generic comparisons (like a stone, like a needle, dry leaves) with fresh, specific, kid-world ones, and add one surprising concrete detail per page. Match the voice of the gold-standard example chapter in the system prompt.

EDITOR'S CHECKLIST:
- Keep every event, the five-page structure, names and facts. Do not add events from later chapters.
- Replace every stock phrase and generic comparison with a specific, surprising, character-true one.
- Sharpen the dialogue: shorter lines, real interruptions, each speaker clearly different.
- Cut anything a narrator explains that a reader can feel. Trim adverbs. Fix flabby openings.
- Make the jokes land with precise details. Make every page-ending line stronger.
- Each page must be about {TARGET} words (never above {HARD}): keep only the best details. No em dashes. No markdown.
- Keep the exact same output format: === PAGE n === / prose / IMAGE: line, for all 5 pages. Output only the chapter."""

def sentences(t): return [x for x in re.split(r"(?<=[.!?])\s+", t) if x.strip()]

def page_issues(text, used):
    """Per-page style problems Qwen can fix by rewriting just that page. Thresholds calibrated on the gold chapter."""
    narr = re.sub(r'"[^"]*"', '', text)
    f, _ = lint(text, CFG.get("extra_banned", []), used)
    f = [x for x in f if not x.startswith(("staccato", "too many very short"))]
    if starter_runs(narr) > 1: f.append("several runs of 3+ sentences start with the same word; reword them")
    sh = short_share(narr)
    if sh > SHORT_HI: f.append(f"{sh:.0%} of the narration sentences are 5 words or fewer; join some into medium sentences (aim 20-35%)")
    if sh < SHORT_LO: f.append("no short punchy sentences; add a few very short ones for rhythm and comic timing (aim 20-35%)")
    long_s = [x for x in sentences(narr) if len(x.split()) > LONG_S]
    if long_s: f.append(f"a sentence is {len(long_s[0].split())} words long; split it (no sentence over 45 words): '{long_s[0][:60]}...'")
    if CFG.get("present_tense"):
        past = len(re.findall(r"\b(I|we|she|he|they) (was|were|had|looked|walked|felt|saw|said|took|went|stood|sat|knew|thought|heard|turned|watched|ran|opened|held|pointed|nodded|smiled|asked|grabbed|stepped|kicked|laughed|shrugged)\b", narr))
        if past > 1: f.append(f"the narration slipped into PAST tense ({past} past-tense verbs); this book is FIRST PERSON PRESENT TENSE: rewrite every past-tense narration verb in the present ('I look', 'she says')")
    sims = SIMILE.findall(text)
    if len(sims) > SIM_MAX: f.append(f"{len(sims)} comparisons on one page (like/as if...); keep only the best {SIM_MAX} and turn the rest into plain concrete description")
    w = wc(text)
    if w > MAXW: f.append(f"too long ({w} words); cut to about {TARGET} words")
    if w < MINW: f.append(f"too short ({w} words); expand to about {TARGET} words with concrete detail")
    return f

def polish_page(n, i, pages, used):
    """Rewrite one page until its style lint passes (max 4 rounds). Keeps the best version."""
    p = pages[i]; best_t, best_i = p["text"], page_issues(p["text"], used)
    for rnd in range(4):
        if not best_i: break
        prev = pages[i-1]["text"] if i else ""
        pr = f"""Rewrite ONE page of a novel chapter. Keep every event, fact, name and the joke content of the page. Change only the writing.

PREVIOUS PAGE (for continuity only, do not repeat it):
{prev or '(none)'}

THE PAGE TO REWRITE:
{best_t}

PROBLEMS TO FIX:
""" + "\n".join(f"- {x}" for x in best_i) + f"""

How: fix ONLY the listed problems, changing as little else as possible. Never stack comparisons: at most {SIM_MAX} per page, each fresh and specific to {WORLD}, otherwise plain concrete description. Keep sentences clear (most under 30 words), with a natural mix of short and medium ones. Keep the dialogue lively. Target about {TARGET} words (never over {HARD}). No em dashes. Keep the voice of the gold-standard example. Output ONLY the rewritten page text: no heading, no notes, no IMAGE line."""
        new = ollama(MODEL, SYSTEM, pr, temperature=0.8, num_predict=900).strip()
        new = re.sub(r"^=== PAGE \d+ ===\s*", "", new); new = re.split(r"\nIMAGE:", new)[0].strip()
        ni = page_issues(new, used)
        print(f"   ch{n} p{i+1} polish{rnd+1}: {wc(new)}w issues {len(best_i)} -> {len(ni)}", flush=True)
        if len(ni) < len(best_i) or (len(ni) == len(best_i) and rnd == 0): best_t, best_i = new, ni
    return best_t, best_i

def write_chapter(n, tail, used):
    c = OUTLINE[n]; best = None
    def keep(pages, issues, sims, tag):
        nonlocal best
        s = score(issues)
        print(f"ch{n} {tag}: words {[wc(p['text']) for p in pages]} issues {len(issues)} score {s}", flush=True)
        for i in issues: print("   -", i, flush=True)
        if len(pages) == 5 and all(p['image'] for p in pages) and (best is None or s < best[0]):
            best = (s, pages, issues, sims)
    for attempt in range(3):
        raw = ollama(MODEL, SYSTEM, build_prompt(n, tail, used))
        (TMP / f"ch{n:02d}_draft{attempt+1}.txt").write_text(raw)
        pages = parse_chapter(raw); issues, sims = check(n, pages, used)
        keep(pages, issues, sims, f"draft{attempt+1}")
        if not issues: break
        if best and score(best[2]) <= 2 and attempt >= 1: break
    if EDIT and best:
        _, pages, _, _ = best
        for i in range(len(pages)):
            pages[i]["text"], _ = polish_page(n, i, pages, used)
        issues, sims = check(n, pages, used)
        best = (score(issues), pages, issues, sims)
        print(f"ch{n} after polish: words {[wc(p['text']) for p in pages]} issues {len(issues)}", flush=True)
        for x in issues: print("   -", x, flush=True)
    if not best: raise SystemExit(f"chapter {n} produced no usable draft")
    _, pages, issues, sims = best
    if c.get("header"):
        pages[0]["text"] = re.sub(r"^\s*(T-MINUS[^\n]*|\*[^\n]*\*)\s*", "", pages[0]["text"])  # drop any header the model wrote anyway
        pages[0]["text"] = c["header"] + "\n\n" + pages[0]["text"]
    return dict(n=n, title=c["title"], part=c["part"], pages=pages, lint=issues), sims

if __name__ == "__main__":
    first = int(args[1]) if len(args) > 1 else 1
    last = int(args[2]) if len(args) > 2 else N
    used = []
    for f in sorted(OUTDIR.glob("ch*.json")):  # simile ledger from chapters already written
        d = json.loads(f.read_text()); used += lint(" ".join(p["text"] for p in d["pages"]))[1]
    for n in range(first, last + 1):
        f = OUTDIR / f"ch{n:02d}.json"
        if f.exists(): print(f"ch{n} exists, skipping", flush=True); continue
        tail = ""
        if n > 1:
            pf = OUTDIR / f"ch{n-1:02d}.json"
            if pf.exists(): tail = json.loads(pf.read_text())["pages"][-1]["text"]
        t0 = time.time()
        ch, sims = write_chapter(n, tail, used)
        used += sims
        f.write_text(json.dumps(ch, indent=1, ensure_ascii=False))
        print(f"ch{n} saved: {ch['title']} ({time.time()-t0:.0f}s, {len(ch['lint'])} remaining lint issues)", flush=True)
