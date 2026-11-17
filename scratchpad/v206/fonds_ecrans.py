import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
JS = r"""(sel)=>{ const e=document.querySelector(sel); if(!e) return null; const o={}; const cs=getComputedStyle(e);
  o.bg=cs.backgroundColor; o.bgi=cs.backgroundImage.slice(0,200); o.cls=e.className;
  for(const ps of ['::before','::after']){ const c=getComputedStyle(e,ps); if(c.content!=='none') o[ps]={bg:c.backgroundColor, bgi:c.backgroundImage.slice(0,300), op:c.opacity, mix:c.mixBlendMode, z:c.zIndex, pos:c.position, inset:[c.top,c.left,c.width,c.height].join(' ')}; }
  o.enfants=[...e.children].filter(x=>{ const c=getComputedStyle(x); return (x.tagName==='CANVAS'||c.position==='absolute') && c.display!=='none' && x.getBoundingClientRect().width>300; }).map(x=>x.tagName+'#'+x.id+'.'+String(x.className).slice(0,30)+' bg:'+getComputedStyle(x).backgroundColor+' op:'+getComputedStyle(x).opacity);
  return o; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('clair','sombre'):
        ctx = B.contexte(b, sombre=(th=='sombre'), vw=430, vh=932); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, 'app.html')
        for nom, js, sel in (('index',"()=>ouvrirIndex()",'#indexSheet'),('fil',"()=>document.getElementById('filBtn').click()",'#feedView'),('aura',"()=>document.getElementById('souffleBtn').click()",'#auraScreen')):
            pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(600); pg.evaluate(js); pg.wait_for_timeout(2500)
            print(th, nom, pg.evaluate(JS, sel))
        ctx.close()
    b.close()
