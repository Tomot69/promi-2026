#!/bin/zsh
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
OUT=scratchpad/v154/serie.txt; : > $OUT
for j in redteam_guide_fond redteam_tenir_presse redteam_tenir redteam_tenir_e3 redteam_guide redteam_ordre_guide redteam_validation redteam_engagement redteam_fluide redteam_volume redteam_registre redteam_decisions redteam_joignable redteam_ecrans redteam_couleurs_ref; do
  L=$(sysctl -n vm.loadavg | awk '{print $2}')
  T0=$(date +%s)
  R=$(perl -e 'alarm shift; exec @ARGV' 1800 python3 $j.py 2>&1 | tail -4 | tr '\n' ' ' | cut -c1-400)
  echo "$j | charge $L | $(( $(date +%s)-T0 )) s | $R" >> $OUT
done
echo FIN >> $OUT
