import sys, json; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'
COL = """(root)=>{ const R=document.querySelector(root); if(!R) return []; const out=[]; const w=document.createTreeWalker(R,NodeFilter.SHOW_TEXT);
  while(w.nextNode()){ const n=w.currentNode; const t=n.nodeValue.trim(); if(!t) continue; const e=n.parentElement; let v=e,vis=true; while(v&&v!==document.body){ const c=getComputedStyle(v); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05){vis=false;break;} v=v.parentElement; }
    if(!vis) continue; const c=getComputedStyle(e); out.push([t, c.webkitTextFillColor||c.color, e.className||e.tagName, e.closest('[id]')?e.closest('[id]').id:'']); }
  return out; }"""
def parcours(pg):
    pages = {}
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(400); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(300)
    pages['prenom'] = pg.evaluate(COL, '#onbV')
    pg.keyboard.press('Enter'); pg.wait_for_timeout(5000)
    pages['parole'] = pg.evaluate(COL, '#onbV')
    pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(5000)
    pages['trait'] = pg.evaluate(COL, '#onbV')
    z = pg.evaluate("()=>{ const c=document.getElementById('onbTrait'); if(!c) return null; const r=c.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return {l:(r.left-D.left)/k, t:(r.top-D.top)/k, k:r.width/390/k, dep:c.getAttribute('data-depart'), arr:c.getAttribute('data-arrivee')}; }")
    a = [float(v) for v in z['dep'].split(',')]; e = [float(v) for v in z['arr'].split(',')]
    x0, y0, x1, y1 = z['l'] + a[0] * z['k'], z['t'] + a[1] * z['k'], z['l'] + (e[0] + 6) * z['k'], z['t'] + e[1] * z['k']
    B.glisse(pg, [[x0 + (x1 - x0) * i / 24, y0 + (y1 - y0) * i / 24 - 14 * (1 - abs(2 * i / 24 - 1))] for i in range(25)], pas=24, tenue=90)
    pg.wait_for_timeout(5600)
    for _ in range(3): B.tap(pg, 195, 300); pg.wait_for_timeout(4000)
    pages['fin'] = pg.evaluate(COL, '#onbV')
    return pages
out = {}
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('clair','sombre'):
        ctx = B.contexte(b, sombre=(th=='sombre'), onb=False, guide=False); pg = B.ouvre(ctx, F, attente=7000)
        out[th] = parcours(pg); ctx.close()
        for et in ('studio','plus'):
            ctx = B.contexte(b, sombre=(th=='sombre')); pg = B.ouvre(ctx, F, attente=1000, q='?guide=1&gfige=4000' + ('&getape=plus' if et=='plus' else ''))
            pg.wait_for_timeout(9000); out[th]['guide-'+et] = pg.evaluate(COL, '#guidePhrase'); ctx.close()
    b.close()
json.dump(out, open('/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/6a98bbcb-8923-46df-9238-4fc6e5ddf3f2/scratchpad/v152/inv.json','w'), ensure_ascii=False, indent=0)
for th in out:
    for pgn, L in out[th].items():
        print('==', th, pgn)
        for t, c, k, i in L: print('   %-40s %-22s %s/%s' % (t[:40], c, k, i))
