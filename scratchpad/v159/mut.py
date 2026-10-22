import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
M=sys.argv[1]; N=int(sys.argv[2])
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, stockage={'promi_monde':M}); B.toile_pleine(ctx,N); pg=B.ouvre(ctx,'app.html',q='?nosilh=1')
    pg.evaluate("m=>{ try{setPremium(true)}catch(e){} if(Toile.getTheme()!==m) Toile.setTheme(m); }", M); pg.wait_for_timeout(4000)
    for w in ['encre','touffe','brouillamini','halin','esquille','mosaique','ramage','guingois','chantourne','volubilis','madrure','chamade','ritournelle','bobinette','mascaret','terrazzo']:
        r=pg.evaluate("""w=>{ const G=()=>Toile_graines().filter(g=>g[0]!=null).map(g=>g[1]+','+g[2]).join('|'); const a=G(), n0=Toile_graines().length; const id=promises.find(p=>!p.draft).id;
          const M=Toile.mondeCourant(); window._rendDalle(id,64,64,{monde:{m:w,p:M.p,h:M.h}}); const b=G(); return [a===b, n0, Toile_graines().length, Toile.getTheme(), Toile.semisNeuf()]; }""", w)
        print(w, r)
    b.close()
