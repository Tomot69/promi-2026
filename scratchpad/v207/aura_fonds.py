import sys, os; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F=os.environ.get('FICH','app.html')
with sync_playwright() as p:
    b=p.webkit.launch()
    for sombre in (False,True):
        ctx=B.contexte(b,sombre=sombre); B.toile_pleine(ctx,10); pg=B.ouvre(ctx,F)
        pg.evaluate("()=>{ closeAll(); document.getElementById('souffleBtn').click(); }"); pg.wait_for_timeout(3500)
        r=pg.evaluate("""()=>{ const q=s=>document.querySelector(s); const st=e=>{ if(!e) return null; const c=getComputedStyle(e), r=e.getBoundingClientRect(); return {bg:c.backgroundColor, bord:c.borderTopWidth+' '+c.borderTopStyle+' '+c.borderTopColor, rad:c.borderRadius, col:c.color, r:[r.left,r.top,r.width,r.height].map(Math.round)}; };
          const a=document.getElementById('auraScreen'); return {ecran:st(a), plateau:st(a.querySelector('.enh')), bouton:st(document.getElementById('auPartage')), fondPage:(window._aura&&_aura.fondPage)?String(_aura.fondPage()):null}; }""")
        print('sombre' if sombre else 'clair', r); ctx.close()
    b.close()
