import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
REC = """()=>{ window.__R=[]; const T=window.TraceLettres, tr=T.trace; T.trace=function(c){ const ctl=tr.apply(this,arguments); const r={id:c.id, F:[], gl:null}; window.__R.push(r);
  ctl.pret.then(()=>{ r.gl=(ctl.glyphes||[]).map(g=>[g.car,g.x,g.variante]); (function f(){ if(ctl.fini) return; r.F.push([performance.now(), ctl.etat().actives]); requestAnimationFrame(f); })(); }); return ctl; }; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, onb=False, guide=False); pg=B.ouvre(ctx,'app.html',attente=7000)
    pg.evaluate(REC); B.tap_sel(pg,'#onbPh'); pg.wait_for_timeout(500); pg.keyboard.type('Camille',delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(9000)
    R=pg.evaluate("()=>window.__R"); print('charge', B.charge())
    for r in R:
        F=r['F']; 
        if not F: continue
        dep={}; fr={}
        for t,a in F:
            for j in a: dep.setdefault(j,t); fr[j]=fr.get(j,0)+1
        js=sorted(dep); st=[dep[j] for j in js]
        rate=(len(st)-1)/((st[-1]-st[0])/1000) if len(st)>1 else 0
        dts=[F[i+1][0]-F[i][0] for i in range(len(F)-1)]; dts.sort()
        dur={j:max(t for t,a in F if j in a)-dep[j] for j in js}
        sp=[(j,fr[j],round(dur[j])) for j in js if fr[j]<4]
        print('   images : méd %.1f ms, max %.1f ; lettres < 4 images : %s'%(dts[len(dts)//2], dts[-1], sp))
        print(r['id'], 'lettres', len(r['gl'] or []), 'max actives', max(len(a) for t,a in F), 'images/lettre min', min(fr.values()) if fr else 0, 'méd', sorted(fr.values())[len(fr)//2] if fr else 0, 'départs/s %.1f'%rate, 'variantes', ''.join((g[2] or '-') for g in r['gl'] or []))
    ctx.close(); b.close()
