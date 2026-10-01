"""Shared helpers for the book factory."""
import json, pathlib, re, urllib.request

FACTORY = pathlib.Path(__file__).resolve().parent.parent
MODELS_DIR = "/Users/Maxi/Code/Models"

def book_dir(slug): return FACTORY / "books" / slug
def load_json(p): return json.loads(pathlib.Path(p).read_text())

def ollama(model, system, prompt, temperature=0.8, num_ctx=16384, num_predict=6000, images=None):
    msg = dict(role="user", content=prompt)
    if images: msg["images"] = images
    body = json.dumps(dict(model=model, stream=True, think=False,
        options=dict(temperature=temperature, num_ctx=num_ctx, num_predict=num_predict),
        messages=[dict(role="system", content=system), msg])).encode()
    req = urllib.request.Request("http://localhost:11434/api/chat", body, {"Content-Type": "application/json"})
    out = []
    with urllib.request.urlopen(req, timeout=3600) as r:
        for line in r:
            d = json.loads(line)
            out.append(d.get("message", {}).get("content", ""))
            if d.get("done"): break
    return "".join(out)

def wc(s): return len(s.split())

def parse_chapter(text):
    """=== PAGE n === / body / IMAGE: line  ->  list of dict(text, image)"""
    pages = []
    for blk in re.split(r"=== PAGE \d+ ===", text)[1:]:
        m = re.search(r"^IMAGE:\s*(.+)$", blk, re.M | re.S)
        img = m.group(1).strip() if m else ""
        body = blk[:m.start()] if m else blk
        pages.append(dict(text=body.strip(), image=" ".join(img.split())))
    return pages
