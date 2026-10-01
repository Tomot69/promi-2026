# SONDE : qu'est-ce qui peint la tache derrière les dalles de l'écran qui vend ?
from playwright.sync_api import sync_playwright
J = r"""()=>{ const ps=document.getElementById('plusScreen'); const out={classes:ps.className};
  ['::before','::after'].forEach(pe=>{ const k=getComputedStyle(ps,pe); out[pe]={content:k.content, display:k.display, bg:k.backgroundImage.slice(0,160), bgc:k.backgroundColor, pos:k.position, w:k.width, h:k.height, top:k.top, left:k.left, anim:k.animationName, op:k.opacity, filter:k.filter, z:k.zIndex}; });
  const k=getComputedStyle(ps); out.self={bg:k.backgroundImage.slice(0,160), bgc:k.backgroundColor};
  // ce qui est peint au centre de la tache (hors dalles) : la pile des éléments
  const dv=document.getElementById('device').getBoundingClientRect(); const x=dv.left+300, y=dv.top+300;
  out.pile=document.elementsFromPoint(x,y).slice(0,6).map(e=>e.id||e.className&&String(e.className).slice(0,40)||e.tagName);
  out.canevas=[...ps.querySelectorAll('canvas')].map(c=>({id:c.id, cls:c.className, vis:c.checkVisibility(), r:(()=>{const q=c.getBoundingClientRect(); return [Math.round(q.left-dv.left),Math.round(q.top-dv.top),Math.round(q.width),Math.round(q.height)];})()}));
  out.regles=[]; for(const sh of document.styleSheets){ let rs; try{ rs=sh.cssRules; }catch(e){ continue; } for(const r of rs){ if(r.selectorText && /tuto-fond[^,]*::?(before|after)|s-plus[^,]*::?(before|after)|plusScreen[^,]*::?(before|after)/.test(r.selectorText)) out.regles.push(r.selectorText.slice(0,120)+' {'+r.style.cssText.slice(0,200)+'}'); } }
  return out; }"""
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.evaluate("()=>setTheme('light')")
    pg.evaluate("()=>{ closeAll(); document.getElementById('cercleTopBtn').click(); }"); pg.wait_for_timeout(1500)
    import json; r = pg.evaluate(J)
    for k, v in r.items(): print(k, ':', json.dumps(v, ensure_ascii=False)[:700])
    br.close()
