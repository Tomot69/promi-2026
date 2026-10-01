# -*- coding: utf-8 -*-
"""LA LUMIÈRE À TRAVERS LA FOURRURE — on mesure l'ALPHA du canevas de la sphère,
   à l'intérieur de la silhouette. Un pixel à alpha bas laisse voir la PAGE :
   c'est exactement ce que Tom voit. On rend aussi l'uniformité (l'écart-type de
   l'alpha par petites tuiles) : une fourrure « uniformément dense » est plate."""
import sys, json
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
JS = r"""()=>{
  const cv=document.getElementById('auBoule'); if(!cv) return null;
  const W=cv.width, g=cv.getContext('2d'), d=g.getImageData(0,0,W,W).data;
  const st=window._aura?_aura.etat():null;
  const CX=W/2, CY=W/2;
  /* le rayon de la boule : on le prend sur l'alpha, en balayant la ligne médiane */
  let R=0; for(let x=W-1;x>CX;x--){ if(d[((CY|0)*W+x)*4+3]>8){ R=x-CX; break; } }
  let dedans=0, trous=[0,0,0,0], somme=0;          /* alpha < 16 · 40 · 80 · 128 */
  const TUI=16, ns=[], nx=Math.floor(W/TUI);
  const acc=new Float64Array(nx*nx), cnt=new Float64Array(nx*nx);
  const r2=(R*0.94)*(R*0.94);                       /* on reste à l'intérieur, pas au limbe */
  for(let y=0;y<W;y++) for(let x=0;x<W;x++){
    const dx=x-CX, dy=y-CY; if(dx*dx+dy*dy>r2) continue;
    const a=d[(y*W+x)*4+3]; dedans++; somme+=a;
    if(a<16) trous[0]++; if(a<40) trous[1]++; if(a<80) trous[2]++; if(a<128) trous[3]++;
    const t=Math.floor(y/TUI)*nx+Math.floor(x/TUI); acc[t]+=a; cnt[t]++;
  }
  for(let i=0;i<nx*nx;i++) if(cnt[i]>TUI*TUI*0.8) ns.push(acc[i]/cnt[i]);
  const moy=ns.reduce((a,b)=>a+b,0)/Math.max(1,ns.length);
  const ec=Math.sqrt(ns.reduce((a,b)=>a+(b-moy)*(b-moy),0)/Math.max(1,ns.length));
  return {W:W, R:Math.round(R), dedans:dedans, alphaMoy:+(somme/dedans).toFixed(1),
    trous16:+(100*trous[0]/dedans).toFixed(2), trous40:+(100*trous[1]/dedans).toFixed(2),
    trous80:+(100*trous[2]/dedans).toFixed(2), trous128:+(100*trous[3]/dedans).toFixed(2),
    tuileMoy:+moy.toFixed(1), tuileEcart:+ec.toFixed(2), tuiles:ns.length,
    palier:st&&st.palier, ms:st&&+st.ms.toFixed(1)};}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(5500)
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(1200)
        pg.evaluate("()=>{try{_aura.fige(true); _aura.vue(2.9,0.32);}catch(e){}}"); pg.wait_for_timeout(1400)
        print(th, json.dumps(pg.evaluate(JS), ensure_ascii=False))
    b.close()
