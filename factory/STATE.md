# Novel series state (read this first after any context compaction)

## Job (started 2026-09-24, user said "Go")
Write 7 more illustrated middle-grade novels (ages 10-12), each 100 pages / 20 chapters (5 pages per chapter, ~200-260 words per page, ~27k words), one illustration per page + front/back cover. QUALITY BAR: **best-seller quality** for story, prose and illustrations. "Do not cut corners." Each book has its own voice, palette and main life lesson (dramatized, never preachy).
Run straight through; after EACH book: release to GitHub (Project-B repo, public, Pages on) so user can read on phone, then send a short update. User authorized this durably.
Use LOCAL AI per the user's global rule: Qwen (Ollama, direct API) drafts/revises prose; Draw Things CLI (z_image_turbo, models on /Users/Maxi/Code/Models) paints. Claude = orchestrator: outlines, style guides, QC, read-through, continuity patches, releases.

## Lineup (user-approved)
1. The Day That Wouldn't End — funny time loop; Max, 11. Lesson: happiness is a choice, not a result.
2. Zia and the Runaway Space Station — sci-fi; Zia, 12. Lesson: asking for help is strength; teamwork ("kids can't be engineers").
3. The Mapmaker's Apprentice — historical-style quest; Tam, 11. Lesson: be better than yesterday; growth speed > where you start.
4. Pip and the Storm-Sparrows — animal fantasy; Pip, smallest sparrow. Lesson: never let anyone tell you that you can't; go get it.
5. Fifty-One Ways to Lose a Soccer Game — realistic sports comedy; Dani, 12. Lesson: confidence from within; a loss changes strategy, not your value.
6. Rue and the Troll Under Bridgewater Bridge — cozy fairy-tale fantasy; Rue, 10. Lesson: empathy, look past appearances, be kind to the left-out; forgiveness. (NO spooky/ghost stuff.)
7. The Garden at the Edge of the Concrete — magic garden; Sana, 11. Lesson: responsibility and patience; good things grow slowly; speaking up.

## Book 0 (done): Juno Vale and the Tide That Forgot — released v1.0 at https://github.com/justinyang13/Project-B , site https://justinyang13.github.io/Project-B/ . Local source: /Users/Maxi/Code/Project-B/factory/legacy/novel. Lessons learned: Qwen overshoots page length, invents plot in summaries, leaks future plot, repeats cliches ("stone in throat", "heart hammered", "Honestly!", "It wasn't X. It was Y.").

## Locations
- Factory (scripts + per-book work): /Users/Maxi/Code/Project-B/factory  (books/<slug>/...)
- Release repo: ~/Code/Project-B  (one folder per book, book.json, build_index.py regenerates index.html; Pages on main)
- Registry of local AI: ~/.claude/local-ai-registry.md (update with lessons)

## Progress log (append below)

- 2026-09-24: Series plan written as spec at ~/Code/Project-B/SPEC.md and committed locally (not pushed yet; goes out with the first book release). Update its status table as books ship.
- 2026-09-24: User set /autocompact 500K (client command). Factory scaffold built: lib/{common,lint,outline}.py, write_book.py, reader_template.html. Book 1 slug `the-day-that-wouldnt-end`: bible.md + config.json done; NEXT: outline.md (100 page beats; parse with `python3 lib/outline.py books/<slug>`), then bake-off on ch1 (qwen3.8:27b vs qwen3.5:35B via --model/--out), then generalize gen_images/build/release scripts.
- 2026-09-24 DECISION (bake-off ch1, both Qwens): Qwen prose = staccato, generic, edit pass just echoes the draft; qwen3.5:35B worse (one giant paragraph/page, timeline errors). For best-seller quality **Claude writes the final prose** per chapter into books/<slug>/src/chNN.txt (=== PAGE n === / prose / IMAGE: line), then `python3 ingest.py <slug>` -> chapters/*.json + lint. Qwen is still used for: continuity/lint review, illustration QC (vision), blurbs/brainstorm. Image style for book 1 chosen by bake-off: B (Quentin-Blake-ish ink+gouache). Tell user this in the first release update. write_book.py stays as optional drafting tool.
- Illustrations can render in the background (draw-things-cli) while Claude writes; keep Ollama unloaded then.
- 2026-09-25: Writer w/ exemplar + per-page polish loop (calibrated lint) works. Book 1 full run started: write_all.log; chapters land in books/the-day-that-wouldnt-end/chapters (ch01 = my gold). Image loop: ./run_images.sh <slug> (start once ch1-2 exist).
- 2026-09-25: **BOOK 1 RELEASED** (the-day-that-wouldnt-end): pushed to Project-B main (commit 6321470, includes SPEC.md), release tag the-day-that-wouldnt-end-v1.0 with zip. Live: https://justinyang13.github.io/Project-B/the-day-that-wouldnt-end/
## WORKFLOW THAT WORKS (use for books 2-7; user-approved: Qwen writes, Claude judges, conserve Claude tokens)
1. Claude writes books/<slug>/bible.md (voice + voice sample + cast + rules), outline.md (20 ch x 5 page beats + synopsis), config.json (min/max words 130/260, first_allowed leak terms, extra_banned tics), style.json (art style, looks regex->descriptor, covers), meta.json (title, blurb, cover text). `python3 lib/outline.py books/<slug>` -> outline.json.
2. Claude writes ONE gold chapter as src/ch01.txt (=== PAGE n === / prose / IMAGE:), `python3 ingest.py <slug> 1` -> chapters/ch01.json. write_book.py auto-uses src/ch01.txt as the exemplar in the system prompt.
3. `nohup python3 write_book.py <slug> 2 20 > write_all.log &` (Qwen3.8 drafts, per-page lint+polish loop, ~3-4 min/chapter, ~1h/book). Run `./run_images.sh <slug>` in parallel (background) once ch1 exists; ~30s/image.
4. Claude: view contact sheets (`contact_sheet.py <slug> 25`), reroll bad pages (`gen_images.py <slug> reroll N..`; improve descriptor in style.json first, e.g. keep 'kid in costume' etc.), covers: `gen_images.py <slug> covers front front2..`, pick, `make_covers.py <slug> <frontname> back`, view.
5. `python3 readthrough.py <slug>` (Qwen continuity review -> review.md; noisy, ~50% false positives: Claude judges each and patches chapters/*.json with small python replaces). Check for banned/spooky words, em dashes, timeline/count consistency.
6. `build_html.py <slug>`, `release.py <slug>`, update SPEC.md status row, git add/commit/push in ~/Code/Project-B, `gh release create <slug>-v1.0 dist/<slug>.zip --repo justinyang13/Project-B`. Check phone width in preview (port 8766 project-b). Then short update to user.
LESSONS: page-level rewrite loop works but Qwen stacks similes: lint thresholds calibrated on gold ch1 (short-sentence share 12-40%, max sentence 50 words, <=2 similes/page). Image prompt must name characters ("Dad", "Gus") so looks regex injects descriptors; Gus needed 'kid in costume' wording. Ollama + Draw Things can run concurrently on 64GB (was fine).
- 2026-09-25: AUTOMATION: queue.sh runs run_book.sh per book (text+images parallel, then covers, sheets, readthrough -> books/<slug>/READY). Claude prepares books ahead (bible, outline.md, config/style/meta json, src/ch01.txt), then QC/patch/build/release when READY. Book 2 queued.
- 2026-09-25: WATCHDOG: watchdog.sh (2-min loop; restarts stalls, logs to factory/watchdog.events). Claude: keep a Monitor on watchdog.events + always end a turn with ScheduleWakeup (<=20 min) so local AI is never left unattended. queue.txt = book order.
- 2026-09-25 USER DIRECTIVE: do NOT queue/prepare further books ahead; finish Book 2 (QC, release), learn lessons, THEN start Book 3. queue.txt = only the current book. Prepared (not queued): mapmakers-apprentice, pip-and-the-storm-sparrows (bible/outline/config/style/meta/ch1 done), fifty-one-ways (bible/style/config/meta done, no outline yet).
- LESSON (book 2): chapter device lines (T-MINUS/epigraph/Sky Report) must be deterministic: outline.md supports 'Header:' line per chapter (added by write_book.py, model told not to write it). Book 2 ch6+ lack headers -> patch at QC from the countdown schedule in outline. For books 3-5 convert 'Open with epigraph' beats into Header lines when starting them.
- LESSON (book 2 images): Qwen's IMAGE lines say 'robot'/'girl' not the name, so descriptors never attach -> looks regexes must include generic words (robot, barrel, the girl) and non-humanoid wording; check a contact sheet after ~25 images (early) and fix style.json, then reroll pages with generic-word mentions.
- LESSON (book 2): when a beat mentions a countdown/time header Qwen repeats it on EVERY page of that chapter (ch11,13,15,19,20); remove stray header lines from pages 2-5 at QC; Header: field in outline avoids it.
- 2026-09-25 08:4x: **BOOK 2 RELEASED** zia-and-the-runaway-space-station (commit pushed, release tag zia-and-the-runaway-space-station-v1.0). Live: https://justinyang13.github.io/Project-B/zia-and-the-runaway-space-station/  Book 2 took ~1h15 machine time (text 1h + images parallel) + ~40 min Claude QC. NEXT: apply lessons, start Book 3 (the-mapmakers-apprentice, prepped): convert epigraph beats to Header: lines, add generic-word looks regex, put in queue.txt.

## Book 3 released (2026-09-25)
- The Mapmaker's Apprentice v1.0 live: https://justinyang13.github.io/Project-B/the-mapmakers-apprentice/ ; release tag the-mapmakers-apprentice-v1.0; SPEC row 3 = Released.
- Lessons: (1) z-image adds stray dogs (esp. with a boy in a green coat); naming "no dogs" in the prompt PRIMES dogs. Fix: drop dog words, use "the only animals in the picture are those named in the scene" + per-character "no animals with him"; reroll. (2) Build a small reroll contact sheet (Chrome headless) after every reroll batch and check before release. (3) A 3rd/4th reroll is sometimes needed; a tiny background creature at the edge is acceptable.
- NEXT: Book 4 (Pip and the Storm-Sparrows): convert "Sky Report" beat-1 lines to Header: lines in outline.md, verify looks regexes, add slug to queue.txt.

## Book 4 released (2026-09-25)
- Pip and the Storm-Sparrows v1.0 live: https://justinyang13.github.io/Project-B/pip-and-the-storm-sparrows/ ; tag pip-and-the-storm-sparrows-v1.0; SPEC row 4 Released. Produced in ~1h (10:19 READY from 9:17 start) + ~25 min QC.
- Lessons: (1) Qwen sometimes writes a stray "*Sky Report:*" line at page 4/5 of a chapter — scan every page i>0 for the header string and strip. (2) Image prompts with color words for a character (chestnut, yellow-billed) make z-image draw other bird species; use the character NAME so the looks regex applies. (3) "rooftop" etc. introduces human objects in animal books. (4) Qwen review had ~40% real hits (fur/teeth on birds, whittling, blood, human-object similes).
- NEXT: Book 5 (Fifty-One Ways to Lose a Soccer Game): needs outline.md (with Header: Loss Log lines), gold chapter src/ch01.txt, bible check, then queue.

## Book 5 started (2026-09-25 ~10:50)
- Qwen-drafted outline was generic/wrong arc; Claude wrote outline.md + gold ch01 instead (lesson: outlines are Claude's job, prose is Qwen's). Queued fifty-one-ways-to-lose-a-soccer-game. Header numbers jump (1,4,7...,51) then Way to Win #1.

## Book 5 released (2026-09-25 ~12:45)
- Fifty-One Ways to Lose a Soccer Game v1.0 live: https://justinyang13.github.io/Project-B/fifty-one-ways-to-lose-a-soccer-game/ ; tag fifty-one-ways-to-lose-a-soccer-game-v1.0; SPEC row 5 Released.
- Lessons: (1) gen_images.py numbered pages by files on disk, so deleting chapters mid-run shifted pages; FIXED to number by chapter filename. Never delete chapters while images run; if you must, delete their images too. (2) First-person-present books: config present_tense=true makes page lint flag past tense (Qwen drifted in ch8-9). (3) Generic words in image prompts ("school bus", "whiteboard", "banner", "scoreboard") make z-image letter gibberish text; rewrite to "blank yellow minibus", "blank easel board", etc. (4) Negatives ("no people") prime people; a "red palette" style word pulled a red-shirted kid into every scene. (5) Qwen outline drafts are generic: Claude writes outlines + gold ch01. (6) Qwen review ~40% real hits; verify each against the text before patching (it invented "Coach Halloway").
- NEXT: Book 6 (Rue and the Troll Under Bridgewater Bridge): write bible check, outline.md with Header lines, gold ch01, style/meta/config, queue.

## Book 6 started (2026-09-25 ~13:10)
- Claude wrote bible, outline (almanac Header lines), gold ch01, style (gouache storybook), meta; queued rue-and-the-troll-under-bridgewater-bridge. QC reminders: scan pages i>0 for stray "From the Bridgewater Almanac" lines; check gibberish text on signs/banners/bridge; troll must stay gentle (not scary); Hobb name first allowed ch4.

## Book 6 released (2026-09-25)
- Rue and the Troll Under Bridgewater Bridge v1.0 live: https://justinyang13.github.io/Project-B/rue-and-the-troll-under-bridgewater-bridge/ ; tag rue-and-the-troll-under-bridgewater-bridge-v1.0; SPEC row 6 Released. Total time ~1h45 incl. Claude prep+QC (the pipeline is now smooth).
- Lessons: word "girl" in a prompt triggers Rue's look for every girl (name secondary girls explicitly, e.g. "Skye, a tall girl with..."); "mossy" made a stray moss-sprite; Qwen review file can ramble, ~30% useful; cover title needs size ~66 for 3-line long titles.
- NEXT: Book 7 (The Garden at the Edge of the Concrete): write bible, outline (Header lines), gold ch01, style/meta/config, queue.

## Book 7 started (2026-09-25)
- Claude wrote bible (first person past, Garden Log Header lines "Garden Log, Day N: ..."), outline, gold ch01, style (gouache + cut-paper collage, concrete grey vs vivid green), meta; queued the-garden-at-the-edge-of-the-concrete. QC reminders: stray Garden Log lines on pages 2-5; first person voice slips (Qwen may drift to third person); "girl" triggers Sana's look — name Nadia/others; tortoise Gherkin must be small (hat-sized); no scary; the final release completes the series.

## Book 7 released — SERIES COMPLETE (2026-09-25)
- The Garden at the Edge of the Concrete v1.0 live; all 7 books released; library home https://justinyang13.github.io/Project-B/ ; SPEC rows 1-7 Released. Watchdog/queue can be stopped.

## Library v1.0 released (2026-09-25)
- Home page reordered (ORDER list in Project-B/build_index.py; new books append at bottom) and intro rewritten with no AI mentions ("The Library for All"). Tagged/released library-v1.0 on justinyang13/Project-B. Project-B repo clean and pushed.

## EXPANSION: 5 more books (user request 2026-09-25) -> 13 total on the site
User picked (order = production order = site order after the 8): 
 8. Mo and the Mountain That Walks (slug mo-and-the-mountain-that-walks) — fantasy adventure, Mo 11, third past + Walk-Book Header lines. Lesson: home is the people, not the place; listening.
 9. The Robot Who Was Bad at Everything (robot-who-was-bad-at-everything) — sci-fi comedy. Lesson: joy comes from trying, not perfection.
10. Ash and the Dragon Who Feared Fire — fantasy. Lesson: courage = acting while afraid.
11. Tilly Quill and the Paper That Told the Truth — 1920s historical. Lesson: truth needs courage + kindness.
12. The River Cousins — survival adventure. Lesson: teamwork beats being right.
Rules: ONE book at a time (no queue-ahead); same workflow as books 3-7; add slug to build_index.py ORDER, SPEC.md rows, library-v1.1 release at the end (user OK'd releasing after each book, same as before). Lessons to apply: name secondary chars in image looks; avoid gibberish-text words (sign, banner...); no negative priming; Header lines deterministic.
## Book 8 started (2026-09-25): writing bible/outline/gold ch01 for Mo and the Mountain That Walks.
- 14:35 Book 8 queued; watchdog+queue started.

## Book 8 released (2026-09-25 ~16:30)
- Mo and the Mountain That Walks v1.0 live: https://justinyang13.github.io/Project-B/mo-and-the-mountain-that-walks/ ; tag mo-and-the-mountain-that-walks-v1.0; ORDER updated (position 9); SPEC row 8. Machine time ~1h (text 1h, images parallel) + QC.
- Lessons: (1) Qwen IMAGE lines say "a boy"/"a girl"/"two children" -> add \bboy\b / \bgirl\b to protagonist looks regexes (does not matter when other kids are named) — fixed Mo/Junie drift; use skin+hair colour first in descriptor. (2) Tor drifted between ram/lion/goat: descriptor now "giant moss-covered bison ... short straight upward-pointing horns" -> consistent. Pick a real-animal analogy for fantasy creatures. (3) New tool reroll_sheet.py <slug> N.. makes a contact sheet of just rerolled pages. (4) Watchdog may not restart queue.sh if pgrep matches own command line; start ./queue.sh manually with nohup. (5) ~24 rerolls of 100 pages were needed; ~15 min.
- NEXT: Book 9 The Robot Who Was Bad at Everything (slug robot-who-was-bad-at-everything).
## Book 9 started (2026-09-25): The Robot Who Was Bad at Everything. Robot narrator Percy (PERFECT-9), first person past, headers 'Percy's Error Log'. Bible/outline/gold ch1 in progress.
- 15:52 Book 9 queued.
- 15:58 User reordered shelf: Juno, Rue, Garden, Pip, Day, Mo, Zia, Fifty-One, Mapmaker (ORDER in build_index.py; new books append after).
- 16:00 library-v1.1 released (9 books, reordered).
- 16:03 CORRECTED shelf order: Juno, Pip, Rue, Day, Garden, Mo, Zia, Fifty-One, Mapmaker (library-v1.1 tag still has the previous order; cut v1.2 after last new book).
- 16:04 library-v1.2 released (corrected order, 9 books).

## STANDING QUALITY RULES (user, 2026-09-25) — see memory book-quality-standards.md
Claude = well-known children's author. Every book: consistent story line; age-appropriate; real proofreading pass; vocabulary/learning value (add Vocabulary/Learning section to each bible, check at QC); good pacing/engagement (no boring sag, no rushing); keep current image + cover style (user loves it). Show public site wording to user before pushing.
- WISHLIST.md created (Asian-culture books; reader tracking w/ SQLite). Not started.

## REVISED EXPANSION (user approved 2026-09-25): 14 books total; books 11-14 are Asian-culture books (wish list item 1)
Robot (book 10, robot-who-was-bad-at-everything) continues unchanged. Then, ONE AT A TIME, after each release:
11. Lin and the Night Market Lanterns — TAIWANESE (night market, Ama's stall, beef noodles, bubble tea, lantern festival, temple festivals; Hokkien/Mandarin words). Lesson: honor where you come from and make it your own.
12. Mei and the Dragon Who Feared Thunder — CHINESE mountain village, drought, rain dragon afraid of his own thunder (Chinese dragons bring rain, not fire); Mid-Autumn mooncakes, dumplings, tea. Lesson: courage = acting while afraid.
13. Haru and the Paper That Told the Truth — JAPANESE, Edo-era woodblock print shop making town news sheets; washi, carved blocks, festivals, soba, mochi. Lesson: truth needs courage and kindness together.
14. The River Cousins — KOREAN, cousins (Seoul + countryside) swept down a river, journey home; hanok, kimchi-making, halmoni's kitchen. Lesson: teamwork beats being right.
Per book extras: (a) CULTURAL-ACCURACY CHECK: research each culture on the web (Qwen web_search / WebSearch), keep a "Cultural notes" list in the bible (names, foods, customs, native words, each verified), spot-check finished chapters against it; (b) Vocabulary/Learning section in the bible (incl. a few native words used naturally); (c) Asian characters drawn with accurate, respectful looks (style.json looks); (d) same image style. Site ORDER: append at bottom in this order. Cut library-v1.3 after book 14.
RULE (user, 2026-09-25): do NOT explicitly label the culture ("Taiwanese", "Chinese", "Japanese", "Korean") in book titles, subtitles, cover text, taglines or blurbs. The culture comes through characters, names, food, places, traditions and story, never a label in the title. (Culture names are fine in internal notes.)
PROJECT GOAL (user, 2026-09-25): teach kids life lessons, culture and English, and most importantly make them enjoy reading and love books. Enjoyment first.

## Book 9 (Robot) released (2026-09-25)
- The Robot Who Was Bad at Everything v1.0 live: https://justinyang13.github.io/Project-B/robot-who-was-bad-at-everything/ ; tag robot-who-was-bad-at-everything-v1.0; ORDER appended (position 10); SPEC row 9.
- Lessons: (1) FULL READ-THROUGH by Claude of the whole book (~19k words, ~30k tokens) is worth it: found naming inconsistency (teacher named him Percy on day 1 vs naming scene), tense slip (ch5 p1 present tense), wrong ribbon logic, Marcus/Moose mix, missing-beak parrot, stray header (Entry 42) in ch14, British/American mix (lorry). Qwen's review.md caught mostly false positives here. Do the full read for every remaining book (standing proofreading rule). (2) Qwen overuses a motif phrase ("I did not have a word for it" x12): trim to ~6. (3) Image looks regexes must include the generic descriptors Qwen writes in IMAGE lines: "yellow raincoat" -> Bea, "lab coat"/"silver bob" -> Dr. Pryce; a nickname that is also an animal ("Moose") makes z-image draw the animal: use the real first name (Marcus) in IMAGE lines. Descriptors for one character (yellow raincoat) leak onto others in the same prompt: give each a distinct clothing colour in its descriptor. (4) Cover: state skin tone/hair explicitly in the cover prompt.
- NEXT: Book 10 = Lin and the Night Market Lanterns (Taiwan). First: research Taiwanese culture (web) -> "Cultural notes" + "Vocabulary/Learning" sections in the bible; user rule: no culture label in title/blurb.
## Book 11 started (2026-09-25): Lin and the Night Market Lanterns (Taiwan). Web research done (night market foods/games, Dongzhi tangyuan, LNY reunion dinner + red envelopes, Lantern Festival, Hokkien words). Writing bible/outline/gold ch01.
- 17:10 Book 11 queued (bible w/ cultural notes, outline, gold ch1 done).

## Book 11 (Lin) released (2026-09-25 ~19:00)
- Live: https://justinyang13.github.io/Project-B/lin-and-the-night-market-lanterns/ ; tag lin-and-the-night-market-lanterns-v1.0; ORDER appended; SPEC row 10. Subtitle shortened to "One Big Pot and Sixty-Three Nights" (kicker wrapped badly).
- Lessons: (1) Qwen slipped into PRESENT tense for a whole chapter (ch17): convert with a Qwen "rewrite in past tense" pass, then check. (2) Qwen invents foreign words ("Shab") and inconsistent timelines/facts (Ama's age vs years, brace on/off, whose lantern melted): read fully for continuity. (3) Images: a cover prompt containing "for a title" makes the model paint giant fake Chinese title text; use "top fifth is an empty smooth deep-blue night sky". Hanging red boards/vertical signs always get pseudo-glyphs: say the stall is a bare wooden counter under a plain cream cloth awning, posts hold only lanterns; append "all signs are smooth plain solid-color cloth" to sign-heavy pages. Use full Lin descriptor (name + green jacket + checked apron) in every IMAGE line: generic "a girl" drifts. (4) `pgrep -f` wait loops in a Bash command match themselves and never exit: wait on a pidfile or check the log count instead.
- NEXT: Book 12 Mei and the Dragon Who Feared Thunder (China). Research first; cultural notes + vocabulary in bible; no culture label in title/blurb.

## Book 12 started (2026-09-25 19:00): Mei and the Dragon Who Feared Thunder (China, Sichuan mountain village)
- Research done (dragon lore, Dragon King shrines/rain rites, Longtaitou, Jingzhe, Guyu, Sichuan mountain life, plum blossom). Bible w/ cultural notes, outline (20 ch), config, style, meta, gold ch01 written. Header device: Nainai's bamboo tally stick "Days without rain: N. Buckets from the spring: N." Timeline: 114 dry days -> rain on Longtaitou night (Day 120) -> Grain Rain epilogue.
- Queued 19:00 (queue.txt = mei-and-the-dragon-who-feared-thunder). Character looks: Mei blue jacket/red-string braids/straw hat; Tao green tiger tee + yellow rain boots; Nainai blue jacket grey bun; Hua red jacket yellow ribbon; Yun sea-green dragon, gold belly, antlers, pearl.
- Cover lessons applied: no word "title" in cover prompts; empty sky sentence; no signs.

## Book 12 (Mei) released (2026-09-25 ~21:00)
- Live: https://justinyang13.github.io/Project-B/mei-and-the-dragon-who-feared-thunder/ ; tag mei-and-the-dragon-who-feared-thunder-v1.0; ORDER appended; SPEC status row 11 Released. Lin cover re-released (duplicate subtitle fixed; zip asset re-uploaded).
- USER FEEDBACK -> new rule (CLAUDE.md in /Users/Maxi/Code/Maxi + SPEC section 6 wording pending approval, uncommitted in ~/Code/Project-B): character consistency QA (hair, clothes, shoe colors, accessories, no lookalikes, nothing changes within a scene).
- Lessons: (1) Root cause of drift: looks regex only fired when the IMAGE line named the character. gen_images.py now supports a third element `true` in a look ([regex, desc, true]) = also fires on the PAGE TEXT (main cast). Use it for the 2-4 main characters in every book; give each unique hair + top color + footwear. (2) Regex bug: case-insensitive `\bGrey\b` matched "grey bun/jacket" and added Old Grey the buffalo to every page: use (?-i:...) for names that are common words; `\bdragon\b` also fired on paper dragon/Dragon King. (3) Style prefix must not say "village" (the model draws a village behind every scene, even at a mountain lake); state the location in each IMAGE line, or append a per-range Setting sentence. (4) Rerolls are cheap (about 10 s/page when nothing else runs): reroll all 100 after a systemic fix, then targeted rerolls. (5) Covers: meta.json cover has both `kicker` and `subtitle`; the subtitle renders as a second italic line, so keep `kicker` only (I introduced a duplicate on Lin). Always VIEW cover_front_final.png after any meta change. (6) Text: Qwen invented a live phone call vs "voice message" inconsistency, a stray header line on ch19 p4, a "wooden railing", Old Grey's bell etc.; full read-through caught them.
- NEXT: Book 13 Haru and the Paper That Told the Truth (Japan, Edo-era woodblock print shop). Research first. Apply consistency design from the start (looks with `true` flag).

## 2026-09-25 HOLD: Books 13 (Haru) and 14 (River Cousins)
User: hold off the last two books until they say go. Do NOT start research or production for either. Shelf reordered by user (pushed e604a71); library-v1.4 waits for the next shelf change.

## 2026-09-26 HOLD LIFTED: user said "Let complete the last two books". Book 13 (Haru) first, then Book 14 (River Cousins), one at a time. SPEC.md has an uncommitted row 0 (Juno lesson) awaiting user's "push".

## 2026-09-26 Book 13 (Haru and the Paper That Told the Truth) started
Researched (web-verified, notes in bible): kawaraban/yomiuri, woodblock roles and process (kento, baren, cherry, washi), terakoya, Edo town life, susuharai, toshikoshi soba, yaki-imo, amazake, Setsubun, fires (hinomi-yagura, machibikeshi, firebreaks), nanushi. Slug haru-and-the-paper-that-told-the-truth; header device "*The Owl Alley Sheet, No. N. Today's news: ...*"; third person past close on Haru; looks: Haru flagged true (rust-orange kimono, vermilion cord topknot, indigo apron); others must be named in IMAGE lines. queue.txt set; Monitor armed. NEXT after READY: full read-through, character QA (sheets), covers, release (show blurb to user before pushing), then Book 14 River Cousins.

## 2026-09-26 Book 13 (Haru) built locally, NOT yet pushed
Lessons: SSD was unmounted for ~3h (images blocked; text ran fine; monitor on /Volumes/SSD-4T-LR). Text-cast `true` looks add the flagged character (Haru) to pages where she is only mentioned, and the model then hallucinated a second adult "Haru" (p95) or child; fix by naming her in the IMAGE line as "small Haru ... in front". Modern anachronisms crept in: firefighter with helmet/reflective stripes, modern jacket for Father, black suit for headman, Western bed/pillow, red gabled houses on the back cover; fixed with explicit descriptors ("traditional padded indigo cotton coat with padded cloth hood, no helmet, no reflective strips", "wrap-front dark brown work coat", "small grey topknot dark navy kimono"). Covers: front = original front, back = back5 (empty alley); back covers need "no people at all". Text patches: gray->grey, cobblestones->earth road, mon/price removed, geta indoors, pencil/nib, stray header ch3 p2, ash-door cause of the spark (furnace ash door open) made consistent in ch16/19. Waiting for user's OK on blurb + SPEC wording before push; then gh release haru-and-the-paper-that-told-the-truth-v1.0.

## 2026-09-26 Book 13 (Haru) RELEASED (haru-and-the-paper-that-told-the-truth-v1.0, commit 5234c3a, Pages 200). SPEC row 0 (Juno lesson) went out with it. User rule: book releases need no approval and no pausing.
NEXT: Book 14 The River Cousins (Korea). Then library-v1.4.

## 2026-09-26 Book 14 (The River Cousins) prepared and queued
Research (verified, in bible): jangma, flash floods, hagwon, ondol, red pepper drying, pajeon on rainy days, family words (Halmoni, Harabeoji, Eomma, Appa, aigoo, jeong), summer foods. Header device "*Jun's phone says: ... Nari's river says: ...*"; POV alternates (odd = Jun, even = Nari); flagged true looks: Jun, Nari; others named in IMAGE lines; life vests descriptor keyed on "life vest". Back cover prompt must say no people. Text patch checklist from Haru: run stray-header scan, em-dash scan, geta/anachronism-type scans (here: modern setting so check "cobblestones" etc not needed). queue.txt set.

## 2026-09-26 PAUSED (user restarting the computer): Book 14 The River Cousins in production
State: chapters 1-18 written (ch01-ch10 read and patched; ch11-18 NOT yet read), images ~90/100 done, all background jobs killed cleanly. Ch01-ch10 patches applied (ch3 header/shoes, ch5 score/paragraphs, ch7 Appa line, ch9 battery 59%/peppers line).
RESUME after restart: (1) check SSD mounted: ls /Users/Maxi/Code/Models; (2) cd factory; nohup ./queue.sh >> queue.log 2>&1 & nohup ./watchdog.sh >> watchdog.log 2>&1 & (queue.txt already = the-river-cousins; run_book.sh resumes missing chapters 19-20 and missing images); (3) re-arm Monitor: tail -F watchdog.events | grep -E "STALL|RESTARTED|READY|IDLE"; (4) when READY: read ch11-20 text, patch (stray headers, em dashes, "gray", cobblestones, anachronisms), check sheets for character consistency (Jun white tee/glasses/white sneakers; Nari yellow tee/braid/red band; life vests orange; Halmoni floral+purple visor; Harabeoji green cap+boots; Uncle straw hat navy; Auntie lilac apron; Mr. Cho hat/vest), covers (front + back with NO people), build_html, release (no approval needed), SendUserFile, STATE, library-v1.4 (13 or 14 books).
gen_images.py fix this session: chapter header line (italic first line) ignored for text-cast matching. River Cousins looks are NOT flagged true (names in IMAGE lines required).

## 2026-09-26 (later): Book 14 RELEASED, The River Cousins v1.0 (all 14 planned books done)
- Restarted after the computer restart; ch19-20 written, all 20 chapters read and patched (tense slip, boots vs shoes, rope/oar continuity, Harabeoji "two words", stone gift explained, em dash, gochugaru -> red pepper paste, cover suitcase color).
- Image QA found ~55 bad pages and rerolled them. New lessons:
  - The word "the Pear" in an IMAGE line paints pear FRUIT; the boat descriptor must not contain "pear" (style.json boat look now matches `boat` and says "faded pale leaf green, never brown").
  - Boat was brown on most pages until the look regex was widened to lowercase "boat"; a named prop needs a look that fires on its plain noun.
  - "life vests" descriptor bled onto adults (Mr. Cho, Uncle): the descriptor now says "only the two children wear ... no adult wears a life vest"; also say "Mr. Cho in his khaki fishing vest".
  - Jun keeps getting Nari's straw hat (p28, p47, p59); "wears no hat" only partly works. Accept a hat behind him when seen from the side, or leave the hat out of the shared scene.
  - Naming "the Pear"/"Jun and Nari" in the IMAGE line is required; "a thin boy and a strong girl" produced random children.
  - Back cover: the phrase "deep-teal area, no people" gave an oil-painting style that did not match; a storybook scene (empty farmyard, drying peppers, boat on bank) with "calm pale-green grassy area across the middle" matched.
  - `gen_images.py covers X` skips if the file exists; delete the png first to regenerate.
- Released: `the-river-cousins-v1.0`, Pages 200, cover sent; `library-v1.4` cut (14 books, shelf order in notes). Queue emptied, watchdog stopped.
- NEXT: wish list items 2-5 (reader tracking, high-school books, stats tags, author/publisher names) need the user's go.

## 2026-09-26 Book 15 started: Wren and the Library at the Bottom of the Sea (sea fantasy, user chose idea #3). Rules-header device (Rule N of the Library at the Bottom of the Sea, true rules, #20 rewrites #1). Looks: Wren flagged true (coral-red hooded sweater, denim overalls, yellow boots, moon-shell from ch5); everyone else named in IMAGE lines. Themes: reading is not a race, slow readers read deepest, read aloud anyway. Queued; bible/outline/config/style/meta/gold ch01 done.

## 2026-09-26 PAUSED (user asked to pause and check in): Book 15 Wren and the Library at the Bottom of the Sea
State: bible, outline (20 ch), config, style (looks + 3 covers: front, front2, back), meta, gold ch01 all done. Chapters 1-2 written; ~5 page images done (p001-p005, style verified: gouache teal/pink, Wren consistent). All background jobs (queue, watchdog, run_book, write_book, gen_images, draw-things) killed cleanly; Monitor stopped. queue.txt still = wren-and-the-library-at-the-bottom-of-the-sea.
RESUME: (1) ls /Users/Maxi/Code/Models; (2) cd factory; nohup ./queue.sh >> queue.log 2>&1 & nohup ./watchdog.sh >> watchdog.log 2>&1 & (run_book.sh resumes missing chapters and images); (3) re-arm Monitor: tail -n0 -F watchdog.events | grep --line-buffered -E "STALL|RESTARTED|READY|IDLE"; (4) when READY: full read-through + patches (stray headers, em dashes, tense, invented facts, "spine" etc.), character QA on sheets (Wren coral hooded sweater/denim overalls/yellow boots/moon-shell from ch5; Dad green cap + navy sweater; Mrs. Pell plum cardigan; Ravi striped shirt + red sneakers + satchel; Ottoline purple octopus; Squib cuttlefish; Bartleby turtle w/ bookcase; Clack red crab blue cap), covers (back cover: no people/animals), release, SendUserFile, library-v1.5.
Note: no culture label issue; watch for stray lanterns (style prefix says amber lantern light) and fake lettering on book covers.

## 2026-09-30 Book 16 prepped: The Wizard School Dropout Club (comedy fantasy, user chose idea #16)
- books/the-wizard-school-dropout-club: bible, outline (20 ch, Header = "From the Dropout Club Handbook, Rule N"), config, style (cozy gouache, butter-yellow/plum/moss; Marnie/Gerald/Toby/Lulu/Bunt flagged true), meta, gold ch01 (ingest clean). NOT queued yet: queue.txt still = wren-and-the-library-at-the-bottom-of-the-sea (paused, ch1-2 done). Waiting for user: run this book first or resume Wren first.
- QC reminders: stray Handbook Rule lines on pages 2-5; the word "grand" trips the Gran leak check; gnome descriptor must apply only after ch10; Gerald->hat flicker plant in ch5; twist words (Founder's Hat, Charter, Balance) not before ch12; Marnie never says "perfect" spells work before ch16.

## 2026-09-30 USER DECISIONS
- Order: finish Wren (run + QC + release), THEN restructure: move factory into Project-B/factory/ (scripts+docs tracked; factory/books work data git-ignored), fix paths (release.py, run_book.sh, watchdog.sh, queue.sh), global CLAUDE.md, registry, memory, jCore backup. THEN re-add the-wizard-school-dropout-club to queue.txt and run it. queue.txt now holds only Wren so Dropout does not auto-start.
- Per-book source folders created early in Project-B/<slug>/source (bible, outline) for wren + dropout; release.py recreates them.
- qwen_image_2.1_q8p.ckpt download was approved by user; leave it alone until done.

## 2026-09-30 Wren released; factory moved into Project-B
- **Book 15 Wren and the Library at the Bottom of the Sea RELEASED** (v1.0, tag wren-and-the-library-at-the-bottom-of-the-sea-v1.0, commit 9c6cec8, Pages 200). SPEC rows added.
- **Restructure (user request):** factory moved from /Users/Maxi/Code/Maxi/factory to Project-B/factory (scripts/docs tracked; books/, dist/, tools/, logs/, legacy/ git-ignored). Old Maxi/novel -> factory/legacy/novel. CLAUDE.md moved to Project-B/CLAUDE.md. release.py uses FACTORY.parent; logs now in factory/logs/.
- **USER RULE: do NOT start the next book until the user confirms.** queue.txt currently = Wren only (READY); the-wizard-school-dropout-club is fully prepped (bible, outline, config, style, meta, gold ch01) but NOT queued.
- **Tooling:** draw-things-cli 26.0928.0 crashes (Metal shader compile, macOS 27.0.1); pinned to v26.0910.1 binary (factory/tools/dt-cli-26.0910.1, copied to /opt/homebrew/bin; brew formula uninstalled). Do not upgrade until a fixed release is verified.
- **Wren lessons:** (1) style prefix "glowing amber lantern light" put a lantern into most pages: say "warm amber glow" and keep lantern words only in IMAGE lines that need them. (2) A look regex on a generic noun (`librarian`) fired Mrs. Pell's descriptor on an octopus librarian: match names only. (3) IMAGE lines with generic words ("a tall man", "a girl") make colors bleed (Dad drew in Wren's coral sweater, lost his beard): rewrite with names ("Ben", "Wren") so the descriptors apply; that fixed it in one reroll. (4) Colors in descriptors: say "never pink or red" for a purple octopus. (5) Reroll-all after a systemic fix, then targeted rerolls; ~13 s/image. (6) Qwen review: ~80% noise; real hits were a few typos, "farmhouse", "man" for a crab, a missing second moon-shell, "Dark Stacks".

## 2026-10-01 Book 16 The Wizard School Dropout Club RELEASED (v1.0, photorealistic art)
- Live: https://justinyang13.github.io/Project-B/the-wizard-school-dropout-club/ ; tag the-wizard-school-dropout-club-v1.0; commit f071fcc; SPEC row 15. User asked for photoreal images for this book: model flux_2_klein_9b_i8x (4 steps, ~6 s/image at 768px, faster and more joyful than z_image_turbo); first gouache attempt kept in books/<slug>/art_gouache.
- Photoreal lessons: (1) style prefix words get rendered: "and a real goose" put a goose in nearly every page; never name an object in the global prefix. (2) Negatives prime (`no animals`, `no geese` drew geese on the back cover): describe a still life of the wanted objects only, and use a prefix without the animal. (3) Look regexes flagged true fire on page TEXT, so the recurring pet appears in most scenes; "exactly one X" in the suffix helps. (4) Descriptors for a transformed character (gnome Marnie) bleed onto the pet (red hat on the goose): accept or reroll with names. (5) Cover: pick the clearest 4-face group shot; kicker must fit one line.
- Text QC lessons: Qwen made handbook rule numbers conflict with chapter headers, a hex test that contradicted the hex rule, wrong pronouns for a recurring minor character (Mayor), wand/notebook continuity slips, wrong location (Dimblewick vs Humbleton). Read it all.
- Time: machine run ~1.5 h overnight; QC, 4 reroll rounds and release ~2 h.
- NEXT: ask the user before starting any new book (user rule). queue.txt should stay empty/this book only.

## 2026-10-09 HIGH SCHOOL BATCH STARTED (5:11AM; user approved 10 books, no pauses, release each as soon as it passes Claude's own QC)
- Started once the GPU was free (another session had the Library That Lent Out Weather renders + a Gillian beach-film LTX job; that Library book is still in queue.txt, unfinished: DO NOT run queue.sh, run `run_book.sh <slug>` directly for HS books).
- User decisions: 10 books, order H1..H10 (see SPEC section 9), SAT-level vocabulary, engineering at the center, light clean romance OK, layered meaningful cover art, author "Yang" / publisher "Yang Ink", NO age range on front cover, separate High School shelf, Claude is the quality check, never wait.
- Factory changes: write_book.py reads config (audience, target_words, hard_words, short_lo/hi, long_sentence, sim_max, extra_craft); vocab.py (words to know); build_html appends words; release.py/book.json author+publisher+shelf; make_covers cover.front_foot; build_index High School section; run_book/run_images count chapters from outline.
- H1 renamed "The Atlas of Unmade Land" (the kids' book The Mapmaker's Apprentice already exists).
- H2 Orbit of the Last Orchard prepped (bible/outline/config/style/meta/ch01); covers chosen: frontA2 + backA (composed). Not yet run.
- H3 Clockwork Summer prepped (bible/outline/config/style/meta/ch01), covers chosen frontA+backA composed. Not yet run.
- H4 The Tidewright's Daughter prepped (all files + ch01); covers frontB2+backA composed. Not yet run.
- H5 The Understudy Heir prepped (all + ch01); covers frontA3+backA composed. Not yet run.
- H6 The Archivist of Small Mercies prepped (all + ch01); covers frontB+backA composed. Not yet run.
- H7 The Quiet Heist of Castle Verrow prepped (all + ch01); covers frontA+backA composed. Not yet run.
- H8 Seven Hundred Words for Rain prepped (all + ch01); covers frontA+backA composed. Not yet run.
- H9 Thirteen Minutes of Thunder prepped (all + ch01); covers frontA+backA composed. Not yet run.
- H10 The Lighthouse Debate Society prepped (all + ch01); covers frontB3+backA composed. Not yet run. ALL 10 PREPPED.
- 2026-10-09 7:57AM USER: pause after the first High School book (Atlas). hs_chain.sh stopped; books 2-10 stay prepped but NOT started until the user says go.

## 2026-10-09 H1 The Atlas of Unmade Land RELEASED (v1.0) - Claude QC log
- Read all 25 chapters (50.7k words) and viewed all 125 page images + final covers. Text fixes via factory/patches/the-atlas-of-unmade-land.py (apply.py): continuity (Hester 44 years ago, matching Vasht age 63 and 19 at the time), wrong names (Mrs. Gable/Wynne, Sergeant Major/Ledger, Broadway), engineering sanity (hot chain adds length, 1:1500 race gradient, third-angle numbers, 4,321 vs 4,231 error = 60 ft, closure 1 in 50,000), anachronisms (bug, tire, heat death), loose ends.
- Images: rerolled p12, p16, p74 (extra girl / headless figure / domes). Lesson: the Vasht descriptor flagged True fires on page text and put his hat on Isla; set to False and name him in IMAGE lines.
- Lessons: Qwen at 400-word pages writes decent prose but reuses "like a stone", "the weight of" and invents wrong numbers; always sanity-check the engineering numbers; a style_prefix word like "domes" gives onion domes.
- Pipeline time: ~3h for text, parallel images ~1h; 9 min/chapter. Remaining books 2-10 prepped (bible/outline/config/style/meta/ch01/covers) and PAUSED by the user.
- 2026-10-09 USER: pause. Atlas photoreal page re-render stopped part-way (art_painterly/ holds the released painterly pages; images/ has partial photoreal pages; style.json now photoreal; seed_base 27000). Live site still has the painterly v1.0.

## 2026-10-09 H1 The Atlas of Unmade Land v1.1: ANIME art restyle (user-approved style)
- Style from `Project-I/Inspiration` (Shinkai/Ghibli RPG key art); recipe + samples in `Project-I/wiki/fantasy-style.md`. Model Qwen-Image 2.1 (`qwen_image_2.1_q8p.ckpt`) via `~/.claude/bin/dt-cli-26.0928.0/draw-things-cli`, pages 768x768 (~50 s each), covers 1024x1536. `style.json` now has `cli`, `page_w/page_h`, `cast_first` (new gen_images.py options) and a `test` mode (`gen_images.py <slug> test N..` -> tmp/).
- User complaint on v1 renders: skin color of the main cast kept changing (some far too dark), Isla looked short on some pages. FIX that worked: `cast_first` puts a "Fixed character designs" block BEFORE the scene, each design starts with explicit skin (Isla LIGHT FAIR SKIN, Joss/Sera PALE FAIR, Mags DEEP-BROWN as the text says), explicit height rank (Joss tallest, Sera tall, Isla normal, Mags shortest), plus a one-line consistency reminder at the end (4th element of each `looks` entry). Same fix for cover prompts.
- Remaining flaws found by contact sheets: Isla hair drifting brown/dark on ~12 pages and "a girl in a mustard coat" in an IMAGE line makes a duplicate Isla (p118/119): always write the character's NAME once, never "a girl in X". Rerolled 26,30,43,69,70,87,89,92,98,115,118,119. Old inconsistent renders: images_anime_v1_inconsistent/, photoreal partial: images_photoreal_partial/, painterly v1.0: art_painterly/.
- Covers: front = frontC, back = backA. Known nit: Vane's "pale rigid face" renders grey on p119; Mags reads small/child-like (she is the shortest, 15).
- Cover changed at user request (2026-10-09): front art = Project-I/wiki/fantasy-style/sample_atlas_s11.png cropped 1024x1536 (offset x=88) as images/cover_frontS.png; compose with make_covers.py the-atlas-of-unmade-land frontS backA.
