# v151 — LA SÉRIE COMPLÈTE (clôture de la série), un juge à la fois, la charge relevée avant et après chacun. redteam_air en dernier.
import subprocess, sys, time, io, os, glob
os.chdir('/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026')
LONG = {'redteam_vivant.py': 4800, 'redteam_corps.py': 2700, 'redteam_marges.py': 2400, 'redteam_couleurs_ref.py': 2700, 'redteam_ecrans.py': 2700, 'redteam_air.py': 2700,
        'banc_rendu.py': 2700, 'redteam_ritournelle.py': 2700, 'redteam_deplace.py': 2700, 'redteam_partage_toile.py': 2700, 'redteam_toucher.py': 2400, 'redteam_fiches_theme.py': 2400,
        'redteam_part.py': 2400, 'redteam_guide.py': 2400, 'redteam_retour.py': 1800, 'redteam_engagement.py': 2400, 'redteam_evol.py': 2400, 'redteam_pleine.py': 2400, 'redteam_rythme.py': 1800,
        'redteam_pages_plus.py': 2400}
PREMIERS = ['redteam_registre.py', 'redteam_volume.py', 'redteam_tokens.py', 'redteam_echeance.py', 'redteam_onb_rejeu.py', 'redteam_ruban.py', 'redteam_garder.py', 'redteam_pages_plus.py',
            'redteam_onb_mots.py', 'redteam_maparole.py', 'redteam_couleurs_ref.py', 'redteam_decisions.py', 'redteam_joignable.py', 'redteam_ecrans.py', 'redteam_engagement.py']
DERNIERS = ['redteam_air.py']
tous = sorted(glob.glob('redteam*.py')) + sorted(glob.glob('releve-*.py')) + ['banc_rendu.py']
L = [f for f in PREMIERS if f in tous] + [f for f in tous if f not in PREMIERS and f not in DERNIERS] + DERNIERS
B = 'scratchpad/v151/serie.txt'
def charge(): return float(os.popen('sysctl -n vm.loadavg').read().split()[1])
io.open(B, 'a', encoding='utf-8').write('DÉBUT %s · %d juges\n' % (time.strftime('%H:%M'), len(L)))
for f in L:
    c0 = charge(); t0 = time.time()
    try: r = subprocess.run([sys.executable, f], capture_output=True, text=True, timeout=LONG.get(f, 1500)); out = r.stdout + r.stderr; code = r.returncode
    except subprocess.TimeoutExpired as e: out = (e.stdout.decode('utf-8', 'ignore') if isinstance(e.stdout, bytes) else (e.stdout or '')) + '\nDÉLAI DÉPASSÉ'; code = -9
    io.open('scratchpad/v151/serie/%s.log' % f, 'w', encoding='utf-8').write(out)
    fin = [l for l in out.strip().splitlines() if l.strip()][-1:] or ['']
    io.open(B, 'a', encoding='utf-8').write('%-34s code %3d · %5.0f s · charge %.1f→%.1f · %s\n' % (f, code, time.time() - t0, c0, charge(), fin[0].strip()[:160]))
io.open(B, 'a', encoding='utf-8').write('FIN DE LA SÉRIE %s\n' % time.strftime('%H:%M'))
