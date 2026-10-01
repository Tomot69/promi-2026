# -*- coding: utf-8 -*-
import json
from playwright.sync_api import sync_playwright
SONDE=r"""()=>{
  var out=[];
  document.querySelectorAll('.scr-t,.scr-ti,.enh-t,.stp-t,h1,.ah-head,.ti-mot').forEach(function(el){
    var r=el.getBoundingClientRect(); if(r.width<4||r.height<4) return;
    var cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.display==='none') return;
    var t=(el.textContent||'').trim(); if(!t) return;
    var c=document.createElement('canvas').getContext('2d');
    c.font=cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily.split(',')[0].replace(/["']/g,'');
    var m=c.measureText(t.toUpperCase());
    var cap=(m.actualBoundingBoxAscent!=null)?m.actualBoundingBoxAscent:null;
    out.push({txt:t.slice(0,22), id:(el.closest('.screen,.sheet,.poster')||{}).id||'', cls:String(el.className).slice(0,18),
      police:cs.fontFamily.split(',')[0].replace(/["']/g,''), taille:cs.fontSize,
      cap:cap!=null?+cap.toFixed(1):null, larg:+m.width.toFixed(1),
      x:+r.left.toFixed(0), y:+r.top.toFixed(0), w:+r.width.toFixed(0), h:+r.height.toFixed(0)});
  });
  return out;
}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("async()=>{await document.fonts.ready;}")
    for nom,js,wt in (('index',"()=>{closeAll(); if(window.ouvrirIndex)ouvrirIndex();}",3000),
                      ('fil',"()=>{closeAll(); document.getElementById('filBtn').click();}",3200),
                      ('studio',"()=>{closeAll(); document.getElementById('studioBtn').click();}",2800),
                      ('aura',"()=>{closeAll(); document.getElementById('souffleBtn').click();}",5000),
                      ('partage',"()=>{closeAll(); document.getElementById('shareBtn').click();}",3600),
                      ('reglages',"()=>{closeAll(); document.getElementById('settingsBtn').click();}",2600)):
        pg.evaluate(js); pg.wait_for_timeout(wt)
        print('==',nom)
        for x in pg.evaluate(SONDE):
            print('   %-22s %-12s %-6s cap %-6s larg %-7s @%d,%d %dx%d  [%s]'%(x['txt'],x['police'],x['taille'],x['cap'],x['larg'],x['x'],x['y'],x['w'],x['h'],x['cls']))
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(500)
    b.close()
