#!/bin/zsh
# batteries EN SÉRIE (§7) — une ligne de bilan par batterie
cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
for b in releve-design.py redteam_ecrans.py redteam.py redteam2.py redteam3.py redteam_demande.py redteam_toile.py redteam_geste.py redteam_verbe.py redteam_filets.py redteam_vide.py redteam_air.py redteam_champ.py redteam_pastilles.py redteam_phrase.py redteam_gens.py redteam_tuiles.py redteam_dalle_figee.py releve-S4-index-fil.py redteam_nuee.py redteam_aveugle.py redteam_reperage.py redteam_nuee_entree.py redteam_accueil.py redteam_zoom.py releve-S2-peaufiner.py redteam_cercle_couleur.py redteam_nuee_dalle.py; do
  python3 $b > scratchpad/_serie_$b.txt 2>&1
  echo "== $b (code $?)"; tail -3 scratchpad/_serie_$b.txt
done
