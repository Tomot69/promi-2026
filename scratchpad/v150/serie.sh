#!/bin/zsh
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
J=(redteam_garder redteam_ruban redteam_onboarding_texte redteam_onboarding redteam_onb_sorties redteam_echelle_onboarding redteam_flash redteam_validation redteam_trait redteam_couleurs_ref redteam_decisions redteam_joignable redteam_ecrans redteam_volume redteam_registre redteam_air)
for j in $J; do
  t0=$(date +%s); python3 $j.py > scratchpad/v150/serie/$j.log 2>&1; rc=$?; t1=$(date +%s)
  echo "$j rc=$rc $((t1-t0))s charge=$(sysctl -n vm.loadavg | awk '{print $2}') :: $(tail -3 scratchpad/v150/serie/$j.log | tr '\n' ' ' | cut -c1-160)" >> scratchpad/v150/serie/bilan.txt
done
echo FINI >> scratchpad/v150/serie/bilan.txt
