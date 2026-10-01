# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
ECR=[('accueil',"()=>{closeAll();}"),('studio',"()=>{closeAll(); document.getElementById('studioBtn').click();}"),
     ('aura',"()=>{closeAll(); document.getElementById('souffleBtn').click();}"),
     ('partage',"()=>{closeAll(); const b=document.getElementById('shareBtn'); if(b)b.click();}")]
JS=r"""()=>{const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const out=[];
  document.querySelectorAll('#device *').forEach(e=>{
    const r=e.getBoundingClientRect(); if(r.width<10||r.height<10) return;
    const y=(r.top-dv.top)/s; if(y<10||y>150) return;
    const cs=getComputedStyle(e);
    const fs=parseFloat(cs.fontSize);
    if(fs<20) return;
    const kids=[...e.children].filter(k=>k.getBoundingClientRect().width>0).length;
    const t=(e.textContent||'').trim().replace(/\s+/g,' ').slice(0,18); if(!t) return;
    if(e.querySelector('*') && e.children.length>2) return;
    out.push({t:t, fs:cs.fontSize, ff:cs.fontFamily.split(',')[0], y:+y.toFixed(0),
      cl:(e.id?'#'+e.id:'.'+String(e.className).split(' ')[0]).slice(0,20),
      col:cs.color,
      x:[...e.querySelectorAll('span,i,b')].map(k=>({c:String(k.className).slice(0,10), t:k.textContent.slice(0,3),
        col:getComputedStyle(k).color, an:getComputedStyle(k).animationName+' '+getComputedStyle(k).animationDuration}))});});
  return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for nom,js in ECR:
        pg.evaluate(js); pg.wait_for_timeout(2200)
        for o in pg.evaluate(JS): print('%-9s' % nom, o)
    b.close()
