# -*- coding: utf-8 -*-
import json,sys
from playwright.sync_api import sync_playwright
SONDE=r"""()=>{
  function lum(c){return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2];}
  function rgb(s){var m=(s||'').match(/-?\d+(\.\d+)?/g); return m?m.slice(0,3).map(Number):null;}
  function fondOpaque(el){
    var n=el;
    while(n && n!==document.documentElement){
      var c=getComputedStyle(n).backgroundColor, v=rgb(c);
      var a=(c.match(/rgba?\([^)]*?,\s*([\d.]+)\)/)); var al=a?parseFloat(a[1]):1;
      if(v && al>0.85) return {col:v, de:(n.id||n.className||n.tagName)};
      n=n.parentElement;
    }
    return null;
  }
  var out=[]; var dp=document.getElementById('detailPoster'); if(!dp) return out;
  dp.querySelectorAll('*').forEach(function(el){
    if(el.children.length) return;
    var t=(el.textContent||'').trim(); if(!t) return;
    var r=el.getBoundingClientRect(); if(r.width<2||r.height<2) return;
    var cs=getComputedStyle(el);
    if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<0.05) return;
    var c=rgb(cs.webkitTextFillColor||cs.color); var f=fondOpaque(el);
    if(!c||!f) return;
    out.push({txt:t.slice(0,30), cls:String(el.className||el.tagName).slice(0,20), couleur:cs.color,
              fond:'rgb('+f.col.join(',')+')', de:String(f.de).slice(0,22),
              dlum:+Math.abs(lum(c)-lum(f.col)).toFixed(1), y:+r.top.toFixed(0)});
  });
  return out.sort(function(a,b){return a.dlum-b.dlum;});
}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(700)
        for nom,idp in (('chiche-groupe',133),('chiche-tenu',129),('promi-tenu',125)):
            pg.evaluate("(i)=>{closeAll(); openDetail(i);}",idp); pg.wait_for_timeout(3200)
            r=pg.evaluate(SONDE)
            print('== %s / %s'%(nom,th))
            for x in r[:8]:
                print('   %5.1f  %-32s %-20s sur %-16s (%s) y%d'%(x['dlum'],x['txt'],x['couleur'],x['fond'],x['de'],x['y']))
            pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(500)
    b.close()
