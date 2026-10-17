import subprocess, sys, time, io, os
os.chdir('/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026')
L = sys.argv[1:]
def charge(): return float(os.popen('sysctl -n vm.loadavg').read().split()[1])
for f in L:
    c0 = charge(); t0 = time.time()
    try: r = subprocess.run([sys.executable] + f.split(), capture_output=True, text=True, timeout=3000); out = r.stdout + r.stderr; code = r.returncode
    except subprocess.TimeoutExpired as e: out = 'DÉLAI DÉPASSÉ'; code = -9
    nom = f.split()[0]
    io.open('scratchpad/v148/serie/rejoue-%s.log' % nom, 'w', encoding='utf-8').write(out)
    fin = [l for l in out.strip().splitlines() if l.strip()][-1:] or ['']
    io.open('scratchpad/v148/rejoue.txt', 'a', encoding='utf-8').write('%-34s code %3d · %5.0f s · charge %.1f→%.1f · %s\n' % (f[:34], code, time.time() - t0, c0, charge(), fin[0].strip()[:160]))
io.open('scratchpad/v148/rejoue.txt', 'a', encoding='utf-8').write('FIN DES REPRISES\n')
