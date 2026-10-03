import subprocess, sys, time
R='/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026'
BATS=['redteam_tokens.py','redteam_fluide.py','redteam_bouton.py','redteam_garder_toile.py','redteam_halo.py','redteam_plein.py','redteam_contour.py','redteam_souffle.py','redteam_volume.py','redteam_corps.py','redteam_flash_etat.py','redteam_decisions.py',
 'redteam_maparole.py','redteam_murs.py','redteam_champ.py','redteam_tonsurton.py','redteam_filets.py','redteam_reperage.py','redteam_verbe.py','redteam_vide.py','redteam_flash.py','redteam_air.py','redteam_ecrans.py','redteam.py','redteam2.py','redteam3.py',
 'redteam_geste.py','redteam_fonctions.py','redteam_toile.py','redteam_joignable.py','redteam_polices.py','redteam_clavier.py','releve-S5-instant.py','releve-aura.py','releve-design.py']
import os
for f in BATS:
    if not os.path.exists(R+'/'+f): print('    —   %-26s absent'%f, flush=True); continue
    t=time.time()
    try:
        p=subprocess.run([sys.executable,f],cwd=R,capture_output=True,text=True,timeout=3000); out=(p.stdout or '')+(p.stderr or '')
    except subprocess.TimeoutExpired: out='(dépassement de 50 min)'
    except Exception as e: out=str(e)
    open(R+'/scratchpad/v124/serie-'+f+'.txt','w').write(out)
    L=[l for l in out.strip().split('\n') if l.strip()]
    print('%5ds  %-26s %s'%(time.time()-t,f,' / '.join(L[-2:])[:180]),flush=True)
