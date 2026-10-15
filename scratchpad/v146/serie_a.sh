#!/bin/bash
# juges touchés par §1, §5–§8 — en série, un par un
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
mkdir -p scratchpad/v146/juges
for j in redteam_decisions redteam_tonsurton redteam_champ redteam_vide redteam_ecrans redteam_phrase_fiche redteam_commentaires redteam_part redteam_motmarque redteam_flash_etat redteam_murs redteam_maparole redteam_accueil redteam_barre redteam_joignable redteam_volume redteam_tokens redteam_lexique redteam_polices redteam_filets redteam_trait redteam_gestes; do
  ( python3 $j.py > scratchpad/v146/juges/$j.log 2>&1; echo "$j → $(tail -4 scratchpad/v146/juges/$j.log | grep -v '^KO' | grep -v '^$' | tail -1 | cut -c1-110)" >> scratchpad/v146/juges/_resume.txt )
done
echo FIN >> scratchpad/v146/juges/_resume.txt
