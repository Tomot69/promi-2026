import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=B.ouvre(ctx,'app.html'); pg.evaluate("m=>Toile.setTheme(m)",'touffe'); pg.wait_for_timeout(1200)
    for t in ['rendre le livre','écrire à Lou','arroser le ficus']: B.plante(pg,t)
    pg.wait_for_timeout(3000)
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
    pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1800)
    pg.evaluate("()=>{document.getElementById('fTitle').value='courir dimanche';document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null}"); pg.wait_for_timeout(2500)
    pg.evaluate("""()=>{ window.__L=[]; const t0=performance.now(); const f=window._repasseSombre; 
      const iv=setInterval(()=>{ const d=document.getElementById('device').getBoundingClientRect(); const e=document.elementFromPoint(d.left+d.width*.5,d.top+d.height*.47);
        const st=window.Toile_state&&Toile_state();
        window.__L.push([Math.round(performance.now()-t0), _evol()?1:0, _toileVue()?1:0, (e&&(e.id||e.className||e.tagName)+'').slice(0,30), st&&st.running?1:0, window._tirageActive?1:0, _arriveeEnCours()?1:0, _trans_en_cours()?1:0]); if(performance.now()-t0>3500) clearInterval(iv); },100);
      document.getElementById('addPromi').click(); }"""); pg.wait_for_timeout(3800)
    for l in pg.evaluate("()=>window.__L"): print(l)
    b.close()
