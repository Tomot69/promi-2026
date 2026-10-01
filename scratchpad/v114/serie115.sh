cd "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
: > scratchpad/v114/serie115.txt
for b in redteam_tokens.py redteam_volume.py redteam_clavier.py redteam_pilules.py redteam_suggestions.py redteam_couronne.py releve-design.py redteam_filets.py redteam_vide.py redteam_flash.py redteam_champ.py redteam_tonsurton.py redteam_decoupe.py redteam_verbe.py redteam_tuiles.py redteam_gens.py releve-S3-plus.py redteam_air.py; do
  [ -f "$b" ] || { echo "=== $b (absent)" >> scratchpad/v114/serie115.txt; continue; }
  echo "=== $b" >> scratchpad/v114/serie115.txt
  python3 -c "import subprocess
try: r=subprocess.run(['python3','$b'],capture_output=True,text=True,timeout=1500); print('\n'.join((r.stdout+r.stderr).strip().splitlines()[-7:]))
except subprocess.TimeoutExpired: print('TIMEOUT')" >> scratchpad/v114/serie115.txt 2>&1
done
echo FIN >> scratchpad/v114/serie115.txt
