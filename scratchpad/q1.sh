python3 redteam_photo.py 2>&1 | tail -4
echo "== photo sur avant-v117b (preuve du contrat réécrit)"; cp sauvegardes/app-avant-v117b.html zz-b.html; sed "s#8752/app.html#8752/zz-b.html#" redteam_photo.py > zz_photo.py; python3 zz_photo.py 2>&1 | tail -5; rm -f zz_photo.py zz-b.html
echo "== souffle seul"; python3 redteam_souffle.py 2>&1 | tail -5
echo "== photo_menu seul"; python3 redteam_photo_menu.py 2>&1 | tail -3
echo "== murs seul"; python3 redteam_murs.py 2>&1 | grep -v "✅" | tail -5
