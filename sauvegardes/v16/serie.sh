cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
for b in redteam_tokens redteam_ecrans redteam_reperage redteam_tonsurton redteam_champ redteam_toile redteam_vide releve-aura redteam_air releve-design; do
  echo "=== $b $(date +%H:%M:%S)" >> sauvegardes/v16/journaux/serie6.log
  python3 $b.py > sauvegardes/v16/journaux/$b.log 2>&1
  tail -4 sauvegardes/v16/journaux/$b.log >> sauvegardes/v16/journaux/serie6.log
done
echo FIN >> sauvegardes/v16/journaux/serie6.log
