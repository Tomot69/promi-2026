#!/bin/zsh
# v145 — la fin de série sur l'arbre FINAL : d'abord les juges de fonction retouchés, puis les juges de cadence, chacun après une attente du calme.
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
J=scratchpad/v145/juges-d
calme(){ local n=0; while [ "$(sysctl -n vm.loadavg | awk '{print ($2>3.2)}')" = "1" ] && [ $n -lt 120 ]; do sleep 5; n=$((n+1)); done; }
passe(){ local nom=$1; shift; local lim=$1; shift; echo "=== $nom · $(date +%H:%M:%S) · charge $(sysctl -n vm.loadavg)" >> $J/_suivi.log; ( "$@" > $J/$nom.log 2>&1 ) & local pid=$!; local t=0
  while kill -0 $pid 2>/dev/null; do sleep 5; t=$((t+5)); if [ $t -gt $lim ]; then kill $pid 2>/dev/null; pkill -P $pid 2>/dev/null; echo "   !! LIMITE DE TEMPS ($lim s)" >> $J/_suivi.log; echo "LIMITE DE TEMPS" >> $J/$nom.log; break; fi; done
  echo "   → $(tail -3 $J/$nom.log | tr '\n' ' ' | cut -c1-300)" >> $J/_suivi.log; }
passe redteam_toucher 1800 python3 redteam_toucher.py
passe redteam_ritournelle 900 python3 redteam_ritournelle.py --ref=8761
passe banc_rendu 2400 python3 banc_rendu.py
passe redteam_reactif 900 python3 redteam_reactif.py
passe redteam_deplace 1800 python3 redteam_deplace.py --mondes=pochade,ritournelle
passe redteam_onb_sorties 900 python3 redteam_onb_sorties.py
passe redteam_decisions 1200 python3 redteam_decisions.py
passe redteam_vide 1200 python3 redteam_vide.py
passe redteam_couleurs_ref 2400 python3 redteam_couleurs_ref.py
echo "=== FIN · $(date +%H:%M:%S)" >> $J/_suivi.log
