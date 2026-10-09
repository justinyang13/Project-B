#!/bin/bash
# usage: run_images.sh <slug>  -- renders page images as chapters appear; prints ALLDONE when 100 exist
cd "$(dirname "$0")"; slug=$1
while true; do
  python3 gen_images.py $slug pages
  i=$(ls books/$slug/images/p[0-9][0-9][0-9].png 2>/dev/null | wc -l)
  tot=$(python3 -c "import json;print(len(json.load(open('books/$slug/outline.json'))['chapters'])*5)")
  if [ "$i" -ge "$tot" ]; then echo ALLDONE; break; fi
  sleep 60
done
