# Project B rules (illustrated novels)

Read first each session: `factory/STATE.md` (log and lessons), `factory/RUNBOOK.md` (commands, exact image prompt recipe, QC, release), `SPEC.md` (plan of record), and the memory index. One book at a time. Qwen writes prose, Claude judges quality; images are local (Draw Things).

## Character consistency QA (mandatory before any release)
The user found that in released or in-progress books characters' clothes and shoe colors were not consistent, two characters looked almost identical, and hair style changed within the same scene. Check this on every book, every page:
1. **Design for it (in the bible and `style.json` `looks`):** give every character a unique silhouette: distinct hair style/length/color, a distinct main clothing color, one signature accessory, and explicit footwear (shoe type and color). No two characters may share both hair style and top color. Put those exact words in the `looks` descriptor and in every `IMAGE:` line that names the character.
2. **Look at every page at readable size, not just thumbnails:** view all contact sheets (25 per sheet) and zoom (Read the `images/pNNN.png` or a small `reroll_sheet.py` sheet) on any page with two or more characters or any doubt.
3. **Per-character checklist, per page:** hair style and length; top color and type; bottom; shoes and their color; accessories (hat, ribbon, bag, glasses); skin tone; approximate age and height relative to the others.
4. **Within a scene** (a run of consecutive pages in one place) hair, clothes and shoes must not change. Two characters must be told apart at a glance (no lookalike pairs); check that the descriptor regexes did not fire on the wrong character (case-sensitive names; generic words like "grey" or "girl" can add the wrong descriptor).
5. **Fix:** tighten the `looks` regexes and descriptors, rewrite the page's `IMAGE:` line with the character's name and clothes, then `gen_images.py <slug> reroll N ...`, and re-check with `reroll_sheet.py`. Up to 3 rounds; change composition or seed if it keeps failing. Record what worked in `STATE.md`.
6. Also check: no stray animals (dogs), no fake lettering, no white borders, right setting (location words in the `IMAGE:` line), covers match the interior style and characters.

## Other standing quality rules
See `~/.claude/projects/-Users-Maxi-Code-Project-B/memory/book-quality-standards.md` and SPEC.md section 6: consistent story line, age-appropriate, real proofreading (full read-through by Claude), vocabulary and learning, engagement and pacing, keep the current image and cover style, culture accuracy, no culture labels in titles or blurbs.

## Public copy
Show new site-level wording (home page intro, taglines) to the user before pushing. Book releases (blurbs, SPEC status) do not need approval, see below.

## Releasing books needs no approval, but ask before starting the next one
Finished books (blurb, cover text, SPEC status row, shelf order, GitHub release) are released without asking the user (user, 2026-09-26): release, verify Pages 200, SendUserFile the front cover, update STATE.md. **Do NOT start the next book (no queue entry, no production) until the user confirms** (user, 2026-09-30; this replaces the old "do not pause between books"). Only site-level copy changes outside a book release (home page intro, taglines) need the user's OK first.

## Release date (user, 2026-10-09)
Every book carries a `released` date (YYYY-MM-DD in its `book.json`, mirrored in `factory/books/<slug>/meta.json`) set to the day it is released for the FIRST time (today's date when we complete and release it). `release.py` keeps the original date on re-releases and fixes. The home page shows "Released <date>" on each card and sorts newest release first, so the oldest books sit at the bottom and a new book goes to the top. One shelf only (no separate High School section). The first 17 books got staggered dates between 2026-09-10 and 2026-10-09 (set by the user's request, not real release days).

## Layout (user, 2026-09-30)
Everything for this project lives under `Project-B/`: published books as `<slug>/` folders, and the production tooling in `factory/` (scripts, RUNBOOK/STATE/WISHLIST tracked; `factory/books/`, `dist/`, `tools/`, `logs/`, `legacy/` are git-ignored work data). Create a book's `Project-B/<slug>/source/` (bible, outline) when the book is prepared; `factory/release.py` fills in the rest.

## Image tooling notes
`draw-things-cli` is pinned to v26.0910.1 (copy in `factory/tools/dt-cli-26.0910.1/`, installed at /opt/homebrew/bin). v26.0928.0 crashes with a Metal shader error on this Mac (macOS 27.0.1). Do not `brew install/upgrade draw-things-cli` until a fixed release is verified.
