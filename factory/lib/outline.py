"""Parse books/<slug>/outline.md into outline.json.
Format:
# PART ONE: TITLE
## 1. Chapter Title
Synopsis: one or two sentences.
Header: (optional) exact line to print at the top of page 1 (e.g. T-MINUS 31:30 or an italic epigraph); added by the script, never by the model.
1. page-1 beat
2. ...
5. page-5 beat
"""
import json, re, sys, pathlib

def parse(md):
    chapters, part, cur = [], "", None
    for line in md.splitlines():
        line = line.rstrip()
        if line.startswith("# "): part = line[2:].strip()
        elif m := re.match(r"## (\d+)\. (.+)", line):
            cur = dict(n=int(m[1]), title=m[2].strip(), part=part, synopsis="", beats=[]); chapters.append(cur)
        elif line.startswith("Synopsis:") and cur: cur["synopsis"] = line[9:].strip()
        elif line.startswith("Header:") and cur: cur["header"] = line[7:].strip()
        elif (m := re.match(r"([1-5])\. (.+)", line)) and cur: cur["beats"].append(m[2].strip())
    for c in chapters:
        assert len(c["beats"]) == 5, f"chapter {c['n']} has {len(c['beats'])} beats"
        assert c["synopsis"], f"chapter {c['n']} lacks synopsis"
    assert [c["n"] for c in chapters] == list(range(1, len(chapters) + 1))
    return dict(chapters=chapters)

if __name__ == "__main__":
    p = pathlib.Path(sys.argv[1])
    out = parse((p / "outline.md").read_text())
    (p / "outline.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(len(out["chapters"]), "chapters OK")
