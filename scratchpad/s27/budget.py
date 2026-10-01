from playwright.sync_api import sync_playwright
import json
ORD=[('fil','#feedView .enh',"()=>{document.getElementById('filBtn').click();}",3200),
     ('studio','#stpHaut',"()=>{document.getElementById('studioBtn').click();}",2800),
     ('index','#indexSheet .enh',"()=>{if(window.ouvrirIndex)ouvrirIndex();}",3000),
     ('aura','#auraScreen .enh',"()=>{document.getElementById('souffleBtn').click();}",5000),
     ('partage','#shareScreen .enh',"()=>{document.getElementById('shareBtn').click();}",3600),
     ('reglages','#settingsScreen .enh',"()=>{document.getElementById('settingsBtn').click();}",2600)]
SONDE=r"""(sel)=>{
  function encreDe(el){ var r=document.createRange(); r.selectNodeContents(el);
    var b=r.getBoundingClientRect(); return [+b.left.toFixed(1),+b.right.toFixed(1),+b.top.toFixed(1),+b.bottom.toFixed(1)]; }
  var p=document.querySelector(sel); if(!p) return null;
  var ti=p.querySelector('.scr-t,.scr-ti,.stp-t,.fd-h2');
  var cl=p.querySelector('.closeb,[data-close]');
  var autres=[];
  p.querySelectorAll('*').forEach(function(e){ if(e===ti||e===cl) return;
    if(ti&&ti.contains(e)) return; if(cl&&cl.contains(e)) return;
    var r=e.getBoundingClientRect(); if(r.width<4||r.height<4) return;
    if(r.left>200 && r.left<300) autres.push([String(e.className||e.tagName).slice(0,14),+r.left.toFixed(1),+r.right.toFixed(1)]);
  });
  return {plateau:(function(){var r=p.getBoundingClientRect();return [+r.left.toFixed(1),+r.width.toFixed(1)];})(),
          titre:ti?{txt:ti.textContent.trim().slice(0,16), fs:getComputedStyle(ti).fontSize, encre:encreDe(ti)}:null,
          fermer:cl?{encre:encreDe(cl), boite:(function(){var r=cl.getBoundingClientRect();return [+r.left.toFixed(1),+r.right.toFixed(1)];})()}:null,
          autres:autres};
}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for nom,sel,js,wt in ORD:
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate(js); pg.wait_for_timeout(wt)
        print(nom, json.dumps(pg.evaluate(SONDE,sel),ensure_ascii=False))
        pg.close()
    b.close()
