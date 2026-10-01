#!/usr/bin/env python3
"""
redteam_pilules.py — LES TROIS PILULES DU + SE LISENT (v115, Tom). Le texte de « Un Cercle », « Un Chiche », « Un Promi » (et leur
sous-titre) doit être à ≥ 4,5 : 1 de son champ, dans les deux thèmes. Mesuré sur les couleurs CALCULÉES (jamais lues dans le code).
Rougi : python3 redteam_pilules.py sauvegardes/app-avant-v115.html   (Chiche 1,42 : 1 · Promi 1,97 : 1)
"""
import sys, os, re, shutil
from playwright.sync_api import sync_playwright
SEUIL=4.5
ARG=next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
if '/' in ARG: shutil.copy(ARG,'zz-pil.html'); ARG='zz-pil.html'
def lum(c):
    r,g,b=[(x/255/12.92 if x/255<=0.04045 else ((x/255+0.055)/1.055)**2.4) for x in c]; return .2126*r+.7152*g+.0722*b
def cr(a,b): la,lb=sorted((lum(a),lum(b)),reverse=True); return (la+.05)/(lb+.05)
rgb=lambda s: tuple(map(int,re.findall(r'\d+',s)[:3]))
ok=True
with sync_playwright() as p:
    b=p.webkit.launch(); pg=b.new_page(viewport={'width':430,'height':932})
    pg.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg.goto('http://127.0.0.1:8752/'+ARG); pg.wait_for_timeout(6500)
    for th in ('light','dark'):
        pg.evaluate("t=>{closeAll();setTheme(t)}",th); pg.wait_for_timeout(300)
        for k,c,cs,bg in pg.evaluate("""()=>[...document.querySelectorAll('#accChoix .acc-pil')].map(e=>[e.dataset.k,getComputedStyle(e).webkitTextFillColor||getComputedStyle(e).color,getComputedStyle(e.querySelector('small')).color,getComputedStyle(e).backgroundColor])"""):
            a=cr(rgb(c),rgb(bg)); s=cr(rgb(cs),rgb(bg)); bon=a>=SEUIL and s>=SEUIL; ok=ok and bon
            print('%-6s [%s]  titre %.2f:1  sous-titre %.2f:1  %s'%(k,th,a,s,'OK' if bon else '✗'))
    b.close()
if ARG=='zz-pil.html': os.remove(ARG)
print('✅ les pilules se lisent' if ok else '❌ une pilule ne se lit pas'); sys.exit(0 if ok else 1)
