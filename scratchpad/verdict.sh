#!/bin/zsh
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
cp app.html /tmp/_app_final.html
restore() { cp /tmp/_app_final.html app.html; echo "== app.html rétabli =="; }
trap restore EXIT INT TERM
echo "########## APRÈS — le fichier livré ##########"
for b in redteam_tuiles.py redteam_zoom.py redteam_nuee.py redteam_tonsurton.py; do
  echo "--- $b"; python3 $b 2>&1 | tail -4
done
for b in releve-S1-fiches.py releve-S4-index-fil.py releve-S5-instant.py releve-design.py; do
  echo "--- $b"; python3 $b 2>&1 | tail -2
done
echo
echo "########## AVANT — sauvegardes/app-avant-CINQ-POINTS.html ##########"
cp sauvegardes/app-avant-CINQ-POINTS.html app.html
for b in redteam_tuiles.py redteam_zoom.py; do
  echo "--- $b"; python3 $b 2>&1 | tail -3
done
for b in releve-S1-fiches.py releve-S4-index-fil.py releve-S5-instant.py releve-design.py; do
  echo "--- $b"; python3 $b 2>&1 | tail -2
done
