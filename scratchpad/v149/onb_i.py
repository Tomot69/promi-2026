# §1 C-153 : le I de PROMI dans l'onboarding — animation, couleur, opacités lues sur 2,4 s, ce qui est au-dessus de lui.
import sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
LIT = """async ()=>{ const v=document.getElementById('onbV'); const mm=v&&v.querySelector('.onbv-mm'), i=mm&&mm.querySelector('i'); if(!i) return {absent:true};
  const s=getComputedStyle(i), r=i.getBoundingClientRect(), h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
  const op=[]; for(let k=0;k<48;k++){ op.push(+getComputedStyle(i).opacity); await new Promise(z=>setTimeout(z,50)); }
  return {anim:s.animationName, dur:s.animationDuration, tf:s.animationTimingFunction, col:s.color, fill:s.webkitTextFillColor, vis:getComputedStyle(mm).visibility, mmop:getComputedStyle(mm).opacity,
    dessus:h?(h.id||h.className||h.tagName):null, op:[...new Set(op)], html:mm.innerHTML.slice(0,200)}; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True); pg = ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(9000)
    print(pg.evaluate(LIT)); b.close()
