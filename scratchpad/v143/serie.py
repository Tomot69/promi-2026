import subprocess, time, re, sys
L = [l.split('|') for l in """redteam_ritournelle.py|900
redteam_barre.py|1500
redteam_trait.py|900
redteam_partage_toile.py|1500
redteam_guide.py|1800
redteam_trace.py|900
redteam_engagement.py|1500
redteam_onb_sorties.py|900
redteam_verrou_onboarding.py|600
redteam_decisions.py|900
redteam_joignable.py|900
redteam_ecrans.py|1500
redteam_volume.py|300
redteam_registre.py|120
redteam_tokens.py|120
redteam_lexique.py|1500
redteam_accueil.py|900
redteam_zoom.py|900
redteam_toucher.py|1500
redteam_deplace.py|1500
redteam_cercle_tom.py|900
redteam_studio_tom.py|900
redteam_murs.py|900
redteam_nuee_dalle.py|900
redteam_bouton.py|1500
redteam_vide.py|1200
redteam_flash.py|1500
redteam_air.py|1500
redteam_decoupe.py|1500
redteam_partage_fiche.py|1500
redteam_partage_dessin.py|1500
redteam_cadre.py|900
redteam_phrase_fiche.py|900
redteam_reactif.py|900
redteam_enfonce.py|900
releve-aura.py|1500
redteam_corps.py --n=20|1800
banc_rendu.py|2400
redteam_rythme.py|1500
redteam_fluide.py|900
redteam_pelote_doigt.py|900
redteam_gestes.py|2700
redteam_couleurs_ref.py|2400""".split('\n')]
if len(sys.argv) > 1: L = [x for x in L if any(a in x[0] for a in sys.argv[1:])]
for cmd, to in L:
    t0 = time.time()
    try:
        r = subprocess.run(['python3'] + cmd.split(), capture_output=True, text=True, timeout=int(to)); out = (r.stdout or '') + (r.stderr or ''); code = r.returncode
    except subprocess.TimeoutExpired as e:
        out = 'TEMPS DÉPASSÉ'; code = 'T'
    open('scratchpad/v143/serie-%s.log' % cmd.split()[0], 'w').write(out)
    lignes = [l for l in out.strip().split('\n') if l.strip()]
    print('== %s [%s] %ds : %s' % (cmd, code, time.time() - t0, ' | '.join(l.strip()[:110] for l in lignes[-2:])), flush=True)
    for x in [l.strip()[:230] for l in lignes if re.match(r'\s*(KO|❌|✗)', l)][:7]: print('     ' + x, flush=True)
print('FIN DE SÉRIE', flush=True)
