#!/bin/bash
# Dynamic queue: reads slugs (one per line) from queue.txt; runs each not-yet-READY book once its prep files exist (prepared by Claude).
cd "$(dirname "$0")"
while true; do
  next=""
  while read -r slug; do
    [ -z "$slug" ] && continue
    [ -f books/$slug/READY ] && continue
    next=$slug; break
  done < queue.txt
  [ -z "$next" ] && { sleep 60; continue; }
  if [ -f books/$next/src/ch01.txt ] && [ -f books/$next/style.json ] && [ -f books/$next/meta.json ] && [ -f books/$next/outline.md ]; then
    if pgrep -f "run_book.sh $next" >/dev/null; then sleep 30; else ./run_book.sh $next; fi
  else sleep 30; fi
done
