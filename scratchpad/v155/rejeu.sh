#!/bin/zsh
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
OUT=scratchpad/v155/rejeu.txt; : > $OUT
run(){ L=$(sysctl -n vm.loadavg | awk '{print $2}'); perl -e 'alarm shift; exec @ARGV' 1800 python3 "$@" > scratchpad/v155/rj.txt 2>&1; echo "$* | charge $L | KO $(grep -c '❌\|^KO\|  KO' scratchpad/v155/rj.txt) | $(grep -E '[0-9]+ */ *[0-9]+' scratchpad/v155/rj.txt | tail -1 | cut -c1-80)" >> $OUT; grep -E '❌|^KO|  KO' scratchpad/v155/rj.txt | head -4 | cut -c1-220 >> $OUT; }
run redteam_transitions_onb.py
run redteam_onboarding_texte.py
run redteam_onboarding.py
run redteam_onb_sorties.py
run redteam_pages_plus.py
run redteam_murs_toucher.py
run redteam_murs_toucher.py zz-av154.html
run redteam_contraste_trait.py --page=zz-av154.html
echo FIN >> $OUT
