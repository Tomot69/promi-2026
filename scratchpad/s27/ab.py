from playwright.sync_api import sync_playwright
import json
SON=r"""()=>{
  function lum(c){return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2];}
  function rgb(s){var m=(s||'').match(/-?\d+(\.\d+)?/g);return m?m.slice(0,3).map(Number):null;}
  function fond(el){var n=el;while(n&&n.nodeType===1){var b=getComputedStyle(n).backgroundColor,c=rgb(b);
    var a=b.match(/rgba?\([^)]*?,\s*([\d.]+)\)/); if(c&&(!a||parseFloat(a[1])>0.85))return c; n=n.parentNode;} return null;}
  var o=[];
  document.querySelectorAll('#detailPoster *').forEach(function(el){
    if(el.children.length) return; var t=(el.textContent||'').trim(); if(!t) return;
    var r=el.getBoundingClientRect(); if(r.width<2||r.height<2) return;
    var cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<0.05) return;
    var c=rgb(cs.webkitTextFillColor||cs.color), f=fond(el); if(!c||!f) return;
    o.push([+Math.abs(lum(c)-lum(f)).toFixed(1), t.slice(0,24), cs.color]);});
  o.sort(function(a,b){return a[0]-b[0];}); return o.slice(0,4);}"""
for url,tag in (('http://127.0.0.1:8752/sauvegardes/app-avant-lot-v13.html','AVANT'),
                ('http://127.0.0.1:8752/app.html','APRES')):
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
        pg.goto(url); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(600)
        pg.evaluate("()=>{closeAll(); openDetail(133);}"); pg.wait_for_timeout(3000)
        print(tag, json.dumps(pg.evaluate(SON),ensure_ascii=False))
        if tag=='APRES':
            # on NEUTRALISE la passe et on rouvre : le defaut doit revenir
            pg.evaluate("()=>{window._lisibiliteCorps=function(){return 0;};}")
            pg.evaluate("()=>{closeAll(); openDetail(133);}"); pg.wait_for_timeout(3000)
            print('APRES sans la passe', json.dumps(pg.evaluate(SON),ensure_ascii=False))
        b.close()
