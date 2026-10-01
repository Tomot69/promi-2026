# -*- coding: utf-8 -*-
"""LES TITRES DE PAGE — on mesure L'ENCRE RENDUE, pas la taille déclarée : la hauteur de
   capitale et la largeur du mot, police chargée. Et on relève la dernière lettre colorée
   et son animation, écran par écran."""
from playwright.sync_api import sync_playwright
ECR=[('accueil',"()=>{closeAll();}"),
     ('fil',"()=>{closeAll(); document.getElementById('filBtn').click();}"),
     ('index',"()=>{closeAll(); document.getElementById('indexBtn').click();}"),
     ('aura',"()=>{closeAll(); document.getElementById('souffleBtn').click();}"),
     ('studio',"()=>{closeAll(); document.getElementById('studioBtn').click();}"),
     ('reglages',"()=>{closeAll(); const b=document.getElementById('settingsBtn'); b&&b.click();}"),
     ('partage',"()=>{closeAll(); const b=document.getElementById('shareBtn'); if(b)b.click();}")]
JS=r"""()=>{const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const vus=new Set(), out=[];
  document.querySelectorAll('.scr-t, .scr-ti, .enh-t, .enh h1, .enh h2, .acc-plat h1, .acc-plat h2').forEach(e=>{
    const r=e.getBoundingClientRect(); if(r.width<3||r.height<3) return;
    if((r.top-dv.top)/s > 300) return;               /* seulement le titre en tête d'écran */
    const t=(e.textContent||'').trim().replace(/\s+/g,' ').slice(0,20);
    if(vus.has(t)) return; vus.add(t);
    const cs=getComputedStyle(e);
    /* l'encre : on mesure la hauteur de capitale RENDUE par une boîte de mesure */
    const m=document.createElement('span');
    m.style.cssText='position:absolute;visibility:hidden;white-space:nowrap;font-family:'+cs.fontFamily
      +';font-weight:'+cs.fontWeight+';font-size:'+cs.fontSize+';letter-spacing:'+cs.letterSpacing;
    m.textContent='H'; document.body.appendChild(m);
    const cap=m.getBoundingClientRect().height; m.remove();
    const x=[...e.querySelectorAll('.ti-x, .uvi, .uvi2')].map(k=>({cl:String(k.className),
      txt:k.textContent, col:getComputedStyle(k).color,
      anim:getComputedStyle(k).animationName+' '+getComputedStyle(k).animationDuration}));
    out.push({t:t, fs:cs.fontSize, ff:cs.fontFamily.split(',')[0], cap:+(cap/s).toFixed(1),
      w:+(r.width/s).toFixed(1), h:+(r.height/s).toFixed(1), derniere:x});});
  return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for nom,js in ECR:
        pg.evaluate(js); pg.wait_for_timeout(2200)
        for o in pg.evaluate(JS):
            print('%-9s %-18s %-7s %-11s cap %-6s' % (nom, o['t'], o['fs'], o['ff'], o['cap']), o['derniere'])
    b.close()
