import subprocess, sys, time, os
R='/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026'
BATS=[['redteam_registre.py'],['redteam_tokens.py'],['redteam_volume.py'],['redteam_reactif.py'],['redteam_entier.py'],['redteam_decisions.py'],['redteam_flash_etat.py'],['redteam_murs.py'],['redteam_maparole.py'],['redteam_tonsurton.py'],['redteam_decoupe.py'],['redteam_zone.py','app.html','--n=12'],['releve-aura.py'],['redteam_photo.py'],['redteam_photo_menu.py'],['redteam_partage_fiche.py'],['redteam_joignable.py'],['redteam_ecrans.py'],['redteam_vide.py'],['redteam_flash.py'],['redteam_champ.py'],['redteam_gens.py'],['redteam_couleurs_ref.py']]
for c in BATS:
    f=c[0]
    if not os.path.exists(R+'/'+f): print('    —   %-26s absent'%f, flush=True); continue
    t=time.time()
    try:
        p=subprocess.run([sys.executable]+c,cwd=R,capture_output=True,text=True,timeout=3000); out=(p.stdout or '')+(p.stderr or '')
    except subprocess.TimeoutExpired: out='(dépassement de 50 min)'
    except Exception as e: out=str(e)
    open(R+'/scratchpad/v131/serie-'+f+'.txt','w').write(out)
    L=[l for l in out.strip().split('\n') if l.strip()]
    print('%5ds  %-26s %s'%(time.time()-t,f,' / '.join(L[-2:])[:180]),flush=True)
