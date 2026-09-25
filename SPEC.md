# Project B — Series Spec

Status: **approved by the owner 2026-09-24, in progress.** This file is the plan of record. Update the status table at the bottom as books ship.

## 1. Goal

Write and publish **7 more illustrated middle-grade novels** (readers aged 10–12) after the first book, *Juno Vale and the Tide That Forgot*. Each book is read on a phone or laptop through a web reader hosted on GitHub Pages.

**Quality bar: best-seller quality**, in story, prose and illustrations. No corners cut. Quality wins over speed if they conflict.

## 2. Book format (every book)

- 100 pages = 20 chapters × 5 pages. About 200–260 words per page (about 27,000 words in total).
- One small illustration on every page, plus a front cover and a back cover.
- Its own folder in this repo: `<book-slug>/` with `index.html` (reader), `book.json`, `img/`, full-size covers and `source/`.
- Its own narrator voice, illustration palette and main life lesson.
- Ages 10–12: warm, funny, emotionally honest. Gentle peril only. No gore, no romance, **no spooky or ghost content**.

## 3. Lineup (approved)

| # | Title | Genre | Hero | Main lesson | Also touches |
|---|---|---|---|---|---|
| 1 | The Day That Wouldn't End | Funny time-loop | Max, 11 | **Happiness is a choice**, not a result. Nothing will make you happy until you choose to be happy. | Appreciating family and friends |
| 2 | Zia and the Runaway Space Station | Sci-fi adventure | Zia, 12 | **Asking for help is a strength**; teamwork | "Kids can't be engineers" |
| 3 | The Mapmaker's Apprentice | Historical-style quest | Tam, 11 | **Be better than you were yesterday.** Growth speed matters more than where you are in life. | Perseverance; mistakes teach |
| 4 | Pip and the Storm-Sparrows | Animal fantasy | Pip, the smallest sparrow | **Never let anyone tell you that you can't.** If you want something, go get it. | Being different is a strength |
| 5 | Fifty-One Ways to Lose a Soccer Game | Realistic sports comedy | Dani, 12 | **Confidence comes from within.** A loss doesn't hurt your value; it only changes your strategy. | Sportsmanship |
| 6 | Rue and the Troll Under Bridgewater Bridge | Cozy fairy-tale fantasy | Rue, 10 | **Empathy:** look past appearances; be kind to people who feel left out | Forgiveness |
| 7 | The Garden at the Edge of the Concrete | Magic-garden adventure | Sana, 11 | **Responsibility and patience**: good things grow slowly | Speaking up |

The owner's four core lessons, in their words, are spread across the books:
1. *Happiness is a choice, not a result.*
2. *If your confidence comes from within, a "loss" in a competition doesn't hurt your value; it just changes your strategy.*
3. *Never let someone tell you, you can't do something. If you want something you have to go get it.*
4. *You just have to be better than you are yesterday. Growth speed is more important than where you are in your life.*

Lessons are **dramatized through the hero's choices**, never preached by the narrator. One earned moment of plain statement is allowed near the end.

## 4. Roles

- **Local AI does the work** (owner's standing rule; all free, all local):
  - `qwen3.8:27b` via Ollama's HTTP API drafts and revises the prose. It also checks illustrations (it can read images).
  - `draw-things-cli` with `z_image_turbo_1.0_q8p` (models on the external SSD) paints illustrations and cover art.
  - Headless Chrome composes cover typography.
- **Claude orchestrates**: writes the story bible and outline, sets the voice, runs quality checks, reads every book end to end, patches continuity, builds and releases.
- Never route through wrapper tools; talk to Ollama and Draw Things directly. One heavy model at a time on the 64 GB machine.

## 5. Production pipeline (per book)

1. **Bible + outline (Claude).** Premise, cast with fixed looks and speech habits, rules of the story world, a narrator-voice sample paragraph, humor style, running gags, setups and payoffs, and a **beat for every one of the 100 pages** (what happens, the feeling, one concrete funny or sensory detail, the hook).
2. **Art direction.** A per-book palette and style prefix, plus fixed character descriptions that are injected into every prompt so heroes look the same on every page. A short style bake-off on the hero picks the look.
3. **Draft (Qwen).** One chapter at a time from its five page beats, using the bible, the voice sample, the outline beats of earlier chapters as context (never the model's own summaries) and a list of similes already used.
4. **Lint gate.** Automatic checks reject or flag: cliché phrases ("stone in her throat", "heart hammered", "held her breath", "It wasn't X. It was Y." overuse, and the like), repeated similes across chapters, page length outside 180–330 words, leaked future plot, missing image prompts.
5. **Edit pass (Qwen).** A second call revises the chapter against the specific lint findings and an editor checklist: show don't tell, fresh specific detail, sharper dialogue, distinct character voices, funnier jokes, stronger page-end hooks.
6. **Claude read-through.** Read the whole book; fix continuity, timeline, tone and lesson delivery; send weak pages back for rewrite or patch them directly.
7. **Illustrations.** One image per page at 768 px. Contact sheets are reviewed by Claude and by Qwen vision; bad ones (wrong character, artifacts, drawn text, odd anatomy) are re-rolled with new seeds. Covers: several candidates, best one picked, typography composed in HTML and exported by headless Chrome.
8. **Build.** `build_html.py` makes the reader (spreads on desktop, single page on phone, contents, text size, paper colors, remembers the page).
9. **Release (automatic, no need to ask).** Copy the book into `Project-B/<slug>/`, add `book.json`, run `build_index.py`, commit, push to `main` (GitHub Pages redeploys), create a GitHub release with a zip, then send the owner a short update with the link.

## 6. Quality checklist a book must pass before release

- [ ] Opening page hooks within the first paragraph; every chapter ends on a hook, laugh or feeling.
- [ ] Clear arc: want → escalating obstacles → midpoint turn → low point → climax where the hero applies the lesson by choice → satisfying, earned ending with a callback to the opening.
- [ ] Voice is distinct from the other books and consistent throughout.
- [ ] Humor lands (running gags pay off); emotion feels true, not sugary.
- [ ] Zero banned clichés; no simile repeated across the book; no more than one "It wasn't X, it was Y" per chapter.
- [ ] Timeline, names, looks and facts are consistent (checked against the bible).
- [ ] Every illustration matches its page, characters look the same throughout, no drawn text or anatomy glitches.
- [ ] Reader opens on desktop and phone width with no console errors; covers look professional.

## 7. Repo layout

```
Project-B/
  SPEC.md                  this file
  index.html               library home page (generated by build_index.py)
  build_index.py
  README.md
  <book-slug>/             one folder per book
    index.html  book.json  img/  cover_front.png  cover_back.png  source/
```

## 8. Status

| # | Book | Status | Release |
|---|---|---|---|
| 0 | Juno Vale and the Tide That Forgot | Released | v1.0 |
| 1 | The Day That Wouldn't End | Released | v1.0 |
| 2 | Zia and the Runaway Space Station | Released | v1.0 |
| 3 | The Mapmaker's Apprentice | Released | v1.0 |
| 4 | Pip and the Storm-Sparrows | Queued | — |
| 5 | Fifty-One Ways to Lose a Soccer Game | Queued | — |
| 6 | Rue and the Troll Under Bridgewater Bridge | Queued | — |
| 7 | The Garden at the Edge of the Concrete | Queued | — |

Working notes and per-book source live outside the repo in `/Users/justin/Code/Maxi/factory/` (see its `STATE.md`).
