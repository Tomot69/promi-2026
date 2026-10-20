#!/bin/zsh
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
OUT=scratchpad/v156/serie.txt; : > $OUT
for j in redteam_achat_fond redteam_deverrouille redteam_depart_orange redteam_guide redteam_guide_fond redteam_ordre_guide redteam_transitions_onb redteam_onboarding_texte redteam_onboarding redteam_onb_sorties redteam_onb_mots redteam_clavier_onb redteam_onb_rejeu redteam_mots_sombre redteam_tenir redteam_fluide redteam_studio_geste redteam_palettes redteam_studio_tom redteam_murs_toucher redteam_engagement redteam_volume redteam_registre redteam_decisions redteam_joignable redteam_ecrans redteam_couleurs_ref; do
  L=$(sysctl -n vm.loadavg | awk '{print $2}'); T0=$(date +%s)
  perl -e 'alarm shift; exec @ARGV' 1800 python3 $j.py > scratchpad/v156/log_$j.txt 2>&1
  R=$(grep -E "^ *(✅|❌) +[0-9]+ */ *[0-9]+|^[0-9]+ / [0-9]+|[0-9]+/[0-9]+ au vert|AUCUN|écart\(s\)|^ *[0-9]+ */ *[0-9]+ *$" scratchpad/v156/log_$j.txt | tail -1)
  NKO=$(grep -c "❌\|^KO" scratchpad/v156/log_$j.txt)
  echo "$j | charge $L | $(( $(date +%s)-T0 )) s | KO $NKO | $R" >> $OUT
done
echo FIN >> $OUT
