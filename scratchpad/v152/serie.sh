#!/bin/zsh
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
J=(redteam_mots_sombre.py redteam_onb_sorties.py redteam_onb_mots.py redteam_onb_rejeu.py redteam_echelle_onboarding.py redteam_onboarding_texte.py redteam_guide.py redteam_ordre_guide.py redteam_engagement.py redteam_verrou_onboarding.py redteam_lexique.py redteam_peaufiner.py redteam_registre.py redteam_tokens.py redteam_volume.py redteam_couleurs_ref.py redteam_decisions.py redteam_joignable.py redteam_ecrans.py)
for j in $J; do
  a=$(sysctl -n vm.loadavg | awk '{print $2}'); t0=$(date +%s)
  perl -e "alarm shift; exec @ARGV" 1500 python3 $j > scratchpad/v152/serie/$j.log 2>&1; c=$?
  b=$(sysctl -n vm.loadavg | awk '{print $2}'); t1=$(date +%s)
  r=$(grep -E "^\s*(✅|❌)\s+[0-9]+ / [0-9]+|^(✅|❌)" scratchpad/v152/serie/$j.log | tail -1)
  echo "$j code $c · $((t1-t0)) s · charge $a→$b · $r" >> scratchpad/v152/serie.txt
done
echo FIN >> scratchpad/v152/serie.txt
