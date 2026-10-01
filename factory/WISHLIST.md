# Project B wish list and to-do (updated 2026-10-01)

Book numbers follow SPEC.md (numbered from 0): Wren = #14, The Wizard School Dropout Club = #15 (16 books live in total).

## Wish list (the user's ideas; nothing here starts until the user says go)

| # | Idea | Status | Notes / what is needed first |
|---|---|---|---|
| 1 | More Asian-culture children's books (Taiwanese, Chinese, Japanese, Korean) | **DONE** | Lin (Taiwan), Mei (China), Haru (Japan), The River Cousins (Korea), all live |
| 2 | Reader tracking with a simple username (per-book progress) | not started | Site is static on GitHub Pages, so phones cannot reach a server on this Mac: needs a tunnel (Cloudflare Tunnel/Tailscale) or other hosting. Privacy: username only, no real names/emails/passwords, kids' data |
| 3 | Higher age-level books (high school) | not started | Decide: age band, "serious but appropriate" content rules, tone and reading level, separate shelf/section, image style for older readers |
| 4 | Book stats tags on every book (and in book.json) | not started | Decide which stats: pages/chapters, word count, reading time, reading level, genre, main lesson, themes, vocabulary words, culture |
| 5 | Author and publisher names on the books | not started | Need from the user: the author name, the publisher name, and where they appear (cover, title page, book pages, site footer, book.json) |

## Project B to-do

**Done recently (2026-09-30 to 10-01):** Wren (#14) and The Wizard School Dropout Club (#15, photorealistic art) released and live; factory moved into `Project-B/factory/`; `draw-things-cli` pinned to v26.0910.1; Project B memory removed from the jCore backup.

**Open:**
- [ ] Pick the next book (unused ideas: polite dragon, unlucky fairy godmother, Library That Lent Out Weather, others). Do not start until the user confirms.
- [ ] Look at the ~1,800 files git shows as modified in the repo (unexplained; images, covers, book.json, README, SPEC). Decide: real changes, or noise to discard.
- [ ] Shelf order: Wren and Dropout Club were appended at the end of the home page; confirm where they belong in `build_index.py` ORDER.
- [ ] Optional: re-roll Dropout Club pages 68 and 79 (a hat shows up on the goose).
- [ ] Optional: cut a library release tag (library-v1.5) now that two books were added (last was library-v1.4 at 14 books).
- [ ] Back up the Project B memory notes somewhere private (they now exist only in `~/.claude/projects/-Users-Maxi-Code-Project-B/memory/`).
- [ ] The downloaded `qwen_image_2.1_q8p` model is unused; try it on a future book if useful, or leave it.
- [ ] Re-test `draw-things-cli` when a newer release than v26.0928.0 appears (the Metal shader crash on macOS 27); only then unpin.
