import sys, json, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
LIT = "()=>{ const L=window.Toile_lecture(); return L.graines.map(s=>[s.pid, s.x, s.y, s.w]); }"
def d(a, b): return round(max(max(abs(x[1]-y[1]), abs(x[2]-y[2]), abs(x[3]-y[3])) for x, y in zip(a, b)), 4)
def pose(pg):
    a = None
    for _ in range(26):
        pg.wait_for_timeout(350); b = pg.evaluate(LIT)
        if a is not None and a == b: return b
        a = b
    return a
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, int(sys.argv[1]) if len(sys.argv) > 1 else 25); pg = B.ouvre(ctx)
    pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} }")
    for m in ('mosaique', 'terrazzo', 'encre', 'pixel'):
        pg.evaluate("m=>Toile.setTheme(m)", m); g0 = pose(pg)
        pg.wait_for_timeout(2500); g1 = pg.evaluate(LIT)
        pg.evaluate("()=>Toile.redraw()"); g2 = pose(pg)
        pg.evaluate("()=>Toile.reGray()"); g3 = pose(pg)
        pg.evaluate("()=>window.Toile_liven&&window.Toile_liven()"); g4 = pose(pg)
        pg.evaluate("()=>window.setTheme('dark')"); g5 = pose(pg)
        pg.evaluate("()=>window.setTheme('light')"); g6 = pose(pg)
        pg.evaluate("()=>window.setTheme('light')"); g7 = pose(pg)
        print('%-9s attente 2,5 s %s · redraw %s · reGray %s · liven %s · sombre %s · clair %s · clair (sans changement) %s' % (m, d(g0, g1), d(g1, g2), d(g2, g3), d(g3, g4), d(g4, g5), d(g5, g6), d(g6, g7)), flush=True)
    b.close()
