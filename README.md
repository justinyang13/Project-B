# Project B

Illustrated novels for young readers. Text drafted with a local LLM (qwen3.8:27b), illustrations rendered locally (Z Image Turbo via Draw Things), covers composed in HTML, and each book is a self-contained web reader.

Open `index.html` (or the GitHub Pages site) to browse the library.

## Books

| Book | Ages | Pages | Folder |
|---|---|---|---|
| **Juno Vale and the Tide That Forgot** — a Saltmarsh Harbor adventure | 10–12 | 100 | [`juno-vale-and-the-tide-that-forgot/`](juno-vale-and-the-tide-that-forgot/index.html) |

## Layout

```
Project-B/
  index.html               library home page (generated)
  build_index.py           regenerates index.html from each book's book.json
  <book-slug>/
    index.html             the book reader (open this to read)
    book.json              title, cover, blurb for the library page
    img/                   page illustrations + covers (web size)
    cover_front.png        full-size covers
    cover_back.png
    source/                story bible, chapter text (JSON) and the scripts used to make the book
```

## Adding a book

1. Make a new folder `<book-slug>/` with an `index.html` reader and a `book.json` (copy the existing one).
2. Run `python3 build_index.py`.
