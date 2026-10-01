# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
JS = r"""(ang)=>{
  const out=[];
  const liste=[...document.querySelectorAll('canvas.kr-c, .au-nb')].filter(e=>{
    const cs=getComputedStyle(e); return cs.boxShadow && cs.boxShadow!=='none' && e.getBoundingClientRect().width>8;});
  for(const e of liste){
    const r=e.getBoundingClientRect(), cx=r.left+r.width/2, cy=r.top+r.height/2, R=r.width/2+1.2;
    for(const a of ang){
      const x=cx+R*Math.cos(a*Math.PI/180), y=cy+R*Math.sin(a*Math.PI/180);
      const pile=document.elementsFromPoint(x,y).slice(0,3).map(k=>(k.id?'#'+k.id:'.'+String(k.className).split(' ')[0]).slice(0,22));
      out.push({el:(e.className?String(e.className).split(' ')[0]:'kr'), a:a, pile:pile,
        clipPere:(function(){let p=e.parentElement, l=[]; for(let i=0;i<3&&p;i++,p=p.parentElement){const c=getComputedStyle(p);
          if(c.overflow!=='visible'||c.clipPath!=='none') l.push((p.id?'#'+p.id:'.'+String(p.className).split(' ')[0]).slice(0,20)+':'+c.overflow);} return l;})()});
    }
  }
  return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee); if(p) openDetail(p.id);}")
    pg.wait_for_timeout(2800)
    print('FICHE'); 
    for o in pg.evaluate(JS,[262,270,90]): print('  ',o)
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(400)
    pg.evaluate("()=>{closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(5200)
    print('AURA')
    for o in pg.evaluate(JS,[174,180,0])[:6]: print('  ',o)
    b.close()
