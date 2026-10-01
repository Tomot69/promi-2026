# -*- coding: utf-8 -*-
"""L'AIR AUTOUR DE LA PHRASE ET DE LA LÉGENDE, AUX BOÎTES ET À L'ENCRE.
   La boule : son bas VISIBLE (l'alpha du canevas), pas sa boîte."""
import base64, json, sys
from playwright.sync_api import sync_playwright
GAP = open('releve-aura.py',encoding='utf-8').read().split('ENCRE_GAP = r"""')[1].split('"""')[0]
BOITES = r"""()=>{const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();return {y:(r.top-dv.top)/s,b:(r.bottom-dv.top)/s,h:r.height/s};};
  const q=x=>document.querySelector('#auraScreen '+x);
  const cv=document.getElementById('auBoule'), rb=cv.getBoundingClientRect();
  /* le bas VISIBLE de la boule, lu sur l'alpha */
  const W=cv.width, g=cv.getContext('2d'), d=g.getImageData(0,0,W,W).data; let bas=0;
  for(let y=W-1;y>0;y--){ let n=0; for(let x=0;x<W;x+=3) if(d[(y*W+x)*4+3]>8){n++; if(n>2)break;} if(n>2){bas=y;break;} }
  return {bouleBas:(rb.top-dv.top)/s + bas/(W/(rb.width/s)) / (W/(rb.width/s)) *0 + (bas*(rb.height/W))/s,
    mot:R(q('.au-mot')), nx:R(q('.au-nx')), lg:R(q('.au-lg')), h3:R(q('.au-mo h3')),
    lgFs:getComputedStyle(q('.au-lg')).fontSize, motFs:getComputedStyle(q('.au-mot')).fontSize};}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(5500)
    for th,fond in (('dark',[32,25,8]),('light',[247,240,222])):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(900)
        pg.evaluate("()=>{try{_aura.fige(true);_aura.vue(2.9,0.32);}catch(e){}}"); pg.wait_for_timeout(1200)
        m=pg.evaluate(BOITES)
        u='data:image/png;base64,'+base64.b64encode(pg.query_selector('#device').screenshot()).decode()
        # à l'encre : au-dessus de la phrase (entre la boule et elle) et en dessous (jusqu'aux disques)
        ha=pg.evaluate(GAP,[u,fond,(m['bouleBas']+m['mot']['y'])/2.0])
        hb=pg.evaluate(GAP,[u,fond,(m['mot']['b']+m['nx']['y'])/2.0])
        la=pg.evaluate(GAP,[u,fond,(m['nx']['b']+m['lg']['y'])/2.0])
        lb=pg.evaluate(GAP,[u,fond,(m['lg']['b']+m['h3']['y'])/2.0])
        print('%-6s phrase %s légende %s | boîtes : boule bas %.1f · mot %.1f→%.1f · nx %.1f · lg %.1f→%.1f · h3 %.1f'
              % (th, (round(ha,1),round(hb,1)), (round(la,1),round(lb,1)),
                 m['bouleBas'], m['mot']['y'], m['mot']['b'], m['nx']['y'], m['lg']['y'], m['lg']['b'], m['h3']['y']))
        print('       tailles : commentaire %s · légende %s' % (m['motFs'], m['lgFs']))
    b.close()
