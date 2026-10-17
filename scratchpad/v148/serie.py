import subprocess, sys, time, io, os, glob, threading
os.chdir('/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026')
LONG = {'redteam_vivant.py': 4800, 'redteam_corps.py': 2700, 'redteam_marges.py': 2400, 'redteam_couleurs_ref.py': 2700, 'redteam_ecrans.py': 2700, 'redteam_air.py': 2700,
        'banc_rendu.py': 2700, 'redteam_ritournelle.py': 2700, 'redteam_deplace.py': 2700, 'redteam_partage_toile.py': 2700, 'redteam_toucher.py': 2400, 'redteam_fiches_theme.py': 2400,
        'redteam_part.py': 2400, 'redteam_guide.py': 2400, 'redteam_retour.py': 1800, 'redteam_engagement.py': 2400, 'redteam_evol.py': 2400, 'redteam_pleine.py': 2400, 'redteam_rythme.py': 1800}
PREMIERS = ['redteam_registre.py', 'redteam_volume.py', 'redteam_tokens.py', 'redteam_joignable.py', 'redteam_ecrans.py', 'redteam_ronds.py', 'redteam_ruban.py', 'redteam_tenir.py', 'redteam_garder.py',
            'redteam_engagement.py', 'redteam_verrou_onboarding.py', 'redteam_onboarding_texte.py', 'redteam_trace_lettres.py', 'redteam_sans_main.py']
FAITS = set(sys.argv[1:])   # déjà passés dans ce lot, sur l'app d'aujourd'hui — repassés à la fin
tous = sorted(glob.glob('redteam*.py')) + sorted(glob.glob('releve-*.py')) + ['banc_rendu.py']
L = [f for f in PREMIERS if f in tous] + [f for f in tous if f not in PREMIERS and f not in FAITS] + [f for f in tous if f in FAITS]
L = [f for f in L if f != 'redteam_couleurs_ref.py']   # passé à part dans ce lot
verrou = threading.Lock(); file = list(L)
def charge(): return float(os.popen('sysctl -n vm.loadavg').read().split()[1])
def un():
    while True:
        with verrou:
            if not file: return
            f = file.pop(0)
        c0 = charge(); t0 = time.time()
        try: r = subprocess.run([sys.executable, f], capture_output=True, text=True, timeout=LONG.get(f, 1500)); out = r.stdout + r.stderr; code = r.returncode
        except subprocess.TimeoutExpired as e: out = (e.stdout.decode('utf-8', 'ignore') if isinstance(e.stdout, bytes) else (e.stdout or '')) + '\nDÉLAI DÉPASSÉ'; code = -9
        io.open('scratchpad/v148/serie/%s.log' % f, 'w', encoding='utf-8').write(out)
        fin = [l for l in out.strip().splitlines() if l.strip()][-1:] or ['']
        with verrou:
            io.open('scratchpad/v148/serie.txt', 'a', encoding='utf-8').write('%-34s code %3d · %5.0f s · charge %.1f→%.1f · %s\n' % (f, code, time.time() - t0, c0, charge(), fin[0].strip()[:160]))
T = [threading.Thread(target=un) for _ in range(2)]
[t.start() for t in T]; [t.join() for t in T]
io.open('scratchpad/v148/serie.txt', 'a', encoding='utf-8').write('FIN DE LA SÉRIE\n')
