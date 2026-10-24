import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, 'app.html')
    pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(3000)
    vus=[]
    for i in range(22):
        m = pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')")
        if m in vus: break
        vus.append(m)
        if m in ('guingois','mascaret','chantourne'):
            pg.wait_for_timeout(4000)
            S = pg.evaluate("""async ()=>{ const c=document.getElementById('stBg').__c; const L=[];
              for(let k=0;k<12;k++){ await new Promise(r=>requestAnimationFrame(r)); const e=c.etat||{}; 
                L.push({n:c.seeds.length, xy:c.seeds.slice(0,4).map(s=>[+(s.x||0).toFixed(3),+(s.px!=null?s.px:0).toFixed(3),+(s.w||0).toFixed(3)]).join(' '), tr:!!e._trans, cy:c.cy?[c.cy.suiv|0,c.cy.pose|0]:null, lc:e.lastChange|0}); }
              return L; }""")
            print(m); [print('   ', x) for x in S[::3]]
        B.glisse(pg, B.droite([300, 300], [80, 300], 10), pas=18); pg.wait_for_timeout(1400)
    b.close()
