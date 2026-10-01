echo "== S1 avant v117"; APP_S1="$PWD/zz-avant117.html" python3 releve-S1-fiches.py 2>&1 | tail -2
echo "== S1 v117"; python3 releve-S1-fiches.py 2>&1 | grep "✗" | cut -c1-140
echo "== aura avant v117"; APP_AURA=http://127.0.0.1:8752/zz-avant117.html python3 releve-aura.py 2>&1 | tail -1
echo "== marges seul"; python3 redteam_marges.py 2>&1 | tail -4
