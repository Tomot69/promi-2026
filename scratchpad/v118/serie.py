import subprocess, sys, time
out = open(sys.argv[1], 'a')
for j in sys.argv[2:]:
    t = time.time(); a = j.split()
    try: r = subprocess.run(['python3'] + a, capture_output=True, text=True, timeout=1800); o = r.stdout + r.stderr; c = r.returncode
    except subprocess.TimeoutExpired: o = 'TIMEOUT'; c = -9
    out.write('=== %s  [code %s, %.0f s]\n%s\n' % (j, c, time.time() - t, '\n'.join(o.strip().splitlines()[-7:]))); out.flush()
out.write('=== FIN\n'); out.flush()
