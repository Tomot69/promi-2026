# Les trois lettres qui clignotent : le i de PROMI (accueil), le S de RÉGLAGES, le R de PARTAGER — mesurées au rendu.
import sys
from playwright.sync_api import sync_playwright
PROBE=r"""(sel)=>{ const cands=[...document.querySelectorAll(sel)].filter(e=>{const r=e.getBoundingClientRect(); const cs=getComputedStyle(e); return r.width>0&&r.height>0&&cs.visibility!=='hidden'&&cs.display!=='none';});
 const e=cands[0]; if(!e) return null; const cs=getComputedStyle(e), r=e.getBoundingClientRect();
 const an=e.getAnimations?e.getAnimations().map(a=>{const t=a.effect&&a.effect.getTiming?a.effect.getTiming():{}; const kf=a.effect&&a.effect.getKeyframes?a.effect.getKeyframes().map(k=>k.offset+':'+(k.opacity||'')).join(' '):''; return (a.animationName||'')+' '+t.duration+'ms '+(t.easing||'')+' ['+kf+']';}):[];
 return {txt:e.textContent.trim().slice(0,3), color:cs.color, fill:cs.webkitTextFillColor, shadow:cs.textShadow, fs:cs.fontSize, ff:cs.fontFamily.split(',')[0], anim:an, rect:[r.left,r.top,r.width,r.height].map(Math.round)}; }"""
ECR=[('accueil i', "closeAll()", '#accPlat .acc-mm i, .acc-mm i'),
     ('réglages S', "closeAll(); (document.getElementById('settingsBtn')||document.querySelector('#accPlat [data-act=reglages]')||{click(){}}).click()", '#settingsScreen h1 .ti-x, #settingsScreen .blink'),
     ('partager R', "closeAll(); openShare()", '#shareScreen h2.scr-t .ti-x, #shareScreen .blink')]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ['dark','light']:
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
        for nom,js,sel in ECR:
            pg.evaluate("()=>{"+js+"}"); pg.wait_for_timeout(1500)
            r=pg.evaluate(PROBE, sel); print(th, nom, r)
            if r:
                x,y,w,h=r['rect']; pg.screenshot(path='sauvegardes/v47/l_%s_%s.png'%(th,nom.split()[1]), clip={'x':x-6,'y':y-6,'width':w+12,'height':h+12})
    b.close()
