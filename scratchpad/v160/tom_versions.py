"""v160 (C-177) — l'état exporté de Tom, ouvert dans chaque version : où sont ses dalles à l'écran, sont-elles entassées ?"""
import sys, json, math; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
FICHIERS = sys.argv[1:] or ['zz-v152.html', 'zz-v158.html', 'zz-v159.html', 'zz-v160a.html', 'app.html']
LIT = """()=>{var L=Toile_lecture(); var c=L.graines.filter(g=>g.kind!=='gray'); var v=L.vue;
  var P=c.map(g=>[+(g.x*v.s+v.ox).toFixed(1), +(g.y*v.s+v.oy).toFixed(1), g.pid]); var dm=1e9, pr=0;
  for(var i=0;i<P.length;i++) for(var j=i+1;j<P.length;j++){ var d=Math.hypot(P[i][0]-P[j][0],P[i][1]-P[j][1]); dm=Math.min(dm,d); if(d<30) pr++; }
  var st=JSON.parse(localStorage.getItem('promi_state')||'{}'); var pl=(st.promises||[]).map(p=>JSON.stringify(p.place));
  return {s:+v.s.toFixed(3), ox:+v.ox.toFixed(1), oy:+v.oy.toFixed(1), n:P.length, dmin:+dm.toFixed(1), proches:pr, pos:P, places:pl, monde:(Toile_state&&Toile_state().theme)||''}; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for F in FICHIERS:
        ctx, d = B.contexte_tom(b, __import__('os').environ.get('ETAT','etats/tom-20261023-125022.json'))
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F, timeout=120000); pg.wait_for_timeout(11000)
        for k in range(int(__import__('os').environ.get('NOUV','4'))):
            if k: pg.reload(timeout=120000); pg.wait_for_timeout(11000)
            r = pg.evaluate(LIT)
            print('%-14s ouverture %d · vue s %s ox %s oy %s · %d dalles · écart mini %s pt · paires à moins de 30 pt : %d' % (F, k+1, r['s'], r['ox'], r['oy'], r['n'], r['dmin'], r['proches']), flush=True)
            print('     positions', r['pos']); print('     places', r['places'])
            if k == 0: pg.screenshot(path='scratchpad/v160/tom-%s.png' % F.replace('.html', ''))
        ctx.close()
    b.close()
