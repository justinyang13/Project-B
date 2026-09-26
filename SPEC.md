# Project B — Series Spec

Status: **approved by the owner 2026-09-24, in progress.** This file is the plan of record. Update the status table at the bottom as books ship.

## 1. Goal

**Purpose.** These books teach kids life lessons, introduce them to cultures from around the world, help them learn English, and, most importantly, help them enjoy reading and fall in love with books.

**Scope.** A growing shelf of illustrated middle-grade novels (readers aged 10–12), starting with *Juno Vale and the Tide That Forgot*. Each book is read on a phone or laptop through a web reader hosted on GitHub Pages, and each one is released as soon as it is finished. Later books bring stories, characters, food, traditions and family life from different cultures; culture comes through the story itself, never through labels in titles or blurbs.

**Quality bar: best-seller quality**, in story, prose and illustrations. No corners cut. Quality wins over speed if they conflict. Every book is written as a well-known children's book author would write it: consistent story line, age-appropriate content, real proofreading, vocabulary and facts a reader takes away, and pacing that never bores or rushes. The illustration and cover style stays consistent across the library.

## 2. Book format (every book)

- 100 pages = 20 chapters × 5 pages. About 200–260 words per page (about 27,000 words in total).
- One small illustration on every page, plus a front cover and a back cover.
- Its own folder in this repo: `<book-slug>/` with `index.html` (reader), `book.json`, `img/`, full-size covers and `source/`.
- Its own narrator voice, illustration palette and main life lesson.
- Ages 10–12: warm, funny, emotionally honest. Gentle peril only. No gore, no romance, **no spooky or ghost content**.

## 3. Lineup (approved)

| # | Title | Genre | Hero | Main lesson | Also touches |
|---|---|---|---|---|---|
| 0 | Juno Vale and the Tide That Forgot | Coastal mystery adventure | Juno, 11 | **Real courage is listening**, not being loud. The sea answers the listening. | Grief and memory; being the new kid; friendship |
| 1 | The Day That Wouldn't End | Funny time-loop | Max, 11 | **Happiness is a choice**, not a result. Nothing will make you happy until you choose to be happy. | Appreciating family and friends |
| 2 | Zia and the Runaway Space Station | Sci-fi adventure | Zia, 12 | **Asking for help is a strength**; teamwork | "Kids can't be engineers" |
| 3 | The Mapmaker's Apprentice | Historical-style quest | Tam, 11 | **Be better than you were yesterday.** Growth speed matters more than where you are in life. | Perseverance; mistakes teach |
| 4 | Pip and the Storm-Sparrows | Animal fantasy | Pip, the smallest sparrow | **Never let anyone tell you that you can't.** If you want something, go get it. | Being different is a strength |
| 5 | Fifty-One Ways to Lose a Soccer Game | Realistic sports comedy | Dani, 12 | **Confidence comes from within.** A loss doesn't hurt your value; it only changes your strategy. | Sportsmanship |
| 6 | Rue and the Troll Under Bridgewater Bridge | Cozy fairy-tale fantasy | Rue, 10 | **Empathy:** look past appearances; be kind to people who feel left out | Forgiveness |
| 7 | The Garden at the Edge of the Concrete | Magic-garden adventure | Sana, 11 | **Responsibility and patience**: good things grow slowly | Speaking up |
| 8 | Mo and the Mountain That Walks | Fantasy adventure | Mo, 11 | **Home is the people you are with**, not the place you stand on | Listening; the courage to change |
| 9 | The Robot Who Was Bad at Everything | School sci-fi comedy | PERFECT-9 (Percy) | **Joy comes from trying**, not from being perfect | Faking a mistake is hiding |
| 10 | Lin and the Night Market Lanterns | Family story, night market | Lin, 11 | **Honor where you come from and make it your own** | Pride, family traditions, food, festivals |
| 11 | Mei and the Dragon Who Feared Thunder | Village fantasy | Mei, 11 | **Courage is acting while you are afraid** | Speaking up; dragon lore, rain, village life |
| 12 | Haru and the Paper That Told the Truth | Historical story, woodblock print shop | Haru | **Truth needs courage and kindness together** | Craft, honesty, town life long ago |
| 13 | The River Cousins | Family adventure | Two cousins | **Teamwork beats being right** | City and countryside, family, food |

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
   **Reference styles (owner's favorites, 2026-09-25, in this order):** (1) *Mo and the Mountain That Walks* (its chapter 1 is "The Morning the Mountain Turned"), (2) *Rue and the Troll Under Bridgewater Bridge*. New books should aim for this level of illustration and pick one of the two looks (or a close cousin) unless the owner approves a new one.
   - **Look 1, Mo: "quiet gouache landscape".** Matte opaque gouache with fine soft-pencil linework, a muted natural palette (sage green, dusty ochre, apricot sunrise), airy skies, small characters against huge calm scenery, gentle whimsical detail. Works best for outdoor, big-scale, misty or sunrise scenes and quiet moods. Style prefix: "Warm storybook illustration in gouache and soft pencil with sweeping painterly landscapes, sage green pines, dusty ochre and apricot sunrise light, small figures against huge quiet scenery, gentle whimsical detail, no text, no writing, no letters, no signs: ".
   - **Look 2, Rue: "cozy textured storybook painting".** Gouache with visible thick brush texture (almost oil-painted, swirling strokes in sky, leaves and stone) plus colored-pencil detail, warm lamplight against plum and slate-blue shadows, rounded friendly shapes, cute expressive characters, fairy-tale village charm. Works best for cozy dusk/lamp-lit scenes, villages, characters up close. Style prefix: "Cozy storybook gouache illustration with soft textured brushwork and colored pencil detail, honey-amber lamplight, moss green, plum and slate-blue shadows, rounded friendly shapes, warm fairy-tale village charm, like a beloved picture-book classic, no text, no writing, no letters, no signs: ".
   - Both are the same family (gouache + pencil, picture-book classic, one small vignette per page, covers with a large calm sky for the title). What differs is the brush texture and the palette. The exact prompts and seeds live in each book's `style.json`; see `RUNBOOK.md` section 4 in the factory for the keyword-to-effect table.
3. **Draft (Qwen).** One chapter at a time from its five page beats, using the bible, the voice sample, the outline beats of earlier chapters as context (never the model's own summaries) and a list of similes already used.
4. **Lint gate.** Automatic checks reject or flag: cliché phrases ("stone in her throat", "heart hammered", "held her breath", "It wasn't X. It was Y." overuse, and the like), repeated similes across chapters, page length outside 180–330 words, leaked future plot, missing image prompts.
5. **Edit pass (Qwen).** A second call revises the chapter against the specific lint findings and an editor checklist: show don't tell, fresh specific detail, sharper dialogue, distinct character voices, funnier jokes, stronger page-end hooks.
6. **Claude read-through.** Read the whole book; fix continuity, timeline, tone and lesson delivery; send weak pages back for rewrite or patch them directly.
7. **Illustrations.** One image per page at 768 px. Contact sheets are reviewed by Claude and by Qwen vision; bad ones (wrong character, artifacts, drawn text, odd anatomy) are re-rolled with new seeds. Every page is also checked for **character consistency** (hair, clothing, shoe colors, accessories, no lookalike characters, nothing changing within a scene); fixes go through tighter character descriptors and re-rolls. Covers: several candidates, best one picked, typography composed in HTML and exported by headless Chrome.
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
- [ ] **Character consistency (checked page by page):** each character keeps the same hair style and length, clothing colors, shoe color and accessories on every page and within every scene; no two characters look alike (each has a distinct hair style, main clothing color, signature accessory and footwear, fixed in the story bible and the art descriptors); the setting matches the text; no stray animals.
- [ ] Reader opens on desktop and phone width with no console errors; covers look professional.
- [ ] Proofread end to end by Claude: tense, spelling, British/American mix, invented or misused foreign words.
- [ ] Age-appropriate (ages 10–12) and consistent with the story bible.
- [ ] Learning value: target vocabulary used in context, and facts or customs a reader takes away.
- [ ] Engagement and pacing: no slow stretches, no rushed ones.
- [ ] Culture books only: cultural facts web-checked, respectful and accurate character looks, no culture label in title, cover or blurb.
- [ ] Illustration and cover style matches the rest of the library.

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
| 4 | Pip and the Storm-Sparrows | Released | v1.0 |
| 5 | Fifty-One Ways to Lose a Soccer Game | Released | v1.0 |
| 6 | Rue and the Troll Under Bridgewater Bridge | Released | v1.0 |
| 7 | The Garden at the Edge of the Concrete | Released | v1.0 |
| 8 | Mo and the Mountain That Walks | Released | v1.0 |
| 9 | The Robot Who Was Bad at Everything | Released | v1.0 |
| 10 | Lin and the Night Market Lanterns | Released | v1.0 |
| 11 | Mei and the Dragon Who Feared Thunder | Released | v1.0 |
| 12 | Haru and the Paper That Told the Truth | Released | v1.0 |
| 13 | The River Cousins | Planned | |

Working notes and per-book source live outside the repo in `/Users/justin/Code/Maxi/factory/` (see its `STATE.md`).
