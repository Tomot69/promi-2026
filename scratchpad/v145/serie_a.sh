#!/bin/zsh
# v145 — la série du premier commit (§1, §2, §3), sur la copie FIGÉE zz-v145a.html (+ son moteur) : app.html peut continuer d'avancer.
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
J=scratchpad/v145/juges; F=zz-v145a.html
calme(){ local n=0; while [ "$(sysctl -n vm.loadavg | awk '{print ($2>4.5)}')" = "1" ] && [ $n -lt 180 ]; do sleep 5; n=$((n+1)); done; }
passe(){ local nom=$1; shift; local lim=$1; shift; echo "=== $nom · $(date +%H:%M:%S) · charge $(sysctl -n vm.loadavg)" >> $J/_suivi.log; ( "$@" > $J/$nom.log 2>&1 ) & local pid=$!; local t=0
  while kill -0 $pid 2>/dev/null; do sleep 5; t=$((t+5)); if [ $t -gt $lim ]; then kill $pid 2>/dev/null; pkill -P $pid 2>/dev/null; echo "   !! LIMITE DE TEMPS ($lim s)" >> $J/_suivi.log; echo "LIMITE DE TEMPS" >> $J/$nom.log; break; fi; done
  echo "   → $(tail -3 $J/$nom.log | tr '\n' ' ' | cut -c1-260)" >> $J/_suivi.log; }
calme; passe pleine-apres-sombre 2400 python3 scratchpad/v145/pleine.py $F --sombre --n=25,50 --sortie=F-apres-sombre --charge=4.5
calme; passe pleine-avant-clair 3000 python3 scratchpad/v145/pleine.py app.html --port=8762 --sortie=F-avant-clair --charge=4.5
calme; passe pleine-avant-sombre 1500 python3 scratchpad/v145/pleine.py app.html --port=8762 --sombre --n=25 --sortie=F-avant-sombre --charge=4.5
calme; passe redteam_pleine 900 python3 redteam_pleine.py $F
calme; passe redteam_pleine-v144 900 python3 redteam_pleine.py --port=8762
passe redteam_ritournelle 900 python3 redteam_ritournelle.py $F --ref=8761
calme; passe redteam_evol 1200 python3 redteam_evol.py $F
passe redteam_reactif 900 python3 redteam_reactif.py $F
passe redteam_toucher 1800 python3 redteam_toucher.py $F
passe banc_rendu 2400 python3 banc_rendu.py $F
calme; passe redteam_rythme 1800 python3 redteam_rythme.py $F
echo "=== FIN · $(date +%H:%M:%S)" >> $J/_suivi.log
