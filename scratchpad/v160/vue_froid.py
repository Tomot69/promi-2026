import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
src = open('redteam_toile_stable.py', encoding='utf-8').read()
exec(src.split('import json, io, glob, os')[1].split('ENTASSE =')[0].replace('def etat', 'import json, io, glob, os\ndef etat', 1), globals())
POSE = src.split('POSE = """')[1].split('"""')[0]
def pose(pg):
    n = 0
    for _ in range(48):
        pg.wait_for_timeout(250); n = n + 1 if pg.evaluate(POSE) else 0
        if n >= 3: return
MONDES = sys.argv[1].split(','); NS = [int(x) for x in sys.argv[2].split(',')]
with sync_playwright() as p:
    br = p.webkit.launch()
    for m in MONDES:
        for n in NS:
            r = []
            for F in ((__import__('os').environ.get('FA','zz-v160a.html'), __import__('os').environ.get('FB','zz-v160b.html')) * int(__import__('os').environ.get('REP','2'))):
                ctx = B.contexte(br, sombre=True, stockage=studio(m)); pose_etat(ctx, etat(n)); pg = B.ouvre(ctx, F); pose(pg)
                v = pg.evaluate("()=>{var l=Toile_lecture(); return [+l.vue.s.toFixed(3), +l.vue.ox.toFixed(1), +l.vue.oy.toFixed(1), window._cadrageLancement||0]}")
                if __import__('os').environ.get('TARD'): pg.wait_for_timeout(6000); v[0] = '%s→%s' % (v[0], pg.evaluate("()=>+Toile_lecture().vue.s.toFixed(3)"))
                r.append(v); ctx.close()
            print('%-12s %2d  v160a %s   corrigé %s' % (m, n, [x[0] for x in r[0::2]], [x[0] for x in r[1::2]]), flush=True)
    br.close()
