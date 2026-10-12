import subprocess, sys, time, io
L=[('redteam_registre.py',[],120),('redteam_volume.py',[],120),('redteam_tokens.py',[],120),('redteam_evol.py',[],1500),('redteam_fluide.py',[],900),('redteam_gestes.py',[],900),('redteam_trait.py',[],900),('redteam_onb_sorties.py',[],900),('redteam_engagement.py',[],1500),('redteam_verrou_onboarding.py',[],900),
   ('redteam_trace.py',[],900),('redteam_enfonce.py',[],900),('redteam_pelote_doigt.py',[],900),('redteam_ritournelle.py',[],1500),('redteam_guide.py',[],1800),('redteam_deplace.py',['--mondes=pochade,ritournelle'],1500),('redteam_toucher.py',[],1800),('redteam_accueil.py',[],900),
   ('redteam_vide.py',[],1500),('redteam_flash.py',[],1800),('redteam_decisions.py',[],1500),('redteam_joignable.py',[],1500),('redteam_ecrans.py',[],2400),('redteam_lexique.py',[],1800),('redteam_partage_toile.py',['--mondes=encre,ritournelle,touffe'],1500),('redteam_barre.py',['--n=20'],900),
   ('banc_rendu.py',[],2400),('redteam_rythme.py',['--sans-reel'],1500),('redteam_air.py',[],2400),('redteam_couleurs_ref.py',[],2400)]
seul=sys.argv[1:]
for f,a,t in L:
    if seul and f not in seul: continue
    t0=time.time()
    try: r=subprocess.run([sys.executable,f]+a,capture_output=True,text=True,timeout=t); out=r.stdout+r.stderr; code=r.returncode
    except subprocess.TimeoutExpired as e: out=(e.stdout or b'').decode('utf-8','ignore') if isinstance(e.stdout,bytes) else (e.stdout or ''); out+='\nDÉLAI DÉPASSÉ'; code=-9
    io.open('scratchpad/v144/serie-%s.log'%f,'w',encoding='utf-8').write(out)
    fin=[l for l in out.strip().splitlines() if l.strip()][-2:]
    print('%-32s code %2d · %4.0f s · %s'%(f,code,time.time()-t0,' | '.join(x.strip()[:150] for x in fin)),flush=True)
