#!/bin/zsh
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
cp app.html /tmp/_app_apres.html
restore() { cp /tmp/_app_apres.html app.html; echo "== app.html rétabli =="; }
trap restore EXIT INT TERM
echo "=== APRÈS (fichier courant) ==="
python3 redteam_air.py 2>&1 | tail -6
python3 redteam_gens.py 2>&1 | tail -6
echo
echo "=== AVANT (sauvegardes/app-avant-CINQ-POINTS.html) ==="
cp sauvegardes/app-avant-CINQ-POINTS.html app.html
python3 redteam_gens.py 2>&1 | tail -6
