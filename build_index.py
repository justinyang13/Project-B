#!/usr/bin/env python3
"""Regenerate the library home page (index.html) from every <book>/book.json.
To add a book: create a folder with an index.html reader and a book.json, then run this script."""
import html, json, pathlib

ROOT = pathlib.Path(__file__).parent
# Display order on the home page. Any book not listed here is added at the bottom (alphabetically).
ORDER = [
    "juno-vale-and-the-tide-that-forgot",
    "mei-and-the-dragon-who-feared-thunder",
    "mo-and-the-mountain-that-walks",
    "rue-and-the-troll-under-bridgewater-bridge",
    "the-day-that-wouldnt-end",
    "the-garden-at-the-edge-of-the-concrete",
    "pip-and-the-storm-sparrows",
    "zia-and-the-runaway-space-station",
    "lin-and-the-night-market-lanterns",
    "fifty-one-ways-to-lose-a-soccer-game",
    "the-mapmakers-apprentice",
    "robot-who-was-bad-at-everything",
]
books = []
for f in sorted(ROOT.glob("*/book.json")):
    b = json.loads(f.read_text()); b["dir"] = f.parent.name; books.append(b)
books.sort(key=lambda b: ORDER.index(b["dir"]) if b["dir"] in ORDER else len(ORDER))

cards = "\n".join(f'''    <a class="card" href="{html.escape(b['dir'])}/index.html">
      <img src="{html.escape(b['dir'])}/{html.escape(b['cover'])}" alt="Cover of {html.escape(b['title'])}" loading="lazy">
      <div class="info">
        <h2>{html.escape(b['title'])}</h2>
        <p class="sub">{html.escape(b['subtitle'])}</p>
        <p class="meta">Ages {html.escape(b['ages'])} · {b['pages']} pages · {b['chapters']} chapters</p>
        <p class="blurb">{html.escape(b['blurb'])}</p>
        <span class="read">Read the book →</span>
      </div>
    </a>''' for b in books)

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Project B — Illustrated Novels</title>
<meta name="description" content="A library of illustrated adventures for curious young readers. Stories about courage, kindness, patience and finding your own way.">
<style>
:root{{--bg:#12202c;--bg2:#1b3244;--ink:#f6efdc;--muted:#b9c3c9;--gold:#f3c76a;--card:#f8f1df;--cardink:#2b2a28}}
*{{box-sizing:border-box}}
body{{margin:0;min-height:100vh;background:radial-gradient(ellipse at 50% 0,var(--bg2),var(--bg) 70%);color:var(--ink);font-family:Georgia,"Iowan Old Style","Palatino Linotype",serif}}
header{{text-align:center;padding:64px 20px 28px}}
.kicker{{font:600 .8rem system-ui,sans-serif;letter-spacing:.42em;text-transform:uppercase;color:var(--gold)}}
h1{{font-family:Baskerville,"Palatino Linotype",Georgia,serif;font-size:clamp(2.6rem,7vw,4.6rem);margin:.15em 0 .1em;color:var(--gold);text-shadow:0 3px 0 #7a4a08,0 8px 24px #0008}}
header p{{max-width:38rem;margin:.6em auto 0;color:var(--muted);font-size:1.15rem;line-height:1.55}}
main{{max-width:1100px;margin:0 auto;padding:24px 20px 80px}}
.shelf{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,460px),1fr));gap:28px}}
.card{{display:flex;gap:22px;background:var(--card);color:var(--cardink);border-radius:14px;padding:18px;text-decoration:none;box-shadow:0 14px 34px #0007;transition:transform .18s,box-shadow .18s}}
.card:hover,.card:focus-visible{{transform:translateY(-4px);box-shadow:0 20px 40px #000a;outline:3px solid var(--gold)}}
.card img{{width:44%;max-width:210px;aspect-ratio:2/3;object-fit:cover;border-radius:6px;box-shadow:0 6px 16px #0006;align-self:flex-start}}
.info{{display:flex;flex-direction:column;min-width:0}}
h2{{font-family:Baskerville,Georgia,serif;font-size:1.45rem;line-height:1.15;margin:.1em 0 .2em}}
.sub{{margin:0;font-style:italic;color:#7a6a44}}
.meta{{margin:.7em 0 0;font:600 .78rem system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#8a7b5b}}
.blurb{{font-size:.98rem;line-height:1.5;margin:.7em 0 1em}}
.read{{margin-top:auto;font:700 .95rem system-ui,sans-serif;color:#a8650b}}
.soon{{border:2px dashed #ffffff33;border-radius:14px;display:flex;align-items:center;justify-content:center;min-height:200px;color:var(--muted);font-style:italic}}
footer{{text-align:center;padding:0 20px 44px;color:var(--muted);font:.85rem system-ui,sans-serif}}
@media (max-width:520px){{.card{{flex-direction:column}}.card img{{width:60%;max-width:none;align-self:center}}}}
</style>
</head>
<body>
<header>
  <div class="kicker">The Library for All</div>
  <h1>Project B</h1>
  <p>A growing shelf of illustrated adventures for curious minds. Big hearts, wild places and small brave choices, each one only a page turn away. Every story carries a little courage you can take with you. Pick a book, turn the page, and find one that feels like it was written for you.</p>
</header>
<main>
  <section class="shelf" aria-label="Books">
{cards}
    <div class="soon">More books coming soon…</div>
  </section>
</main>
<footer>Open a book, then use ← → keys or swipe to turn the pages.</footer>
</body>
</html>
'''
(ROOT / "index.html").write_text(page)
print(f"built index.html with {len(books)} book(s)")
