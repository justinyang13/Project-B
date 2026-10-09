#!/bin/bash
# Runs the High School books one after another (text + page images + sheets + vocab), starting each as soon as the previous one is READY.
# usage: nohup ./hs_chain.sh > logs/hs_chain.log 2>&1 &
cd "$(dirname "$0")"
BOOKS="the-atlas-of-unmade-land orbit-of-the-last-orchard clockwork-summer the-tidewrights-daughter the-understudy-heir the-archivist-of-small-mercies the-quiet-heist-of-castle-verrow seven-hundred-words-for-rain thirteen-minutes-of-thunder the-lighthouse-debate-society"
for b in $BOOKS; do
  if [ ! -f books/$b/READY ]; then
    if ! pgrep -f "run_book.sh $b" >/dev/null; then echo "$(date) starting $b"; ./run_book.sh $b; fi
    while [ ! -f books/$b/READY ]; do sleep 30; done
  fi
  echo "$(date) READY $b"
done
echo "$(date) all HS books READY"
