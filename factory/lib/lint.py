"""Prose lint: catches the clichés and tics local LLMs love. Returns a list of findings (strings)."""
import re

# regex, label
BANNED = [
    (r"\b(heart|hearts)\b[^.]{0,20}\b(hammer\w*|pound\w*|rac(?:e|ed|ing)|skipp?\w*|leap\w*|thud\w*|drumm\w*|lurch\w*|sank|sink\w*)\b", "heart-verb cliché"),
    (r"\b(held|holding|hold|hoding)\b[^.]{0,12}\b(her|his|their|my|a)\b[^.]{0,6}\bbreath\b", "held breath"),
    (r"breath (?:she|he|they|i) (?:didn.t|did not) (?:know|realize)", "breath she didn't know"),
    (r"\bstone\b[^.]{0,15}\b(in|inside|dropped|settled|sank)\b[^.]{0,15}\b(stomach|chest|throat|gut)\b", "stone-in-stomach"),
    (r"\b(shiver|chill)s?\b[^.]{0,12}\b(down|up|ran|crept)\b[^.]{0,12}\bspine\b", "shiver down spine"),
    (r"smile that (?:didn.t|did not) (?:quite )?reach", "smile that didn't reach"),
    (r"silence (?:was|felt) (?:deafening|heavy|thick)", "deafening/heavy silence"),
    (r"for the first time in (?:days|weeks|months|years|a long time|ages)", "for the first time in..."),
    (r"\bsomething (?:shifted|stirred|clicked|changed) (?:inside|in)\b", "something shifted"),
    (r"\bgoing to be (?:okay|fine|alright)\b", "going-to-be-okay filler"),
    (r"\bmix of\b", "mix of"),
    (r"\ba (?:wave|flood|surge|rush) of (?:relief|emotion|panic|guilt|warmth|sadness)\b", "wave of emotion"),
    (r"\b(?:eyes|gaze) (?:widened|went wide|sparkled|twinkled|glinted|shone)\b", "eye cliché"),
    (r"\bthe weight of\b", "the weight of"),
    (r"\bbarely above a whisper\b|\bvoice (?:barely|no) (?:more than|above) a whisper\b", "barely a whisper"),
    (r"\bcouldn.t help but\b", "couldn't help but"),
    (r"\bmagic(?:al)? (?:hung|filled|crackled) (?:in|the) air\b|\bair (?:crackled|hummed|thrummed) with\b", "air crackled"),
    (r"\bgrin(?:ned)?\b[^.]{0,10}\bear to ear\b", "ear-to-ear grin"),
    (r"\bthe kind of\b[^.]{0,40}\bthat\b", "'the kind of X that' (count-limited)"),
    (r"\bmy dear\b|\bmy child\b", "fairy-godmother speech"),
    (r"—", "em dash"),
]
LIMITS = {  # label -> max allowed per chapter (default 0)
    "'the kind of X that' (count-limited)": 2,
    "em dash": 4,
}
NOT_X_BUT_Y = re.compile(r"\b(?:It|That|This|He|She|They) (?:wasn.t|was not|weren.t|isn.t|didn.t) [^.?!]{2,60}[.,;] (?:It|That|This|He|She|They|It.s|That.s)\b", re.I)
SUDDENLY = re.compile(r"\bsuddenly\b", re.I)
SIMILE = re.compile(r"\b(?:like|as if|as though) (?:a|an|the|some|someone|something)\b [^.,;!?]{3,60}|\bas \w+ as (?:a|an|the) [^.,;!?]{2,30}", re.I)

def starter_runs(text):
    """Runs of 3+ consecutive sentences that begin with the same word (staccato 'It was. It was. It was.')"""
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    firsts = [re.sub(r"\W", "", s.split()[0]).lower() for s in sents]
    runs, i = 0, 0
    while i < len(firsts):
        j = i
        while j + 1 < len(firsts) and firsts[j + 1] == firsts[i] and firsts[i] not in ("", "i\"", ): j += 1
        if j - i >= 2: runs += 1
        i = j + 1
    return runs

def short_share(text):
    sents = [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    if not sents: return 0
    return sum(1 for s in sents if len(s.split()) <= 5) / len(sents)

def lint(text, extra_banned=(), used_similes=()):
    """Returns (findings, similes_in_text)."""
    f = []
    for rx, label in BANNED:
        hits = re.findall(rx, text, re.I)
        n = len(list(re.finditer(rx, text, re.I)))
        if n > LIMITS.get(label, 0): f.append(f"{label} x{n}")
    for phrase in extra_banned:
        n = len(re.findall(re.escape(phrase), text, re.I))
        if n: f.append(f"book-tic '{phrase}' x{n}")
    n = len(NOT_X_BUT_Y.findall(text))
    if n > 1: f.append(f"'It wasn't X. It was Y.' pattern x{n} (max 1 per chapter)")
    n = len(SUDDENLY.findall(text))
    if n > 1: f.append(f"'suddenly' x{n} (max 1)")
    n = starter_runs(re.sub(r'"[^"]*"', '', text))
    if n > 2: f.append(f"staccato runs (3+ sentences starting with the same word) x{n}; vary sentence openings and combine short sentences")
    sh = short_share(re.sub(r'"[^"]*"', '', text))
    if sh > 0.34: f.append(f"too many very short sentences ({sh:.0%} of narration are 5 words or fewer; combine some, aim under 30%)")
    sims = [" ".join(s.lower().split()) for s in SIMILE.findall(text)]
    for s in sims:
        key = re.sub(r"[^a-z ]", "", s)
        for u in used_similes:
            if key[:28] == re.sub(r"[^a-z ]", "", u)[:28] and len(key) > 12:
                f.append(f"repeated simile: '{s}'"); break
    return f, sims
