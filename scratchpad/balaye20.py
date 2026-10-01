# -*- coding: utf-8 -*-
"""LE GARDE-FOU, MESURÉ SUR LES VINGT ET UNE PALETTES — sur l'IMAGE rendue, vue figée,
   sans les îles (on mesure LE SOL). Seuil du §3 : 42."""
import sys
from playwright.sync_api import sync_playwright
from PIL import Image
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
SEUIL=42.0
def lum(c): return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def moyenne(p):
    im=Image.open(p).convert('RGB'); W,H=im.size; px=im.load()
    fond=px[3,3]; s=[0,0,0]; n=0
    for y in range(0,H,3):
        for x in range(0,W,3):
            c=px[x,y]
            if abs(c[0]-fond[0])+abs(c[1]-fond[1])+abs(c[2]-fond[2])>26:
                s[0]+=c[0];s[1]+=c[1];s[2]+=c[2];n+=1
    return (tuple(v/max(1,n) for v in s), fond) if n else (None,fond)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6300)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    PALS=pg.evaluate("()=>Object.keys(window.Toile.palettes())")
    print('%d palettes · seuil %d\n'%(len(PALS),SEUIL))
    ko=0; res={}
    for theme in ('sombre','clair'):
        pg.evaluate("(t)=>{setTheme(t==='clair'?'light':'dark');}", theme); pg.wait_for_timeout(500)
        print('══ %s ══'%theme)
        print('%-16s %-22s %-11s %s'%('palette','sol rendu (moyen)','boule↔page','seuil 42'))
        for k in PALS:
            pg.evaluate("(x)=>{window.Toile.setPalette(x);}", k); pg.wait_for_timeout(1300)
            pg.evaluate("()=>{try{closeAll();}catch(e){}}"); pg.wait_for_timeout(450)
            pg.evaluate("()=>{document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(4000)
            pg.evaluate("()=>{try{window._aura.fige(true);window._aura.vue(0,0);window._aura.sansIles(true);}catch(e){}}")
            pg.wait_for_timeout(1500)
            pg.locator('#auBoule').screenshot(path='cap/b20.png')
            pg.evaluate("()=>{try{window._aura.sansIles(false);}catch(e){}}")
            m,_=moyenne('cap/b20.png')
            if not m: print('%-16s —'%k); continue
            pgc=pg.evaluate("()=>{var d=document.getElementById('device');return getComputedStyle(d).backgroundColor;}")
            rgbp=[int(x) for x in pgc.replace('rgb(','').replace(')','').split(',')[:3]]
            e=abs(lum(m)-lum(rgbp))
            sol=pg.evaluate("()=>{try{return window._aura.verifie?null:null}catch(e){return null}}")
            bon = e>=SEUIL
            if not bon: ko+=1
            res[(theme,k)]=e
            print('%-16s (%3d,%3d,%3d)  page %-4.0f  %-11.1f %s'%(k,int(m[0]),int(m[1]),int(m[2]),lum(rgbp),e,'✓' if bon else '✗'))
        print()
    b.close()
print('%d palette(s) sous le seuil sur %d mesures.'%(ko,len(res)))
if res:
    mn=min(res.items(), key=lambda kv:kv[1]); mx=max(res.items(), key=lambda kv:kv[1])
    print('le plus faible : %s %s → %.1f   ·   le plus fort : %s %s → %.1f'%(mn[0][1],mn[0][0],mn[1],mx[0][1],mx[0][0],mx[1]))
