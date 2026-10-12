# la Toile quand une dalle apparaît ou disparaît — banc_tom (WebKit, 390 × 844, @3x), images et rappels chronométrés
import sys, json, collections; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
MONDES=(sys.argv[2] if len(sys.argv)>2 else 'encre,touffe,mosaique,ritournelle,brouillamini').split(',')
NB=int(sys.argv[3]) if len(sys.argv)>3 else 3
PROF=open('scratchpad/v143/profil.py',encoding='utf-8').read().split('PROF = r"""')[1].split('"""')[0]
def stat(F,a,z):
    I=[(round(F[i]-a),round(F[i+1]-F[i],1)) for i in range(len(F)-1) if a<=F[i]<=z]
    L=[x for x in I if x[1]>20]
    return '%3d images · %2d au-delà de 20 ms · pire %5.0f ms · somme des dépassements %4.0f ms'%(len(I),len(L),max([x[1] for x in I] or [0]),sum(x[1]-16.7 for x in L)), L
res={}
with sync_playwright() as p:
    b=p.webkit.launch()
    for m in MONDES:
        ctx=B.contexte(b); ctx.add_init_script(PROF); pg=B.ouvre(ctx,F)
        pg.evaluate("m=>{ try{ Toile.setTheme(m); }catch(e){} }",m); pg.wait_for_timeout(1500)
        for i in range(NB): B.plante(pg,['rendre le livre','écrire à Lou','arroser le ficus','appeler Mamie','ranger le garage','finir le puzzle'][i])
        pg.wait_for_timeout(3200)
        # planter, mesuré
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{document.getElementById('fTitle').value='courir dimanche';document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null}")
        pg.wait_for_timeout(3200)
        pg.evaluate("()=>{ window.__Pon(true); window.__t0=performance.now(); document.getElementById('addPromi').click(); }"); pg.wait_for_timeout(4000)
        r=pg.evaluate("()=>({t0:window.__t0,F:window.__F.slice(),P:window.__P.slice(),n:promises.length})")
        s,L=stat(r['F'],r['t0'],r['t0']+3500); print('%-12s %-13s planter  %s'%(F,m,s),L[:8],flush=True)
        P1=[(e[0]-r['t0'],e[1],e[2]) for e in r['P'] if e[0]-r['t0']<3500]
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(3500)
        # retirer, mesuré
        pg.evaluate("()=>{ window._v16SupprimerPromi(promises[promises.length-1]); }"); pg.wait_for_timeout(900)
        pg.evaluate("()=>{ window.__Pon(true); window.__t0=performance.now(); }"); B.tap_sel(pg,'.v16-oui'); pg.wait_for_timeout(4000)
        r2=pg.evaluate("()=>({t0:window.__t0,F:window.__F.slice(),P:window.__P.slice(),n:promises.length})")
        s2,L2=stat(r2['F'],r2['t0'],r2['t0']+3500); print('%-12s %-13s retirer  %s'%(F,m,s2),L2[:8],'(%d → %d paroles)'%(r['n'],r2['n']),flush=True)
        P2=[(e[0]-r2['t0'],e[1],e[2]) for e in r2['P'] if e[0]-r2['t0']<3500]
        res[m]=(P1,P2)
        if '--detail' in sys.argv:
            for t,d,n in P1:
                if 600<=t<=1500 and d>=3: print('        %5.0f ms  %5.1f  %s'%(t,d,n[:110]))
        for nom,P in (('planter',P1),('retirer',P2)):
            A=collections.defaultdict(lambda:[0,0,0,[]])
            for t,d,n in P:
                x=A[n]; x[0]+=d; x[1]+=1; x[2]=max(x[2],d); x[3].append(round(t))
            for n,x in sorted(A.items(),key=lambda kv:-kv[1][2])[:6]:
                if x[2]>=8: print('      %s · pire %5.1f ms · %2d appels · %5.0f ms en tout · à %s · %s'%(nom,x[2],x[1],x[0],x[3][:4],n[:130]))
        ctx.close()
    b.close()
