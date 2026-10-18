#!/bin/zsh
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
J=(redteam_contraste_trait redteam_cercle_couleur redteam_titres_cartes redteam_menu_plus redteam_flash redteam_ordre_guide redteam_onboarding_texte redteam_echelle_onboarding redteam_onb_sorties redteam_onboarding redteam_transitions_onb redteam_tenir redteam_trait redteam_part redteam_commentaires redteam_engagement redteam_lexique redteam_fluide redteam_couleurs_ref redteam_decisions redteam_joignable redteam_ecrans redteam_volume redteam_registre redteam_air)
for j in $J; do
  t0=$(date +%s); python3 $j.py > scratchpad/v149/serie/$j.log 2>&1; rc=$?; t1=$(date +%s)
  echo "$j rc=$rc $((t1-t0))s charge=$(sysctl -n vm.loadavg | awk '{print $2}') :: $(tail -3 scratchpad/v149/serie/$j.log | tr '\n' ' ' | cut -c1-160)" >> scratchpad/v149/serie/bilan.txt
done
echo FINI >> scratchpad/v149/serie/bilan.txt
