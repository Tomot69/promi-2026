cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
for j in redteam_echelle_onboarding redteam_onb_sorties redteam_clavier_onb redteam_onboarding redteam_onboarding_texte redteam_ritournelle redteam_guide redteam_guide_studio redteam_guide_fond redteam_deplace redteam_toucher redteam_zoom redteam_accueil redteam_couleurs_ref redteam_decisions redteam_joignable redteam_ecrans redteam_volume redteam_registre redteam_decoupe redteam_flash redteam_croix; do
  echo "== $j $(sysctl -n vm.loadavg)"; python3 $j.py 2>&1 | grep "❌\|/ \|NON JUG" | tail -8 | cut -c1-330
done
echo FIN
