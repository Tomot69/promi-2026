import sys, json; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from banc_tom import *
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'
M = sys.argv[2] if len(sys.argv)>2 else 'terrazzo'
GEO = "()=>{var c=Toile_cellules();return {v:c.view,W:c.W,H:c.H,g:c.c.filter(s=>s.pid!=null).map(s=>[s.pid,+s.x.toFixed(1),+s.y.toFixed(1)]),T:(()=>{var t=document.getElementById('toileCv');var x=t.getContext('2d');return x.getTransform().a+','+x.getTransform().d+','+t.width+'x'+t.height})()}}"
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b, stockage={'promi_premium':'1'}); toile_pleine(ctx, 25); pg = ouvre(ctx, F)
    pg.evaluate("m=>{Toile.setTheme(m)}", M); pg.wait_for_timeout(2500)
    a = pg.evaluate(GEO); capture(pg, 'scratchpad/v159/a.png')
    tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{var k=Object.keys(Toile.palettes());Toile.setPalette(k[3])}"); pg.wait_for_timeout(800)
    tap_sel(pg, "#studioScreen .closeb"); pg.wait_for_timeout(2500)
    bb = pg.evaluate(GEO); capture(pg, 'scratchpad/v159/b.png')
    print(a['T'], bb['T'], a['v'], bb['v'])
    d = [(x,y) for x,y in zip(a['g'], bb['g']) if abs(x[1]-y[1])>0.5 or abs(x[2]-y[2])>0.5]
    print('graines déplacées', len(d), d[:4], len(a['g']))
    print(pg.__dict__['erreurs'])
    b.close()
