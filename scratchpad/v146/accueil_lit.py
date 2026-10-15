import sys, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
J = """()=>{ const d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; const R=e=>{ const q=e.getBoundingClientRect(); return [Math.round((q.left-d.left)/k*10)/10, Math.round((q.top-d.top)/k*10)/10, Math.round(q.width/k*10)/10, Math.round(q.height/k*10)/10]; };
  const o={}; const i=document.querySelector('.acc-plat .acc-mm i'); if(i){ const c=getComputedStyle(i); o.I={col:c.color, fill:c.webkitTextFillColor, anim:c.animationName}; }
  const pl=document.getElementById('accPlat'); o.plat={bg:getComputedStyle(pl).backgroundColor, r:R(pl), enfants:[...pl.children].map(e=>[(e.id||e.className)+'', R(e), getComputedStyle(e).display])};
  const ba=document.querySelector('.acc-barre'); o.barre={bg:getComputedStyle(ba).backgroundColor, r:R(ba), fond:(document.getElementById('accBarreFond')?getComputedStyle(document.getElementById('accBarreFond')).backgroundColor:null)};
  o.entrees=[...ba.querySelectorAll('*')].filter(e=>e.children.length===0 && (e.textContent||'').trim().length>1).map(e=>{ const c=getComputedStyle(e); return [e.textContent.trim(), (e.className||e.tagName)+'', (e.parentElement.id||e.parentElement.className)+'', c.color, c.webkitTextFillColor, c.fontFamily.split(',')[0], c.fontSize, R(e)]; });
  const cb=document.getElementById('createBtn'); o.plus={r:R(cb), html:cb.innerHTML.slice(0,400), col:getComputedStyle(cb).color, bg:getComputedStyle(cb).backgroundColor};
  o.plusEnfants=[...cb.querySelectorAll('*')].map(e=>{ const c=getComputedStyle(e); return [(e.tagName+'.'+(e.className.baseVal!==undefined?e.className.baseVal:e.className)), R(e), c.stroke, c.fill, c.color, c.backgroundColor]; }).slice(0,12);
  const cs=getComputedStyle(cb,'::before'), ca=getComputedStyle(cb,'::after'); o.plusPseudo={before:[cs.content, cs.background.slice(0,160), cs.width, cs.height], after:[ca.content, ca.background.slice(0,160), ca.width, ca.height, ca.color]};
  return o; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        ctx = B.contexte(b, sombre=sombre); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx)
        o = pg.evaluate(J); print('=== %s' % ('SOMBRE' if sombre else 'CLAIR'))
        for k, v in o.items(): print(k, ':', json.dumps(v, ensure_ascii=False)[:900])
        B.capture(pg, 'planche-v146/accueil-avant-%s.png' % ('sombre' if sombre else 'clair')); ctx.close()
    b.close()
