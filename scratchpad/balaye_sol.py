# -*- coding: utf-8 -*-
"""CE QUE LA DÉCISION COÛTE — le sol suivant la palette, on rebalaye les deux cotes
   que Q210 avait calibrées sur le bleu : l'écart boule ↔ page, et la lisibilité des îles.
   On lit la MESURE de l'app elle-même (celle que le juge emploie), à vue figée."""
import sys, json
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
PALS = ['signal','primesautier','candide','irascible','allegre','taciturne','fielleux','minaudier']
ECART = {'sombre':76.0, 'clair':116.0}   # les cotes décidées (Q210), ±8
MES = r"""()=>{
 var c=document.getElementById('auBoule'); if(!c) return null;
 var g=c.getContext('2d'), W=c.width, H=c.height, d=g.getImageData(0,0,W,H).data;
 /* la couleur de la page, prise hors de la boule */
 function px(x,y){var i=((y|0)*W+(x|0))*4; return [d[i],d[i+1],d[i+2],d[i+3]];}
 var cx=W/2, cy=H/2, R=Math.min(W,H)/2;
 var s=[0,0,0], n=0;
 for(var y=0;y<H;y+=3) for(var x=0;x<W;x+=3){
   var p=px(x,y); if(p[3]<10) continue;
   var dx=x-cx, dy=y-cy; if(dx*dx+dy*dy > (0.72*R)*(0.72*R)) continue;
   s[0]+=p[0];s[1]+=p[1];s[2]+=p[2];n++; }
 if(!n) return null;
 return {sol:[s[0]/n,s[1]/n,s[2]/n]};}"""
PAGE = r"""()=>{var e=document.getElementById('auraScreen'); return getComputedStyle(e).backgroundColor;}"""
def lum(c): return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932})
    pg.goto(URL); pg.wait_for_timeout(6300)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print('%-14s %-9s %-22s %-9s %-9s %s'%('palette','thème','sol moyen (rgb)','boule↔page','décidé','plancher des îles'))
    print('-'*96)
    for theme in ('sombre','clair'):
        pg.evaluate("(t)=>{setTheme(t==='clair'?'light':'dark');}", theme); pg.wait_for_timeout(600)
        for k in PALS:
            pg.evaluate("(p)=>{window.Toile.setPalette(p);}", k); pg.wait_for_timeout(1500)
            pg.evaluate("()=>{try{closeAll();}catch(e){}}"); pg.wait_for_timeout(500)
            pg.evaluate("()=>{document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(4200)
            pg.evaluate("()=>{try{window._aura.fige(true);window._aura.vue(0,0);}catch(e){}}"); pg.wait_for_timeout(700)
            m=pg.evaluate(MES); pgc=pg.evaluate(PAGE)
            v=None
            try: v=pg.evaluate("()=>{var r=window._aura.verifie&&window._aura.verifie(); return r?{min:r.min,med:r.med,boule:r.boule,contour:r.contour}:null;}")
            except Exception: pass
            rgbp=[int(x) for x in pgc.replace('rgb(','').replace(')','').split(',')[:3]]
            eb = abs(lum(m['sol'])-lum(rgbp)) if m else None
            dec=ECART[theme]
            ok = (abs(eb-dec)<=8) if eb is not None else False
            print('%-14s %-9s %-22s %-9s %-9s %s'%(k,theme,
                  '(%3d,%3d,%3d)'%tuple(int(x) for x in m['sol']) if m else '—',
                  ('%.1f'%eb) if eb is not None else '—', ('%.0f ±8 %s'%(dec,'✓' if ok else '✗')),
                  ('min %.1f · méd %.1f'%(v['min'],v['med'])) if v and v.get('min') is not None else '—'))
    b.close()
