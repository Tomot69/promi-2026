import subprocess, sys, time, os
R='/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026'
BATS=[['redteam_registre.py'],['redteam_tokens.py'],['redteam_volume.py'],['redteam_decisions.py'],['redteam_joignable.py'],['redteam_ecrans.py'],['redteam_onboarding.py'],['redteam_studio_geste.py'],
 ['redteam_pelote_doigt.py'],['redteam_halo.py'],['redteam_plein.py'],['redteam_contour.py'],['redteam_souffle.py'],['redteam_corps.py','--n=20'],['redteam_zone.py','--n=12'],['redteam_mesure.py'],['redteam_bouton.py','--n=20'],
 ['releve-aura.py'],['redteam_flash.py'],['redteam_vide.py'],['redteam_toile.py'],['redteam_geste.py'],['redteam_accueil.py'],['redteam_apercus.py'],['redteam_ramage_onde.py'],['banc_rendu.py'],['redteam_rythme.py','--sans-reel'],['releve-design.py'],['redteam_couleurs_ref.py']]
for c in BATS:
    f=c[0]
    if not os.path.exists(R+'/'+f): print('    —   %-26s absent'%f, flush=True); continue
    t=time.time()
    try:
        p=subprocess.run([sys.executable]+c,cwd=R,capture_output=True,text=True,timeout=3000); out=(p.stdout or '')+(p.stderr or '')
    except subprocess.TimeoutExpired: out='(dépassement de 50 min)'
    except Exception as e: out=str(e)
    open(R+'/scratchpad/v126/serie-'+f+'.txt','w').write(out)
    L=[l for l in out.strip().split('\n') if l.strip()]
    print('%5ds  %-26s %s'%(time.time()-t,f,' / '.join(L[-2:])[:180]),flush=True)
