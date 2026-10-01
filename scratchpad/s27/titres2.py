# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
SONDE=r"""()=>{
  function encre(el){
    // rectangle de l'ENCRE du premier noeud de texte
    var n=null; for(var i=0;i<el.childNodes.length;i++){ var c=el.childNodes[i];
      if(c.nodeType===3 && c.textContent.trim()){ n=c; break; } }
    if(!n) return null;
    var r=document.createRange(); r.selectNodeContents(n);
    var b=r.getBoundingClientRect();
    return {txt:n.textContent.trim().slice(0,18), w:+b.width.toFixed(1), h:+b.height.toFixed(1), x:+b.left.toFixed(1), y:+b.top.toFixed(1)};
  }
  var out=[];
  ['.scr-t','.scr-ti','.stp-t','.fd-h2'].forEach(function(sel){
    document.querySelectorAll(sel).forEach(function(el){
      var r=el.getBoundingClientRect(); if(r.width<4||r.height<4) return;
      var cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.display==='none') return;
      var e=encre(el); if(!e) return;
      out.push({sel:sel, txt:e.txt, police:cs.fontFamily.split(',')[0].replace(/["']/g,''),
        taille:cs.fontSize, encreH:e.h, encreW:e.w, x:e.x, y:e.y,
        boite:[+r.left.toFixed(0),+r.top.toFixed(0),+r.width.toFixed(0),+r.height.toFixed(0)]});
    });
  });
  return out;
}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("async()=>{await document.fonts.ready;}")
    for nom,js,wt in (('fil',"()=>{closeAll(); document.getElementById('filBtn').click();}",3200),
                      ('studio',"()=>{closeAll(); document.getElementById('studioBtn').click();}",2800),
                      ('index',"()=>{closeAll(); if(window.ouvrirIndex)ouvrirIndex();}",3000),
                      ('aura',"()=>{closeAll(); document.getElementById('souffleBtn').click();}",5000),
                      ('partage',"()=>{closeAll(); document.getElementById('shareBtn').click();}",3600),
                      ('reglages',"()=>{closeAll(); document.getElementById('settingsBtn').click();}",2600)):
        pg.evaluate(js); pg.wait_for_timeout(wt)
        for x in pg.evaluate(SONDE):
            if x['boite'][1]<300 and x['boite'][1]>-50:
                print('%-9s %-14s %-11s %-6s encre %5.1f x %5.1f   boite %s'%(nom,x['txt'],x['police'],x['taille'],x['encreW'],x['encreH'],x['boite']))
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(500)
    b.close()
