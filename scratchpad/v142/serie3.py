import subprocess, time, re
L = [("releve-aura.py",1500),("banc_rendu.py",2400),("redteam_deplace.py",1500),("redteam_ritournelle.py",900),("redteam_guide.py",1800),("redteam_rythme.py --app=zz-av142.html --mondes=brouillamini,terrazzo,encre,chamade,sillons",900),("redteam_rythme.py --mondes=brouillamini,terrazzo,encre,chamade,sillons",900),("redteam_corps.py --n=20",1800),("redteam_kaki.py",900)]
for cmd, to in L:
    t0 = time.time()
    try:
        r = subprocess.run(['python3'] + cmd.split(), capture_output=True, text=True, timeout=to); out = (r.stdout or '') + (r.stderr or ''); code = r.returncode
    except subprocess.TimeoutExpired as e:
        out = 'TEMPS DÉPASSÉ'; code = 'T'
    open('scratchpad/v142/serie3-%s.log' % re.sub(r'[^a-z0-9_.-]', '_', cmd)[:60], 'w').write(out)
    lignes = [l for l in out.strip().split('\n') if l.strip()]
    print('== %s [%s] %ds : %s' % (cmd, code, time.time() - t0, ' | '.join(l.strip()[:110] for l in lignes[-2:])), flush=True)
    for x in [l.strip()[:230] for l in lignes if re.match(r'\s*(KO|❌|✗)', l) or 'illisible' in l or 'se noient' in l][:9]: print('     ' + x, flush=True)
print('FIN DE SÉRIE', flush=True)
