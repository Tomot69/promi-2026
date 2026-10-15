import re, io, subprocess, sys, os, tempfile
S = io.open(sys.argv[1] if len(sys.argv) > 1 else 'app.html', encoding='utf-8').read()
bad = 0; n = 0
d = tempfile.mkdtemp()
for m in re.finditer(r'<script([^>]*)>(.*?)</script>', S, re.S):
    a, c = m.group(1), m.group(2)
    if 'src=' in a or not c.strip() or 'application/json' in a: continue
    n += 1; f = os.path.join(d, 's%d.js' % n); io.open(f, 'w', encoding='utf-8').write(c)
    r = subprocess.run(['node', '--check', f], capture_output=True, text=True)
    if r.returncode: bad += 1; print('KO', a.strip()[:60], r.stderr.strip().split('\n')[:4])
print('scripts', n, 'fautifs', bad)
