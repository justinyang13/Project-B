# Project B factory RUNBOOK

How to produce and release one illustrated novel, with the exact commands and prompt recipe. Companion files: `SPEC.md` (plan of record, public, in the Project-B repo), `STATE.md` (dated log and lessons, private), `WISHLIST.md`, `~/.claude/local-ai-registry.md` (local tools and models). Rule: ONE book at a time; Claude judges quality, Qwen writes prose, local tools draw.

All commands run from `/Users/Maxi/Code/Project-B/factory`. `<slug>` = folder name under `books/`.

## 0. Environment
- Text: Ollama `qwen3.8:27b` at http://localhost:11434 (HTTP API, no wrappers). Coder model `qwen3-coder:30b`.
- Images: `draw-things-cli` with `z_image_turbo_1.0_q8p.ckpt`, `DRAWTHINGS_MODELS_DIR=/Users/Maxi/Code/Models` (SSD must be mounted). Never the Draw Things app, never cloud generators.
- One heavy model at a time (64 GB Mac). Text and page images run in parallel because Qwen is light enough; covers and rerolls run after, alone.
- Release target: public repo `justinyang13/Project-B` cloned at `~/Code/Project-B`, Pages site https://justinyang13.github.io/Project-B/.

## 1. Files per book (`books/<slug>/`)
| File | What |
|---|---|
| `bible.md` | premise, voice + sample, cast with fixed looks, cultural notes (web-verified), vocabulary/learning, motifs, lesson, things to avoid |
| `outline.md` | `# PART`, `## N. Title`, `Synopsis:`, `Header:` (tally line), 5 numbered page beats, x20 chapters. Parsed by `python3 lib/outline.py books/<slug>` into `outline.json` |
| `config.json` | min/max words (130/260), `first_allowed` (term -> first chapter it may appear), `extra_banned` phrases, `present_tense` |
| `style.json` | `seed_base`, `style` prefix, `suffix`, `looks` (regex -> character description), `covers` (name -> prompt, seed) |
| `meta.json` | title, subtitle, blurb, cover text/colors (`cover` block) |
| `src/ch01.txt` | gold chapter written by Claude: `=== PAGE n ===`, prose, `IMAGE:` line per page; ingest with `python3 ingest.py <slug> 1` |
| `chapters/chNN.json` | generated chapters (pages: text + image prompt) |
| `images/` | `pNNN.png` (768x768), `cover_*.png`, `cover_*_final.png` |
| `READY` | written by the pipeline when text, images, covers and sheets are done |

## 2. Prepare a book (Claude)
1. Web-research culture/topic; write `bible.md` with verified notes only (never invent foreign words).
2. Write `outline.md` (20 chapters x 5 beats). Check: `python3 lib/outline.py books/<slug>` -> "20 chapters OK".
3. Write `config.json`, `style.json`, `meta.json`, and the gold `src/ch01.txt`; run `python3 ingest.py <slug> 1`.
4. Put the slug in `queue.txt` (only the current book).

## 3. Run the pipeline
`queue.sh` (loop) picks the slug in `queue.txt` and runs `run_book.sh <slug>`:
1. `write_book.py <slug> 2 20` : per chapter draft -> lint -> edit-revise loop with Qwen (log `write_all.log`).
2. `run_images.sh <slug>` : `gen_images.py <slug> pages` renders each page as its chapter appears (log `images.log`).
3. `gen_images.py <slug> covers front front2 back`
4. `contact_sheet.py <slug> 25` (Chrome headless HTML -> PNG sheets in `sheets/`)
5. `readthrough.py <slug>` (Qwen review -> `review.md`; mostly false positives, do not trust)
6. writes `READY`.

Keep-alive: `nohup ./watchdog.sh &` (2-minute loop, restarts stalled queue/writer/images, appends to `watchdog.events`). Watch with Monitor on `tail -F watchdog.events | grep -E "STALL|RESTARTED|READY|IDLE"` (expires every 30 min: re-arm). If the watchdog fails to restart `queue.sh` (pgrep matches its own command line), start `nohup ./queue.sh >> queue.log 2>&1 &` by hand. Do NOT write `until ! pgrep -f ...` wait loops in Bash: they match themselves and never exit; count `ok` lines in the log or use the READY file instead.

## 4. The image prompt recipe (exact)
`gen_images.py` `page_prompt()` builds each page prompt as:

`style` + scene text + ". " + character descriptions + ". " + `suffix`

- `style` (from `style.json`), example (Lin): "Warm glowing storybook illustration in gouache and colored pencil, cozy detailed night scenes with warm lantern light against deep blue evening, soft rising steam, lively crowds, expressive kind faces, rich but gentle colors, no text, no writing, no letters, no signs, all stall boards and banners are blank: "
- scene = the page's `IMAGE:` line. Text inside quotation marks is stripped, and phrases like "a sign that says ..." are cut.
- character descriptions: every `looks` regex that matches the scene appends its description (joined with "; "). So put the character's name AND clothing in every IMAGE line ("Lin, an eleven-year-old girl with a chin-length black bob ... in a dark green padded jacket and a red-and-white checked apron").
- `suffix`: "Spot illustration with soft vignette edges, expressive faces, no captions, no readable text."
- Render: `draw-things-cli generate --model z_image_turbo_1.0_q8p.ckpt --no-download-missing --disable-preview --width 768 --height 768 --seed <seed> --prompt "<prompt>" --output images/pNNN.png` (steps left at the model default; retries once).
- Seed = `seed_base` + page number + 1000 x number of rerolls (tracked in `rerolls.json`).
- Covers: 1024x1536, prompt and seed hand-written in `style.json` `covers`; then `python3 make_covers.py <slug> <front_art> <back_art>` composes type over the art with headless Chrome (settings in `meta.json` `cover`).
- Juno Vale (book 0, pre-factory) used a soft watercolor-and-ink style; exact cover prompts are in `Project-B/juno-vale-and-the-tide-that-forgot/source/covers.json`. All later books use gouache and colored pencil.

### Reference styles (user's favorites, 2026-09-25): Mo first, Rue second
The user loves the illustrations of `mo-and-the-mountain-that-walks` (ch 1 "The Morning the Mountain Turned") and `rue-and-the-troll-under-bridgewater-bridge`. For new books start from one of these two `style.json` files (copy `style`, `suffix`, cover prompt structure) and change only the palette/setting words and the `looks`. Model: z_image_turbo, 768x768 pages, 1024x1536 covers, default steps.

| Keyword in `style` | Effect (what we observed) | Look |
|---|---|---|
| "gouache" (both) | matte, opaque, flat-ish color like a picture-book original; the base of the whole shelf | both |
| "soft pencil" | thin sketchy pencil outlines on figures and trees, light and airy | Mo |
| "colored pencil detail" | fine hatching, extra detail in faces, cloth, grass | Rue |
| "soft textured brushwork" | visible thick brush strokes, almost oil-paint impasto, swirling sky/leaves/stone (the "painted" feel) | Rue |
| "sweeping painterly landscapes" + "small figures against huge quiet scenery" | wide airy scenes, characters small, lots of calm space | Mo |
| "sage green pines, dusty ochre and apricot sunrise light" | muted natural palette, sunrise haze | Mo |
| "honey-amber lamplight, moss green, plum and slate-blue shadows" | warm glow with colored (purple/blue) shadows, dusk mood | Rue |
| "rounded friendly shapes", "warm fairy-tale village charm", "like a beloved picture-book classic" | cute proportions, cozy cottage/village look, classic children's-book feel | Rue |
| "gentle whimsical detail" | small charming extras (mushrooms, cottages, flowers) | Mo |
| "no text, no writing, no letters, no signs" | suppresses fake lettering (but see lessons below) | both |

Rule of thumb: the *medium* words (gouache, pencil, brushwork) set the painting technique, the *palette* words set the mood, and the *composition* words (small figures / rounded friendly shapes) set scale and character cuteness. Change one group at a time when tuning. Do not add artist names; they were never tested and are not needed. Keep the same `style` prefix for every page and cover of a book (character `looks` carry the identity).

Image lessons: a "no sign" phrase primes signs, so for sign-heavy scenes say the stall is a bare wooden counter under a plain cream cloth awning and append "All shop signs, banners and hanging boards are smooth plain solid-color cloth."; never write "for a title" in a cover prompt (it paints fake title text): say "the top fifth is an empty smooth sky"; a nickname that is an animal makes the model draw the animal (use the real name); give each character distinct clothing colors; state skin tone and hair on covers; fantasy creatures work best via a real-animal analogy.

## 5. QC after READY (Claude)
1. Full read-through of the whole book (dump: chapters -> one text file; read all). Check tense slips, stray Header lines on pages 2-5, name and timeline consistency, British/American mix, overused motif phrases, invented foreign words, culture facts against the bible, no culture label words in text where forbidden. Patch with a Python replace script that asserts each string exists.
2. Contact sheets: view every `sheets/sheetN.png`. List pages with drifting characters, fake lettering, dogs/stray animals, white borders, odd anatomy, wrong setting. **Character consistency QA is mandatory** (see `/Users/Maxi/Code/Project-B/CLAUDE.md`): per character and per page check hair style/length, clothing colors, shoe color, accessories; no lookalike pairs; no changes within a scene; zoom in on multi-character pages.
3. Fix images: edit the page's `image` string in `chapters/chNN.json`, then `python3 gen_images.py <slug> reroll N N ...` (new seed each time); review with `python3 reroll_sheet.py <slug> N N ...` (sheet of just those pages). Repeat up to 3 rounds.
4. Covers: pick front/back art; `python3 make_covers.py <slug> <front> <back>`; view `images/cover_front_final.png` and `cover_back_final.png`. Make new candidates by adding entries to `style.json` `covers` and `python3 gen_images.py <slug> covers <name>`.

## 6. Build and release
0. Release date: `release.py` stamps `released` = today on the FIRST release only (kept on re-releases); the home page sorts newest first. See Project-B/CLAUDE.md "Release date".
1. `python3 build_html.py <slug>` (reader) then `python3 release.py <slug>` (copies into `~/Code/Project-B/<slug>/`, writes `book.json`, builds zip `dist/<slug>.zip`).
2. In `~/Code/Project-B`: append the slug to `ORDER` in `build_index.py` (new books go at the bottom), add a row to `SPEC.md` section 8, `python3 build_index.py`.
3. `git add -A && git commit && git push`; then `gh release create <slug>-v1.0 ~/Code/Project-B/factory/dist/<slug>.zip --repo justinyang13/Project-B --latest=false --title "<Title> v1.0" --notes "..."`.
4. Wait for the Pages URL `https://justinyang13.github.io/Project-B/<slug>/` to return 200.
5. SendUserFile the front cover with the link and a short summary; append a dated entry and lessons to `STATE.md`.
6. Public-site wording changes (home page intro, titles, blurbs) are shown to the user BEFORE pushing. Library-level releases (`library-vX.Y`) are cut only when the shelf changes.

## 7. Troubleshooting
- Stalled text: check `write_all.log`, `ollama ps`; restart via watchdog or `pkill -f write_book.py` and rerun `./run_book.sh <slug>` (it resumes missing chapters).
- Stalled images: check `images.log` for "retry"; SSD mounted? `pkill -f draw-things-cli` then rerun `python3 gen_images.py <slug> pages`.
- Qwen slips into present tense or invents foreign words: rewrite the chapter through Qwen with a targeted instruction, then re-read (see the Lin and Mei notes in STATE.md).
- Context lost: re-read `STATE.md`, this file, the book's `bible.md`, and the memory index.
