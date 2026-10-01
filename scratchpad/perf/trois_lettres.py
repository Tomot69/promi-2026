# Les trois lettres qui clignotent : mêmes propriétés calculées, deux thèmes ; capture du titre de Partager.
from playwright.sync_api import sync_playwright
M=r"""(sel)=>{const e=document.querySelector(sel); if(!e) return null; const s=getComputedStyle(e), r=e.getBoundingClientRect();
 return {txt:e.textContent, col:s.color, fill:s.webkitTextFillColor, anim:[s.animationName,s.animationDuration,s.animationTimingFunction,s.animationIterationCount].join(' '), op:s.opacity, vis:r.width>0&&s.visibility!=='hidden', x:Math.round(r.left), y:Math.round(r.top)};}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for clair in (False,True):
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("c=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(c?'light':'dark');}", clair)
        th='clair' if clair else 'sombre'
        print(th,'I  PROMI   ',pg.evaluate(M,'.acc-mm i'))
        pg.evaluate("()=>{closeAll();document.getElementById('settingsBtn').click()}"); pg.wait_for_timeout(1200)
        print(th,'S  RÉGLAGES',pg.evaluate(M,'#settingsScreen h1.scr-ti .ti-x'))
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800); pg.evaluate("c=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(c?'light':'dark');}", clair); pg.evaluate("()=>{document.getElementById('shareScreen').classList.add('show');shareRender();}"); pg.wait_for_timeout(1500)
        print(th,'R  PARTAGER',pg.evaluate(M,'#shareScreen h2.scr-t .ti-x'))
        print(th,'   vieil h2',pg.evaluate(M,'#shareScreen .sh-top h2'))
        r=pg.evaluate("()=>{const r=document.getElementById('shcTitre').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
        pg.screenshot(path='scratchpad/perf/partager_%s.png'%th, clip={'x':r[0]-10,'y':r[1]-10,'width':r[2]+20,'height':r[3]+20})
        pg.close()
    b.close()
