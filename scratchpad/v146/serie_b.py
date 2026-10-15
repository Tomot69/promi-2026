# la série de fin de lot v146 : un juge à la fois, une limite de temps chacun, la dernière ligne de chacun dans _resume_b.txt
import subprocess, sys, time, os
J = ['redteam_registre.py', 'redteam_tokens.py', 'redteam_decisions.py', 'redteam_volume.py', 'redteam_joignable.py', 'redteam_ecrans.py', 'redteam_maparole.py', 'redteam_murs.py',
     'redteam_flash_etat.py', 'redteam_engagement.py', 'redteam_verrou_onboarding.py', 'redteam_onboarding.py', 'redteam_gestes.py', 'redteam_trait.py', 'redteam_toucher.py',
     'redteam_deplace.py', 'redteam_accueil.py', 'redteam_barre.py', 'redteam_partage_toile.py', 'redteam_partage_fiche.py', 'redteam_vide.py', 'redteam_champ.py', 'redteam_tonsurton.py',
     'redteam_phrase_fiche.py', 'redteam_lexique.py', 'redteam_polices.py', 'redteam_filets.py', 'redteam_clavier.py', 'redteam_gens.py', 'redteam_ajouter.py', 'redteam_cercle_tom.py',
     'redteam_nuee_dalle.py', 'redteam_nuee.py', 'redteam_air.py', 'redteam_couleurs_ref.py', 'redteam_fluide.py', 'redteam_pleine.py', 'redteam_evol.py', 'redteam_rythme.py', 'banc_rendu.py']
os.makedirs('scratchpad/v146/juges', exist_ok=True)
R = open('scratchpad/v146/juges/_resume_b.txt', 'a')
for j in J:
    if not os.path.exists(j): R.write('%s → absent\n' % j); R.flush(); continue
    t0 = time.time(); log = 'scratchpad/v146/juges/b-%s.log' % j.replace('.py', '')
    try:
        with open(log, 'w') as f: rc = subprocess.run([sys.executable, j], stdout=f, stderr=subprocess.STDOUT, timeout=2400).returncode
    except subprocess.TimeoutExpired: rc = 'DÉLAI'
    der = [l.strip() for l in open(log, encoding='utf-8', errors='replace') if l.strip()][-1:] or ['']
    R.write('%s → %s · %s · %.0f s\n' % (j, rc, der[0][:140], time.time() - t0)); R.flush()
