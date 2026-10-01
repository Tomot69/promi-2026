# -*- coding: utf-8 -*-
"""LES TROUS DANS LA FOURRURE — mesurés sur l'image rendue, vue figée, sans les îles.
   Un trou = un pixel du cœur nettement plus SOMBRE que la moyenne locale : c'est la peau
   qu'on voit entre les poils. On rend aussi la médiane d'image, pour savoir ce qu'on paie."""
import sys, statistics
from playwright.sync_api import sync_playwright
from PIL import Image
sys.path.insert(0,'.')
from col import lab
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
NOM = sys.argv[2] if len(sys.argv)>2 else 'velu'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6300)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(5200)
    pg.evaluate("()=>{try{window._aura.fige(true);window._aura.vue(0,0);window._aura.sansIles(true);}catch(e){}}")
    pg.wait_for_timeout(1800)
    et=pg.evaluate("()=>{try{var e=window._aura.etat();return {palier:e.palier,ms:e.ms};}catch(x){return{}}}")
    pg.locator('#auBoule').screenshot(path='cap/%s.png'%NOM)
    b.close()
im=Image.open('cap/%s.png'%NOM).convert('RGB'); W,H=im.size; px=im.load()
pts=[(x,y) for y in range(H) for x in range(W) if px[x,y][3-3]+px[x,y][1]+px[x,y][2]>0 and im.getpixel((x,y))!=(0,0,0)]
xs=[q[0] for q in pts]; ys=[q[1] for q in pts]
cx,cy=(min(xs)+max(xs))/2,(min(ys)+max(ys))/2; R=(max(xs)-min(xs))/2
L={}
for x,y in pts:
    if (x-cx)**2+(y-cy)**2 < (0.78*R)**2: L[(x,y)]=lab(im.getpixel((x,y)))[0]
vals=list(L.values()); moy=sum(vals)/len(vals)
# ⚑ LA GRANDEUR QUI A LA FORME DU DÉFAUT (§7) : LE TAUX DE COUVERTURE.
# Un « trou » n'est pas un pixel aberrant, c'est de la PEAU qu'on voit entre les poils.
# On prend la peau au 10e centile de clarté, le poil au 90e, et on compte la part de la
# surface qui est du côté du POIL. Plus la fourrure couvre, plus ce taux monte.
vals.sort()
peau = vals[int(0.10*len(vals))]
poil = vals[int(0.90*len(vals))]
mid  = (peau+poil)/2
couv = sum(1 for v in vals if v>mid)/len(vals)
import statistics as st
print('%s · palier %s · médiane %s ms · %d px de cœur'%(NOM, et.get('palier'), (('%.1f'%et['ms']) if et.get('ms') else '?'), len(L)))
print('   peau (10e centile)        L* %.1f'%peau)
print('   poil (90e centile)        L* %.1f'%poil)
print('   écart peau → poil         %.1f de L*'%(poil-peau))
print('   COUVERTURE (part du poil) %.1f %%'%(100*couv))
print('   grain local (σ)           %.2f de L*'%st.pstdev(vals))
