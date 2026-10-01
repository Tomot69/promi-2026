#!/bin/zsh
# usage : v102_air.sh "écran1|écran2"  → paires resserrées (encre) contre la référence d'avant v96, thème sombre
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
sed -e "s|for d, e, a, b, av, ap in perdu\[:40\]:|for d, e, a, b, av, ap in perdu:|" -e "s|if '--figer' in sys.argv:|if False:|" redteam_air.py > v102_air_liste.py
AIR_ECRANS="$1" REF_AIR="sauvegardes/air-encre-avant-v96.json" python3 v102_air_liste.py 2>&1 | grep "^   −\|INTACT" | grep -v "\[light\]" | cut -c1-165
rm -f v102_air_liste.py
