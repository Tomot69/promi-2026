#!/bin/zsh
# Batteries EN SÉRIE (CLAUDE.md §7) — une à la fois, sortie + code de retour consignés.
# usage : batteries.sh <etiquette> <script1.py> <script2.py> ...
# Le journal va dans sauvegardes/audit-cercle/journaux/ (dans le projet) : il survit à la session.
# Copie adaptée de sauvegardes/aura-orbite-lot/batteries.sh, qui écrivait dans le scratchpad
# d'une session précédente (chemin en dur). On peut forcer un autre dossier : JOURNAUX=/chemin batteries.sh …
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
SP=${JOURNAUX:-"$PWD/sauvegardes/audit-cercle/journaux"}
mkdir -p "$SP"
ET=$1; shift
LOG="$SP/bat_$ET.log"
: > "$LOG"
echo "md5 app.html $(md5 -q app.html)  $(date '+%H:%M:%S')" >> "$LOG"
for s in "$@"; do
  t0=$(date +%s)
  out=$(perl -e 'alarm 1200; exec @ARGV' python3 $s 2>&1)
  rc=$?
  t1=$(date +%s)
  echo "=== $s  rc=$rc  $((t1-t0))s" >> "$LOG"
  echo "$out" | tail -n 40 >> "$LOG"
done
echo "FIN $(date '+%H:%M:%S')" >> "$LOG"
echo "$LOG"
