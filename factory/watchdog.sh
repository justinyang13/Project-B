#!/bin/bash
# Watchdog: every 2 min checks the queue, writer (Qwen) and image (Draw Things) jobs. Restarts stalls, logs events to logs/watchdog.events.
cd "$(dirname "$0")"
ev(){ echo "$(date +%H:%M) $*" >> logs/watchdog.events; }
last_prog=0
while true; do
  # keep queue alive
  pgrep -f "queue.sh" >/dev/null || { nohup ./queue.sh >> logs/queue.log 2>&1 & ev "RESTARTED queue.sh"; }
  cur=""
  while read -r s; do [ -z "$s" ] && continue; [ -f books/$s/READY ] && continue; cur=$s; break; done < queue.txt
  if [ -n "$cur" ] && [ -f books/$cur/src/ch01.txt ]; then
    B=books/$cur; now=$(date +%s)
    ch=$(ls $B/chapters/ch*.json 2>/dev/null | wc -l); im=$(ls $B/images/p[0-9][0-9][0-9].png 2>/dev/null | wc -l)
    newest=$(ls -t $B/chapters/*.json $B/images/*.png $B/write_all.log $B/images.log 2>/dev/null | head -1)
    age=$(( now - $(stat -f %m "$newest" 2>/dev/null || echo $now) ))
    running=$(pgrep -f "run_book.sh $cur" | wc -l)
    if [ $running -eq 0 ]; then ev "IDLE-DETECTED $cur not running (queue will start it)"; fi
    if [ $running -gt 0 ] && [ $age -gt 900 ]; then
      ev "STALL $cur no output for ${age}s -> restarting jobs (ch=$ch img=$im)"
      pkill -f "run_book.sh $cur"; pkill -f "write_book.py $cur"; pkill -f "gen_images.py $cur"; pkill -f "run_images.sh $cur"; pkill -f draw-things-cli
      sleep 5
    fi
    if [ $((now - last_prog)) -ge 600 ]; then ev "PROGRESS $cur chapters=$ch/20 images=$im/100 (last output ${age}s ago)"; last_prog=$now; fi
  fi
  for s in $(cat queue.txt); do [ -f books/$s/READY ] && ! grep -q "READY-NOTIFIED $s" logs/watchdog.events 2>/dev/null && ev "BOOK READY for Claude QC: $s (READY-NOTIFIED $s)"; done
  sleep 120
done
