import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
ENV="""()=>{ window.__D=[]; const env=(o,n,nom)=>{ const f=o[n]; if(typeof f!=='function') return; o[n]=function(){ const t=performance.now(); try{ return f.apply(this,arguments); } finally{ window.__D.push([nom, Math.round((performance.now()-t)*10)/10]); } }; };
  env(Toile,'addPromi','Toile.addPromi'); env(Toile,'sync','Toile.sync'); env(window,'relayout','relayout'); env(window,'caption','caption'); env(window,'syncAll','syncAll'); env(window,'render','render'); env(window,'buildFeed','buildFeed'); env(window,'saveState','saveState'); env(window,'closeAll','closeAll'); if(window._paroles) env(window._paroles,'publie','_paroles.publie'); }"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for m in ['encre','ritournelle','brouillamini']:
        ctx=B.contexte(b); pg=B.ouvre(ctx,F); pg.evaluate("m=>Toile.setTheme(m)",m); pg.wait_for_timeout(1200)
        for t in ['rendre le livre','écrire à Lou','arroser le ficus']: B.plante(pg,t)
        pg.wait_for_timeout(3000)
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{document.getElementById('fTitle').value='courir dimanche';document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null}"); pg.wait_for_timeout(2500)
        pg.evaluate(ENV); pg.evaluate("()=>document.getElementById('addPromi').click()"); pg.wait_for_timeout(3500)
        print(m,'planter',pg.evaluate("()=>window.__D.filter(e=>e[1]>=1)"))
        pg.evaluate("()=>{closeAll(); window.__D=[]; window._v16SupprimerPromi(promises[promises.length-1]); }"); pg.wait_for_timeout(800); B.tap_sel(pg,'.v16-oui'); pg.wait_for_timeout(3500)
        print(m,'retirer',pg.evaluate("()=>window.__D.filter(e=>e[1]>=1)"))
        ctx.close()
    b.close()
