# Relevé : dans chaque titre d'écran, les lettres dont la couleur ou l'animation diffèrent du reste du mot.
import json
from playwright.sync_api import sync_playwright
PORTES = {'accueil':"()=>closeAll()", 'reglages':"()=>{closeAll();document.getElementById('settingsScreen').classList.add('show')}",
  'partage':"()=>{closeAll(); (window.openShare||function(){document.getElementById('shareBtn').click()})()}",
  'index':"()=>{closeAll(); document.querySelector('[data-open=index],#indexBtn,#ixBtn')&&document.querySelector('[data-open=index],#indexBtn,#ixBtn').click()}",
  'fil':"()=>{closeAll(); var b=document.getElementById('filBtn'); b&&b.click()}",
  'studio':"()=>{closeAll(); var b=document.getElementById('studioBtn')||document.querySelector('[data-studio]'); b&&b.click()}",
  'aura':"()=>{closeAll(); var b=document.getElementById('auraBtn'); b&&b.click()}"}
REL = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(); const out=[];
 const tit=[...document.querySelectorAll('h1,h2,.scr-ti,.scr-t,.acc-mm,#shcTitre .t,.cs-mark,.t')].filter(e=>{const r=e.getBoundingClientRect(); return r.width>0&&r.top>=dv.top-5&&r.bottom<dv.top+dv.height*0.2&&r.left>=dv.left-5&&r.right<=dv.right+5 && getComputedStyle(e).visibility!=='hidden'});
 for(const t of tit){ const cs=getComputedStyle(t); const kids=[...t.querySelectorAll('*')].filter(k=>k.textContent.trim().length===1||k.tagName==='I');
   out.push({titre:t.textContent.trim().slice(0,24), cls:t.className, col:cs.color, lettres:kids.map(k=>{const s=getComputedStyle(k); return {txt:k.textContent.trim(), tag:k.tagName, cls:String(k.className), col:s.color, fill:s.webkitTextFillColor, anim:s.animationName+' '+s.animationDuration+' '+s.animationTimingFunction, op:s.opacity}})}); }
 return out; }"""
with __import__('playwright.sync_api').sync_api.sync_playwright() as p:
    b=p.chromium.launch()
    for clair in (False,True):
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("c=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} document.getElementById('device').classList.toggle('light',c);}", clair)
        for n,js in PORTES.items():
            try: pg.evaluate(js)
            except Exception as e: print(n,'porte KO',e); continue
            pg.wait_for_timeout(1400)
            for t in pg.evaluate(REL):
                print('clair' if clair else 'sombre', n, '|', t['titre'], '|', t['col'], '|', json.dumps(t['lettres'],ensure_ascii=False))
        pg.close()
    b.close()
