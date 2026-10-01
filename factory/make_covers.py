#!/usr/bin/env python3
"""Compose cover typography over art with headless Chrome.
usage: make_covers.py <slug> [front_art=front] [back_art=back]
books/<slug>/meta.json 'cover': {kicker, title_lines:[..], subtitle, tagline, foot_left, foot_right, blurb_hook, blurb:[paragraphs],
   font, title_color, accent, text, shade_rgb, title_size, panel_rgb}  -> images/cover_front_final.png, cover_back_final.png"""
import html, pathlib, subprocess, sys
from lib.common import *
slug = sys.argv[1]; B = book_dir(slug); C = load_json(B / "meta.json")["cover"]
fa = sys.argv[2] if len(sys.argv) > 2 else "front"; ba = sys.argv[3] if len(sys.argv) > 3 else "back"
E = html.escape
font = C.get("font", "Baskerville,Georgia,serif"); tc = C.get("title_color", "#ffd35c"); ac = C.get("accent", "#f3c76a")
tx = C.get("text", "#fff3cf"); sh = C.get("shade_rgb", "8,20,40"); tsz = C.get("title_size", 150)
shadow = C.get("title_shadow", "0 3px 0 rgba(0,0,0,.35),0 6px 0 rgba(0,0,0,.25),0 10px 26px rgba(0,0,0,.7)")
lines = "<br>".join(E(x) for x in C["title_lines"])
front = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:1024px;height:1536px;overflow:hidden}}
.c{{position:relative;width:1024px;height:1536px;background:url(file://{B}/images/cover_{fa}.png) center/cover;font-family:{font};text-align:center;color:{tx}}}
.c::before{{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,rgba({sh},.75) 0,rgba({sh},.4) 22%,rgba({sh},0) 38%,rgba({sh},0) 82%,rgba({sh},.6) 100%)}}
.t{{position:absolute;top:64px;left:60px;right:60px}}
.kick{{font:700 26px/1 {font};letter-spacing:.36em;text-transform:uppercase;color:{ac};margin-bottom:20px;text-shadow:0 2px 8px #0009}}
.name{{font-size:{tsz}px;font-weight:800;line-height:.95;color:{tc};text-shadow:{shadow};text-transform:uppercase}}
.sub{{font-style:italic;font-size:58px;margin-top:16px;text-shadow:0 3px 14px rgba(0,0,0,.8)}}
.b{{position:absolute;bottom:46px;left:0;right:0;font:700 27px/1.2 {font};letter-spacing:.16em;text-transform:uppercase;text-shadow:0 2px 10px #000}}
.b small{{display:block;font-size:22px;letter-spacing:.35em;color:{tx};margin-top:10px}}
</style></head><body><div class="c"><div class="t"><div class="kick">{E(C['kicker'])}</div><div class="name">{lines}</div><div class="sub">{E(C.get('subtitle',''))}</div></div>
<div class="b">{E(C['tagline'])}<small>A novel for ages 10–12</small></div></div></body></html>'''
paras = "".join(f"<p>{E(p)}</p>" for p in C["blurb"])
back = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:1024px;height:1536px;overflow:hidden}}
.c{{position:relative;width:1024px;height:1536px;background:url(file://{B}/images/cover_{ba}.png) center/cover;font-family:{font};color:{tx}}}
.c::before{{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,rgba({sh},.5),rgba({sh},.3) 40%,rgba({sh},.65))}}
.panel{{position:absolute;left:90px;right:90px;top:150px;padding:52px 56px 44px;background:rgba({C.get('panel_rgb',sh)},.78);border:2px solid {ac};border-radius:18px;box-shadow:0 10px 40px rgba(0,0,0,.5)}}
.hook{{font-size:44px;font-style:italic;font-weight:700;line-height:1.2;text-align:center;color:{ac};margin:0 0 28px}}
p{{font-size:29px;line-height:1.48;margin:0 0 18px}}
.tag{{font-size:33px;font-weight:800;text-align:center;margin-top:24px;color:#fff}}
.foot{{position:absolute;bottom:52px;left:90px;right:90px;display:flex;justify-content:space-between;font:700 22px/1.4 {font};letter-spacing:.2em;text-transform:uppercase;color:{ac};text-shadow:0 2px 8px #000}}
</style></head><body><div class="c"><div class="panel"><div class="hook">{C['blurb_hook']}</div>{paras}<div class="tag">{E(C['tagline_back'])}</div></div>
<div class="foot"><div>{C['foot_left']}</div><div>{C['foot_right']}</div></div></div></body></html>'''
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for name, doc in (("front", front), ("back", back)):
    hp = B / f"cover_{name}.html"; hp.write_text(doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files", "--hide-scrollbars",
                    "--window-size=1024,1536", f"--screenshot={B}/images/cover_{name}_final.png", f"file://{hp}"], capture_output=True)
    print("cover", name)
