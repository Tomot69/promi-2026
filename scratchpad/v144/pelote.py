# la Pelote sous le doigt — banc WebKit, vrai toucher (rayon de contact), images et rappels chronométrés
import sys, json, collections; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'; N=int(sys.argv[2]) if len(sys.argv)>2 else 2; DEMO='--demo' in sys.argv
PROF=open('scratchpad/v143/profil.py',encoding='utf-8').read().split('PROF = r"""')[1].split('"""')[0]
with sync_playwright() as p:
    b=p.webkit.launch(); A=collections.defaultdict(lambda:[0,0,0])
    for k in range(N):
        ctx=B.contexte(b)
        if DEMO: ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return true},configurable:true});}catch(e){}")
        ctx.add_init_script(PROF); pg=B.ouvre(ctx,F)
        pg.evaluate("()=>{closeAll();document.getElementById('souffleBtn').click()}"); pg.wait_for_timeout(5000)
        bo=pg.evaluate("()=>{const r=document.querySelector('#auraScreen .au-bo').getBoundingClientRect(); return [r.left,r.top,r.width,r.height]}")
        cx,cy=bo[0]+bo[2]/2,bo[1]+bo[3]/2
        for nom,pts,pas,tenue in [('caresse lente',[[cx-50+i*1.6,cy-10+(i%9)] for i in range(70)],33,0),('caresse vive',[[cx-60+i*4,cy+20-i*1.2] for i in range(30)],16,0),('appui',[[cx,cy]]*40,33,0),('lancer',[[cx-70+i*14,cy] for i in range(10)],16,0)]:
            pg.evaluate("()=>{ window.__Pon(true); window.__t0=performance.now(); }")
            B.glisse(pg,pts,pas=pas,tenue=tenue,appareil=False,rx=11,ry=9)
            r1=pg.evaluate("()=>({t0:window.__t0,t1:performance.now(),F:window.__F.slice(),P:window.__P.slice()})")
            pg.wait_for_timeout(1500)
            r2=pg.evaluate("()=>({t1:performance.now(),F:window.__F.slice(),P:window.__P.slice(),n:(window._aura&&_aura.palier&&_aura.palier())||0})")
            def stat(F,a,z):
                T=[F[i+1]-F[i] for i in range(len(F)-1) if a<=F[i]<=z]; T.sort()
                if not T: return 'aucune image'
                q=lambda x:T[min(len(T)-1,int(len(T)*x))]
                return 'p50 %.0f p95 %.0f max %.0f · %d images · %d au-delà de 20 ms'%(q(.5),q(.95),T[-1],len(T),sum(1 for t in T if t>20))
            print('%-10s passe %d · %-14s | sous le doigt : %s | 1,5 s après : %s'%(F,k,nom,stat(r1['F'],r1['t0'],r1['t1']),stat(r2['F'],r1['t1'],r2['t1'])),flush=True)
            for t,d,n in r2['P']:
                x=A[(nom,n)]; x[0]+=d; x[1]+=1; x[2]=max(x[2],d)
        ctx.close()
    b.close()
print('\nrappels les plus coûteux (ms cumulés par passe · appels · pire)')
for (nom,n),x in sorted(A.items(),key=lambda kv:-kv[1][0])[:14]: print('%-14s %7.1f %5.1f %6.1f  %s'%(nom,x[0]/N,x[1]/N,x[2],n[:150]))
