# Project B

Illustrated novels for young readers. Text drafted with a local LLM (qwen3.8:27b), illustrations rendered locally (Z Image Turbo via Draw Things), covers composed in HTML, and each book is a self-contained web reader.

Open `index.html` (or the GitHub Pages site) to browse the library.

## Books

| Book | Genre | Ages | Pages | Folder |
|---|---|---|---|---|
| **Juno Vale and the Tide That Forgot** | Fantasy adventure | 10–12 | 100 | [`juno-vale-and-the-tide-that-forgot/`](juno-vale-and-the-tide-that-forgot/index.html) |
| **Mei and the Dragon Who Feared Thunder** | Fantasy adventure | 10–12 | 100 | [`mei-and-the-dragon-who-feared-thunder/`](mei-and-the-dragon-who-feared-thunder/index.html) |
| **Mo and the Mountain That Walks** | Fantasy adventure | 10–12 | 100 | [`mo-and-the-mountain-that-walks/`](mo-and-the-mountain-that-walks/index.html) |
| **Rue and the Troll Under Bridgewater Bridge** | Cozy fairy-tale fantasy | 10–12 | 100 | [`rue-and-the-troll-under-bridgewater-bridge/`](rue-and-the-troll-under-bridgewater-bridge/index.html) |
| **The Day That Wouldn't End** | Funny time-loop adventure | 10–12 | 100 | [`the-day-that-wouldnt-end/`](the-day-that-wouldnt-end/index.html) |
| **The Garden at the Edge of the Concrete** | Magic-garden adventure | 10–12 | 100 | [`the-garden-at-the-edge-of-the-concrete/`](the-garden-at-the-edge-of-the-concrete/index.html) |
| **Pip and the Storm-Sparrows** | Animal fantasy adventure | 10–12 | 100 | [`pip-and-the-storm-sparrows/`](pip-and-the-storm-sparrows/index.html) |
| **Zia and the Runaway Space Station** | Sci-fi adventure | 10–12 | 100 | [`zia-and-the-runaway-space-station/`](zia-and-the-runaway-space-station/index.html) |
| **Lin and the Night Market Lanterns** | Family adventure | 10–12 | 100 | [`lin-and-the-night-market-lanterns/`](lin-and-the-night-market-lanterns/index.html) |
| **Fifty-One Ways to Lose a Soccer Game** | Sports comedy | 10–12 | 100 | [`fifty-one-ways-to-lose-a-soccer-game/`](fifty-one-ways-to-lose-a-soccer-game/index.html) |
| **The Mapmaker's Apprentice** | Historical-style adventure quest | 10–12 | 100 | [`the-mapmakers-apprentice/`](the-mapmakers-apprentice/index.html) |
| **The Robot Who Was Bad at Everything** | School sci-fi comedy | 10–12 | 100 | [`robot-who-was-bad-at-everything/`](robot-who-was-bad-at-everything/index.html) |
| **Haru and the Paper That Told the Truth** | Historical adventure | 10–12 | 100 | [`haru-and-the-paper-that-told-the-truth/`](haru-and-the-paper-that-told-the-truth/index.html) |
| **The River Cousins** | Summer adventure | 10–12 | 100 | [`the-river-cousins/`](the-river-cousins/index.html) |
| **Wren and the Library at the Bottom of the Sea** | Cozy sea fantasy | 10–12 | 100 | [`wren-and-the-library-at-the-bottom-of-the-sea/`](wren-and-the-library-at-the-bottom-of-the-sea/index.html) |
| **The Wizard School Dropout Club** | Comedy fantasy | 10–12 | 100 | [`the-wizard-school-dropout-club/`](the-wizard-school-dropout-club/index.html) |

## Layout

```
Project-B/
  index.html               library home page (generated)
  build_index.py           regenerates index.html from each book's book.json
  SPEC.md                  series plan of record
  CLAUDE.md                project rules for Claude
  <book-slug>/             one folder per published book
    index.html             the book reader (open this to read)
    book.json              title, cover, blurb for the library page
    img/                   page illustrations + covers (web size)
    cover_front.png  cover_back.png
    source/                story bible, outline, chapter text (JSON)
  factory/                 production tooling (scripts, RUNBOOK.md, STATE.md, WISHLIST.md)
    books/ dist/ tools/ logs/ legacy/   local work data, git-ignored
```

## Adding a book

Prepare it in `factory/books/<slug>/` (see `factory/RUNBOOK.md`), then `factory/release.py <slug>` copies it into `<slug>/`, writes `book.json` and runs `build_index.py`.
