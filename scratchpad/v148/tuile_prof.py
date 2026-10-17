import sys
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null }"
ARME = r"""()=>{ window.__pr={}; const N=['closeAll','syncAll','peintMinis','_s4Index','_garderEtat','_pinceauRangee','renderCsDalle','_peintGrappe','_phraseRendu','renderTileIcons','_csColorLabels','_pgDeform','_teinterFil','buildIndex','_rendDalle','_poseDalle'];
  const enve=(o,k,nom)=>{ const f=o[k]; if(typeof f!=='function'||f.__pr) return; const w=function(){ const t=performance.now(); try{ return f.apply(this, arguments); } finally{ const d=performance.now()-t; const e=window.__pr[nom]||(window.__pr[nom]=[0,0]); e[0]+=d; e[1]++; } }; w.__pr=1; o[k]=w; };
  Object.keys(window).forEach(n=>{ try{ if(typeof window[n]==='function' && !/^(webkit|on|setTimeout|setInterval|requestAnimationFrame|clearTimeout|fetch|alert|getComputedStyle|matchMedia|Image|Promise|Error|Date|Math|JSON|Array|Object|String|Number|Boolean|Map|Set|WeakMap|Symbol|Function|RegExp|Path2D|DOMParser|XMLSerializer|MutationObserver|ResizeObserver|IntersectionObserver|Event|CustomEvent|Blob|URL|Worker|performance|console)/.test(n) && !/^[A-Z]/.test(n)) enve(window,n,n); }catch(e){} }); if(window.Toile){ ['sync','dalleTrame','addPromi','renderTo'].forEach(k=>enve(window.Toile,k,'Toile.'+k)); } }"""
F = sys.argv[1]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); pg = ouvre(ctx, F)
    def page_plus(t):
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
        pg.evaluate("a=>{document.getElementById('fTitle').value=a;document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} }", t); pg.wait_for_timeout(400)
    page_plus('rendre'); z = pg.evaluate(ZONE, 'planterZone'); y = z[1] + z[3] * 0.45
    glisse(pg, [[40 + 70 * i / 10, y] for i in range(11)], pas=100); pg.wait_for_timeout(3200)
    pg.evaluate(ARME)
    t = pg.evaluate("()=>{ const t0=performance.now(); closeAll(); const a=performance.now(); document.getElementById('createBtn').click(); const b=performance.now(); window.__gap=[]; let p=performance.now(); const iv=setInterval(()=>{ const n=performance.now(); if(n-p>60) window.__gap.push([Math.round(p-t0), Math.round(n-p)]); p=n; if(n-t0>2000) clearInterval(iv); }, 10); return [a-t0, b-a]; }")
    pg.wait_for_timeout(2200); print('   trous', pg.evaluate("()=>window.__gap"))
    print(F, 'closeAll %.0f ms · createBtn.click %.0f ms' % tuple(t)); pr = pg.evaluate("()=>window.__pr")
    for k, v in sorted(pr.items(), key=lambda x: -x[1][0])[:22]: print('   %-18s %7.1f ms  ×%d' % (k, v[0], v[1]))
    b.close()
