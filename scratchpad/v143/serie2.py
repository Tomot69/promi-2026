import subprocess, time, re, sys
L = [("redteam_barre.py",1500),("redteam_guide.py",1800),("redteam_trace.py",900),("redteam_air.py",1500),("redteam_rythme.py --mondes=halin,encre,brouillamini",900),("redteam_gestes.py",2700),("redteam_accueil.py",900),("redteam_joignable.py",900),("redteam_ecrans.py",1500),("redteam_engagement.py",1500),("redteam_cadre.py",900),("redteam_studio_mur.py",900),("redteam_murs_toucher.py",1200)]
if len(sys.argv) > 1: L = [x for x in L if any(a in x[0] for a in sys.argv[1:])]
for cmd, to in L:
    t0 = time.time()
    try:
        r = subprocess.run(['python3'] + cmd.split(), capture_output=True, text=True, timeout=int(to)); out = (r.stdout or '') + (r.stderr or ''); code = r.returncode
    except subprocess.TimeoutExpired as e:
        out = 'TEMPS DÉPASSÉ'; code = 'T'
    open('scratchpad/v143/serie2-%s.log' % cmd.split()[0], 'w').write(out)
    lignes = [l for l in out.strip().split('\n') if l.strip()]
    print('== %s [%s] %ds : %s' % (cmd, code, time.time() - t0, ' | '.join(l.strip()[:110] for l in lignes[-2:])), flush=True)
    for x in [l.strip()[:230] for l in lignes if re.match(r'\s*(KO|❌|✗)', l)][:7]: print('     ' + x, flush=True)
print('FIN DE SÉRIE', flush=True)
