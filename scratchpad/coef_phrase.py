# -*- coding: utf-8 -*-
"""LE COEFFICIENT 0,53 DU §2.8 A ÉTÉ RELEVÉ SUR LA POLICE DE LA PLANCHE.
   On le remesure sur la police que la phrase porte AUJOURD'HUI : largeur rendue
   d'un mot ÷ (nombre de caractères × taille). S'il est plus petit, l'estimation
   surévalue — et la phrase sort plus petite qu'elle ne devrait."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{const t=document.querySelector('.pp-choix .tile, #ppChoix .tile'); if(t) t.click();}")
    pg.wait_for_timeout(2500)
    print(pg.evaluate(r"""()=>{
      const txt=document.querySelector('.ph-txt'); if(!txt) return 'pas de phrase';
      const cs=getComputedStyle(txt);
      const c=document.createElement('canvas').getContext('2d');
      const mots=['reprendre la guitare','Je me promets','courir dimanche matin','rappeler maman','de','finir le dossier avant jeudi'];
      const out={};
      for(const fs of [29,36]){
        c.font=cs.fontWeight+' '+fs+'px '+cs.fontFamily;
        out[fs]=mots.map(m=>+ (c.measureText(m).width/(m.length*fs)).toFixed(4));
      }
      return {police:cs.fontFamily, poids:cs.fontWeight, taille:cs.fontSize,
              coef:out, phrase:txt.textContent.trim().slice(0,60)};}"""))
    b.close()
