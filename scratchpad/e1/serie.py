import subprocess, sys, time, os
R='/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026'
BATS=[['redteam_registre.py'],['redteam_tokens.py'],['redteam_volume.py'],['redteam_gestes.py'],['redteam_verrou_onboarding.py'],['redteam_lexique.py'],['redteam_halo.py'],['redteam_bord.py','--gl'],['redteam_zone.py','--n=12'],['redteam_contour.py'],['redteam_plein.py'],['redteam_souffle.py'],['releve-aura.py'],['redteam_flash.py'],['redteam_flash_etat.py'],['redteam_dessin.py'],['redteam_entier.py'],['redteam_partage_dessin.py'],['redteam_partage_fiche.py'],['redteam_phrase_fiche.py'],['redteam_reactif.py'],['redteam_accueil.py'],['redteam_murs.py'],['redteam_decisions.py'],['redteam_joignable.py'],['redteam_ecrans.py'],['redteam_vide.py'],['redteam_air.py'],['redteam_couleurs_ref.py']]
for c in BATS:
    f=c[0]
    if not os.path.exists(R+'/'+f): print('    —   %-26s absent'%f, flush=True); continue
    t=time.time()
    try:
        p=subprocess.run([sys.executable]+c,cwd=R,capture_output=True,text=True,timeout=3000); out=(p.stdout or '')+(p.stderr or '')
    except subprocess.TimeoutExpired: out='(dépassement de 50 min)'
    except Exception as e: out=str(e)
    open(R+'/scratchpad/e1/serie-'+f+'.txt','w').write(out)
    L=[l for l in out.strip().split('\n') if l.strip()]
    print('%5ds  %-26s %s'%(time.time()-t,f,' / '.join(L[-2:])[:180]),flush=True)
