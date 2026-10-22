import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
exec(open('redteam_toile_stable.py').read().split('res = []')[1].split('with sync_playwright()')[0].replace('def juge','def _j'))
F=sys.argv[1]; Q=sys.argv[2] if len(sys.argv)>2 else ''
with sync_playwright() as p:
    br=p.webkit.launch(); ctx=B.contexte(br, stockage={'promi_monde':'ramage'}); B.toile_pleine(ctx,25); pg=B.ouvre(ctx,F,q=Q)
    pg.evaluate("m=>{ try{ setPremium(true); }catch(e){} if(Toile.getTheme()!==m) Toile.setTheme(m); }", 'ramage'); pg.wait_for_timeout(2800)
    a=pg.evaluate(GEO); a0=pg.evaluate("()=>Toile_lecture().graines.filter(g=>g.pid!=null).map(g=>[g.pid,+g.x.toFixed(1),+g.y.toFixed(1),+g.w.toFixed(2)])")
    page(pg,'studio'); 
    for k in range(4):
        b=pg.evaluate(GEO); print(k, ecart(a,b)[0][:70], pg.evaluate("()=>Toile_state().running")); pg.wait_for_timeout(2000)
    b0=pg.evaluate("()=>Toile_lecture().graines.filter(g=>g.pid!=null).map(g=>[g.pid,+g.x.toFixed(1),+g.y.toFixed(1),+g.w.toFixed(2)])")
    A={x[0]:x for x in a0}; print([ (x[0],A[x[0]][1:],x[1:]) for x in b0 if abs(A[x[0]][1]-x[1])>1 or abs(A[x[0]][2]-x[2])>1][:5])
    br.close()
