import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
REC = """()=>{ window.__R=[]; const T=window.TraceLettres, tr=T.trace; T.trace=function(c){ const ctl=tr.apply(this,arguments); const r={id:c.id, F:[], G:null}; window.__R.push(r);
  ctl.pret.then(()=>{ (function f(){ if(ctl.fini) return; const e=ctl.etat(); r.F.push([performance.now(), e.t, e.actives, e.glyphe]); requestAnimationFrame(f); })(); }); return ctl; }; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, onb=False, guide=False); pg=B.ouvre(ctx,'app.html',attente=7000)
    pg.evaluate(REC); B.tap_sel(pg,'#onbPh'); pg.wait_for_timeout(500); pg.keyboard.type('Camille',delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(6000)
    R=pg.evaluate("()=>window.__R")
    for r in R[1:2]:
        F=r['F']; w0=F[0][0]
        for w,t,a,g in F[:40]: print('%6.1f  t=%7.1f  ig=%2d  %s'%(w-w0,t,g,a))
    ctx.close(); b.close()
