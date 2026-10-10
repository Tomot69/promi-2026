import subprocess, sys, time, os, json
R='/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026'
BATS=json.loads(sys.argv[1]); nom=sys.argv[2]
log=open(R+'/scratchpad/v139/'+nom+'.log','w')
for c in BATS:
    f=c[0]; t=time.time()
    try:
        p=subprocess.run([sys.executable]+c,cwd=R,capture_output=True,text=True,timeout=3000); out=(p.stdout or '')+(p.stderr or '')
    except subprocess.TimeoutExpired: out='(dépassement de 50 min)'
    except Exception as e: out=str(e)
    open(R+'/scratchpad/v139/serie-'+f+'.txt','w').write(out)
    L=[l for l in out.strip().split('\n') if l.strip()]
    log.write('%5ds  %-28s %s\n'%(time.time()-t,' '.join(c),' / '.join(L[-2:])[:200])); log.flush()
log.write('FIN\n'); log.close()
