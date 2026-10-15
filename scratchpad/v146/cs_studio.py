import sys, json, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
ST = """()=>{ const r=v=>Math.round(v*100)/100; return [...document.querySelectorAll('#studioScreen canvas')].filter(c=>c.__c&&c.__c.seeds).map(c=>({id:c.id||c.className, n:c.__c.seeds.length, th:c.__c.th, g:c.__c.seeds.map(s=>[s.kind==='gray'?0:1, r(s.x), r(s.y), r(s.w), s.gray?s.gray.join(','):'', s.pid==null?null:s.pid])})); }"""
def cmp(a, b):
    out = []
    for x, y in zip(a, b):
        if x['n'] != y['n']: out.append('%s nombre %d/%d' % (x['id'], x['n'], y['n'])); continue
        d = max([max(abs(u[1]-v[1]), abs(u[2]-v[2]), abs(u[3]-v[3])) for u, v in zip(x['g'], y['g'])] or [0])
        col = sum(1 for u, v in zip(x['g'], y['g']) if u[0] != v[0]); gris = sum(1 for u, v in zip(x['g'], y['g']) if u[4] != v[4])
        out.append('%s (%s) %d graines · écart max %.2f pt · colorées changées %d · gris changés %d' % (x['id'], x['th'], x['n'], d, col, gris))
    return out
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx)
    pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} }")
    B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(5000)
    a1 = pg.evaluate(ST); pg.wait_for_timeout(1500); a1b = pg.evaluate(ST)
    print('témoin (1,5 s sans rien toucher) :', cmp(a1, a1b))
    # la vraie bascule : le disque SOMBRE du Studio
    r = pg.evaluate("()=>{ const e=[...document.querySelectorAll('#studioScreen [data-th], #studioScreen .st3-th, #studioScreen button')].filter(x=>/SOMBRE|CLAIR/i.test(x.textContent||'')||x.dataset.th).map(x=>[(x.textContent||'').trim().slice(0,12), x.dataset.th||'', x.className, Math.round(x.getBoundingClientRect().left), Math.round(x.getBoundingClientRect().top)]); return e; }")
    print('commandes de thème au Studio :', r[:6])
    pg.evaluate("()=>window.setTheme('dark')"); pg.wait_for_timeout(3000); a2 = pg.evaluate(ST)
    print('clair → sombre :', cmp(a1b, a2))
    pg.evaluate("()=>window.setTheme('light')"); pg.wait_for_timeout(3000); a3 = pg.evaluate(ST)
    print('retour clair   :', cmp(a1b, a3))
    b.close()
