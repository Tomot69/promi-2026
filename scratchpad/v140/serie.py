import subprocess, sys, time, io, re
L = [l.strip() for l in io.open(sys.argv[1], encoding='utf-8').read().split('\n') if l.strip() and not l.startswith('#')]
out = io.open(sys.argv[2], 'a', encoding='utf-8')
for cmd in L:
    t0 = time.time(); nom = cmd.split()[0]
    try:
        r = subprocess.run(['python3'] + cmd.split(), capture_output=True, text=True, timeout=2400); rc = r.returncode; txt = (r.stdout or '') + (r.stderr or '')
    except subprocess.TimeoutExpired as e:
        rc = -9; txt = (e.stdout or b'').decode('utf-8', 'ignore') if isinstance(e.stdout, bytes) else (e.stdout or ''); txt += '\nDÉLAI DÉPASSÉ'
    io.open('scratchpad/v140/serie-%s.txt' % re.sub(r'[^A-Za-z0-9_.-]', '_', cmd), 'w', encoding='utf-8').write(txt)
    fin = [x for x in txt.strip().split('\n') if x.strip()][-1:] or ['']
    out.write('%s | rc %d | %d s | %s\n' % (cmd, rc, time.time() - t0, fin[0][:160])); out.flush()
out.write('FIN\n'); out.close()
