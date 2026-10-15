import sys, json, io; sys.path.insert(0, '.'); sys.path.insert(0, 'scratchpad/v146')
from playwright.sync_api import sync_playwright
import banc_tom as B
LIT = """()=>{ const L=window.Toile_lecture(); const r=v=>Math.round(v*1000)/1000;
  return {vue:[r(L.vue.s),r(L.vue.ox),r(L.vue.oy)],g:L.graines.map(s=>[s.pid, s.kind, r(s.x), r(s.y), r(s.w)]), clair:document.getElementById('device').classList.contains('light'), monde:Toile.getTheme()}; }"""
def lit(b, N, sombre, monde=None):
    ctx = B.contexte(b, sombre=sombre)
    st = json.load(io.open('banc-etats/etat-%d.json' % N, encoding='utf-8')); st['promi_theme'] = 'dark' if sombre else 'light'
    ctx.add_init_script("try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st))
    pg = B.ouvre(ctx, attente=8000)
    if monde: pg.evaluate("m=>{ try{ setPremium(true); }catch(e){} Toile.setTheme(m); }", monde); pg.wait_for_timeout(2500)
    g = pg.evaluate(LIT); ctx.close(); return g
def cmp(a, b):
    pa = {x[0]: x for x in a['g'] if x[0] is not None}; pb = {x[0]: x for x in b['g'] if x[0] is not None}
    dp = max([max(abs(pa[k][2]-pb[k][2]), abs(pa[k][3]-pb[k][3]), abs(pa[k][4]-pb[k][4])) for k in pa if k in pb] or [0])
    va = sorted([tuple(x[2:5]) for x in a['g'] if x[0] is None]); vb = sorted([tuple(x[2:5]) for x in b['g'] if x[0] is None])
    dv = (max(max(abs(p-q) for p, q in zip(x, y)) for x, y in zip(va, vb)) if len(va) == len(vb) and va else (0 if not va and not vb else 'nombre %d/%d' % (len(va), len(vb))))
    return 'paroles %d/%d écart %.3f · vides %s/%s écart %s · vue %s / %s' % (len(pa), len(pb), dp, len(va), len(vb), dv if isinstance(dv, str) else round(dv, 3), a['vue'], b['vue'])
with sync_playwright() as p:
    b = p.webkit.launch()
    for N in (1, 5, 25):
        for monde in (None, 'ritournelle'):
            c1 = lit(b, N, False, monde); c2 = lit(b, N, False, monde); s1 = lit(b, N, True, monde)
            print('N=%d %s (%s, clair %s / sombre %s)' % (N, monde or 'monde sauvé', c1['monde'], c1['clair'], s1['clair']))
            print('   clair / clair  :', cmp(c1, c2)); print('   clair / sombre :', cmp(c1, s1), flush=True)
    b.close()
