cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
for j in releve-S1-fiches.py releve-S4-index-fil.py releve-S5-instant.py redteam_apercus.py redteam_murs.py redteam_kaki.py releve-aura.py; do python3 $j > scratchpad/v119/tri-$j.txt 2>&1; done
echo FIN > scratchpad/v119/tri-FIN.txt
