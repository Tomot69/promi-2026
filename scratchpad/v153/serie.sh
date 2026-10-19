#!/bin/zsh
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
until [ -f scratchpad/v153/serie2.fin ]; do sleep 5; done
: > scratchpad/v153/serie.txt
for j in redteam_guide redteam_clavier_onb redteam_mots_sombre redteam_onb_sorties redteam_onb_mots redteam_onboarding_texte redteam_echelle_onboarding redteam_transitions_onb redteam_onb_rejeu redteam_onboarding redteam_verrou_onboarding redteam_ordre_guide redteam_emoji redteam_tenir redteam_validation redteam_tenir_e3 redteam_engagement redteam_registre redteam_couleurs_ref redteam_decisions redteam_joignable redteam_ecrans redteam_volume; do
  t0=$(date +%s); python3 $j.py > scratchpad/v153/s-$j.txt 2>&1; rc=$?; t1=$(date +%s)
  echo "$j rc=$rc $((t1-t0))s charge=$(sysctl -n vm.loadavg | awk '{print $2}') :: $(grep -E '[0-9]+ ?/ ?[0-9]+|ROUGE|redteam_engagement :' scratchpad/v153/s-$j.txt | tail -1 | cut -c1-120)" >> scratchpad/v153/serie.txt
done
echo FINI >> scratchpad/v153/serie.txt
