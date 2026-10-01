#!/usr/bin/env python3
"""Local illustrations with draw-things-cli (z_image_turbo).
usage: gen_images.py <slug> pages            render every missing page image
       gen_images.py <slug> reroll N [N..]   delete + re-render pages with a new seed (tracked in rerolls.json)
       gen_images.py <slug> covers [name..]  render cover art candidates from style.json 'covers' (name -> prompt,seed)
books/<slug>/style.json: {style, looks:[[regex,desc]], seed_base, covers:{name:{prompt,seed,w,h}}}"""
import json, os, pathlib, re, subprocess, sys
from lib.common import *

slug, what = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "pages")
B = book_dir(slug); IMG = B / "images"; IMG.mkdir(exist_ok=True)
ST = load_json(B / "style.json")
ENV = dict(os.environ, DRAWTHINGS_MODELS_DIR=MODELS_DIR)
MODEL = ST.get("model", "z_image_turbo_1.0_q8p.ckpt")
RR = B / "rerolls.json"
rerolls = load_json(RR) if RR.exists() else {}

def render(prompt, out, w=768, h=768, seed=1, steps=None):
    if out.exists(): return True
    cmd = ["draw-things-cli", "generate", "--model", MODEL, "--no-download-missing", "--disable-preview",
           "--width", str(w), "--height", str(h), "--seed", str(seed), "--prompt", prompt, "--output", str(out)]
    if steps: cmd += ["--steps", str(steps)]
    for _ in range(2):
        r = subprocess.run(cmd, env=ENV, capture_output=True, text=True)
        if out.exists(): print("ok", out.name, flush=True); return True
        print("retry", out.name, r.stderr[-200:], flush=True)
    return False

def page_prompt(p, text=""):
    text = re.sub(r"^\s*\*[^\n]*\*\s*", "", text or "")  # ignore the italic chapter header line
    p = re.sub(r'["“][^"”]*["”]', '', p)
    p = re.sub(r'(?i)\b(sign|banner|label|note|letter|book|page|clipboard|list|card|poster)s?\b[^,.;]*?\b(reading|that says|saying|which says|labeled|marked|titled)\b[^,.;]*', r'\1', p)
    extra = []
    for look in ST["looks"]:
        pat, d = look[0], look[1]
        # third element True = main cast: also add the descriptor when the PAGE TEXT names the character (keeps looks consistent on pages whose IMAGE line says just "a girl")
        if (re.search(pat, p, re.I) or (len(look) > 2 and look[2] and text and re.search(pat, text))) and d not in extra: extra.append(d)
    return ST["style"] + p + (". " + "; ".join(extra) if extra else "") + (". " + ST["suffix"] if ST.get("suffix") else "")

def all_pages():
    for f in sorted((B / "chapters").glob("ch*.json")):
        c = int(re.search(r"ch(\d+)", f.name)[1])
        for i, p in enumerate(load_json(f)["pages"]):
            yield (c - 1) * 5 + i + 1, p

def seed_for(n): return ST.get("seed_base", 1000) + n + 1000 * rerolls.get(str(n), 0)

if what == "pages":
    for n, p in all_pages():
        render(page_prompt(p["image"], p.get("text", "")), IMG / f"p{n:03d}.png", 768, 768, seed_for(n))
elif what == "reroll":
    want = {int(x) for x in sys.argv[3:]}
    for n, p in all_pages():
        if n in want:
            rerolls[str(n)] = rerolls.get(str(n), 0) + 1; RR.write_text(json.dumps(rerolls))
            (IMG / f"p{n:03d}.png").unlink(missing_ok=True)
            render(page_prompt(p["image"], p.get("text", "")), IMG / f"p{n:03d}.png", 768, 768, seed_for(n))
elif what == "covers":
    names = sys.argv[3:] or list(ST["covers"])
    for k in names:
        v = ST["covers"][k]
        render(v["prompt"], IMG / f"cover_{k}.png", v.get("w", 1024), v.get("h", 1536), v.get("seed", 11))
