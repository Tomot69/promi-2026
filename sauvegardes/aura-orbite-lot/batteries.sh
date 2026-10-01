#!/bin/zsh
# Batteries EN SÉRIE (CLAUDE.md §7) — une à la fois, sortie + code de retour consignés.
# usage : batteries.sh <etiquette> <script1.py> <script2.py> ...
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
SP=/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/dcd8febe-cb8b-4dd6-a4f8-2c1646ff8fa4/scratchpad
ET=$1; shift
LOG=$SP/bat_$ET.log
: > $LOG
echo "md5 app.html $(md5 -q app.html)  $(date '+%H:%M:%S')" >> $LOG
for s in "$@"; do
  t0=$(date +%s)
  out=$(perl -e 'alarm 1200; exec @ARGV' python3 $s 2>&1)
  rc=$?
  t1=$(date +%s)
  echo "=== $s  rc=$rc  $((t1-t0))s" >> $LOG
  echo "$out" | tail -n 40 >> $LOG
done
echo "FIN $(date '+%H:%M:%S')" >> $LOG
