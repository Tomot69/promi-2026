#!/usr/bin/env python3
"""v158 (C-175) — les 20 mondes au Studio, sur le vrai chemin : glisser d'un monde à l'autre, rester au repos, faire glisser la dalle de la jauge.
Image par image, dans la page (requestAnimationFrame) : images > 34 ms, la plus longue, le p95. Usage : studio_mesure.py [fichier] [--json=sortie]"""
import sys, json, os; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
OUT = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--json=')), None)
SEG = """(n)=>{ window.__seg=n; }"""
INIT = """()=>{ window.__T=[]; window.__seg='-'; let av=performance.now(); (function f(t){ window.__T.push([window.__seg, t-av]); av=t; requestAnimationFrame(f); })(performance.now()); }"""
def stats(T, seg):
    v = sorted(d for s, d in T if s == seg)
    if not v: return None
    return {'n': len(v), 'p95': round(v[int(0.95 * (len(v) - 1))], 1), 'max': round(v[-1], 1), 'gt34': sum(1 for d in v if d > 34), 'gt50': sum(1 for d in v if d > 50)}
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, F)
    if '--membre' in sys.argv: pg.evaluate("()=>{ try{ setPremium(true); }catch(e){} }"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{ closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(3000)
    c = pg.evaluate("()=>{const e=document.querySelector('#studioScreen .stp-ton'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
    if c: pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(1200)
    pg.evaluate(INIT); res = {}; charge0 = B.charge()
    vus = []
    for i in range(22):
        m = pg.evaluate("()=>document.getElementById('studioScreen').getAttribute('data-stp-monde')||Toile.mondeCourant().m")
        if m in vus: break
        vus.append(m); lock = pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')")
        pg.evaluate(SEG, m + '|repos'); pg.wait_for_timeout(1800)
        sp = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, e=document.getElementById('st3thumb'), s=document.getElementById('st3spec'); if(!e||!s) return null; const r=e.getBoundingClientRect(), q=s.getBoundingClientRect(); if(r.width<2 || getComputedStyle(s).visibility==='hidden') return null; return [(r.left-D.left)/k+r.width/k/2, (r.top-D.top)/k+r.height/k/2, (q.left-D.left)/k, (q.right-D.left)/k]; }")
        if sp and not lock:
            pg.evaluate(SEG, m + '|jauge'); x, y, a, z = sp
            pts = [[x + (min(z - 6, x + 120) - x) * t / 20, y] for t in range(21)] + [[min(z - 6, x + 120) - (min(z - 6, x + 120) - max(a + 6, x - 120)) * t / 30, y] for t in range(31)]
            B.glisse(pg, pts, pas=24); pg.wait_for_timeout(300)
        pg.evaluate(SEG, m + '|passage'); B.glisse(pg, B.droite([300, 300], [80, 300], 10), pas=18); pg.wait_for_timeout(1400)
        res[m] = {'verrou': lock}
    T = pg.evaluate("()=>window.__T"); charge1 = B.charge()
    for m in res:
        for s in ('repos', 'jauge', 'passage'):
            st = stats(T, m + '|' + s)
            if st: res[m][s] = st
    b.close()
print('charge %.1f → %.1f' % (charge0, charge1))
for m, r in res.items():
    print('%-14s %s  repos %-38s jauge %-38s passage %s' % (m, 'payant' if r['verrou'] else 'libre ', r.get('repos'), r.get('jauge', '—'), r.get('passage')))
if OUT: json.dump({'charge': [charge0, charge1], 'mondes': res}, open(OUT, 'w'), indent=1)
