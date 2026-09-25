#!/usr/bin/env python3
"""Render one small spot illustration per page (+ covers art) with draw-things-cli (local, z_image_turbo)."""
import json, os, pathlib, subprocess, sys, re

ROOT = pathlib.Path(__file__).parent
IMG = ROOT / "images"; IMG.mkdir(exist_ok=True)
ENV = dict(os.environ, DRAWTHINGS_MODELS_DIR="/Volumes/SSD-4T-LR/AI/Models")
STYLE = ("Soft watercolor and ink children's book spot illustration, warm coastal colors, whimsical, gentle light, "
         "loose brushwork, plain cream paper background with soft vignette edges, no text, no letters: ")
LOOKS = [  # keep characters consistent across pages
    (r"\bJuno\b|\bgirl\b", "the girl has curly dark-brown hair in two puffs, freckles and a bright yellow raincoat"),
    (r"\bTeo\b|\bboy\b", "the boy has round glasses, messy black hair, a green cap and a canvas tool belt"),
    (r"\bOzzie\b|\bgrandpa\b|\bold man\b|\bman\b", "the old man is tall with a bushy white beard, blue knitted hat and a driftwood cane"),
    (r"\bBiscuit\b|\bcat\b", "the cat is fat and orange with a chewed left ear"),
    (r"\bBarnacle\b|\bhermit crab\b|\bcrab\b", "the hermit crab lives in a chipped blue teapot"),
]

def render(prompt, out, w=768, h=768, seed=1):
    if out.exists(): return
    cmd = ["draw-things-cli", "generate", "--model", "z_image_turbo_1.0_q8p.ckpt", "--no-download-missing",
           "--disable-preview", "--width", str(w), "--height", str(h), "--seed", str(seed),
           "--prompt", prompt, "--output", str(out)]
    for attempt in range(2):
        r = subprocess.run(cmd, env=ENV, capture_output=True, text=True)
        if out.exists(): print("ok", out.name, flush=True); return
        print("retry", out.name, r.stderr[-200:], flush=True)

def page_prompt(p):
    p = re.sub(r'(?i)\b(sign|banner|label|note|letter|book|page)s?\b[^,.;]*?\b(reading|that says|saying|which says|labeled)\b[^,.;]*', r'\1', p)
    p = re.sub(r'["“][^"”]*["”]', '', p)
    extra = [d for pat, d in LOOKS if re.search(pat, p, re.I)]
    return STYLE + p + (". " + "; ".join(extra) if extra else "")

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "pages"
    if what == "covers":
        c = json.loads((ROOT / "covers.json").read_text())
        for k, v in c.items():
            render(v["prompt"], IMG / f"cover_{k}.png", 1024, 1536, v.get("seed", 11))
    else:
        n = 0
        for f in sorted((ROOT / "chapters").glob("ch*.json")):
            ch = json.loads(f.read_text())
            for p in ch["pages"]:
                n += 1
                render(page_prompt(p["image"]), IMG / f"p{n:03d}.png", 768, 768, 1000 + n)
