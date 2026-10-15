# fin de lot v146, série C : un juge à la fois, la charge notée au départ de chacun
import subprocess, sys, time, os
J = [['redteam_ajout_personne.py'], ['redteam_tenir.py'], ['redteam_clair_sombre.py'], ['redteam_aura_latence.py'], ['redteam_trace_lettres.py'],
     ['redteam_decisions.py'], ['redteam_tonsurton.py'], ['redteam_reperage.py'], ['redteam_cercle_tom.py'], ['redteam_noms.py'], ['redteam_commentaires.py'],
     ['redteam_peaufiner.py'], ['redteam_murs.py'], ['redteam_maparole.py'], ['redteam_joignable.py'], ['redteam_ecrans.py'], ['redteam_volume.py'], ['redteam_tokens.py'],
     ['redteam_registre.py'], ['redteam_onboarding.py'], ['redteam_engagement.py'], ['redteam_gestes.py'], ['redteam_guide.py'], ['redteam_guide.py', '--cadence'],
     ['redteam_partage_toile.py', '--mondes=terrazzo'], ['redteam_fluide.py'], ['redteam_evol.py'], ['redteam_pleine.py'], ['redteam_rythme.py'], ['banc_rendu.py']]
R = open('scratchpad/v146/juges/_resume_d.txt', 'a')
for j in J:
    nom = ' '.join(j); t0 = time.time(); log = 'scratchpad/v146/juges/d-%s.log' % nom.replace('.py', '').replace(' --', '-').replace(' ', '')
    w0 = time.time()
    while os.getloadavg()[0] > 10 and time.time() - w0 < 1200: time.sleep(30)
    charge = os.getloadavg()[0]
    try:
        with open(log, 'w') as f: rc = subprocess.run([sys.executable] + j, stdout=f, stderr=subprocess.STDOUT, timeout=2700).returncode
    except subprocess.TimeoutExpired: rc = 'DÉLAI'
    der = [l.strip() for l in open(log, encoding='utf-8', errors='replace') if l.strip()][-1:] or ['']
    R.write('%s → %s · %s · %.0f s · charge au départ %.1f\n' % (nom, rc, der[0][:150], time.time() - t0, charge)); R.flush()
