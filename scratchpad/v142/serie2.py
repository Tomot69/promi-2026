import subprocess, time, re
L = [("redteam_rythme.py",1500),("redteam_toucher.py",1500),("redteam_nuee_dalle.py",900),("redteam_vide.py",1200),("redteam_bouton.py",1500),("releve-aura.py",1500),("redteam_guide.py",1800),("redteam_gestes.py --seul=tenir",900),("redteam_air.py",1500)]
for cmd, to in L:
    t0 = time.time()
    try:
        r = subprocess.run(['python3'] + cmd.split(), capture_output=True, text=True, timeout=to); out = (r.stdout or '') + (r.stderr or ''); code = r.returncode
    except subprocess.TimeoutExpired as e:
        out = 'TEMPS DÉPASSÉ'; code = 'T'
    open('scratchpad/v142/serie2-%s.log' % cmd.split()[0], 'w').write(out)
    lignes = [l for l in out.strip().split('\n') if l.strip()]
    print('== %s [%s] %ds : %s' % (cmd, code, time.time() - t0, ' | '.join(l.strip()[:110] for l in lignes[-2:])), flush=True)
    for x in [l.strip()[:230] for l in lignes if re.match(r'\s*(KO|❌|✗)', l)][:8]: print('     ' + x, flush=True)
print('FIN DE SÉRIE', flush=True)
