#!/bin/zsh
# v145 — la série sur l'arbre FINAL (app.html), juges de fonction d'abord ; les juges de cadence passent à part, machine au calme.
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
J=scratchpad/v145/juges-b
passe(){ local nom=$1; shift; local lim=$1; shift; echo "=== $nom · $(date +%H:%M:%S) · charge $(sysctl -n vm.loadavg)" >> $J/_suivi.log; ( "$@" > $J/$nom.log 2>&1 ) & local pid=$!; local t=0
  while kill -0 $pid 2>/dev/null; do sleep 5; t=$((t+5)); if [ $t -gt $lim ]; then kill $pid 2>/dev/null; pkill -P $pid 2>/dev/null; echo "   !! LIMITE DE TEMPS ($lim s)" >> $J/_suivi.log; echo "LIMITE DE TEMPS" >> $J/$nom.log; break; fi; done
  echo "   → $(tail -3 $J/$nom.log | tr '\n' ' ' | cut -c1-300)" >> $J/_suivi.log; }
for j in "$@"; do
  case $j in
    releve-*) passe $j 1500 python3 $j.py ;;
    redteam_couleurs_ref) passe $j 2400 python3 $j.py ;;
    redteam_gestes|redteam_air|redteam_joignable|redteam_ecrans) passe $j 2400 python3 $j.py ;;
    *) passe $j 1200 python3 $j.py ;;
  esac
done
echo "=== FIN · $(date +%H:%M:%S)" >> $J/_suivi.log
