# Lance des batteries EN SÉRIE (§7), 900 s au plus chacune, et GARDE LE JOURNAL COMPLET de chaque passage
# dans sauvegardes/journaux/<horodatage>-<batterie>.txt — un rouge intermittent doit pouvoir être relu.
import sys, subprocess, time, os, re
RAC=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); J=os.path.join(RAC,'sauvegardes','journaux')
for arg in sys.argv[1:]:
    parts=arg.split(); nom=re.sub(r'[^\w.-]+','_',arg)[:60]
    print('=== '+arg, flush=True)
    t0=time.time()
    try: r=subprocess.run(['python3']+parts, cwd=RAC, capture_output=True, text=True, timeout=900); out=r.stdout+r.stderr
    except subprocess.TimeoutExpired as e: out=(e.stdout or b'').decode() if isinstance(e.stdout,bytes) else (e.stdout or ''); out+='\nTIMEOUT'
    f=os.path.join(J, time.strftime('%m%d-%H%M%S')+'-'+nom+'.txt'); open(f,'w').write(out)
    for L in out.splitlines():
        if re.search(r'^\d+/\d+|KO|❌|✅|TIMEOUT|Traceback', L): print(L)
    print('    (%.0f s · journal %s)' % (time.time()-t0, os.path.basename(f)), flush=True)
