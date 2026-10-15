import sys, json, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
ORDRE = ['encre','touffe','brouillamini','halin','esquille','mosaique','braille','pixel','ramage','guingois','chantourne','volubilis','madrure','chamade','ritournelle','bobinette','mascaret','terrazzo','gravure','sillons']
LIT = """()=>{ const L=window.Toile_lecture(); const r=v=>Math.round(v*1000)/1000;
  return {W:L.W,H:L.H,vue:[r(L.vue.s),r(L.vue.ox),r(L.vue.oy)],g:L.graines.map(s=>[s.pid, s.kind, r(s.x), r(s.y), r(s.w), s.boite?s.boite.map?s.boite.map(r):JSON.stringify(s.boite):null]), clair:document.getElementById('device').classList.contains('light'), monde:Toile.getTheme()}; }"""
def pose(pg, max_ms=7000):
    a = None; t = 0
    while t < max_ms:
        pg.wait_for_timeout(350); t += 350
        b = pg.evaluate(LIT)
        if a is not None and json.dumps(a) == json.dumps(b): return b
        a = b
    return a
def ecart(a, b):
    if len(a['g']) != len(b['g']): return ('nombre', len(a['g']), len(b['g']))
    m = 0.0; pire = None
    for x, y in zip(a['g'], b['g']):
        if x[0] != y[0] or x[1] != y[1]: return ('ordre', x[:2], y[:2])
        d = max(abs(x[2]-y[2]), abs(x[3]-y[3]), abs(x[4]-y[4]) * 1.0)
        if d > m: m = d; pire = (x, y)
    v = max(abs(p-q) for p, q in zip(a['vue'], b['vue']))
    bo = sum(1 for x, y in zip(a['g'], b['g']) if json.dumps(x[5]) != json.dumps(y[5]))
    return ('ok', round(m, 3), round(v, 3), bo, pire if m > 0.01 else None)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b)
    st = json.load(io.open('banc-etats/etat-%d.json' % N, encoding='utf-8')); st.pop('promi_theme', None)
    ctx.add_init_script("try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st))
    pg = B.ouvre(ctx); pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} }")
    for m in ORDRE:
        pg.evaluate("m=>{ Toile.setTheme(m); }", m); g1 = pose(pg)
        pg.evaluate("()=>window.setTheme('dark')"); g2 = pose(pg)
        pg.evaluate("()=>window.setTheme('light')"); g3 = pose(pg)
        print('%-13s n=%d graines %d  clair %s sombre %s | clair→sombre %s | retour %s' % (m, N, len(g1['g']), g1['clair'], g2['clair'], ecart(g1, g2), ecart(g1, g3)), flush=True)
    print(pg.__dict__['erreurs'][:2]); b.close()
