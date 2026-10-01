import subprocess,sys,time
for b in sys.argv[1:]:
    t=time.time()
    try: r=subprocess.run(['python3',b+'.py'],capture_output=True,text=True,timeout=1500); out=r.stdout+r.stderr
    except subprocess.TimeoutExpired as e: out=(e.stdout or b'').decode() if isinstance(e.stdout,bytes) else (e.stdout or '')+'\nTIMEOUT'
    open('scratchpad/v106/'+b+'.txt','w').write(out)
    open('scratchpad/v106/_resume.txt','a').write('%s (%.0fs) :: %s\n'%(b,time.time()-t,' | '.join(out.strip().split('\n')[-3:])))
open('scratchpad/v106/_resume.txt','a').write('FIN\n')
