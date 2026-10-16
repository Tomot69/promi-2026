#!/bin/zsh
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
for j in redteam_onb_sorties redteam_onboarding_texte redteam_commentaires redteam_ecrans redteam_fiches_theme redteam_part redteam_guide; do
  echo "=== $j $(sysctl -n vm.loadavg)" >> scratchpad/v147/serie_a.log
  python3 $j.py > scratchpad/v147/j_$j.log 2>&1
  echo "--- $j : $(tail -1 scratchpad/v147/j_$j.log)" >> scratchpad/v147/serie_a.log
done
echo FINI >> scratchpad/v147/serie_a.log
