import subprocess, sys, time
J=sys.argv[1:]
out=open(''+(sys.argv[0].endswith('b.py') and 'scratchpad/serie117b.txt' or 'scratchpad/serie117.txt')+'','a')
for j in J:
    t=time.time(); a=j.split()
    try: r=subprocess.run(['python3']+a,capture_output=True,text=True,timeout=1500); o=(r.stdout+r.stderr)
    except subprocess.TimeoutExpired: o='TIMEOUT'
    out.write('=== %s (%.0f s)\n%s\n'%(j,time.time()-t,'\n'.join(o.strip().splitlines()[-6:]))); out.flush()
