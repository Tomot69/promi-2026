import sys, math, re, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
src = io.open('redteam_deplace.py', encoding='utf-8').read()
OU = re.search(r'OU = """(.*?)"""', src, re.S).group(1)
def essai(b, monde, n, fichier='app.html'):
    ctx = B.contexte(b, stockage={'promi_premium': '1'}); B.toile_pleine(ctx, n); pg = B.ouvre(ctx, fichier)
    pg.evaluate("(m)=>{try{setPremium(true)}catch(e){} Toile.setTheme(m)}", monde); pg.wait_for_timeout(2500)
    neuf = pg.evaluate("()=>Toile.semisNeuf()"); G = pg.evaluate(OU); pids = sorted(G, key=lambda k: -G[k][2])
    a = pids[len(pids)//2]; x0, y0 = G[a][0], G[a][1]; cx, cy = 195, 400; d = math.hypot(cx - x0, cy - y0) or 1
    x1, y1 = (x0 + (cx - x0) / d * 110, y0 + (cy - y0) / d * 110) if d >= 60 else (x0 + 90, y0 + 90)
    B.glisse(pg, B.droite((x0, y0), (x1, y1), 14), pas=40, tenue=950); pg.wait_for_timeout(1600)
    G2 = pg.evaluate(OU); ou = G2.get(a); pg.wait_for_timeout(2500); G2b = pg.evaluate(OU); oub = G2b.get(a)
    pg.reload(); pg.wait_for_timeout(6500); G3 = pg.evaluate(OU); o3 = G3.get(a)
    f = lambda o: o and [round(v) for v in o[:2]]
    print('%-12s n=%d semis neuf=%s · départ %s · lâcher (%d, %d) · à 1,6 s %s (à %s pt du doigt) · à 4,1 s %s · relue %s' % (monde, n, neuf, f(G[a]), x1, y1, f(ou), ou and round(math.hypot(ou[0]-x1, ou[1]-y1)), f(oub), f(o3)), flush=True)
    ctx.close()
with sync_playwright() as p:
    b = p.webkit.launch()
    for monde, n in (('esquille', 10), ('ritournelle', 10), ('pochade', 10)): essai(b, monde, n)
    b.close()
