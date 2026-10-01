# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import json
SONDE=r"""()=>{
  var sc=document.getElementById('auraScreen'); if(!sc) return null;
  var out=[]; var base=sc.getBoundingClientRect();
  sc.querySelectorAll('*').forEach(function(e){
    var r=e.getBoundingClientRect(); if(r.width<6||r.height<6) return;
    var cs=getComputedStyle(e); if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<0.05) return;
    var cl=String(e.className||'');
    if(!/au-|scr-|klegend|ah-|share|kr-/.test(cl) && !e.id) return;
    out.push({q:(e.id?'#'+e.id:'.'+cl.split(' ')[0]), y:+(r.top-base.top+sc.scrollTop).toFixed(0),
              h:+r.height.toFixed(0), x:+r.left.toFixed(0), w:+r.width.toFixed(0),
              txt:(e.children.length?'':(e.textContent||'').trim().slice(0,22))});
  });
  return {scrollH:sc.scrollHeight, clientH:sc.clientHeight, blocs:out.sort(function(a,b){return a.y-b.y;})};
}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(600)
    pg.evaluate("()=>{closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(5600)
    r=pg.evaluate(SONDE)
    print('scrollH',r['scrollH'],'clientH',r['clientH'])
    for x in r['blocs']:
        print('  y%-5d h%-5d x%-4d w%-4d %-16s %s'%(x['y'],x['h'],x['x'],x['w'],x['q'],x['txt']))
    # capture pleine hauteur
    pg.evaluate("()=>{var s=document.getElementById('auraScreen'); s.scrollTop=9999;}"); pg.wait_for_timeout(1500)
    open('scratchpad/s27/aura-bas.png','wb').write(pg.query_selector('#device').screenshot())
    b.close()
