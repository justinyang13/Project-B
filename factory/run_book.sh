#!/bin/bash
# usage: run_book.sh <slug>  -- full automatic production for one prepared book (needs bible/outline.json/config/style/meta + src/ch01.txt)
# text (Qwen) and images (Draw Things) run in parallel; then cover candidates + contact sheets; writes books/<slug>/READY when done.
cd "$(dirname "$0")"; slug=$1; B=books/$slug
python3 lib/outline.py $B >/dev/null
[ -f $B/chapters/ch01.json ] || python3 ingest.py $slug 1
python3 write_book.py $slug 2 $(python3 -c "import json;print(len(json.load(open('$B/outline.json'))['chapters']))") > $B/write_all.log 2>&1 &
WP=$!
./run_images.sh $slug > $B/images.log 2>&1 &
IP=$!
wait $WP; echo "$(date) text done" >> $B/progress.log
wait $IP; echo "$(date) images done" >> $B/progress.log
[ -f $B/NOCOVERS ] || python3 gen_images.py $slug covers front front2 back >> $B/images.log 2>&1
python3 contact_sheet.py $slug 25 >> $B/images.log 2>&1
python3 vocab.py $slug >> $B/progress.log 2>&1
python3 readthrough.py $slug > $B/readthrough.log 2>&1
echo "$(date) READY for Claude QC (sheets, review.md, covers)" >> $B/progress.log; touch $B/READY
