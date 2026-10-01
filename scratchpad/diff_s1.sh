#!/bin/zsh
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
cp app.html /tmp/_app_final2.html
restore() { cp /tmp/_app_final2.html app.html; echo "== app.html rétabli =="; }
trap restore EXIT INT TERM
python3 redteam_tonsurton.py 2>&1 | tail -6 > /tmp/_tst.txt
python3 releve-S1-fiches.py 2>&1 | grep '✗' | sort > /tmp/_s1_apres.txt
cp sauvegardes/app-avant-CINQ-POINTS.html app.html
python3 releve-S1-fiches.py 2>&1 | grep '✗' | sort > /tmp/_s1_avant.txt
restore; trap - EXIT
echo "=== tonsurton, repassé seul ==="; cat /tmp/_tst.txt
echo; echo "=== releve-S1 : ce que MON lot ajoute ==="
comm -13 /tmp/_s1_avant.txt /tmp/_s1_apres.txt | head -10
echo "=== et ce qu'il retire ==="
comm -23 /tmp/_s1_avant.txt /tmp/_s1_apres.txt | head -10
echo "(avant $(wc -l < /tmp/_s1_avant.txt) · après $(wc -l < /tmp/_s1_apres.txt))"
