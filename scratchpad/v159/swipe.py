import sys, json; sys.path.insert(0,'.'); sys.argv+=['']*4
from playwright.sync_api import sync_playwright
from banc_tom import *
F = sys.argv[1] or 'app.html'; M = sys.argv[2] or 'terrazzo'; N=int(sys.argv[3] or 25)
SENS=[int(x) for x in (sys.argv[4] or '1,1,-1,-1').split(',')]
GEO = "()=>{var c=Toile_cellules();return {v:[+c.view.s.toFixed(3),+c.view.ox.toFixed(1),+c.view.oy.toFixed(1)],n:c.c.length,g:c.c.filter(s=>s.kind!=='gray').map(s=>[s.pid,+s.x.toFixed(1),+s.y.toFixed(1)]),th:Toile.getTheme()}}"
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b, stockage={'promi_monde':M}); toile_pleine(ctx, N); pg = ouvre(ctx, F)
    pg.evaluate("()=>{try{setPremium(true)}catch(e){document.getElementById('device').classList.add('premium')}}")
    pg.evaluate("m=>{if(Toile.getTheme()!==m)Toile.setTheme(m)}", M); pg.wait_for_timeout(2500)
    a = pg.evaluate(GEO); capture(pg,'scratchpad/v159/s_a.png')
    tap_sel(pg,'#studioBtn'); pg.wait_for_timeout(2600)
    seq=[]
    for sens in SENS:
        x0,x1 = (300,90) if sens>0 else (90,300)
        glisse(pg, droite([x0,420],[x1,420],10), pas=16); pg.wait_for_timeout(1800); seq.append(pg.evaluate("()=>Toile.getTheme()"))
    tap_sel(pg,'#studioScreen .closeb'); pg.wait_for_timeout(2500)
    bb = pg.evaluate(GEO); capture(pg,'scratchpad/v159/s_b.png')
    print('lecture', pg.evaluate("()=>{var l=Toile_lecture(); var c1=l.cible; window._recadreDemande=true; Toile_autoView(); return [l.vue, c1, Toile_lecture().cible, window._vueMain]}"))
    print('mondes parcourus', seq, 'fin', bb['th'])
    A={x[0]:x for x in a['g']}; B={x[0]:x for x in bb['g']}
    d=[(k,A[k][1:],B.get(k)) for k in A if k not in B or abs(A[k][1]-B[k][1])>0.5 or abs(A[k][2]-B[k][2])>0.5]
    print('vue', a['v'], bb['v'], 'cellules', a['n'], bb['n'], 'déplacées', len(d), d[:3])
    print(pg.__dict__['erreurs'][:2]); b.close()
