import subprocess, re, time
B=['redteam', 'redteam2', 'redteam3', 'redteam_accueil', 'redteam_air', 'redteam_apercus', 'redteam_aveugle', 'redteam_cercle_couleur', 'redteam_champ', 'redteam_champs', 'redteam_dalle_figee', 'redteam_decoupe', 'redteam_demande', 'redteam_ecrans', 'redteam_enchaine', 'redteam_filets', 'redteam_fonctions', 'redteam_formes', 'redteam_gens', 'redteam_geste', 'redteam_nuee', 'redteam_nuee_dalle', 'redteam_nuee_entree', 'redteam_onboarding', 'redteam_pastilles', 'redteam_pelote_partage', 'redteam_photo', 'redteam_phrase', 'redteam_polices', 'redteam_reperage', 'redteam_studio_geste', 'redteam_superpo', 'redteam_toile', 'redteam_tokens', 'redteam_tonsurton', 'redteam_tuiles', 'redteam_verbe', 'redteam_vide', 'redteam_zoom', 'releve-design', 'releve-aura', 'releve-S4-index-fil']
for b in B:
    t=time.time()
    try:
        r=subprocess.run(['python3',b+'.py'],capture_output=True,text=True,timeout=1200)
        L=[l for l in (r.stdout+r.stderr).splitlines() if l.strip()]
        ko=[l for l in L if re.search(r'\bKO\b|✗|❌|DEBORDE|ÉCART|Traceback|Error',l)]
        print('===',b,'(%.0f s)'%(time.time()-t)); print('\n'.join(ko[-15:])); print('  →',L[-1] if L else '(rien)', flush=True)
    except subprocess.TimeoutExpired:
        print('===',b,'→ BLOQUÉ (20 min)', flush=True); subprocess.run(['pkill','-f','chrome-headless-shell'])
print('FIN SÉRIE', flush=True)
