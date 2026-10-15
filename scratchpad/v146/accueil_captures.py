# v146 — les deux images de l'accueil pour la page du guide : MÊME Toile (relue de la même sauvegarde), clair puis sombre ; et les boîtes des cibles
import sys, json, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
BO = """()=>{ const d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; const R=(x0,y0,x1,y1)=>[+((x0-d.left)/k).toFixed(2), +((y0-d.top)/k).toFixed(2), +((x1-x0)/k).toFixed(2), +((y1-y0)/k).toFixed(2)];
  function vu(el){ let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9; el.querySelectorAll('svg, .l').forEach(e=>{ const q=e.getBoundingClientRect(); if(q.width<2) return; x0=Math.min(x0,q.left); y0=Math.min(y0,q.top); x1=Math.max(x1,q.right); y1=Math.max(y1,q.bottom); }); return R(x0,y0,x1,y1); }
  const st=document.getElementById('studioBtn'), pl=document.getElementById('createBtn'), q=pl.getBoundingClientRect(), au=document.getElementById('souffleBtn'), ix=document.getElementById('indexBtn'), ba=document.querySelector('.acc-barre').getBoundingClientRect();
  return {studio:vu(st), plus:R(q.left,q.top,q.right,q.bottom), aura:vu(au), index:vu(ix), barre:R(ba.left,ba.top,ba.right,ba.bottom)}; }"""
out = {}
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        ctx = B.contexte(b, sombre=sombre); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx); pg.evaluate("()=>{ window._vivantOff=true; }"); pg.wait_for_timeout(600)
        nom = 'sombre' if sombre else 'clair'; B.capture(pg, 'variantes/accueil-%s.png' % nom); out[nom] = pg.evaluate(BO); ctx.close()
    b.close()
print(json.dumps(out)); io.open('variantes/accueil-boites.js', 'w', encoding='utf-8').write('/* v146 — les boîtes des cibles du guide sur l\'accueil, relevées sur l\'app (scratchpad/v146/accueil_captures.py). */\nwindow.ACCUEIL_BOITES=' + json.dumps(out) + ';\n')
