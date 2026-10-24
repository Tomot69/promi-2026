#!/bin/zsh
# une batterie à la fois, avec une limite de temps (perl alarm : macOS n'a pas `timeout`)
for j in "$@"; do
  perl -e 'alarm shift; exec @ARGV' 1500 python3 $j.py > scratchpad/v162/g-$j.txt 2>&1
  echo "== $j : $(tail -1 scratchpad/v162/g-$j.txt)"
done
